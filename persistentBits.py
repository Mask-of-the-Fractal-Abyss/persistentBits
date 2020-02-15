import os.path

class StorageLocation:
    # if valuelength is not provided, storage will automatically be in list form.
    def __init__(self, keylength, valuelength=None, path="./bits.b", debug=False, List=False):
        self.keylength = keylength
        if valuelength is None or List or valuelength == 0:
            valuelength = 0
            List = True
        self.valuelength = valuelength
        self.path = path
        self.debug = debug
        self.isList = List
        if not os.path.isfile(self.path):
            if self.debug:
                print("File not found, creating file...")
        self.data = self.getImmutableData()
        self.datalength = len(self.data)
        self.length = len(self)
        self.inRange = lambda: range(0, len(self.data), self.keylength + self.valuelength)

    # returns the file contents as a bytearray, or bytes, and stores it in self.data
    def getData(self, immutable=False):
        with open(self.path, "rb") as f:
            b = f.read()
            self.data = b
            if immutable:
                return b
            return bytearray(b)

    # clears the file contents
    def clear(self):
        with open(self.path, "w") as f:
            f.write("")

    # sets the entire file contents equal to (b)
    def write(self, b):
        b = bytes(b)
        with open(self.path, "wb") as f:
            if self.debug:
                print(f"Writing: {b}")
            f.write(b)
            self.datalength = len(b)
            self.data = b
    
    def getImmutableData(self): return self.getData(immutable=True)

    # gets raw index of the first occurance of bytes (e) in the file
    def index(self, e, searchForKey=True): # search for key or value
        t = type(e)
        if not (t == bytes or t == bytearray):
            print(f"{e} parameter (e) must be of type bytes or bytearray.  Is type {type(e)}\n")
            raise TypeError
        d = lambda : 0
        if searchForKey:
            d = lambda : self.data[i : i + self.keylength]        
        else:
            d = lambda : self.data[i + self.keylength : i + self.keylength + self.valuelength]
        for i in self.inRange():
            if d() == e:
                return i // self.keylength + self.valuelength - 1
        return None

    # indexing a file in dict form instead of list form will set the value of the nth key
    def __setitem__(self, key, val):
        if len(val) != self.valuelength:
            print("value in setitem is not of length self.valuelength")
            raise IndexError
        b = bytearray(self.data)
        t = type(key)
        if type(val) is int:
            val = bytes(chr(val), 'utf-8')
        elif type(val) is str:
            val = bytes(val, 'utf-8')
        if t is int:
            i = key * (self.keylength + self.valuelength)
            if self.debug:
                print(f"Writing {val} at {i}")
            if not i in range(len(self)):
                print(i)
                print(f"index {i} > {self.datalength} out of bounds {key}")
                raise IndexError
            if not self.isList:
                n = self.valuelength
                i += self.keylength
            else:
                n = self.keylength
            for j in range(n):
                b[i+j] = val[j]
        elif t in [bytearray, bytes, str]:
            if t is str:
                key = bytes(key, 'utf-8')
            i = self.index(key) + self.keylength - self.valuelength
            if i < 0:
                print(f"Item with key {key} not found.")
                raise KeyError
            if self.isList:
                print("""
Index must be of type int when self.isList is True.
""")
                raise TypeError
            if self.debug:
                print(f"Writing: {val} at {i}")
            for j in range(self.valuelength):
                b[i+j] = val[j]
        self.write(b)
        return self.data    

    def __getitem__(self, key):
        t = type(key)
        if t is int:
            n = key * (self.keylength + self.valuelength)
            return self.data[n:n+self.keylength]
        elif t in [bytearray, bytes, str]:
            if t is str:
                key = bytes(key, 'utf-8')
            if len(key) != self.keylength:
                print(key, "not a valid key length.")
                raise KeyError
            index = self.index(key) * (self.keylength + self.valuelength) 
            if index is None and self.isList:
                print("""
Index must be of type int when self.isList is True.
""")
                raise TypeError
            i = index + self.keylength
            if i < 0:
                print(f"Item with key {key} not found.")
                raise KeyError
            return self.data[i:i+self.valuelength]
        raise TypeError         

    def __len__(self):
        return self.datalength

    def __str__(self):
        return str(self.getImmutableData())
