########################## THE TOON LAND DLC ##########################
# Filename: HackerCrypt.py
# Created by: Cody/Fd Green Cat Fd (January 31st, 2013)
####
# Description:
#
# Cryptography algorithm written by Cody/Fd Green Cat Fd in 2011 for
# Team FD's public releases.
####

from base64 import b64encode, b64decode
from binascii import hexlify, unhexlify
from random import randrange
from bz2 import compress as compress_bz2
from bz2 import decompress as decompress_bz2
from zlib import compress as compress_zlib
from zlib import decompress as decompress_zlib
from sha import sha as sha1

class HackerCrypt:

    __version__ = 'v1.2.0.3'

    def __init__(self):
        self.MAGIC = sha1('[TL]').digest()
        self.KEY   = sha1('TL-Cookies').digest()

    def makeIV(self):
        iv = ''
        for i in range(4):
            iv += chr(randrange(256))
        return iv

    def rc4(self, data, key):
        j = 0
        s = range(256)
        for i in range(256):
            j = (j + s[i] + ord(key[i % len(key)])) % 256
            s[i], s[j] = s[j], s[i]
        j = i = 0
        results = []
        for c in data:
            j = (j + 1) % 256
            i = (i + s[j]) % 256
            s[j], s[i] = s[i], s[j]
            results.append(chr(ord(c) ^ s[(s[j] + s[i]) % 256]))
        return ''.join(results)

    def encode(self, data):
        return b64encode(hexlify(data))

    def decode(self, encoding):
        return unhexlify(b64decode(encoding))

    def compress(self, data):
        bz2 = ('x\x9c' + compress_bz2(data)[4:])
        return ('BZh9' + compress_zlib(bz2)[2:])

    def decompress(self, compression):
        bz2 = (decompress_zlib('x\x9c' + compression[4:]))
        return (decompress_bz2('BZh9' + bz2[2:]))

    def encrypt(self, data):
        compression = self.compress(data)
        encoding = self.encode(compression)
        data = (self.MAGIC + encoding)
        iv = self.makeIV()
        key = (self.KEY + iv)
        return compress_zlib(iv + self.rc4(data, key))

    def decrypt(self, encryption):
        decompression = decompress_zlib(encryption)
        if len(decompression) < 4:
            return ''
        iv = decompression[:4]
        data = decompression[4:]
        key = (self.KEY + iv)
        data = self.rc4(data, key)
        if not data.startswith(self.MAGIC):
            return None
        decoding = self.decode(data[len(self.MAGIC):])
        return self.decompress(decoding)