.. -*- coding: utf-8 -*-

Changes
-------

1.16 (2021-02-20)
~~~~~~~~~~~~~~~~~

- Promote to the *stable* state

- Move the job of building and uploading binary wheels from TravisCI to GitHub Actions


1.15 (2021-02-19)
~~~~~~~~~~~~~~~~~

- Fix ``IF EXISTS`` variant of ``RenameStmt`` printer (`PR #70`__), thanks to Jonathan
  Mortensen

  __ https://github.com/lelit/pglast/pull/70

- Update libpg_query to 10-1.0.5


1.14 (2020-10-24)
~~~~~~~~~~~~~~~~~

- Produce Python 3.9 wheels, thanks to ``cibuildwheel`` 1.6.3

- Expose the ``libpg_query``'s `fingerprint`__ functionality (`PR #64`__), thanks to Yiming
  Wang

  __ https://github.com/lfittl/libpg_query/wiki/Fingerprinting
  __ https://github.com/lelit/pglast/pull/64


1.13 (2020-09-26)
~~~~~~~~~~~~~~~~~

- Handle ``SELECT FROM foo``


1.12 (2020-06-08)
~~~~~~~~~~~~~~~~~

- Double quote column names in the ``TYPE_FUNC_NAME_KEYWORDS`` set (`issue #55`__)

  __ https://github.com/lelit/pglast/issues/55

- Possibly wrap ``SELECT`` in ``UNION``/``INTERSECT`` between parens, when needed
  (`issue #55`__)

  __ https://github.com/lelit/pglast/issues/55


1.11 (2020-05-08)
~~~~~~~~~~~~~~~~~

- Fix ``A_Expr`` printer, when ``lexpr`` is missing (`PR #54`__), thanks to Aiham

  __ https://github.com/lelit/pglast/pull/54

- Support ``DISABLE ROW LEVEL SECURITY`` in ``AlterTableCmd`` (`PR #49`__), thanks to Ronan
  Dunklau

  __ https://github.com/lelit/pglast/pull/49

- Implement ``CreateOpClassStmt`` printer (`PR #47`__), thanks to Ronan Dunklau

  __ https://github.com/lelit/pglast/pull/47


1.10 (2020-01-25)
~~~~~~~~~~~~~~~~~

- Fix collation name printer (`PR #44`__), thanks to Ronan Dunklau

  __ https://github.com/lelit/pglast/pull/44

- Implement ``CreatePLangStmt`` printer (`PR #42`__), thanks to Bennie Swart

  __ https://github.com/lelit/pglast/pull/42

- Fix privileges printer (`PR #41`__), thanks to Bennie Swart

  __ https://github.com/lelit/pglast/pull/41

- Handle ``TRUNCATE`` event in ``CreateTrigStmt`` printer (`PR #40`__), thanks to Bennie Swart

  __ https://github.com/lelit/pglast/pull/40

- Fix function body dollar quoting (`PR #39`__), thanks to Bennie Swart

  __ https://github.com/lelit/pglast/pull/39


1.9 (2019-12-20)
~~~~~~~~~~~~~~~~

- Prettier ``INSERT`` representation


1.8 (2019-12-07)
~~~~~~~~~~~~~~~~

- Prettier ``CASE`` representation

- New option to emit a semicolon after the last statement (`issue #24`__)

  __ https://github.com/lelit/pglast/issues/24


1.7 (2019-12-01)
~~~~~~~~~~~~~~~~

- Implement ``NotifyStmt`` printer

- Implement ``RuleStmt`` printer, thanks to Gavin M. Roy for his `PR #28`__

  __ https://github.com/lelit/pglast/pull/28

- Fix ``RenameStmt``, properly handling object name

- Produce Python 3.8 wheels, thanks to `cibuildwheel`__ 1.0.0

  __ https://github.com/joerick/cibuildwheel

- Support ``ALTER TABLE RENAME CONSTRAINT`` (`PR #35`__), thanks to Ronan Dunklau

  __ https://github.com/lelit/pglast/pull/35


1.6 (2019-09-04)
~~~~~~~~~~~~~~~~

- Fix issue with boolean expressions precedence (`issue #29`__)

  __ https://github.com/lelit/pglast/issues/29

