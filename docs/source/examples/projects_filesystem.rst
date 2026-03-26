Projects Filesystem Examples
============================

This page demonstrates how to use the Projects API to manage files in a
nanoHUB project: listing projects, browsing directories, creating folders,
writing and editing files, reading file contents, and deleting files.

Authentication
--------------

.. code-block:: python

   import nanohubremote as nr

   auth_data = {
       'grant_type': 'personal_token',
       'token': 'your_personal_token_here'
   }

List Available Projects
-----------------------

.. code-block:: python

   with nr.Project(auth_data) as project:
       response = project.requestGet('projects/list')
       projects = response.json().get('projects', [])

       for p in projects:
           print(f"  ID: {p['id']}  |  Name: {p.get('title', p.get('alias', 'N/A'))}")

Get a Project Filesystem
------------------------

Pass the project ID (or alias) to ``project.files()`` to get a
PyFilesystem2 interface for that project.

.. code-block:: python

   with nr.Project(auth_data) as project:
       fs = project.files('18832')   # replace with your project ID

List Files in a Directory
--------------------------

.. code-block:: python

   files = fs.listdir('/')
   print(files)
   # ['deposition', 'etching', 'metrology', 'test.txt', 'thermal']

   # List a subdirectory
   files = fs.listdir('/metrology')
   print(files)

Create a Folder
---------------

.. code-block:: python

   fs.makedir('/example_folder')

Create a File
-------------

Use ``openbin()`` with mode ``"w"`` and write bytes.

.. code-block:: python

   with fs.openbin('/example_folder/hello.txt', 'w') as f:
       f.write(b"Hello from nanohubremote!\nThis is the initial content.\n")

Edit a File
-----------

Overwrite the file by opening it again in write mode.

.. code-block:: python

   with fs.openbin('/example_folder/hello.txt', 'w') as f:
       f.write(b"Hello from nanohubremote!\nThis content has been updated.\n")

Print File Contents
-------------------

.. code-block:: python

   with fs.openbin('/example_folder/hello.txt', 'r') as f:
       content = f.read().decode('utf-8')
   print(content)

Delete a File
-------------

.. code-block:: python

   fs.remove('/example_folder/hello.txt')

Delete a Folder
---------------

The folder must be empty before it can be removed.

.. code-block:: python

   fs.removedir('/example_folder')

Full Example
------------

.. literalinclude:: ../../../examples/projects_filesystem.py
   :language: python
