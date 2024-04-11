"""
Custom DB command: Causes app to await DB startup b4 making requests.
"""
import time
from typing import Any

from psycopg import OperationalError as PsycopgError

from django.core.management.base import BaseCommand
from django.db.utils import OperationalError


class Command(BaseCommand):
    """Wait for DB to start before connecting and making requests to it.
    """
    help = __doc__

    def handle(self, *args: Any, **options: Any) -> str | None:
        """Handles the running of the command"""
        self.stdout.write('Checking for DB availability...')
        db_up = False
        while db_up is False:
            try:
                self.check(databases=['default'])
                db_up = True
            except (PsycopgError, OperationalError):
                self.stderr.write(
                    self.style.WARNING('DB not available, trying again...')
                )
                time.sleep(1)
        self.stdout.write(
            self.style.SUCCESS('DB is available.')
        )
        return None
