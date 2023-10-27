import time
from email.header import decode_header

Subject_main = "=?gb18030?B?suLK1NPDwP0gVGVzdCDV4srH0ru49rLiytQhQCMk?=" \
               "=?gb18030?B?JV4mKigpLT0=?="

Content_main = \
    "=?gb18030?B?suLK1NPDwP0gVGVzdCDV4srH0ru49rLiytQhQCMkJV4mYW1wOyooKS09DQqy4srU08PA/SBU?=" \
    "=?gb18030?B?ZXN0INXiysfSu7j2suLK1CFAIyQlXiZhbXA7KigpLT0NCrLiytTTw8D9IFRlc3Qg1eLKx9K7?=" \
    "=?gb18030?B?uPay4srUIUAjJCVeJmFtcDsqKCktPQ0KsuLK1NPDwP0gVGVzdCDV4srH0ru49rLiytQhQCMk?=" \
    "=?gb18030?B?JV4mYW1wOyooKS09DQqy4srU08PA/SBUZXN0INXiysfSu7j2suLK1CFAIyQlXiZhbXA7Kigp?="

print("* " * 10)
print(decode_header(Subject_main)[0][0])
print("* " * 10)
Subject_main = decode_header(Subject_main)[0][0].decode("GBK")
print(decode_header(Subject_main)[0][0])

print("* " * 10)
print(decode_header(Content_main)[0][0])
print("* " * 10)
Content_main = decode_header(Content_main)[0][0].decode("GBK")
print(decode_header(Content_main)[0][0])

print("")

MyKey = "897vsU*(^(&TGSDF&(ASU_HANDS(AHNSFIOAJSF)A*)_WQJMJAPSOSad987syhy)(&^&%*d"

def encrypt(key_origin, MyKey):
    key_encrypt = ""
    for i, j in zip(key_origin, MyKey):
        temp = str(ord(i) + ord(j)) + " "  # 加密字符 = 字符的Unicode码 + 秘钥的Unicode码
        key_encrypt = key_encrypt + temp
    return key_encrypt


# 解密
def decrypt(key_encrypt, MyKey):
    key_dencrypt = ""
    for i, j in zip(key_encrypt.split(" ")[:-1], MyKey):
        # i 为加密字符，j为秘钥字符
        temp = chr(int(i) - ord(j))  # 解密字符 = (加密Unicode码字符 - 秘钥字符的Unicode码)的单字节字符
        key_dencrypt = key_dencrypt + temp
    return key_dencrypt


data = "zmister.com"
print("原始数据为：", data)
enc_str = encrypt(data,MyKey)
print("加密数据为：", enc_str)
dec_str = decrypt(enc_str,MyKey)
print("解密数据为：", dec_str)

NowTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

print(len("2023-10-25 17:49:14 last_len:"))

with open("info.txt", 'a')as f:
    f.write(NowTime + ' last_len:\n')

with open("info.txt", 'r') as f:
    f_content = f.readlines()
    f_lines = len(f.readlines())
    last_len = int(f_content[f_lines-1][29:].strip('\n'))

if not last_len:
    last_len = 0
print(last_len)



from email.header import decode_header

msg = ""
with open("message.txt", 'r') as f:
    for line in f.readlines():
        msg = msg + str(line)
receive_begin, receive_end = msg.find("<"), msg.find(">")
Subject_begin = msg.find("Subject: ")


if msg.find("MIME") + 1:
    Subject_end = msg.find("MIME") - 1
    if msg.find("Mime") + 1:
        Subject_end = min(msg.find("MIME"),msg.find("Mime"))
else:
    Subject_end = msg.find("Mime")

receive_main = msg[receive_begin + len("<"): receive_end]
Subject_main = msg[Subject_begin + len("Subject: "):Subject_end]

if "?gb18030?B?" in Subject_main or "?GB2312" in Subject_main:
    # print(decode_header(Subject_main)[0][0])
    Subject_main = decode_header(Subject_main)[0][0].decode("GBK")

print("receive_main:", receive_main)
print("Subject_main:", Subject_main)
print("Start delivering the email...")

print(msg.find("Mime"))
print(msg.find("MIME"))