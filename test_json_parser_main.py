#!/usr/bin/env python3
import os
import sys
import unittest

from json_parser_main import parser


class TestDemoModeAndModules(unittest.TestCase):
    """Check environment variable and required dependencies."""
    def setUp(self):
        self.lark_demo_mode = os.getenv('LARK_DEMO_MODE') or 'dependency'

    def test_environment_variable(self):
        """Validate LARK_DEMO_MODE environment variable."""
        valid_choices = ['standalone', 'dependency']
        self.assertIn(self.lark_demo_mode, valid_choices)

    def test_parser_module(self):
        """Check if `parser` is stand-alone or dependent on `lark`."""
        module = parser.__module__

        if self.lark_demo_mode == 'standalone':
            self.assertEqual(module, 'standalone_module')
        elif self.lark_demo_mode == 'dependency':
            self.assertEqual(module, 'lark.lark')

    def test_lark_installation(self):
        if self.lark_demo_mode == 'standalone':
            msg = '`lark` should not be installed for "standalone" mode'
            with self.assertRaises(ImportError, msg=msg):
                import lark
        elif self.lark_demo_mode == 'dependency':
            try:
                import lark
            except ImportError:
                self.fail('`lark` should be installed for "dependency" mode')


class TestJsonParser(unittest.TestCase):
    """Check behavior of parser instance."""
    def test_json_string(self):
        result = parser.parse('"some string"')
        expected = 'some string'
        self.assertEqual(result, expected)

    def test_json_number(self):
        result = parser.parse('3.14')
        expected = 3.14
        self.assertEqual(result, expected)

    def test_json_object(self):
        result = parser.parse('{"A": "some string", "B": 3.14}')
        expected = {'A': 'some string', 'B': 3.14}
        self.assertEqual(result, expected)

    def test_json_array(self):
        result = parser.parse('["some string", 3.14]')
        expected = ['some string', 3.14]
        self.assertEqual(result, expected)

    def test_json_true(self):
        result = parser.parse('true')
        expected = True
        self.assertEqual(result, expected)

    def test_json_false(self):
        result = parser.parse('false')
        expected = False
        self.assertEqual(result, expected)

    def test_json_null(self):
        result = parser.parse('null')
        expected = None
        self.assertEqual(result, expected)

    def test_nested_values(self):
        result = parser.parse('{"A": ["some string", 3.14], "B": {"C": [1, 5, 9]}}')
        expected = {'A': ['some string', 3.14], 'B': {'C': [1, 5, 9]}}
        self.assertEqual(result, expected)


if __name__ == '__main__':
    from unittest import main
    main()
