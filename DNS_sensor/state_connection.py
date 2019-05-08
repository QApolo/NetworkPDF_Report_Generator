import subprocess
import time

def ping(host):
  ret = subprocess.call(['ping', '-c', '3', '-W', '5', host],
    stdout=open('/dev/null', 'w'),
    stderr=open('/dev/null', 'w'))
  return ret == 0

def net_is_up(host):
  print ("[%s] Checking if network is up..." % time.strftime("%Y-%m-%d %H:%M:%S"))
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


"""
if __name__ == "__main__":
    domain = input("Dominio: ")
    dictionary = main_process(domain)
    for value in dictionary:
        print(value)
"""