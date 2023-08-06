#!/usr/bin/env python
__author__ = "Gao Wang"
__copyright__ = "Copyright 2016, Stephens lab"
__email__ = "gaow@uchicago.edu"
__license__ = "MIT"

import os, sys, time
from sos.utils import env, get_traceback
from .version import __version__
from .syntax import DSC_CACHE


class Timer(object):
    def __init__(self, verbose=False):
        self.verbose = verbose

    def __enter__(self):
        self.start = time.time()
        return self

    def __exit__(self, *args):
        self.end = time.time()
        self.secs = self.end - self.start
        self.msecs = self.secs * 1000  # millisecs
        if self.verbose:
            env.logger.info('Elapsed time ``%.03f`` seconds.' % self.secs)

    def disable(self):
        self.verbose = False


def remove(workflows, groups, modules, db, purge=False):
    from .dsc_database import remove_unwanted_output, remove_obsolete_output
    if purge and modules:
        remove_unwanted_output(workflows, groups, modules, db, zap=False)
    elif purge:
        remove_obsolete_output(db)
        # Clean up task signatures
        env.logger.info("Cleaning up obsolete job cache ...")
        from sos.__main__ import cmd_purge
        from .addict import Dict as dotdict
        # purge current completed tasks
        settings = {
            'tasks': None,
            'all': False,
            'age': None,
            'status': ['completed'],
            'tags': None,
            'queue': None,
            'config': None,
            'verbosity': 1
        }
        cmd_purge(dotdict(settings), [])
        # purge all tasks of more than 3 days old
        settings['all'] = True
        settings['age'] = '3d'
        settings['status'] = None
        cmd_purge(dotdict(settings), [])
    else:
        remove_unwanted_output(workflows, groups, modules, db, zap=True)


def plain_remove(outdir):
    import shutil
    shutil.rmtree(outdir, ignore_errors=True)
    to_remove = [outdir + '.html', outdir + '.scripts.html']
    for item in to_remove:
        if os.path.isfile(item):
            os.remove(item)


