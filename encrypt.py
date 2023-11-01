import os


def encrypt(key_decrypt, MyKey_encrypt):
    key_encrypt = ""
    for i, j in zip(key_decrypt, MyKey_encrypt):
        key_encrypt = key_encrypt + str(ord(i) + ord(j)) + " "
    return key_encrypt


with open('config.txt','r')as f:
    f_content = eval(f.readlines()[0])
    encrypted = f_content['encrypted']

if not encrypted:
    print("Not encrypted yet !")
    SUPER_TOKEN = input("SUPER_TOKEN : ")
    print("Start encrypting...")
    with open('config.txt','w')as f:
        f_content['account'] = encrypt(f_content['account'],SUPER_TOKEN)
        f_content['password'] = encrypt(f_content['password'], SUPER_TOKEN)
        f_content['pop3_server'] = encrypt(f_content['pop3_server'], SUPER_TOKEN)
        f_content['receiver'] = encrypt(f_content['receiver'], SUPER_TOKEN)
        f_content['encrypted'] = 1
        f.write(str(f_content))
        print("End encrypting...")
else:
    print("Already encrypted!!!")

input("PRESS ANY KEY TO EXIT")

