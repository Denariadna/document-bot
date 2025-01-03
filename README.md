# Бот хранения-документов
## Выполняли
Ступишин Даниил - @danula-ded
Денисова Арина - @denariadna

## Run
### Clear ports
```bash
scripts/cleanup_ports.sh
```

можно запустить через polling и через webhook, но на polling не будет работать работать отправка файлов через ручку /get-file

### Up docker compose 
```bash
docker compose up --build
```
возможно бот упадет при запуске, но если его перезагрузить (только бота), то он будет работать
под ботом понимается продюсер в папке src/app.py

### Migrate
```bash
PYTHONPATH=. python3 scripts/migrate.py
```


# Вопросы:

- Fast api
  - Что такое Middleware / Depends? Для чего? Как реализуется? 
  - Что такое gunicorn / uvicorn? Как правильно запускать Fast api на нескольких worker
  - Что такое lifespan? Когда отрабатывает код после yield?
  - Зачем нужен exec в startup.sh? Что будет если его убрать?
  - Как работают соединения к базе? Что такое Null Pool, какие альтернативы?
  - Где хранить настройки(конфиги) приложения? Какие удобные инструменты для этого?
  - Какая разница между аутентификацией и авторизацией? Как работает jwt?
- Docker
  - Что такое image?
  - Что такое слои image?
  - Что такое volume?
  - Что такое container?
  - Что такое ports?
  - Как вести разработку с докером, не пересобирая Image?
  - Что такое healthcheck?
- Telegram
  - Разница работы polling и webhook
  - Уметь рассказать как правильно организовать работы webhook
  - Что такое State?
  - Где хранить данные о пользователе?
  - Как передать данные через callback?
- RabbitMQ
  - Что такое exchange?
  - Что такое queue? За что отвечает параметр no_ack?
  - Что такое routing key, bind?
  - Как отправить и получить сообщение в очередь?
  - Как получить сообщение из очереди?
  - Как в рамках Fast api сделать получение сообщения из очереди?
  - Уметь рассказать про парадигму асинхронного бекенда? Зачем оно надо? Чем надежнее?
- Тесты
  - Что такое pytest? Как работает conftest?
  - Что такое fixture? Какие есть scope у fixture? Зачем нужны scope?
  - Как сделать удаление после теста через transaction?
  - Что такое mock? Что такое monkeypatch? Как работает AsyncMock?
- Общие вопросы
  - Что такое сквозное логирование? Как его настроить?
  - Где лежат данные в вашем проекте? Уметь ответить на вопросы - что лежит в бд? Что лежит в очереди? И подобные
  - Знать что делает каждая библиотека в pyproject.toml


Бот для документа-хранения 
   - пользователь для который будет управлять документами
   - меню
     - добавить документ 
       - после нажатия диалог с помощью которого можно добавить тип документа, его название
     - показать документы
       - первым на выбор идут типы документов (в разрезе типа может быть много объектов)
       - после нажатия на тип, сам выбор документа

Требования к проекту:
- ✅ Упаковка проекта в докер-компоуз и запуск через docker compose up без дополнительной настройки
- ✅ Два формата запуска - через polling и через webhook
- ✅ прохождение flake8 + mypy в соответствии с конфигурациями проекта
- ✅ Стейт отдельный под каждого пользователя
- ✅ Без доступа к бд в сервисе aiogram
- ✅ Метрики: 
  - Время выполнения всех интеграционных методов (запросы на бекенд и телеграм)
  - Иметь свой декоратор для обертки таких методов. Использовать Histogram для подсчета времени (Декоратор необязательно)
  - Сделать свою middleware для подсчета rps на сервис (*)
  - Сделать счетчик отправленных из бота сообщений в очередь и полученных сообщений консумером 
- ✅ Настройки в env
- ✅ Без дублирования кода
- ✅ poetry как сборщик пакетов
- ✅ Обработка ошибок и соответствующие ответы от бота
- Обработка флуда (*)
- ✅ В README.md ожидается увидеть как что работает, чтобы можно было ознакомиться проще с проектом
- ✅ Сквозное логирование                                                                                                  
- ✅ Если в сервисе используется хранилище s3(minio), то для этого сделать отдельную ручку. Можно использовать nginx
- ✅ Обратить внимание на индексацию в моделях, подумать об unique_constraint
- тесты 
  - Сделать тест интеграционный на консюмера
  - Сделать юнит тест на обработчик сообщения aiogram (средний обработчик)