def execute(args, unknown_args):
    if args.to_remove:
        if args.target is None and args.to_remove not in ('obsolete', 'all'):
            raise ValueError("``-d`` must be specified with ``--target``.")
        rm_objects = args.target
        args.target = None
    if args.target:
        env.logger.info("Load command line DSC sequence: ``{}``".\
                        format(' '.join(', '.join(args.target).split())))
    # Import packages
    from .utils import workflow2html, transcript2html
    from sos import execute_workflow
    from .dsc_parser import DSC_Script, DSC_Pipeline, remote_config_parser
    from .dsc_translator import DSC_Translator
    # Parse DSC script
    script = DSC_Script(args.dsc_file,
                        output=args.output,
                        sequence=args.target,
                        global_params=unknown_args,
                        truncate=args.truncate,
                        replicate=1 if args.truncate else args.replicate,
                        host=args.host,
                        debug = args.debug)
    script.init_dsc(env)
    pipeline_obj = DSC_Pipeline(script).pipelines
    db = os.path.basename(script.runtime.output)
    # Apply clean-up
    if args.to_remove:
        if args.to_remove == 'all':
            plain_remove(script.runtime.output)
        else:
            remove(pipeline_obj, {
                **script.runtime.concats,
                **script.runtime.groups
            }, rm_objects, script.runtime.output, args.to_remove == 'obsolete')
        return
    # Archive scripts
    script.to_html()
    env.logger.info(f"DSC script exported to ``{script.runtime.output}.html``")
    if args.debug:
        workflow2html(f'{DSC_CACHE}/{db}_workflow.html', pipeline_obj,
                      list(script.dump().values()))
    # Generate remote job configuration settings
    if args.host:
        conf = remote_config_parser(args.host)
        conf_tpl = {'localhost': 'localhost', 'hosts': conf['DSC']}
    else:
        conf = conf_tpl = dict()
    # Obtain pipeline scripts
    pipeline = DSC_Translator(
        pipeline_obj, script.runtime, args.__construct__ == "none",
        args.__max_jobs__, False, None
        if len(conf) == 0 else {k: v
                                for k, v in conf.items() if k != 'DSC'},
        args.debug and args.verbosity == 0)
    # Generate DSC meta databases
    env.logger.info(f"Constructing DSC from ``{args.dsc_file}`` ...")
    script_prepare = pipeline.get_pipeline("prepare", args.debug)
    settings = {
        'sig_mode': 'default',
        'error_mode': 'default',
        'max_running_jobs': None if args.host else args.__max_jobs__,
        'worker_procs': args.__max_jobs__,
    }
    if args.__construct__ == "none":
        settings['sig_mode'] = "force"
    # Get mapped IO database
    settings['verbosity'] = args.verbosity if args.debug else 1
    status = execute_workflow(script_prepare,
                              workflow='deploy',
                              options=settings)
    env.verbosity = args.verbosity
    if args.__construct__ == "existing":
        settings['sig_mode'] = "build"
    if args.__construct__ == "lenient":
        settings['sig_mode'] = "skip"
    # Get DSC meta database
    env.logger.info("Building DSC database ...")
    status = execute_workflow(script_prepare,
                              workflow='build',
                              options=settings)
    if args.__construct__ == "all":
        return
    # Get the executed pipeline
    pipeline.filter_execution(args.debug)
    script_run = pipeline.get_pipeline("run", args.debug)
    if args.debug:
        if args.host:
            import yaml
            yaml.safe_dump(conf_tpl,
                           open(f'{DSC_CACHE}/{db}_remote_config.yml', 'w'),
                           default_flow_style=False)
        return
    env.logger.debug(f"Running command ``{' '.join(sys.argv)}``")
    if os.path.isfile(f'{env.exec_dir}/transcript.txt'):
        os.remove(f'{env.exec_dir}/transcript.txt')
    env.logger.info(f"Building execution graph & running DSC ...")
    # making verbosity level consistent with before SoS version 0.21.2
    verbosity_map = {0:1,1:0,2:2 if args.host else 0,3:3,4:4}
    try:
        if not args.error_mode == 'ignore-safe':
            settings['error_mode'] = args.error_mode
        settings['verbosity'] = verbosity_map[args.verbosity]
        settings['output_dag'] = f'{db}.dot' if args.__dag__ else None
        status = execute_workflow(script_run,
                                  workflow='DSC',
                                  options=settings,
                                  config=conf_tpl)
        env.verbosity = args.verbosity
    except Exception as e:
        if args.host is None:
            transcript2html(f'{env.exec_dir}/transcript.txt',
                            f'{db}.scripts.html',
                            title=db)
            env.logger.error(f"Please examine ``stderr`` files below and/or run commands ``in green`` to reproduce " \
                               "the errors;\nadditional scripts upstream of the error can be found in " \
                               f"``{db}.scripts.html``.\n" + '=' * 75)
        raise Exception(e)
    # Plot DAG
    if args.__dag__:
        from sos.utils import dot_to_gif
        try:
            env.logger.info(
                "Generating DAG animation for benchmark (may take a while; can be disrupted if no longer wanted) ..."
            )
            dag = dot_to_gif(f"{db}.dot")
            with open(f'{db}_DAG.html', 'w') as f:
                f.write(
                    f'<img class="dag-image" src="data:image/png;base64,{dag}">'
                )
            env.logger.info(f"Execution graph saved to ``{db}_DAG.html``")
        except Exception as e:
            env.logger.warning(f'Failed to generate execution graph: {e}')
    env.logger.info("DSC complete!")


