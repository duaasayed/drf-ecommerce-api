FROM python
RUN apt-get update && apt-get install -y nginx
COPY . /myapp
WORKDIR /myapp
RUN pip install -r requirements.txt
COPY /core/.env.example /core/.env
RUN python manage.py migrate
EXPOSE 8088
ENTRYPOINT ["python", "manage.py", "runserver", "0.0.0.0:8088"]