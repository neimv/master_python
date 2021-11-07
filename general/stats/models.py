from datetime import datetime
from pony.orm import (
    Database, PrimaryKey, Required, Set, Optional
)


db = Database()


class Client(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Required(str, 64, unique=True)
    ip = Required(str, 16)
    ram = Set('Ram')
    swap = Set('Swap')
    cpu = Set('Cpu')
    single_cpu = Set('SingleCPU')
    disk = Set('Disk')


class Ram(db.Entity):
    id = PrimaryKey(int, auto=True)
    client = Optional(Client)
    date = Required(datetime, precision=0, default=lambda: datetime.now())
    total = Optional(float)
    used = Optional(float)
    free = Optional(float)
    unit = Optional(str, 8)


class Swap(db.Entity):
    id = PrimaryKey(int, auto=True)
    client = Optional(Client)
    date = Optional(datetime, default=lambda: datetime.now())
    total = Optional(float)
    used = Optional(float)
    free = Optional(float)
    unit = Optional(str, 8)


class Cpu(db.Entity):
    id = PrimaryKey(int, auto=True)
    client = Optional(Client)
    date = Optional(datetime, default=lambda: datetime.now())
    percent_use = Optional(float)
    min_freq = Optional(float)
    max_freq = Optional(float)
    actual_freq = Optional(float)


class SingleCPU(db.Entity):
    id = PrimaryKey(int, auto=True)
    client = Optional(Client)
    date = Optional(datetime, default=lambda: datetime.now())
    num_cpu = Optional(int)
    percent_use = Optional(float)
    min_freq = Optional(float)
    max_freq = Optional(float)
    actual_freq = Optional(float)


class Disk(db.Entity):
    id = PrimaryKey(int, auto=True)
    client = Optional(Client)
    date = Optional(datetime, default=lambda: datetime.now())
    total = Optional(float)
    used = Optional(float)
    free = Optional(float)
    unit = Optional(str, 8)


db.bind(provider='sqlite', filename='stats_db.sqlite', create_db=True)
db.generate_mapping(create_tables=True)
