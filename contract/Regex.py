class Regex:
    '''
    public static class
    '''
    # The first part is for the libraries (73<address>3014)
    SOLIDITY = r"^(73[0-9a-fA-F]{40}3014)?60(60|80)604052[0-9a-fA-F]*$"
    # Used to split runtime code
    RUNTIME = r"(?=60(60|80)604052)"

    # From version solc-0.4.17
    # 0xa1
    # 0x65 'b' 'z' 'z' 'r' '0' 0x58 0x20 <32 bytes swarm hash>
    # 0x00 0x29
    SOLC_0_4_17 = r"a165627a7a72305820[0-9a-f]{64}0029"
    # SOLC_0_4_17 = r"^[0-9a-f]*a165627a7a72305820[0-9a-f]{64}0029[0-9a-f]*$"
    # SOLC_0_4_17_D = r"(?<=a165627a7a72305820[0-9a-f]{64}0029)"

    # Experimental option in Solidity due to ABIEncoderV2
    # example: a265627a7a723058201e1bfc77d507025cf70760b0848f01673dd1fb26af9d47b555da548df16224066c6578706572696d656e74616cf50037
    # 0xa2
    # 0x65 'b' 'z' 'z' 'r' '0' 0x58 0x20 <32 bytes swarm hash>
    # 0x6c 'e' 'x' 'p' 'e' 'r' 'i' 'm' 'e' 'n' 't' 'a' 'l' 0xf5
    # 0x00 0x37
    ABIENCODER_V2_1 = r"a265627a7a72305820[0-9a-f]{64}6c6578706572696d656e74616cf50037"
    # ABIENCODER_V2_1 = r"^[0-9a-f]*a265627a7a72305820[0-9a-f]{64}6c6578706572696d656e74616cf50037[0-9a-f]*$"
    # ABIENCODER_V2_1_D = r"(?<=a265627a7a72305820[0-9a-f]{64}6c6578706572696d656e74616cf50037)"

    # From version solc-0.5.9
    # 0xa2
    # 0x65 'b' 'z' 'z' 'r' '0' 0x58 0x20 <32 bytes swarm hash>
    # 0x64 's' 'o' 'l' 'c' 0x43 <3 byte version encoding>
    # 0x00 0x32
    SOLC_0_5_9 = r"a265627a7a72305820[0-9a-f]{64}64736f6c6343[0-9a-f]{6}0032"
    # SOLC_0_5_9 = r"^[0-9a-f]*a265627a7a72305820[0-9a-f]{64}64736f6c6343[0-9a-f]{6}0032[0-9a-f]*$"
    # SOLC_0_5_9_D = r"(?<=a265627a7a72305820[0-9a-f]{64}64736f6c6343[0-9a-f]{6}0032)"

    # Experimental option in Solidity due to ABIEncoderV2
    # example: a365627a7a7230582022316da6de015a68fad6ca8a732898f553832e95b48e9f39b85fe694b2264db26c6578706572696d656e74616cf564736f6c634300050a0040
    # 0xa3
    # 0x65 'b' 'z' 'z' 'r' '0' 0x58 0x20 <32 bytes swarm hash>
    # 0x6c 'e' 'x' 'p' 'e' 'r' 'i' 'm' 'e' 'n' 't' 'a' 'l' 0xf5
    # 0x64 's' 'o' 'l' 'c' 0x43 <3 byte version encoding>
    # 0x00 0x40
    ABIENCODER_V2_2 = r"a365627a7a72305820[0-9a-f]{64}6c6578706572696d656e74616cf564736f6c6343[0-9a-f]{6}0040"
    # ABIENCODER_V2_2 = r"^[0-9a-f]*a365627a7a72305820[0-9a-f]{64}6c6578706572696d656e74616cf564736f6c6343[0-9a-f]{6}0040[0-9a-f]*$"
    # ABIENCODER_V2_2_D = r"(?<=a365627a7a72305820[0-9a-f]{64}6c6578706572696d656e74616cf564736f6c6343[0-9a-f]{6}0040)"

    # From version solc-0.5.12
    # 0xa2
    # 0x65 'b' 'z' 'z' 'r' '1' 0x58 0x20 <32 bytes swarm hash>
    # 0x64 's' 'o' 'l' 'c' 0x43 <3 byte version encoding>
    # 0x00 0x32
    SOLC_0_5_12 = r"a265627a7a72315820[0-9a-f]{64}64736f6c6343[0-9a-f]{6}0032"
    # SOLC_0_5_12 = r"^[0-9a-f]*a265627a7a72315820[0-9a-f]{64}64736f6c6343[0-9a-f]{6}0032[0-9a-f]*$"
    # SOLC_0_5_12_D = r"(?<=a265627a7a72315820[0-9a-f]{64}64736f6c6343[0-9a-f]{6}0032)"

    # Experimental option in Solidity due to ABIEncoderV2
    # example: a365627a7a7231582076f04f08ed9ab2d9078ead8a728e5e444700aed42abb0cd3bd94a1ae5612d38f6c6578706572696d656e74616cf564736f6c63430005110040
    # 0xa3
    # 0x65 'b' 'z' 'z' 'r' '1' 0x58 0x20 <32 bytes swarm hash>
    # 0x6c 'e' 'x' 'p' 'e' 'r' 'i' 'm' 'e' 'n' 't' 'a' 'l' 0xf5
    # 0x64 's' 'o' 'l' 'c' 0x43 <3 byte version encoding>
    # 0x00 0x40
    ABIENCODER_V2_3 = r"a365627a7a72315820[0-9a-f]{64}6c6578706572696d656e74616cf564736f6c6343[0-9a-f]{6}0040"
    # ABIENCODER_V2_3 = r"^[0-9a-f]*a365627a7a72315820[0-9a-f]{64}6c6578706572696d656e74616cf564736f6c6343[0-9a-f]{6}0040[0-9a-f]*$"
    # ABIENCODER_V2_3_D = r"(?<=a365627a7a72315820[0-9a-f]{64}6c6578706572696d656e74616cf564736f6c6343[0-9a-f]{6}0040)"

    # From version solc-0.6.0
    # 0xa2
    # 0x64 'i' 'p' 'f' 's' 0x58 0x22 <34 bytes IPFS hash>
    # 0x64 's' 'o' 'l' 'c' 0x43 <3 byte version encoding>
    # 0x00 0x32
    SOLC_0_6_0 = r"a264697066735822[0-9a-f]{68}64736f6c6343[0-9a-f]{6}0032"
    # SOLC_0_6_0 = r"^[0-9a-f]*a264697066735822[0-9a-f]{68}64736f6c6343[0-9a-f]{6}0032[0-9a-f]*$"
    # SOLC_0_6_0_D = r"(?<=a264697066735822[0-9a-f]{68}64736f6c6343[0-9a-f]{6}0032)"

    # From version solc-0.6.2
    # 0xa2
    # 0x64 'i' 'p' 'f' 's' 0x58 0x22 <34 bytes IPFS hash>
    # 0x64 's' 'o' 'l' 'c' 0x43 <3 byte version encoding>
    # 0x00 0x33
    SOLC_0_6_2 = r"a264697066735822[0-9a-f]{68}64736f6c6343[0-9a-f]{6}0033"
    # SOLC_0_6_2 = r"^[0-9a-f]*a264697066735822[0-9a-f]{68}64736f6c6343[0-9a-f]{6}0033[0-9a-f]*$"
    # SOLC_0_6_2_D = r"(?<=a264697066735822[0-9a-f]{68}64736f6c6343[0-9a-f]{6}0033)"
