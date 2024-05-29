import datetime
import http.server
import socketserver
import urllib.parse
import re
import requests
import linecache
import json
import ipaddress
import random
import requests

print ("---------------start----------------")
with open('conf/conf.txt') as conffile:
  print(f'{datetime.datetime.now().strftime("%Y-%m-%d %X")} open conf json file')
  conff = conffile.read()
  confj = json.loads(conff)

print(f'{datetime.datetime.now().strftime("%Y-%m-%d %X")} youre configuration is\n{confj[0]}')

######must be filled
#port for trackmiddle
port1=confj[0]["port1"]
#backup port for trackmiddle
port2=confj[0]["port2"]
#traccar osmand port
osmandport=confj[0]["osmandport"]
#traccar ip/hostname/containername
containername=confj[0]["containername"]
#containername="127.0.0.1"
######must be filled
accuracyerr=confj[0]["accuracyerr"]
ipheader=confj[0]["header"]
hostname="http://"+containername+":"+osmandport
key="id="
key='/?'+key

yandexurl="https://api.lbs.yandex.net/geolocation/"
keysarr=[confj[0]["yaapikey1"],confj[0]["yaapikey2"],confj[0]["yaapikey3"]]


with open('conf/ip.txt') as ipfile:
  print(f'{datetime.datetime.now().strftime("%Y-%m-%d %X")} open ip json file')
  ipf = ipfile.read()
  ipj = json.loads(ipf)

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class CustomHttpRequestHandler(http.server.SimpleHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/x-www-form-urlencoded')
        self.end_headers()
    def do_POST(self):
        global ipj
        global yandexuri
        global yaapikey
        uri=urllib.parse.unquote(self.path)
        ipislocal = False
        if uri.startswith(key):
          devid = re.search('id=(.*)&time', uri)
          devid = devid.group(1)
          uri=uri.replace('&lat=&', '&lat=0.0&')
          uri=uri.replace('&lon=&', '&lon=0.0&')
          uri=uri.replace('&realip=&', '&')
          print(f'{bcolors.OKBLUE}{datetime.datetime.now().strftime("%Y-%m-%d %X")} script started for device {devid}{bcolors.ENDC}')
          print(f'{datetime.datetime.now().strftime("%Y-%m-%d %X")} youre uri={uri}')


          try:
            print(f'{bcolors.HEADER}{datetime.datetime.now().strftime("%Y-%m-%d %X")} headers=\n{self.headers}{bcolors.ENDC}')
            try:
              ip = ipaddress.ip_address(self.headers[ipheader])
            except:
              ip = ipaddress.ip_address(self.client_address[0])
            try:
              realip = re.search('&realip=(\\d*.\\d*.\\d*.\\d*)&', uri)
              realip = realip.group(1)
              realip = ipaddress.ip_address(realip)
            except:
              realip = ip
            print(f'{bcolors.BOLD}{datetime.datetime.now().strftime("%Y-%m-%d %X")} yore ip={ip}{bcolors.ENDC}')
            print(f'{bcolors.BOLD}{datetime.datetime.now().strftime("%Y-%m-%d %X")} yore realip={realip}{bcolors.ENDC}')
            for item in ipj:
              msk = ipaddress.ip_network(item["mask"])
              if (ip in msk) or (realip in msk):
                print(f'{bcolors.BOLD}{datetime.datetime.now().strftime("%Y-%m-%d %X")} msk={msk} ip={ip} realip={realip} loc={item["name"]}{bcolors.ENDC}')
                ipislocal = True

                latr = item["lat"]
                lonr = item["lon"]
                latr = latr[:item["rnd"]] + str(random.randint(0,99))
                lonr = lonr[:item["rnd"]] + str(random.randint(0,99))

                lat = re.search('lat=(\\d*.\\d*)&', uri)
                lat = lat.group(1)
                lon = re.search('lon=(\\d*.\\d*)&', uri)
                lon = lon.group(1)
                try:
                  accuracyr=''
                  accuracy = re.search('accuracy=(\\d*.\\d*)&', uri)
                  accuracy = 'accuracy='+accuracy.group(1)
                  accuracyr = 'accuracy='+item["accuracy"]
                  uri = uri.replace(accuracy, accuracyr)
                except:
                  uri = uri + '&accuracy='+item["accuracy"]
                try:
                  altitude = re.search('altitude=(\\d*.\\d*)&', uri)
                  altitude = 'altitude='+altitude.group(1)
                  altituder = 'altitude='+item["altitude"]
                  uri = uri.replace(altitude, altituder)
                except:
                  uri = uri + '&altitude='+item["altitude"]
                try:
                  speed = re.search('&speed=(\\d*.\\d*)&', uri)
                  speed = 'speed='+speed.group(1)
                  speedr = 'speed=0'
                  uri = uri.replace(speed, speedr)
                except:
                  uri = uri + '&speed=0'


                uri=uri.replace(lat, latr)
                uri=uri.replace(lon, lonr)
                uri=uri + '&script=trackmiddle'
                uri=uri+ '&loc='+item["name"]
                ipislocal = True

            content_len = self.headers.get("Content-Length")
            if int(content_len) > 160 and ipislocal is False: # and checkrealip !='':
              body = self.rfile.read(int(content_len))
              yaapikeyj=random.choices(keysarr, k=1)
              yaapikey=yaapikeyj[0]
              print(f'{datetime.datetime.now().strftime("%Y-%m-%d %X")} start yandex yaapikey={yaapikey}')
              yandexjson=str(body)
              yandexjson=yandexjson.replace('yaapikey', yaapikey)
              yandexjson=yandexjson.replace('b\'', '')
              yandexjson=yandexjson.replace('}\'', '}')
              ryan = requests.post(url=yandexurl,data=yandexjson)
              yandexjsonresponse = json.loads(ryan.content)
              print(f'{bcolors.OKCYAN}{datetime.datetime.now().strftime("%Y-%m-%d %X")} yandexjson={yandexjson}{bcolors.ENDC}')
              if "error" not in str(yandexjsonresponse):
                print(f'{bcolors.WARNING}{datetime.datetime.now().strftime("%Y-%m-%d %X")} yandex ok, length={int(content_len)} yandexjsonresponse={yandexjsonresponse}{bcolors.ENDC}')
                latr=yandexjsonresponse["position"]["latitude"]
                lonr=yandexjsonresponse["position"]["longitude"]
                lat = re.search('lat=(\\d*.\\d*)&', uri)
                lat = lat.group(1)
                lon = re.search('lon=(\\d*.\\d*)&', uri)
                lon = lon.group(1)
                uri=uri.replace(lat, str(latr))
                uri=uri.replace(lon, str(lonr))
                uri=uri+'&yaloc=true'
                if yandexjsonresponse["position"]["precision"] <= accuracyerr:
                  try:
                    accuracy = re.search('accuracy=(\\d*.\\d*)&', uri)
                    accuracy = 'accuracy='+accuracy.group(1)
                    accuracyr = 'accuracy='+yandexjsonresponse["position"]["precision"]
                    uri = uri.replace(accuracy, str(accuracy))
                  except:
                    uri = uri + '&accuracy='+str(yandexjsonresponse["position"]["precision"])
                else:
                  uri = uri + '&accuracy=0'
                print(f'{bcolors.OKGREEN}{datetime.datetime.now().strftime("%Y-%m-%d %X")} coordinates fixed by yandex{bcolors.ENDC}')



            uri=uri.replace('&driverUniqueId=&', '&')
            url=hostname+uri+'&sourceip='+str(ip)
            print(f'{bcolors.BOLD}{datetime.datetime.now().strftime("%Y-%m-%d %X")} request={url}{bcolors.ENDC}')
            req = requests.post(url=url,data="")
            print(f'{bcolors.OKCYAN}{datetime.datetime.now().strftime("%Y-%m-%d %X")} response from traccar={req}{bcolors.ENDC}')
            self._set_headers()
            self.send_response(req.status_code)
            self.end_headers()
            self.path = 'true.txt'
          except:
            print(f'{bcolors.FAIL}{datetime.datetime.now().strftime("%Y-%m-%d %X")} parsing fail!{bcolors.ENDC}')
            self.send_response(500)
            self.path = 'fail.txt'
        else:
          message = "key failure"
          self.send_response(400)
          self.path = 'fail.txt'
        if (self.path == 'true.txt'):
           print(f'{bcolors.OKGREEN}{datetime.datetime.now().strftime("%Y-%m-%d %X")} script finished for device {devid}{bcolors.ENDC}')
        else:
          print(f'{bcolors.FAIL}{datetime.datetime.now().strftime("%Y-%m-%d %X")} false={self.client_address} device={devid}{bcolors.ENDC}')
    def do_GET(self):
      self.send_response(403)
      self.path = 'fail.txt'

handler = CustomHttpRequestHandler
try:
  port=port1
  server=socketserver.TCPServer(("", port), handler)
except:
  port=port2
  server=socketserver.TCPServer(("", port), handler)
print(f'{datetime.datetime.now().strftime("%Y-%m-%d %X")} Server started at port {port}. Press CTRL+C to close the server.')
try:
  server.serve_forever()
  httpd.timeout = 5
except KeyboardInterrupt:
  server.server_close()
  print(f'{datetime.datetime.now().strftime("%Y-%m-%d %X")} Server Closed')
