"""
this module tests over mailmonitor utils
"""
import sys, getopt
import threading

from Services.Mailmonitor.IMAP import IMAPclient
from Services.Mailmonitor.SMTP import SMTPclient


def test_send(sender, receiver, message):
    server = SMTPclient("localhost")
    server.sendmail(sender, receiver, message)
    server.close()


def test_receive(user, passw, criteria):
    server = IMAPclient("localhost")
    server.login(user, passw)
    server.fetch_mail( criteria)
    server.close()


def monitor_service(number_of_messages, sender, receiver, receiverpass, host):
    print(f"{number_of_messages} {sender} {receiver} {receiverpass} {host}")
    smtp_server = SMTPclient("localhost")
    imap_server = IMAPclient("localhost")
    imap_server.login(receiver, receiverpass)
    times_smtp = {}
    times_imap = {}
    message_available = threading.Event()
    for i in range(number_of_messages):
        times_smtp[i] = smtp_server.sendmail(sender, receiver, "test", message_available)
        message_available.wait()
        times_imap[i] = imap_server.fetch_mail("UNSEEN")
    smtp_server.close()
    imap_server.close()
    return times_smtp, times_imap


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
            print('usage MAILmonitor_test.py -m <numberOftestEmails> <sender> <receiver> <receiverpass> <host>')
            sys.exit()
        elif opt in ("-s", "--ifile"):
            test_send(args[0], args[1], args[2])
        elif opt in ("-r", "--ofile"):
            test_receive(args[0], args[1], "ALL" if len(args) == 2 else args[2])
        elif opt in ("-m", "--ofile"):
            print("times:\n",monitor_service(int(arg), args[0], args[1], args[2], args[3]))


if __name__ == '__main__':
    # server = SMTPclient("localhost")
    # server.sendmail("elcris@losanciosos.com", "elkai@losanciosos.com","correo de pruevba python")
    main(sys.argv[1:])
