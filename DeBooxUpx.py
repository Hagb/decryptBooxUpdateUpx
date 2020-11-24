from Cryptodome.Cipher import AES
from Cryptodome.Cipher import DES
from Cryptodome.Hash import MD5
from base64 import b64decode

boox_strings = {
    'NovaPro': {
        "MODEL": "NovaPro",
        "STRING_7F00500": "j857wYAQcWZgvIEQ/tcQqzxreUJgFHwJl6D2TN9BuSkQ",
        "STRING_7F00501": "+soGw/YVdGIRJiAs5SMmv1ihW37H1Fa9+/1w2Vgt14Ag",
        "STRING_7F00502": "lpsj9NJ8Kzv8jHb+OO8A5lxC+9Zhl243bFmDZYaF"
    },
    'NovaPlus': {
        "MODEL": "NovaPlus",
        "STRING_7F00500": "MtoBkApRAVwzdGe2CTnaE4MIgevRYNQfaKo606tyUQNY",
        "STRING_7F00501": "Nttwkwxaei8xorBu/uUBpUu8nNZHTRIAZMZc0xrJs9Ti",
        "STRING_7F00502": "LIYj1F9NVXFrOfi24/C76gFFxHYSCJ4mfhYI4q5w"
    },
    'Nova2': {
        "MODEL": "Nova2",
        "STRING_7F00500": "lxXh4Vv6aqYecCAFc/hsn4mnXNbI6H4S3bZFW5Jh8NHj",
        "STRING_7F00501": "lBabky+FbaOtZ7luDK+7BlApiYcGEi8PndwIc5WaemXQ",
        "STRING_7F00502": "iDDDo3jsN4hhLA3tQhaIkM4XLcxZT4czBMM7ExnK"
    },
    'Max3': {
        "MODEL": "Max3",
        "STRING_7F00500": "1wdvUHZmcz32N1pgG4fkHmDsTDVihMJsPCNV4mW/6u1k",
        "STRING_7F00501": "3nxuLgdpBE3B3n1Yyymt4cOS8dNucfQxK8YOsmcemuyO",
        "STRING_7F00502": "yCA9YlFxLBdLbDUl3vwzPkn9vtYuVFZCfhrOTvR1"
    },
    'MaxLumi': {
        "MODEL": "MaxLumi",
        "STRING_7F00500": "mTZFN0K+oMcGnn2n7+zV5DH7kr/Hbes2x/wKDJp6K7Kq",
        "STRING_7F00501": "mj0zR0Oy3L4R+6y49MIEQT9bdx9AVz8TWyG9q3N+d9VY",
        "STRING_7F00502": "hWAUdhOp9ekIYxIW+LpVj6OviWBbCbRa1c7s1jtW"
    },
    'Note2': {
        "MODEL": "Note2",
        "STRING_7F00500": "etwiPPEXAQRj3m+e0Q2FOxT16aJ8XexQAqhGn5NqZWv1",
        "STRING_7F00501": "et0jSPpmd3ueGHLmMf+2yyXVn18sa2HrDg56dCTFH6lf",
        "STRING_7F00502": "YY9wfqN7K1LlSug47Tr5Y8QkDHmmJ4VDCJ58mhoV"
    },
    'NotePro':{
        "MODEL": "NotePro",
        "STRING_7F00500": "MjR72bOazBUacJwDcuWgtm/E0A9F9ahIt1buweEPA020",
        "STRING_7F00501": "RjV8r7+fx2Wjp6rUSrBOpmqYnHKs7eReqTTcy9k4c3tn",
        "STRING_7F00502": "W2co6eaDmEl7jIjOSqr11C71RDHHiV3p5oG2G54X"
    },
    'Note3': {
        "MODEL": "Note3",
        "STRING_7F00500": "uTiMM5JgTXOCZAZKMcZIzc1yQpfX1+jxTFOred3te4z9",
        "STRING_7F00501": "zEf3SZ8TOADA8QuwOHicGLrrc4EA7sffKfc01TlUfe/q",
        "STRING_7F00502": "pmXVBMt5EllxXhD9L6/NWH/pTZXRURP6QLsrNlx6"
    }
}


class DeBooxUpx:
    blockSize: int = 2**12  # 4KiB

    def __init__(self,
                 MODEL: str,
                 STRING_7F00500: str,
                 STRING_7F00501: str,
                 STRING_7F00502: str = ''):
        tmpKey: bytes = MD5.new((MODEL * 2).encode()).digest()[:8]
        self.key: bytes = bytes.fromhex(self.decryptStr(
            tmpKey, STRING_7F00500))
        self.iv: bytes = bytes.fromhex(self.decryptStr(tmpKey, STRING_7F00501))
        self.path: str = self.decryptStr(tmpKey, STRING_7F00502)

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
