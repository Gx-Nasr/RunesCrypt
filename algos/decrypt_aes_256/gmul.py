from decrypt_aes_256_utils import xor


def gmul2(byte):
    msb = byte[0]

    byte = byte[1:] + '0'

    if msb == '1':
        return xor([byte, "00011011"])

    return byte

def gmul9(byte):
    x2 = gmul2(byte)
    x4 = gmul2(x2)
    x8 = gmul2(x4)

    return xor([x8, byte])

def gmul11(byte):
    x2 = gmul2(byte)
    x4 = gmul2(x2)
    x8 = gmul2(x4)

    return xor([x8, x2, byte])

def gmul13(byte):
    x2 = gmul2(byte)
    x4 = gmul2(x2)
    x8 = gmul2(x4)

    return xor([x8, x4, byte])

def gmul14(byte):
    x2 = gmul2(byte)
    x4 = gmul2(x2)
    x8 = gmul2(x4)

    return xor([x8, x4, x2])