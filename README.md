# decrypt Boox Update Upx

[The detail of algorithm (Simplified Chinese)](algorithm-zh_cn.md)

## Demo

There are python class `DeBooxUpx` in [DeBooxUpx.py](DeBooxUpx.py).

Following is a example to use this class to decrypt the `update.upx` of Boox Nove Pro:

``` python3
from DeBooxUpx import DeBooxUpx

MODEL = "NovaPro" 
STRING_2131034112 = "j857wYAQcWZgvIEQ/tcQqzxreUJgFHwJl6D2TN9BuSkQ" 
STRING_2131034113 = "+soGw/YVdGIRJiAs5SMmv1ihW37H1Fa9+/1w2Vgt14Ag" 
STRING_2131034114 = "lpsj9NJ8Kzv8jHb+OO8A5lxC+9Zhl243bFmDZYaF" 
updateUpxPath = 'update.upx'
decryptedPath = 'update.zip'

decrypter = DeBooxUpx(MODEL, STRING_2131034112, STRING_2131034113, STRING_2131034114)
decrypter.deUpx(updateUpxPath, decryptedPath)
```

## The strings

|       |  MODEL  |            STRING_7F00500 (S1)               |               STRING_7F00501 (S2)            |           STRING_7F00501 (S3)            |
|-------|---------|----------------------------------------------|----------------------------------------------|------------------------------------------|
|NovaPro|`NovaPro`|`j857wYAQcWZgvIEQ/tcQqzxreUJgFHwJl6D2TN9BuSkQ`|`+soGw/YVdGIRJiAs5SMmv1ihW37H1Fa9+/1w2Vgt14Ag`|`lpsj9NJ8Kzv8jHb+OO8A5lxC+9Zhl243bFmDZYaF`|
