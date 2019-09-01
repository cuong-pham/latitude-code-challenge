import argparse
import sys, logging
from fixed_width.io import FixedWidthFileSpec, FixedWidthFileReader, fixed_width_to_csv
import json

def main(args):
    parser = argparse.ArgumentParser("Convert fixed-width file to csv")

    parser.add_argument("--input", dest="input_file", required = True,
                        help="input fixed width file")
   
    parser.add_argument("--spec", dest="spec_file", type=argparse.FileType("r"),
                        required = True,
                        help="input fixed width file")

    parser.add_argument("--output", dest="output_file", required=True,
                        default=sys.stdout,
                        help="output file")

    options = parser.parse_args(args)

    spec = FixedWidthFileSpec(json.load(options.spec_file))

    fixed_width_to_csv(options.input_file, options.output_file, spec)

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))