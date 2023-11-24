#!/usr/bin/env python3
try:
    from Cryptodome.Cipher import AES
except ModuleNotFoundError:
    from Crypto.Cipher import AES
    from Crypto import version_info
    if version_info[0] == 2:
        raise SystemExit('Need either `pycryptodome` or `pycryptodomex`,'\
                ' NOT `pycrypto`!')
import csv

class DeBooxUpx:
    blockSize: int = 2**12  # 4KiB

    def __init__(self,
                 KEY: str,
                 IV: str):
        self.key: bytes = bytes.fromhex(KEY)
        self.iv: bytes = bytes.fromhex(IV)

    def deUpxStream(self, inputFile, outputFile):
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
        self.deUpxStream(inputFile, outputFile)
        inputFile.close()
        outputFile.close()

def findKeyIv(path: str, Name: str):
    try:
        with open(path) as file:
            reader = csv.reader(file, delimiter=',')
            line = 0
            for row in reader:
                if line > 0 and row[0] == Name:
                    return(row)
                line += 1
        return None
    except:
        print(f'"{path}" not found')
        sys.exit()

if __name__ == '__main__':
    import sys
    import os.path
    if 2 <= len(sys.argv) <= 4:
        csvPath = os.path.join(os.path.split(sys.argv[0])[0], 'BooxKeys.csv')
        device_name = sys.argv[1]
        updateUpxPath = "update.upx" if len(sys.argv) == 2 else sys.argv[2]
        if len(sys.argv) == 4:
            decryptedPath = sys.argv[3]
        else:
            basename = os.path.basename(updateUpxPath)
            name, ext = os.path.splitext(basename)
            decryptedPath = name + '.zip' if ext == '.upx' else basename + '.zip'
        row = findKeyIv(csvPath, device_name)
        if row is None:
            print(f'No model named "{device_name}" found')
            sys.exit()
        decrypter = DeBooxUpx(row[2], row[3])
        decrypter.deUpx(updateUpxPath, decryptedPath)
        print(f"Saved decrypted file to {decryptedPath}")
    else:
        print('Usage:\npython DeBooxUpdate.py <device name> [input file name [output file name]]')
        print('For supported devices see BooxKeys.csv')
