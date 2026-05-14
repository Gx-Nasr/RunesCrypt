def add_0_to_32(number):
    b_len = len(number)

    while b_len < 32:
        number = "0" + number
        b_len += 1

    return number

def convert_base(number: int, base: str) -> str:
    result = ""
    len_base = len(base)
    while number > 0:
        index = number % len_base
        result = base[index] + result
        number = number // len_base
    
    return result


def rotate_right(block: str, k: int) -> str:
    block_len = len(block)
    k = k % block_len
    index = block_len - k
    
    return block[index:] + block[:index]


def shift_right(block: str, k: int) -> str:
    n = len(block)
    k %= n

    return "0" * k + block[:n-k]


def w_generater(blocks: list[str], i: int) -> str:
    from hash_sha_256.operations import sigma0, sigma1

    w_1 = int(blocks[i-16], 2)
    w_2 = int(sigma0(blocks[i-15]), 2)
    w_3 = int(blocks[i-7], 2)
    w_4 = int(sigma1(blocks[i-2]), 2)
    total = (w_1 + w_2 + w_3 + w_4) % (2**32)
    binary_result = add_0_to_32(convert_base(total, "01"))

    return binary_result
