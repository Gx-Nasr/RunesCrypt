from decrypt_aes_256_utils import *
from gmul import gmul9, gmul11, gmul13, gmul14
from key_expansion import creat_round_key

def RevSubBytes(hex):
    if len(hex) == 1:
        hex = '0' + hex
    RevLookupTable = [
        ["52","09","6A","D5","30","36","A5","38","BF","40","A3","9E","81","F3","D7","FB"],
        ["7C","E3","39","82","9B","2F","FF","87","34","8E","43","44","C4","DE","E9","CB"],
        ["54","7B","94","32","A6","C2","23","3D","EE","4C","95","0B","42","FA","C3","4E"],
        ["08","2E","A1","66","28","D9","24","B2","76","5B","A2","49","6D","8B","D1","25"],
        ["72","F8","F6","64","86","68","98","16","D4","A4","5C","CC","5D","65","B6","92"],
        ["6C","70","48","50","FD","ED","B9","DA","5E","15","46","57","A7","8D","9D","84"],
        ["90","D8","AB","00","8C","BC","D3","0A","F7","E4","58","05","B8","B3","45","06"],
        ["D0","2C","1E","8F","CA","3F","0F","02","C1","AF","BD","03","01","13","8A","6B"],
        ["3A","91","11","41","4F","67","DC","EA","97","F2","CF","CE","F0","B4","E6","73"],
        ["96","AC","74","22","E7","AD","35","85","E2","F9","37","E8","1C","75","DF","6E"],
        ["47","F1","1A","71","1D","29","C5","89","6F","B7","62","0E","AA","18","BE","1B"],
        ["FC","56","3E","4B","C6","D2","79","20","9A","DB","C0","FE","78","CD","5A","F4"],
        ["1F","DD","A8","33","88","07","C7","31","B1","12","10","59","27","80","EC","5F"],
        ["60","51","7F","A9","19","B5","4A","0D","2D","E5","7A","9F","93","C9","9C","EF"],
        ["A0","E0","3B","4D","AE","2A","F5","B0","C8","EB","BB","3C","83","53","99","61"],
        ["17","2B","04","7E","BA","77","D6","26","E1","69","14","63","55","21","0C","7D"]
    ]

    row = int(hex[0], 16)
    column = int(hex[1], 16)

    return RevLookupTable[row][column]



def AddRoundKey(states, round_key):
    for state in states:
        for i, W in enumerate(state):
            state[i] = W_xor(W, round_key[i])

def RevSubWord(W):
    new_w = []
    base = "0123456789abcdef"
    for byte in W:
        tmp_w = add_0_to_bn(convert_base(RevSubBytes(convert_base(byte, base, 2)), '01', 16), 8)
        new_w.append(tmp_w)

    return new_w


def rev_shift_states(states):
    for state in states:
        for i, W in enumerate(state):
            state[i] = rev_shift_row(W, i)

def RevSubStates(states):
    for state in states:
        for i, W in enumerate(state):
            state[i] = RevSubWord(W)


def rev_mix_one_column(column):
    a, b, c, d = column

    c_0 = xor([gmul14(a), gmul11(b), gmul13(c), gmul9(d)])
    c_1 = xor([gmul9(a),  gmul14(b), gmul11(c), gmul13(d)])
    c_2 = xor([gmul13(a), gmul9(b),  gmul14(c), gmul11(d)])
    c_3 = xor([gmul11(a), gmul13(b), gmul9(c),  gmul14(d)])

    return (c_0, c_1, c_2, c_3)


def RevMixColumns(states):
    for state in states:
        for col in range(4):
            a = state[0][col]
            b = state[1][col]
            c = state[2][col]
            d = state[3][col]

            a, b, c, d = rev_mix_one_column([a, b, c, d])

            state[0][col] = a
            state[1][col] = b
            state[2][col] = c
            state[3][col] = d

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

def decrypting_process(states, round_keys):
    AddRoundKey(states, round_keys[14])
    for i in range(13, 0, -1):
        rev_shift_states(states)
        RevSubStates(states)
        AddRoundKey(states, round_keys[i])
        RevMixColumns(states)

    rev_shift_states(states)
    RevSubStates(states)
    AddRoundKey(states, round_keys[0])

def aes_256(data: str, key: str):
    data = data.split("-")
    states = creat_rev_matrix(data)
    key = creat_matrix(key)
    key = creat_round_key(key)

    decrypting_process(states, key)

    res = []

    for state in states:
        for col in range(4):
            for row in range(4):
                res.append(chr(int(state[row][col], 2)))

    plaintext = "".join(res)

    return plaintext
