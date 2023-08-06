=======================================
Getui Custom-Developed ownCloud library
=======================================

个推定制化修改版本 Owncloud SDK，提供客户方进行数据文件交互使用。

Features
========

Supports connecting to ownCloud 8.2, 9.0, 9.1 and newer.

General information
-------------------

- retrieve information about ownCloud instance (e.g. version, host, URL, etc.)

Accessing files
---------------

- basic file operations like getting a directory listing, file upload/download, directory creation, etc
- read/write file contents from strings
- upload with chunking and mtime keeping
- upload whole directories
- directory download as zip
- access files from public links
- upload files to files drop link target

Sharing (OCS Share API)
-----------------------

- share a file/directory via public link
- share a file/directory with another user or group
- unshare a file/directory
- check if a file/directory is already shared
- get information about a shared resource
- update properties of a known share

Apps (OCS Provisioning API)
---------------------------

- enable/disable apps
- retrieve list of enabled apps

Users (OCS Provisioning API)
----------------------------

- create/delete users
- create/delete groups
- add/remove user from groups

App data
--------

- store app data as key/values using the privatedata OCS API

Requirements
============

- Python >= 2.7 or Python >= 3.5
- requests module (for making HTTP requests)

Installation
============

Automatic installation with pip:

.. code-block:: bash

    $ pip install gtocclient


Usage
=====

Example for uploading a file then sharing with link:

.. code-block:: python

    import owncloud

    oc = owncloud.Client('http://domain.tld/owncloud')

    oc.login('user', 'password')

    oc.mkdir('testdir')

    oc.put_file('testdir/remotefile.txt', 'localfile.txt')

    link_info = oc.share_file_with_link('testdir/remotefile.txt')

    print "Here is your link: " + link_info.get_link()

Running the unit tests
======================

To run the unit tests, create a config file called "owncloud/test/config.py".
There is a config file example called "owncloud/test/config.py.sample". All the
information required is in that file. 
It should point to a running ownCloud instance to test against.

You might also need to install the unittest-data-provider package:

.. code-block:: bash

    $ pip install unittest-data-provider

Then run the script "runtests.sh":

.. code-block:: bash

    $ ./runtests.sh

Building the documentation
==========================

To build the documentation, you will need to install Sphinx and docutil.
Then run the following commands:

.. code-block:: bash

    $ sphinx-apidoc -e -f -o docs/source owncloud/ owncloud/test
    $ cd docs
    $ make html

You can then find the documentation inside of "doc/build/html".

