#!/usr/bin/env python3
import os
import sys
from datetime import datetime, timezone

from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

SCOPES = ["https://www.googleapis.com/auth/drive.file"]


def main() -> None:
    credentials_path = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
    folder_id = os.environ.get("DRIVE_FOLDER_ID")
    apk_path = os.environ.get("APK_PATH", "app/build/outputs/apk/release/app-release.apk")

    if not credentials_path:
        print("GOOGLE_APPLICATION_CREDENTIALS is not set", file=sys.stderr)
        sys.exit(1)
    if not folder_id:
        print("DRIVE_FOLDER_ID is not set", file=sys.stderr)
        sys.exit(1)
    if not os.path.isfile(apk_path):
        print(f"APK not found: {apk_path}", file=sys.stderr)
        sys.exit(1)

    sha = os.environ.get("GITHUB_SHA", "local")[:7]
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    file_name = f"app-release-{sha}-{timestamp}.apk"

    credentials = service_account.Credentials.from_service_account_file(
        credentials_path, scopes=SCOPES
    )
    drive = build("drive", "v3", credentials=credentials)

    file_metadata = {
        "name": file_name,
        "parents": [folder_id],
    }
    media = MediaFileUpload(
        apk_path,
        mimetype="application/vnd.android.package-archive",
        resumable=True,
    )

    uploaded = (
        drive.files()
        .create(
            body=file_metadata,
            media_body=media,
            fields="id,name,webViewLink",
            supportsAllDrives=True,
        )
        .execute()
    )

    print(f"Uploaded {uploaded['name']} (id: {uploaded['id']})")
    print(f"Link: {uploaded.get('webViewLink', 'N/A')}")


if __name__ == "__main__":
    main()
