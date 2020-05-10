import email, getpass, imaplib, os
from progressbar import progressbar
import re
from email.policy import default
import pandas as pd
from tqdm import tqdm

FROM_EMAIL  = "ursol.toma" + ORG_EMAIL
FROM_PWD    = "WeWeWe11"




def create_connection(FROM_EMAIL,FROM_PWD):
    SMTP_SERVER = "imap.gmail.com"
    SMTP_PORT   = 993
    mail = imaplib.IMAP4_SSL(SMTP_SERVER)
    mail.login(FROM_EMAIL,FROM_PWD)
    return mail

def load_data():
    mail.select('inbox')
    type_, data = mail.search(None, 'ALL')
    mail_ids = data[0]
    
    id_list = mail_ids.split()   
    first_email_id = int(id_list[0])
    latest_email_id = int(id_list[-1])
    
    mail_list=[]
    df_mail=pd.DataFrame(columns=['id','source','subject'])
    ids=data[0].split()[-5000:-1]
    for num in progressbar(ids, redirect_stdout=True):
        typ, data_ = mail.fetch(num, '(RFC822)')
        msg_uid=data_[0][0]
        msg = email.message_from_bytes(data_[0][1],policy=default)
        mail_list.append(msg)
        df_mail=df_mail.append({'id':num,'from':msg['source'],'subject':msg['subject']},ignore_index=True)
        df_mail.to_csv('mail_list.csv',index=False)


def move_mail(df):
    for cluster in df.cluster.unique():
        results={}
        mail=create_connection(FROM_EMAIL,FROM_PWD,ORG_EMAIL,SMTP_SERVER)
        mailbox='label_{}'.format(str(cluster)[0])
        print(mailbox)
        results['create']=mail.create(mailbox)
        ids=df[df.cluster==cluster].id.apply(lambda x:bytes(str(int(x[2:-1])),'utf-8')).values
        mail.select('inbox')
        for i in progressbar(ids, redirect_stdout=True):
            mail.uid('COPY',i,mailbox)
            mail.uid('STORE', i , '+FLAGS', '(\Deleted)')
            mail.expunge()
        
#for part in msg.walk():
#    if part.get_content_maintype() == 'multipart':
#        continue
#    charset = part.get_content_charset()
#    if charset is not None:
#        print('=== charset {} ==='.format(charset))
#        print(part.get_content())

