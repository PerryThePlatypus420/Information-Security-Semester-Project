import streamlit as st
import functions

def encrypt(plaintext, key):
    ciphertext = functions.encrypt(plaintext, key)
    return ciphertext

def decrypt(ciphertext, key):
    plaintext = functions.decrypt(ciphertext, key)
    return plaintext

def main():
    st.title("YASSIPHER")
    with st.form("Encryption and Decryption"):
        plaintext = st.text_input("Enter the plaintext:").strip()
        key = st.text_input("Enter the key:").strip()
        
        submit_encrypt = st.form_submit_button("Encrypt")
        submit_decrypt = st.form_submit_button("Decrypt")

        if submit_encrypt:
            encrypted_text = encrypt(plaintext, key)
            st.success(f"Encrypted Text: {encrypted_text}")
            
        if submit_decrypt:
            decrypted_text = decrypt(plaintext, key)
            st.success(f"Decrypted Text: {decrypted_text}")

if __name__ == "__main__":
    main()
