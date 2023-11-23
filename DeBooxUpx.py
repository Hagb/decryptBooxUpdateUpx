#!/usr/bin/env python3
try:
    from Cryptodome.Cipher import AES
except ModuleNotFoundError:
    from Crypto.Cipher import AES
    from Crypto import version_info
    if version_info[0] == 2:
        raise SystemExit('Need either `pycryptodome` or `pycryptodomex`,'\
                ' NOT `pycrypto`!')

boox_strings = {
    'FLOW': {
        'MODEL': 'FLOW',
        'KEY': '42F6E69DB0A176DC5FBA04DE2C4C0C7D',
        'IV': '9C0F30369B5539A1E0696598638D4731'
    },
    'Gulliver-ru': {
        'MODEL': 'MC_GULLIVER',
        'KEY': '0CBE6C03F589353182354085D8E20F31',
        'IV': '7E34FC7B6E6FD0A39C0E43CBAF32FB52'
    },
    'KonTiki2-ru': {
        'MODEL': 'Kon_Tiki2',
        'KEY': '98AC5EB0D8D7A0A0B2E75B278DB8B288',
        'IV': '745555DF150183D4C92AFBC4EDE58ED2'
    },
    'Leaf': {
        'MODEL': 'Leaf',
        'KEY': '2FA5F9484C5079FA25B89FD6A926F0FD',
        'IV': '0CB5EBC30E284C71108ACC344026DFD6'
    },
    'Leaf2': {
        'MODEL': 'Leaf2',
        'KEY': '4131D58DC6CB5D85BFD23D9F576CAB16',
        'IV': 'A60D8B8DEE2A494194F1AC6C80E850AC'
    },
    'Leaf2-cn': {
        'MODEL': 'Leaf2_P',
        'KEY': 'E95EE8726EC4B63A2241F38829C27FCC',
        'IV': '8093A741A8A4C45E11690B72D78C59A1'
    },
    'Leaf3': {
        'MODEL': 'Leaf3',
        'KEY': '6ABE99B43B928F351C83CDD5A2516A6E',
        'IV': '1009E8860F53BB40483A83173F844198'
    },
    'Lomonosov-ru': {
        'MODEL': 'Lomonosov',
        'KEY': 'D2F7E3354FC07C2521BF609D01FBC90F',
        'IV': '0070D3F87818CF23DB5EE9798B8B0657'
    },
    'Max2': {
        'MODEL': 'Max2',
        'KEY': '7B71BD797D7E3721D69F4449E12B4C22',
        'IV': '38B2BB851DAF20E1BE6E7E3F349CABA0'
    },
    'Max2Pro': {
        'MODEL': 'Max2Pro',
        'KEY': '8BEAEE4D037DAC8E2DB18458CDFA4A53',
        'IV': '706038B3497224CCC2B81572EACAA780'
    },
    'Max3': {
        'MODEL': 'Max3',
        'KEY': '0C3FF83E57334391A2D4171E99EAC1A9',
        'IV': '982877D54100A07BBF205F31193B2D3D'
    },
    'MaxLumi': {
        'MODEL': 'MaxLumi',
        'KEY': '3205089AF7E08108730ABFC237D94BE8',
        'IV': '09FE14E89ABE38654112885A43352D30'
    },
    'MaxLumi2': {
        'MODEL': 'MaxLumi2',
        'KEY': '25F86689E5FE3DEB2856983CCF21FB6D',
        'IV': '14E98D0F357F7087D27D22406D7291E0'
    },
    'Note': {
        'MODEL': 'Note',
        'KEY': '1D7A5202269D384B72F348CE25D55120',
        'IV': 'A0828A338A06FF2CD3618B219D3E30E2'
    },
    'Note2': {
        'MODEL': 'Note2',
        'KEY': '47363CF9416ADE0231B61D62DD8F4539',
        'IV': '462B820F6C4B3BC72EE48FDFF0FA3E39'
    },
    'Note3': {
        'MODEL': 'Note3',
        'KEY': '098C863EB6E1F8DC96720031B32EA200',
        'IV': 'EFC95EF6B02442EE518F2D2BD5594250'
    },
    'NoteAir': {
        'MODEL': 'NoteAir',
        'KEY': 'AED5E8AE8AB08319EC791849310171C2',
        'IV': 'F62715B99809212131696C2FD7C6F75D'
    },
    'NoteAir2': {
        'MODEL': 'NoteAir2',
        'KEY': '856C9D4ADCE8015F272357F5DDF08B71',
        'IV': '879D69054D57C76152CF272A0C121006'
    },
    'NoteAir2P': {
        'MODEL': 'NoteAir2P',
        'KEY': '1276ECC6636DA6AFCEF5D7F300E5C915',
        'IV': '1F6CF46EC279E61EDB7FC150C3471972'
    },
    'NoteAir3C': {
        'MODEL': 'NoteAir3C',
        'KEY': '4DEAED7F843CDCEDB384E6FC468C540E',
        'IV': '964E8856F922178810AEC06E0D363512'
    },
    'NotePro': {
        'MODEL': 'NotePro',
        'KEY': 'F72D46836B5B1A0D1CB5BB27C6895A4F',
        'IV': '2652833CDDC4C4CDD3BEC6F8D6AD3914'
    },
    'NoteS': {
        'MODEL': 'NoteS',
        'KEY': '0B82F60DB060E404F752E9B91F0BE28B',
        'IV': '363A003F2C54F1DA3412F7A9CC7DFDBE'
    },
    'NoteX': {
        'MODEL': 'NoteX',
        'KEY': '8CC1464D7009076D571D4FF249F47B3D',
        'IV': '2E3D8332638FED444BA24D5462C12046'
    },
    'NoteX2': {
        'MODEL': 'NoteX2',
        'KEY': '00D996A8B45734B9E7943C0FF3333646',
        'IV': 'AE9ACFDF9C871C2B9458B2F2245035E0'
    },
    'Note_YDT': {
        'MODEL': 'Note_YDT',
        'KEY': 'A5BEEB144025D73FD90971E4906232BA',
        'IV': '18870C4F426A494320868606DA2091BB'
    },
    'Nova': {
        'MODEL': 'Nova',
        'KEY': 'F03A6BBC306066AB1B3A5BE5AEC1D3F3',
        'IV': '558CD7D43E17869A50FFFF6C72C26282'
    },
    'Nova2': {
        'MODEL': 'Nova2',
        'KEY': '0AC6B91ABB5988ADE6313FD62F6EDB0B',
        'IV': '3B9D6F6DE8D1795D3D265C0EFC9B59C7'
    },
    'Nova3': {
        'MODEL': 'Nova3',
        'KEY': '6D89ABF9B380998958D8002897BBF650',
        'IV': '7F1224824C0B41DAAE907ADE10828C58'
    },
    'Nova3Color': {
        'MODEL': 'Nova3Color',
        'KEY': '796FD580A4BE82B6FEAC8CFDA676585B',
        'IV': 'AFB0DFEBD0A2D71F37F21231808BD1A9'
    },
    'NovaAir': {
        'MODEL': 'NovaAir',
        'KEY': '20A25EB3B9363810BCFFA9A2E1B55B0A',
        'IV': '1B5380830BF637ECB7181C3926D5B479'
    },
    'NovaAir2': {
        'MODEL': 'NovaAir2',
        'KEY': '88520228DF831062B6CB7AAED5166156',
        'IV': 'C0A91A092BC76A46F7AE6FDC4EED5C20'
    },
    'NovaAirC': {
        'MODEL': 'NovaAirC',
        'KEY': '3E37242727DD67DF9D4EC08D936974E2',
        'IV': '4DB17A985684B7319A349743B22BF41B'
    },
    'NovaPlus': {
        'MODEL': 'NovaPlus',
        'KEY': '18C0438BE7CE881BC86BC6C84CEC096D',
        'IV': '592328C13A578E053FA565A5B684294D'
    },
    'NovaPro': {
        'MODEL': 'NovaPro',
        'KEY': '619A3C6290FEDA02418091AE2F39592F',
        'IV': 'C5DCEF361A60239DB4E8648DD9F7847A'
    },
    'PadMu3': {
        'MODEL': 'PadMuAP3',
        'KEY': 'A8BAA1F101DB9FC7CA0CD9FB04A97694',
        'IV': '16ED3B30C6F251BA4267679433765E5F'
    },
    'Poke2': {
        'MODEL': 'Poke2',
        'KEY': 'C5E45730FBD665FC3857C6D78FD63E43',
        'IV': '528DB4C57394F09D3C00E2D45E5C9641'
    },
    'Poke2Color': {
        'MODEL': 'Poke2Color',
        'KEY': 'D314CF54B76931B6309F83B2F037D419',
        'IV': 'C397190FD2E48874C1CFBE52A782AB59'
    },
    'Poke3': {
        'MODEL': 'Poke3',
        'KEY': '3DC53116D8AE3DCCEAD99F53E08E1E35',
        'IV': '42B996AB6E252DCA4EDBC668BA3E5A3A'
    },
    'Poke4': {
        'MODEL': 'Poke4',
        'KEY': 'E155E2D73EFC3EB70745B434BE203EFD',
        'IV': 'C3AC2D3955E32709F10511C3B662B27F'
    },
    'Poke4Lite': {
        'MODEL': 'Poke4Lite',
        'KEY': '6C74952C3EA2E07244D6B3D91C222335',
        'IV': 'EB037125447814B0F4198E201A966B3D'
    },
    'Poke4S': {
        'MODEL': 'Poke4S',
        'KEY': 'CFD60D360BD91B04843F8B3090B2DA08',
        'IV': '3595F7FCE8B4F2AD5804DEE46299281C'
    },
    'Poke5P': {
        'MODEL': 'Poke5P',
        'KEY': '550504B1DE28C363172040829BFFA408',
        'IV': '26C4D62584DA0619AB972B66ACC3689A'
    },
    'Poke_Pro': {
        'MODEL': 'Poke_Pro',
        'KEY': 'AA151AD6C888DFB010433F3B1EC676EC',
        'IV': 'FD83B38456D9C052F22414DF9A2C0FEC'
    },
    'SP_NoteSL': {
        'MODEL': 'SP_NoteS',
        'KEY': '3992B2A532F9ABDCB953EDAD7EC95FFF',
        'IV': '12C928CF2C665AF83B50361C80B88297'
    },
    'Tab10CPro': {
        'MODEL': 'Tab10CPro',
        'KEY': 'D999393AEAA81119AC0F8C8C1EA11089',
        'IV': 'CD7894A509490BAF2BAA129686A083E4'
    },
    'Tab13': {
        'MODEL': 'Tab13',
        'KEY': '1072DE10B43097036B98B9021F308FB0',
        'IV': 'F180C655AABF3EB02D9E45B9FD5379B2'
    },
    'Tab8': {
        'MODEL': 'Tab8',
        'KEY': 'ECC953580D49BAD70D9DBA526EC091D2',
        'IV': '46085FF59CCE685B38FB651876E8964B'
    },
    'TabUltra': {
        'MODEL': 'TabUltra',
        'KEY': 'A01FF8E0F4D139FC75FAA49D61E12E9C',
        'IV': 'EC94D4BA3550734EA8C69DD726444DE3'
    },
    'TabUltraC': {
        'MODEL': 'TabUltraC',
        'KEY': '2DB550268389D895AACB781AB3515DCB',
        'IV': '13FDC3C394EAB6323BF42428CD275AA2'
    },
    'TabX': {
        'MODEL': 'TabX',
        'KEY': '28E3BE85609F0D5CAA3796643512AAA2',
        'IV': '8952832CBE65133CF531C978B7AC0696'
    },
    'livingstone-ru': {
        'MODEL': 'LIVINGSTONE',
        'KEY': 'CDA476FB48B341F03C3217EBDFCA1BFA',
        'IV': 'B642BDF244FCC321E1A62BBE0EE4C15A'
    }
}

