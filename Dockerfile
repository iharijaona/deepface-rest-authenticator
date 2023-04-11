FROM tensorflow/tensorflow:2.9.0-gpu

ENV NVIDIA_VISIBLE_DEVICES all
ENV NVIDIA_DRIVER_CAPABILITIES compute,utility
ENV PATH $PATH:/home/user/.local/bin
# Create a working directory
RUN mkdir /app
WORKDIR /app

RUN apt-get update && apt-get install -y libgl1 && apt-get install -y --reinstall netbase

COPY requirements.txt /app/requirements.txt
RUN echo ${PATH}
RUN /usr/bin/python3 -m pip install --upgrade pip
RUN pip3 install -r requirements.txt
COPY . /app

RUN  mkdir -p ~/.deepface/weights

EXPOSE 8888

CMD ["gunicorn", "-c", "./gunicorn.config.py", "wsgi:app"]