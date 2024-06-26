FROM python:3.10-slim

ENV DEBIAN_FRONTEND noninteractive
ENV LANG C.UTF-8
ENV GRADIO_SERVER_NAME 0.0.0.0

RUN useradd -m -u 1000 user
WORKDIR /home/user/app

RUN --mount=target=requirements.txt,source=requirements.txt :\
    && pip install --no-cache-dir -r requirements.txt

COPY . .
EXPOSE 7860

ENTRYPOINT ["python", "app.py"]