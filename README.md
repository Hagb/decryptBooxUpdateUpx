# decrypt Boox Update Upx

This project is aimed to help get the plain firmware packages of Boox devices, from the firmware packages named update.upx which are provided and encrypted by Onyx.

It has been tested only in [these Boox ereaders](./BooxKeys.csv). A few of models sold in China and most (if not all) of models sold in Russia are marked with suffixes `-cn`/`-ru`, **the firmwares for which don't use the same strings with their international versions!** SP\_NoteS is SuperStar (chaoxing) verison.

If your device hasn't been included, you could try to [get its keys](https://github.com/Hagb/decryptBooxUpdateUpx/blob/master/CONTRIBUTING.md). If you found it available for any other Boox ereader, please [submit the keys](CONTRIBUTING.md).

Note 1: There is also [another method to fetch decrypted `update.zip`](https://github.com/Hagb/decryptBooxUpdateUpx/issues/1) from [@shunf4](https://github.com/shunf4).

Note 2: There is [a way to get downloading url of latest firmware](https://github.com/Hagb/decryptBooxUpdateUpx/issues/2#issuecomment-704006389).

Note 3: `payload.bin` can be extracted with <https://github.com/cyxx/extract_android_ota_payload>.

Any other issue and pull request is also welcomed!

## How to run?

Python3 should be installed to run the script, and `pycryptodome` a dependency of the script should also be installed:

(BTW: in some environments, the following `pip` and `python` should be replaced with `pip3` and `python3`)

```bash
pip install pycryptodome
```

There are two components to this application: `DeBooxUpd.py` (the program) and `BooxKeys.csv` (the database of decryption keys).
These must be placed together in the same directory but the location does not matter.
For simplicity `update.upx` (the update to be decrypted) may be put in the same directory.
By default, `update.zip` (the decrypted update) will be generated in the current directory.

To run the application:
```bash
python DeBooxUpx.py <device model> [input file name [output file name]]
```

`<device model>` is required, and `[input file name [output file name]]` is optional. The input file will be `update.upx` and the output file will be saved in the current working directory, if not set in the arguments.

For a list of the currently supported models please refer to the file [BooxKeys.csv](BooxKeys.csv).

## Keys

Previously the raw strings extracted from Onyx software were used.
These strings were 44 alphanumeric characters long.
Since the newer Onyx models no longer use this level of obfuscation we've switched to using what the true gist of the keys are, a 32 character hexadecimal string.
Older Onyx models continue to be supported, although the key strings may appear to be unfamiliar.

## API

There is a python class `DeBooxUpx` in [DeBooxUpx.py](DeBooxUpx.py) to decrypt `update.upx`.

Following is a example of how to use this class to decrypt the `update.upx` using manual strings:

``` python3
from DeBooxUpx import DeBooxUpx

Key = "3DC53116D8AE3DCCEAD99F53E08E1E35" 
IV = "42B996AB6E252DCA4EDBC668BA3E5A3A" 
updateUpxPath = 'update.upx'
decryptedPath = 'update.zip'

decrypter = DeBooxUpx(Key, IV)
print('When updating, the device decrypt update package into', decrypter.path)
decrypter.deUpx(updateUpxPath, decryptedPath)
```

## Contributing

Refer to [CONTRIBUTING.md](CONTRIBUTING.md).
