help:
	@echo "Usage: make <target>"
	@echo "  dev            Starts the development server"
	@echo "  tunnel         Creates a tunnel to the server"
	@echo "  i18n-extract   Extracts the texts from the code"
	@echo "  i18n-update    Adds the translations to the code"
	@echo "  i18n-compile   Compiles the translations"
	@echo "  build          Build docker images"
	@echo "  rebuild        Rebuild docker images to update source code"


# docker commands
build:
	docker compose build
	docker compose up -d

rebuild:
	docker compose up -d db
	docker compose build web
	docker compose up --no-deps -d web

# i18n commands
i18n-extract:
	pybabel extract -o ./app/translations/messages.pot .

i18n-update:
	pybabel update -i ./app/translations/messages.pot -d ./app/translations -l es

i18n-compile:
	pybabel compile -d ./app/translations


# Dev commands
tunnel:
	cloudflared tunnel --url http://localhost:8000

dev:
	uvicorn app.main:app --host 127.0.0.1 --port 8000 --workers 1 --reload