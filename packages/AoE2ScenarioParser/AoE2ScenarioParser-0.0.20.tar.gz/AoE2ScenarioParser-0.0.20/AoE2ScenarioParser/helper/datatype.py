class DataType:
    """ A class to identify what data you want to retrieve. This class has two parameters which are very useful.
        var:
            - Almost always a string representation of the data you want to retrieve. This project uses the types from:
                http://dderevjanik.github.io/agescx/formatscx/#format
                s: Signed integer       All integers (signed and unsigned) are parsed as little endian
                u: Unsigned integer     All integers (signed and unsigned) are parsed as little endian
                f: float
                c: Character string of fixed length
                (Empty): Is interpreted as regular byte data. In this project the '' is converted to 'data'
                str: Character string of variable length.
                    This type will read the number in bits given and parse it as an int. The number retrieved from it
                    will be the amount of bytes read as a character string.
            - Another option for the var parameter is to give a Struct (not Python struct) subclass as var. This will
            parse all DataType values in the Struct subclass. This can be handy for when blocks of data are repeated.
            - Per data type you can save how large the value is bit/byte wise. While this may be confusing not all
            values are in bit format. Some are in byte format.
                Bit format: [s, u, f, str]
                Byte format: [c, data]
            - To define a length to your data type, write the datatype with the length behind it (no whitespaces)
                Example 1:  s16             > A signed integer of 16 bits.
                Example 2:  f32             > A 32 bit floating point number.
                Example 3:  c4              > A 32 bit (4 bytes) character string.
                Example 4:  str16           > A 16 bit integer will be parsed (n). Now n bytes will be read as character
                                            string.
                Example 5:  TerrainStruct   > The TerrainStruct will be instantiated and DataTypes from that struct will
                                            be loaded in it's place.
        repeat:
            The amount of times the above datatype needs to be repeated
    """

    def __init__(self, var="0", repeat=1, log_value=False):
        self.var = var
        self._repeat = repeat
        self.log_value = log_value
        self._debug_retriever_name = "???"

    def to_simple_string(self):
        return str(self._repeat) + " * " + (self.var if type(self.var) is str else self.var.__name__)

    def __repr__(self):
        return f"[DataType] " + self.to_simple_string()

    @property
    def repeat(self):
        if self.log_value:
            print(f"[DataType] {self._debug_retriever_name} Retrieved as " + self.to_simple_string())
        return self._repeat

    @repeat.setter
    def repeat(self, value):
        if self.log_value:
            print(f"[DataType] {self._debug_retriever_name} Repeat set to {value} from: " + self.to_simple_string())
        self._repeat = value
