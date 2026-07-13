# Python_Automation_Week_09
Using Python for Automation:
1.File Organizer Write a script that automatically sorts files in a directory into subfolders based on type(e.g., .pdf,.jpg,.csv)
2.Watcher Monitor a folder for new files and automatically move them to a backup location.
3.Web Scraper Automate fetching headlines from a news site saving them into a text file.
4.Create an API caller that retrives customer data from a public API, flatters it using pandas, and stores the results in excel or csv files.
5.System Monitor Create a script that logs CPU and memory usage every minutes into a file.

Note: Publish the scripts for each task in a separate folder named along with snapshots of the execution results. Also ensure that the prompts used for each exercise are published in a text file.
Python_Automation_Week_09/
├── requirements.txt
├── Task_01_File_Organizer/
│   ├── problem_statement.txt
│   ├── prompts.txt
│   ├── file_organizer.py         ✅ sorts 22 files into 8 category folders
│   ├── create_test_files.py      ✅ generates dummy test files
│   └── test_files/               (organized subfolders created at runtime)
├── Task_02_Watcher/
│   ├── problem_statement.txt
│   ├── prompts.txt
│   ├── watcher.py                ✅ real-time backup via watchdog
│   ├── watch_folder/
│   └── backup_folder/
├── Task_03_Web_Scraper/
│   ├── problem_statement.txt
│   ├── prompts.txt
│   ├── web_scraper.py            ✅ fetched 20 BBC headlines → headlines.txt
│   └── headlines.txt
├── Task_04_API_Caller/
│   ├── problem_statement.txt
│   ├── prompts.txt
│   ├── api_caller.py             ✅ 10 customers, 15 flat columns → CSV + Excel
│   └── output/customers_*.csv/xlsx
└── Task_05_System_Monitor/
    ├── problem_statement.txt
    ├── prompts.txt
    ├── system_monitor.py         ✅ logs CPU/RAM/Disk every N seconds
    └── logs/system_monitor.log

    --------------------------------------------------------
    # Install once
python -m pip install -r requirements.txt

# Task 1 — generate test files then organize them
python Task_01_File_Organizer/create_test_files.py
python Task_01_File_Organizer/file_organizer.py

# Task 2 — start watcher, then drop files into watch_folder/
python Task_02_Watcher/watcher.py

# Task 3 — scrape BBC headlines
python Task_03_Web_Scraper/web_scraper.py

# Task 4 — fetch & flatten API data to CSV/Excel
python Task_04_API_Caller/api_caller.py

# Task 5 — monitor system (default 60s; pass seconds as arg)
python Task_05_System_Monitor/system_monitor.py 60