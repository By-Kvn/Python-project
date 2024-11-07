import json
import os
import boto3
import uuid
from http import HTTPStatus
from requests import HTTPError
from functools import wraps

def exception_handler(func):
    @wraps(func)
    def wrapper(event, context):
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

@exception_handler
def handler(event, context):
    print("Début de la fonction Lambda")
    print("Event reçu :", event)

    # Ici je recup l'email depuis le body de la requête
    try:
        body = json.loads(event.get('body', '{}'))
        email = body.get('email')
        if not email:
            raise ValueError("L'email est requis et ne peut pas être vide.")
    except Exception as e:
        print(f"Erreur lors de l'extraction du body: {str(e)}")
        return {
            'statusCode': HTTPStatus.BAD_REQUEST,
            'body': json.dumps({'message': 'Invalid request body or missing email'})
        }

    # ici je recup le nom de la table DynamoDB depuis les variables d'environnement
    user_table_name = os.environ.get('STORAGE_USERS_NAME')
    if not user_table_name:
        print("Erreur : Nom de la table non défini dans les variables d'environnement")
        return {
            'statusCode': HTTPStatus.INTERNAL_SERVER_ERROR,
            'body': json.dumps({'message': 'Table name not set in environment variables'})
        }

    # Ma Connexion à DynamoDB
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(user_table_name)

    # La recherche de l'utilisateur dans DynamoDB
    res = table.query(
        IndexName='emails',
        KeyConditionExpression=boto3.dynamodb.conditions.Key('email').eq(email)
    )

    user_id = None
    if res['Items']:  # Si un utilisateur est trouvé
        user_id = res['Items'][0].get('id')
    else:  # Si aucun utilisateur n'est trouvé, je crée un nouveau
        user_id = str(uuid.uuid4())
        table.put_item(Item={'id': user_id, 'email': email})

    # Retourner l'ID de l'utilisateur
    return {
        'statusCode': HTTPStatus.OK,
        'body': json.dumps({'id': user_id})
    }
