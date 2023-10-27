def decrypt(key_encrypt, MyKey):
    key_dencrypt = ""
    for i, j in zip(key_encrypt.split(" ")[:-1], MyKey):
        # i 为加密字符，j为秘钥字符
        temp = chr(int(i) - ord(j))  # 解密字符 = (加密Unicode码字符 - 秘钥字符的Unicode码)的单字节字符
        key_dencrypt = key_dencrypt + temp
    return key_dencrypt


MyKey = "897vsU*(^(&TGSDF&(ASU_HANDS(AHNSFIOAJSF)A*)_WQJMJAPSOSad987syhy)(&^&%*d"

temp = ""
with open("config.txt", 'r') as f:
    f_content = f.readlines()
    
for line in f_content:
    temp = temp + decrypt(line, MyKey)

with open("config.txt", 'w') as f:
    f.write(temp)


