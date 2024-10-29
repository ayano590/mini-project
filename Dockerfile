FROM python:3.12

WORKDIR /app

COPY . .

RUN pip install --upgrade pip && pip install -r requirements.txt

CMD python main.py

# docker build -t <imagename> .

# docker run -it --rm -v "${PWD}:/app" <imagename>