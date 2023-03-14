Startups webscraper
==

# Install
## Requirements
### Python version
known to work with python versions:
* Python 3.9

### Playwright
documentation:
https://playwright.dev/python/docs/intro

follow these commands:

* First install requirements.txt with "playwright" in it
* Then in command line

```
pip install pytest-playwright
```

```
playwright install
```

### Other requirements

install other requirements from requirements.txt file using command line:

```
pip install -r requirements.txt
```
# Use app from command line
from root folder
## scrap data
on Windows:
```
python main.py
```
on Linux/Mac:
```
python3 main.py
```

# GIT command lines
## get latest version
```
git clone https://github.com/nono-london/french_tech.git
```
## update to the latest version
depending on the name of your branch 'master' or 'origin'
```
git pull origin master
```
or
```
git pull origin main
```
# Web Interface
The web interface uses the streamlit library and is used for data visualization purposes

## start the interface

to start the web interface, type in the venv command line:
on Windows

```
python -m streamlit run ./french_tech/main_streamlit.py
```

on Linux/mac

```
python3 -m streamlit run ./french_tech/main_streamlit.py
```

# TODO:

* Add web interface
* optimize company urls:
  * load all data rather than read each time
  * use Google Sheet to store info
* web interface:
  * select by company name
  * existing website
  *

# Source of information

## Startups

### Free

### Not free
