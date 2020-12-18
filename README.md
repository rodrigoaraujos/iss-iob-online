# iss-iob-online

Navigation, data collection and storage of information with Python

## Prerequisites
What things you need to install the software and how to install them

Python 3.x  
Chromedriver  
Chrome (you can use another browser)  
Some Python libraries following  

## Installing  
A step by step series of examples that tell you how to get a development env running  
Install the following Python libraries:  
pandas - A great Python Data Analysis Library;  
selenium - An API to write functional/acceptance tests using Selenium WebDriver.  
toml - A Python library for parsing and creating TOML.

## With:  
pip install -r requirements.txt  

## Chromedriver  
You can find install instructions in the official repository.  
https://chromedriver.chromium.org/downloads

## Running the code  
python main.py

__note: You need to have prior access to the [IOB online](https://www.iobonline.com.br/) , and put your access data in the username and password fields, located on lines 9 and 12 of the config.toml file  
```
7  [login.landing_page.modal.username]  
8  xpath = '//*[@id="txtLogin"]'  
9  value = 'your username'  
10 [login.landing_page.modal.password]  
11 xpath = '//*[@id="txtPassword"]'  
12 value = 'your password'  
```
