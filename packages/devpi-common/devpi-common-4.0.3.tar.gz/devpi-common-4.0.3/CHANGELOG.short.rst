

=========
Changelog
=========




.. towncrier release notes start

4.0.3 (2023-11-23)
==================

Bug Fixes
---------

- Add ``is_prerelease`` and other methods to ``LegacyVersion`` to fix ``get_sorted_versions`` with ``stable=True`` and some other cases.


4.0.2 (2023-10-15)
==================

Bug Fixes
---------

- Do not mark commands with returncode ``None`` from tox 4.x as failed.


4.0.1 (2023-10-15)
==================

Bug Fixes
---------

- Restore flushing after each written line in new TerminalWriter.


4.0.0 (2023-10-11)
==================

Deprecations and Removals
-------------------------

- Removed ``HTMLPage`` class originally vendored from pip.

- Dropped support for Python <= 3.6.



Features
--------

- Add ``chdir`` context handler in devpi_common.contextlib. Starting with Python 3.11 the original from ``contextlib`` is used.

- Hide username from URL representation.

- Added stripped down TerminalWriter from ``py`` library which only supports coloring.



Bug Fixes
---------

- Fix #939: custom legacy version parsing (non PEP 440) after packaging >= 22.0 removed support.


3.7.2 (2023-01-24)
==================





Bug Fixes
---------

- Fix #928: correct default for pre-release matching after switching from ``pkg_resources`` to ``packaging``.

- Fix #949: correct parsing of wheel tags for Python 3.10 and above.

