"""
this module tests over mailmonitor utils
"""
from Services.Mailmonitor.SMTP import SMTPclient
if __name__ == '__main__':
    server = SMTPclient("198.168.0.15")
    server.sendmail("elcris@losanciosos.com", "elkai@losanciosos.com","correo de pruevba python")
