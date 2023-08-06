.. image:: https://raw.githubusercontent.com/senaite/senaite.core.supermodel/master/static/logo_pypi.png
   :target: https://github.com/senaite/senaite.core.supermodel#readme
   :alt: senaite.core.supermodel
   :height: 128

*A beautiful content wrapper for SENAITE that you will love*
============================================================

.. image:: https://img.shields.io/pypi/v/senaite.core.supermodel.svg?style=flat-square
   :target: https://pypi.python.org/pypi/senaite.core.supermodel

.. image:: https://img.shields.io/github/issues-pr/senaite/senaite.core.supermodel.svg?style=flat-square
   :target: https://github.com/senaite/senaite.core.supermodel/pulls

.. image:: https://img.shields.io/github/issues/senaite/senaite.core.supermodel.svg?style=flat-square
   :target: https://github.com/senaite/senaite.core.supermodel/issues

.. image:: https://img.shields.io/badge/README-GitHub-blue.svg?style=flat-square
   :target: https://github.com/senaite/senaite.core.supermodel#readme

.. image:: https://img.shields.io/badge/Built%20with-%E2%9D%A4-brightgreen.svg
   :target: https://github.com/senaite/senaite.core.supermodel/blob/master/src/senaite/core/supermodel/docs/SUPERMODEL.rst

.. image:: https://img.shields.io/badge/Made%20for%20SENAITE-%E2%AC%A1-lightgrey.svg
   :target: https://www.senaite.com


About
=====

The SENAITE CORE SUPERMODEL is a content wrapper for objects and catalog brains
in SENAITE and provides a unified dictionary interface to access the schema
fields, methods and metadata.


For what is it needed?
======================

The purpose of the SUPERMODEL is to help coders to access the data from content
objects. It also ensures that the most effective and efficient method is used to
achieve a task.


How does it work?
-----------------

A `SuperModel` can be instantiated with an `UID` of a content object::

    >>> from senaite.core.supermodel import SuperModel
    >>> supermodel = SuperModel('e37c1b659137414e872c08af410f09b4')

This will give transparent access to all schema fields of the wrapped object as
well to all the metadata columns of the primary catalog of this object::

    >>> supermodel.MySchemaField'
    'Value of MySchemaField'

Please read the `full functional doctest`_ to see the super powers of the
`SuperModel` in action.


Installation
============

SENAITE.CORE.SUPERMODEL is a dependency of SENAITE.CORE and therefore no
additional installation steps are required.


.. _full functional doctest: https://github.com/senaite/senaite.core.supermodel/blob/master/src/senaite/core/supermodel/docs/SUPERMODEL.rst


Changelog
=========

1.2.4 (2020-08-04)
------------------

- version bump


1.2.3 (2020-03-02)
------------------

- #10 Fix API import


1.2.2 (2020-03-01)
------------------

- #9 Support Dexterity Fields


1.2.1 (2019-07-01)
------------------

- #8 Do not process "0" values to Portal-SuperModels
- #7 Fix traceback when initializing a supermodel with a catalog brain
- #6 Added Destructor and further improvements
- #5 Fix UID->SuperModel conversion of UIDReferenceFields
- #4 Skip private fields starting with `_`


1.2.0 (2019-03-30)
------------------

- Compatibility release for SENAITE CORE 1.3.0


1.1.0 (2018-10-04)
------------------

- #2 Allow to pass in a catalog brain or instance to initialize a SuperModel


1.0.0 (2018-07-19)
------------------

- Initial Release


