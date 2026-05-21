import os
from pathlib import Path

from validation_sellin import split_issues, validate_csv

from minio import Minio


def validate_source_file(file_path: str | Path) -> None:
    issues = validate_csv(file_path)
    errors, warnings = split_issues(issues)

    if errors:
        grouped = "\n".join(
            f"- linha {issue.row_number}: {issue.code} ({issue.field})"
            for issue in errors[:20]
        )
        raise ValueError(f"Arquivo reprovado na validação:\n{grouped}")

    if warnings:
        print(f"[WARN] arquivo validado com {len(warnings)} warning(s).")


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
        client.fget_object(BUCKET, "raw/raw.parquet", "/tmp/raw.parquet")

        if not os.path.exists(TEMP_FOLDER_PATH):
            os.makedirs(TEMP_FOLDER_PATH)

        full_path_validated = os.path.join(TEMP_FOLDER_PATH, "validated.parquet")
        full_path_quality = os.path.join(TEMP_FOLDER_PATH, "report_quality.json")

        with open(full_path_validated, "w") as filename:
            pass
        with open(full_path_quality, "w") as filename:
            pass

        client.fput_object(
            BUCKET,
            "validated/validated.parquet",
            f"{TEMP_FOLDER_PATH}/validated.parquet",
        )
        client.fput_object(
            BUCKET,
            "quality/report_quality.json",
            f"{TEMP_FOLDER_PATH}/report_quality.json",
        )
    except Exception as e:
        raise e
