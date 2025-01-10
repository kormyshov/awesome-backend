import boto3
from boto3.dynamodb.conditions import Key
from pickle import dumps, loads

from config import Config

from user_orm import UserORM
from abstract_base import AbstractBase, UserDoesntExistInDB


class Database(AbstractBase):
    def __init__(self):
        self.dynamodb = boto3.resource(
            'dynamodb',
            endpoint_url=Config.USER_STORAGE_URL,
            region_name='ru-central1',
            aws_access_key_id=Config.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=Config.AWS_SECRET_ACCESS_KEY,
        )

    def get_user_info(self, user_id: str) -> UserORM:
        table_users = self.dynamodb.Table('users')
        response = table_users.get_item(Key={'id': {'S': user_id}})

        if 'Item' not in response:
            raise UserDoesntExistInDB

        orm = UserORM(
            id=user_id,
            tasks=loads(bytes(response['Item'].get('tasks', dumps([])))),
            projects=loads(bytes(response['Item'].get('projects', dumps([])))),
        )
        return orm

    def set_user_info(self, user: UserORM) -> None:
        table_users = self.dynamodb.Table('users')
        item = {
            'id': user.id,
            'tasks': dumps(user.tasks),
            'projects': dumps(user.projects),
        }
        table_users.put_item(Item=item)

    def create_tables(self) -> None:
        self.dynamodb.create_table(
            TableName='users',
            KeySchema=[
                {
                    'AttributeName': 'id',
                    'KeyType': 'HASH',
                },
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'id',
                    'AttributeType': 'S',
                },
            ],
        )
