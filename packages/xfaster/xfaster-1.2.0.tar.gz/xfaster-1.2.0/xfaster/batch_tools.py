import os
import stat
import shutil
import subprocess as sp
import tempfile
import re
import datetime as dt
from warnings import warn
import numpy as np
import argparse as ap

__all__ = [
    "get_job_logfile",
    "get_job_id",
    "batch_sub",
    "batch_group",
    "JobArgumentParser",
]


def get_job_logfile():
    """
    Generate a path to use for the output log, based on job environment

    Returns
    -------
    logfile : str
        Path to log file.
    """
    if os.getenv("SLURM_SUBMIT_DIR"):
        workdir = os.getenv("SLURM_SUBMIT_DIR")
        jobname = os.getenv("SLURM_JOB_NAME")
        jobid = os.getenv("SLURM_JOB_ID").split(".", 1)[0]
        if jobname == "bash":
            logfile = None
        else:
            logfile = os.path.join(workdir, "{}-{}.log".format(jobname, jobid))
    else:
        logfile = None
    return logfile


def get_job_id():
    """
    Get the current job ID, based on job environment.

    Returns
    -------
    jobid: str
        Job ID.
    """
    if os.getenv("SLURM_SUBMIT_DIR"):
        jobid = os.getenv("SLURM_JOB_ID").split(".", 1)[0]
    else:
        jobid = None

    return jobid


def format_time(t):
    """
    Format a time to string for use by qsub.

    Arguments
    ---------
    t : datetime.timedelta object or float
        The time for the job.
        If floating point, will be interpreted in hours

    Returns
    -------
    time : str
        Time in the format expected by scheduler.
    """
    if isinstance(t, str):
        m = re.match("([0-9]+):([0-9]{2}):([0-9]{2})", t)
        if not m:
            raise ValueError("unable to parse qsub time string")
        hh, mm, ss = map(int, m.groups())
        t = dt.timedelta(hours=hh, minutes=mm, seconds=ss)
    if not isinstance(t, dt.timedelta):
        t = dt.timedelta(hours=t)
    if t <= dt.timedelta(0):
        raise ValueError("qsub time must be positive")
    hours, rem = divmod(t.seconds + t.days * 86400, 3600)
    minutes, seconds = divmod(rem, 60)
    return "{:d}:{:02d}:{:02d}".format(hours, minutes, seconds)


