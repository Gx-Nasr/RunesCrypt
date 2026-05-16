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
    result: str = ""
    len_base: int = len(base)

    while number > 0:
        index: int = number % len_base
        result = base[index] + result
        number = number // len_base
    
    return result



def creat_matrix(msg):
    base = "0123456789abcdef"
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
                    hx_char = convert_base(ord(msg[i]), base) 
                    tmp_list[k].append(hx_char)

                elif end > 0:
                    tmp_list[k].append(hx_char)

                else:
                    end = 16 - ((j+1) * k)
                    hx_char = convert_base(end, base) 
                    tmp_list[k].append(hx_char)

                k += 1
                i += 1

            j += 1
        matrix_list.append(tmp_list)

    return matrix_list

msg_matrxi = creat_matrix("abdilah mol srdil")
pass_matrxi = creat_matrix("123456")

for c in msg_matrxi:
    for n in c:
        print(n)
    print("\n")


for c in pass_matrxi:
    for n in c:
        print(n)
    print("\n")
