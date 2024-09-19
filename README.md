# File Upload

## Overview
A Flask-based web application for securely uploading files with user authentication and password-protected downloads.

## Features
- **User Authentication:** Only registered users can upload files.
- **Password-Protected Downloads:** Files can only be downloaded by entering the correct password.
- **File Management:** View a list of all uploaded files (only accessible to logged-in users).
- **No Search Engine Indexing:** Optional configuration to prevent search engines from indexing the site.
- **User Management via CLI:** Easily create and delete users through a command-line interface.

## Installation

**Clone the repository**
```bash
git clone https://github.com/lytexdev/file-upload.git
cd file-upload
```

**Create a virtual environment and activate it:**
```bash
python3 -m venv .venv
source .venv/bin/activate
# On windows use: .venv\Scripts\activate
```

**Install required packages:**
```bash
pip install -r requirements.txt
```

**Copy and rename `.env.example` to `.env`**
```bash
cp .env.example .env
```

**Configure environment variables** Edit the `.env` file to set the following variables:

`FLASK_SECRET_KEY`: a secret key for Flask

`DATABASE_URL`: the URL of the database (e.g. sqlite:///app.db)

`SEARCH_ENGINE_INDEXING`: a boolean value to enable or disable search engine indexing (default: False)

`PORT`: the port to listen on (default: 8080)

**Run application**
```bash
python3 app.py
```

## Usage

### User Management

- Create a new user: `python user.py create`
- Delete a user: `python user.py delete`

### File Upload

- Upload a file: navigate to `http://localhost:8080/upload` and select a file to upload

### File Management

- View a list of all uploaded files: navigate to `http://localhost:8080/files`

### Password-Protected Downloads

- Download a file: navigate to `http://localhost:8080/download/<file_name>` and enter the correct password

## License
This project is licensed under the MIT License. See the `LICENSE` file for details.