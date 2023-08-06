.. image:: https://raw.githubusercontent.com/senaite/senaite.jsonapi/master/static/logo_pypi.png
   :target: https://github.com/senaite/senaite.jsonapi
   :alt: senaite.jsonapi
   :height: 128px

RESTful JSON API for SENAITE LIMS
=================================

.. image:: https://img.shields.io/pypi/v/senaite.jsonapi.svg?style=flat-square
    :target: https://pypi.python.org/pypi/senaite.jsonapi

.. image:: https://img.shields.io/travis/senaite/senaite.jsonapi/master.svg?style=flat-square
    :target: https://travis-ci.org/senaite/senaite.jsonapi

.. image:: https://readthedocs.org/projects/pip/badge/
  :target: https://senaitejsonapi.readthedocs.org

.. image:: https://img.shields.io/github/issues-pr/senaite/senaite.jsonapi.svg?style=flat-square
    :target: https://github.com/senaite/senaite.jsonapi/pulls

.. image:: https://img.shields.io/github/issues/senaite/senaite.jsonapi.svg?style=flat-square
    :target: https://github.com/senaite/senaite.jsonapi/issues

.. image:: https://img.shields.io/badge/Made%20for%20SENAITE-%E2%AC%A1-lightgrey.svg
   :target: https://www.senaite.com


About
-----

This SENAITE.JSONAPI is a RESTful JSON API for `SENAITE LIMS`_, that allows to
Create, Read and Update (CRU operations) through http GET/POST requests. It uses
JSON as the format for data representation.


Installation
------------

Add *senaite.jsonapi* in the eggs section of your buildout:

.. code-block:: ini

  eggs =
      senaite.lims
      senaite.jsonapi


and run *bin/buildout*.


Documentation
-------------

* https://senaitejsonapi.readthedocs.io


Feedback and support
--------------------

* `Community site <https://community.senaite.org/>`_
* `Gitter channel <https://gitter.im/senaite/Lobby>`_
* `Users list <https://sourceforge.net/projects/senaite/lists/senaite-users>`_


License
-------

**SENAITE.JSONAPI** Copyright (C) 2017-2020 RIDING BYTES & NARALABS

This program is free software; you can redistribute it and/or modify it under
the terms of the `GNU General Public License version 2
<https://github.com/senaite/senaite.jsonapi/blob/master/LICENSE>`_ as published
by the Free Software Foundation.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.


.. Links

.. _SENAITE LIMS: https://www.senaite.com


Changelog
=========

1.2.4 (unreleased)
------------------

- #41 Push endpoint for custom jobs


1.2.3 (2020-08-05)
------------------

- #40 Prevent the id of objects of being accidentally updated
- #40 Do not allow to update objects from setup folder
- #40 Do not allow to update objects from portal root
- #40 Fix upgrade does not work on post-only mode
- #40 Adapter for custom handling of `update` operation
- #37 Do not allow to create objects in setup folder
- #37 Do not allow to create objects in portal root
- #37 Adapter for custom handling of `create` operation
- #37 Make the creation operation to be portal_type-naive
- #35 Added `catalogs` route
- #34 Make senaite.jsonapi catalog-agnostic on searches


1.2.2 (2020-03-03)
------------------

- Missing package data


1.2.1 (2020-03-02)
------------------

- Fixed tests and updated build system


1.2.0 (2018-01-03)
------------------

**Added**

- Added `parent_path` to response data
- Allow custom methods as attributes in adapter

**Removed**

**Changed**

- Integration to SENAITE CORE
- License changed to GPLv2

**Fixed**

- #25 Null values are saved as 'NOW' in Date Time Fields
- Fixed Tests

**Security**


1.1.0 (2017-11-04)
------------------

- Merged PR https://github.com/collective/plone.jsonapi.routes/pull/90
- Get object by UID catalog


1.0.1 (2017-09-30)
------------------

- Fixed broken release (missing MANIFEST.in)


1.0.0 (2017-09-30)
------------------

- First release


