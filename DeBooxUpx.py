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
    'Poke4': {
        "MODEL": "Poke4",
        "STRING_SETTINGS": "uTKx3XVyRhlbI7hoHuy/NiYdwlWViPlc4EecZKYTThN/",
        "STRING_UPGRADE": "vzDFqwIEMRfqTPUCV82ahjnz0hXfcZCIxRY8ljuLmTaf",
    },
    'Poke4S': {
        "MODEL": "Poke4S",
        "STRING_SETTINGS": "iq8+KrwLX7JGcq/B823vpSmVn5CJR2QscYDeArKjtn0B",
        "STRING_UPGRADE": "+txDKcp4Kse6Ve1kBswZWQ68i+Kpab8BoXDrgpmqQrjz"
    },
    'Poke2Color': {
        "MODEL": "Poke2Color",
        "STRING_SETTINGS": "I7ewiUSud0x9auT0PKp29393K5Hg3ymr1VJY5eUhoHEm",
        "STRING_UPGRADE": "JLe4ijbRcj5L8S9cRPRGL7eoEIKjT8OOblhy/wyvSbze",
        "STRING_LOCAL": "SODgyWbHLhfjy4WWk6lhqhYXnP1FTjSjtzMTyZkl",
    },
   'Poke4Lite': {
        "MODEL": "Poke4Lite",
        "STRING_SETTINGS": "9SHJReeuD4hvqiwtY8mNlKTYqGkvgao4d9/9og7/EXhV",
        "STRING_UPGRADE": "hiDOQumqD/7tGPsr5l69IdujC33cOPwOQw6C9wE8s8Xn"
    },
    'Nova': {
        "MODEL": "Nova",
        "STRING_SETTINGS": "L0uopm+jYaWWf/0e/POLt0kkBuS3H+5axpS6cqUpn4ft",
        "STRING_UPGRADE": "XE6jpB3WZ9J5xQdh6GFchFbeBMALt6Zx/UIg8jaiaI72",
        "STRING_LOCAL": "Rh/6kzjOT4nJCsXC5JMEkcbPzzBmNkB8i/c6ZNun"
    },
    'NoteAir': {
        "MODEL": "NoteAir",
        "STRING_SETTINGS": "U04vqHYo0LFoJQAvP3Rs1aBxySs7z4T1B+asamimEoAf",
        "STRING_UPGRADE": "VD1ZqgIl08305CVeftRI7qGBtq9bCMrJ3a1VkpkzjOu2",
        "STRING_LOCAL": "PW8K6VI//Zt6iqjYQWN0LIwRTVYyDHJvHNEXFwWV"
    },
    'NoteAir2': {
        "MODEL": "NoteAir2",
        "STRING_SETTINGS": "iCTAyj86sQAvF/XUuLBO2dS4AWZVJsy+pPmvR9wkKqhe",
        "STRING_UPGRADE": "iCbPzTBHtXSRc3HdNnswRPX6Vp222OGR/rgGb3ZYtKIM"
    },
    'NoteAir2P': {
        "MODEL": "NoteAir2P",
        "STRING_SETTINGS": "9dRjKa5Bv6SumZaiR6B5Bmxgu/JuRoSCdqVEX1P8itHp",
        "STRING_UPGRADE": "9aBiXK02yte/JCfSq1/AtQg74phmxvZv1dGaRVsM646e"
    },
    "Nova3Color": {
        "MODEL": "Nova3Color",
        "STRING_SETTINGS": "5VJqMbDB52k04k29Wc4itQBtLTRDq5kEdQaQ+GZ324PC",
        "STRING_UPGRADE": "ky0eR7CymhuAUrRBaeii5tq/ezcnXMQkT+WV1OrmRqQa",
        "STRING_LOCAL": "/Q89A5Xbsza/FBiIu8LUV5bIiLf9kXDjAdJPjyz+"
    },
    'Note': {
        "MODEL": "Note",
        "STRING_SETTINGS": "0WZeSahj4BlwNAJJkcSJEdktwbc2xdYhN+pEl+7XwuJv",
        "STRING_UPGRADE": "oRJROqUQ4xgcx7zvmLyPLeysH+cCU39EGXg77NZar8AP",
        "STRING_LOCAL": "z0YIfPx+vETibLDToPlDQPl54yE55JUFayfkx1+G"
    },
    'KonTiki2-ru': {
        "MODEL": "Kon_Tiki2",
        "STRING_SETTINGS": "eqxOVE1h8e8hbGNiV2ZHed6hMpcOH3vULx6XMm/WguZ1",
        "STRING_UPGRADE": "dKA6Ik0R95nDwjGR/dfPwxkYYNBkfngJk51A2MlRxBsq",
        "STRING_LOCAL": "bPBuYxkL37AYgKbD6nRxEL6EaFCFzFgPij53pTwH"
    },
    'Note_YDT': {
        "MODEL": "Note_YDT",
        "STRING_SETTINGS": "Utaad8dgPmSgBOjFknI0PQAp/Sc+v71Hml0ldJIzecDx",
        "STRING_UPGRADE": "ItvgBbJhOxaKjMyiE/yDufmOWwHvTPNfxdOJ2XQTHXaO",
        "STRING_LOCAL": "PIe5RuMNYz8G5FmaqRUu2qHI0br1Is3too/sLts/"
    },
    'Poke_Pro': {
        "MODEL": "Poke_Pro",
        "STRING_SETTINGS": "6GxQ6Iei3y2PSf6Wlayz+0f6yVnl1GXe5OC3q3i2lasO",
        "STRING_UPGRADE": "72lZ7vTQoy9/ESDKRQtx2V5uBMDiR+ik3n+soo9wGAbJ",
        "STRING_LOCAL": "hkkAqdfM93RpnCgXxhUqzme3OMzT6tDWC3fyibgW"
    },
    'NovaAir': {
        "MODEL": "NovaAir",
        "STRING_SETTINGS": "6NTlwbVEYP1BPTdQE25u6TCpoCg988I/Cjcs0Wxrwa4O",
        "STRING_UPGRADE": "66aRwLgxGv1vNmOsbVWp37OBy4RugvpZvUom3VQxWGrM",
        "STRING_LOCAL": "9YDFh+EuTqFECXRvmEbL78mtW69CQRENjADM8A+L"
    },
    'SP_NoteSL': {
        "MODEL": "SP_NoteS",
        "STRING_SETTINGS": "XjzywnKKh3FNVKphg5MZ9xILmDNYBZiCHTnkd6Q0fqpq",
        "STRING_UPGRADE": "XDeIyQKAhQKj6/UmdAIWoL0aXmw9PeEFl9OpII/1TO9i",
        "STRING_LOCAL": "QmGqhFGXqiuQ9yoeVx0a2SQ8BNojjPn96o6hQW6U"
    },
    'NoteS': {
        "MODEL": "NoteS",
        "STRING_SETTINGS": "+YKimeg208RzM8InqtuUjSIopyM2OLIMpFeeTQby2Au4",
        "STRING_UPGRADE": "+vap6p4w0MaT5A8RB4+ru3gnFtIq2g4K+tcjQjy3N599",
        "STRING_LOCAL": "5qT7388vj+/FwLMX/cIXSCgSxSIg9SAf0tB4NcEI"
    },
    "MaxLumi2": {
        "MODEL": "MaxLumi2",
        "STRING_SETTINGS": "zR5/dfK/2XhmwhA9AIGr+gx6Vzho5sbklSTjLAgnC8/C",
        "STRING_UPGRADE": "zh98dPzN0QdwbRem1Yfx28DFxU+Gkvg4MpLDIp0GorRU"
    },
    "NoteX": {
        "MODEL": "NoteX",
        "STRING_SETTINGS": "xhffOONo9wDGZquv93yJoLm0z6igW+XL17PUyfR8ky4l",
        "STRING_UPGRADE": "zBGvTe9t8HZQXu2Q85Dl0iI9R9tEg2VRw/8cEYXauU3o"
    },
    'Leaf': {
        "MODEL": "Leaf",
        "STRING_SETTINGS": "kh5V130fLNcO5lgsSDq7aUxQOz98DzEmiur3YsYKreIs",
        "STRING_UPGRADE": "kBtW135kW9zvvgRlsTolCktkJ7+MeW5ZoNgr3xyr2SpX",
        "STRING_LOCAL": "jzx1lloJdIBGjmcyS9oYPmXvTKFp4dpj66fPcaON"
    },
    "Gulliver-ru": {
        "MODEL": "MC_GULLIVER",
        "STRING_SETTINGS": "wDNy4yMayA4nnQfzAYYqV3ih6uu363MoyfhaX9MtbCQk",
        "STRING_UPGRADE": "xzUDklMaz39aPNJAl45ca7c3hOrBQlNYZh+iZdK64fIo",
        "STRING_LOCAL": "3xRR0nR2lFLKpw5g71X5JGqc0/hZQhmJM9idyx1b"
    },
    'NovaAirC': {
        "MODEL": "NovaAirC",
        "STRING_SETTINGS": "ycihhTCxjfQO85KdVPvpA1ZzCPr3eJ/KhcKEKlqMhEfR",
        "STRING_UPGRADE": "zsnQgzXEhvsfL4pk48rtEckIPyDedhybURHP198tag+Z"
    },
    'livingstone-ru': {
        "MODEL": "LIVINGSTONE",
        "STRING_SETTINGS": "ES5zbiHTesxFb+zdkjxiqJ+1dOwyOCv2BzCV7fOYDJxf",
        "STRING_UPGRADE": "EFwGaFSherxX1k6Hl/U6TiQhGJOzTPDfsPzHg+z9guln",
        "STRING_LOCAL": "fQ5TLnfKUOHq0f7XXdu9b1FGAckqI576ZBPkZfPg"
    },
    'Max2': {
        "MODEL": "Max2",
        "STRING_SETTINGS": "vtIkV3LyRAzlnqbIHX3PFsRUI4iP6AgBDlYmkw8OtkZQ",
        "STRING_UPGRADE": "uqhRVHL0SwBFPHF8wgyzGaR9XhIlkW/1ab0p7UjuDCjo",
        "STRING_LOCAL": "pvRyElGZH1rWeTUPJ8K3uV2MqyYmjpYYTW2y1Grc"
    },
    'Tab8': {
        "MODEL": "Tab8",
        "STRING_SETTINGS": "Yjr0qRHMwEvCt4U3K5QtAVT97968eeMOFF2zx6f6ctFg",
        "STRING_UPGRADE": "E0+HqBG5s0Z9WT+eKt0oTL2BucEMDdsaElDGQQFOV9uF"
    },
    'Poke2': {
        "MODEL": "Poke2",
        "STRING_SETTINGS": "Lu3Xbc5vobO/8sveD6qjO/LEYeqd199myw3pybHynUEO",
        "STRING_UPGRADE": "WOqqHbls0bZ67ofyutQ+XG37zR09inkP+4G3Z/t9e7m6",
        "STRING_LOCAL": "QrzzLZp3/uz4MwBzb6SJ040+l8AshzAz1t/rG8B/"
    },
    'FLOW': {
        "MODEL": "FLOW",
        "STRING_SETTINGS": "tzct2Ic6HFZzobeHcxxJ/EVt9EKMUZcaGHMN/uHZjEYW",
        "STRING_UPGRADE": "ukZbqPE8FiTbM2U12bfY4v0Xhwioj9zdKb5R2RuGL6/i",
        "STRING_LOCAL": "rGEKmqMjSX3+VMxtZNdDHF/ectjjqKIRuDMu5Mn2"
    },
    'NoteX2':{
        "MODEL": "NoteX2",
        "STRING_SETTINGS": "CTvhm+r7t0WkCO0GSd3wsPz9XM9I8NPkCE01nWR8jbii",
        "STRING_UPGRADE": "eE6c45CLsjvPltIFTvnZjS7n9TX57Pergj9uRyAOFK4w"
    }
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
        header_checked = False
        while block:
            block = inputFile.read(self.blockSize)
            decrypted_block = cipher.decrypt(block)
            if not header_checked:
                if decrypted_block[:4] != b'\x50\x4b\x03\x04':
                    raise ValueError("The decrypted data seems not a zip package, "
                                     "please ensure that the strings or model is correct.")
                header_checked = True
            outputFile.write(decrypted_block)

    def deUpx(self, inputFileName: str, outputFileName: str):
        inputFile = open(inputFileName, mode='rb', buffering=self.blockSize)
        outputFile = open(outputFileName, mode='wb', buffering=self.blockSize)
        self.deUpxSteam(inputFile, outputFile)
        inputFile.close()
        outputFile.close()


if __name__ == '__main__':
    import sys
    if 2 <= len(sys.argv) <= 4:
        device_name = sys.argv[1]
        updateUpxPath = "update.upx" if len(sys.argv) == 2 else sys.argv[2]
        if len(sys.argv) == 4:
            decryptedPath = sys.argv[3]
        else:
            import os.path
            basename = os.path.basename(updateUpxPath)
            name, ext = os.path.splitext(basename)
            decryptedPath = name + '.zip' if ext == '.upx' else basename + '.zip'
        if device_name not in boox_strings.keys():
            print(f'The device "{device_name}" is not supported, or the name is wrong')
            print("Supported devices:")
            print(" ".join(sorted(boox_strings.keys())))
            sys.exit()
        decrypter = DeBooxUpx(**boox_strings[device_name])
        decrypter.deUpx(updateUpxPath, decryptedPath)
        print(f"Saved decrypted file to {decryptedPath}")
    else:
        print("Usage:\npython DeBooxUpdate.py <device name> [input file name [output file name]]")
        print("Supported devices: (those marked with suffix '-ru' are Russian models)")
        print(" ".join(sorted(boox_strings.keys())))
