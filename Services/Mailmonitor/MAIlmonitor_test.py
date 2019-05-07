"""
this module tests over mailmonitor utils
"""
import sys, getopt

from Services.Mailmonitor.IMAP import IMAPclient
from Services.Mailmonitor.SMTP import SMTPclient


def test_send(sender, receiver, message):
    server = SMTPclient("localhost")
    server.sendmail(sender, receiver, message)
    server.close()

def test_receive(user,passw):
    server = IMAPclient("localhost")
    server.fetch_mail(user, passw)

def main(argv):
    inputfile = ''
    outputfile = ''
    try:
        opts, args = getopt.getopt(argv, "hsrm:")
    except getopt.GetoptError:
        print('usage MAILmonitor_test.py -option <args>*', "-s <")
        sys.exit(2)
    for opt, arg in opts:
        print(f"opt {opt} arg {arg}")
        if opt == '-h':
            print('usage MAILmonitor_test.py -option <args>*')
            sys.exit()
        elif opt in ("-s", "--ifile"):
            test_send(args[0], args[1], args[2])
        elif opt in ("-r", "--ofile"):
            test_receive(args[0], args[1])
            pass
        elif opt in ("-m", "--ofile"):
            outputfile = arg


if __name__ == '__main__':
    # server = SMTPclient("localhost")
    # server.sendmail("elcris@losanciosos.com", "elkai@losanciosos.com","correo de pruevba python")
    main(sys.argv[1:])
