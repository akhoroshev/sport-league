# sport-league
https://wiki.compscicenter.ru/index.php/Devdays_%D0%9E%D1%81%D0%B5%D0%BD%D1%8C_2018#Ping-Pong_league


Как установить docker-compose

https://docs.docker.com/compose/install/

После установки, переходим в корень проекта, пишем

`sudo docker-compose up -d`

Для остановки контейнеров, в этой же директории пишем

`sudo docker-compose stop`

Для удаления контейнеров

`sudo docker-compose down`

Если внесли изменения в код, и хотите перезапустить, то

`sudo docker-compose restart`

Команда, что-бы подлкючиться к БД

`sudo docker run -it --rm --net=host  mysql sh -c 'exec mysql -h"127.0.0.1" -uroot -p"root_password"'`
