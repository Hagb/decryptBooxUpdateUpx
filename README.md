# decrypt Boox Update Upx

Have been tested only in Onyx Boox Nova Pro. If you found that it is available for any other Boox ereader, please submit an [issue](https://github.com/Hagb/decryptBooxUpdateUpx/issues) or [pull request](https://github.com/Hagb/decryptBooxUpdateUpx/pulls), with [the strings](#the-strings) following.

Any other issue and pull request is also welcomed!

[The detail of algorithm (Simplified Chinese)](algorithm-zh_cn.md)

## Demo

There is a python class `DeBooxUpx` in [DeBooxUpx.py](DeBooxUpx.py) to decrypt `update.upx`.

Following is a example to use this class to decrypt the `update.upx` of Boox Nove Pro:

``` python3
from DeBooxUpx import DeBooxUpx

MODEL = "NovaPro" 
STRING_7F00500 = "j857wYAQcWZgvIEQ/tcQqzxreUJgFHwJl6D2TN9BuSkQ" 
STRING_7F00501 = "+soGw/YVdGIRJiAs5SMmv1ihW37H1Fa9+/1w2Vgt14Ag" 
STRING_7F00502 = "lpsj9NJ8Kzv8jHb+OO8A5lxC+9Zhl243bFmDZYaF" 
updateUpxPath = 'update.upx'
decryptedPath = 'update.zip'

decrypter = DeBooxUpx(MODEL, STRING_7F00500, STRING_7F00501, STRING_7F00502)
print('When updating, the device decrypt the plain update package into', decrypter.path)
decrypter.deUpx(updateUpxPath, decryptedPath)
```

## The strings

|       |  MODEL  |            STRING_7F00500 (S1)               |               STRING_7F00501 (S2)            |           STRING_7F00502 (S3)            |
|-------|---------|----------------------------------------------|----------------------------------------------|------------------------------------------|
|NovaPro|`NovaPro`|`j857wYAQcWZgvIEQ/tcQqzxreUJgFHwJl6D2TN9BuSkQ`|`+soGw/YVdGIRJiAs5SMmv1ihW37H1Fa9+/1w2Vgt14Ag`|`lpsj9NJ8Kzv8jHb+OO8A5lxC+9Zhl243bFmDZYaF`|

