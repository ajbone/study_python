# !/usr/bin/env python
# coding: utf-8
'''

'''

from Crypto.Cipher import AES
from binascii import b2a_hex, a2b_hex
import base64
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class MyCrypt():
    def __init__(self, key):
        self.key = key
        self.mode = AES.MODE_CBC

    def myencrypt(self, text):
        length = 16
        count = len(text)
        print count
        if count < length:
            add = length - count
            text= text + ('\0' * add)

        elif count > length:
            add = (length -(count % length))
            text= text + ('\0' * add)

        # print len(text)
        cryptor = AES.new(self.key, self.mode, b'0000000000000000')
        self.ciphertext = cryptor.encrypt(text)
        print self.ciphertext
        return base64.encrypt(self.ciphertext)

    def mydecrypt(self, text):
        cryptor = AES.new(self.key, self.mode, b'0000000000000000')
        plain_text = cryptor.decrypt(base64.b64decode(text))
        print plain_text
        return plain_text

if __name__ == '__main__':
    mycrypt = MyCrypt('EPhijQiyiIU4wx9EscgoUg==')
    e = mycrypt.myencrypt('hello,world!')
    #e = "fB44DrojAVbj/DMaa294PpShmaQqgN5mkkU6XvgeqT5hUyGXTF2HIpdbLWdSARS8IEZFeQK4GLZJZh2D5WFJ8qnyEnUWaZplOYkMdUGDdrZQcq4qSUa66zDgOa1q6WkIGv2MmIGbKdOMXsd+X/YJxVajM4Oxlr79kXaHVLm32tlpXCj7ctm8Sh5QH2F/WQrq45YwHHNrgp94qtrQLp7C23J/vu9URCHfQdKqVlK+69bRWujbGdTJGWsFvXTDoDJn4u/dqgBEoGWk6cFbCFJlLARNLUCw3e2qZoVFcURatA7768Zx1CIEFsTVzLia1KmPl1Bx+3jQHCqQMaYUB8wgLsz76ZJv7u87cbz0vBL83s331VZh0p+cLbC5GJnYUFcdPndT6WlfD0Kd/9OEDR4MCCL6y7FrxYEvMuYvmx3u8IuBi1EO2XRZnYpab/8DMSfGN/MmdbKcCYWFGfW11bedq+dYH3pw6mx3kviM0yE7TEhcPEu4cBQxomqfM58do54z3rJLTEBQMg7iSWGLHke1Kw=="
    d = mycrypt.mydecrypt(e)
    print "11111111111111111111111111111"
    print e
    print "22222222222222222222222222222"
    print d