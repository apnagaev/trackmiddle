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
######must be filled
#port for trackmiddle
port1=8899
#backup port for trackmiddle
port2=8898
#traccar osmand port
osmandport="15055"
#traccar ip/hostname/containername
containername="traccar"
######must be filled
accuracyerr=1000
hostname="http://"+containername+":"+osmandport
key="id="
key='/?'+key

yandexurl="https://api.lbs.yandex.net/geolocation/"
yaapikey="24ae0420-1a56-4c0c-af5f-2b8eb4ad0138"


with open('conf/ip.txt') as ipfile:
  print(f'{datetime.datetime.now().strftime("%Y-%m-%d %X")} open ip json file')
  ipf = ipfile.read()
  ipj = json.loads(ipf)


class CustomHttpRequestHandler(http.server.SimpleHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
    def do_POST(self):
        global ipj
        global yandexuri
        global yaapikey
        uri=urllib.parse.unquote(self.path)
        ipislocal = False
        if uri.startswith(key):
          devid = re.search('id=(.*)&t', uri)
          devid = devid.group(1)
          print(f'{datetime.datetime.now().strftime("%Y-%m-%d %X")} =============================== script started for device {devid} ========================')
          print(f'{datetime.datetime.now().strftime("%Y-%m-%d %X")} youre uri={uri}')
          print(f'{datetime.datetime.now().strftime("%Y-%m-%d %X")} youre ip={self.client_address[0]}')
          try:
            print(f'{datetime.datetime.now().strftime("%Y-%m-%d %X")} headers=\n{self.headers}')
            try:
              print(f'{datetime.datetime.now().strftime("%Y-%m-%d %X")} check header ip')
              ip = ipaddress.ip_address(self.headers["x-real-ip"])
              print(f'{datetime.datetime.now().strftime("%Y-%m-%d %X")} headerip={ip}')
            except:
              ip = ipaddress.ip_address(self.client_address[0])
            for item in ipj:
              msk = ipaddress.ip_network(item["mask"])
#              print(f'{datetime.datetime.now().strftime("%Y-%m-%d %X")} ip={ip} mask={msk}')
              if ip in msk:
                print(f'{datetime.datetime.now().strftime("%Y-%m-%d %X")} mask true')
                print(f'{datetime.datetime.now().strftime("%Y-%m-%d %X")} msk={msk} ip={ip}')
                print(f'{datetime.datetime.now().strftime("%Y-%m-%d %X")} json string={item}')


#                latr = item["lat"]
#                lonr = item["lon"]

                latr = item["lat"]
                lonr = item["lon"]
                r=random.randint(0,99)
                latr = latr[:item["rnd"]] + str(random.randint(0,99))
                lonr = lonr[:item["rnd"]] + str(random.randint(0,99))

                print(f'{datetime.datetime.now().strftime("%Y-%m-%d %X")} uri_old={uri}')
                lat = re.search('lat=(\\d*.\\d*)&', uri)
                lat = lat.group(1)
                lon = re.search('lon=(\\d*.\\d*)&', uri)
                lon = lon.group(1)
                try:
                  accuracyr=''
                  accuracy = re.search('accuracy=(\\d*.\\d*)&', uri)
                  print (f'{datetime.datetime.now().strftime("%Y-%m-%d %X")} old_accuracy={accuracy.group(1)}')
                  accuracy = 'accuracy='+accuracy.group(1)
                  print(item["accuracy"])
                  accuracyr = 'accuracy='+item["accuracy"]
                  uri = uri.replace(accuracy, accuracyr)
                except:
                  print(f'{datetime.datetime.now().strftime("%Y-%m-%d %X")} accuracy empty')
                  uri = uri + '&accuracy='+item["accuracy"]
                try:
                  altitude = re.search('altitude=(\\d*.\\d*)&', uri)
                  altitude = 'altitude='+altitude.group(1)
                  altituder = 'altitude='+item["altitude"]
                  uri = uri.replace(altitude, altituder)
                except:
                  print(f'{datetime.datetime.now().strftime("%Y-%m-%d %X")} altitude empty')
                  uri = uri + '&altitude='+item["altitude"]
                try:
                  speed = re.search('&speed=(\\d*.\\d*)&', uri)
                  speed = 'speed='+speed.group(1)
                  speedr = 'speed=0'
                  uri = uri.replace(speed, speedr)
                except:
                  print(f'{datetime.datetime.now().strftime("%Y-%m-%d %X")}  speed empty')
                  uri = uri + '&speed=0'


#                print(f'{datetime.datetime.now().strftime("%Y-%m-%d %X")} if accuracy {accuracy} accurancyr {accuracyr}')
#                if accuracy > item["accuracy"]:
#                  print(f'{datetime.datetime.now().strftime("%Y-%m-%d %X")} fix accuracy from {accuracy} to {accuracyr}')
#                  uri = uri.replace(accuracy, accuracyr)

                uri=uri.replace(lat, latr)
                uri=uri.replace(lon, lonr)
                ipislocal = True
#                uri=uri.replace('&driverUniqueId=&', '&')
                uri=uri + '&script=trackmiddle'
                uri=uri+ '&loc='+item["name"]
                print(f'{datetime.datetime.now().strftime("%Y-%m-%d %X")} uri_new={uri}')

            content_len = self.headers.get("Content-Length")
            print(content_len)
#            body = self.rfile.read(int(content_len))
#            print(str(body))
            if int(content_len) > 6 and ipislocal is False:
              body = self.rfile.read(int(content_len))
#              print(body)
              print(yaapikey)
              yandexjson=str(body)
              print(f'{datetime.datetime.now().strftime("%Y-%m-%d %X")} work with body')
              yandexjson=yandexjson.replace('yaapikey', yaapikey)
              yandexjson=yandexjson.replace('b\'', '')
              yandexjson=yandexjson.replace('}\'', '}')
              print(f'{datetime.datetime.now().strftime("%Y-%m-%d %X")} body={yandexjson}')
              ryan = requests.post(url=yandexurl,data=yandexjson)
              print(f'{datetime.datetime.now().strftime("%Y-%m-%d %X")} yandexresponse={ryan.content}')
              print(f'{datetime.datetime.now().strftime("%Y-%m-%d %X")} uri_old={uri}')
              lat = re.search('lat=(\\d*.\\d*)&', uri)
              lat = lat.group(1)
              lon = re.search('lon=(\\d*.\\d*)&', uri)
              lon = lon.group(1)
              yandexjsonresponse = json.loads(ryan.content)
              print(f'{datetime.datetime.now().strftime("%Y-%m-%d %X")} {yandexjsonresponse}')
              latr=yandexjsonresponse["position"]["latitude"]
              lonr=yandexjsonresponse["position"]["longitude"]
              print(f'{lat} {lon} {yandexjsonresponse["position"]["latitude"]} {yandexjsonresponse["position"]["longitude"]}')
              print(f'uri={uri}')
              uri=uri.replace(lat, str(latr))
              uri=uri.replace(lon, str(lonr))
              if yandexjsonresponse["position"]["precision"] <= accuracyerr:
                try:
                  accuracy = re.search('accuracy=(\\d*.\\d*)&', uri)
                  accuracy = 'accuracy='+accuracy.group(1)
                  accuracyr = 'accuracy='+yandexjsonresponse["position"]["precision"]
                  uri = uri.replace(accuracy, str(accuracy))
                except:
                  print(f'{datetime.datetime.now().strftime("%Y-%m-%d %X")} accuracy empty')
                  uri = uri + '&accuracy='+str(yandexjsonresponse["position"]["precision"])
              else:
                uri = uri + '&accuracy=0'
              print(f'{datetime.datetime.now().strftime("%Y-%m-%d %X")} coordinates fixed by yandex')



            print(f'{datetime.datetime.now().strftime("%Y-%m-%d %X")} sending message')
            print(f'{datetime.datetime.now().strftime("%Y-%m-%d %X")} hostname={hostname}')
            print(f'{datetime.datetime.now().strftime("%Y-%m-%d %X")} path={uri}')
            print(f'{datetime.datetime.now().strftime("%Y-%m-%d %X")} ip={str(ip)}')
            uri=uri.replace('&driverUniqueId=&', '&')
            url=hostname+uri+'&sourceip='+str(ip)
            print(f'{datetime.datetime.now().strftime("%Y-%m-%d %X")} request={url}')
            r = requests.post(url=url,data="")
            print(f'{datetime.datetime.now().strftime("%Y-%m-%d %X")} !!!!!!!!!!!!!!!!!!!!response from traccar={r}')
            self._set_headers()
            self.send_response(r.status_code)
            self.end_headers()
            self.path = 'true.txt'
          except:
            print(f'{datetime.datetime.now().strftime("%Y-%m-%d %X")} !!!!!!!!!!!!!!!!!!!!!!!!parsing fail!!!!!!!!!!!!!!!')
            self.send_response(500)
            self.path = 'fail.txt'
        else:
          message = "key failure"
          self.send_response(400)
          self.path = 'fail.txt'
        if (self.path == 'true.txt'):
           print(f'{datetime.datetime.now().strftime("%Y-%m-%d %X")} =======================script finished for device {devid}=========================')
        else:
          print(f'{datetime.datetime.now().strftime("%Y-%m-%d %X")} false={self.client_address}')
        return http.server.SimpleHTTPRequestHandler.do_GET(self)
    def do_GET(self):
      if self.path == '/favicon.ico':
        print(f'{datetime.datetime.now().strftime("%Y-%m-%d %X")} skip favicon')
        self.send_response(400)
        self.path = 'fail.txt'
      else:
        self.send_response(400)
        self.path = 'fail.txt'
      return http.server.SimpleHTTPRequestHandler.do_GET(self)

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
except KeyboardInterrupt:
  server.server_close()
  print(f'{datetime.datetime.now().strftime("%Y-%m-%d %X")} Server Closed')
