
curl -LsSf https://astral.sh/uv/install.sh | sh

uv sync --dev
uv run python manage.py runserver 0.0.0.0:8000