def batch_sub(
    cmd,
    name=None,
    mem=None,
    nodes=None,
    node_list=None,
    ppn=None,
    cput=None,
    wallt=None,
    output=None,
    error=None,
    queue=None,
    dep_afterok=None,
    workdir=None,
    batch_args=[],
    omp_threads=None,
    env_script=None,
    env=None,
    nice=None,
    echo=True,
    delete=True,
    submit=True,
    scheduler="slurm",
    debug=False,
    exclude=None,
    verbose=False,
    srun=None,
    srun_args="",
):
    """
    Create and submit a SLURM job.

    Arguments
    ---------
    cmd : string or list of strings
        A command sequence to run via SLURM.
        The command will be inserted into a qsub submission script
        with all of the options specified in the remaining arguments.
    name : string, optional
        Name of the job.
    mem : float or string, optional
        Amount of memory to request for the job. float values in GB.
        Or pass a string (eg '4gb') to use directly.
    nodes : int or string, optional
        Number of nodes to use in job
        If using SLURM and a string, will overwrite node_list if None
    node_list : string or list of strings
        List of nodes that can be used for job. SLURM-only.
    ppn : int, optional
        Number of processes per node
    cput : string or float or datetime.timedelta, optional
        Amount of CPU time requested.
        String values should be in the format HH:MM:SS, e.g. '10:00:00'.
        Numerical values are interpreted as a number of hours.
    wallt : string or float or datetime.timedelta, optional
        Amount of wall clock time requested.
        String values should be in the format HH:MM:SS, e.g. '10:00:00'.
        Numerical values are interpreted as a number of hours.
    output : string, optional
        Scheduler standard output filename.
    error : string, optional
        Scheduler error output filename.
    queue : string, optional
        The name of the queue to which to submit jobs
    dep_afterok : string or list of strings
        Dependency. Job ID (or IDs) on which to wait for successful completion,
        before starting this job
    workdir : string, optional
        Directory from where the script will be submitted.
        This is where the output and error files will be created
        by default.  Default: current directory.
    batch_args : string or list of strings, optional
        Any additional arguments to pass to slurm.
    omp_threads : int, optional
        Number of OpenMP threads to use per process
    env_script : string, optional
        Path to script to source during job script preamble
        For loading modules, setting environment variables, etc
    env : dict, optional
        Dictionary of environment variables to set in job script
    nice : int, optional
        Adjust scheduling priority (SLURM only).
        Unprivileged users can only increase niceness (lower job priority).
    echo : bool, optional
        Whether to use bash "set -x" in job script to echo commands to stdout.
    delete : bool, optional
        If True, delete the submit script upon job submission.
    submit : bool, optional
        If True (default) submit the job script once create. Will override the
        default option when False, to keep the script
    scheduler : string, optional
        Which scheduler system to write a script for. Only "slurm" is currently
        supported.
    debug : bool, optional
        If True, print the contents of the job script to stdout for debugging.
    exclude : string or list of strings
        List of nodes that will be excluded for job. SLURM-only.
    verbose : bool, optional
        Print the working directory, and the job ID if submitted successfully.
    srun : bool, optional
        Invoke jobs with srun.  Defaults to True when using SLURM, set to False
        to disable.  Use `srun_args` to pass extra arguments to this command.
    srun_args : string, optional
        If `srun=True`, additional arguments to pass to the `srun` command.

    Returns
    -------
    jobid : string
        The ID of the submitted job.

    Example
    -------
    >>> jobid = batch_sub("echo Hello", name="testing", nodes="1:ppn=1",
    ... cput='1:00:00', mem='1gb')
    >>> print(jobid)
    221114.feynman.princeton.edu
    >>> print(open('testing.o221114','r').read())
    Hello
    """

    if isinstance(cmd, list):
        cmd = " ".join(cmd)
    scheduler = scheduler.lower()
    if mem is not None and not isinstance(mem, str):
        if mem < 0:
            mem = None
        elif scheduler == "slurm":
            mem = "{:d}".format(int(np.ceil(mem * 1024.0)))
    if isinstance(dep_afterok, str):
        dep_afterok = [dep_afterok]
    if isinstance(batch_args, str):
        batch_args = batch_args.split()
    if not debug and not submit:
        delete = False
    try:
        nodes = int(nodes)
    except ValueError:
        # nodes is a string that's not convertible to int
        if scheduler == "slurm" and node_list is None:
            node_list = nodes
            nodes = 1
    if srun is None:
        srun = scheduler == "slurm"

    job_script = ["#!/usr/bin/env bash"]

    # TODO can maybe replace manual option with some automatic detection
    if scheduler == "slurm":
        # create slurm header
        if name:
            job_script += ["#SBATCH --job-name={:s}".format(name)]
        if mem:
            job_script += ["#SBATCH --mem={:s}".format(mem)]
        if nodes:
            job_script += ["#SBATCH --nodes={}".format(nodes)]
        if node_list is not None:
            if len(node_list) > 1 and not isinstance(node_list, str):
                node_list = ",".join(node_list)
            job_script += ["#SBATCH --nodelist={}".format(node_list)]
        if exclude is not None:
            if len(exclude) > 1 and not isinstance(exclude, str):
                exclude = ",".join(exclude)
            elif len(exclude) == 1 and not isinstance(exclude, str):
                exclude = exclude[0]
            job_script += ["#SBATCH --exclude={}".format(exclude)]
        if ppn:
            job_script += ["#SBATCH --ntasks-per-node={}".format(ppn)]
        if omp_threads:
            job_script += ["#SBATCH --cpus-per-task={}".format(omp_threads)]
        if cput:
            if wallt is None:
                warn("Using CPU time as wall time for slurm")
                job_script += ["#SBATCH --time={:s}".format(format_time(cput))]
            else:
                warn("Ignoring CPU time for slurm, using wall time only")
        if wallt:
            job_script += ["#SBATCH --time={:s}".format(format_time(wallt))]
        if nice is not None:
            job_script += ["#SBATCH --nice={}".format(nice)]
        if output:
            job_script += ["#SBATCH --output={:s}".format(output)]
        if error:
            job_script += ["#SBATCH --error={:s}".format(error)]
        if queue:
            job_script += ["#SBATCH --partition={:s}".format(queue)]
        if dep_afterok:
            job_script += [
                "#SBATCH --dependency=afterok:{}".format(":".join(dep_afterok))
            ]

    # create job script preamble
    if echo:
        job_script += ["set -x"]
    if env_script:
        if not os.path.exists(env_script):
            raise ValueError("Could not find environment script: {}".format(env_script))
        job_script += ["source {}".format(env_script)]
    if env:
        for k, v in env.items():
            job_script += ["export {}={}".format(k, v)]
    if scheduler == "slurm":
        job_script += ["cd $SLURM_SUBMIT_DIR"]
    if omp_threads:
        job_script += ["export OMP_NUM_THREADS={}".format(omp_threads)]
        if srun:
            job_script += ["export SRUN_CPUS_PER_TASK={}".format(omp_threads)]

    # finally, add the command string to script
    cmd_prefix = None
    if srun:
        if scheduler != "slurm":
            raise ValueError('srun=True requires scheduler="slurm"')
        if not cmd.startswith("srun"):
            cmd_prefix = "srun {:s} ".format(srun_args)
    if cmd_prefix is not None:
        cmd = "\n".join(
            [
                (cmd_prefix + line) if line != "wait" else line
                for line in cmd.split("\n")
            ]
        )
    job_script += [cmd]
    job_script = "\n".join(job_script)

    # create and navigate to workdir
    cwd = os.getcwd()
    if workdir is None:
        workdir = cwd
        pwd = workdir
    else:
        pwd = cwd
    if not os.path.exists(workdir):
        os.makedirs(workdir)
    os.chdir(workdir)
    if verbose:
        print(workdir)

    if debug:
        print(job_script)

    # create and submit script
    prefix = "{}_".format(name if name else "job")
    if scheduler == "slurm":
        suffix = ".slurm"
    with tempfile.NamedTemporaryFile(
        prefix=prefix, suffix=suffix, mode="w", dir=workdir, delete=delete
    ) as f:
        f.write(job_script)
        f.flush()
        os.chmod(f.name, stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR | stat.S_IRGRP)
        if submit:
            if scheduler == "slurm":
                ret = sp.check_output(["sbatch"] + batch_args + [f.name]).decode(
                    "UTF-8"
                )
                jobid = ret.split("\n")[0].split()[-1]  # parse jobid
                if not re.match("[0-9]+", jobid):
                    raise RuntimeError("slurm error:\n{}".format(ret))
        elif debug:
            jobid = "314159test"
        if submit and not delete:
            new = "{}.q{}".format(
                name if name else os.path.basename(f.name), jobid.split(".", 1)[0]
            )
            new = os.path.join(os.path.dirname(f.name), new)
            shutil.copy2(f.name, new)
            fname = f.name

    if submit and not delete:
        os.remove(fname)

    os.chdir(pwd)

    if submit or debug:
        if verbose:
            print("Job ID: {}\n".format(jobid))
        return jobid
    else:
        return None


