# decrypt Boox Update Upx

Have been tested only in [these Boox ereaders](#the-strings). If you found it available for any other Boox ereader, please [submit the strings](CONTRIBUTING.md#new-strings).

Note 1: There is also [another method to fetch decrypted `update.zip`](https://github.com/Hagb/decryptBooxUpdateUpx/issues/1) from [@shunf4](https://github.com/shunf4).

Note 2: There is [a way to get downloading url of latest firmware](https://github.com/Hagb/decryptBooxUpdateUpx/issues/2#issuecomment-704006389).

Note 3: `payload.bin` can be extracted with <https://github.com/cyxx/extract_android_ota_payload>.

Any other issue and pull request is also welcomed!

[The detail of algorithm (Simplified Chinese)](algorithm-zh_cn.md)

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

There is a python class `DeBooxUpx` in [DeBooxUpx.py](DeBooxUpx.py) to decrypt `update.upx`, and dict `boox_strings` where there are known strings.

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

A few of models sold in China and most (if not all) of models sold in Russia are marked with suffixes `-cn`/`-ru`, **the firmwares for which don't use the same strings with their international versions!**

PS: SP\_NoteS is SuperStar (chaoxing) verison.

### How to get the strings (Method 1, for Android <= 10)

`MODEL` string is the model name, exactly the output of `getprop ro.product.model` and/or value of `ro.product.model` in the file `/system/build.prop`.

Other strings can be got in following steps:

1. Get `/system/app/OnyxOtaService/OnyxOtaService.apk`
    
    USB Debugging (adb) is one of the the available ways:
    
    1. Turn on adb in Settings -> Applications -> USB Debugging Mode
    2. (from [@mgrub](https://github.com/mgrub)'s [note](https://github.com/Hagb/decryptBooxUpdateUpx/issues/5)) Connect the ebook to computer by usb, run
       ``` shell
       adb wait-for-device
       adb shell 'pm list packages -f | grep ota'
       ```
       And then the path of ota package will be showed. For example, the following output is in Nova Pro:
       ```
       package:/system/app/OnyxOtaService/OnyxOtaService.apk=com.onyx.android.onyxotaservice
       ```
       So in this case the path is `/system/app/OnyxOtaService/OnyxOtaService.apk`.

       In the following steps, we assume that the path is `/system/app/OnyxOtaService/OnyxOtaService.apk`.

    3. Run the following command
       ``` shell
       adb pull /system/app/OnyxOtaService/OnyxOtaService.apk .
       ```
    Now the apk is got.

2. Get the strings from apk

    1. Use [Apktool](https://github.com/iBotPeaches/Apktool) to decode the apk:
       ``` shell
       apktool d OnyxOtaService.apk
       ```
    2. Now the strings should be in `./OnyxOtaService/res/values/strings.xml`, for example the NovaPro one:
       ``` xml
       <?xml version="1.0" encoding="utf-8"?>
       <resources>
           <string name="settings">j857wYAQcWZgvIEQ/tcQqzxreUJgFHwJl6D2TN9BuSkQ</string>
           <string name="upgrade">+soGw/YVdGIRJiAs5SMmv1ihW37H1Fa9+/1w2Vgt14Ag</string>
           <string name="local">lpsj9NJ8Kzv8jHb+OO8A5lxC+9Zhl243bFmDZYaF</string>
           
       </resources>
       ```
       
      `settings` is `STRING_SETTINGS`, `upgrade` is `STRING_UPGRADE`, and `local` is `STRING_LOCAL`

3. Add and verify (optional) the strings

    Add the strings to `boox_strings` in [DeBooxUpx.py](DeBooxUpx.py), use this script to decrypt a `update.upx` file (it can be got by [the method in #2](https://github.com/Hagb/decryptBooxUpdateUpx/issues/2#issuecomment-704006389)), and see if the `update.zip` file is a vaild zip file.

### How to get the strings (Method 2, for Android >= 11)

In Boox OS since Android 11, these strings, which have been moved to `libota_jni.so`, are empty in `strings.xml`. In this case, please install and run [GetBooxUpxKeys](https://github.com/Hagb/GetBooxUpxKeysApp/releases) in your device to get keys, or refer to [22#issuecomment-964035840](https://github.com/Hagb/decryptBooxUpdateUpx/issues/22#issuecomment-964035840).

This method requires you install an apk in your device.

### How to get the strings (Method 3, for Android >= 11)

If you don't want to install the apk in **Method 2**, you can use **Method 3**. This method uses the emulator to get the strings.

`MODEL` string is the model name, exactly the output of `getprop ro.product.model` and/or value of `ro.product.model` in the file `/system/build.prop`.

Other strings can be got in following steps:

1. Get `/system/lib/libota_jni.so` (for 32-bit device) or `/system/lib64/libota_jni.so` (for 64-bit device)

    Connect to device via `adb` as above. Then execute command:

    ```
    adb pull /system/lib/libota_jni.so
    ```

    or

    ```
    adb pull /system/lib64/libota_jni.so
    ```

2. Prepare environment

    Clone the submodule.

    ```
    git submodule init
    git submodule update
    ```

    Install python dependencies.

    ```
    pip3 install unicorn capstone
    ```

3. Execute `ota_jni.py`

    ```
    python ota_jni.py libota_jni.so
    ERROR:androidemu.internal.modules:=> Undefined external symbol:
    ERROR:androidemu.internal.modules:=> Undefined external symbol: __cxa_finalize
    ERROR:androidemu.internal.modules:=> Undefined external symbol: __register_atfork
    ERROR:androidemu.internal.modules:=> Undefined external symbol: __cxa_atexit
    ro.kernel.qemu was not found in system_properties dictionary.
    libc.debug.malloc was not found in system_properties dictionary.
    WARNING:root:File does not exist '/proc/stat'
    WARNING:androidemu.internal.modules:libcrypto.so needed by libota_jni.so do not exist in vfs ExAndroidNativeEmu/vfs
    WARNING:androidemu.internal.modules:libutils.so needed by libota_jni.so do not exist in vfs ExAndroidNativeEmu/vfs
    ----------------
    STRING_SETTINGS uTKx3XVyRhlbI7hoHuy/NiYdwlWViPlc4EecZKYTThN/
    STRING_UPGRADE vzDFqwIEMRfqTPUCV82ahjnz0hXfcZCIxRY8ljuLmTaf
    ```
    
    You can test this method with `python ota_jni.py test/libota_jni.so`, which should give the above output.


## Contributing

Refer to [CONTRIBUTING.md](CONTRIBUTING.md).
