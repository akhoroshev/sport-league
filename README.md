# sport-league
https://wiki.compscicenter.ru/index.php/Sport-league

Как установить docker-compose

https://docs.docker.com/compose/install/

После установки, переходим в корень проекта, пишем (предварительно заменив TOKEN на свой в файле bot/main.py, иначе ничего не будет работать)

`sudo docker-compose up -d`

Для остановки контейнеров, в этой же директории пишем

`sudo docker-compose stop`

Для удаления контейнеров

`sudo docker-compose down`

Если внесли изменения в код, и хотите перезапустить, то

`sudo docker-compose restart`

Команда, что-бы подлкючиться к БД

`sudo docker run -it --rm --net=host  mysql sh -c 'exec mysql -h"127.0.0.1" -uroot -p"root_password"'`
