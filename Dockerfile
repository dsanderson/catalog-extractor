FROM library/ubuntu:16.04
RUN apt-get update
RUN apt-get install -y python-pip python-dev build-essential
RUN apt-get install -y tesseract-ocr
RUN pip install --upgrade pip
RUN pip install pyocr

COPY ocr-test.py ocr-test.py

CMD python ocr-test.py
