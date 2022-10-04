# Onyx Boox update.upx 更新包解密算法

## 获取字符串 方式一：资源文件（仅在 Onyx Nova Pro 上测试过，以 Onyx Nova Pro 为例）

先将设备开启 adb 调试。

- MODEL 可将设备接上计算机后使用

    ```
    adb shell getprop ro.product.model
    ```

    来获取.（NovaPro 中得到的是`NovaPro`）

- 以下三个字符串：

    先从设备中`pull`出`/system/app/OnyxOtaService/OnyxOtaService.apk`并用`apktool`工具解包，然后在其中查找`id`分别为`0x7f050000`、`0x7f050001`、`0x7f050002`的`name`值，再根据这三个`name`值查找得到三条`string`值，我们分别将它们记作 S1, S2, S3。

    以 NovaPro 为例，以上 `name` 值首先在`res/values/public.xml`中找到，分别为

    - `"settings"`
    - `"upgrade"`
    - `"local"`

    接着在`res/values/strings.xml`中可找到其对应的`string`值即 S1、S2、S3 的值，分别为

    - `"j857wYAQcWZgvIEQ/tcQqzxreUJgFHwJl6D2TN9BuSkQ"`
    - `"+soGw/YVdGIRJiAs5SMmv1ihW37H1Fa9+/1w2Vgt14Ag"`
    - `"lpsj9NJ8Kzv8jHb+OO8A5lxC+9Zhl243bFmDZYaF"`

- 在 Android 11 以上的设备上，这些字符串被移到了 `libota_jni.so`，在这种情况下，请查看安装该 APP [GetBooxUpxKeys](https://github.com/Hagb/GetBooxUpxKeysApp/releases) 来获得keys。或者参考 [22#issuecomment-964035840](https://github.com/Hagb/decryptBooxUpdateUpx/issues/22#issuecomment-964035840).


## 获取字符串 方式二：libota_jni.so

在 Android 11 以上的设备上（例如Poke4），Onyx Boox 将解密用的key移到了 shared library里。获取它的方法有很多，这里提供了一种模拟执行的方式来获取。

先将设备开启 adb 调试。

- MODEL 可将设备接上计算机后使用

    ```
    adb shell getprop ro.product.model
    ```

    来获取.（Poke4 中得到的是`Poke4`）

- 获取 libota_jni.so

    32位机使用命令

    ```
    adb pull /system/lib/libota_jni.so
    ```

    64位机使用命令

    ```
    adb pull /system/lib64/libota_jni.so
    ```

- 准备运行环境

    将 submodule 克隆回来

    ```
    git submodule init
    git submodule update
    ```

    安装python依赖

    ```
    pip install unicorn capstone
    ```

- 模拟执行 libota_jni.so

    将拖回来的 libota_jni.so 作为脚本的入参。下方指令使用的是 Poke4 中拖出来的 libota_jni.so，未测试其他机型。

    ```
    python ota_jni.py test/libota_jni.so
    ```
  
    输出内容示例，最后两行就是结果

    ```
    python ota_jni.py test/libota_jni.so
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

## 解密算法

1. 求两份 MODEL 相连（如 MODEL 值为`NovaPro`，则该值为`MovaProNovaPro`）的 md5，（二进制）截取前 8 字节，作为临时密钥 tmpK；
2. Base64 解码 S1、S2、S3，分别得字符串 s1、s2、s3
3. 用 DES 算法 CFB 模式

    - 初始化向量（initialization vector）: 8 字节的 0xff 
    - 分段长度（segment size）: 64 bits
    - 密钥：上述临时密钥 tmpK

    来解密 s1，得密钥 K 的 hex，进一步可求出密钥 K；

4. 用上述 3 的方法解密 s2 得初始化向量 IV 的 hex，从而可进一步得到初始化向量 IV；
5. 再用同样的方法解密 s3 得路径 P（这步可不做）；
6. 以 AES 算法 CFB 模式

    - 初始化向量: 上述 IV
    - 分段长度: 128 bits
    - 密钥: 上述 K

    解密 update.upx 更新包，即可得到能够被 Recovery 读取的明文 zip 更新包。
