lib_travis
==========


Version v2.3.11 as of 2021-02-15 see `Changelog`_

|travis_build| |license| |jupyter| |pypi| |black|

|codecov| |better_code| |cc_maintain| |cc_issues| |cc_coverage| |snyk|


.. |travis_build| image:: https://img.shields.io/travis/bitranox/lib_travis/master.svg
   :target: https://travis-ci.com/bitranox/lib_travis

.. |license| image:: https://img.shields.io/github/license/webcomics/pywine.svg
   :target: http://en.wikipedia.org/wiki/MIT_License

.. |jupyter| image:: https://mybinder.org/badge_logo.svg
 :target: https://mybinder.org/v2/gh/bitranox/lib_travis/master?filepath=lib_travis.ipynb

.. for the pypi status link note the dashes, not the underscore !
.. |pypi| image:: https://img.shields.io/pypi/status/lib-travis?label=PyPI%20Package
   :target: https://badge.fury.io/py/lib_travis

.. |codecov| image:: https://img.shields.io/codecov/c/github/bitranox/lib_travis
   :target: https://codecov.io/gh/bitranox/lib_travis

.. |better_code| image:: https://bettercodehub.com/edge/badge/bitranox/lib_travis?branch=master
   :target: https://bettercodehub.com/results/bitranox/lib_travis

.. |cc_maintain| image:: https://img.shields.io/codeclimate/maintainability-percentage/bitranox/lib_travis?label=CC%20maintainability
   :target: https://codeclimate.com/github/bitranox/lib_travis/maintainability
   :alt: Maintainability

.. |cc_issues| image:: https://img.shields.io/codeclimate/issues/bitranox/lib_travis?label=CC%20issues
   :target: https://codeclimate.com/github/bitranox/lib_travis/maintainability
   :alt: Maintainability

.. |cc_coverage| image:: https://img.shields.io/codeclimate/coverage/bitranox/lib_travis?label=CC%20coverage
   :target: https://codeclimate.com/github/bitranox/lib_travis/test_coverage
   :alt: Code Coverage

.. |snyk| image:: https://img.shields.io/snyk/vulnerabilities/github/bitranox/lib_travis
   :target: https://snyk.io/test/github/bitranox/lib_travis

.. |black| image:: https://img.shields.io/badge/code%20style-black-000000.svg
   :target: https://github.com/psf/black

small utils for travis:
 - print colored banners
 - wrap commands into run/success/error banners, with automatic retry
 - resolve the branch to test, based on the travis environment variables

----

automated tests, Travis Matrix, Documentation, Badges, etc. are managed with `PizzaCutter <https://github
.com/bitranox/PizzaCutter>`_ (cookiecutter on steroids)

Python version required: 3.6.0 or newer

tested on linux "bionic" with python 3.6, 3.7, 3.8, 3.9, 3.9-dev, pypy3 - architectures: amd64, ppc64le, s390x, arm64

`100% code coverage <https://codecov.io/gh/bitranox/lib_travis>`_, flake8 style checking ,mypy static type checking ,tested under `Linux, macOS <https://travis-ci.org/bitranox/lib_travis>`_, automatic daily builds and monitoring

----

- `Try it Online`_
- `Usage`_
- `Usage from Commandline`_
- `Installation and Upgrade`_
- `Requirements`_
- `Acknowledgements`_
- `Contribute`_
- `Report Issues <https://github.com/bitranox/lib_travis/blob/master/ISSUE_TEMPLATE.md>`_
- `Pull Request <https://github.com/bitranox/lib_travis/blob/master/PULL_REQUEST_TEMPLATE.md>`_
- `Code of Conduct <https://github.com/bitranox/lib_travis/blob/master/CODE_OF_CONDUCT.md>`_
- `License`_
- `Changelog`_

----

Try it Online
-------------

You might try it right away in Jupyter Notebook by using the "launch binder" badge, or click `here <https://mybinder.org/v2/gh/{{rst_include.
repository_slug}}/master?filepath=lib_travis.ipynb>`_

