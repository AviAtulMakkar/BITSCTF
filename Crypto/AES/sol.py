import multiprocessing
from aes import AES # Ensure aes.py from the challenge is in the same directory

# Configuration
KEY_HINT = bytes.fromhex("26ab77cadcca0ed41b03c8f2e5")
# Replace these with actual values from your output.txt
PT = bytes.fromhex("PASTE_ONE_PLAINTEXT_HEX_HERE") 
EXPECTED_CT = bytes.fromhex("PASTE_CORRESPONDING_CIPHERTEXT_HEX_HERE")
FLAG_ENC = bytes.fromhex("PASTE_ENCRYPTED_FLAG_HEX_HERE")

def check_first_byte(b1):
    """Worker function to brute force the remaining 2 bytes for a given first byte"""
    for b2 in range(256):
        for b3 in range(256):
            guess_key = KEY_HINT + bytes([b1, b2, b3])
            cipher = AES(guess_key)
            
            # Known-Plaintext oracle check
            if cipher.encrypt(PT) == EXPECTED_CT:
                print(f"\n[+] Key Found: {guess_key.hex()}")
                
                # Decrypt Flag immediately upon finding key
                flag_cipher = AES(guess_key)
                decrypted_flag = flag_cipher.decrypt(FLAG_ENC)
                print(f"[+] Flag: {decrypted_flag}")
                return guess_key
    return None

if __name__ == "__main__":
    print(f"[*] Starting brute force for 2^24 combinations...")
    # Adjust processes based on your CPU thread count
    with multiprocessing.Pool(processes=20) as pool:
        pool.map(check_first_byte, range(256))