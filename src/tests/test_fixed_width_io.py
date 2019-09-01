import unittest
import context
from fixed_width.io import FixedWidthFileSpec, FixedWidthFileReader, FixedWidthFileWriter, _generate_random_string
import tempfile 

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

class FixedWidthFileReaderTest(unittest.TestCase):
    def setUp(self):
        self.spec = FixedWidthFileSpec({
            "ColumnNames":"f1, f2, f3",
            "Offsets":"2,5,2",
            "InputEncoding":"windows-1252",
            "IncludeHeader":"False",
            "OutputEncoding":"utf-8"
        })
        self.temp_input_file = tempfile.NamedTemporaryFile("w")
        self.temp_input_file.write("123456789\n")
        self.temp_input_file.write("abcdefghi")
        self.temp_input_file.flush()
        self.temp_input_file.seek(0)

    def tearDown(self):
        self.temp_input_file.close()

    def test_iterate_and_parse(self):
        with FixedWidthFileReader(self.temp_input_file.name, self.spec) as fwr:
            i_fwr = iter(fwr)
            digit_row = next(i_fwr)
            alphabet_row = next(i_fwr)

            self.assertEqual(digit_row, ["12","34567","89"])
            self.assertEqual(alphabet_row, ["ab","cdefg","hi"])
        
class FixedWidthFileWriterTest(unittest.TestCase):
    def setUp(self):
        import tempfile 
        self.spec = FixedWidthFileSpec({
            "ColumnNames":"f1, f2, f3",
            "Offsets":"2,5,2",
            "InputEncoding":"windows-1252",
            "IncludeHeader":"True",
            "OutputEncoding":"utf-8"
        })

    def test_convert_row_to_fixed_width_line(self):
        fww = FixedWidthFileWriter("some_unused_file", self.spec)
        line = fww.convert_to_fixed_width_line(["1","242","23"])

        self.assertEqual(line, " 1  24223")

    def test_generate_random_string(self):
        max_length = 10
        random_string = _generate_random_string(max_length)
        self.assertLessEqual(len(random_string), max_length)

    def test_write_row(self):
        output_tmp_file = tempfile.NamedTemporaryFile("r")

        with FixedWidthFileWriter(output_tmp_file.name, self.spec) as fww:
            fww.writerow(["1","242","23"])

        i_outfile = iter(output_tmp_file)
        header = next(i_outfile)
        line = next(i_outfile)

        self.assertEqual(header, "f1   f2f3\n")
        self.assertEqual(line, " 1  24223\n")
if __name__ == "__main__":
    unittest.main()