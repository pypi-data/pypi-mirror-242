import boto3
from dotenv import load_dotenv
from rich import print

import os

REG_FORM_QUEUE_NAME = "md410-2024-conv.fifo"
REG_FORM_QUEUE_URL = (
    "https://sqs.af-south-1.amazonaws.com/960171457841/md410-2024-conv.fifo"
)


load_dotenv()

SESSION = boto3.Session(
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
)
SQS = SESSION.resource(
    "sqs",
    region_name="af-south-1",
)
REG_FORM_QUEUE = SQS.Queue(REG_FORM_QUEUE_URL)


def send_data(data: str, msg_id: str):
    response = REG_FORM_QUEUE.send_message(
        MessageBody=data,
        MessageGroupId=msg_id,
    )


def read_data(max_number_of_messages=1, timeout=5, delete=True):
    results = REG_FORM_QUEUE.receive_messages(
        AttributeNames=["All"],
        MaxNumberOfMessages=max_number_of_messages,
        WaitTimeSeconds=timeout,
    )
    if delete:
        [r.delete() for r in results]
    return [(r.attributes.get("MessageGroupId"), r.body) for r in results]


if __name__ == "__main__":
    import json

    # send_data(json.dumps({"a": "b"}, "reg_form"))
    res = read_data(max_number_of_messages=10, delete=False)
    for r in res:
        print(r)
