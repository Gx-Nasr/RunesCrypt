from .aes_256_utils import *
from .key_expansion import creat_round_key
from .encryption_process_utils import AddRoundKey, MixColumns, shift_states, SubStates

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


def encryption_process(states, round_keys):
    AddRoundKey(states, round_keys[0])

    for i in range(1, 14):
        SubStates(states)
        shift_states(states)
        MixColumns(states)
        AddRoundKey(states, round_keys[i])

    SubStates(states)
    shift_states(states)
    AddRoundKey(states, round_keys[14])


def aes_256(data: str, key: str) -> str:
    states = creat_matrix(data)
    key = creat_matrix(key)
    key = creat_round_key(key)

    encryption_process(states, key)

    res = ""
    res_list = []
    for state in states:
        for col in range(4):
            for row in range(4):
                res_list.append(convert_base(state[row][col], "0123456789abcdef", 2) + '-')

    res = "".join(res_list)
    res = res[:-1]

    return res