def batch_group(cmds, group_by=1, serial=False, *args, **kwargs):
    """
    Create and submit SLURM job scripts for a group of similar commands. The
    commands can be grouped together into larger single jobs that run them in
    parallel on multiple processors on a node.

    Keyword arguments are passed on to the batch_sub function.
    These will be applied to EACH job. For example, using ``nodes="1:ppn=8"``
    with ``group_by=8`` and 16 elements in cmds will result in 2 jobs, each using
    8 processors on 1 node.

    Arguments
    ---------
    cmds : list
        The commands to run.
        The commands themselves should be a string, or a list of tokens, as
        per the ``batch_sub`` function.
    group_by : int, optional
        The number of commands to group together into a single job. Does not
        balance well when ``len(cmds)%group_by != 0``
        Eg. on scinet use ``group_by=8`` to efficiently use whole nodes.
    serial : bool, optional
        Set to ``True`` to run cmds sequentially, rather than starting them all
        in parallel. This will also work with OpenMP parallel jobs.
    args, kwargs : arb
        Additional arguments passed to batch_sub

    Returns
    -------
    jobids : list of strings
        List of job IDs used by the scheduler
    """
    grouped = []
    jobids = []

    name = kwargs.pop("name", None)

    for i, cmd in enumerate(cmds):
        if not isinstance(cmd, str):
            cmd = " ".join(cmd)
        if group_by > 1 and not serial:
            cmd = "{} &".format(cmd)
        grouped += [cmd]
        if len(grouped) == group_by or i + 1 == len(cmds):
            # group is full, or last command. write out a job
            if group_by > 1:
                grouped += ["wait"]
            if name:
                if (i + 1 == len(cmds)) and (len(jobids) == 0):
                    # all jobs in a single group
                    kwargs["name"] = name
                else:
                    kwargs["name"] = "{}_grp{}".format(name, len(jobids) + 1)
            jobid = batch_sub("\n".join(grouped), *args, **kwargs)
            if jobid:
                jobids.append(jobid)
            grouped = []

    if jobids:
        return jobids
    else:
        return None


