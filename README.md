# Journal Publication Portal

> This project is under development and not fully deployed yet.

> Supervisor: Dr. Prakash Chauhan, Assistant Professor, Dept. of CS&IT, Cotton University, Guwahati, Assam

## Table of Contents

 - [Installation of Python Latest Version](#installation-of-python-latest-version)
    - [Installation in Windows](#installation-in-windows)
  - [Setting Up the Requirements for the project](#setting-up-the-requirements-for-the-project)
  - [Setting Up the Django Server for Debugging](#setting-up-the-django-server-for-debugging)
    - [Directories with Purpose](#directories-with-purpose)
    - [Server Start and Stop](#server-start-and-stop)

## Installation of Python Latest Version

### Installation in Windows
- Download and install the latest version of Python
    > - To download the latest version of the Python interpreter in your Windows PC, please go to the  [Python 3 Latest Release | Windows](https://www.python.org/.downloads/windows/) site and download the installer.
    > - Run the installer.



## Setting Up the Requirements for the project

Run the following command to install the project dependencies:
```
pip install -r requirements.txt
```

>[!TIP]
>You can use a Python Virtual Environment and install the project dependencies within the virtual environment. A Python virtual environment is a self-contained directory that contains a specific Python installation and its associated packages. This helps isolate project dependencies and avoid conflicts.


## Setting Up the Django Server for Debugging

The Django server is already setup for you. All the necessary directories are mapped for the development. The following are the Django applications configured to redirect to specific landing pages:

### Directories with Purpose

1. **/dept_admin:** Landing site for the department admin.
2. **/user:** Landing site for the normal users.
3. **/faculty:** Landing site for the logged in faculties.


### Server Start and Stop

To start the Django server, type the following commands in sequence:

1. Go to the project directory:
   ```
   cd your\project\directory\on\disk
   ```
2. Start the server:
   ```
   python .\manage.py runserver
   ```
   OR simply
   
   ```
   py manage.py runserver
   ```
4. You have any port issues, then type the following command with your desired port number to start the server:
   ```
   python .\manage.py runserver <port-number>
   ```
5. To stop the server, press `Ctrl + C` on your keyboard while your terminal is in focus.

<!-- Will be updated later regarding database migration, user authentication, security etc. -->

