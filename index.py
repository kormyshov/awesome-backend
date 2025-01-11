import base64
from utils import (
    validate_telegram_data,
    validate_init_db,
)
from database import Database
from user import User


def handler(event, context):
    db = Database()

    print(event)
    print(context)

    # if event['httpMethod'] == 'GET' and event['headers']['Origin'] == 'https://awesome-index.website.yandexcloud.net':
    if event['httpMethod'] == 'GET' or event['httpMethod'] == 'POST':
        if event['queryStringParameters']['method'] == 'init_db' and validate_init_db(event['queryStringParameters']['user']):
            db.create_tables()

        if event['queryStringParameters']['user'] == 'test' or validate_telegram_data(event['queryStringParameters'].get('validate', '')):
            user = User(event['queryStringParameters']['user'], db)
            if event['queryStringParameters']['method'] == 'get_tasks':
                return {
                    'statusCode': 200,
                    'body': '''
                        {
                            "projects": ''' + user.get_projects_str() + ''', 
                            "tasks": ''' + user.get_tasks_str() + '''
                        }
                    ''',
                }

            if event['queryStringParameters']['method'] == 'set_tasks':
                user.set_tasks_str(base64.b64decode(event['body']).decode("utf-8"))
                # print(user.get_tasks_str())
                user.save()

            if event['queryStringParameters']['method'] == 'set_projects':
                user.set_projects_str(base64.b64decode(event['body']).decode("utf-8"))
                user.save()

    return {
        'statusCode': 200,
        'body': '{"projects": [], "tasks": []}',
    }
