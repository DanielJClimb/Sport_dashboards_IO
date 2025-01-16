# 1. SCOS (Scrunity of Sport)
Description: the application is designed to allow the creation of quick visualizations and summaries of the game of selected players. Based on the data downloaded using the API, graphics will be used to create a short report of player’s performance during the game.

# 3. Requirements specification
/ Id / Name / Short description / Priority [1 - required, 2 - needed, 3 - optional] / Functional category /
| :--: |
| A1 | API Connections | Downloading data for selected player and match using the API from Statsbomb website | 1 | functional |
| A2 | Selection of players and matches | Possible option to select the match and player for which the application should prepare a report | 1 | functional |
| A3 | Visualizations of field players performance | Creating a visualization showing maps of passes, ball recoveries, duels and shots  of a given player during a match | 1 | functional | 
| A4 | Visualizations of goalkeepers performance| Creating a visualization showingmaps of passes and ball recoveries map of a given goalkeeper during a match | 1 | functional |
| A5 | Table with statistics | Creating a table showing basic and specific statistics for selected player | 2 | functional |
| A6 | Non-failure | The app is creating report and visualisations with no failures and inform about any inconvenience | 2 | non- functional |
| A7 | Ease of use | Creating proper interface easy to understand for every user and with short wait time (maximum 3 minutes) | 2 | non - functional |
| A8 | Interface color | Creating proper interface color of dashboard | 3 | non - functional |
| A9 | Plot and statistics export | The app allows user to export report for each player in PDF format with specific requirements of use it | 3 | functional |

# 4. Architecture
## 4.1 Development architecture

| Id | Tool | Purpose | Version |
| :--: |
| T1 | Python | Programmin langueage | 3.9 | 
| T2 | Spyder | Development environment | 5.0 |
| T3 | pandas | Data analyses tool | 2.1.1 | 
| T4 | statsBombpy | Connectig with Api services | 1.14.0 |
| T5 | mplsoccer | Pitch visualizations | 1.4.0 |
| T6 | matplotlib | Visualizations tool | 3.8.0 |
| T7 | streamlit | Creating graphical interface | 1.40.2 |
| T8 | os | crrating script for opening application | 3.9 | 

## 4.2 Runtime architecture

| Id | Tool | Purpose |
| :--: |
| R1 | Internet connection | Provide connection to api services for data extraction | 
Due to teh creation of thi exe file users do not have to install python or development enviroment








