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


def convert_base(number: int, base: str, is_nb=0) -> str:
    if is_nb > 0:
        number = int(number, is_nb)
    if number == 0:
        return '0'

    result: str = ""
    len_base: int = len(base)

    while number > 0:
        index: int = number % len_base
        result = base[index] + result
        number = number // len_base
    
    return result


def xor_matrix(matrix1, matrix2):
    matrix = []
    max_len = len(matrix1)
    min_len = len(matrix2)
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
                xor_res = xor([mx_1, mx_2])
                tmp_list[i].append(xor_res)
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

res = xor_matrix(msg_matrxi, pass_matrxi)

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