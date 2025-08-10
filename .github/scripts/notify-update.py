import boto3
import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import messaging

bucket_name = "wicked-woods-notifications"
creds_file = "ome-push-notifications-firebase-adminsdk-fbsvc-e58bb1d562.json"

def get_creds_file():
    s3_client = boto3.client("s3")
    s3_client.download_file(bucket_name, creds_file, "creds.json")

def send_notification():
    
    cred = credentials.Certificate("creds.json")
    firebase_admin.initialize_app(cred)
    message = messaging.Message(
        data={
            'updated': "true",
        },
        topic="data-updates",
    )
    
    # send message
    response = messaging.send(message)
                      

get_creds_file()
send_notification()
print("script has run")