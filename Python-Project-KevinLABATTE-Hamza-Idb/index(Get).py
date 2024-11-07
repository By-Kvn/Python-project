import json
import os
import boto3
from http import HTTPStatus
from functools import wraps
from requests import HTTPError

def exception_handler(func):
    @wraps(func)
    def wrapper(event, context):
        print(event)
        response = {}
        try:
            res = func(event, context)
            if res:
                response['body'] = json.dumps(res)
            response['statusCode'] = HTTPStatus.OK
        except HTTPError as error:
            response['statusCode'] = error.response.status_code
        except Exception as error:
            response['statusCode'] = HTTPStatus.INTERNAL_SERVER_ERROR
            response['body'] = json.dumps({'message': str(error)})
        return response
    return wrapper

# Fonction Lambda pour rechercher un utilisateur par ID
@exception_handler
def handler(event, context):
    print("Début de la fonction Lambda")
    print("Event reçu :", event)

    # ici je recup le nom de la table DynamoDB depuis les variables d'environnement
    user_table_name = os.environ.get('STORAGE_USERS_NAME')
    if not user_table_name:
        print("Erreur : Nom de la table non défini dans les variables d'environnement")
        return {
            'statusCode': HTTPStatus.INTERNAL_SERVER_ERROR,
            'body': json.dumps({'message': 'Table name not set in environment variables'})
        }

    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(user_table_name)

    user_id = event['headers'].get('x-api-key')
    if not user_id:
        print("Erreur : ID utilisateur non fourni dans les headers")
        return {
            'statusCode': HTTPStatus.BAD_REQUEST,
            'body': json.dumps({'message': 'User ID not provided'})
        }

    # je check l'existence de l'utilisateur par son ID
    try:
        print("Vérification de l'utilisateur dans DynamoDB")
        res = table.get_item(Key={'id': user_id})
        data = res.get('Item')
        if not data:
            print("Utilisateur non trouvé avec l'ID fourni")
            return {
                'statusCode': HTTPStatus.NOT_FOUND,
                'body': json.dumps({'message': 'User not found'})
            }
    except Exception as e:
        print("Erreur lors de l'accès à DynamoDB :", str(e))
        return {
            'statusCode': HTTPStatus.INTERNAL_SERVER_ERROR,
            'body': json.dumps({'message': f'Error accessing DynamoDB: {str(e)}'})
        }

    # Si l'utilisateur est trouvé, je retourne son email
    return {'email': data['email']}
