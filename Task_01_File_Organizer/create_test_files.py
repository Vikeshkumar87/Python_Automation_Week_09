"""
create_test_files.py
--------------------
Generates dummy sample files with various extensions inside ./test_files/
so that file_organizer.py can be demonstrated immediately.

Usage:
    python create_test_files.py
"""

import os

# Target directory
TEST_DIR = os.path.join(os.path.dirname(__file__), "test_files")

# (filename, content) pairs covering all organizer categories
SAMPLE_FILES = [
    # Images
    ("photo_vacation.jpg",      "DUMMY JPEG IMAGE DATA"),
    ("logo_company.png",        "DUMMY PNG IMAGE DATA"),
    ("banner.gif",              "DUMMY GIF IMAGE DATA"),
    # Documents
    ("annual_report.pdf",       "DUMMY PDF DOCUMENT"),
    ("meeting_notes.docx",      "DUMMY WORD DOCUMENT"),
    ("readme.txt",              "This is a plain text readme file."),
    ("slides.pptx",             "DUMMY POWERPOINT FILE"),
    # Data
    ("sales_data.csv",          "id,name,amount\n1,Alice,500\n2,Bob,750"),
    ("config.json",             '{"debug": true, "version": "1.0"}'),
    ("users.xml",               "<users><user id='1'>Alice</user></users>"),
    ("report.xlsx",             "DUMMY EXCEL FILE"),
    # Videos
    ("tutorial.mp4",            "DUMMY MP4 VIDEO DATA"),
    ("clip.avi",                "DUMMY AVI VIDEO DATA"),
    # Audio
    ("podcast_ep1.mp3",         "DUMMY MP3 AUDIO DATA"),
    ("theme_music.wav",         "DUMMY WAV AUDIO DATA"),
    # Archives
    ("project_backup.zip",      "DUMMY ZIP ARCHIVE"),
    ("source_code.tar",         "DUMMY TAR ARCHIVE"),
    # Code
    ("app.js",                  "console.log('Hello, World!');"),
    ("index.html",              "<!DOCTYPE html><html><body>Hi</body></html>"),
    ("styles.css",              "body { margin: 0; padding: 0; }"),
    # Others (unknown extension)
    ("mystery_file.xyz",        "UNKNOWN FILE TYPE"),
    ("raw_data.dat",            "BINARY-LIKE RAW DATA"),
]


def create_test_files():
    os.makedirs(TEST_DIR, exist_ok=True)
    created = 0
    for filename, content in SAMPLE_FILES:
        filepath = os.path.join(TEST_DIR, filename)
        if not os.path.exists(filepath):
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"  Created: {filename}")
            created += 1
        else:
            print(f"  Skipped (already exists): {filename}")

    print(f"\n{created} test file(s) created in: {TEST_DIR}")
    print("Now run  python file_organizer.py  to organize them.\n")


if __name__ == "__main__":
    create_test_files()
