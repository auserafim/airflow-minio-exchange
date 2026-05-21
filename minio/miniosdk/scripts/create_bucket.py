import os
import time
from mimetypes import suffix_map
from sys import prefix

from minio.error import S3Error
from minio.notificationconfig import NotificationConfig, PrefixFilterRule, QueueConfig
from typing_extensions import Any

from minio import Minio

DATA_PATH = "/app/data"


def add_event_to_bucket(
    bucket: str,
    client: Any,
) -> None:
    config = NotificationConfig(
        queue_config_list=[
            QueueConfig(
                queue="arn:minio:sqs::primary:webhook",
                events=[
                    "s3:ObjectCreated:*",
                ],
                # only triggers new data at raw, not every change in the whole bucket
                prefix_filter_rule=PrefixFilterRule("raw/"),
            )
        ]
    )

    client.set_bucket_notification(bucket, config)


if __name__ == "__main__":
    try:
        client = Minio(
            "minio:9000", access_key="minadmin", secret_key="minadmin", secure=False
        )
        bucketList = ["superclient"]
        foldersToCreate = [
            "raw",
            "validated",
            "quality",
            "cleaned",
            "curated",
            "analytics",
        ]

        for b in bucketList:
            if not client.bucket_exists(b):
                client.make_bucket(b)
                for f in foldersToCreate:
                    folder_path = f"{DATA_PATH}/{f}/"
                    if not os.path.exists(folder_path):
                        os.makedirs(folder_path)

                    full_path = os.path.join(folder_path, ".minioignore")
                    with open(full_path, "w") as filename:
                        # filename.write("1")
                        pass

                    client.fput_object(
                        b,
                        f"{f}/.minioignore",
                        f"{DATA_PATH}/{f}/.minioignore",
                    )
        try:
            for c in bucketList:
                add_event_to_bucket(c, client)
        except Exception as e:
            raise RuntimeError(
                "Could not add event to bucket Error",
            ) from e

    except S3Error as exc:
        print("error occured:", exc)

# if __name__ == "__main__":
#     try:
#         client = Minio(
#             "minio:9000", access_key="minadmin", secret_key="minadmin", secure=False
#         )
#         bucketList = ["processed", "raw"]
#         destinationFiles = ["processed.csv", "raw.csv"]
#         sourceFiles = [f"{PROCESSED}/processed.csv", f"{RAW}/raw.csv"]

#         for b, d, f in zip(bucketList, destinationFiles, sourceFiles):
#             if not client.bucket_exists(b):
#                 client.make_bucket(b)
#                 client.fput_object(b, d, f)
#                 print(f"Bucket created : {b}\nFile: {f} written to it.")
#                 continue
#             print(f"Bucket {b} arealdy existed!")

#         # adding events to the bucket
#         try:
#             for c in bucketList:
#                 add_event_to_bucket(c, client)
#         except Exception as e:
#             raise RuntimeError(
#                 "Could not add event to bucket Error",
#             ) from e

#     except S3Error as exc:
#         print("error occured:", exc)
