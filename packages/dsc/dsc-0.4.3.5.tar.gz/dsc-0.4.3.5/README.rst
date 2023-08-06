Dynamic Statistical Comparisons (DSC)
=====================================

|PyPI Version| |Travis Status|

The `project wiki <https://stephenslab.github.io/dsc-wiki>`__ is the
main source of documentation for both developers and users of the DSC
project. If you are new to the concept of DSC, it may worth reading this
`blog
post <http://stephens999.github.io/blog/2014/10/Data-Driven-Discovery.html>`__
to understand the motivation behind this project.

This work is supported by the the Gordon and Betty Moore Foundation via
an Investigator Award to Matthew Stephens, `Grant
GBMF4559 <https://www.moore.org/grants/list/GBMF4559>`__, as part of the
`Data-Driven Discovery
program <https://www.moore.org/programs/science/data-driven-discovery>`__.
If you have any questions or want to share some information with the
developer / user community, please open a `github
issue <https://github.com/stephenslab/dsc/issues>`__.

Developer notes
---------------

Upgrading DSC to latest development version
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

For most users, we recommend installing the `most recent stable
release <https://stephenslab.github.io/dsc-wiki/installation.html>`__.
If you would like to upgrade your existing installation of DSC to the
most recent (unstable) development version, follow these steps.

DSC is closely developed in parallel with
`SoS <http://github.com/vatlab/sos>`__. Therefore, the development
version of DSC (maintained in the ``master`` branch of the GitHub
repository) typically requires the development version of SoS.

To update,

.. code:: bash

   pip install git+https://github.com/vatlab/sos -U
   pip install git+https://github.com/stephenslab/dsc -U

Install dscrutils from source
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Assuming the working directory in your R environment is the ``dsc``
repository, run the following code in R to install the latest
development version of the dscrutils R package:

.. code:: r

   getwd() # Should be ... /dsc
   install.packages("dscrutils",repos = NULL,type = "source")

Project maintenance
^^^^^^^^^^^^^^^^^^^

Although relatively stable and usable in practice, DSC is still actively
being developed. Occasionally upgrades to the most recent version will
lead to changes of file signatures that triggers rerun of existing
benchmark even if they have not been changed. When this happens we will
indicate in bold in our release note below that “a file signature clean
up is recommended” (see release note 0.2.7.7 for example). That means
after such DSC upgrades you should rerun your benchmark with
``-s existing`` (or, ``--touch``) option to update file signatures. If
possible, it is recommended that you rerun your benchmark from scratch
(if resources can afford) with ``-s none`` instead of ``-s existing`` to
skip all existing files. We apologize for the inconveniences it incurs.

Change Log
----------

0.4.3
~~~~~

-  Issue #94 revisited.
-  [minor] Fix syntax incompatibility with earlier versions of
   ``msgpack``.
-  [minor] Fix a bug of not updating meta-database when ``-s existing``
   is used.

**A file signature clean up is required after this upgrade.**

.. _section-1:

0.4.2
~~~~~

-  Issue #214 for container support.
-  SoS bumped to version 0.21.5 for container support.

.. _section-2:

0.4.0
~~~~~

-  Issue #194
-  Issue #202
-  [minor] #209, #196
-  Improve scripts command options.

**A file signature clean up is required after this upgrade.**

0.3.x
~~~~~

0.3.10

-  Issue #154
-  Add a remote job option ``nodes_per_job`` and provide such mechanism
   to run on multiple nodes.
-  SoS bumped to version 0.20.2.

0.3.9

-  Issue #179
-  Issue #182
-  Issue #183
-  SoS bumped to version 0.19.11 for additional improvements in cluster
   job submission.

0.3.8

-  Issue #171 is partially improved.

0.3.7

-  ``dscquery`` now properly handles ``NULL`` module output variables.
-  Some performance improvements on I/O database.
-  SoS bumped to version 0.19.7 for various bug fixes on cluster job
   submitter.

0.3.6

-  Now SQLite keywords can be used as module names: no error message
   will be triggered.
-  Introduce an explicit syntax for base module: a module without
   executable is considered base module.
-  Bump ``rpy2`` version requirment version 3.0.0+ for benchmark with R
   and Python modules.
-  SoS bumped to version 0.19.5 for improved memory usage on job
   submitter and improved Python module version check.

0.3.5

Major improvements to ``dscrquery``

-  Performance improvement #168
-  Output format improvement #174

0.3.4

