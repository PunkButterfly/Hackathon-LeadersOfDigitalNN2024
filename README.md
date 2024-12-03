# Структура репозитория

ВАЖНО! Тестовый стенд поднят на http://hackathon-leaders-of-digital-nn.punkbutterfly.tech:8129/ , руками не обязательно запускать весь процесс.

Краткая навигация:

workflows -> Сценарии CI/CD  
backend -> Бекэнд микросервис с инференсом моделей  
frontend -> Фронтэнд микросервис с демонстрационным сайтом  
notebooks -> Папка с ноутбуком обучения  
preimages -> Зависимости для первого слоя Docker-образа  

Чтобы запустить сервис, нужно собрать пре-изображения бекенда

```
docker build -t hach-leaders-of-digital-backend-preimage:latest -f preimages/backend/Dockerfile .
```

```
docker build -t hach-leaders-of-digital-frontend-preimage:latest -f preimages/frontend/Dockerfile .
```

После чего запустить сам docker-compose

```
sudo docker compose up --build -d
```

Еще, важно сложить порты в .env фалы, без этого сервис не запустится. 
