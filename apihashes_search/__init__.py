# (c) 2025, @section_remadev

from ctypes import *
import zlib, bisect

tokens = None
decomp = None

class HashRecBin(Structure):
    _fields_ = [ ('hash', c_uint64), ('off', c_uint64 ) ]

    def __lt__(self,other):
        return self.hash < other

def LoadHashes(fileName):
    global tokens, decomp

    with open(fileName, "rb") as f:
        b = bytes(f.read())
        decomp = zlib.decompress(b)
        numItems = int(len(decomp) / 16)
        tokensArr = HashRecBin * numItems
        tokens = tokensArr.from_buffer_copy(decomp)


def FindHash(value):
    i = bisect.bisect_left(tokens, value)
    if i >= len(tokens):
        return None
    if tokens[i].hash != value:
        return None
    fname = ""
    for c in decomp[tokens[i].off:]:
        if c == 0:
            break
        fname = fname + chr(c)
    return fname

def main():
    print('Apihashes test')
    LoadHashes("apihashes_storage.bin")
    print('hashes loaded')
    print(FindHash(0x20a))

if __name__ == "__main__":
    main()
