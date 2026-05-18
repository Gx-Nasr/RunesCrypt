def add_0_to_bn(number: str, add_0) -> str:
    b_len: int = add_0 - len(number)
    if b_len <= 0:
        return number
    zeros = "0" * b_len

    return zeros + number

def xor(binary_list: list[str]) -> str:
    result: list[str] = []
    len_s: int = len(binary_list[0])

    # Loop through each bit position
    for i in range(0, len_s):
        number: int = 0

        # Count number of 1s in current position
        for c in binary_list:
            number += int(c[i])

        # XOR rule: odd number of 1s -> 1, even -> 0
        result.append(str(number % 2))

    return "".join(result)


def convert_base(number: int, base: str, from_base=0) -> str:
    if from_base > 0:
        number = int(number, from_base)
    if number == 0:
        return '0'

    result: str = ""
    len_base: int = len(base)

    while number > 0:
        index: int = number % len_base
        result = base[index] + result
        number = number // len_base
    
    return result

def SubBytes(state_hex):
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
    row = int(state_hex[0], 16)
    column = int(state_hex[1], 16)

    return LookupTable[row][column]



def state(matrix1, matrix2):
    matrix = []
    max_len = len(matrix1)
    min_len = len(matrix2)
    base = "0123456789abcdef"
    a = 0
    b = 0
    while a < max_len:
        if b == min_len:
            b = 0
        i = 0
        tmp_list = [[], [], [], []]
        while i < 4:
            j = 0
            while j < 4:
                mx_1 = matrix1[a][i][j]
                mx_2 = matrix2[b][i][j]
                xor_res = convert_base(xor([mx_1, mx_2]), base, 2)
                tmp_list[i].append(SubBytes(xor_res))
                j += 1
            i += 1
        matrix.append(tmp_list)
        a += 1
        b += 1

    return matrix


def creat_matrix(msg):
    base = "01"
    matrix_list = []
    i = 0
    end = 0
    msg_len = len(msg)
    while i < msg_len:
        j = 0
        tmp_list = [[], [], [], []]

        while j < 4:
            k = 0

            while k < 4:
                if i < msg_len:
                    bn_char = add_0_to_bn(convert_base(ord(msg[i]), base), 8) 
                    tmp_list[k].append(bn_char)

                elif end > 0:
                    tmp_list[k].append(bn_char)

                else:
                    end = 16 - ((j+1) * k)
                    bn_char = add_0_to_bn(convert_base(end, base), 8) 
                    tmp_list[k].append(bn_char)

                k += 1
                i += 1

            j += 1
        matrix_list.append(tmp_list)

    return matrix_list

msg_matrxi = creat_matrix("abdilah mol srdil")
pass_matrxi = creat_matrix("123456")

res = state(msg_matrxi, pass_matrxi)

print("\nfirst matrix:\n")
for c in msg_matrxi:
    for n in c:
        print(n)
    print("\n\n")

print("-"*48)
print("\nsecend matrix:\n")

for c in pass_matrxi:
    for n in c:
        print(n)
    print("\n\n")

print("-"*48)
print("\nXor result:\n")

for c in res:
    for n in c:
        print(n)
    print("\n\n")


#      0    1    2    3    4    5    6    7    8    9    A    B    C    D    E    F
#    ------------------------------------------------------------------------------
# 0 | 63   7C   77   7B   F2   6B   6F   C5   30   01   67   2B   FE   D7   AB   76
# 1 | CA   82   C9   7D   FA   59   47   F0   AD   D4   A2   AF   9C   A4   72   C0
# 2 | B7   FD   93   26   36   3F   F7   CC   34   A5   E5   F1   71   D8   31   15
# 3 | 04   C7   23   C3   18   96   05   9A   07   12   80   E2   EB   27   B2   75
# 4 | 09   83   2C   1A   1B   6E   5A   A0   52   3B   D6   B3   29   E3   2F   84
# 5 | 53   D1   00   ED   20   FC   B1   5B   6A   CB   BE   39   4A   4C   58   CF
# 6 | D0   EF   AA   FB   43   4D   33   85   45   F9   02   7F   50   3C   9F   A8
# 7 | 51   A3   40   8F   92   9D   38   F5   BC   B6   DA   21   10   FF   F3   D2
# 8 | CD   0C   13   EC   5F   97   44   17   C4   A7   7E   3D   64   5D   19   73
# 9 | 60   81   4F   DC   22   2A   90   88   46   EE   B8   14   DE   5E   0B   DB
# A | E0   32   3A   0A   49   06   24   5C   C2   D3   AC   62   91   95   E4   79
# B | E7   C8   37   6D   8D   D5   4E   A9   6C   56   F4   EA   65   7A   AE   08
# C | BA   78   25   2E   1C   A6   B4   C6   E8   DD   74   1F   4B   BD   8B   8A
# D | 70   3E   B5   66   48   03   F6   0E   61   35   57   B9   86   C1   1D   9E
# E | E1   F8   98   11   69   D9   8E   94   9B   1E   87   E9   CE   55   28   DF
# F | 8C   A1   89   0D   BF   E6   42   68   41   99   2D   0F   B0   54   BB   16