- Implement ``BitString`` printer

- Support ``LEAKPROOF`` option (`PR #31`__), thanks to Ronan Dunklau

  __ https://github.com/lelit/pglast/pull/31

- Support ``DEFERRABLE INITIALLY DEFERRED`` option (`PR #32`__), thanks to Ronan Dunklau

  __ https://github.com/lelit/pglast/pull/32


1.5 (2019-06-04)
~~~~~~~~~~~~~~~~

- Fix issue with ``RETURNS SETOF`` functions, a more general solution than the one proposed by
  Ronan Dunklau (`PR #22`__)

  __ https://github.com/lelit/pglast/pull/22

- Allow more than one empty line between statements (`PR #26`__), thanks to apnewberry

  __ https://github.com/lelit/pglast/pull/26


1.4 (2019-04-06)
~~~~~~~~~~~~~~~~

- Fix wrap of trigger's WHEN expression (`issue #18`__)

  __ https://github.com/lelit/pglast/issues/18

- Support for variadic functions (`PR #19`__), thanks to Ronan Dunklau

  __ https://github.com/lelit/pglast/pull/19

- Support ORDER / LIMIT / OFFSET for set operations (`PR #20`__), thanks to Ronan Dunklau

  __ https://github.com/lelit/pglast/pull/20

- Implement ``ConstraintsSetStmt`` and improve ``VariableSetStmt`` printers


1.3 (2019-03-28)
~~~~~~~~~~~~~~~~

- Support ``CROSS JOIN`` and timezone modifiers on time and timestamp datatypes (`PR #15`__),
  thanks to Ronan Dunklau

  __ https://github.com/lelit/pglast/pull/15

- Many new printers and several enhancements (`PR #14`__), thanks to Ronan Dunklau

  __ https://github.com/lelit/pglast/pull/14

- Expose the package version as pglast.__version__ (`issue #12`__)

  __ https://github.com/lelit/pglast/issues/12


1.2 (2019-02-13)
~~~~~~~~~~~~~~~~

- Implement new `split()` function (see `PR #10`__)

  __ https://github.com/lelit/pglast/pull/10

- Implement ``BooleanTest`` printer (`issue #11`__)

  __ https://github.com/lelit/pglast/issues/11


1.1 (2018-07-20)
~~~~~~~~~~~~~~~~

- No visible changes, but now PyPI carries binary wheels for Python 3.7.


1.0 (2018-06-16)
~~~~~~~~~~~~~~~~

.. important:: The name of the package has been changed from ``pg_query`` to ``pglast``, to
               satisfy the request made by the author of ``libpg_query`` in `issue #9`__.

               This affects both the main repository on GitHub, that from now on is
               ``https://github.com/lelit/pglast``, and the ReadTheDocs project that hosts the
               documentation, ``http://pglast.readthedocs.io/en/latest/``.

               I'm sorry for any inconvenience this may cause.

__ https://github.com/lelit/pglast/issues/9


0.28 (2018-06-06)
~~~~~~~~~~~~~~~~~

- Update libpg_query to 10-1.0.2

- Support the '?'-style parameter placeholder variant allowed by libpg_query (details__)

__ https://github.com/lfittl/libpg_query/issues/45


0.27 (2018-04-15)
~~~~~~~~~~~~~~~~~

- Prettier JOINs representation, aligning them with the starting relation


0.26 (2018-04-03)
~~~~~~~~~~~~~~~~~

- Fix cosmetic issue with ANY() and ALL()


0.25 (2018-03-31)
~~~~~~~~~~~~~~~~~

- Fix issue in the safety belt check performed by ``pgpp`` (`issue #4`__)

__ https://github.com/lelit/pglast/issues/4


0.24 (2018-03-02)
~~~~~~~~~~~~~~~~~

- Implement ``Null`` printer


0.23 (2017-12-28)
~~~~~~~~~~~~~~~~~

- Implement some other DDL statements printers

- New alternative style to print *comma-separated-values* lists, activated by a new
  ``--comma-at-eoln`` option on ``pgpp``


0.22 (2017-12-03)
~~~~~~~~~~~~~~~~~

- Implement ``TransactionStmt`` and almost all ``DROP xxx`` printers