Usage
-----------

usage commandline:

.. code-block:: text

   Usage: lib_travis [OPTIONS] COMMAND [ARGS]...

     travis related utilities

   Options:
     --version                     Show the version and exit.
     --traceback / --no-traceback  return traceback information on cli
     -h, --help                    Show this message and exit.

   Commands:
     install
        updates pip, setuptools, wheel, pytest-pycodestyle
        --dry-run

     script
        updates pip, setuptools, wheel, pytest-pycodestyle
        --dry-run

     after_success
        coverage reports
        --dry-run

     deploy
        deploy on pypi
        --dry-run

     get_branch
        get the branch to work on

     info
        get program informations

     run [Options] <description> <command>
        run string command wrapped in run/success/error banners
        -r --retry              retry n times, default = 3
        -s --sleep              sleep when retry, default = 30 seconds
        --banner --no-banner    wrap in banners, default = True


- run a command passed as string

.. code-block:: bash

    # to be used in travis.yml
    # run a command passed as string, wrap it in colored banners, retry 3 times, sleep 30 seconds when retry
    $> lib_travis run "description" "command -some -options" --retry=3 --sleep=30


- get the branch to work on from travis environment variables

.. code-block:: bash

    $> BRANCH=$(lib_travis get_branch)

python methods:

- install, jobs to do in the Travis "install" section

.. code-block:: python

    def install(dry_run: bool = True) -> None:
        """
        upgrades pip, setuptools, wheel and pytest-pycodestyle


        Parameter
        ---------
        cPIP
            from environment, the command to launch pip, like "python -m pip"


        Examples
        --------

        >>> if os.getenv('TRAVIS'):
        ...     install(dry_run=True)

        """

- script, jobs to do in the Travis "script" section

.. code-block:: python

    def script(dry_run: bool = True) -> None:
        """
        travis jobs to run in travis.yml section "script":
        - run setup.py test
        - run pip with install option test
        - run pip standard install
        - test the CLI Registration
        - install the test requirements
        - install codecov
        - install pytest-codecov
        - run pytest coverage
        - run mypy strict
            - if MYPY_STRICT="True"
        - rebuild the rst files (resolve rst file includes)
            - needs RST_INCLUDE_SOURCE, RST_INCLUDE_TARGET set and BUILD_DOCS="True"
        - check if deployment would succeed, if setup.py exists and not a tagged build

        Parameter
        ---------
        cPREFIX
            from environment, the command prefix like 'wine' or ''
        cPIP
            from environment, the command to launch pip, like "python -m pip"
        cPYTHON
            from environment, the command to launch python, like 'python' or 'python3' on MacOS
        CLI_COMMAND
            from environment, must be set in travis - the CLI command to test with option --version
        MYPY_STRICT
            from environment, if pytest with mypy --strict should run
        PACKAGE_NAME
            from environment, the package name to pass to mypy
        BUILD_DOCS
            from environment, if rst file should be rebuilt
        RST_INCLUDE_SOURCE
            from environment, the rst template with rst includes to resolve
        RST_INCLUDE_TARGET
            from environment, the rst target file
        DEPLOY_WHEEL
            from environment, if a wheel should be generated
            only if setup.py exists and on non-tagged builds (there we deploy for real)
        dry_run
            if set, this returns immediately - for CLI tests


        Examples
        --------
        >>> script()

        """

- after_success, jobs to do in the Travis "after_success" section

.. code-block:: python

    def after_success(dry_run: bool = True) -> None:
        """
        travis jobs to run in travis.yml section "after_success":
            - coverage report
            - codecov
            - codeclimate report upload


        Parameter
        ---------
        cPREFIX
            from environment, the command prefix like 'wine' or ''
        cPIP
            from environment, the command to launch pip, like "python -m pip"
        CC_TEST_REPORTER_ID
            from environment, must be set in travis
        TRAVIS_TEST_RESULT
            from environment, this is set by TRAVIS automatically
        dry_run
            if set, this returns immediately - for CLI tests


        Examples
        --------
        >>> after_success()

        """

