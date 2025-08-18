import unittest
from main import safe_int_convert

class TestYtAnalyzer(unittest.TestCase):
    def test_safe_int_convert_valid(self):
        self.assertEqual(safe_int_convert("123"), 123)
        self.assertEqual(safe_int_convert(456), 456)
        
    def test_safe_int_convert_invalid(self):
        self.assertEqual(safe_int_convert("abc"), 0)
        self.assertEqual(safe_int_convert(None), 0)
        self.assertEqual(safe_int_convert(""), 0)

if __name__ == '__main__':
    unittest.main()