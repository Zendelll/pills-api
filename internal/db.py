import psycopg2
from psycopg2.extras import NamedTupleCursor
from dotenv import load_dotenv
import json
import os
import atexit
from typing import NamedTuple
from internal.logger import logger

with open("/usr/src/app/config.json") as f:
        CONF = json.load(f)
QUERY_PATH = CONF['QUERY_PATH']
#QUERY_PATH = "/Users/zendell/Pills-service/pills-api/query"
load_dotenv()
connection = psycopg2.connect(dbname = os.getenv("DB_NAME"), user = os.getenv("DB_USER"), password = os.getenv("DB_PASS"), host = os.getenv("DB_HOST"), port = int(os.getenv("DB_PORT")), async_ = False )

def close_connection(conn):
    conn.close()

def postgres_request(query: str, params: dict = None) -> NamedTuple:
    with connection.cursor(cursor_factory=NamedTupleCursor) as curs:
        curs.execute(query, params)
        result = curs.fetchall()
    connection.commit()
    logger.debug(result)
    return result

def get_user_meds(login: str) -> list:
    """Returns list of NamedTuples where each element = 1 med that user have

    NamedTuple conatins: user_login, med_name, amount, daily_usage, last_count_date
    """
    logger.debug("и уже в функции дб")
    with open(f"{QUERY_PATH}/get_user_meds.sql", 'r') as f:
        query = f.read().replace('\n', ' ')
    return postgres_request(query, {"login":login})

def get_user_state(login: str) -> str:
    """Returns string with user state"""
    with open(f"{QUERY_PATH}/get_user_state.sql", 'r') as f:
        query = f.read().replace('\n', ' ')
    result = postgres_request(query, {"login":login})
    if result:
        return result[0].user_state
    return ""

def update_user_state(login: str, state: str) -> NamedTuple:
    """Updates state in db. Used only in telegram bot
    
    Returns NamedTuple (f_column_=True) on success"""
    with open(f"{QUERY_PATH}/update_user_state.sql", 'r') as f:
        query = f.read().replace('\n', ' ')
    result = postgres_request(query, {"login": login, "state": state})
    if result: return result[0]
    return ()

def set_med(login: str, med_name: str, daily_usage: int, amount: int) -> NamedTuple:
    """Creates new med for user. 
    If med with this name exists for this user, update old with new daily_usage and amount
    
    Returns NamedTuple (f_column_=True) on success"""
    with open(f"{QUERY_PATH}/set_med.sql", 'r') as f:
        query = f.read().replace('\n', ' ')
    result = postgres_request(query, {"login": login, "med_name": med_name, "daily_usage": daily_usage, "amount": amount})
    if result: return result[0]
    return ()

def delete_med(login: str, med_name: str) -> NamedTuple:
    """Delete row with this med for this user
    
    Returns NamedTuple (f_column_=True) on success"""
    with open(f"{QUERY_PATH}/delete_med.sql", 'r') as f:
        query = f.read().replace('\n', ' ')
    result = postgres_request(query, {"login": login, "med_name": med_name})
    if result: return result[0]
    return ()

def get_med(login: str, med_name: str) -> NamedTuple:
    """Returns NamedTuple with med_name for login
    
    NamedTuple conatins: user_login, med_name, amount, daily_usage, last_count_date
    """
    with open(f"{QUERY_PATH}/get_med.sql", 'r') as f:
        query = f.read().replace('\n', ' ')
    result = postgres_request(query, {"login": login, "med_name": med_name})
    if result: return result[0]
    return ()


#table = get_user_meds("test")
#result = {}
#for med in table:
#    result[med.med_name] = {"count": med.amount, "pills_use": med.daily_usage, "date": f"{med.last_count_date}"}
#table = get_user_meds("test2")
#for line in table:
#    print(line)
#print(result)
#if not table: print("Empty")

atexit.register(close_connection, conn=connection)