# Let's Bid 

This repository is for ICT3x03 Secure Software Development Project. 
The purpose of this repository is to keep all the files updated and everybody in-sync.

##IMPORTANT 
1) Team member to request .env file from our leader to fully run the application with DB connection. 
2) Current Server's .env file is located in the nginx webroot. 
   1) This is to allow flask, which is integrated with Nginx, to use the .env.
3) Do note that the application requires the .env file for certain functions to work as it should be.

## Requirements
1) Python Version 3.9+
2) Flask 2.0.1
3) Web Browser / Mobile
4) Visual Studio Code / PyCharm
5) MySQL Workbench


## Setup
### Use Python virtual environment for all apps in this GitHub
### Local Desktop
1) Download / Clone the codes into your local desktop. 
2) Set up virtual environment (venv) in the project file.
3) Cd to your `venv/Scripts` and `activate` your venv
4) Enter the command: `pip install -r requirements.txt` to install necessary requirements into the project.
5) Cd out of the venv folder, to the root folder and enter the command `flask run --reload`
   1) This is to run flask app with auto-reload

####[Alternatively, you may follow the steps below:]
1) Ensure that python3 is installed.
2) Run the startup_ps.ps1 
3) Open cmd and cd to the file dir
4) Enter the command: `flask run`
5) Use preferred browser and type in the URL "127.0.0.1:5000"
   1) Suitable Browser: Google Chrome, Mozilla Firefox, Microsoft Edge
6) Enjoy surfing the application :)

### Web / VM
1) Pushing the updated web application files will trigger a Jenkins process, which will fullfill both CI and CD portion. The Jenkinsfile detailed how the iItegration and Deployment is handled.
2) To surf the application, visit the website: https://dabestteam.sitict.net/

### Things to take note:
<li> The application only accepts image file extensions: png, jpg, and jpeg.


## VM Details:
1) IP Addr: 139.59.252.115
2) Default ports are used as per OWASP Security Principle - Keep Security Simple.

## Database Access
For the data access layer, the team is using AWS RDS. 