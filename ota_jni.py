import sys

sys.path.append('ExAndroidNativeEmu')

from unicorn import UcError
from unicorn.arm64_const import UC_ARM64_REG_PC

from androidemu.const import emu_const
from androidemu.emulator import Emulator
from androidemu.internal import elf_reader
from androidemu.java.classes.types import *


def main(so_path):
    # Initialize emulator
    reader = elf_reader.ELFReader(so_path)
    if reader.is_elf32():
        emulator = Emulator(
            vfs_root="ExAndroidNativeEmu/vfs",
            arch=emu_const.ARCH_ARM32,
            config_path="ExAndroidNativeEmu/emu_cfg/default.json"
        )
    else:
        emulator = Emulator(
            vfs_root="ExAndroidNativeEmu/vfs",
            arch=emu_const.ARCH_ARM64,
            config_path="ExAndroidNativeEmu/emu_cfg/default.json"
        )
    try:
        libtest = emulator.load_library(so_path)
        print("----------------")
        r = emulator.call_symbol(libtest, 'Java_com_onyx_android_onyxotaservice_RsaUtil_nativeGetSecretKey',
                                 emulator.java_vm.jni_env.address_ptr)
        pystr = emulator.java_vm.jni_env.get_local_reference(r).value.get_py_string()
        print("STRING_SETTINGS", pystr)
        r = emulator.call_symbol(libtest, 'Java_com_onyx_android_onyxotaservice_RsaUtil_nativeGetIvParameter',
                                 emulator.java_vm.jni_env.address_ptr)
        pystr = emulator.java_vm.jni_env.get_local_reference(r).value.get_py_string()
        print("STRING_UPGRADE", pystr)
    except UcError as e:
        print("Exit at 0x%08X" % emulator.mu.reg_read(UC_ARM64_REG_PC))
        emulator.memory.dump_maps(sys.stdout)
        raise


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("python %s /path/to/libota_jni.so" % __file__)
        exit(0)
    main(sys.argv[1])
