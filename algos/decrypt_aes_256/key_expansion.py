from .decrypt_aes_256_utils import *

def SubBytes(hex):
    if len(hex) == 1:
        hex = '0' + hex
    LookupTable = [
        ["63", "7C", "77", "7B", "F2", "6B", "6F", "C5", "30", "01", "67", "2B", "FE", "D7", "AB", "76"],
        ["CA", "82", "C9", "7D", "FA", "59", "47", "F0", "AD", "D4", "A2", "AF", "9C", "A4", "72", "C0"],
        ["B7", "FD", "93", "26", "36", "3F", "F7", "CC", "34", "A5", "E5", "F1", "71", "D8", "31", "15"],
        ["04", "C7", "23", "C3", "18", "96", "05", "9A", "07", "12", "80", "E2", "EB", "27", "B2", "75"],
        ["09", "83", "2C", "1A", "1B", "6E", "5A", "A0", "52", "3B", "D6", "B3", "29", "E3", "2F", "84"],
        ["53", "D1", "00", "ED", "20", "FC", "B1", "5B", "6A", "CB", "BE", "39", "4A", "4C", "58", "CF"],
        ["D0", "EF", "AA", "FB", "43", "4D", "33", "85", "45", "F9", "02", "7F", "50", "3C", "9F", "A8"],
        ["51", "A3", "40", "8F", "92", "9D", "38", "F5", "BC", "B6", "DA", "21", "10", "FF", "F3", "D2"],
        ["CD", "0C", "13", "EC", "5F", "97", "44", "17", "C4", "A7", "7E", "3D", "64", "5D", "19", "73"],
        ["60", "81", "4F", "DC", "22", "2A", "90", "88", "46", "EE", "B8", "14", "DE", "5E", "0B", "DB"],
        ["E0", "32", "3A", "0A", "49", "06", "24", "5C", "C2", "D3", "AC", "62", "91", "95", "E4", "79"],
        ["E7", "C8", "37", "6D", "8D", "D5", "4E", "A9", "6C", "56", "F4", "EA", "65", "7A", "AE", "08"],
        ["BA", "78", "25", "2E", "1C", "A6", "B4", "C6", "E8", "DD", "74", "1F", "4B", "BD", "8B", "8A"],
        ["70", "3E", "B5", "66", "48", "03", "F6", "0E", "61", "35", "57", "B9", "86", "C1", "1D", "9E"],
        ["E1", "F8", "98", "11", "69", "D9", "8E", "94", "9B", "1E", "87", "E9", "CE", "55", "28", "DF"],
        ["8C", "A1", "89", "0D", "BF", "E6", "42", "68", "41", "99", "2D", "0F", "B0", "54", "BB", "16"]
    ]
    row = int(hex[0], 16)
    column = int(hex[1], 16)

    return LookupTable[row][column]

def SubWord(W):
    new_w = []
    base = "0123456789abcdef"
    for byte in W:
        tmp_w = add_0_to_bn(convert_base(SubBytes(convert_base(byte, base, 2)), '01', 16), 8)
        new_w.append(tmp_w)

    return new_w

def g(W: list, for_xor: str):
    W = W.copy()

    tmp = W.pop(0)
    W.append(tmp)
    base = "0123456789abcdef"

    for i, byte in enumerate(W):
        s_byte = SubBytes(convert_base(byte, base, 2))
        W[i] = add_0_to_bn(convert_base(s_byte, "01", 16), 8)

    W[0] = xor([W[0], for_xor])

    return W


def creat_round_key(p_b: list):
    W0 = [p_b[0][0][0], p_b[0][1][0], p_b[0][2][0], p_b[0][3][0]]
    W1 = [p_b[0][0][1], p_b[0][1][1], p_b[0][2][1], p_b[0][3][1]]
    W2 = [p_b[0][0][2], p_b[0][1][2], p_b[0][2][2], p_b[0][3][2]]
    W3 = [p_b[0][0][3], p_b[0][1][3], p_b[0][2][3], p_b[0][3][3]]

    W4 = [p_b[1][0][0], p_b[1][1][0], p_b[1][2][0], p_b[1][3][0]]
    W5 = [p_b[1][0][1], p_b[1][1][1], p_b[1][2][1], p_b[1][3][1]]
    W6 = [p_b[1][0][2], p_b[1][1][2], p_b[1][2][2], p_b[1][3][2]]
    W7 = [p_b[1][0][3], p_b[1][1][3], p_b[1][2][3], p_b[1][3][3]]
    W8 = W_xor(W0, g(W7, "00000001"))
    W9 = W_xor(W1, W8)
    W10 = W_xor(W2, W9)
    W11 = W_xor(W3, W10)

    W12 = W_xor(W4, SubWord(W11))
    W13 = W_xor(W5, W12)
    W14 = W_xor(W6, W13)
    W15 = W_xor(W7, W14)

    W16 = W_xor(W8, g(W15, "00000010"))
    W17 = W_xor(W9, W16)
    W18 = W_xor(W10, W17)
    W19 = W_xor(W11, W18)

    W20 = W_xor(W12, SubWord(W19))
    W21 = W_xor(W13, W20)
    W22 = W_xor(W14, W21)
    W23 = W_xor(W15, W22)

    W24 = W_xor(W16, g(W23, "00000100"))
    W25 = W_xor(W17, W24)
    W26 = W_xor(W18, W25)
    W27 = W_xor(W19, W26)

    W28 = W_xor(W20, SubWord(W27))
    W29 = W_xor(W21, W28)
    W30 = W_xor(W22, W29)
    W31 = W_xor(W23, W30)

    W32 = W_xor(W24, g(W31, "00001000"))
    W33 = W_xor(W25, W32)
    W34 = W_xor(W26, W33)
    W35 = W_xor(W27, W34)

    W36 = W_xor(W28, SubWord(W35))
    W37 = W_xor(W29, W36)
    W38 = W_xor(W30, W37)
    W39 = W_xor(W31, W38)

    W40 = W_xor(W32, g(W39, "00010000"))
    W41 = W_xor(W33, W40)
    W42 = W_xor(W34, W41)
    W43 = W_xor(W35, W42)

    W44 = W_xor(W36, SubWord(W43))
    W45 = W_xor(W37, W44)
    W46 = W_xor(W38, W45)
    W47 = W_xor(W39, W46)

    W48 = W_xor(W40, g(W47, "00100000"))
    W49 = W_xor(W41, W48)
    W50 = W_xor(W42, W49)
    W51 = W_xor(W43, W50)

    W52 = W_xor(W44, SubWord(W51))
    W53 = W_xor(W45, W52)
    W54 = W_xor(W46, W53)
    W55 = W_xor(W47, W54)

    W56 = W_xor(W48, g(W55, "01000000"))
    W57 = W_xor(W49, W56)
    W58 = W_xor(W50, W57)
    W59 = W_xor(W51, W58)

    return [
        [W0, W1, W2, W3],
        [W4, W5, W6, W7],
        [W8, W9, W10, W11],
        [W12, W13, W14, W15],
        [W16, W17, W18, W19],
        [W20, W21, W22, W23],
        [W24, W25, W26, W27],
        [W28, W29, W30, W31],
        [W32, W33, W34, W35],
        [W36, W37, W38, W39],
        [W40, W41, W42, W43],
        [W44, W45, W46, W47],
        [W48, W49, W50, W51],
        [W52, W53, W54, W55],
        [W56, W57, W58, W59],
    ]