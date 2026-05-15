# Pads a binary string with leading zeros until it reaches 32 bits
def add_0_to_32(number: str) -> str:
    b_len: int = len(number)

    while b_len < 32:
        number = "0" + number
        b_len += 1

    return number


# Converts a decimal number to a custom base representation
def convert_base(number: int, base: str) -> str:
    result: str = ""
    len_base: int = len(base)

    while number > 0:
        index: int = number % len_base
        result = base[index] + result
        number = number // len_base
    
    return result


# Rotates bits to the right by k positions
def rotate_right(block: str, k: int) -> str:
    block_len: int = len(block)
    k = k % block_len
    index: int = block_len - k
    
    return block[index:] + block[:index]


# Shifts bits to the right and fills left side with zeros
def shift_right(block: str, k: int) -> str:
    n: int = len(block)
    k %= n

    return "0" * k + block[:n-k]


# Generates a new word in the SHA-256 message schedule
def w_generater(blocks: list[str], i: int) -> str:
    from hash_sha_256.operations import sigma0, sigma1

    w_1: int = int(blocks[i-16], 2)
    w_2: int = int(sigma0(blocks[i-15]), 2)
    w_3: int = int(blocks[i-7], 2)
    w_4: int = int(sigma1(blocks[i-2]), 2)

    total: int = (w_1 + w_2 + w_3 + w_4) % (2**32)
    binary_result: str = add_0_to_32(convert_base(total, "01"))

    return binary_result