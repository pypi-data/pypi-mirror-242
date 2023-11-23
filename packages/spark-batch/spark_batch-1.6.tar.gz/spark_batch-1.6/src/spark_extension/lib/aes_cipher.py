from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from base64 import b64encode, b64decode
from Crypto.Util.Padding import pad, unpad
import string

class AESCipher:
    def __init__(self, key_str, iv_str):
        self.key = key_str.encode('utf-8')
        self.iv = iv_str.encode('utf-8')

    def encrypt(self, plaintext):
        cipher = Cipher(algorithms.AES(self.key), modes.CBC(self.iv), backend=default_backend())
        encryptor = cipher.encryptor()

        # Apply PKCS7 padding
        plaintext_padded = pad(plaintext.encode('utf-8'), algorithms.AES.block_size)

        ciphertext = encryptor.update(plaintext_padded) + encryptor.finalize()
        return b64encode(ciphertext).decode('utf-8')

    def decrypt(self, ciphertext):
        return self._decrypt(ciphertext)
    
    def decrypt_nopading(self, ciphertext):
        return self._decrypt(ciphertext, padding=False, remove_control_chars=True)

    def _decrypt(self, ciphertext, padding=True, remove_control_chars=False):
        ciphertext = b64decode(ciphertext)
        cipher = Cipher(algorithms.AES(self.key), modes.CBC(self.iv), backend=default_backend())
        decryptor = cipher.decryptor()

        # Decrypt the data
        plaintext_padded = decryptor.update(ciphertext) + decryptor.finalize()

        # Remove PKCS7 padding
        plaintext = unpad(plaintext_padded, algorithms.AES.block_size) if padding else plaintext_padded

        if remove_control_chars:
             plaintext = self.remove_control_characters(plaintext)

        if plaintext is not None:
            return plaintext.decode('utf-8')

        return None 

    def remove_control_characters(self, text):
        # excluding specific ones like tab, newline, and carriage return
        control_characters = bytes([char for char in range(32) if char not in [9, 10, 13]])
        cleaned_data = text.translate(None, control_characters)
        return cleaned_data

# 예제 사용
if __name__ == "__main__":
    # 생성된 AESCipher 인스턴스
    aes_cipher = AESCipher("BCParkingWeb2022BCParkingWeb2022", "BCParkingWeb2022")

    # 암호화 예제
    plaintext = "Hello!"
    encrypted_text = aes_cipher.encrypt(plaintext)
    print("Encrypted:", encrypted_text)

    # 복호화 예제
    decrypted_text = aes_cipher.decrypt(encrypted_text)
    print("Decrypted:", decrypted_text)
    
    # 복호화 예제
    decrypted_text = aes_cipher.decrypt_nopading("30AN2+xpbvqAktXEEiY00Q==")
    print("Decrypted:", decrypted_text)    
