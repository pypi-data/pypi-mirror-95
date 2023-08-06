# Containers test classes.
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

import unittest

from io import StringIO
from unittest.mock import patch

from simpleline import App
from simpleline.render.containers import WindowContainer, ListRowContainer, ListColumnContainer, \
    KeyPattern
from simpleline.render.screen import UIScreen, InputState
from simpleline.render.widgets import TextWidget

from .widgets_test import BaseWidgets_TestCase


class Containers_TestCase(BaseWidgets_TestCase):

    def _test_callback(self, data):
        pass

    def test_listrow_container(self):
        c = ListRowContainer(columns=2,
                             items=[self.w2, self.w3, self.w5],
                             columns_width=10,
                             spacing=2,
                             numbering=False)
        c.render(25)

        expected_result = [u"Test        Test 2",
                           u"Test 3"]
        res_lines = c.get_lines()

        self.evaluate_result(res_lines, expected_result)

    def test_empty(self):
        c = ListRowContainer(columns=1)

        c.render(10)
        result = c.get_lines()

        self.assertEqual(len(result), 0)

    def test_more_columns_than_widgets(self):
        c = ListRowContainer(columns=3, items=[self.w1], columns_width=40, numbering=False)
        c.render(80)

        expected_result = [u"Můj krásný dlouhý text"]

        res_lines = c.get_lines()
        self.evaluate_result(res_lines, expected_result)

    def test_listrow_wrapping(self):
        # spacing is 3 by default
        c = ListRowContainer(2,
                             [self.w1, self.w2, self.w3, self.w4],
                             columns_width=15,
                             numbering=False)
        c.render(25)

        expected_result = [u"Můj krásný        Test",
                           u"dlouhý text",
                           u"Test 2            Krásný dlouhý",
                           u"                  text podruhé"]
        res_lines = c.get_lines()
        self.evaluate_result(res_lines, expected_result)

    def test_newline_wrapping(self):
        widgets = [TextWidget("Hello"), TextWidget("Wrap\nthis\ntext"), TextWidget("Hi"),
                   TextWidget("Hello2")]

        c = ListRowContainer(3, widgets, columns_width=6, spacing=1, numbering=False)
        c.render(80)

        expected_result = [u"Hello  Wrap   Hi",
                           u"       this",
                           u"       text",
                           u"Hello2"]
        res_lines = c.get_lines()
        self.evaluate_result(res_lines, expected_result)

    def test_listcolumn_container(self):
        c = ListColumnContainer(columns=2,
                                items=[self.w2, self.w3, self.w5],
                                columns_width=10,
                                spacing=2,
                                numbering=False)
        c.render(25)

        expected_result = [u"Test        Test 3",
                           u"Test 2"]
        res_lines = c.get_lines()
        self.evaluate_result(res_lines, expected_result)

    def test_listcolumn_wrapping(self):
        # spacing is 3 by default
        c = ListColumnContainer(2,
                                [self.w1, self.w2, self.w3, self.w4],
                                columns_width=15,
                                numbering=False)
        c.render(25)

        expected_result = [u"Můj krásný        Test 2",
                           u"dlouhý text",
                           u"Test              Krásný dlouhý",
                           u"                  text podruhé"]
        res_lines = c.get_lines()
        self.evaluate_result(res_lines, expected_result)

    def test_add_new_container(self):
        c = ListRowContainer(columns=2,
                             items=[TextWidget("Ahoj")],
                             columns_width=15,
                             spacing=0,
                             numbering=False)

        expected_result = [u"Ahoj"]

        c.render(80)
        self.evaluate_result(c.get_lines(), expected_result)

        c.add(TextWidget("Nový widget"))
        c.add(TextWidget("Hello"))

        expected_result = [u"Ahoj           Nový widget",
                           u"Hello"]

        c.render(80)
        self.evaluate_result(c.get_lines(), expected_result)

    def test_column_numbering(self):
        # spacing is 3 by default
        c = ListColumnContainer(2, [self.w1, self.w2, self.w3, self.w4], columns_width=16)
        c.render(25)

        expected_result = [u"1) Můj krásný      3) Test 2",
                           u"   dlouhý text",
                           u"2) Test            4) Krásný dlouhý",
                           u"                      text podruhé"]
        res_lines = c.get_lines()
        self.evaluate_result(res_lines, expected_result)

    def test_row_numbering(self):
        # spacing is 3 by default
        c = ListRowContainer(2, [self.w1, self.w2, self.w3, self.w4], columns_width=16)
        c.render(25)

        expected_result = [u"1) Můj krásný      2) Test",
                           u"   dlouhý text",
                           u"3) Test 2          4) Krásný dlouhý",
                           u"                      text podruhé"]
        res_lines = c.get_lines()
        self.evaluate_result(res_lines, expected_result)

    def test_custom_numbering(self):
        # spacing is 3 by default
        c = ListRowContainer(2, [self.w1, self.w2, self.w3, self.w4], columns_width=20)
        c.key_pattern = KeyPattern("a {:d} a ")
        c.render(25)

        expected_result = [u"a 1 a Můj krásný       a 2 a Test",
                           u"      dlouhý text",
                           u"a 3 a Test 2           a 4 a Krásný dlouhý",
                           u"                             text podruhé"]
        res_lines = c.get_lines()
        self.evaluate_result(res_lines, expected_result)

    def test_window_container(self):
        c = WindowContainer(title="Test")

        c.add(TextWidget("Body"))
        c.render(10)

        expected_result = [u"Test",
                           u"",
                           u"Body"]

        res_lines = c.get_lines()
        self.evaluate_result(res_lines, expected_result)

    def test_window_container_with_multiple_items(self):
        c = WindowContainer(title="Test")

        c.add(TextWidget("Body"))
        c.add(TextWidget("Body second line"))
        c.render(30)

        expected_result = [u"Test",
                           u"",
                           u"Body",
                           u"Body second line"]

        res_lines = c.get_lines()
        self.evaluate_result(res_lines, expected_result)

    def test_window_container_wrapping(self):
        c = WindowContainer(title="Test")

        c.add(TextWidget("Body long line"))
        c.add(TextWidget("Body"))
        c.render(5)

        expected_result = [u"Test",
                           u"",
                           u"Body",
                           u"long",
                           u"line",
                           u"Body"]

        res_lines = c.get_lines()
        self.evaluate_result(res_lines, expected_result)

    def test_list_container_without_width(self):
        column_count = 3
        spacing_width = 3
        c = ListRowContainer(column_count, spacing=spacing_width, numbering=False)

        c.add(TextWidget("AAAA"))
        c.add(TextWidget("BBBB"))
        c.add(TextWidget("CCCCC"))  # this line is too long
        c.add(TextWidget("DDDD"))

        expected_col_width = 4
        expected_spacing_sum = 2 * spacing_width  # three columns so 2 spacing between them
        render_width = (column_count * expected_col_width) + expected_spacing_sum
        c.render(render_width)

        expected_result = [u"AAAA   BBBB   CCCC",
                           u"              C",
                           u"DDDD"]

        res_lines = c.get_lines()
        self.evaluate_result(res_lines, expected_result)

    def test_list_container_too_small(self):
        # to be able to render this container we need at least 11 width
        # 8 will take only spacing and then 1 for every column
        c = ListRowContainer(3, spacing=4, numbering=False)

        c.add(TextWidget("This can't be rendered."))
        c.add(TextWidget("Because spacing takes more space than maximal width."))
        c.add(TextWidget("Exception will raise."))

        with self.assertRaisesRegex(ValueError, "Columns width is too small."):
            c.render(10)

    def test_list_container_too_small_turn_off_numbering(self):
        # to be able to render this container we need
        # 11 width + three times numbers (3 characters) = 20
        #
        # 8 will take only spacing and then 1 for every column
        c = ListRowContainer(3, spacing=4, numbering=True)

        c.add(TextWidget("This can't be rendered."))
        c.add(TextWidget("Because spacing takes more space than maximal width."))
        c.add(TextWidget("Exception will raise with info to turn off numbering."))

        with self.assertRaisesRegex(ValueError, "Increase column width or disable numbering."):
            c.render(19)


