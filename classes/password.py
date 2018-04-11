from hashlib import sha256

class Password:
    def __init__(self):
        self.SYMBOLS = ('0123456789!@#$%^&*()-_')
        self.SECRET_KEY = 's3cr3t'
        self.ALPHABET = ('abcdefghijklmnopqrstuvwxyz'
                         'ABCDEFGHIJKLMNOPQRSTUVWXYZ')

    def get_hexdigest(self, plaintext, salt):
        return sha256(salt.encode('utf-8') + plaintext.encode('utf-8')).hexdigest()

    def make_password(self, plaintext, service):
        salt = self.get_hexdigest(self.SECRET_KEY, service)[:20]
        hsh = self.get_hexdigest(salt, plaintext)
        return ''.join((salt, hsh))

    def getPassword(self, plaintext, service, length=10, symbols=True):
        if symbols:
            alphabet = self.ALPHABET + self.SYMBOLS
        else:
            alphabet = self.ALPHABET
        self.length = length

        raw_hexdigest = self.make_password(plaintext, service)

        # Convert the hexdigest into decimal
        num = int(raw_hexdigest, 16)

        # What base will we convert `num` into?
        num_chars = len(alphabet)

        # Build up the new password one "digit" at a time,
        # up to a certain length
        chars = []
        while len(chars) < length:
            num, idx = divmod(num, num_chars)
            chars.append(alphabet[idx])

        return ''.join(chars)
