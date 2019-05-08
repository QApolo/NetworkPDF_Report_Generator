import time
import subprocess
import json
import dns.name as DNS
import dns.resolver as SOLVER
import dns.reversename as REVERSE

address_domain = ""

def ping(host):
  ret = subprocess.call(['ping', '-c', '3', '-W', '5', host],
    stdout=open('/dev/null', 'w'),
    stderr=open('/dev/null', 'w'))
  return ret == 0

def net_is_up(host):
  print ("[%s] Checking if network is up..." % time.strftime("%Y-%m-%d %H:%M:%S"))
  start = time.time()       # Start time to verify DNS
  xstatus = 1

  if ping(host):
      print ("[%s] Network is up!" % time.strftime("%Y-%m-%d %H:%M:%S"))
      xstatus = 0

  if xstatus:
      print ("[%s] Network is down :(" % time.strftime("%Y-%m-%d %H:%M:%S"))

  return xstatus

def main_process(host = "google.com"):
    # DNS UP   = 0      # DNS DOWN = 1
    start = time.time()
    state = "Down" if net_is_up(host) else "Up"
    response_time = time.time() - start

    return {    "state" : state,
                "server_response_time" : response_time
            }

def menu():
    print("|===\tQueryTypes: A(IPv4), AAAA(IPv6), MX(MailServers), NS(NameServers)\n")

def dnsQuery(domain, lookuptype):
    try:
        answer = SOLVER.query(domain,lookuptype)
        for ans in answer:
            address_domain = ans.address
            if lookuptype == 'A' or lookuptype=='a':
                print('\tDomain: {}\n\tDNS Lookuptype: {}\n\tAnswer: {}'.format(domain,lookuptype,ans.address))
            elif lookuptype == 'AAAA' or lookuptype=='aaaa':
                print('Domain: {} - DNS Lookuptype: {} - Answer: {}'.format(domain,lookuptype,ans.address))
            elif lookuptype == 'MX' or lookuptype=='mx':
                print('Domain: {} - DNS Lookuptype: {} - Answer: {} - Preference: {}'.format(domain,lookuptype,ans.exchange,ans.preference))
            elif lookuptype == 'NS' or lookuptype=='ns':
                print('Domain: {} - DNS Lookuptype: {} - Answer: {}'.format(domain,lookuptype,ans.target))
    except Exception as e:
            print(e)

    return answer

def info_DNS( myDomain = "www.google.com"):
    domain = DNS.from_text(myDomain)
    # Imprimiendo partes del dominio
    print("\tComposed in the following way:\t{}".format(domain.labels))
    return domain

def info_reverse_DNS( ip = "127.0.0.1"):
    domain = REVERSE.from_address(ip)
    print("\n\n\tNombre de dominio de {0} : {1}".format(ip, domain))
    print("\n\n\tIP {0} del dominio {1}".format(REVERSE.to_address(domain), domain))

def proccess(domain = "www.google.com", query_type = "A"):
    data_complete = {"domain": "",
                     "dns_lookuptype": "",
                     "compused": "",
                     "descrition": "",
                     "state": "",
                     "server_response_time": ""
                     }

    # Getting response of a query type
    ans = dnsQuery(domain, query_type)
    description = info_DNS(domain)
    data = main_process(domain)



    data_complete = { "domain" : str(domain),
                      "dns_lookuptype" : str(query_type),
                      "compused" : str(description.labels),
                      "descrition" : str(ans.response.to_text()).replace("\n"," - "),
                      "state" : str(data["state"]),
                      "server_response_time" : str(data["server_response_time"])
                    }
    

    dns = json.dumps(data_complete)
    f = open("dns.json", "w")
    f.write(dns)

    print("\t|====== Response of DNS' Query ======|")
    print("\t", ans.response.to_text())
    print("\tState:\t", data["state"])
    print("\tServer response time:\t", data["server_response_time"])
    print(dns)


"""
    for k, value in data_complete.items():
        print("{0},{1}".format(k,value))
"""


if __name__ == "__main__":
    print("*****************************")
    menu()
    domain     = input("Dominio :\t")
    query_type = input("Query Type:\t")
    print("*****************************\n")
    proccess(domain,query_type)


