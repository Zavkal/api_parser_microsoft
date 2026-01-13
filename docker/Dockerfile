FROM python:3.12-slim

WORKDIR /app

COPY pyproject.toml uv.lock* ./

# Устанавливаем uv
RUN pip install uv

# Устанавливаем только зависимости (БЕЗ установки проекта)
# Извлекаем зависимости из pyproject.toml и устанавливаем их
RUN python3 -c "import tomllib; f=open('pyproject.toml','rb'); d=tomllib.load(f); deps=d['project']['dependencies']; open('/tmp/deps.txt','w').write('\n'.join(deps))" && \
    uv pip install --system -r /tmp/deps.txt && \
    rm /tmp/deps.txt

CMD ["uv", "run", "python", "main.py"]