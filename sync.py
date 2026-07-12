"""
sync.py
Automatically detects new, modified and deleted documents.
"""

import os
import json
import hashlib

from config import (
    DOCUMENT_FOLDER,
    MANIFEST_FILE,
)


class FileSynchronizer:

    def __init__(self):
        self.manifest = self.load_manifest()

    # -------------------------------------------------
    # Load manifest
    # -------------------------------------------------

    def load_manifest(self):

        if os.path.exists(MANIFEST_FILE):
            with open(MANIFEST_FILE, "r") as f:
                return json.load(f)

        return {}

    # -------------------------------------------------
    # Save manifest
    # -------------------------------------------------

    def save_manifest(self):

        with open(MANIFEST_FILE, "w") as f:
            json.dump(self.manifest, f, indent=4)

    # -------------------------------------------------
    # SHA256 Hash
    # -------------------------------------------------

    def file_hash(self, filepath):

        sha = hashlib.sha256()

        with open(filepath, "rb") as f:

            while True:

                chunk = f.read(8192)

                if not chunk:
                    break

                sha.update(chunk)

        return sha.hexdigest()

    # -------------------------------------------------
    # Scan folder
    # -------------------------------------------------

    def scan_documents(self):

        current = {}

        for root, _, files in os.walk(DOCUMENT_FOLDER):

            for file in files:

                path = os.path.join(root, file)

                current[path] = {
                    "hash": self.file_hash(path),
                    "modified": os.path.getmtime(path)
                }

        return current

    # -------------------------------------------------
    # Compare
    # -------------------------------------------------

    def compare(self):

        current = self.scan_documents()

        new_files = []
        modified_files = []
        deleted_files = []

        # New / Modified
        for path, data in current.items():

            if path not in self.manifest:

                new_files.append(path)

            elif self.manifest[path]["hash"] != data["hash"]:

                modified_files.append(path)

        # Deleted
        for path in self.manifest:

            if path not in current:

                deleted_files.append(path)

        return (
            new_files,
            modified_files,
            deleted_files,
            current
        )

    # -------------------------------------------------
    # Update Manifest
    # -------------------------------------------------

    def update(self, current):

        self.manifest = current

        self.save_manifest()

    # -------------------------------------------------
    # Check changes
    # -------------------------------------------------

    def changes_detected(self):

        (
            new_files,
            modified_files,
            deleted_files,
            current
        ) = self.compare()

        if new_files:

            print("\n🟢 New files")

            for file in new_files:
                print(" +", os.path.basename(file))

        if modified_files:

            print("\n🟡 Modified files")

            for file in modified_files:
                print(" *", os.path.basename(file))

        if deleted_files:

            print("\n🔴 Deleted files")

            for file in deleted_files:
                print(" -", os.path.basename(file))

        changed = (
            len(new_files)
            or len(modified_files)
            or len(deleted_files)
        )

        if changed:

            self.update(current)

        return changed