def main():
    from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter, SUPPRESS

    class ArgumentParserError(Exception):
        pass

    class MyArgParser(ArgumentParser):
        def error(self, message):
            raise ArgumentParserError(message)

    #
    p = MyArgParser(description=__doc__,
                    formatter_class=ArgumentDefaultsHelpFormatter,
                    add_help=False)
    p.add_argument('dsc_file',
                   metavar="DSC script",
                   help='DSC script to execute.')
    ce = p.add_argument_group('Benchmark options')
    ce.add_argument('--target',
                    metavar="str",
                    nargs='+',
                    help='''This argument can be used in two contexts:
                   1) When used without "-d" it overrides "DSC::run" in DSC file.
                   Input should be quoted string(s) defining one or multiple valid DSC pipelines
                   (multiple pipelines should be separated by space).
                   2) When used along with "-d" it specifies one or more computational modules,
                   separated by space, whose output are to be removed or replaced by a (smaller) placeholder file.'''
                    )
    ce.add_argument(
        '--truncate',
        action='store_true',
        help='''When applied, DSC will only run one value per parameter.
                   For example with "--truncate", "n: 1,2,3,4,5" will be truncated to "n: 1".
                   This can be used in exploratory analysis and diagnostics, particularly when used in combination with "--target".'''
    )
    ce.add_argument(
        '--replicate',
        metavar='N',
        type=int,
        help=
        '''Overrides "DSC::replicate" to set number of replicates. Will be set to 1 when "--truncate" is in action.'''
    )
    ce.add_argument(
        '-o',
        metavar="str",
        dest='output',
        help=
        '''Benchmark output. It overrides "DSC::output" defined in DSC file.'''
    )
    mt = p.add_argument_group('Execution modes')
    mt.add_argument('-s',
                    metavar="option",
                    choices=["strict", "lenient", "existing", "all", "none"],
                    dest='__construct__',
                    default="strict",
                    help='''How DSC skips or overwrites existing results.
                   "strict": skips jobs whose input, output and code have not been changed since previous execution.
                   "lenient": skips jobs whose output timestamp are newer than their input.
                   It can be used to avoid re-run when nuisent changes are made to module scripts that should not impact results.
                   "existing": skips jobs whose output exists, and mark existing output as "up-to-date" for future re-runs.
                   It can be used to avoid re-run completely even after file status cache have been deleted
                   (eg, after partially transferring output data from one location to another).
                   "all": skips all modules and only build meta-database required to run `dsc-query` command.
                   It can be used for salvaging a partially completed benchmark making it possible to query from it.
                   "none": force executes DSC from scratch.''')
    mt.add_argument('--touch',
                    action='store_true',
                    dest='__recover__',
                    help=SUPPRESS)
    mt.add_argument('-e',
                    metavar='option',
                    choices=['ignore-safe', 'ignore', 'abort'],
                    dest='error_mode',
                    default="ignore-safe",
                    help='''How DSC responds to errors.
                    "abort": stop all module instances immediately after an error occurs.
                    "ignore": ignore all errors and try to complete the benchmark.
                    "ignore-safe": only stop module instances with errors or has errors in their upstream modules.
                    ''')
    mt.add_argument('-d',
                    metavar="option",
                    choices=["obsolete", "replace", "all"],
                    dest='to_remove',
                    help='''How DSC deletes benchmark files.
                   Use option "all" to remove all output from the current benchmark.
                   "obsolete", when used without "--target", removes from output folder anything irrelevant
                   to the most recent successful execution of the benchmark.
                   When used with "--target" it deletes specified files, or files from specified modules or module groups.
                   "replace", when used with "--target", deletes files as option "obsolete" does with "--target",
                   but additionally puts in placeholder files with "*.zapped" extension to prevent the module from being executed
                   until they are needed for re-running a downstream module.
                   It can be used to remove large yet unused intermediate module output without triggering re-runs when possible.'''
                    )
    ro = p.add_argument_group('Computing options')
    ro.add_argument(
        '-c',
        type=int,
        metavar='N',
        default=max(min(int(os.cpu_count() / 2), 8), 1),
        dest='__max_jobs__',
        help=
        '''Maximum number of CPU threads for local runs, or job managing sockets for remote execution.'''
    )
    ro.add_argument(
        '-v',
        '--verbosity',
        type=int,
        choices=list(range(5)),
        default=2,
        help='''Various levels of output information to screen.''')
    ro.add_argument(
        '-g',
        dest='__dag__',
        action='store_true',
        help='''Output benchmark execution graph animation in HTML format.''')
    rt = p.add_argument_group('HPC settings')
    rt.add_argument(
        '--host',
        metavar='file',
        help='''Configuration file for DSC computational environments.''')
    ot = p.add_argument_group('Other options')
    ot.add_argument('--version', action='version', version=__version__)
    ot.add_argument("-h",
                    "--help",
                    action="help",
                    help="show this help message and exit")
    ot.add_argument('--debug', action='store_true', help=SUPPRESS)
    p.set_defaults(func=execute)
    if len(sys.argv) > 2 and '-h' in sys.argv:
        try:
            from .dsc_parser import DSC_Script
            script = DSC_Script(sys.argv[1])
            script.print_help(print_version='-v' in sys.argv)
            sys.exit(0)
        except Exception as e:
            if '--debug' in sys.argv:
                raise
            else:
                env.logger.error(
                    f'No help information is available for script {sys.argv[1]}: ``{e}``'
                )
                sys.exit(1)
    try:
        args, unknown_args = p.parse_known_args()
    except Exception as e:
        env.logger.error(e)
        env.logger.info("Please type ``{} -h`` to view available options".\
                        format(os.path.basename(sys.argv[0])))
        sys.exit(1)
    #
    env.verbosity = args.verbosity
    # keep `args.__recover__` to maintain backwards compatibility for `--touch` option.
    if args.__recover__:
        env.logger.warning(
            f'Option ``--touch`` is deprecated. Please use ``-s existing`` next time.'
        )
        args.__construct__ = 'existing'
    with Timer(verbose=True if (args.verbosity > 0) else False) as t:
        try:
            args.func(args, unknown_args)
        except KeyboardInterrupt:
            t.disable()
            sys.exit('KeyboardInterrupt')
        except Exception as e:
            if args.debug:
                raise
            if args.verbosity > 2:
                sys.stderr.write(get_traceback())
            t.disable()
            env.logger.error(e)
            sys.exit(1)


if __name__ == '__main__':
    main()