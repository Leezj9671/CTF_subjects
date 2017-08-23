# Solution
解压zip有两个文件，一个是flag.py，一个是key_is_here_but_do_you_know_rfc4042。
首先第一步看提示rfc4042的文件，查询可得，它是utf9或者是utf18的编码。在github上找到utf9解码的库，代码如下：
```
import utf9

dt = ''
with open('key_is_here_but_do_you_know_rfc4042', 'r') as f:
    t = f.read()
    dt = utf9.utf9decode(t)
print dt
```
解出为
```
_____*((__//__+___+______-____%____)**((___%(___-_))+________+(___%___+_____+_______%__+______-(______//(_____%___)))))+__*(((________/__)+___%__+_______-(________//____))**(_*(_____+_____)+_______+_________%___))+________*(((_________//__+________%__)+(_______-_))**((___+_______)+_________-(______//__)))+_______*((___+_________-(______//___-_______%__%_))**(_____+_____+_____))+__*(__+_________-(___//___-_________%_____%__))**(_________-____+_______)+(___+_______)**(________%___%__+_____+______)+(_____-__)*((____//____-_____%____%_)+_________)**(_____-(_______//_______+_________%___)+______)+(_____+(_________%_______)*__+_)**_________+_______*(((_________%_______)*__+_______-(________//________))**_______)+(________/__)*(((____-_+_______)*(______+____))**___)+___*((__+_________-_)**_____)+___*(((___+_______-______/___+__-_________%_____%__)*(___-_+________/__+_________%_____))**__)+(_//_)*(((________%___%__+_____+_____)%______)+_______-_)**___+_____*((______/(_____%___))+_______)*((_________%_______)*__+_____+_)+___//___+_________+_________/___
```
刚开始还以为是类似brainfuck之类的东西，但是观察到有括号和运算符，于是猜测是不是下划线的个数代表数字，验证了一下结果是正确的。运算之后得到了一串数字，应该为key。
```
# 似乎不能直接u'_'会验证不出来，因此用dt[0]代替
ul = dt[0]
cnt = 0
ns = ''
for i in dt:
    if i is ul:
        cnt += 1
    else:
        if cnt != 0:
            ns += str(cnt)
            cnt = 0
            ns += i
        else:
            ns += i
# add
ns += str(cnt)
ns = ns.replace('//', '/')
print ns
key = eval(ns)
print key
# 5287002131074331513 key
```
第二步是难点，看marshal.loads()应该处理之后的是编译后的二进制流，查阅资料 http://www.cnblogs.com/rainduck/p/3524557.html找到反编译的方法，因此用uncompyle2是最好不过的了，反编译得出py文件。
```
import marshal, zlib, base64

bs = marshal.loads(zlib.decompress(base64.b64decode('eJxtVP9r21YQvyd/ieWm66Cd03QM1B8C3pggUuzYCSWstHSFQijyoJBhhGq9OXJl2ZFeqAMOK6Q/94f9Ofvn1s+d7Lgtk/3O997du/vc584a0eqpYP2GVfwDEeOrKCU6g2LRRyiK4oooFsVVUSqkqxTX6J1F+SfSNYrrdKPorC76luhbpOEGCZNFZw2KG3Rmk26QtuXi3xTb7ND6/aVu0g2RuvhEcZNut5lAGbTvAFbyH57TkYLKy8J6xpDvQxiiiaIlcdqJxVcHbXY6bXNlZgviPCrO0+StqfKd88gzNh/qRZyMdWHE29TZZvIkG7eZFRGGRcBmsXJaUoKCQ9fWKHwSqNeKFnsM5PnwJ7q2aKk4AFhcWtQCh+ChB5+Lu/RmyYUxmtOEYxas7i/2iuR7Ti14OEOSmU0RADd4+dQzbM1FJhukAUeQ+kZROuLyioagrau76kc1slY1NNaY/y3LAxDQBrAICJisV2hMdF2lxQcyFuMoqcX3+TCl6xotqzSpkqmxYVmjXVjAXiwBsEfBrd1VvTvLCj2EXRnhoryAKdpxcIgJcowUB68yAx/tlCAuPHqDuZo0CN3CUGHwkPhGMA7aXMfphjbmQLhLhJcHa0a+mpgB191c1U1lnHJQbgkHx+WGxeJbejnpkzSavo2jkxZ7i725npGAaTc8FXmUjbUETHUmkxXN5zqL5WiWxwE7Bc11yyYzNJpN02jerq+DzNNodfxOX8kE4FcmYKscDdYD1oPGGucXYNmgs1F+NTf3GOt3Mg7b+NTVruqoQyX1hOEUacKw+AGbP38ZOq9THRXaSbL5pXGQ8bho/Z/lrzQaHxdoCrlev+t6nZ7re57r+57rHXag93Deh37k+vuw9zorO/Qj/B50cAf2oyOsvut3D+ADWxdxfN/1Drqu39mHzvcRswv/Hvz7sHeg9w8Qzy99DzuFwxhPhs6zWTbOI3OZRiaZZcVj5wVwOklx7OwVxR47PR46r/SVM8ulBJic9zku/eqY/MqJxiDj+Gd55wS3f35pbLCzHoEwzKKpDkN5i+TR+1AYCWTo5IV0Z0P9H3phDDd6lMzPdS5bbo9eJGbTsW9nbDqLL1N9Iq+rRxDbll2x67a9Lf27hw5uK1s1rZr6DOPF+FI=')))

import uncompyle2
with open('f.py', 'w') as f:
    uncompyle2.uncompyle('2.7', bs, f)
```

看encrypt函数，加密方法如下：
```
def encrypt(plain, key):
    keySHA1 = sha1(key)
    intSHA1 = calc(keySHA1)
    r = []
    for i in range(len(plain)):
        r.append(ord(plain[i]) + int('0x%s' % keySHA1[i % 40], 16) - intSHA1)
        intSHA1 = calc(sha1(plain[:i + 1])[:20] + sha1(str(intSHA1))[:20])

    return ''.join(map(lambda x: str(x), r))
```

对key进行sha1加密为16进制串，再处理为10进制串保存到intSHA1；
对plain里面的每一位ascii编码与keySHA1的某位进行相加后减去intSHA1，放入r中；
intSHA1变化为plain前i位的sha1前二十位与intSHA1的SHA1前二十位相加的十进制值；
将r中的元素转化为字符串得到加密后的字符串，因此，该加密方法是前后字符关联的，第n位的加密都与前n-1位有关。
了解了加密方法后，接下来尝试用第一步爆出的key爆破，爆破代码如下：
```
...
if __name__ == '__main__'
    cipherText = '-185-147-211-221-164-217-188-169-205-174-211-225-191-234-148-199-198-253-175-157-222-135-240-229-201-154-178-187-244-183-212-222-164'

    key = '5287002131074331513'
    flag =''
    for i in range(len(cipherText)/4):
        for j in range(31, 128):   # 一般31-128才是常用字符
            if encrypt(flag+chr(j), key) == cipherText[0:i*4+4]:
                print j,
                flag += chr(j)
                break
    print flag
```

发现爆破出的都是无意义字符串，猜想是否key有问题，尝试将key转换为16进制、16进制转字符串发现有意义字符串I_4m-k3y
```
hk = hex(key)[2:]
print hk
kk = ''
for i in range(len(hk)/2):
    kk += chr(int('0x' + hk[i*2:i*2+2], 16))
print kk
```

将key代入爆破代码即可解出flag。