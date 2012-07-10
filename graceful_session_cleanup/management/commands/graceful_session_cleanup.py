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
        sleep_seconds = int(options['sleep_seconds'])
        delete_count = int(options['delete_count'])
        iteration_count = int(options['iteration_count'])
        from django.db import connection
        import time
        cursor = connection.cursor()
        i = 0
        while iteration_count>i:
            i += 1
            t0 = time.clock()
            self.stdout.write("starting iteration %s of %s...\n" % (i, iteration_count))
            actual_delete_count = cursor.execute("DELETE FROM django_session WHERE expire_date<now() LIMIT %s;", [delete_count])
            t = time.clock() - t0
            self.stdout.write("    deleted %s expired sessions in %s seconds in iteration %s of %s. sleeping for %s seconds...\n\n" % (actual_delete_count, t, i, iteration_count, sleep_seconds))
            time.sleep(sleep_seconds)
