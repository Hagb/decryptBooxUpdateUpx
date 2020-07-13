from Cryptodome.Cipher import AES
from Cryptodome.Cipher import DES
from Cryptodome.Hash import MD5
from base64 import b64decode


class DeBooxUpx:
    blockSize: int = 2**12  # 4KiB

    def __init__(self, MODEL: str, STRING_7F00500: str,
                 STRING_7F00501: str, STRING_7F00502: str = ''):
        tmpKey: bytes = MD5.new((MODEL * 2).encode()).digest()[:8]
        self.key: bytes = bytes.fromhex(
            self.decryptStr(tmpKey, STRING_7F00500))
        self.iv: bytes = bytes.fromhex(
            self.decryptStr(tmpKey, STRING_7F00501))
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
