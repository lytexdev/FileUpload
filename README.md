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

### Prerequisites
- Python 3.11+
- Docker
- Docker Compose

**Clone the repository**
```bash
git clone https://github.com/lytexdev/FileUpload.git
cd FileUpload
```

**Copy and rename `.env.example` to `.env`**
```bash
cp .env.example .env
```

**Build and run the Docker image**
```bash
# with docker-compose-v2
docker compose up -d

# with docker-compose-v1
docker-compose up -d
```
By default it runs on port 8080

## Usage

### User Management

- Create a new user: `python3 user.py create`
- Delete a user: `python3 user.py delete`

### File Upload

- Upload a file: navigate to `http://localhost:8080/upload` and select a file to upload

### File Management

- View a list of all uploaded files: navigate to `http://localhost:8080/files`

### Password-Protected Downloads

- Download a file: navigate to `http://localhost:8080/download/<file_name>` and enter the correct password

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
