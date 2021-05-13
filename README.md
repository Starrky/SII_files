# SII_files
 
When you run main.py file script will check if file exists on Spanish PC, create info with bot on MS Teams channel and create ticket if needed. (Please check if you have access to PC's C drive before)

# Installation

**In order to use this tool, you need to install python3 and chrome browser and keep it updated**: https://www.python.org/downloads/ and choose newest version of the installers for your OS**(select "Add to path" checkbox during installation)**.

![alt text](https://i.imgur.com/06EspWQ.png)

You have two options:
A) Use virtual environment, in project folder:

Create and activate venv:
```
python -m venv c:\path\to\myenv
c:\path\to\myenv\Scripts\activate.bat
```
Then install requirements
```
pip install -r requirements.txt
```

B) Use global environment and just install requirements:
```
python -m venv c:\path\to\myenv
c:\path\to\myenv\Scripts\activate.bat
```

Then install requirements
```
CD into folder with main.py script
pip install -r requirements.txt
```

# Usage
Run main.py by opening CMD in the folder with script, then type in: 
```
python main.py
```
Results should be shown in CMD and on MS Teams channel ( can't connect to PC/ No file/ File found)