class JobArgumentParser(object):
    def __init__(
        self, name=None, mem=None, time=None, workdir=None, outkey=None, **kwargs
    ):
        """
        Standardized way to add job submission arguments to a script.

        Keyword arguments are used to fix values for parameters not needed by a
        script. The corresponding command line arguments will not be added. See
        the ``.opt_list`` attribute for a complete list.

        Arguments
        ---------
        name : string
            This will be the name of the jobs.
        mem : float
            Memory per job in GB. Will scale up for grouped jobs.
        time : float
            Time per job in hours.
        workdir : string
            Fixed location to use as working directory (ie place for job
            scripts and logs).
        outkey : string
            Alternative to ``workdir``. The key/name of an argument added to
            normal argparse that indicates output path. A "logs" subfolder
            of that path will be used as ``workdir``.

        Example
        -------
        >>> jp = sa.batch.JobArgumentParser("some_serial_job", mem=4, time=1.5,
                    omp_threads=1, workdir="/path/to/logs")
        >>> AP = argparse.ArgumentParser(description="Do some job")
        >>> AP.add_argument(...)  # other non-job arguments
        >>> jp.add_arguments(AP)
        >>> args = AP.parse_args()
        >>> jp.set_job_opts(args)
        >>> jobs = [...]  # list of commands to run in jobs
        >>> jp.submit(jobs)
        """
        self.name = name
        self.mem = float(mem) if mem is not None else None
        self.time = float(time)
        self.workdir = workdir
        self.outkey = outkey
        self.fixed_opts = kwargs
        self.opt_list = self._opt_list()
        bad_opts = [k for k in kwargs if k not in self.opt_list]
        if bad_opts:
            raise ValueError("Unknown options: {}".format(bad_opts))

    def _opt_list(self):
        """
        All options supported by this class.
        Initialize from a function to conceivably allow subclass overrides.
        """
        from collections import OrderedDict

        return OrderedDict(
            [
                ("queue", dict(default=None, help="Queue to which to submit jobs")),
                (
                    "nodes",
                    dict(
                        type=str,
                        default=1,
                        help="Name or number of nodes to submit job to",
                    ),
                ),
                (
                    "ppn",
                    dict(
                        type=int,
                        default=None,
                        help="Processes per node. Default based on group and omp_threads",
                    ),
                ),
                (
                    "exclude",
                    dict(
                        type=str,
                        default=None,
                        nargs="+",
                        help="Nodes to exclude from jobs",
                    ),
                ),
                (
                    "use_cput",
                    dict(
                        action="store_true",
                        default=False,
                        help="Use CPU time rather than wall clock for jobs",
                    ),
                ),
                (
                    "cpu_speed",
                    dict(
                        type=float,
                        default=1.0,
                        help="Relative CPU speed factor, to adjust run times",
                    ),
                ),
                (
                    "nice",
                    dict(
                        type=int,
                        default=None,
                        help="Adjust job priority. SLURM only",
                    ),
                ),
                (
                    "env_script",
                    dict(
                        default=None,
                        help="Script to source in jobs to set up environment",
                    ),
                ),
                (
                    "test",
                    dict(
                        action="store_true",
                        default=False,
                        help="Print options for debugging",
                    ),
                ),
                (
                    "omp_threads",
                    dict(
                        type=int, default=1, help="Number of OpenMP threads per process"
                    ),
                ),
                (
                    "group",
                    dict(
                        type=int,
                        default=1,
                        help="Number of processes to group into single job",
                    ),
                ),
                (
                    "serial",
                    dict(
                        action="store_true",
                        default=False,
                        help="Run grouped commands serially.",
                    ),
                ),
            ]
        )

    def add_arguments(self, parser=None, add_group=True):
        """
        Add job submission arguments to an argparse.ArgumentParser.

        Arguments
        ---------
        parser : argparse.ArgumentParser
            The parser to which to add arguments. If None, a new parser will
            be made and returned.
        add_group : bool or string
            Whether to add job submit options in an argument group.
            If a string, use as description for the group.

        Returns
        -------
        parser : argparse.ArgumentParser
            The updated argument parser object.
        """
        if parser is None:
            parser = ap.ArgumentParser()
        if add_group:
            if not isinstance(add_group, str):
                add_group = "Job Submit Options"
            group = parser.add_argument_group(add_group)
        else:
            group = parser

        for arg, opts in self.opt_list.items():
            if arg not in self.fixed_opts:
                group.add_argument("--" + arg.replace("_", "-"), **opts)
        return parser

    def pop_job_opts(self, args_dict, pop_submit=True):
        """
        Pop all of the job-related options from a dictionary of arguments

        Arguments
        ---------
        args_dict : dict
            The dictionary to pop from
        pop_submit : bool
            Whether to also pop an argument named "submit"
        """
        for key in self.opt_list:
            args_dict.pop(key, None)
        if pop_submit:
            args_dict.pop("submit", None)
        return args_dict

    def set_job_opts(self, args, load_defaults=True, **kwargs):
        """
        Set job submission options based on parsed arguments.

        Keyword arguments will be passed to ``update``.  Can be used to override
        particular job submission options. Any argument to the ``batch_sub`` or
        ``batch_group`` functions can be overridden in this way.

        Arguments
        ---------
        args : argparse.Namespace or dict
            The parsed command line arguments (from
            argparse.ArgumentParser.parse_args()).
        load_defaults : bool
            Whether to automatically load the default value for options
        """
        if isinstance(args, ap.Namespace):
            args = vars(args)
        else:
            args = args.copy()
        args.update(self.fixed_opts)

        # get default values for any missing options
        # can happen if called from python without doing argparse
        if load_defaults:
            for arg, opts in self.opt_list.items():
                if arg not in args:
                    args[arg] = opts["default"]

        if args["ppn"] is None:
            args["ppn"] = args["group"]

        mem_scale = args["group"] if not args["serial"] else 1.0
        mem = self.mem * mem_scale if self.mem is not None else None

        self.job_opts = dict(
            name=self.name,
            mem=mem,
            nodes=args["nodes"],
            exclude=args["exclude"],
            ppn=args["ppn"],
            queue=args["queue"],
            omp_threads=args["omp_threads"],
            env_script=args["env_script"],
            nice=args["nice"],
            delete=args["test"],
            submit=not args["test"],
            debug=args["test"],
            group_by=args["group"],
            serial=args["serial"],
        )
        self.job_opts["scheduler"] = "slurm"

        time = self.time / args["cpu_speed"]
        if time < 0.25:
            time = 0.25
        if args["use_cput"]:
            self.job_opts["cput"] = time * args["group"]
        else:
            self.job_opts["wallt"] = time

        if self.workdir:
            self.job_opts["workdir"] = self.workdir
        elif self.outkey in args:
            outd = args[self.outkey]
            if not np.isscalar(outd):
                outd = outd[0]
            self.job_opts["workdir"] = os.path.join(outd, "logs")

        self.update(**kwargs)

    def update(self, **kwargs):
        """
        Update particular job submission options.

        Keyword arguments can be used to override particular job submission
        options. Any argument to the ``batch_sub`` or ``batch_group`` functions
        can be overridden in this way.
        """
        self.job_opts.update(kwargs)

    def submit(self, jobs, **kwargs):
        """
        Submit jobs based on the parsed arguments. Must be called after
        set_job_opts.

        Keyword arguments will be passed to ``update``.  Can be used to override
        particular job submission options. Any argument to the ``batch_sub`` or
        ``batch_group`` functions can be overridden in this way.

        Arguments
        ---------
        jobs : string or list of strings
            The job(s) to submit.

        Returns
        -------
        List of job IDs for submitted jobs.
        """
        self.update(**kwargs)
        if isinstance(jobs, str):
            jobs = [jobs]
        return batch_group(jobs, **self.job_opts)
