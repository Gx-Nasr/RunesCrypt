from hash_sha_256.sha_256_utils import add_0_to_32, rotate_right, shift_right, convert_base

def xor(binary_list: list[str]) -> str:
    result = []
    len_s = len(binary_list[0])
    for i in range(0, len_s):
        number = 0

        for c in binary_list:
            number += int(c[i])

        result.append(str(number%2))

    return "".join(result)

def sigma0(x: str) -> str:
    x = add_0_to_32(x)
    r_7 = rotate_right(x, 7)
    r_18 = rotate_right(x, 18)
    s_3 = shift_right(x, 3)
    return xor([r_7, r_18, s_3])


def sigma1(x: str) -> str:
    x = add_0_to_32(x)
    r_17 = rotate_right(x, 17)
    r_19 = rotate_right(x, 19)
    s_10 = shift_right(x, 10)
    return xor([r_17, r_19, s_10])

def big_sigma0(x: str) -> str:
    x = add_0_to_32(x)
    r_2 = rotate_right(x, 2)
    r_13 = rotate_right(x, 13)
    r_22 = rotate_right(x, 22)
    return xor([r_2, r_13, r_22])

def big_sigma1(x: str) -> str:
    x = add_0_to_32(x)
    r_6 = rotate_right(x, 6)
    r_11 = rotate_right(x, 11)
    r_25 = rotate_right(x, 25)
    return xor([r_6, r_11, r_25])


def ch(x: int, y: int, z: int) -> str:
    x = add_0_to_32(convert_base(x, "01"))
    y = add_0_to_32(convert_base(y, "01"))
    z = add_0_to_32(convert_base(z, "01"))

    i = 0
    choice = ""
    for c in x:
        if c == "1":
            choice += y[i]
        else:
            choice += z[i]
        i += 1

    return choice


def maj(x: int, y: int, z: int) -> str:
    x = add_0_to_32(convert_base(x, "01"))
    y = add_0_to_32(convert_base(y, "01"))
    z = add_0_to_32(convert_base(z, "01"))

    choice = []
    x_len = len(x)
    l_c = [x, y, z]
    for n in range(0, x_len):
        zero = 0
        one = 0
        for num in l_c:
            if num[n] == "1":
                one += 1
            else:
                zero += 1

        choice.append("1" if one >= 2 else "0")

    return "".join(choice)