@patch('simpleline.input.input_handler.InputHandlerRequest._get_input')
@patch('sys.stdout', new_callable=StringIO)
class ContainerInput_TestCase(unittest.TestCase):

    def setUp(self):
        self._callback_id = None
        self._callback_called = None

    def _prepare_callbacks(self, container, count):
        for i in range(count):
            container.add(TextWidget("Test"), self._callback, i + 1)

    def test_list_widget_input_processing(self, out_mock, in_mock):
        # call first container callback
        in_mock.return_value = "2"

        screen = ScreenWithListWidget(3)

        App.initialize()
        App.get_scheduler().schedule_screen(screen)
        App.run()

        self.assertEqual(1, screen.container_callback_input)

    # TEST 0 or less as user input

    def test_list_input_processing_input_0(self, out_mock, in_mock):
        c = ListRowContainer(1)

        self._prepare_callbacks(c, 3)

        self.assertFalse(c.process_user_input("0"))

    def test_list_input_processing_negative_number(self, out_mock, in_mock):
        c = ListRowContainer(1)

        self._prepare_callbacks(c, 3)

        self.assertFalse(c.process_user_input("-2"))

    def test_list_input_processing_exceeded(self, out_mock, in_mock):
        c = ListRowContainer(1)

        self._prepare_callbacks(c, 2)

        self.assertFalse(c.process_user_input("3"))

    def test_list_without_callback(self, out_mock, in_mock):
        c = ListRowContainer(1)

        c.add(TextWidget("Test"))

        self.assertTrue(c.process_user_input("1"))

    def test_list_callback_without_data(self, out_mock, in_mock):
        c = ListRowContainer(1)

        c.add(TextWidget("Test"), self._callback)

        self.assertTrue(c.process_user_input("1"))
        self.assertIsNone(self._callback_called)

    def test_list_correct_input_processing(self, out_mock, in_mock):
        c = ListRowContainer(1)

        self._prepare_callbacks(c, 3)

        self.assertTrue(c.process_user_input("2"))

        self.assertEqual(self._callback_called, 2)

    def test_list_wrong_input_processing(self, out_mock, in_mock):
        c = ListRowContainer(1)

        self._prepare_callbacks(c, 3)

        self.assertFalse(c.process_user_input("c"))

    def test_list_input_processing_none(self, out_mock, in_mock):
        c = ListRowContainer(1)

        self._prepare_callbacks(c, 2)

        self.assertFalse(c.process_user_input(None))

    def _callback(self, data):
        self._callback_called = data


class ScreenWithListWidget(UIScreen):

    def __init__(self, widgets_count):
        super().__init__()
        self._widgets_count = widgets_count
        self._list_widget = None
        self.container_callback_input = -1

    def refresh(self, args=None):
        super().refresh(args)

        self._list_widget = ListRowContainer(2)
        for i in range(self._widgets_count):
            self._list_widget.add(TextWidget("Test %s" % i), self._callback, i)

        self.window.add(self._list_widget)

    def input(self, args, key):
        self.close()
        if self._list_widget.process_user_input(key):
            return InputState.PROCESSED

        return InputState.DISCARDED

    def _callback(self, data):
        self.container_callback_input = data
