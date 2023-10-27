def encrypt(key_origin, MyKey):
    key_encrypt = ""
    for i, j in zip(key_origin, MyKey):
        temp = str(ord(i) + ord(j)) + " "  # 加密字符 = 字符的Unicode码 + 秘钥的Unicode码
        key_encrypt = key_encrypt + temp
    return key_encrypt


MyKey = "897vsU*(^(&TGSDF&(ASU_HANDS(AHNSFIOAJSF)A*)_WQJMJAPSOSad987syhy)(&^&%*d"

with open("config.txt", 'r') as f:
    f_content = f.readlines()

temp = ""
for line in f_content:
    temp = temp + encrypt(line, MyKey) + '\n'

with open("config.txt", 'w') as f:
    f.write(temp)


with open("config.txt", 'r') as f:
    f_content = f.readlines()
    print("加密：\n",f_content)

