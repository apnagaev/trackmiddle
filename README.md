# trackmiddle
middle server for osmand
For use, you must clone directory and chnge variables in conf/conf.txt
port1 - default script port
port2 - backup script port
osmandport - traccar osmand port
containername - traccar ip, hostname or containername
accuracyerr - if accuracy > accuracyerr, then accuracy=0
yaapikey - apikey for yandex locator service

file conf/ip.txt contains json with ip/coordinates/altitude/accuracy

you can dockerize it
docker build -t trackmiddle .

compose example:
  trackmiddle:
    image: trackmiddle
    dns:
      - 10.255.253.2
    networks:
      - traccar
    ports:
      - 8899:8899
    container_name: trackmiddle
    restart: unless-stopped
    environment:
      TZ: "Europe/Moscow"
    volumes:
      - ./ip.txt:/httpserver/conf/ip.txt
      - ./conf.txty:/httpserver/conf/conf.txt
