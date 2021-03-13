#!/usr/local/bin/python3
from email.mime.text import MIMEText
import smtplib

USER_NAME_CONTACT = "contact@bluenosekai.com"
PASSWORD_CONTACT = "20210313"
RECIPIENT_CONTACT = "lamp-admin@bluenosekai.com"
HOST = "om1002.coreserver.jp"
PORT = 465

def contact_create(email, name, contents, *args):
  if not args:
    body1 = """
    {0}様
    当サイトをご覧頂きありがとうございます。
    お問い合わせを承りました。
    返答に多少のお時間を頂く事がございます。
    ご理解・ご協力をよろしくお願い致します。
    ※こちらは自動返信メールとなっております。ご返信はお控え下さい。

    (お問い合わせ内容)
    お名前:　{0}様
    メールアドレス:　{1}
    お問い合わせ内容:　{2}
    """.format(name, email, contents)

    body2 = """
    お名前:　{0}
    メールアドレス:　{1}
    お問い合わせ内容:　{2}
    """.format(name, email, contents)
  else:
    body1 = """
    {0}様
    当サイトをご覧頂きありがとうございます。
    当社での制作依頼申込みを承りました。
    返信に多少のお時間を頂く事がございます。
    ご理解・ご協力をよろしくお願い致します。
    ※こちらは自動返信メールとなっております。ご返信はお控え下さい。

    (受付内容)
    会社名/個人名:　{0}様
    メールアドレス:　{1}
    電話番号:　{2}
    ご依頼内容:　{3}
    想定予算: {4}
    ご希望納期: {5}
    目的・概要:　{6}
    """.format(name, email, args[0], args[1], args[2], args[3], contents)

    body2 = """
    会社名/個人名:　{}
    メールアドレス:　{}
    電話番号:　{}
    ご依頼内容:　{}
    想定予算: {}
    ご希望納期: {}
    目的・概要:　{}
    """.format(name, email, args[0], args[1], args[2], args[3], contents)

  msg1 = MIMEText(body1)
  msg1["Subject"] = "受付完了"
  msg1["From"] = USER_NAME_CONTACT
  msg1["To"] = email

  msg2 = MIMEText(body2)
  msg2["Subject"] = "お問い合わせの受付"
  msg2["From"] = USER_NAME_CONTACT
  msg2["To"] = RECIPIENT_CONTACT
  
  host = HOST
  port = PORT

  smtp = smtplib.SMTP_SSL(host, port)
  smtp.login(USER_NAME_CONTACT, PASSWORD_CONTACT)
  smtp.send_message(msg1)
  smtp.send_message(msg2)
  smtp.quit()