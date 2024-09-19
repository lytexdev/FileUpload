from models import db, User


def create_user():
    username = input("Enter username: ")
    password = input("Enter password: ")

    if User.query.filter_by(username=username).first():
        print("User already exists!")
        return

    user = User(username=username)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    
    print("User created successfully!")


if __name__ == '__main__':
    create_user()