- deploy, deploy to pypi in the Travis "after_success" section

.. code-block:: python

    def deploy(dry_run: bool = True) -> None:
        """
        uploads sdist and wheels to pypi on success


        Parameter
        ---------
        cPREFIX
            from environment, the command prefix like 'wine' or ''
        PYPI_PASSWORD
            from environment, passed as secure, encrypted variable to environment
        TRAVIS_TAG
            from environment, needs to be set
        DEPLOY_SDIST, DEPLOY_WHEEL
            from environment, one of it needs to be true
        dry_run
            if set, this returns immediately - for CLI tests


        Examples
        --------
        >>> deploy()

        """

- get_branch, determine the branch to work on from Travis environment

.. code-block:: python

    def get_branch() -> str:
        """
        Return the branch to work on


        Parameter
        ---------
        TRAVIS_BRANCH
            from environment
        TRAVIS_PULL_REQUEST_BRANCH
            from environment
        TRAVIS_TAG
            from environment

        Result
        ---------
        the branch


        Exceptions
        ------------
        none


        ============  =============  ==========================  ==========  =======================================================
        Build         TRAVIS_BRANCH  TRAVIS_PULL_REQUEST_BRANCH  TRAVIS_TAG  Notice
        ============  =============  ==========================  ==========  =======================================================
        Custom Build  <branch>       ---                         ---         return <branch> from TRAVIS_BRANCH
        Push          <branch>       ---                         ---         return <branch> from TRAVIS_BRANCH
        Pull Request  <master>       <branch>                    ---         return <branch> from TRAVIS_PULL_REQUEST_BRANCH
        Tagged        <tag>          ---                         <tag>       return 'master'
        ============  =============  ==========================  ==========  =======================================================

        TRAVIS_BRANCH:
            for push builds, or builds not triggered by a pull request, this is the name of the branch.
            for builds triggered by a pull request this is the name of the branch targeted by the pull request.
            for builds triggered by a tag, this is the same as the name of the tag (TRAVIS_TAG).
            Note that for tags, git does not store the branch from which a commit was tagged. (so we use always master in that case)

        TRAVIS_PULL_REQUEST_BRANCH:
            if the current job is a pull request, the name of the branch from which the PR originated.
            if the current job is a push build, this variable is empty ("").

        TRAVIS_TAG:
            If the current build is for a git tag, this variable is set to the tag’s name, otherwise it is empty ("").

        """

- run, usually used internally

.. code-block:: python

    def run(
        description: str,
        command: str,
        retry: int = 3,
        sleep: int = 30,
        banner: bool = True,
        show_command: bool = True,
    ) -> None:
        """
        runs and retries a command passed as string and wrap it in "success" or "error" banners


        Parameter
        ---------
        description
            description of the action, shown in the banner
        command
            the command to launch
        retry
            retry the command n times, default = 3
        sleep
            sleep for n seconds between the commands, default = 30
        banner
            if to use banner for run/success or just colored lines.
            Errors will be always shown as banner
        show_command
            if the command is shown - take care not to reveal secrets here !


        Result
        ---------
        none


        Exceptions
        ------------
        none


        Examples
        ------------

        >>> run('test', "unknown command", sleep=0)
        Traceback (most recent call last):
            ...
        SystemExit: ...

        >>> run('test', "unknown command", sleep=0, show_command=False)
        Traceback (most recent call last):
            ...
        SystemExit: ...

        >>> run('test', "echo test")
        >>> run('test', "echo test", show_command=False)

        """

- travis.py example

