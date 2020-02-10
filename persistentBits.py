import os.path

class StorageLocation:
    # if valuelength is not provided, storage will automatically be in list form.
    def __init__(self, keylength, valuelength=None, path="./bits.b", debug=False, List=False):
        self.keylength = keylength
        if valuelength is None or List:
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
        with open(self.path, "wb") as f:
            if self.debug:
                print(f"Writing: {b}")
            f.write(b)
            self.data = b
    
    def getImmutableData(self): return self.getData(immutable=True)

    # gets raw index of the first occurance of bytes (e) in the file
    def index(self, e, searchForKey=True): # search for key or value
        t = type(e)
        if not (t == bytes or t == bytearray):
            print(f"{e} parameter (e) must be of type bytes or bytearray")
            raise TypeError
        d = 0
        if not searchForKey:
            d = self.valuelength
        for i in self.inRange():
            if self.data[i + d : i + d + self.keylength] == e:
                return i // self.keylength + self.valuelength
        return None

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
            if i in len(self.data):
                print(f"index out of bounds {key}")
                raise IndexError
            if self.debug:
                print(f"Writing {val} at {i}")
            for j in range(self.keylength):
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
Used getitem to call self.index when self.isList True.  Illadvised.
key should be of type int for list style storage""")
                raise TypeError
            for j in range(self.valuelength):
                print(i, j, val, type(i), type(j))
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
            i = self.index(key) - self.valuelength
            if i < 0:
                print(f"Item with key {key} not found.")
                raise KeyError
            if self.isList:
                print("""
Used getitem to call self.index when self.isList True.  Illadvised.
key should be of type int for list style storage""")
                raise TypeError
            return self.data[i+self.keylength:i+self.keylength+self.valuelength]
        raise TypeError         

    def __len__(self):
        return len(self.data)

    def __str__(self):
        return str(self.getImmutableData())
