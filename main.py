import poplib
import smtplib
import time
from email.parser import Parser
from email.header import decode_header
from email.utils import parseaddr
from email.mime.text import MIMEText
from email.header import Header
import os
import sys

global last_len

def encrypt(key_decrypt, MyKey_encrypt):
    key_encrypt = ""
    for i, j in zip(key_decrypt, MyKey_encrypt):
        key_encrypt = key_encrypt + str(ord(i) + ord(j)) + " "
    return key_encrypt


def decrypt(key_encrypt, MyKey_decrypt):
    key_decrypt = ""
    for i, j in zip(key_encrypt.split(" ")[:-1], MyKey_decrypt):
        key_decrypt = key_decrypt + chr(int(i) - ord(j))
    return key_decrypt


def parser_address(msg):
    hdr, addr = parseaddr(msg['From'])
    name, charset = decode_header(hdr)[0]
    if charset:
        name = name.decode(charset)
    return format(name) + '\n\n' + format(addr) + '\n\n' + 'Check your mailbox'


def parser_subject(msg):
    subject = msg['Subject']
    value, charset = decode_header(subject)[0]
    if charset:
        value = value.decode(charset)
    return format(value)


def mail_deliver(user, Subject_main, Content_main):
    message = MIMEText(Content_main, 'plain', 'utf-8')
    message['From'] = Header(user.account)
    message['To'] = Header(user.receiver, 'utf-8')
    message['Subject'] = Header(Subject_main, 'utf-8')
    try:
        smtpObj = smtplib.SMTP(user.pop3_server)
        smtpObj.connect(user.pop3_server, 25)  # 25 为 SMTP 端口号
        smtpObj.login(user.account, user.password)
        smtpObj.sendmail(user.account, user.receiver, message.as_string())
        smtpObj.quit()
        print("Deliver successfully!\nCheck your mailbox.")

        return True
    except smtplib.SMTPException:
        print("Deliver failed!\nCheck the code.")
        return False


def get_msg(user, last_len):
    server = poplib.POP3(user.pop3_server)
    # server.set_debuglevel(1)
    # print(server.getwelcome().decode('GBK'))
    server.user(user.account)
    server.pass_(user.password)

    email_num, email_size = server.stat()
    # print("Total number of emails: {0}, Total scale of emails: {1}".format(email_num, email_size))

    # 使用list()返回所有邮件的编号，默认为字节类型的串
    rsp, msg_list, rsp_siz = server.list()
    # print("服务器的响应: {0},\n消息列表： {1},\n返回消息的大小： {2}".format(rsp, msg_list, rsp_siz))

    print('The number of messages at this access: {}'.format(len(msg_list)))

    if last_len < len(msg_list):
        total_mail_numbers = len(msg_list)

        rsp, msglines, msgsiz = server.retr(total_mail_numbers)
        # print("服务器的响应: {0},\n原始邮件内容： {1},\n该封邮件所占字节大小： {2}".format(rsp, msglines, msgsiz))

        msg_content = b'\r\n'.join(msglines).decode('gb18030', 'ignore')
        msg = Parser().parsestr(text=msg_content)
        server.close()
        return msg, len(msg_list)

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

def get_config():
    with open("config.txt", 'r', encoding='utf-8') as f:
        f_content = eval(f.readlines()[0])
        encrypted = f_content['encrypted']

    if encrypted:
        account = decrypt(f_content['account'], MyKey_decrypt)
        password = decrypt(f_content['password'], MyKey_decrypt)
        pop3_server = decrypt(f_content['pop3_server'], MyKey_decrypt)
        receiver = decrypt(f_content['receiver'], MyKey_decrypt)
    else:
        account = f_content['account']
        password = f_content['password']
        pop3_server = f_content['pop3_server']
        receiver = f_content['receiver']
    print("Original SJTU email address:" + account)
    print("SJTU email server address:" + pop3_server)
    print("Transfer to:" + receiver)

    NEW_user = user(account=account, password=password, pop3_server=pop3_server, receiver=receiver)
    return NEW_user, encrypted


try:
    SUPER_TOKEN = os.environ['SUPER_TOKEN']
except KeyError:
    print('Please define the environment variable SUPER_TOKEN')
    sys.exit(1)

MyKey_decrypt = SUPER_TOKEN
MyKey_encrypt = SUPER_TOKEN

print("* " * 11)
print("*   Start running!  *")
print("* " * 11)

NEW_user, encrypted = get_config()

try:
    with open("info.txt", 'r', encoding='utf-8') as f:
        info_content = f.readlines()
        print("Checking the info.txt...")
        if info_content:
            info_lines = len(f.readlines())
            last_len = int(info_content[info_lines - 1][29:])
            print("Complete checking of info.txt!")
        else:  # 初始化info.txt
            _msg, last_len = get_msg(NEW_user, 0)
            with open("info.txt", 'w', encoding='utf-8') as f:
                NowTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                f.write(NowTime + ' last_len:' + str(last_len) + '\n')
            print("Complete initialization of info.txt!")
            quit()
except:
    _msg, last_len = get_msg(NEW_user, 0)
    with open("info.txt", 'w', encoding='utf-8') as f:
        NowTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        f.write(NowTime + ' last_len:' + str(last_len) + '\n')
    print("Complete initialization of info.txt!")
    quit()

print("The number of messages at last access: " + str(last_len))
msg, this_len = get_msg(NEW_user, last_len)
with open("info.txt", 'a', encoding='utf-8') as f:
    NowTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    f.write(NowTime + ' last_len:' + str(this_len) + '\n')

if not msg:
    print("Nothing happened.\nNo mail is delivered.")
else:
    # with open("message.txt", 'w')as f:
    # f.write(format(msg))
    print("Start delivering the mail...")
    mail_deliver(NEW_user, parser_subject(msg), parser_address(msg))

if not encrypted:
    f_content = {'account': encrypt(NEW_user.account, MyKey_encrypt),
                 'password': encrypt(NEW_user.password, MyKey_encrypt),
                 'pop3_server': encrypt(NEW_user.pop3_server, MyKey_encrypt),
                 'receiver': encrypt(NEW_user.receiver, MyKey_encrypt),
                 'encrypted': 1}
    with open('config.txt', 'w', encoding='utf-8') as f:
        f.write(str(f_content))

print("* " * 11)
print("*    End running!   *")
print("* " * 11)
for i in range(0, 10):
    print("This windows will close after " + str(10 - i) + " seconds.")
    time.sleep(1)
