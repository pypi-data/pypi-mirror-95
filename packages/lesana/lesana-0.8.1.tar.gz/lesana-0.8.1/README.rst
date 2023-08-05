===============================
 lesana - a collection manager
===============================

lesana is a python3 library to organize collections of various kinds.
It is designed to have a data storage / serialization format that is
friendly to git and other VCSs, but decent performances.

To reach this aim it uses yaml_ as its serialization format, which is
easy to store in a VCS, share between people and syncronize between
different computers, but it also keeps an index of this data in a local
xapian_ database in order to allow for fast searches.

.. _yaml: http://yaml.org/
.. _xapian: https://xapian.org/

lesana supports collections of any kind, as long as their entries can be
described with a mostly flat dictionary of fields of the types described
in the documentation file ``field_types``.

Some example collection schemas are provided, but one big strenght of
lesana is the ability to customize your collection with custom fields
by simply writing a personalized ``settings.yaml``.

Installation
------------

The source code for lesana can be downloaded from the git repository at
https://git.sr.ht/~valhalla/lesana; releases are made
on `pypi <https://pypi.org/project/lesana/>`_.

lesana expects to run on a POSIX-like system and requires the following
dependencies:

* python3
* xapian_
* `ruamel.yaml <https://bitbucket.org/ruamel/yaml>`_
* `jinja2 <http://jinja.pocoo.org/>`_
* `dateutil <https://dateutil.readthedocs.io/>`_
* `GitPython <https://github.com/gitpython-developers/GitPython>`_
  optional, to add git support.

Under debian (and derivatives), the packages to install are::

   apt install python3-jinja2 python3-ruamel.yaml python3-xapian \
               python3-dateutil python3-git

lesana can be run in place from the git checkout / extracted tarball; to
use ``setup.py`` you will also need setuptools (e.g. from the
``python3-setuptools`` package under debian and derivatives).

License
-------

Copyright (C) 2016-2020 Elena Grandi

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
