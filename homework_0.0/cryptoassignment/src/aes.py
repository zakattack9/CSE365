from Crypto.Cipher import AES


class AESCipher:

    def __init__(self, key):
        self.key = key

    def encrypt(self, raw):
        cipher = AES.new(self.key, AES.MODE_ECB)
        if len(raw) % 16 != 0:
            raw += ' ' * (16 - (len(raw) % 16))
        return cipher.encrypt(raw)

    def decrypt(self, enc):
        cipher = AES.new(self.key, AES.MODE_ECB)
        overflow = len(enc) % 16
        if overflow != 0:
            enc += b' ' * (16 - overflow)
        return cipher.decrypt(enc)
