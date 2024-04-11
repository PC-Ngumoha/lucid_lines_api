"""
Tests for custom commands created specifically for this project
"""
from typing import Any
from unittest.mock import patch

from psycopg import OperationalError as PsycopgError

from django.core.management import call_command
from django.test import TestCase
from django.db.utils import OperationalError


@patch('core.management.commands.await_db.Command.check')
class TestCommand(TestCase):
    """Tests commands"""

    def test_command_called(self, patched_check: Any) -> None:
        """Tests that the command is called"""
        patched_check.return_value = True

        call_command('await_db')

        patched_check.assert_called_once_with(databases=['default'])

    @patch('time.sleep')
    def test_command_side_effect(self, patched_sleep: Any,
                                 patched_check: Any) -> None:
        """Tests a real case simulation of the use of this command."""
        patched_check.side_effect = [OperationalError] * 3 + \
                                    [PsycopgError] * 2 + [True]

        call_command('await_db')

        self.assertEqual(patched_check.call_count, 6)
        patched_sleep.assert_called()
        patched_check.assert_called_with(databases=['default'])
