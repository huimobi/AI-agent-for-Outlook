import imaplib
from dotenv import load_dotenv
import email
from email.header import decode_header
import os
from bs4 import BeautifulSoup

#First create a .env file with EMAIL and PASSWORD variables

#reads email and password from .env file
load_dotenv()
EMAIL=os.getenv("EMAIL")
PASSWORD=os.getenv("PASSWORD")

#set gmail server
IMAP_SERVER = "imap.gmail.com"


def text_extract(html):
    """
    Only extracts the text of the body in a html code
    """
    soup = BeautifulSoup(html, 'html.parser')
    
    # extract text
    clean_text = soup.get_text(separator='\n').strip()
    return clean_text

def read_emails():
    #login to gmail
    mail = imaplib.IMAP4_SSL(IMAP_SERVER)
    mail.login(EMAIL, PASSWORD)
    print("Login successful!\n")


    #selects inbox
    mail.select("inbox")
    
    #search for unseen emails
    status, messages = mail.search(None, 'UNSEEN')

    #get email ids list
    email_ids = messages[0].split()
    print(f"You have {len(email_ids)} unseen e-mails.\n")

    for email_id in email_ids:

        #search for the email from the id
        status, msg_data = mail.fetch(email_id, '(RFC822)')
        for response_part in msg_data:
            if isinstance(response_part, tuple):
                #decode email
                msg = email.message_from_bytes(response_part[1])

                #get subject
                subject, encoding = decode_header(msg["Subject"])[0]
                if isinstance(subject, bytes):
                    #decode bytes to str
                    subject = subject.decode(encoding or "utf-8",errors='ignore')
                print(f"Subject: {subject}\n")

                #gets who sent the email
                from_ = msg.get("From")
                print(f"From: {from_}\n")

                #checks if the email is multipart
                if msg.is_multipart():
                    for part in msg.walk():
                        if part.get_content_type() == "text/plain":
                            body = part.get_payload(decode=True).decode(errors='ignore')
                            body=text_extract(body)
                            print(f"Message:\n\n{body}\n\n")
                            break
                else:
                    body = msg.get_payload(decode=True).decode(errors='ignore')
                    body=text_extract(body)
                    print(f"Message:\n\n{body}\n\n")
    
    print("Thats all for today.\nBye!!")
    #disconnect from server
    mail.logout()

#call for email reading function
read_emails()
