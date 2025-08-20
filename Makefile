help:
	@echo "Usage: make <target>"
	@echo "  dev            Starts the development server"
	@echo "  tunnel         Creates a tunnel to the server"
	@echo "  i18n-extract   Extracts the texts from the code"
	@echo "  i18n-update    Adds the translations to the code"
	@echo "  i18n-compile   Compiles the translations"

dev:
	uvicorn app.main:app --host 127.0.0.1 --port 8000 --workers 1 --reload

i18n-extract:
	pybabel extract -o ./app/translations/messages.pot .

i18n-update:
	pybabel update -i ./app/translations/messages.pot -d ./app/translations -l es

i18n-compile:
	pybabel compile -d ./app/translations

tunnel:
	cloudflared tunnel --url http://localhost:8000
