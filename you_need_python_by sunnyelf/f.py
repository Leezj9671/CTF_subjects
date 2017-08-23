import hashlib

def sha1(string):
    return hashlib.sha1(string).hexdigest()


def calc(strSHA1):
    r = 0
    for i in strSHA1:
        r += int('0x%s' % i, 16)

    return r


def encrypt(plain, key):
    keySHA1 = sha1(key)
    intSHA1 = calc(keySHA1)
    r = []
    for i in range(len(plain)):
        r.append(ord(plain[i]) + int('0x%s' % keySHA1[i % 40], 16) - intSHA1)
        intSHA1 = calc(sha1(plain[:i + 1])[:20] + sha1(str(intSHA1))[:20])

    return ''.join(map(lambda x: str(x), r))


if __name__ == '__main__':
    # key = raw_input('[*] Please input key:')
    # plain = raw_input('[*] Please input flag:')
    # encryptText = encrypt(plain, key)
    cipherText = '-185-147-211-221-164-217-188-169-205-174-211-225-191-234-148-199-198-253-175-157-222-135-240-229-201-154-178-187-244-183-212-222-164'
    # if encryptText == cipherText:
    #     print '[>] Congratulations! Flag is: %s' % plain
    #     exit()
    # else:
    #     print '[!] Key or flag is wrong, try again:)'
    #     exit()

    key = 'I_4m-k3y'
    flag =''
    for i in range(len(cipherText)/4):
        # 一般31-128才是常用字符
        for j in range(31, 128):
            if encrypt(flag+chr(j), key) == cipherText[0:i*4+4]:
                print j,
                flag += chr(j)
                break
    print '\n'
    print flag