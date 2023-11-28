# CONTRIBUTING

## New decryption keys

If you have a device for which no decryption keys are known and listed in [BooxKeys.csv](BooxKyes.csv) you can help by supplying them.
You can start an [Issue](https://github.com/Hagb/decryptBooxUpdateUpx/issues), but you'll still need to supply some information for someone else to extract the decryption keys.
You may be able to find the decryption keys yourself.
As the way these decryption keys are stored has changed over time you may have to use different approaches.

## Preliminaries

First you have to determine what the actual model of your device is called.
Yes, you know what you think is the model, but the actual model name usually does not have any spaces in it and may often have a surprising suffix.
ADB is a common and necessary tool for many operations on Android.
If you are not familiar with it, just Google "minimal ADB".
The simple command in an ADB shell `getprop ro.product.model` will tell you the real model name.
You can also check the fingerprints with `getprop | grep finger`.

## Decryption keys stored as resources

This was the oldest approach.
The app responsible for decrypting updates was usually in `/system/priv-app/OnyxOtaService/OnyxOtaService.apk`
You can download this app by `adb pull /system/priv-app/OnyxOtaService/OnyxOtaService.apk`.
Now you will have to disassemble the app using [Apktool](https://github.com/iBotPeaches/Apktool).
If this is beyond your pay grade, just start an issue and post the apk.
The strings that we are looking for are stored in res/values/strings.xml in the disassembled app.
``` xml
<string name="settings">j857wYAQcWZgvIEQ/tcQqzxreUJgFHwJl6D2TN9BuSkQ</string>
<string name="upgrade">+soGw/YVdGIRJiAs5SMmv1ihW37H1Fa9+/1w2Vgt14Ag</string>
```
As these are the "old style" strings they need to be converted to "new style" strings.
You can use [BooxKeyConverter.py](BooxKeyConverter.py) or, as always, just post an issue.

## Decryption keys stored in a library file

This is the newer approach and may have variants now and in the future.
You can easily see if this might be the case by the presence of a library file.
You can download this library by `adb pull /system/lib64/libota_jni.so`.
Although this is specific to 64 bit devices, only the newer 64 bit devices use this approach.
As before, you can just start an issue and post this file if that's your limit as it gets a bit more complicated now.

### Decryption keys accessed by JNI method

The old style decryption keys may be extracted by calling JNI methods in libota_jni.so.
The two exported functions are:
```
Java_com_onyx_android_onyxotaservice_RsaUtil_nativeGetSecretKey
Java_com_onyx_android_onyxotaservice_RsaUtil_nativeGetIvParameter
```
The utility [ota_jni.py](ota_jni.py) can extract the decryption keys.
You can use [BooxKeyConverter.py](BooxKeyConverter.py) to convert them to new style.

### Decryption keys accessed by C++ call

The new style decryption keys may be extracted by calling C++ functions in libota_jni.so.
The two exported functions are:
```
getKeyString(void)         _Z12getKeyStringv
getInitVectorString(void)  _Z19getInitVectorStringv
```

### Decryption keys not accessible directly from the library file

There may not be any methods or functions to directly access the encryption keys.
Please post your libota_jni.so and we will see what we can do.

