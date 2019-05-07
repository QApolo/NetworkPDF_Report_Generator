"""
this module tests over mailmonitor utils
"""
from Services.Mailmonitor.SMTP import SMTPclient
if __name__ == '__main__':
    server = SMTPclient("localhost")
    server.sendmail("elcris@losanciosos.com", "elkai@losanciosos.com","correo de pruevba python")
