# Copyright 2014-2018 Laszlo Attila Toth
# Distributed under the terms of the GNU Lesser General Public License v3

import unittest


class TestCase(unittest.TestCase):
    maxDiff = None

    def set_up(self):
        pass

    def tear_down(self):
        pass

    def setUp(self):
        self.set_up()

    def tearDown(self):
        self.tear_down()

    assert_almost_equal = unittest.TestCase.assertAlmostEqual
    assert_count_equal = unittest.TestCase.assertCountEqual
    assert_dict_equal = unittest.TestCase.assertDictEqual
    assert_equal = unittest.TestCase.assertEqual
    assert_false = unittest.TestCase.assertFalse
    assert_greater = unittest.TestCase.assertGreater
    assert_greater_equal = unittest.TestCase.assertGreaterEqual
    assert_in = unittest.TestCase.assertIn
    assert_is = unittest.TestCase.assertIs
    assert_is_instance = unittest.TestCase.assertIsInstance
    assert_is_none = unittest.TestCase.assertIsNone
    assert_is_not = unittest.TestCase.assertIsNot
    assert_is_not_none = unittest.TestCase.assertIsNotNone
    assert_less = unittest.TestCase.assertLess
    assert_less_equal = unittest.TestCase.assertLessEqual
    assert_list_equal = unittest.TestCase.assertListEqual
    assert_logs = unittest.TestCase.assertLogs
    assert_multi_line_equal = unittest.TestCase.assertMultiLineEqual
    assert_not_almost_equal = unittest.TestCase.assertNotAlmostEqual
    assert_not_equal = unittest.TestCase.assertNotEqual
    assert_not_in = unittest.TestCase.assertNotIn
    assert_not_is_instance = unittest.TestCase.assertNotIsInstance
    assert_not_regex = unittest.TestCase.assertNotRegex
    assert_raises = unittest.TestCase.assertRaises
    assert_raises_regex = unittest.TestCase.assertRaisesRegex
    assert_regex = unittest.TestCase.assertRegex
    assert_sequence_equal = unittest.TestCase.assertSequenceEqual
    assert_set_equal = unittest.TestCase.assertSetEqual
    assert_true = unittest.TestCase.assertTrue
    assert_tuple_equal = unittest.TestCase.assertTupleEqual
    assert_warns = unittest.TestCase.assertWarns
    assert_warns_regex = unittest.TestCase.assertWarnsRegex
