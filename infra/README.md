# PostgreSQL dev

`modules/database` описывает БД PostgreSQL. `dev` вызывает модуль
для создания `control_plane_dev` и содержит настройки подключения Terraform.

Контейнер PostgreSQL запускается через `deploy/database/postgresql`.
Compose использует `.env.dev` из этого каталога. Для Terraform нужны:

- `POSTGRES_HOST=cps-pg`: адрес сервиса внутри Docker-сети.
- `POSTGRES_PORT=5432`: внутренний порт PostgreSQL.
- `POSTGRES_USER` и `POSTGRES_PASSWORD`: учётные данные администратора БД.

Для первоначальной инициализации Compose явно задаёт `POSTGRES_DB=postgres`,
перекрывая одноимённое значение из `.env.dev`. Terraform подключается
к этой служебной БД и управляет отдельной БД `control_plane_dev`.
Существующий том PostgreSQL при этом не переинициализируется.

Команды выполняются из корня репозитория:

```bash
make -C deploy/database/postgresql docker-dev-up
make -C infra/dev init
make -C infra/dev fmt-check
make -C infra/dev validate
```

Дождись готовности PostgreSQL к подключениям. Если `control_plane_dev`
уже существует, но отсутствует в текущем Terraform state, сначала импортируй её:

```bash
docker compose --env-file deploy/database/postgresql/.env.dev \
  -f deploy/database/postgresql/docker-compose.dev.yaml \
  run --rm terraform import \
  module.database.postgresql_database.this control_plane_dev
```

Для новой БД импорт не нужен. Затем проверь план и примени его:

```bash
make -C infra/dev plan
make -C infra/dev apply
```

State хранится в `infra/dev/terraform.tfstate`, служебные файлы —
в `infra/dev/.terraform/`. State нужно сохранять между запусками;
он исключён из Git вместе с сохранёнными планами.
`.terraform.lock.hcl` сохраняет зафиксированную версию провайдера.

Если используется state от прежнего каталога `deploy/database/postgresql/terraform`,
его нужно отдельно перенести в `infra/dev`. Блок `moved` сопоставляет
прежний адрес ресурса с адресом внутри модуля; сам файл state он не переносит.

Backend подключается к `control_plane_dev` после её создания.
Запуск backend остаётся отдельной командой корневого Makefile.
