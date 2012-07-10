#-*- coding: utf-8 -*-
from optparse import make_option
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = "Can be run as a cronjob or directly to clean out old data from the database (only expired sessions at the moment). Does this in a live db friendly way by never hogging the connection too long."
    option_list = BaseCommand.option_list + (
        make_option('-s', '--sleep-seconds',
            dest='sleep_seconds',
            default=5,
            help='How long to sleep between each delete operation.'
        ),
        make_option('-c', '--delete-count',
            dest='delete_count',
            default=500,
            help='How many expired sessions to delete per iteration.'
        ),
        make_option('-i', '--iteration-count',
            dest='iteration_count',
            default=25,
            help='How many iterations to run.'
        ),
        )

    def handle(self, *args, **options):
        from django.db import connection
        import time
        import datetime

        sleep_seconds = int(options['sleep_seconds'])
        delete_count = int(options['delete_count'])
        iteration_count = int(options['iteration_count'])

        start_at = datetime.datetime.now()
        blocked_time = datetime.timedelta(seconds=0)

        self.stdout.write("started at %s...\n" % (start_at, ))

        cursor = connection.cursor()
        i = 0
        while iteration_count>i:
            i += 1
            iteration_start_at = datetime.datetime.now()
            self.stdout.write("    started iteration %s of %s...\n" % (i, iteration_count))
            actual_delete_count = cursor.execute("DELETE FROM django_session WHERE expire_date<now() LIMIT %s;", [delete_count])
            iteration_duration = datetime.datetime.now() - iteration_start_at
            blocked_time += iteration_duration
            iteration_duration_in_seconds = iteration_duration.seconds + iteration_duration.microseconds / 1E6
            self.stdout.write("        deleted %s expired sessions in %s seconds\n" % (actual_delete_count, iteration_duration_in_seconds,))
            self.stdout.write("    finished iteration %s of %s (sleeping for %s seconds)...\n" % (i, iteration_count, sleep_seconds))
            time.sleep(sleep_seconds)
        end_at = datetime.datetime.now()
        self.stdout.write("finished at %s after running for %s and running queries for %s...\n\n" % (end_at, end_at-start_at, blocked_time))

