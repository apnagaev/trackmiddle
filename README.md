# trackmiddle
middle server for osmand
For use, you must clone directory and chnge variables in conf/conf.txt
port1 - default script port
port2 - backup script port
osmandport - traccar osmand port
containername - traccar ip, hostname or containername
accuracyerr - if accuracy > accuracyerr, then accuracy=0
yaapikey1-3 - randomized apikeys for yandex locator service, used with https://github.com/apnagaev/geotracking/blob/main/laptoplocation.ps1
header - http header with real device IP

file conf/ip.txt contains json with ip/coordinates/altitude/accuracy/altitude and rnd parametrs. rnd make changes after rnd nubmer digit for avoid hits all devices to single point

you can dockerize it
docker build -t trackmiddle .

compose example:
  trackmiddle:
    image: trackmiddle
    dns:
      - dns_server_ip
    networks:
      - traccar
    ports:
      - 8899:8899
      - 8898:8898
    container_name: trackmiddle
    restart: unless-stopped
    environment:
      TZ: "Europe/Moscow"
    volumes:
      - ./ip.txt:/httpserver/conf/ip.txt
      - ./conf.txty:/httpserver/conf/conf.txt
