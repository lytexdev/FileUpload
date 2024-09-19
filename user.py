from flask import Flask
from models import db, User
import click
from getpass import getpass
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)


@click.group()
def cli():
    pass


@cli.command('create')
def create_user():
    username = input("Enter username: ")
    password = getpass("Enter password: ")
    confirm_password = getpass("Confirm password: ")

    if password != confirm_password:
        print("Error: Passwords do not match.")
        return

    with app.app_context():
        if User.query.filter_by(username=username).first():
            print("Error: A user with this username already exists.")
            return

        new_user = User(username=username)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        print(f"User '{username}' created successfully.")


@cli.command('delete')
def delete_user():
    username = input("Enter the username of the user to delete: ")

    with app.app_context():
        user = User.query.filter_by(username=username).first()

        if not user:
            print(f"Error: No user found with the username '{username}'.")
            return

        confirm = input(f"Are you sure you want to delete the user '{username}'? (y/n): ")
        if confirm.lower() == 'y':
            db.session.delete(user)
            db.session.commit()
            print(f"User '{username}' has been deleted.")
        else:
            print("Operation cancelled.")


if __name__ == '__main__':
    cli()
