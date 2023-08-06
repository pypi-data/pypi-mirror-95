# Widgets test classes.
#
# This file is part of Simpleline Text UI library.
#
# Copyright (C) 2020  Red Hat, Inc.
#
# Simpleline is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Simpleline is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with Simpleline.  If not, see <https://www.gnu.org/licenses/>.
#

from unittest import TestCase

from simpleline.event_loop.ticket_machine import TicketMachine


class TicketMachine_TestCase(TestCase):

    def setUp(self):
        self._tickets = TicketMachine()

    def test_take_ticket(self):
        line_id = 0
        t = self._tickets.take_ticket(line_id)
        self.assertEqual(t, 0)
        t2 = self._tickets.take_ticket(line_id)
        self.assertNotEqual(t, t2)

    def test_check_ticket(self):
        line_id = 0
        t = self._tickets.take_ticket(line_id)

        self.assertFalse(self._tickets.check_ticket(line_id, t))

        self._tickets.mark_line_to_go(line_id)

        self.assertTrue(self._tickets.check_ticket(line_id, t))

    def test_mark_multiple_tickets(self):
        line_id = 0

        t1 = self._tickets.take_ticket(line_id)
        t2 = self._tickets.take_ticket(line_id)
        t3 = self._tickets.take_ticket(line_id)
        t4 = self._tickets.take_ticket(line_id)

        self._tickets.mark_line_to_go(line_id)
        self.assertTrue(self._tickets.check_ticket(line_id, t1))
        self.assertTrue(self._tickets.check_ticket(line_id, t2))
        self.assertTrue(self._tickets.check_ticket(line_id, t3))
        self.assertTrue(self._tickets.check_ticket(line_id, t4))

    def test_mark_one_of_lines(self):
        line_id1 = "a"
        line_id2 = "b"

        t1 = self._tickets.take_ticket(line_id1)
        t2 = self._tickets.take_ticket(line_id1)
        t3 = self._tickets.take_ticket(line_id2)
        t4 = self._tickets.take_ticket(line_id2)

        self._tickets.mark_line_to_go(line_id1)

        self.assertTrue(self._tickets.check_ticket(line_id1, t1))
        self.assertTrue(self._tickets.check_ticket(line_id1, t2))
        self.assertFalse(self._tickets.check_ticket(line_id2, t3))
        self.assertFalse(self._tickets.check_ticket(line_id2, t4))

    def text_check_re_using(self):
        line_id = "a"

        t1 = self._tickets.take_ticket(line_id)
        t2 = self._tickets.take_ticket(line_id)
        t3 = self._tickets.take_ticket(line_id)

        self._tickets.mark_line_to_go(line_id)

        self.assertTrue(self._tickets.check_ticket(line_id, t1))
        self.assertTrue(self._tickets.check_ticket(line_id, t2))

        # it needs to be False when you check it again
        self.assertFalse(self._tickets.check_ticket(line_id, t1))
        self.assertFalse(self._tickets.check_ticket(line_id, t2))

        # take new ticket and mark the line again

        t4 = self._tickets.take_ticket(line_id)

        self._tickets.mark_line_to_go(line_id)

        # old checked tickets should be invalid now
        self.assertFalse(self._tickets.check_ticket(line_id, t1))
        self.assertFalse(self._tickets.check_ticket(line_id, t2))
        # old not checked ticket should work
        self.assertTrue(self._tickets.check_ticket(line_id, t3))
        # new tickets should work
        self.assertTrue(self._tickets.check_ticket(line_id, t4))
