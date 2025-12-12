# ベースイメージ（必要ならバージョン固定も可）
FROM python:3.13

# コンテナ内の作業ディレクトリ
WORKDIR /container-api

# 依存関係だけ先にコピー＆インストール
COPY ./requirements.txt /container-api/requirements.txt

RUN pip install --no-cache-dir -r /container-api/requirements.txt

# アプリ本体をコピー
COPY ./app /container-api/app

# FastAPI は通常 8000 番ポートで動かすことが多い
EXPOSE 8080

# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080", "--reload"]
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8080}"]
