# -*- coding: utf-8 -*-
"""
This module tests over mailmonitor utils
Changelog:
--Version 4 CrisCastro
    ---implemented plot functionality
--Version 3 CrisCastro
    ---generate N mail samples and monitoring their delivery times
--Version 2 CrisCastro
    ---receive mail test
--Version 1 CrisCastro
    ---send mail test

USAGE:
     MAILmonitor_test.py -option <args>*
Check Mail:
    MAILmonitor_test.py -r <user> <password> <criteria>
Send Mail:
    MAILmonitor_test.py -s <sender> <receiver> <message>
Generate N number of samples and monitor their delivery times:
    MAILmonitor_test.py -m <numberOftestEmails> <sender> <receiver> <receiverpass> <logfile>
Plot delivery times stored in a json file
    MAILmonitor_test.py -p <datafile.json> <outputfile>
Todo:
"""
import getopt
import json
import sys
import threading
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from numpy import sum

from tqdm import tqdm

from Services.Mailmonitor.IMAP import IMAPclient
from Services.Mailmonitor.SMTP import SMTPclient


def test_send(sender, receiver, message):
    server = SMTPclient("localhost")
    server.sendmail(sender, receiver, message)
    server.close()


def test_receive(user, passw, criteria):
    server = IMAPclient("localhost")
    server.login(user, passw)
    server.fetch_mail(criteria)
    server.close()


def monitor_service(number_of_messages, sender, receiver, receiverpass, criteria="LAST"):
    print(f"Generating  {number_of_messages} samples.")
    times_smtp = []
    times_imap = []
    smtp_server = SMTPclient("localhost")
    imap_server = IMAPclient("localhost")
    imap_server.login(receiver, receiverpass)
    message_available = threading.Event()
    for i in tqdm(range(number_of_messages)):
        times_smtp.append(smtp_server.sendmail(sender, receiver, "test", message_available, verbose=False))
        message_available.wait()
        times_imap.append(imap_server.fetch_mail(criteria, delete=True))
    smtp_server.close()
    imap_server.close()
    return {"smtp_times": times_smtp, "imap_times": times_imap}


def plot(stmptimes, imaptimes, name):
    total_time = sum([stmptimes, imaptimes], axis=0)
    plt.plot(stmptimes, label='SMTP time')  # plotting by columns
    plt.plot(imaptimes, label='IMAP time')
    plt.plot(total_time, label='Total Mail time')
    plt.title("Mail Service Times")
    plt.xlabel('Number of iteration')
    plt.ylabel('Time in s')
    plt.legend(loc='upper right')
    plt.savefig(f'{name}.png')

def main(argv):
    inputfile = ''
    outputfile = ''
    try:
        opts, args = getopt.getopt(argv, "phsrm:")
    except getopt.GetoptError:
        print('usage MAILmonitor_test.py -option <args>*', "-s <")
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print("USAGE:"
                  "\n- MAILmonitor_test.py -option <args>*"
                  "\n\nCheck Mail:"
                  "\n\n- MAILmonitor_test.py -r <user> <password> <criteria>"
                  "\n\nSend Mail:"
                  "\n- MAILmonitor_test.py -s <sender> <receiver> <message>"
                  "\n\nGenerate N number of samples and monitor their delivery times:"
                  "\n- MAILmonitor_test.py -m <numberOftestEmails> <sender> <receiver> <receiverpass> <logfile>"
                  "\n\nPlot delivery times stored in a json file"
                  "\n- MAILmonitor_test.py -p <datafile.json> <outputfile>")
            sys.exit()
        elif opt in ("-s", "--send"):
            test_send(args[0], args[1], args[2])
        elif opt in ("-r", "--receive"):
            test_receive(args[0], args[1], "ALL" if len(args) == 2 else args[2])
        elif opt in ("-p", "---plot"):
            with open(f"{args[0]}.json", 'r') as fp:
                dict = json.load(fp)
                plot(dict["smtp_times"], dict["imap_times"], args[1])
                print(f"Plot has been saved as {args[1]}.png")
        elif opt in ("-m", "--monitor"):
            with open(args[3], 'w') as fp:
                json.dump(monitor_service(int(arg), args[0], args[1], args[2]), fp)


if __name__ == '__main__':
    # server = SMTPclient("localhost")
    # server.sendmail("elcris@losanciosos.com", "elkai@losanciosos.com","correo de pruevba python")
    main(sys.argv[1:])
