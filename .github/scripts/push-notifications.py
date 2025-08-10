import boto3
import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import messaging

bucket_name = "wicked-woods-notifications"
event_name = 2025
notifications_directory = "2025/communications"
creds_file = "ome-push-notifications-firebase-adminsdk-fbsvc-e58bb1d562.json"

def get_creds_file():
    s3_client = boto3.client("s3")
    s3_client.download_file(bucket_name, creds_file, "creds.json")

def send_notification(filename, channel_info_file):

    # get topic name
    with open(channel_info_file, 'r', encoding='utf-8') as f:
            for line in f:
                if "firebaseTopicName:" in line:
                    firebase_topic_name = line.split("firebaseTopicName: ")[1].replace('"','').strip()
    
    # get title
    with open(filename, 'r', encoding='utf-8') as f:
            for line in f:
                if "title:" in line:
                    title = line.split("title: ")[1].strip()

    # get body
    with open(filename, 'r', encoding='utf-8') as f:
            delineator_count = 0
            body = ""
            for line in f:
                 if line.strip() == "---":
                      delineator_count += 1
                 elif delineator_count >= 2:
                      body += line

    # get channel
    channel_name = filename.split("/")[-2]

    # get post_stub
    post_stub = filename.replace("\\","/").split("/")[-1].replace(".md","")
    
    cred = credentials.Certificate("creds.json")
    firebase_admin.initialize_app(cred)
    message = messaging.Message(
        notification=messaging.Notification(
            title=title,
            body=body,
        ),
        data={
            'event': event_name,
            'channel': channel_name,
            'post-stub': post_stub,
        },
        topic=firebase_topic_name,
    )
    
    # send message
    # response = messaging.send(message)
                      


def get_pending_notifications():

    pending_notifications = []

    # get list of items in bucket
    sent_notifications = []
    s3_client = boto3.client("s3")
    paginator = s3_client.get_paginator("list_objects_v2")

    kwargs = {"Bucket": bucket_name}
    
    for page in paginator.paginate(**kwargs):
        # Check if the page has 'Contents' (it might be empty)
        if "Contents" in page:
            for obj in page["Contents"]:
                sent_notifications.append(obj["Key"])

    # loop communications files
    for subdir, dirs, files in os.walk(notifications_directory):
        for file in files:
            filename = os.path.join(subdir, file)
            object_name = filename.split(notifications_directory)[1]
            object_name = object_name.replace("\\","/")
            
            # check if files exist in s3
            if object_name not in sent_notifications:
                # filter out channel-info
                if "channel-info.yaml" not in object_name:
                    # check if "sendPush: true" in file
                    send = False
                    with open(filename, 'r', encoding='utf-8') as f:
                        for line in f:
                             if "sendPush: true" in line:
                                  send = True
                                  break
                    if send:
                        # get channel-info
                        channel = object_name.split("/")[1]
                        channel_info_file = notifications_directory + "/" + channel + "/channel-info.yaml"
                        
                        print("sending " + object_name)
                        send_notification(filename, channel_info_file)

                # upload key to s3
                s3_client.upload_file(filename, bucket_name, object_name)

get_creds_file()
get_pending_notifications()
print("script has run")