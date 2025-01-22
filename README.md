# Mini App для лэндинговой рекламы в telegram
1. Создайте Telegram бота в @BotFather и получите токен бота.
2. Выполните команду `git pull <ссылка>` для получения репозитория из Git.
3. Создайте файл с названием`.env` в корне проекта (см. `env.example`) и внесите туда токен бота.
4. Создайте или используйте свой почтовый для отправки уведомлений по почте и внесите информацию о нем в файл .env
5. Выполните команду `docker compose up -d --build` на сервере с поддержкой https (до этого необходимо сделать на сервере сертификат и приватный ключ).
6. Укажите в `.env` файле доменное имя сервера.
7. Включите мини-приложение в Telegram в настройках бота в @BotFather и также введите туда доменное имя.
8. Ready!