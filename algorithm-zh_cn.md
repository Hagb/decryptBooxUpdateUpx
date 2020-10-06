# Onyx Boox update.upx 更新包解密算法

## 获取字符串（仅在 Onyx Nova Pro 上测试过，以 Onyx Nova Pro 为例）

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
