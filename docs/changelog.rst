Changelog
=========

Version 1.0.1 (2015-11-03)
--------------------------

No changes whatsoever from previous release. This is an artificial release
because PYPI won't allow me to replace the distribution files after they've been
uploaded.


Version 1.0 Final (2015-11-03)
------------------------------

No code change from previous release -- This is just to say "it's definitely
production-ready". However, the following minor changes were made:

- Altered test suite to ensure Python 3.4 and 3.5 were supported, as well as
  PyPy3.
- Dropped support for Python 3.2 because ``coverage.py`` v4 no longer supports
  it, so the test suite wouldn't run anymore in this environment. This version
  will work on Python 3.2, but future releases may not.
- Marked `Wheel <http://wheel.readthedocs.org/en/latest/>`_ distribution as
  universal.


Version 1.0rc2 (2015-02-18)
---------------------------

Made records pickable by setting the ``__module__`` on the record type.


Version 1.0rc1 (2014-11-08)
---------------------------

Initial release.
