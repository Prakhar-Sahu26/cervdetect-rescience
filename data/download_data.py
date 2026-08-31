"""
Download and verify the UCI Cervical Cancer (Risk Factors) dataset.

Usage:
    python data/download_data.py

The file risk_factors_cervical_cancer.csv will be written to data/.
The dataset is publicly available from the UCI Machine Learning Repository
and is not redistributed with this code.
"""

import hashlib
import os
import sys
import urllib.request

DATA_DIR = os.path.dirname(os.path.abspath(__file__))
FILENAME = "risk_factors_cervical_cancer.csv"
DEST = os.path.join(DATA_DIR, FILENAME)

# Direct download URL (UCI ML Repository)
URL = (
    "https://archive.ics.uci.edu/static/public/383/"
    "cervical+cancer+risk+factors.zip"
)

# SHA-256 of the CSV file as distributed by UCI (verify after extraction)
# Run: python -c "import hashlib; print(hashlib.sha256(open('risk_factors_cervical_cancer.csv','rb').read()).hexdigest())"
# on a fresh download and fill this in if you want checksum verification.
EXPECTED_SHA256 = "8df193ad5c9ff4288fb4c401eef70dcd2cbda404ce7f82ac74c68cfc960ab063"


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def download_zip():
    import io
    import zipfile

    print(f"Downloading dataset from UCI ML Repository...")
    with urllib.request.urlopen(URL) as response:
        data = response.read()

    zf = zipfile.ZipFile(io.BytesIO(data))
    csv_name = next(n for n in zf.namelist() if n.endswith(".csv"))
    with zf.open(csv_name) as src, open(DEST, "wb") as dst:
        dst.write(src.read())
    print(f"Saved to {DEST}")


def main():
    if os.path.exists(DEST):
        print(f"File already exists: {DEST}")
    else:
        download_zip()

    if EXPECTED_SHA256:
        actual = sha256(DEST)
        if actual != EXPECTED_SHA256:
            print(f"ERROR: SHA-256 mismatch.")
            print(f"  Expected: {EXPECTED_SHA256}")
            print(f"  Got:      {actual}")
            sys.exit(1)
        print("Checksum OK.")
    else:
        print(f"SHA-256: {sha256(DEST)}")
        print("(Set EXPECTED_SHA256 in this script to enable future verification.)")


if __name__ == "__main__":
    main()