.. code-block:: yaml

    language: python
    group: travis_latest
    dist: bionic
    sudo: true

    env:
        global:
            # prefix before commands - used for wine, there the prefix is "wine"
            - cPREFIX=""
            # command to launch python interpreter (its different on macOs, there we need python3)
            - cPYTHON="python"
            # command to launch pip (its different on macOs, there we need pip3)
            - cPIP="python -m pip"
            # switch off wine fix me messages
            - WINEDEBUG=fixme-all

            # PYTEST
            - PYTEST_DO_TESTS="True"

            # FLAKE8 tests
            - DO_FLAKE8_TESTS="True"

            # MYPY tests
            - MYPY_DO_TESTS="True"
            - MYPY_OPTIONS="--follow-imports=normal --implicit-reexport --no-warn-unused-ignores --strict"
            - MYPYPATH="./lib_travis/3rd_party_stubs"

            # coverage
            - DO_COVERAGE="True"
            - DO_COVERAGE_UPLOAD_CODECOV="True"
            - DO_COVERAGE_UPLOAD_CODE_CLIMATE="True"

            # package name
            - PACKAGE_NAME="lib_travis"
            # the registered CLI Command
            - CLI_COMMAND="lib_travis"
            # the source file for rst_include (rebuild rst file includes)
            - RST_INCLUDE_SOURCE="./.docs/README_template.rst"
            # the target file for rst_include (rebuild rst file includes)
            - RST_INCLUDE_TARGET="./README.rst"

            # secure environment variable
            - secure: "O8oOuJ4NfK9HRstY43GSgZcvmR2K/3N+rWzzNYHgKoNvOeBUMMQ6t90Pmgir/VfBF6TvkMxJwXnkAvFCtFAvzRN6KdgVq9UqkJ7CCS9woQxddPfFoTNwQDrySWmbD+cefh1Dt2uIGbnIhvWVCWlYbNAxfZ3IOTEhqfl2OOza44P8PJPplp83wKgbD899Th3qY8k77Kzh9+B2ErFVDBtVe8M10vI74WkuyZ/HP4ue1z5noa9cklkm9B1stf1Jqf4vW4lGnnsaR1camM5PH03OpFquxOvTTaoI+FAntW8zl8C+sFLC1xp4Emu3lT73OFtEXYUsvI7InWFEwl5k4pMMAXFVE4Nqf5PZviXGxtOTNI13gSBVcMw44eujoRpVrXzixQdrbhYUcID9mC3ApRh2002XxGVvHgLXxiKkBG/1yMNCsuRZrev45j4J/GItNvfswEtLDUTWOO+plxWsNSh2V7qfHFLnNJyBCU8sGj7sgyzQvS4YyJQ5V7pMeoXyvwnOU1lHYRCXbshO6Y/r3+PkCr1UcQXwH6/1awwwNDGK4DJ3BZHGeJTr7NI/IiJvgnLnXUAN6hpNW1V3GEbPMkz3FmcPkivmvVD8XOBl+w8OLghGCyqETbIfFhvplZ/S3dBthJLxlpEqJItNeG5dwdLAytwpFLWu40biRzrf/GsjkS8="  # CC_TEST_REPORTER_ID.secret
            - secure: "ME0CLFezdNlt8gbWEXNq6c8uT2kzbLmp4GoxUlJpsYG8A3xV+KrDXJ/RR66So62A5tvdxd8d8IN7j3HcapXqMyi/mbCDVu2eZXKOl/cGphMUS5lI80jjs/Yp6CwNC/qvBhe6bqkOXvhZS4I+4GTJOtRUEQJ5OLrf0uoGEVq9Tx6WKAElgcYMXdJNKwW8hSfUg5N2Ujq/PaaMXj7vIJSUBKWioIIx5doF7YSlixwCxj0HStyxX/lSy6VO1FJO2ZFsNN/jglduBJzbrYh6gcUbUc6fHCKzlr4RM70Ylb1rRkZSSY1uDvgTM6WiUS/LwN+65v+Z/rbucPJ/l8SGoEyrS/xytcECUq1oiyq+IMvJplspCV3/m+UGYd8jdJsG+O+WQQE0PknhBAtp22HJgI8xjU67SArXtbxA0/WhN/R7hulphnCDCqkyjR8lsao6mjXligsGbvHdm17u6dm0OCgpjA+R10ZW4SCOwDuGyA0prqOCsODRYLNnGXrNHUhJvrmx1TgkrIPL5VJIW3urujIj/G+clCgPzb+Dr/VAys0FNaRug1qFaoGAEFDutSJ/cALfTdiIU3RAVJ8lIChxmnaGneDf7GUKo36jjs9rdc5cqjHX4BG/7t5XSIymS8tBx1CWTxYVIGEhzSswDwcT2iZhBEuj+AJnY5ThE+bVNg2zhDw="  # PYPI_PASSWORD.secret



    addons:
        apt:
            packages:
                - xvfb      # install xvfb virtual framebuffer - this we need for WINE
                - winbind   # needed for WINE

    services:   			# start services
      - xvfb    			# is needed for WINE on headless installation

    matrix:
        include:


        - os: linux
          arch: "amd64"
          if: true
          language: python
          python: "3.6"
          before_install:
              - export BUILD_DOCS="False"
              - export DEPLOY_SDIST="True"
              - export DEPLOY_WHEEL="True"
              - export BUILD_TEST="True"
              - export MYPY_DO_TESTS="True"

        - os: linux
          arch: "amd64"
          if: true
          language: python
          python: "3.7"
          before_install:
              - export BUILD_DOCS="False"
              - export DEPLOY_SDIST="True"
              - export DEPLOY_WHEEL="False"
              - export BUILD_TEST="True"
              - export MYPY_DO_TESTS="True"

        - os: linux
          arch: "amd64"
          if: true
          language: python
          python: "3.8"
          before_install:
              - export BUILD_DOCS="False"
              - export DEPLOY_SDIST="True"
              - export DEPLOY_WHEEL="True"
              - export BUILD_TEST="True"
              - export MYPY_DO_TESTS="True"

        - os: linux
          arch: "amd64"
          if: true
          language: python
          python: "3.9"
          before_install:
              - export BUILD_DOCS="True"
              - export DEPLOY_SDIST="True"
              - export DEPLOY_WHEEL="True"
              - export BUILD_TEST="True"
              - export MYPY_DO_TESTS="True"

        - os: linux
          arch: "amd64"
          if: true
          language: python
          python: "3.9-dev"
          before_install:
              - export BUILD_DOCS="False"
              - export DEPLOY_SDIST="True"
              - export DEPLOY_WHEEL="True"
              - export BUILD_TEST="True"
              - export MYPY_DO_TESTS="True"

        - os: linux
          arch: "amd64"
          if: true
          language: python
          python: "pypy3"
          before_install:
              - export BUILD_DOCS="False"
              - export DEPLOY_SDIST="True"
              - export DEPLOY_WHEEL="True"
              - export BUILD_TEST="True"
              - export MYPY_DO_TESTS="False"

        - os: linux
          arch: "ppc64le"
          if: tag IS present
          language: python
          python: "3.8"
          before_install:
              - export BUILD_DOCS="False"
              - export DEPLOY_SDIST="True"
              - export DEPLOY_WHEEL="True"
              - export BUILD_TEST="True"
              - export MYPY_DO_TESTS="True"

        - os: linux
          arch: "s390x"
          if: tag IS present
          language: python
          python: "3.8"
          before_install:
              - export BUILD_DOCS="False"
              - export DEPLOY_SDIST="True"
              - export DEPLOY_WHEEL="True"
              - export BUILD_TEST="True"
              - export MYPY_DO_TESTS="True"

        - os: linux
          arch: "arm64"
          if: tag IS present
          language: python
          python: "3.8"
          before_install:
              - export BUILD_DOCS="False"
              - export DEPLOY_SDIST="True"
              - export DEPLOY_WHEEL="True"
              - export BUILD_TEST="True"
              - export MYPY_DO_TESTS="True"

        - os: osx
          if: true
          language: sh
          name: "macOS 10.15.7"
          python: "3.8"
          osx_image: xcode12.2
          env:
            # on osx pip and python points to python 2.7 - therefore we have to use pip3 and python3 here
            - cPREFIX=""				# prefix before commands - used for wine, there the prefix is "wine"
            - cPYTHON="python3"			# command to launch python interpreter (its different on macOs, there we need python3)
            - cPIP="python3 -m pip"   	# command to launch pip (its different on macOs, there we need pip3)
            - export BUILD_DOCS="False"
            - export DEPLOY_SDIST="False"
            - export DEPLOY_WHEEL="False"
            - export DEPLOY_TEST="True"
            - export MYPY_DO_TESTS="True"


    install:
        - ${cPIP} install lib_travis
        - log_util --colortest
        - lib_travis install

    script:
        - BRANCH=$(lib_travis get_branch)
        - log_util --level=NOTICE --banner "working on branch ${BRANCH}"
        - lib_travis script

    after_success:
        - lib_travis after_success
        - lib_travis deploy
        - ls -l ./dist

    notifications:
      email:
        recipients:
            - bitranox@gmail.com
        # on_success default: change
        on_success: never
        on_failure: always

