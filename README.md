# big-finish

The purpose of this is to scan Big Finish website for Audio Books you own to create the metadata in compatible JSON files for use in Audiobookshelf. It is work in progress. 

I have used the version provided by https://github.com/valdearg/big-finish and modified it to use Edge Chronium on Windows 11. I have also fixed some minor issues like Narrators not pulling all narrators into the JSON. 

## Requirments
Windows Using Edge

These were the files I installed not all may be needed.

winget install python3
winget install selenium
winget install pip
pip install -U selenium
pip install webdriver_manager
pip install bs4
pip install xmltodict
pip install fake_useragent==1.1.3
pip install numpy
pip install tqdm
pip install selenium webdriver-manager msedge-selenium-tools 
pip install --upgrade selenium 
pip install --upgrade webdriver-manager 
pip install pandas  

## Commands
### Inital Scan

python main.py --scan https://bigfinish.com

### Single URL for Episode Updates

python main.py --url https://www.bigfinish.com/releases/v/torchwood-torchwood-one-i-hate-mondays-2984 --overwrite

### Compile CSV

python compile_csv.py

### Move Files

python search_csv.py

## To Do
- [ ] Create Docker/Linux version
- [ ] Migrate script to PowerShell
- [ ] Improve moving files and renaming. 
- [X] Improve Series name generation into more logical format. 
