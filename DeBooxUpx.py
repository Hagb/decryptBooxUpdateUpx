#!/usr/bin/env python3
try:
    from Cryptodome.Cipher import AES
    from Cryptodome.Cipher import DES
    from Cryptodome.Hash import MD5
except ModuleNotFoundError:
    from Crypto.Cipher import AES
    from Crypto.Cipher import DES
    from Crypto.Hash import MD5
    from Crypto import version_info
    if version_info[0] == 2:
        raise SystemExit('Need either `pycryptodome` or `pycryptodomex`,'\
                ' NOT `pycrypto`!')
from base64 import b64decode

boox_strings = {
    'PadMu3': {
        "MODEL": "PadMuAP3",
        "STRING_SETTINGS": "TCP3lGFLuxm7wOXWnaomQAdYikpFPAOj5U2LK0Dck3Un",
        "STRING_UPGRADE": "PC3wkRM4zhgstNIQLGR+dW9jourXdEXZXU/mN7bTACu0",
        "STRING_LOCAL": "In/UoUFVkUdHTCqlSfCgKi8MEZGHK0Xc70Y5trXs"
    },
    'NovaPro': {
        "MODEL": "NovaPro",
        "STRING_SETTINGS": "j857wYAQcWZgvIEQ/tcQqzxreUJgFHwJl6D2TN9BuSkQ",
        "STRING_UPGRADE": "+soGw/YVdGIRJiAs5SMmv1ihW37H1Fa9+/1w2Vgt14Ag",
        "STRING_LOCAL": "lpsj9NJ8Kzv8jHb+OO8A5lxC+9Zhl243bFmDZYaF"
    },
    'NovaPlus': {
        "MODEL": "NovaPlus",
        "STRING_SETTINGS": "MtoBkApRAVwzdGe2CTnaE4MIgevRYNQfaKo606tyUQNY",
        "STRING_UPGRADE": "Nttwkwxaei8xorBu/uUBpUu8nNZHTRIAZMZc0xrJs9Ti",
        "STRING_LOCAL": "LIYj1F9NVXFrOfi24/C76gFFxHYSCJ4mfhYI4q5w"
    },
    'Nova2': {
        "MODEL": "Nova2",
        "STRING_SETTINGS": "lxXh4Vv6aqYecCAFc/hsn4mnXNbI6H4S3bZFW5Jh8NHj",
        "STRING_UPGRADE": "lBabky+FbaOtZ7luDK+7BlApiYcGEi8PndwIc5WaemXQ",
        "STRING_LOCAL": "iDDDo3jsN4hhLA3tQhaIkM4XLcxZT4czBMM7ExnK"
    },
    'Nova3': {
        "MODEL": "Nova3",
        "STRING_SETTINGS": "VUkFew9KjsE54uQMSZI+S2tT1RRckT/vKkfiFFqImxi7",
        "STRING_UPGRADE": "VEsMcHw88MpwOByhT7zqNhRFTQcruVMqhdllIlY6T+6f",
        "STRING_LOCAL": "TGlcNi8npJe4EHxzOKbCXakJKDssoRldHueY5OGl"
    },
    'Max3': {
        "MODEL": "Max3",
        "STRING_SETTINGS": "1wdvUHZmcz32N1pgG4fkHmDsTDVihMJsPCNV4mW/6u1k",
        "STRING_UPGRADE": "3nxuLgdpBE3B3n1Yyymt4cOS8dNucfQxK8YOsmcemuyO",
        "STRING_LOCAL": "yCA9YlFxLBdLbDUl3vwzPkn9vtYuVFZCfhrOTvR1"
    },
    'MaxLumi': {
        "MODEL": "MaxLumi",
        "STRING_SETTINGS": "mTZFN0K+oMcGnn2n7+zV5DH7kr/Hbes2x/wKDJp6K7Kq",
        "STRING_UPGRADE": "mj0zR0Oy3L4R+6y49MIEQT9bdx9AVz8TWyG9q3N+d9VY",
        "STRING_LOCAL": "hWAUdhOp9ekIYxIW+LpVj6OviWBbCbRa1c7s1jtW"
    },
    'Note2': {
        "MODEL": "Note2",
        "STRING_SETTINGS": "etwiPPEXAQRj3m+e0Q2FOxT16aJ8XexQAqhGn5NqZWv1",
        "STRING_UPGRADE": "et0jSPpmd3ueGHLmMf+2yyXVn18sa2HrDg56dCTFH6lf",
        "STRING_LOCAL": "YY9wfqN7K1LlSug47Tr5Y8QkDHmmJ4VDCJ58mhoV"
    },
    'NotePro': {
        "MODEL": "NotePro",
        "STRING_SETTINGS": "MjR72bOazBUacJwDcuWgtm/E0A9F9ahIt1buweEPA020",
        "STRING_UPGRADE": "RjV8r7+fx2Wjp6rUSrBOpmqYnHKs7eReqTTcy9k4c3tn",
        "STRING_LOCAL": "W2co6eaDmEl7jIjOSqr11C71RDHHiV3p5oG2G54X"
    },
    'Note3': {
        "MODEL": "Note3",
        "STRING_SETTINGS": "uTiMM5JgTXOCZAZKMcZIzc1yQpfX1+jxTFOred3te4z9",
        "STRING_UPGRADE": "zEf3SZ8TOADA8QuwOHicGLrrc4EA7sffKfc01TlUfe/q",
        "STRING_LOCAL": "pmXVBMt5EllxXhD9L6/NWH/pTZXRURP6QLsrNlx6"
    },
    'Poke3': {
        "MODEL": "Poke3",
        "STRING_SETTINGS": "lU95mOkt0cGucrsrIdAWuYnoJEnTTfIvu/QNUlcmI42A",
        "STRING_UPGRADE": "kjl4lOMqobWYQyqX4KzBGYS8Q0OwPSfqwf29ymkypULP",
        "STRING_LOCAL": "iW9b2bszjJhv3puv87HNQXLW3Fb5uQVhWnnKU4nV",
    },
    'Poke2Color': {
        "MODEL": "Poke2Color",
        "STRING_SETTINGS": "I7ewiUSud0x9auT0PKp29393K5Hg3ymr1VJY5eUhoHEm",
        "STRING_UPGRADE": "JLe4ijbRcj5L8S9cRPRGL7eoEIKjT8OOblhy/wyvSbze",
        "STRING_LOCAL": "SODgyWbHLhfjy4WWk6lhqhYXnP1FTjSjtzMTyZkl",
    },
    'Nova': {
        "MODEL": "Nova",
        "STRING_SETTINGS": "L0uopm+jYaWWf/0e/POLt0kkBuS3H+5axpS6cqUpn4ft",
        "STRING_UPGRADE": "XE6jpB3WZ9J5xQdh6GFchFbeBMALt6Zx/UIg8jaiaI72",
        "STRING_LOCAL": "Rh/6kzjOT4nJCsXC5JMEkcbPzzBmNkB8i/c6ZNun"
    },
}


