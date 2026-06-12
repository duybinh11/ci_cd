#!/usr/bin/env python3
import os
import sys
from datetime import datetime, timezone

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

SCOPES = ["https://www.googleapis.com/auth/drive.file"]


def main() -> None:
    client_id = os.environ.get("GOOGLE_DRIVE_CLIENT_ID")
    client_secret = os.environ.get("GOOGLE_DRIVE_CLIENT_SECRET")
    refresh_token = os.environ.get("GOOGLE_DRIVE_REFRESH_TOKEN")
    folder_id = os.environ.get("DRIVE_FOLDER_ID")
    apk_path = os.environ.get("APK_PATH", "app/build/outputs/apk/release/app-release.apk")

    missing = [
        name
        for name, value in [
            ("GOOGLE_DRIVE_CLIENT_ID", client_id),
            ("GOOGLE_DRIVE_CLIENT_SECRET", client_secret),
            ("GOOGLE_DRIVE_REFRESH_TOKEN", refresh_token),
            ("DRIVE_FOLDER_ID", folder_id),
        ]
        if not value
    ]
    if missing:
        print(f"Missing required environment variables: {', '.join(missing)}", file=sys.stderr)
        sys.exit(1)
    if not os.path.isfile(apk_path):
        print(f"APK not found: {apk_path}", file=sys.stderr)
        sys.exit(1)

    sha = os.environ.get("GITHUB_SHA", "local")[:7]
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    file_name = f"app-release-{sha}-{timestamp}.apk"

    credentials = Credentials(
        token=None,
        refresh_token=refresh_token,
        token_uri="https://oauth2.googleapis.com/token",
        client_id=client_id,
        client_secret=client_secret,
        scopes=SCOPES,
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
