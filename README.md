# File Upload

## Overview
A Flask-based web application for securely uploading files with user authentication and password-protected downloads.

## Features
- **User Authentication:** Only registered users can upload files
- **Password-Protected Downloads:** Users can download files with a password
- **File Management:** View a list of all uploaded files (only accessible to logged-in users)
- **No Search Engine Indexing:** Optional configuration to prevent search engines from indexing the site

## Installation

### Prerequisites
- docker-compose

**Clone the repository**
```bash
git clone https://github.com/lytexdev/FileUpload.git
cd FileUpload
```

**Copy and rename `.env.example` to `.env`**
```bash
cp .env.example .env
```

**Insert a Flask secret key in `.env`**
```bash
FLASK_SECRET_KEY=your-secret-key
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

#### Create a new user:
```bash
docker exec -it fileupload-web-1 sh -c "python3 user.py create"
```
#### Delete a user:
```bash
docker exec -it fileupload-web-1 sh -c "python3 user.py delete"
```

### File Upload

- Upload a file: navigate to `http://localhost:8080/upload` and select a file to upload

### File Management

- View a list of all uploaded files: navigate to `http://localhost:8080/files`

### Password-Protected Downloads

- Download a file: navigate to `http://localhost:8080/file/<file_name|custom_route>`

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
