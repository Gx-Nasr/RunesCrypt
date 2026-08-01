from .aes_256_utils import *

def SubStates(states):
    for state in states:
        for i, W in enumerate(state):
            state[i] = SubWord(W)


def AddRoundKey(states, round_key):
    for state in states:
        for i, W in enumerate(state):
            state[i] = W_xor(W, round_key[i])

def shift_states(states):
    for state in states:
        for i, W in enumerate(state):
            state[i] = shift_row(W, i)

def gmul2(byte):
    msb = byte[0]

    byte = byte[1:] + '0'

    if msb == '1':
        return xor([byte, "00011011"])

    return byte


def gmul3(byte):
    return xor([gmul2(byte), byte])


def mix_one_column(column):
    a ,b , c, d = column

    c_0 = xor([gmul2(a), gmul3(b), c, d])
    c_1 = xor([a, gmul2(b), gmul3(c), d])
    c_2 = xor([a, b, gmul2(c), gmul3(d)])
    c_3 = xor([gmul3(a), b, c, gmul2(d)])

    return (c_0, c_1, c_2, c_3)

def MixColumns(states):
    for state in states:
        for i in range(4):
            a = state[0][i]
            b = state[1][i]
            c = state[2][i]
            d = state[3][i]
            a, b, c, d = mix_one_column([a, b, c, d])
            state[0][i] = a
            state[1][i] = b
            state[2][i] = c
            state[3][i] = d