-  Reimplement ``dsc-query`` and ``dscrquery`` for improved handling of
   missing value #145.
-  Reimplement ``dscrquery``\ ’s ``condition`` statement to make it more
   R-user friendly.
-  Add unknown command argument #162.
-  [minor] Introduce ``DSC::run::default``, for the behavior of running
   the script without targets.
-  [minor] #161
-  SoS bumped to version 0.19.1 for improved sockets management and
   improved R library auto-installation.

0.3.3

-  [minor] #160
-  SoS bumped to version 0.18.4 for performance optimizations.

0.3.2

-  Various improvements for remote job submission and execution (mostly
   on SoS).
-  SoS bumped to version 0.18.1 to support these changes.

0.3.1

-  Improved database I/O performance to cope with file system latency.
-  Improved Python to R data flow.
-  Paralleled data extraction in ``dscquery``.
-  SoS bumped to version 0.17.4 to support a new implementation of job
   queues.

0.3.0

-  SoS bumped to version 0.16.9 to support a new implementation of
   signatures.
-  [minor] Bug fix #147.

.. _x-1:

0.2.x
~~~~~

0.2.9.1

-  Stop moving library imports to the front of scripts, due to various
   side effect.

0.2.9.0

-  SoS bumped to version 0.9.16.0 for optimized remote task file
   management.
-  [minor] Bug fixes.

**A file signature clean up is required after this upgrade.**

0.2.8.6

-  Change in query behavior #145

0.2.8.5

-  Bug fixes for cluster execution #142, #143, #144.
-  Add ``-d`` option to output DAG #141.
-  Removed ``-p`` option because it triggers rerun and cannot be easily
   implemented otherwise.
-  SoS bumped to version 0.9.14.10 for many of the fixes above.

**A file signature clean up is recommended after this upgrade.**

0.2.8.4

-  Fix running Python 3 based modules on Mac computer with ``homebrew``
   installed Python #140.

0.2.8.3

-  ``dsc-io`` can now convert CSV to HTML with pop-up figures.
-  Add ``groups`` and ``load.pkl`` options to ``dscrutils::dscquery``.
-  [minor] Bug fixes.

0.2.8.2

-  Add ``-p`` option to print stdout and stderr to screen.
-  SoS bumped to version 0.9.14.1 for

   -  Improved parallel slot management.
   -  Improved messaging on executed steps (use ``-v 3`` to display in
      DSC).

0.2.8.1

-  Minor file check performance optimization.
-  Force overwrite converted ``pkl`` to ``rds`` in
   ``dscutils::dscquery``, as a save default.

0.2.8

Input string parameter behavior has changed since this version. Now
un-quoted strings will be treated input script code; string parameters
will have to be quoted. A new DSC configuration parser has been
implemented to overcome ``pyYAML`` restrictions. Please submit a bug
report if the new parser misbehaves.

**A file signature clean up is recommended after this upgrade.**

0.2.7.11

-  [minor] More stringent check on improper module names ending with
   ``_{digits}``.

0.2.7.10

-  Stop adding script hash to default seed #136.
-  [minor] SoS bumped to version 0.9.13.8 a bug fix release.

**A file signature clean up is recommended after this upgrade.**

0.2.7.9

Minor touches on 0.2.7.8 – just a celebration of the 1,000-th commit to
the DSC repo on github, after 2 years and 3 months into this project.

0.2.7.8

-  Implement a preliminary ``%include`` feature to provide alternative
   code organization style.
-  Allow for ``!`` operator in ``List()`` and ``Dict()``.
-  SoS bumped to version 0.9.13.7 for improved remote job support.
-  [minor] Various bug fixes.

0.2.7.7

-  Improvements for module with shell executables and command options.
-  Improvements for remote execution #131.
-  Improved logging.
-  Bug fixes #126, #127.
-  SoS bumped to version 0.9.13.4 for #128 and related.

**A file signature clean up is recommended after this upgrade.**

0.2.7.6

-  Add new feature ``dscrutils::shiny_plot`` to display simple benchmark
   results.
-  [minor] Display unused modules with ``-h`` option.

0.2.7.5

-  Add R / Python packages and version display with ``-h`` option.
-  Add ``.gitignore`` for cache folder when a git environment is
   detected.
-  SoS bumped to 0.9.13.3 that now bundles the ``pbs`` module.

0.2.7.4

-  Improved R’s sessionInfo format.
-  Bug fixes #119, #121, #122
-  [minor] Error message improvements.

