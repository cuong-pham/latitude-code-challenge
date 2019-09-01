import logging
import itertools

class FixedWidthFileSpec:
    config_keys = frozenset(["ColumnNames", "Offsets", "InputEncoding", "IncludeHeader", "OutputEncoding"])
    def __init__(self, spec: dict):
        if self.config_keys != spec.keys():
            raise Exception("Spec must have all keys")
        
        self.col_widths = [int(o) for o in spec['Offsets'].split(',')]
        self.abs_offsets = [0] + list(itertools.accumulate(self.col_widths))
        self.cols = [col.strip() for col in spec['ColumnNames'].split(',')]
        
        if len(self.col_widths) != len(self.cols):
            raise Exception("Number of offsets and number of columns must be the same")
        
        self.has_header = spec['IncludeHeader'] == 'True'
        self.fixed_width_encoding = spec['InputEncoding']
        self.output_encoding = spec['OutputEncoding']

class FixedWidthFileReader:
    def __init__(self, src_file: str, spec: FixedWidthFileSpec):
        self.src_file = src_file
        self.spec = spec        
        
    def __enter__(self):
        self.open_file = open(self.src_file, "r", encoding=self.spec.fixed_width_encoding)
        return self        
   
    def __exit__(self, type, value, traceback):
        self.open_file.close()

    def __iter__(self):
        if self.spec.has_header:
            next(self.open_file)
            
        for line in self.open_file:
            data =  [
                line[start:end].strip()
                for start, end in zip(self.spec.abs_offsets, self.spec.abs_offsets[1:])
            ]
            yield data

class FixedWidthFileWriter:
    def __init__(self, dest_file: str, spec: FixedWidthFileSpec):
        self.dest_file = dest_file
        self.spec = spec        
    
    def __enter__(self):
        self.open_file = open(self.dest_file, "w", encoding = self.spec.fixed_width_encoding)
        if self.spec.has_header:
            self.writerow(self.spec.cols)
        return self

    def __exit__(self, type, value, traceback):
        self.open_file.close()

    def writerow(self, row: list) -> None:
        if self.open_file is None: 
            raise Exception("file is not open to write")
        
        self.open_file.write(self.convert_to_fixed_width_line(row)+"\n")

    def convert_to_fixed_width_line(self, row: list) -> str:
        _str = ""
        for width, string in zip(self.spec.col_widths, row):
            _str = _str + string.rjust(width)[:width]        
        return _str

def fixed_width_to_csv(input_file: str, output_file: str, spec: FixedWidthFileSpec, delim=',') -> None:
    import csv
    with FixedWidthFileReader(input_file, spec) as fwr, \
        open(output_file, "w", encoding=spec.output_encoding) as f:
        writer = csv.writer(f, delimiter=delim)
        if spec.has_header:
            writer.writerow(spec.cols)

        for line in fwr:
            writer.writerow(line)

def generate_fixed_width_file(output_file: str, spec: FixedWidthFileSpec, num_lines=50) -> None: 
    with FixedWidthFileWriter(output_file, spec) as fww:
        for _ in range(num_lines):
            row = [_generate_random_string(max_length = 6) for _ in range(len(spec.cols))]
            fww.writerow(row)

def _generate_random_string(max_length: int) -> str:
    import random, string
    return ''.join(
            random.choices(
                string.ascii_letters, 
                k = random.choices(range(1, max_length+1))[0]
            )
        )
