from Crypto.PublicKey import RSA


class RSACipher:

    def __init__(self, publicKeyFileName, privateKeyFileName):
        """
        Generate a RSA key pair for server
        """
        try:
            f = open(privateKeyFileName, 'rb')
            self.keys = RSA.importKey(f.read())
        except FileNotFoundError:
            self.keys = RSA.generate(2048)
            self.publickey = self.keys.publickey()
            # export public and private keys
            privHandle = open(privateKeyFileName, 'wb')
            privHandle.write(self.keys.exportKey('PEM'))
            privHandle.close()

            pubHandle = open(publicKeyFileName, 'wb')
            pubHandle.write(self.keys.publickey().exportKey())
            pubHandle.close()
        self.publickey = self.keys.publickey()

    def decrypt(self, ciphertext):
        """-
        Decrypt a ciphertext
        """
        return self.keys.decrypt(ciphertext)

    def encrypt(self, message):
        """
        Encrypt a message
        """
        return self.publickey.encrypt(message, 32)
