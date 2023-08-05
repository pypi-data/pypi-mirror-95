=====================
NEWS for flufl.i18n
=====================

3.1.5 (2021-02-14)
==================
* I `blue <https://blue.readthedocs.io/en/latest/>`_ it!

3.1.4 (2021-01-01)
==================
* Update copyright years.
* Include ``test/__init__.py`` and ``docs/__init__.py`` (GL#9)

3.1.3 (2020-10-22)
==================
* Rename top-level tests/ directory to test/ (GL#8)

3.1.2 (2020-10-21)
==================
* Small documentation fix.

3.1.1 (2020-10-21)
==================
* Fix the site-packages pollution.  (GL#7)

3.1 (2020-10-20)
================
* Improve the documentation.
* Reorganized docs and tests out of the code directory. (GL#5)
* Fix the Windows CI job. (GL#6)

3.0.1 (2020-07-28)
==================
* Fix pytest 6.0.0 compatibility
* Add CI for Python 3.9 on Windows

3.0 (2020-07-12)
================
* Drop support for Python 3.4 and 3.5.  Add support for Python 3.9.
* ``Translator.catalog`` property is now exposed.
* New abstract classes for defining the types in this library:
  ``TranslationContextManager``, ``RuntimeTranslator``, ``TranslationStrategy``
* When ``expand()`` gets an exception, the original exception is re-raised.
  This used to inadvertently return None.
* Add type annotations and API reference documentation.
* Other internal improvements.

2.0.2 (2019-05-17)
==================
* Add (testing) support for Python 3.7 and 3.8.
* Add LICENSE and the top level README.rst file to release tarball. (Closes #4)

2.0.1 (2017-11-14)
==================
* Restore Python 3.4 support.

2.0 (2017-07-24)
================
* Add ``_.defer_translation()`` context manager for marking, but not
  translating a string at the point of use.  (Closes #2)
* Drop Python 2, 3.3, and 3.4 compatibility; add Python 3.5 and 3.6.
* Switch to the Apache License Version 2.0
* Use flufl.testing for nose2 and flake8 plugins.

1.1.3 (2014-04-25)
==================
* Include MANIFEST.in in the sdist tarball, otherwise the Debian package
  won't built correctly.

1.1.2 (2014-03-31)
==================
* Fix documentation bug.  LP: #1026403
* Use modern setuptools rather than distutils.
* Bump copyright years.

1.1.1 (2012-04-19)
==================
* Add classifiers to setup.py and make the long description more compatible
  with the Cheeseshop.
* Other changes to make the Cheeseshop page look nicer.  (LP: #680136)
* setup_helper.py version 2.1.

1.1 (2012-01-19)
================
* Support Python 3 without the need for 2to3.

1.0.4 (2010-12-06)
==================
* Restore missing line from MANIFEST.in to fix distribution tarball.

1.0.3 (2010-12-01)
==================
* Fix setup.py to not install myfixers artifact directory on install.
* Remove pylint.rc; we'll use pyflakes instead.

1.0.2 (2010-06-23)
==================
* Small documentation fix.

1.0.1 (2010-06-09)
==================
* Ditch the use of zc.buildout.
* Improved documentation.

1.0 (2010-04-24)
================
* Use Distribute instead of Setuptools.
* Port to Python 3 when used with 2to3.
* More documentation improvements.

0.6 (2010-04-21)
================
* Documentation and lint clean up.

0.5 (2010-04-20)
================
* Added a simplified initialization API for one-language-context
  applications. This works much better for non-server applications.
* Added a SimpleStrategy which recognizes the $LOCPATH environment variable.
* Show how PEP 292 strings are supported automatically.
* When strategies are called with zero arguments, they supply the default
  translation context, which is usually a NullTranslation.  This is better
  than hardcoding the NullTranslation in the Application.

0.4 (2010-03-04)
================
* Add the ability to get the current language code, via _.code

0.3 (2009-11-15)
================
* Initial release.