Usage from Commandline
------------------------

.. code-block:: bash

   Usage: lib_travis [OPTIONS] COMMAND [ARGS]...

     travis related utilities

   Options:
     --version                     Show the version and exit.
     --traceback / --no-traceback  return traceback information on cli
     -h, --help                    Show this message and exit.

   Commands:
     after_success  coverage reports
     deploy         deploy on pypi
     get_branch     get the branch to work on
     info           get program informations
     install        updates pip, setuptools, wheel, pytest-pycodestyle
     run            run string command wrapped in run/success/error banners
     script         updates pip, setuptools, wheel, pytest-pycodestyle

Installation and Upgrade
------------------------

- Before You start, its highly recommended to update pip and setup tools:


.. code-block:: bash

    python -m pip --upgrade pip
    python -m pip --upgrade setuptools

- to install the latest release from PyPi via pip (recommended):

.. code-block:: bash

    python -m pip install --upgrade lib_travis

- to install the latest version from github via pip:


.. code-block:: bash

    python -m pip install --upgrade git+https://github.com/bitranox/lib_travis.git


- include it into Your requirements.txt:

.. code-block:: bash

    # Insert following line in Your requirements.txt:
    # for the latest Release on pypi:
    lib_travis

    # for the latest development version :
    lib_travis @ git+https://github.com/bitranox/lib_travis.git

    # to install and upgrade all modules mentioned in requirements.txt:
    python -m pip install --upgrade -r /<path>/requirements.txt


