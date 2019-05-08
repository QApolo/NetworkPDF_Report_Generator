from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer
authorizer = DummyAuthorizer()
authorizer.add_user("user", "12345", "/home/rublend", perm="elradfmw") #Modificar el nombre
authorizer.add_anonymous("/home/rublend", perm="elradfmw") #Modificar nombre de usuario.
handler = FTPHandler
handler.authorizer = authorizer
server = FTPServer(("localhost", 1026), handler)
server.serve_forever()
