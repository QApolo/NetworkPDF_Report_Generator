"""
this module tests over mailmonitor utils
"""
import getopt
import json
import sys
import threading

import matplotlib.pyplot as plt
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
    plt.plot(stmptimes, label='SMTP time')  # plotting by columns
    plt.plot(imaptimes, label='IMAP time')
    plt.title("Mail Service Times")
    plt.xlabel('Time in s')
    plt.ylabel('Number of iteration')
    plt.legend(loc='upper right')
    plt.savefig(f'{name}.png')


def main(argv):
    inputfile = ''
    outputfile = ''
    try:
        opts, args = getopt.getopt(argv, "hsrm:")
    except getopt.GetoptError:
        print('usage MAILmonitor_test.py -option <args>*', "-s <")
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('usage MAILmonitor_test.py -option <args>*')
            print('usage MAILmonitor_test.py -r <user> <password> <criteria>')
            print('usage MAILmonitor_test.py -s <sender> <receiver> <message>')
            print('usage MAILmonitor_test.py -m <numberOftestEmails> <sender> <receiver> <receiverpass> ')
            print('usage MAILmonitor_test.py -p <datafile.json> <outputfile>')
            sys.exit()
        elif opt in ("-s", "--send"):
            test_send(args[0], args[1], args[2])
        elif opt in ("-r", "--receive"):
            test_receive(args[0], args[1], "ALL" if len(args) == 2 else args[2])
        elif opt in ("-p", "---plot"):
            with open(args[0], 'r') as fp:
                dict = json.load(fp)
                plot(dict["smtp_times"], dict["imap_times"], args[1])
                print(f"Plot has been saved as {args[1]}.png")
        elif opt in ("-m", "--monitor"):
            with open('mydict.json', 'w') as fp:
                json.dump(monitor_service(int(arg), args[0], args[1], args[2]), fp)


if __name__ == '__main__':
    # server = SMTPclient("localhost")
    # server.sendmail("elcris@losanciosos.com", "elkai@losanciosos.com","correo de pruevba python")
    main(sys.argv[1:])
