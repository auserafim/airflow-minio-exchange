import os
from pathlib import Path

from minio import Minio

if __name__ == "__main__":
    print("I got called!")

    client = Minio(
        "minio:9000",
        access_key="minadmin",
        secret_key="minadmin",
        secure=False,
    )

    BUCKET = "superclient"
    TEMP_FOLDER_PATH = "/app/tmp"
    try:
        client.fget_object(BUCKET, "validated/validated.parquet", "/tmp/raw.csv")

        if not os.path.exists(TEMP_FOLDER_PATH):
            os.makedirs(TEMP_FOLDER_PATH)

        full_path_clean = os.path.join(TEMP_FOLDER_PATH, "cleaned.parquet")

        with open(full_path_clean, "w") as filename:
            pass

        client.fput_object(
            BUCKET, "cleaned/cleaned.parquet", f"{TEMP_FOLDER_PATH}/cleaned.parquet"
        )
        client.fput_object(
            BUCKET,
            "cleaned/cleaned.parquet",
            f"{TEMP_FOLDER_PATH}/cleaned.parquet",
        )
    except Exception as e:
        raise e
