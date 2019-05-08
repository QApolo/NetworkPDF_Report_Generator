# -*- coding: utf-8 -*-
"""
This describes an  IMAPClient
Changelog:
--Version 1 CrisCastro
    ---basic fetch email  method written
Todo: delete the email once is  readed
"""
import imaplib
import time


class IMAPclient(imaplib.IMAP4):
    """IMAP client  to send messages
    Note:
        This extends from imaplib.IMAP4
    :param host (str): the name of the remote host to which to connect.
    :param port (str): the port to which to connect
    """

    def __init__(self, host, port=143):
        super().__init__(host, port)

    def fetch_mail(self, criteria="ALL", delete=False):
        """
            :param criteria: a search criteria to lookup.
            :return: time of delivery in seconds it returns -1 if an error has raised
        """
        f_t = -1
        try:
            self.select('Inbox')
            if criteria == "LAST":
                s_t = time.time()
                rv, data = self.search(None, "ALL")
                num = data[0].split()[-1]
                body = self.fetch(num, "(UID BODY[TEXT])")[1][0][1]
                f_t = time.time() - s_t
                print(f"{num}\n{body}")
                print(f"Successfully fetch email ", f"{f_t*1000:.4}ms" if f_t // 1000 < 1 else f"{f_t:.4s}s", " taken")
                if delete:
                    print(f"deleting")
                    self.store(num, '+FLAGS', '\\Deleted')
                    self.expunge()
            else:
                s_t = time.time()
                rv, data = self.search(None, criteria)
                for num in data[0].split():
                    # subj = self.fetch(num, '(BODY[HEADER.FIELDS (SUBJECT)])')
                    body = self.fetch(num, "(UID BODY[TEXT])")[1][0][1]
                    f_t = time.time() - s_t
                    print(f"{num}\n{body}")
                    print(f"Successfully fetch email ", f"{f_t*1000:.4}ms" if f_t // 1000 < 1 else f"{f_t:.4s}s",
                          " taken")
        except imaplib.IMAP4.error as error:
            print(f"Error: unable to fetch email\nlog: {error}")
        return f_t
