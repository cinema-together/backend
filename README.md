# Бекэнд «Кино вместе»

## Запуск локально для разработки
1. Создать сеть в докере, если она ещё не создана
```shell
docker network create -d bridge cinema-together-net
```
2. Скопировать env-файл
```shell
cat config/.env.template > config/.env
```
3. Заполнить `config/.env` файл секретами.
4. Запустить контейнеры
```sh
docker-compose up
```
## Запуск тестов
```shell
docker-compose run  --rm app pytest
```
