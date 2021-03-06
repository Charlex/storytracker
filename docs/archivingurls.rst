Archiving URLs
==============

From the command line
---------------------

Once installed, you can start using storytracker's command-line tools immediately, like :py:func:`storytracker.archive`.

.. code-block:: bash

    $ storytracker-archive http://www.latimes.com

That should pour out a scary looking stream of data to your console. That is the content of the page you requested compressed using `gzip <http://en.wikipedia.org/wiki/Gzip>`_.
If you'd prefer to see the raw HTML, add the ``--do-not-compress`` option.

.. code-block:: bash

    $ storytracker-archive http://www.latimes.com --do-not-compress

You could save that yourself using `a standard UNIX pipeline <http://en.wikipedia.org/wiki/Pipeline_%28Unix%29>`_.

.. code-block:: bash

    $ storytracker-archive http://www.latimes.com --do-not-compress > archive.html

But why do that when :py:func:`storytracker.create_archive_filename` will work behind the scenes to automatically come
up with a tidy name that includes both the URL and a timestamp?

.. code-block:: bash

    $ storytracker-archive http://www.latimes.com --do-not-compress --output-dir="./"

Run that and you'll see the file right away in your current directory.

.. code-block:: bash

    # Try opening the file you spot here with your browser
    $ ls | grep .html


Using Python
------------

UNIX-like systems typically come equipped with a built in method for scheduling tasks known as `cron <http://en.wikipedia.org/wiki/Cron>`_.
To utilize it with storytracker, one approach is to write a Python script that retrieves a series of sites each time it is run.

.. code-block:: python

    import storytracker

    SITE_LIST = [
        # A list of the sites to archive
        'http://www.latimes.com',
        'http://www.nytimes.com',
        'http://www.kansascity.com',
        'http://www.knoxnews.com',
        'http://www.indiatimes.com',
    ]
    # The place on the filesystem where you want to save the files
    OUTPUT_DIR = "/path/to/my/directory/"

    # Runs when the script is called with the python interpreter
    # ala "$ python cron.py"
    if __name__ == "__main__":
        # Loop through the site list
        for s in SITE_LIST:
            # Spit out what you're doing
            print "Archiving %s" % s
            try:
                # Attempt to archive each site at the output directory
                # defined above
                storytracker.archive(s, output_dir=OUTPUT_DIR)
            except Exception as e:
                # And just move along and keep rolling if it fails.
                print e

Scheduling with cron
--------------------

Then edit the cron file from the command line.

.. code-block:: bash

    $ crontab -e

And use `cron's custom expressions <http://en.wikipedia.org/wiki/Cron#Examples>`_ to schedule the job however you'd like.
This example would schedule the script to run a file like the one above at the top of every hour. Though it assumes
that ``storytracker`` is available to your global Python installation at ``/usr/bin/python``. If you are using a virtualenv or different Python
configuration, you should begin the line with a path leading to that particular ``python`` executable.

.. code-block:: bash

    0 * * * *  /usr/bin/python /path/to/my/script/cron.py
