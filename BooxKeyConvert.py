#!/usr/bin/env python3
try:
    from Cryptodome.Cipher import DES
    from Cryptodome.Hash import MD5
except ModuleNotFoundError:
    from Crypto.Cipher import DES
    from Crypto.Hash import MD5
    from Crypto import version_info
    if version_info[0] == 2:
        raise SystemExit('Need either pycryptodome or pycryptodomex, NOT pycrypto!')
import sys
from base64 import b64decode
from base64 import b64encode

def decryptStr(tmpKey: bytes, string: str) -> str:
    if len(string) != 44:
        print('Key is not the correct length of 44')
        return None
    try:
        data: bytes = b64decode(string)
    except:
        print('Key is not valid base64 encoding')
        return None;
    if len(data) != 33:
        print('Base64 decoding of key returned length less than 33')
        return None;
    cypher = DES.new(tmpKey, DES.MODE_CFB, iv=b'\xff' * 8, segment_size=64)
    data = cypher.decrypt(data)
    try:
        out: str = data.decode()
    except:
        print('Key did not decode correctly for this model')
        return None
    if out[32] != '\n': print('Decrypted key missing standard newline')
    return out[:32]

def encryptStr(tmpKey: bytes, string: str) -> str:
    cypher = DES.new(tmpKey, DES.MODE_CFB, iv=b'\xff' * 8, segment_size=64)
    out: str = b64encode(cypher.encrypt(bytearray(string.upper()+'\n', 'ascii'))).decode()
    return out

if __name__ == '__main__':
    if len(sys.argv) >= 3:
        model = sys.argv[1];
        tmpKey: bytes = MD5.new((model * 2).encode()).digest()[:8]
        for i in range(2, len(sys.argv)):
            if i > 2: print()
            x = sys.argv[i]
            print(x)
            y = decryptStr(tmpKey, x)
            if y != None:
                print(y)
                z = encryptStr(tmpKey, y)
                if z != x: print('Key does not "round-trip" correctly')
    else: print('Usage: BooxKeyConvert.py <model> <settings> <upgrade>')
