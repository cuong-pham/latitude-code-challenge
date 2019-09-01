import unittest
import context
from fixed_width.io import FixedWidthFileSpec, FixedWidthFileReader, FixedWidthFileWriter


class FixedWidthFileSpecTest(unittest.TestCase):
    def test_incorrect_missing_keys_in_spec(self):
        spec_dict = {
            "ColumnNames":"f1, f2, f3",
            "Offsets":"3,12,3",
        }

        with self.assertRaises(Exception) as c:
            FixedWidthFileSpec(spec_dict)

        self.assertEqual(str(c.exception), "Spec must have all keys")

    def test_offset_length_not_equal_columns_length(self):
        spec_dict = {
            "ColumnNames":"f1, f2, f3, f4, f5, f6, f7, f8, f9",
            "Offsets":"3,12,3,2,13,2,10,13,3,13",
            "InputEncoding":"windows-1252",
            "IncludeHeader":"True",
            "OutputEncoding":"utf-8"
        }

        with self.assertRaises(Exception) as c:
            FixedWidthFileSpec(spec_dict)

        self.assertEqual(str(c.exception), "Number of offsets and number of columns must be the same")

    def test_correct_spec(self):
        spec_dict = {
            "ColumnNames":"f1, f2, f3",
            "Offsets":"3,12,3",
            "InputEncoding":"windows-1252",
            "IncludeHeader":"True",
            "OutputEncoding":"utf-8"
        }

        spec = FixedWidthFileSpec(spec_dict)

        self.assertEqual(spec.cols, ["f1","f2","f3"])
        self.assertTrue(spec.has_header)
        self.assertEqual(spec.fixed_width_encoding, "windows-1252")
        self.assertEqual(spec.output_encoding, "utf-8")
        self.assertEqual(spec.col_widths, [3,12,3] )
        self.assertEqual(spec.abs_offsets, [0,3,15,18])

if __name__ == "__main__":
    unittest.main()