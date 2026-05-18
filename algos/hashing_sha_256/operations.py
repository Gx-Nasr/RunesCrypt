from algos.hashing_sha_256.sha_256_utils import add_0_to_bn, rotate_right, shift_right, convert_base


# Perform XOR operation on multiple binary strings
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


# Small sigma0 function used in SHA-256 message schedule
def sigma0(x: str) -> str:
    x = add_0_to_bn(x, 32)

    # Right rotations and right shift
    r_7: str = rotate_right(x, 7)
    r_18: str = rotate_right(x, 18)
    s_3: str = shift_right(x, 3)

    # XOR all results together
    return xor([r_7, r_18, s_3])


# Small sigma1 function used in SHA-256 message schedule
def sigma1(x: str) -> str:
    x = add_0_to_bn(x, 32)

    r_17: str = rotate_right(x, 17)
    r_19: str = rotate_right(x, 19)
    s_10: str = shift_right(x, 10)

    return xor([r_17, r_19, s_10])


# Big Sigma0 function used in SHA-256 compression
def big_sigma0(x: str) -> str:
    x = add_0_to_bn(x, 32)

    r_2: str = rotate_right(x, 2)
    r_13: str = rotate_right(x, 13)
    r_22: str = rotate_right(x, 22)

    return xor([r_2, r_13, r_22])


# Big Sigma1 function used in SHA-256 compression
def big_sigma1(x: str) -> str:
    x = add_0_to_bn(x, 32)

    r_6: str = rotate_right(x, 6)
    r_11: str = rotate_right(x, 11)
    r_25: str = rotate_right(x, 25)

    return xor([r_6, r_11, r_25])


# Choice function (Ch)
# Chooses bits from y or z depending on x
def ch(x: int, y: int, z: int) -> str:
    # Convert numbers to 32-bit binary strings
    x = add_0_to_bn(convert_base(x, "01"), 32)
    y = add_0_to_bn(convert_base(y, "01"), 32)
    z = add_0_to_bn(convert_base(z, "01"), 32)

    i: int = 0
    choice: str = ""

    # If bit in x is 1 -> take bit from y
    # Else -> take bit from z
    for c in x:
        if c == "1":
            choice += y[i]
        else:
            choice += z[i]

        i += 1

    return choice


# Majority function (Maj)
# Returns the majority bit among x, y, and z
def maj(x: int, y: int, z: int) -> str:
    # Convert numbers to 32-bit binary strings
    x = add_0_to_bn(convert_base(x, "01"), 32)
    y = add_0_to_bn(convert_base(y, "01"), 32)
    z = add_0_to_bn(convert_base(z, "01"), 32)

    choice: list[str] = []
    x_len: int = len(x)

    # Store all binaries in one list
    l_c: list[str] = [x, y, z]

    # Check each bit position
    for n in range(0, x_len):
        zero: int = 0
        one: int = 0

        # Count number of 0s and 1s
        for num in l_c:
            if num[n] == "1":
                one += 1
            else:
                zero += 1

        # Majority wins
        choice.append("1" if one >= 2 else "0")

    return "".join(choice)