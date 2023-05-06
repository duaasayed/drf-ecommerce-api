FROM python:3.10-slim
COPY . /myapp
WORKDIR /myapp
RUN pip install -r requirements.txt
COPY /core/.env.example /core/.env
RUN python manage.py migrate
EXPOSE 8000
ENTRYPOINT ["python", "manage.py", "runserver", "0.0.0.0:8000"]