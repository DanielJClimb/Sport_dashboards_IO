# Documentation

## 1. Software characteristics
Short name: **SCOS** \
Full name: **Scrunity of Sport** <br><br>
Short description: This application is designed to allow the creation of quick visualizations and summaries of the game of selected players. Based on the data downloaded using the API, graphics will be used to create a short report of player’s performance during the game, which can be later downloaded in PDF format.

## 2. Copyrights
Authors: Daniel Jarzymowski, Jakub Lewandowski \
License: GNU GENERAL PUBLIC LICENSE, Version 2 (???)
<br>

## 3. Requirements specification
| Id | Name | Short description | Priority | Functional category |
| :--: | :--: | :--: | :--: | :--: | 
| A1 | API Connections | Downloading data for selected player and match using the API from Statsbomb website | Required | functional |
| A2 | Selection of players and matches | Possible option to select the match and player for which the application should prepare a report | Required | functional |
| A3 | Visualizations of field players performance | Creating a visualization showing maps of passes, ball recoveries, duels and shots of a given player during a match | Required | functional | 
| A4 | Visualizations of goalkeepers performance| Creating a visualization showing maps of passes and ball recoveries of a given goalkeeper during a match | Required | functional |
| A5 | Table with statistics | Creating a table showing basic and specific statistics for selected player | Needed | functional |
| A6 | Non-failure | The app is creating report and visualisations with no failures and inform about any inconvenience | Needed | non- functional |
| A7 | Ease of use | Creating proper interface easy to understand for every user and with short wait time (maximum 3 minutes) | Needed | non - functional |
| A8 | Interface color | Creating proper interface color of dashboard | Optional | non - functional |
| A9 | Plot and statistics export | The app allows user to export report for each player in PDF format | Optional | functional | 
<br>

## 4. Architecture
### 4.1 Development architecture
| Id | Tool | Purpose | Version |
| :--: | :--: | :--: | :--: | 
| T1 | Python | Programming language | 3.9 | 
| T2 | Spyder | Development environment | 5.0 |
| T3 | pandas | Data analyses tool | 2.1.1 | 
| T4 | statsBombpy | Connecting with Api services | 1.14.0 |
| T5 | mplsoccer | Pitch visualizations | 1.4.0 |
| T6 | matplotlib | Visualizations tool | 3.8.0 |
| T7 | streamlit | Creating graphical interface | 1.40.2 |
| T8 | os | creating script for openning application | 3.9 | 

### 4.2 Runtime architecture
| Id | Tool | Purpose |
| :--: | :--: | :--: | 
| R1 | Internet connection | Provide connection to api services for data extraction | 
| R2 | Programming language | Downloading and installing Python version 3.9 for running script |
| R3 | Spyder | Downloading and installing Spyder version 5.0 and selecting python intepreter for running script | 
| R4 | Libraries | Installing libraries mentioned in point 4.1 for script to run | 
| R5 | Script for opening app | Opening app by running opening_streamlit.py script in development environment | 
<br>

## 5. Tests
### 5.1 Tests scenarios
| Id | Aspect | Scenario | 
| :--: | :--: | :--: | 
| Test1 | Opening app using spyder environment | Try opening application by running opening_streamlit.py script in Spyder  |
| Test2 | Checking the need for an internet connection | Openning app without internet connection |
| Test3 | Changing the match | Select different match from options to check if it offers choice of different players | 
| Test4 | Changing the player | Select different player from provided options | 
| Test5 | Different plots and statistics for goalkeepers | Veryfing if app show different aspects of performance for goalkeepers and players from the field | 
| Test6 | Printing report to pdf file | Using button to download palyer repport to pdf file | 

### 5.2 Tests results 
| Id | Result |
| :--: | :--: |
| Test1 | App opens after few seconds only if opening_streamlit.py and main.py scripts are in the same location |
| Test2 | Error requests.exceptions.ConnectionError appears, which means internet connection is required for app to work |
| Test3 | After selecting another match app automatically provides report for player from selected game | 
| Test4 | After selecting another player app automatically provides report for this player |
| Test5 | After selecting goalkeepr different statistics were provided | 
| Test6 | After clicking button pdf file with report for selected player is downloaded to app location | 
