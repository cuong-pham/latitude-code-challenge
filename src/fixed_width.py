class FixedWidthFileSpec:
    config_keys = frozenset(["ColumnNames", "Offsets", "InputEncoding", "IncludeHeader", "OutputEncoding"])
    def __init__(self, spec: dict):
        intersection = spec.keys() & self.config_keys
        if len(intersection) != len(spec.keys()):
            raise ValueError("Unrecognised keys {}".format(intersection))
        
        self.cols = spec['ColumnNames'].split(',')
        self.col_widths = list(map(int, spec['Offsets'].split(',')))
        self.header = spec['IncludeHeader'] == 'True'
        self.input_encoding = spec['InputEncoding']
        self.output_encoding = spec['OutputEncoding']
    
    def __repr__(self):
        return '{type}{content}'.format(
            type=type(self),
            content=self.__dict__
        )
        