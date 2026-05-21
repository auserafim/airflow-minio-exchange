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
        client.fget_object(BUCKET, "curated/curated.parquet", "/tmp/curated.parquet")

        if not os.path.exists(TEMP_FOLDER_PATH):
            os.makedirs(TEMP_FOLDER_PATH)

        full_path_clean = os.path.join(TEMP_FOLDER_PATH, "analytics.parquet")

        with open(full_path_clean, "w") as filename:
            pass

        client.fput_object(
            BUCKET,
            "analytics/analytics.parquet",
            f"{TEMP_FOLDER_PATH}/analytics.parquet",
        )
    except Exception as e:
        raise e
