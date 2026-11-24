import os
from dotenv import load_dotenv

from pathlib import Path

from azure.core.exceptions import ResourceExistsError
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient

load_dotenv()

ACCOUNT_URL = os.environ["AZURE_STORAGE_ACCOUNT_URL"]
CONTAINER = "raw"
RAW_DIR = Path("data/raw")


def main():
    service = BlobServiceClient(ACCOUNT_URL, credential=DefaultAzureCredential())
    container = service.get_container_client(CONTAINER)

    uploaded = 0
    skipped = 0

    for path in sorted(RAW_DIR.rglob("*.json")):
        blob_name = path.relative_to(RAW_DIR).as_posix()
        with open(path, "rb") as f:
            try:
                container.upload_blob(blob_name, f, overwrite=False)
                uploaded += 1
            except ResourceExistsError:
                skipped += 1

    print(f"uploaded {uploaded}, skipped {skipped}")


if __name__ == "__main__":
    main()