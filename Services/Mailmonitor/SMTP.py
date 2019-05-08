# -*- coding: utf-8 -*-
"""
This describes an  SMTPclient
Changelog:
--Version 1 CrisCastro
    ---basic sendmail method written
Todo:
"""
import smtplib
import time

class SMTPclient(smtplib.SMTP):
    """SMTP client  to send messages
    Note:
        This extends from smtplib.SMTP
    :param host (str): the name of the remote host to which to connect.
    :param port (str): the port to which to connect
    """
    def __init__(self, host, port=''):
        super().__init__(host, port)

    def sendmail(self, sender, receivers, message,event=None,verbose=True):
        """
        :param sender: The address sending this mail.
        :param receivers: A list of addresses to send this mail to.
        :param message: the message to send.
        :return: time of delivery in seconds it returns -1 if an error has raised
        """
        f_t = -1
        try:
            s_t = time.time()
            super().sendmail(sender, receivers, message)
            f_t = time.time() - s_t
            if verbose:
                print(f"Successfully sent email {f_t}s taken")
        except smtplib.SMTPException as error:
            print(f"Error: unable to send email\nlog: {error}")
        if event:
            event.set()
        return f_t
