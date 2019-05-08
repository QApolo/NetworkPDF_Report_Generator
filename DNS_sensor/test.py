
import dns
import dns.resolver
#Definimos los tipos de registro
dns_reg=("A","AAAA","MX","CNAME","NS","PTR","SOA","ANY")

domain = input("Ingrese el nombre de dominio para buscar:> ")

for i in dns_reg:
    print("###################")
    print("###%s###" % i)
    print("###################")
    try:
        #Hacemos la consultar al DNS
        res = dns.resolver.query(domain,i)
        #Ponemos la respuesta en formato texto
        print(res.response.to_text())
    except:
        pass