import string
import functions

def brute_force_attack(ciphertext):
    for key_candidate in generate_key_candidates():
        decrypted_text = functions.decrypt(ciphertext, key_candidate)
        
        if is_plaintext_valid(decrypted_text):
            return decrypted_text, key_candidate
    return None, None

def generate_key_candidates():
    # Generate all possible keys in the keyspace
    for key in range(2**128):
        yield bin(key)[2:].zfill(128)  # Convert to binary and zero-fill to 128 bits

def is_plaintext_valid(plaintext):
    # Check if the decrypted text contains only printable ASCII characters
    return all(char in string.printable for char in plaintext)


# Example usage
if __name__ == "__main__":
    ciphertext = "+ô4]1·s`æ±æ¥♥9¾à¿½RRß·`2êÎ9x"
    decrypted_text, key = brute_force_attack(ciphertext)
    if decrypted_text is not None:
        print("Decrypted Text:", decrypted_text)
        print("Key:", key)
    else:
        print("Brute-force attack unsuccessful.")
