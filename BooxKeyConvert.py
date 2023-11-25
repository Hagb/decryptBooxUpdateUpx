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
    try:
        cipher = DES.new(tmpKey, DES.MODE_CFB, iv=b'\xff' * 8, segment_size=64)
        out: str = cipher.decrypt(b64decode(string)).decode()
        if len(out) != 33 or out[32] != '\n': return None
        return out[:32]
    except:
        return None

def encryptStr(tmpKey: bytes, string: str) -> str:
    cipher = DES.new(tmpKey, DES.MODE_CFB, iv=b'\xff' * 8, segment_size=64)
    out: str = b64encode(cipher.encrypt(bytearray(string.upper()+'\n', 'ascii'))).decode()
    return out

if __name__ == '__main__':
    if len(sys.argv) >= 3:
        model = sys.argv[1];
        tmpKey: bytes = MD5.new((model * 2).encode()).digest()[:8]
        for i in range(2, len(sys.argv)):
            if i > 2: print()
            x = sys.argv[i]
            print(x)
            if len(x) == 44:
                y = decryptStr(tmpKey, x)
                if y != None:
                    print(y)
                    z = encryptStr(tmpKey, y)
                    if z != x: print('Key does not "round-trip" correctly')
                else: print('Key does not decode correctly for this model')
            else: print('Key is not the correct length of 44')
    else: print('Usage: BooxKeyConvert.py <model> <settings> <upgrade>')