0.2.7.3

-  More stringent R library and command executable check.
-  [minor] Fix a regression bug on path due to 0.2.7.2.

0.2.7.2

-  Improved Windows path support.
-  [minor] Fix a bug with nested tuple with ``raw()``.

0.2.7.1

-  Dump individual data object with scripts using ``dsc-query *.pkl``
   and ``dsc-query *.rds``.
-  [minor] Improve behavior for length 1 vector in R’s list with ``R()``
   operator.
-  [minor] Various bug fixes.

0.2.7

-  `#92 <https://github.com/stephenslab/dsc/issues/92>`__ paired
   parameter input convention.
-  `#90 <https://github.com/stephenslab/dsc/issues/90>`__ and
   `#93 <https://github.com/stephenslab/dsc/issues/93>`__ use ``Rmd``
   files as module executables.
-  `#94 <https://github.com/stephenslab/dsc/issues/94>`__ and
   `#95 <https://github.com/stephenslab/dsc/issues/95>`__ added
   ``DSC::replicate`` and command option ``--replicate``.
-  Enhance ``R()`` operator due to use of
   `dscrutils <https://github.com/stephenslab/dsc/tree/master/dscrutils>`__
   package. This packages is now required to parse DSC file when ``R``
   modules are involved.
-  Add, by default, a variable ``DSC_DEBUG`` to output files that saves
   various runtime info.
-  SoS bumped to 0.9.13.2

   -  Support R github package force install when version mismatches.
   -  Force use ``pip`` to install local development version.
   -  `#97 <https://github.com/stephenslab/dsc/issues/97>`__ Improved
      error logging and reporting behavior.

-  [minor] Revert from ``ruamel.yaml`` to ``yaml`` for better
   performance.
-  [minor] `#96 <https://github.com/stephenslab/dsc/issues/96>`__
-  [minor] `#98 <https://github.com/stephenslab/dsc/issues/98>`__
-  [minor] Various bug fixes.

0.2.6.5

-  Bring back partial mixed languages support. **Piplines with mixed R
   and Python code can communicate data of limited types (recursively
   support array, matrix, dataframe), via ``rpy2`` as in versions prior
   to 0.2.5.x**. Support for additional languages will be implemented on
   need basis with ``HDF5`` format
   `#86 <https://github.com/stephenslab/dsc/issues/86>`__.

0.2.6.4

-  Add a ``dsc-io`` command to convert between python ``pickle`` and R
   ``RDS`` files – an internal command for data conversion and a test
   for ``rpy2`` configuration.

0.2.6.3

-  Inline module executable via language interpreters (eg. ``R()``,
   ``Python()``).

0.2.6.2

-  [minor] Ignore leading ``.`` in ``file()``: ``file(.txt)`` and
   ``file(txt)`` are equivalent.
-  [minor] Disallow derivation of modules from ensemble.
-  [minor] Various bug fixes.

0.2.6.1

-  Internally replace ``RDS`` format with ``HDF5`` format for Python
   routines. **Pipeline with mixed languages is now officially broken at
   this point until the next major release that supports ``HDF5`` in
   R**.
-  SoS required version bumped to 0.9.12.7 for relevant upstream bug
   fixes for remote host computing.
-  [minor] Various bug fixes.

0.2.6

-  Bring back ``--host`` option; add a companion option ``--to-host`` to
   facilicate sending resources to remote computer.
-  Add ``--truncate`` switch.
-  SoS required version bumped to 0.9.12.3 for relevant upstream bug
   fixes.
-  [minor] Improved command interface.

0.2.5.2

-  SoS required version bumped to 0.9.12.2 for relevant upstream bug
   fixes.

0.2.5.1

-  Change in ``seed`` behavior: since this release ``seed`` will no
   longer be a DSC keyword. Users are responsible to set seeds on their
   own.
-  [minor] Allow for both lower case and capitalized operator names
   ``File/file, List/list, Dict/dict``.

0.2.5

-  New syntax release, compatible with SoS 0.9.12.1.
-  Removed ``--host`` option due to upstream changes.

.. _x-2:

0.1.x
~~~~~

0.1.0

-  First release, compatible with SoS 0.6.4.

.. |PyPI Version| image:: https://badge.fury.io/py/dsc.svg
   :target: https://badge.fury.io/py/dsc
.. |Travis Status| image:: https://travis-ci.org/stephenslab/dsc.svg?branch=master
   :target: https://travis-ci.org/stephenslab/dsc
