django-graceful-session-cleanup
===============================

A simple management command that can delete expired sessions from large session tables without killing the site.

The main use case is if you have a live application with millions of stale sessions in the database. Runnung the
regular ``python manage.py cleanup`` will potentially lock your database for hours, essentially killing your site.

With ``django-graceful-session-cleanup`` you can gradually delete all the sessions.

To achieve this it will always only delete a small amount of the expired sessions per query and then sleep for
a few seconds. There are commandline options to control interval, sleep time and amount of sessions to delete
per interval.


Installation
------------

install the package::

    pip install django-graceful-session-cleanup

add it to ``INSTALLED_APPS``::

    INSTALLED_APPS = [
    	....
    	'graceful_session_cleanup',
    ]

run the management command::

    python manage.py graceful_session_cleanup


There are a few options you can use::

    python manage.py graceful_session_cleanup --sleep-seconds 9 --delete-count 1000 --iteration-count 200

This will delete ``1000`` expired session entries, wait for ``5`` seconds so other processes can use the
database and then repeat this ``200`` times. Depending on database load (assuming deleting takes ``1s``) this
will take ``(9s + 1s) * 200 = 2000s``.


there is help on the commandline::

    $ python manage.py help graceful_session_cleanup
    Usage: django graceful_session_cleanup [options]

    Can be run as a cronjob or directly to clean out old data from the database (only expired sessions at the moment). Does this in a live db friendly way by never hogging the connection too long.

    Options:
      -v VERBOSITY, --verbosity=VERBOSITY
                            Verbosity level; 0=minimal output, 1=normal output,
                            2=all output
      --settings=SETTINGS   The Python path to a settings module, e.g.
                            "myproject.settings.main". If this isn't provided, the
                            DJANGO_SETTINGS_MODULE environment variable will be
                            used.
      --pythonpath=PYTHONPATH
                            A directory to add to the Python path, e.g.
                            "/home/djangoprojects/myproject".
      --traceback           Print traceback on exception
      -s SLEEP_SECONDS, --sleep-seconds=SLEEP_SECONDS
                            How long to sleep between each delete operation.
      -c DELETE_COUNT, --delete-count=DELETE_COUNT
                            How many expired sessions to delete per iteration.
      -i ITERATION_COUNT, --iteration-count=ITERATION_COUNT
                            How many iterations to run.
      --version             show program's version number and exit
      -h, --help            show this help message and exit