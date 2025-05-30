import psycopg2
from util.loader import getenv


async def postgres_connect():
    DB_NAME = getenv('DB_NAME')
    USER = getenv('DB_USER')
    PORT = getenv('DB_PORT')
    HOST = getenv('DB_HOST')
    PASSWORD = getenv('DB_PASSWORD')
    connect = psycopg2.connect(
        dbname=DB_NAME,
        user=USER,
        password=PASSWORD,
        host=HOST, port=PORT)
    return connect, connect.cursor()

async def create_tables():
    con, cur = await postgres_connect()
    cur.execute("""create table if not exists users(
    chat_id bigint primary key,
    fullname varchar(100),
    username varchar(100),
    phone_number varchar(20) unique,
    is_employee bool default FALSE
)""")

    cur.execute("""create table if not exists services(
    id serial primary key,
    name varchar(100)
)""")

    cur.execute("""create table if not exists employees(
    chat_id bigint references users(chat_id) unique,
    firstname varchar(100),
    lastname varchar(100),
    username varchar(100),
    phone_number varchar(20),
    service_id int references services(id)
)""")

    cur.execute("""create table if not exists orders(
    id serial primary key,
    user_id bigint references users(chat_id),
    user_phone varchar(20) references users(phone_number),
    employee_id int references employees(chat_id),
    service_id int references services(id),
    date varchar(50),
    time varchar(50),
    comment varchar(200)
)""")

    cur.execute("""create table if not exists messages(
    id serial primary key,
    user_id bigint references users(chat_id),
    message varchar(200)
)""")

    cur.execute("""create table if not exists deleted_users(
    user_id bigint
)""")

    con.commit()



async def check_user(chat_id) -> bool:
    con, cur = await postgres_connect()
    cur.execute("select * from users where chat_id = %s", (chat_id,))
    return True if cur.fetchone() else False

async def add_user(chat_id, fullname, username, phone):
    con, cur = await postgres_connect()
    cur.execute("insert into users(chat_id, fullname, username, phone_number) values (%s, %s, %s, %s)", (chat_id, fullname, username, phone))
    cur.execute("delete from deleted_users where user_id = %s", (chat_id, ))
    con.commit()

async def get_user(id: int):
    con, cur = await postgres_connect()
    cur.execute("select * from users where chat_id = %s", (id,))
    return cur.fetchone()

async def update_username(id: int, username):
    con, cur = await postgres_connect()
    cur.execute("update users set username = %s where chat_id = %s", (username, id))
    con.commit()

async def update_user(id: int, name = None, phone = None):
    con, cur = await postgres_connect()
    if name:
        cur.execute("update users set fullname = %s where chat_id = %s", (name, id))
    elif phone:
        cur.execute("update users set phone_number = %s where chat_id = %s", (phone, id))
    else:
        raise Exception("No data")
    con.commit()

async def delete_user_pg(id: int):
    con, cur = await postgres_connect()
    cur.execute("delete from users where chat_id = %s", (id,))
    cur.execute("insert into deleted_users(user_id) values (%s)", (id,))
    con.commit()



async def is_employee(chat_id):
    con, cur = await postgres_connect()
    cur.execute("select * from employees where chat_id = %s", (chat_id,))
    return True if cur.fetchone() else False

async def add_employee(chat_id, firstname, lastname, username, phone, service_id):
    con, cur = await postgres_connect()
    cur.execute("insert into employees(chat_id, firstname, lastname, username, phone_number, service_id) values (%s, %s, %s, %s, %s, %s)", (chat_id, firstname, lastname, username, phone, service_id))
    con.commit()



async def add_order():
    pass



async def get_all_services():
    con, cur = await postgres_connect()
    cur.execute("select * from services")
    return cur.fetchall()

async def get_service(service_id: int):
    con, cur = await postgres_connect()
    cur.execute("select * from services where id = %s", (service_id,))
    return cur.fetchone()
