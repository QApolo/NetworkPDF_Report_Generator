# -*- coding: utf-8 -*-
"""
This describes an  IMAPClient
Changelog:
--Version 1 CrisCastro
    ---basic fetch email  method written
Todo: delete the email once is  readed
"""
import imaplib
import pprint
import time

class IMAPclient(imaplib.IMAP4):
    """IMAP client  to send messages
    Note:
        This extends from imaplib.SMTP
    :param host (str): the name of the remote host to which to connect.
    :param port (str): the port to which to connect
    """
    def __init__(self, host, port=143):
        super().__init__(host, port)

    def fetch_mail(self, user, passw, criteria="ALL"):
        """
            :param user: The email address to lookup.
            :param passw: the password of the user email.
            :param criteria: a search criteria to lookup.
            :return: time of delivery in seconds it returns -1 if an error has raised
        """
        f_t = -1
        try:
            self.login(user, passw)
            self.select('Inbox')
            s_t = time.time()
            tmp, data = self.search(None, criteria)
            f_t = time.time() - s_t
            print(f"Successfully fetch email {f_t}s taken")
            for num in data[0].split():
                tmp, data = self.fetch(num, '(RFC822)')
                print('Message: {0}\n'.format(num))
                pprint.pprint(data[0][1])
                break
            self.close()
        except imaplib.IMAP4.error as error:
            print(f"Error: unable to fetch email\nlog: {error}")
        return f_t