- to install the latest development version from source code:

.. code-block:: bash

    # cd ~
    $ git clone https://github.com/bitranox/lib_travis.git
    $ cd lib_travis
    python setup.py install

- via makefile:
  makefiles are a very convenient way to install. Here we can do much more,
  like installing virtual environments, clean caches and so on.

.. code-block:: shell

    # from Your shell's homedirectory:
    $ git clone https://github.com/bitranox/lib_travis.git
    $ cd lib_travis

    # to run the tests:
    $ make test

    # to install the package
    $ make install

    # to clean the package
    $ make clean

    # uninstall the package
    $ make uninstall

Requirements
------------
following modules will be automatically installed :

.. code-block:: bash

    ## Project Requirements
    click
    cli_exit_tools
    lib_log_utils
    rst_include

Acknowledgements
----------------

- special thanks to "uncle bob" Robert C. Martin, especially for his books on "clean code" and "clean architecture"

Contribute
----------

I would love for you to fork and send me pull request for this project.
- `please Contribute <https://github.com/bitranox/lib_travis/blob/master/CONTRIBUTING.md>`_

License
-------

This software is licensed under the `MIT license <http://en.wikipedia.org/wiki/MIT_License>`_

---

Changelog
=========

- new MAJOR version for incompatible API changes,
- new MINOR version for added functionality in a backwards compatible manner
- new PATCH version for backwards compatible bug fixes