class DeBooxUpx:
    blockSize: int = 2**12  # 4KiB

    def __init__(self,
                 MODEL: str,
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

if __name__ == '__main__':
    import sys
    if 2 <= len(sys.argv) <= 4:
        device_name = sys.argv[1]
        updateUpxPath = "update.upx" if len(sys.argv) == 2 else sys.argv[2]
        if len(sys.argv) == 4:
            decryptedPath = sys.argv[3]
        else:
            import os.path
            basename = os.path.basename(updateUpxPath)
            name, ext = os.path.splitext(basename)
            decryptedPath = name + '.zip' if ext == '.upx' else basename + '.zip'
        if device_name not in boox_strings.keys():
            print(f'The device "{device_name}" is not supported, or the name is wrong')
            print("Supported devices:")
            print(" ".join(sorted(boox_strings.keys())))
            sys.exit()
        decrypter = DeBooxUpx(**boox_strings[device_name])
        decrypter.deUpx(updateUpxPath, decryptedPath)
        print(f"Saved decrypted file to {decryptedPath}")
    else:
        print("Usage:\npython DeBooxUpdate.py <device name> [input file name [output file name]]")
        print("Supported devices: (those marked with suffix '-ru' are Russian models)")
        print(" ".join(sorted(boox_strings.keys())))
