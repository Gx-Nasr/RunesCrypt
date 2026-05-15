from hash_sha_256.sha_256_utils import convert_base, w_generater
from hash_sha_256.operations import big_sigma1, big_sigma0, ch, maj


# Splits a 512-bit binary string into 32-bit blocks
def creat_blocks(binary_block: str) -> list[str]:
    blocks_list: list[str] = []
    str_block: str = ""
    i: int = 0

    for c in binary_block:
        if i == 32:
            blocks_list.append(str_block)
            str_block = ""
            i = 0

        str_block += c
        i += 1

    blocks_list.append(str_block)
    
    return blocks_list


# Converts the password into padded SHA-256 binary blocks
def binary_blocks(password: str) -> list[str]:
    result: str = ""
    num_ord: int = 0

    for c in password:
        num_ord = ord(c)
        binary_number: str = convert_base(num_ord, "01")

        while 8 > len(binary_number):
            binary_number = '0' + binary_number

        result += binary_number

    result += '1'

    i: int = len(result)

    while i < 448:
        result += '0'
        i += 1

    len_number: int = len(password) * 8
    binary_len: str = convert_base(len_number, "01")

    while i < 512 - len(binary_len):
        result += '0'
        i += 1

    result += binary_len
    
    return creat_blocks(result)


# Computes the SHA-256 hash of a password
def sha_256(hash_string: str) -> str:
    blocks: list[str] = binary_blocks(hash_string)

    # Generate remaining message schedule words
    for i in range(16, 64):
        new_w: str = w_generater(blocks, i)
        blocks.append(new_w)

    # Initial hash values
    H: list[int] = [
        int("6a09e667", 16),
        int("bb67ae85", 16),
        int("3c6ef372", 16),
        int("a54ff53a", 16),
        int("510e527f", 16),
        int("9b05688c", 16),
        int("1f83d9ab", 16),
        int("5be0cd19", 16)
    ]

    a, b, c, d, e, f, g, h = H

    # SHA-256 round constants
    K: list[str] = [
        "428a2f98", "71374491", "b5c0fbcf", "e9b5dba5",
        "3956c25b", "59f111f1", "923f82a4", "ab1c5ed5",
        "d807aa98", "12835b01", "243185be", "550c7dc3",
        "72be5d74", "80deb1fe", "9bdc06a7", "c19bf174",
        "e49b69c1", "efbe4786", "0fc19dc6", "240ca1cc",
        "2de92c6f", "4a7484aa", "5cb0a9dc", "76f988da",
        "983e5152", "a831c66d", "b00327c8", "bf597fc7",
        "c6e00bf3", "d5a79147", "06ca6351", "14292967",
        "27b70a85", "2e1b2138", "4d2c6dfc", "53380d13",
        "650a7354", "766a0abb", "81c2c92e", "92722c85",
        "a2bfe8a1", "a81a664b", "c24b8b70", "c76c51a3",
        "d192e819", "d6990624", "f40e3585", "106aa070",
        "19a4c116", "1e376c08", "2748774c", "34b0bcb5",
        "391c0cb3", "4ed8aa4a", "5b9cca4f", "682e6ff3",
        "748f82ee", "78a5636f", "84c87814", "8cc70208",
        "90befffa", "a4506ceb", "bef9a3f7", "c67178f2"
    ]

    # Main SHA-256 compression loop
    for t in range(0, 64):
        b_sigma1: int = int(big_sigma1(convert_base(e, "01")), 2)
        ch_1: int = int(ch(e, f, g), 2)
        Wt: int = int(blocks[t], 2)
        Kt: int = int(K[t], 16)
    
        T1: int = (h + b_sigma1 + ch_1 + Kt + Wt) % (2**32)

        m: int = int(maj(a, b, c), 2)
        b_sigma0: int = int(big_sigma0(convert_base(a, "01")), 2)

        T2: int = (b_sigma0 + m) % (2**32)

        tmp1: int = (T1 + T2) % (2**32)
        tmp2: int = (d + T1) % (2**32)

        d = c
        c = b
        b = a
        a = tmp1

        h = g
        g = f
        f = e
        e = tmp2

    # Update final hash values
    H[0] = (H[0] + a) % (2**32)
    H[1] = (H[1] + b) % (2**32)
    H[2] = (H[2] + c) % (2**32)
    H[3] = (H[3] + d) % (2**32)
    H[4] = (H[4] + e) % (2**32)
    H[5] = (H[5] + f) % (2**32)
    H[6] = (H[6] + g) % (2**32)
    H[7] = (H[7] + h) % (2**32)

    # Convert final hash to hexadecimal string
    result: str = ""

    for w in H:
        result += convert_base(w, "0123456789abcdef")

    return result
