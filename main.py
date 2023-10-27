import poplib
import time
from email.parser import Parser
from email.header import decode_header
import smtplib
from email.mime.text import MIMEText
from email.header import Header

MyKey = "897vsU*(^(&TGSDF&(ASU_HANDS(AHNSFIOAJSF)A*)_WQJMJAPSOSad987syhy)(&^&%*d"


def encrypt(key_decrypt):
    key_encrypt = ""
    for i, j in zip(key_decrypt, MyKey):
        key_encrypt = key_encrypt + str(ord(i) + ord(j)) + " "
    return key_encrypt


def decrypt(key_encrypt):
    key_dencrypt = ""
    for i, j in zip(key_encrypt.split(" ")[:-1], MyKey):
        key_dencrypt = key_dencrypt + chr(int(i) - ord(j))
    return key_dencrypt


def mail_deliver(user, Subject_main):
    Content_main = ""
    message = MIMEText(Content_main, 'plain', 'utf-8')
    message['From'] = Header(user.account)
    message['To'] = Header(user.receiver, 'utf-8')
    message['Subject'] = Header(Subject_main, 'utf-8')
    try:
        smtpObj = smtplib.SMTP()
        smtpObj.connect(user.pop3_server, 25)  # 25 为 SMTP 端口号
        smtpObj.login(user.account, user.password)
        smtpObj.sendmail(user.account, user.receiver, message.as_string())
        print("Deliver successfully!\nCheck your mailbox.")
        return True
    except smtplib.SMTPException:
        print("Nothing happened.\nNo mail is delivered.")
        return False


def get_mail_content(user, last_len):
    # 开始连接到服务器
    server = poplib.POP3(user.pop3_server)

    # 打开或者关闭调试信息，为打开，会在控制台打印客户端与服务器的交互信息
    # server.set_debuglevel(1)

    # 打印POP3服务器的欢迎文字，验证是否正确连接到了邮件服务器
    # print(server.getwelcome().decode('GBK'))

    # 开始进行身份验证
    server.user(user.account)
    server.pass_(user.password)

    # 返回邮件总数目和占用服务器的空间大小（字节数）， 通过stat()方法即可
    email_num, email_size = server.stat()
    # print("Total number of emails: {0}, Total scale of emails: {1}".format(email_num, email_size))

    # 使用list()返回所有邮件的编号，默认为字节类型的串
    rsp, msg_list, rsp_siz = server.list()
    # print("服务器的响应: {0},\n消息列表： {1},\n返回消息的大小： {2}".format(rsp, msg_list, rsp_siz))

    print('The number of messages at this access: {}'.format(len(msg_list)))

    if last_len < len(msg_list):
        # 下面单纯获取最新的一封邮件
        total_mail_numbers = len(msg_list)

        rsp, msglines, msgsiz = server.retr(total_mail_numbers)
        # print("服务器的响应: {0},\n原始邮件内容： {1},\n该封邮件所占字节大小： {2}".format(rsp, msglines, msgsiz))

        msg_content = b'\r\n'.join(msglines).decode('gb18030','ignore')
        msg = Parser().parsestr(text=msg_content)
        # print('解码后的邮件信息:\n{}'.format(msg))

        # 关闭与服务器的连接，释放资源
        server.close()

        # return msg
        return format(msg), len(msg_list)

    else:
        server.close()
        return "", len(msg_list)


class user:
    account = ''
    password = ''
    pop3_server = ''
    receiver = ''

    def __init__(self, account, password, pop3_server, receiver):
        self.account = account
        self.password = password
        self.pop3_server = pop3_server
        self.receiver = receiver


def get_user_info():
    with open("config.txt", 'r', encoding='utf-8') as f:
        f_content = f.readlines()
        encrypted_or_not = int(f_content[4][0])

    if encrypted_or_not:
        with open("config.txt", 'r', encoding='utf-8') as f:
            f_content = f.readlines()
        temp = ""
        for line in f_content:
            temp = temp + decrypt(line)
        with open("config.txt", 'w', encoding='utf-8') as f:
            f.write(temp)

    with open("config.txt", 'r', encoding='utf-8') as f:
        f_content = f.readlines()
    print("Original SJTU email address: " + f_content[0][8:-1])
    print("SJTU email server address: " + f_content[2][5:-1])
    print("Transfer to: " + f_content[3][9:-1])
    account = f_content[0][8:-1]
    password = f_content[1][9:-1]
    pop3_server = f_content[2][5:-1]
    receiver = f_content[3][9:-1]

    NEW_USER = user(account=account, password=password, pop3_server=pop3_server, receiver=receiver)
    return NEW_USER, encrypted_or_not


print("* " * 11)
print("*   Start running!  *")
print("* " * 11)
NEW_USER, encrypted = get_user_info()
try:
    with open("info.txt", 'r', encoding='utf-8') as f:
        info_content = f.readlines()
        print("Checking the info.txt...")
        if info_content:
            info_lines = len(f.readlines())
            last_len = int(info_content[info_lines - 1][29:])
            print("Complete checking of info.txt!")
        else:  # 初始化info.txt
            _msg, last_len = get_mail_content(NEW_USER, 0)
            with open("info.txt", 'w', encoding='utf-8') as f:
                NowTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                f.write(NowTime + ' last_len:' + str(last_len) + '\n')
            print("Complete initialization of info.txt!")
            quit()
except:
    with open("info.txt", 'w', encoding='utf-8') as f:
        pass
    _msg, last_len = get_mail_content(NEW_USER, 0)
    with open("info.txt", 'w', encoding='utf-8') as f:
        NowTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        f.write(NowTime + ' last_len:' + str(last_len) + '\n')
    print("Complete initialization of info.txt!")
    quit()


print("The number of messages at last access: " + str(last_len))
msg, this_len = get_mail_content(NEW_USER, last_len)

with open("info.txt", 'a', encoding='utf-8') as f:
    NowTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    f.write(NowTime + ' last_len:' + str(this_len) + '\n')

if not msg:
    pass
else:
    with open("message.txt", 'w')as f:
        f.write(msg)
    receive_begin, receive_end = msg.find("<"), msg.find(">")
    Subject_begin = msg.find("Subject: ")

    if msg.find("MIME") + 1:
        Subject_end = msg.find("MIME") - 1
        if msg.find("Mime") + 1:
            Subject_end = min(msg.find("MIME"), msg.find("Mime"))
    else:
        Subject_end = msg.find("Mime")

    receive_main = msg[receive_begin + len("<"): receive_end]
    Subject_main = msg[Subject_begin + len("Subject: "):Subject_end]

    if "?gb18030?B?" in Subject_main or "?GB2312" in Subject_main:
        # print(decode_header(Subject_main)[0][0])
        Subject_main = decode_header(Subject_main)[0][0].decode("GBK")

    print(receive_main)
    print(Subject_main)
    print("Start delivering the email...")
    mail_deliver(NEW_USER, Subject_main)

with open("config.txt", 'r', encoding='utf-8') as f:
    f_content = f.readlines()
temp = ""
for line in f_content:
    temp = temp + encrypt(line) + '\n'
with open("config.txt", 'w', encoding='utf-8') as f:
    f.write(temp)

print("* " * 11)
print("*    End running!   *")
print("* " * 11)
for i in range(0, 10):
    print("This windows will close after " + str(10 - i) + " seconds.")
    time.sleep(1)
