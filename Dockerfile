FROM python:3.7
ENV PYTHONUNBUFFERED 1

RUN pip3.7 install pipenv

COPY . code
WORKDIR /code
RUN pipenv install --system --dev

EXPOSE 8000

CMD cd backend && python manage.py migrate && gunicorn --bind 0.0.0.0:8000 --access-logfile - backend.wsgi:application
