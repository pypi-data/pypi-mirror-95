.. |travis status| image:: https://img.shields.io/travis/com/EGuthrieWasTaken/add_juniper_software/main
.. |pypi version| image:: https://img.shields.io/pypi/v/add_juniper_software
.. |license| image:: https://img.shields.io/pypi/l/add_juniper_software
.. |pypi status| image:: https://img.shields.io/pypi/status/add_juniper_software

.. |code size| image:: https://img.shields.io/github/languages/code-size/EGuthrieWasTaken/add_juniper_software
.. |downloads| image:: https://img.shields.io/pypi/dw/add-juniper-software
.. |python versions| image:: https://img.shields.io/pypi/pyversions/add_juniper_software
.. |pypi format| image:: https://img.shields.io/pypi/format/add_juniper_software

.. |readthedocs status| image:: https://readthedocs.org/projects/ezpyz/badge/?version=latest

===========================================================================
add_juniper_software |travis status| |pypi version| |license| |pypi status|
===========================================================================
Welcome to add_juniper_software! 

**This project is under development, and will likely not work as intended. You have been warned.**

--------------------------------------------------------------------
Installation |code size| |downloads| |python versions| |pypi format|
--------------------------------------------------------------------
This package is installed using pip. Pip should come pre-installed with all versions of Python for which this package is compatible. Nonetheless, if you wish to install pip, you can do so by downloading `get-pip.py <https://pip.pypa.io/en/stable/installing/>`_ and running that python file (Windows/MacOS/Linux/BSD), or you can run the following command in terminal (Linux/BSD):

.. code:: bash

    sudo apt install python3-pip

If you're using brew (most likely for MacOS), you can install pip (along with the rest of Python 3) using brew:

.. code:: bash

    brew install python3

**Note: The creator of this software does not recommend the installation of python or pip using brew, and instead recommends that Python 3.7+ be installed using the installation candidates found on** `python.org <https://www.python.org/downloads/)>`_, **which include pip by default.**

Using Pip to install from PyPi
==============================
Fetching this repository from PyPi is the recommended way to install this package. From your terminal, run the following command:

.. code:: bash

    pip3 install add_juniper_software

And that's it! Now you can go right ahead to the quick-start guide!

Install from GitHub
===================
Not a big fan of pip? Well, you're weird, but weird is OK! I've written a separate script to help make installation from GitHub releases as easy as possible. To start, download the installation script and run it:

.. code:: bash

    wget https://raw.githubusercontent.com/EGuthrieWasTaken/add_juniper_software/main/source_install.py
    python3 source_install.py

After completing, the script will have downloaded the latest tarball release and extracted it into the working directory. Now, all you have to do is switch into the newly-extracted directory and run the install command:

.. code:: bash

    cd EGuthrieWasTaken-add_juniper_software-[commit_id]/
    python3 setup.py install

If you get a permission denied error, you may have to re-run using ``sudo`` or equivalent. Congratulations, you just installed add_juniper_software from GitHub releases! Feel free to check out the quick-start guide!

Alternatively, you can download the latest code from GitHub to install from source. **This is not recommended:**

.. code:: bash

    gh repo clone EGuthrieWasTaken/add_juniper_software 
    cd add_juniper_software/
    python3 setup.py install

And with a little bit of luck, you should have just installed from source!

-----------------
Quick-Start Guide
-----------------
Getting started with this package is easy! Just run ``add-juniper-software`` from your machine! Use the ``-h`` flag to see the help menu!

.. code:: bash

    add-juniper-software -h

----------------------------------
Documentation |readthedocs status|
----------------------------------
Documentation for this project can be found on `Read the Docs <https://add_juniper_software.readthedocs.io/en/latest>`_. Otherwise, feel free to browse the source code within the repository! It is (hopefully) well-documented...
