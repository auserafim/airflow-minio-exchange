from pathlib import Path

from validation_sellin import split_issues, validate_csv


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
