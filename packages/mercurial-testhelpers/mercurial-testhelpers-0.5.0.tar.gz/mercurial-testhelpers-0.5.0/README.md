# Mercurial Test Helpers
![test tube logo](https://foss.heptapod.net/mercurial/testhelpers/-/blob/branch/default/img/test_tube_icon_200.png)

This is a collection of facilities to help writing integration tests
for Python code around Mercurial: core development and extensions or other
downstreams like forges and graphical user interfaces.

It also provides a `coverage` plugin, allowing to check statements according to
the current Mercurial version.

See the [Integration Tests Plan wiki page](https://www.mercurial-scm.org/wiki/IntegrationTestsPlan) for more details.

This project is tested with its own helpers, so that many of the provided tests
can also be used as examples.

It has a 100% coverage policy, enforced by pre-landing continuous integration.

## FAQ

### Goal of the project

The goal is to include these test helpers in Mercurial core.

Once that happens, this project will serve to provide backwards compatibility,
especially for extensions that need to be compatible with
Mercurial versions that predate inclusion in core.

### Is pytest mandatory?

These helpers are just shortcuts to create setups easily and handle Mercurial
repositories. They don't depend themselves on a testing framework.
Only their own tests do.

Tighter integration with pytest will be provided as a separate project:
[pytest-mercurial](https://pypi.org/project/pytest-mercurial)

### What are the Python and Mercurial versions supported?

CPython 2.7, 3.7 and 3.8 are supported.

PyPy should work if Mercurial does,
except maybe for the discovery of Mercurial extensions used for tests skips.

Mercurial versions are those listed in [tox.ini](tox.ini).
As of this writing, these are Mercurial 4.3 to 5.6 on Python 2 and
5.3 to 5.6 on Python 3.

### Why not a generic Mercurial library?

The choices made are oriented towards being efficient (in particular fast) for
the task of writing tests. Some features wouldn't be legitimate in a
general-purpose library, for example random commit messages and file content.

On the other hand, some of the extra care about corner cases is not necessary:
users always have the option to go lower level if the helpers behave badly in
their case. This is much more acceptable in tests than in main application
code: it's better to add a missing test right away and reap the benefits
(non-regression, basis for main code refactors) than to postpone it for
breaking rules (not to say that technical debt does not exist in tests).

### Compatibility and stability

This project is too young and simple to get a clear picture of what will
happen, but we have reasons to be optimistic.

It was first started on Mercurial 5.2 and
turned out to easy to port down to 4.3. Forward compatibility won't be
a problem anyway once it's landed in Mercurial core.
The reason is that it calls Mercurial at a high level, actually often
through the functions that are right behind the command line interface.

For the same reasons that compatibility seems to be easy, providing stability
to downstream users shouldn't be too hard once we're settled about the basic
names.

Also, the fact that `bytes` are not mandatory in the API of the test helpers
is intended directly to help with the `bytes` vs `str` changes that
may happen after the final dismissal of Python 2 in Mercurial
(e.g `dict` keys and the like). While it's certain that such changes will be
painful for Mercurial developers, be it in the core or elsewhere,
at least if the tests setups keep working, we can hope that it will help a bit.

## Using the coverage plugin

The plugin has to be [activated in `.coveragerc`](https://coverage.readthedocs.io/en/coverage-5.3/plugins.html#using-plug-ins):

```
[run]
plugins = coverage_mercurial
```

Statements can then annotated with comments describing the versions of Mercurial
that are expected to run it. Example:

```python
from mercurial import util

if util.versiontuple() < (5, 4):
   do_something()  # hg<5.4
```

With the comment above, the `do_something()` statement will be excluded from
coverage when running with, e.g, Mercurial 5.5.

Details:

 - only simple comparisons with `<`, `>`, `=`, `<=`, and `>=` are supported.
 - no whitespace is allowed anywhere in the annotation itself. Leading and
   trailing words in the comment should be ignored.
 - it's not possible to create more complex rules with and/or logical
    connectors. Current behaviour when using several markers is unspecified
    and will change in some future release – don't depend on it.
 - supported Mercurial versions are of type `x.y`. Neither broader
   specifications (e.g., `hg<5`) nor more precise ones (e.g., `hg>4.8.2`)
   are understood. What happens with them is also unspecified, and can
   change in any future version.

## Running the tests of these test helpers

The quickest way to get a test run is to use
[tox](https://pypi.org/project/tox/), as this package comes with a
tox [configuration file](tox.ini) that defines a bunch of Python and Mercurial
combinations.

0. Pre-requisites:
   - target Python version, available on `$PATH` as `python2` or `python3`
   - required dependencies to build Mercurial from source (Python development
     files, usually in a package called `python$VERSION-dev` or
     `python$VERSION-devel`)

1. install tox

   Versions provided by package managers are usually fine.

   - Debian and derivatives: `apt install tox`
   - Fedora: `dnf install python3-tox`
   - MacPorts/HomeBrew: ?
   - generic: `$somepython -m pip install tox`. This `$somepython` can be
     completely different from those actually running the tests. Also tox is
     among other things a `virtualenv` manager.

2. run for a precise Python and Mercurial version: `tox -e py3-hg-5.6`.

   The first run will build Mercurial, the subsequent ones will be much
   faster.

3. run tox for all combinations: `tox`

   While the first run will be looong, as it will build Mercurial for all
   version combinations, the subsequent ones are pretty reasonable:

   ```
   $ time tox
   (...)
   ____________ summary ____________
     py3-hg5.6: commands succeeded
     py3-hg5.5: commands succeeded
     py3-hg5.4: commands succeeded
     py3-hg5.3: commands succeeded
     py2-hg5.6: commands succeeded
     py2-hg5.5: commands succeeded
     py2-hg5.4: commands succeeded
     py2-hg5.3: commands succeeded
     py2-hg5.2: commands succeeded
     py2-hg5.1: commands succeeded
     py2-hg5.0: commands succeeded
     py2-hg4.9: commands succeeded
     py2-hg4.8: commands succeeded
     py2-hg4.7: commands succeeded
     py2-hg4.6: commands succeeded
     py2-hg4.5: commands succeeded
     py2-hg4.4: commands succeeded
     py2-hg4.3: commands succeeded
     congratulations :)
   tox  39.53s user 5.27s system 99% cpu 45.044 total
   ```

## Included examples, and how to run them

### examples/core

These are actual tests from Mercurial core, translated (case of `.t` tests)
or not (Python tests).

They are run as part of the main suite. If you already had a `tox` test run,
then you've tried them already.

`tests/test_repo_wrapper.py` is also a source of examples to get an idea of
what can be done.

### examples/evolve

These are toy examples of testing with the `evolve` and `topic` extensions,
and how the `hg-evolve` project could extend on these helpers.

To run them, one has to use the `run-all-tests` script in a context where
Mercurial and hg-evolve are available. Example:

```
python3 -m venv venv_hg_evolve
venv_hg_evolve/bin/pip install Mercurial==5.5.2 hg-evolve
source venv_hg_evolve/bin/activate
pip install -r test-requirements.txt
./run-all-tests
```

Remarks:

 - For Python 2, start with `virtualenv -p python2`, then it's the same.
 - Often, `mercurial` is not importable right after installation in a
   virtualenv. That's why the first `pip` above was before activation.
 - It's also possible to run only the hg-evolve examples:

   ```
   pytest examples/hg_evolve
   ```

### examples/hg-git
Another toy example, this time with an additional integration need (Git itself).

Prerequisite: `git` standard executable, available on `$PATH`.

To run the tests, one has to use the `run-all-tests` script in a context where
Mercurial and hg-git are available. Example:

```
python3 -m venv venv_hg_git
venv_hg_git/bin/pip install Mercurial==5.6 hg-git
source venv_hg_git/bin/activate
pip install -r test-requirements.txt
./run-all-tests
```

Remarks:

 - For Python 2, start with `virtualenv -p python2`, then it's the same.
 - Often, `mercurial` is not importable right after installation in a
   virtualenv. That's why the first `pip` above was before activation.
 - It's also possible to run only the hg-git examples:

   ```
   pytest examples/hg_git
   ```

## Credits

Test tube logo by User:Townie on Wikimedia Commons,
License Creative Commons by-sa international 4.0