class DeBooxUpx:
    blockSize: int = 2**12  # 4KiB

    def __init__(self,
                 MODEL: str,
                 STRING_SETTINGS: str,
                 STRING_UPGRADE: str,
                 STRING_LOCAL: str = ''):
        tmpKey: bytes = MD5.new((MODEL * 2).encode()).digest()[:8]
        self.key: bytes = bytes.fromhex(
            self.decryptStr(tmpKey, STRING_SETTINGS))
        self.iv: bytes = bytes.fromhex(self.decryptStr(tmpKey, STRING_UPGRADE))
        self.path: str = self.decryptStr(tmpKey, STRING_LOCAL)

    @staticmethod
    def decryptStr(tmpKey: bytes, string: str) -> str:
        cipher = DES.new(tmpKey, DES.MODE_CFB, iv=b'\xff' * 8, segment_size=64)
        return cipher.decrypt(b64decode(string)).decode().strip()

    def deUpxSteam(self, inputFile, outputFile):
        block: bytes = b'1'
        cipher = AES.new(self.key, AES.MODE_CFB, iv=self.iv, segment_size=128)
        while block:
            block = inputFile.read(self.blockSize)
            outputFile.write(cipher.decrypt(block))

    def deUpx(self, inputFileName: str, outputFileName: str):
        inputFile = open(inputFileName, mode='rb', buffering=self.blockSize)
        outputFile = open(outputFileName, mode='wb', buffering=self.blockSize)
        self.deUpxSteam(inputFile, outputFile)
        inputFile.close()
        outputFile.close()


if __name__ == '__main__':
    import sys
    if len(sys.argv) >= 2:
        device_name = sys.argv[1]
        updateUpxPath = "update.upx" if len(sys.argv) == 2 else sys.argv[2]
        name = updateUpxPath[:-4]
        ext = updateUpxPath[-4:].lower()
        decryptedPath = name + '.zip' if ext == '.upx' else updateUpxPath + '.zip'
        if device_name not in boox_strings.keys():
            print("Following device is not supported, or the name is wrong")
            print("Supported devices:")
            print(" ".join(boox_strings.keys()))
            sys.exit()
        decrypter = DeBooxUpx(**boox_strings[device_name])
        decrypter.deUpx(updateUpxPath, decryptedPath)
        print(f"Saved decrypted file to {decryptedPath}")
    else:
        print("Usage:\npython DeBooxUpdate.py <device name> [input file name]")
        print("Supported devices:")
        print(" ".join(boox_strings.keys()))