0.21 (2017-11-22)
~~~~~~~~~~~~~~~~~

- Implement ``NamedArgExpr`` printer

- New alternative printers for a set of *special functions*, activated by a new
  ``--special-functions`` option on ``pgpp`` (`issue #2`__)

__ https://github.com/lelit/pglast/issues/2


0.20 (2017-11-21)
~~~~~~~~~~~~~~~~~

- Handle special de-reference (``A_Indirection``) cases


0.19 (2017-11-16)
~~~~~~~~~~~~~~~~~

- Fix serialization of column labels containing double quotes

- Fix corner issues surfaced implementing some more DDL statement printers


0.18 (2017-11-14)
~~~~~~~~~~~~~~~~~

- Fix endless loop due to sloppy conversion of command line option

- Install the command line tool as ``pgpp``


0.17 (2017-11-12)
~~~~~~~~~~~~~~~~~

- Rename printers.sql to printers.dml (**backward incompatibility**)

- List printer functions in the documentation, referencing the definition of related node type

- Fix inconsistent spacing in JOIN condition inside a nested expression

- Fix representation of unbound arrays

- Fix representation of ``interval`` data type

- Initial support for DDL statements

- Fix representation of string literals containing single quotes


0.16 (2017-10-31)
~~~~~~~~~~~~~~~~~

- Update libpg_query to 10-1.0.0


0.15 (2017-10-12)
~~~~~~~~~~~~~~~~~

- Fix indentation of boolean expressions in SELECT's targets (`issue #3`__)

__ https://github.com/lelit/pglast/issues/3


0.14 (2017-10-09)
~~~~~~~~~~~~~~~~~

- Update to latest libpg_query's 10-latest branch, targeting PostgreSQL 10.0 final


0.13 (2017-09-17)
~~~~~~~~~~~~~~~~~

- Fix representation of subselects requiring surrounding parens


0.12 (2017-08-22)
~~~~~~~~~~~~~~~~~

- New option ``--version`` on the command line tool

- Better enums documentation

- Release the GIL while calling libpg_query functions


0.11 (2017-08-11)
~~~~~~~~~~~~~~~~~

- Nicer indentation for JOINs, making OUTER JOINs stand out

- Minor tweaks to lists rendering, with less spurious whitespaces

- New option ``--no-location`` on the command line tool


0.10 (2017-08-11)
~~~~~~~~~~~~~~~~~

- Support Python 3.4 and Python 3.5 as well as Python 3.6


0.9 (2017-08-10)
~~~~~~~~~~~~~~~~

- Fix spacing before the $ character

- Handle type modifiers

- New option ``--plpgsql`` on the command line tool, just for fun


0.8 (2017-08-10)
~~~~~~~~~~~~~~~~

- Add enums subpackages to the documentation with references to their related headers

- New ``compact_lists_margin`` option to produce a more compact representation when possible
  (see `issue #1`__)

__ https://github.com/lelit/pglast/issues/1


0.7 (2017-08-10)
~~~~~~~~~~~~~~~~

- Fix sdist including the Sphinx documentation


0.6 (2017-08-10)
~~~~~~~~~~~~~~~~

- New option ``--parse-tree`` on the command line tool to show just the parse tree

- Sphinx documentation, available online


0.5 (2017-08-09)
~~~~~~~~~~~~~~~~

- Handle some more cases when a name must be double-quoted

- Complete the serialization of the WindowDef node, handling its frame options


0.4 (2017-08-09)
~~~~~~~~~~~~~~~~

- Expose the actual PostgreSQL version the underlying libpg_query libray is built on thru a new
  ``get_postgresql_version()`` function

- New option `safety_belt` for the ``prettify()`` function, to protect the innocents

- Handle serialization of ``CoalesceExpr`` and ``MinMaxExpr``


0.3 (2017-08-07)
~~~~~~~~~~~~~~~~

- Handle serialization of ``ParamRef`` nodes

- Expose a ``prettify()`` helper function


0.2 (2017-08-07)
~~~~~~~~~~~~~~~~

- Test coverage at 99%

- First attempt at automatic wheel upload to PyPI, let's see...


0.1 (2017-08-07)
~~~~~~~~~~~~~~~~

- First release ("Hi daddy!", as my soul would tag it)
