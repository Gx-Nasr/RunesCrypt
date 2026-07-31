def add_0_to_bn(number: str, add_0) -> str:
    b_len: int = add_0 - len(number)
    if b_len <= 0:
        return number
    zeros = "0" * b_len

    return zeros + number

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


def W_xor(W1, W2):
    W = []
    for i in range(4):
        W.append(xor([W1[i], W2[i]]))

    return W

def rev_shift_row(W, n):
    return W[-n:] + W[:-n]

def creat_rev_matrix(msg):
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
                    bn_char = add_0_to_bn(convert_base(msg[i], base, from_base=16), 8) 
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