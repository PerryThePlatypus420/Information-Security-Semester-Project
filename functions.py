import random

def pad_or_truncate_key(key):
    if len(key) < 16:  # If key is shorter than 128 bits, pad it with zeros
        key = key + '0' * (16 - len(key))
    elif len(key) > 16:  # If key is longer than 128 bits, truncate it
        key = key[:16]
    return key

def divide_into_substrings(text):
    if len(text) % 16 != 0:
        padding = '0' * (16 - (len(text) % 16))
        text += padding
    substrings = [text[i:i+16] for i in range(0, len(text), 16)]
    return substrings

def merge_substrings(substrings):
    return ''.join(substrings)

def left_round_shift(text, shift):
    return text[shift:] + text[:shift]

def right_round_shift(text, shift):
    return text[-shift:] + text[:-shift]

def generate_s_box(key):
    s_box = [[0] * 16 for _ in range(16)]
    permutation = list(range(256))
    random.seed(key)
    random.shuffle(permutation)
    for i in range(16):
        for j in range(16):
            index = i * 16 + j
            s_box[i][j] = permutation[index]
    return s_box


def xor(text, key):
    key = pad_or_truncate_key(key)
    key = key * ((len(text) + 15) // 16)  # Repeat key to match plaintext length
    result = ""
    for i in range(len(text)):
        result += chr(ord(text[i]) ^ ord(key[i]))
    return result


def encrypt(plaintext, key):
    key = pad_or_truncate_key(key)
    for _ in range(10):
        substrings = divide_into_substrings(plaintext)
        ciphertext = ""
        for substring in substrings:
            half_length = len(substring) // 2
            left_half = substring[:half_length]
            right_half = substring[half_length:]
            key_length = len(key)//2
            shifted_left_half = left_round_shift(left_half, key_length)
            shifted_right_half = right_round_shift(right_half, key_length)
            transposed_ciphertext = shifted_left_half + shifted_right_half
            s_box = generate_s_box(key)
            encrypted_substring = ""
            for char in transposed_ciphertext:
                row = ord(char) // 16
                col = ord(char) % 16
                encrypted_substring += chr(s_box[row][col])
            ciphertext += encrypted_substring
        plaintext = ciphertext
    ciphertext = xor(ciphertext, key)
    return ciphertext

def decrypt(ciphertext, key):
    key = pad_or_truncate_key(key)
    ciphertext = xor(ciphertext, key)
    for _ in range(10):
        substrings = divide_into_substrings(ciphertext)
        plaintext = ""
        for substring in substrings:
            s_box = generate_s_box(key)
            decrypted_substring = ""
            for char in substring:
                for i in range(16):
                    for j in range(16):
                        if s_box[i][j] == ord(char):
                            decrypted_substring += chr(i * 16 + j)
                            break
            half_length = len(decrypted_substring) // 2
            left_half = decrypted_substring[:half_length]
            right_half = decrypted_substring[half_length:]
            key_length = len(key)//2
            shifted_left_half = right_round_shift(left_half, key_length)
            shifted_right_half = left_round_shift(right_half, key_length)
            plaintext += shifted_left_half + shifted_right_half
        ciphertext = plaintext
    plaintext = plaintext.replace("0", "")
    return plaintext


# # Example Usage

plaintext = "free palestine from israel"
key = "israel eww bad bad bad"

print("Plaintext:", plaintext)
print("Key:", key)

ciphertext = encrypt(plaintext, key)
print("Ciphertext:", ciphertext)

decrypted_text = decrypt(ciphertext, key)
print("Decrypted Text:", decrypted_text)