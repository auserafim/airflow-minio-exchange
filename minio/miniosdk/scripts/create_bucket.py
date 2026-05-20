import time
from mimetypes import suffix_map
from sys import prefix

from minio.error import S3Error
from minio.notificationconfig import FilterRule, NotificationConfig, QueueConfig
from typing_extensions import Any

from minio import Minio

DATA_PATH = "../data"
RAW = f"{DATA_PATH}/raw"
PROCESSED = f"{DATA_PATH}/processed"


def add_event_to_bucket(
    bucket: str,
    client: Any,
) -> None:
    config = NotificationConfig(
        queue_config_list=[
            QueueConfig(
                queue="arn:minio:sqs::primary:webhook",
                events=["s3:ObjectCreated:Put"],
            )
        ]
    )

    client.set_bucket_notification(bucket, config)


if __name__ == "__main__":
    try:
        client = Minio(
            "minio:9000", access_key="minadmin", secret_key="minadmin", secure=False
        )
        bucketList = ["processed", "raw"]
        destinationFiles = ["processed.csv", "raw.csv"]
        sourceFiles = [f"{PROCESSED}/processed.csv", f"{RAW}/raw.csv"]

        for b, d, f in zip(bucketList, destinationFiles, sourceFiles):
            if not client.bucket_exists(b):
                client.make_bucket(b)
                client.fput_object(b, d, f)
                print(f"Bucket created : {b}\nFile: {f} written to it.")
                continue
            print(f"Bucket {b} arealdy existed!")

        # adding events to the bucket
        try:
            for c in bucketList:
                add_event_to_bucket(c, client)
        except Exception as e:
            raise RuntimeError(
                "Could not add event to bucket Error",
            ) from e
    except S3Error as exc:
        print("error occured:", exc)
