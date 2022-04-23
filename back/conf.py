from os import environ as env
from dotenv import load_dotenv


load_dotenv()


def database(**kwargs):
    return {
        'host': env.get('HOST'),
        'user': env.get('ITEAMS_DB_USER'),
        'password': env.get('ITEAMS_DB_PASSWORD'),
        'database': 'HIU',
        'charset': 'utf8mb4'
    }
