from utils import (
    validate_telegram_data,
    validate_init_db,
)
from database import Database


def handler(event, context):
    db = Database()

    print(event)
    print(context)

    # if event['httpMethod'] == 'GET' and event['headers']['Origin'] == 'https://awesome-index.website.yandexcloud.net':
    if event['httpMethod'] == 'GET':
        if event['queryStringParameters']['method'] == 'init_db' and validate_init_db(event['queryStringParameters']['user']):
            db.create_tables()

        if event['queryStringParameters']['user'] == 'test' or validate_telegram_data(event['queryStringParameters'].get('validate', '')):
            if event['queryStringParameters']['method'] == 'get_tasks':
                return {
                    'statusCode': 200,
                    'body': '''
                        {
                            "projects": [{"id": "1", "projectName": "Написать таск-менеджер", "projectDescription": "Не отвлекайся", "projectStatus": "ACTIVE"}], 
                            "tasks": [
                                {"id": "2", "taskName": "Сделать бэк", "taskDescription": "Нормальный, а не то, что сейчас", "isChecked": false, "taskStatus": ""}
                            ]
                        }
                    ''',
                }

    return {
        'statusCode': 200,
        'body': '{"projects": [], "tasks": []}',
    }
