import datetime
from uuid import uuid4


def date():
    return datetime.datetime.now()


def generate_id():
    id = str(uuid4())
    return id