v2.3.11
--------
2021-02-15: service release
    - update macOS to 10.15.7

v2.3.10
--------
2021-02-15: service release
    - disable rust-crypto build for architectures s390x and ppc64le, since compile errors

v2.3.9
--------
2021-02-15: service release
    - install rust compiler for pypy3 on linux, needed for twine
    - update secrets for travis-ci.com

v2.3.8
--------
2021-02-15: service release
    - install rust compiler for pypy3 on linux, needed for twine

v2.3.7
--------
2020-10-09: service release
    - update travis build matrix for linux 3.9-dev
    - update travis build matrix (paths) for windows 3.9 / 3.10

v2.3.6
--------
2020-08-16: service release
    - correct requirements

v2.3.5
--------
2020-08-15: service release
    - install requirements
    - more cleanup
    - black codestyle

v2.3.4
--------
2020-08-08: service release
    - cleanup

v2.3.3
--------
2020-08-08: service release
    - fix documentation
    - fix travis
    - deprecate pycodestyle
    - implement flake8

v2.3.2
---------
2020-08-07:
    - fix pypy eggs

v2.3.1
---------
2020-08-07:
    - fix mypy pypy

v2.3.0
---------
2020-08-07:
    - mypy without pytest
    - coverage refractor

v2.2.0
---------
2020-08-06: integrate flake8 (in transition)

v2.1.0
---------
2020-08-06: integrate flake8 (in transition)

v2.0.9
---------
2020-08-01: fix environment namings

v2.0.8
---------
2020-08-01: fix pypi deploy

v1.0.6
---------
2020-07-29: feature release
    - preserve Travis Tag

v1.0.5
---------
2020-07-29: feature release
    - pass correct package name to mypy and codecov

v1.0.4
---------
2020-07-29: feature release
    - use the new pizzacutter template
    - use cli_exit_tools

v1.0.3
---------
2020-07-29: feature release
    - fix code coverage test report

v1.0.2
---------
2020-07-29: feature release
    - do not reveal secrets in error messages

v1.0.1
---------
2020-07-29: feature release
    - documentation updates

v1.0.0
---------
2020-07-29: Release 1.0.0 fully functional

v0.4.9
---------
2020-07-27: feature release
    - add command script
    - add command after_success
    - add command deploy

v0.4.8
---------
2020-07-27: debug

v0.4.7
---------
2020-07-27: debug

v0.4.6
---------
2020-07-27: debug

v0.4.5
---------
2020-07-27: feature release
    - add command run_tests

v0.4.3
---------
2020-07-27: feature release
    - set default to --no-split on run_x
    - add command upgrade_setup_related

v0.4.2
---------
2020-07-27: feature release
    - change colors
    - catch all in run exceptions (OS Error)

v0.4.1
---------
2020-07-27: feature release
    - use cli_exit_tools
    - adding banner parameter to "run" commands

v0.4.0
---------
2020-07-23: feature release
    - rename commands

v0.3.1
---------
2020-07-23: feature release
    - add splitting of commands

v0.3.0
---------
2020-07-23: feature release
    - add second run method
    - add automatic quoting for commands passed as string

v0.2.1
---------
2020-07-23: patch release
    - flush streams on exit

v0.2.0
---------
2020-07-23: feature release
    - change arguments
    - add options for retry and sleep on run command

v0.1.3
---------
2020-07-23: patch release
    - correct doctests

v0.1.2
---------
2020-07-23: patch release
    - ignore unused options on cli run command
    - added description argument to run command

v0.1.1
---------
2020-07-23: initial release
    - setup
    - log utils
    - run wrapper
    - get the branch to work on

