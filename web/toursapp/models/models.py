__author__ = 'Guo'
from flask_sqlalchemy import SQLAlchemy
from toursapp.extensions import bcrypt
from toursapp.extensions import login_manager
from flask_login import AnonymousUserMixin
db_user = SQLAlchemy()


class User(db_user.Model):

    id = db_user.Column(db_user.INTEGER(), primary_key=True)
    user_name = db_user.Column(db_user.String(255))
    password = db_user.Column(db_user.String(255))

    def __init__(self, username):
        self.user_name = username

    def __repr__(self):
        return "<User '{}'>".format(self.user_name)

    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password)

    def check_password(self, password):

        return bcrypt.check_password_hash(self.password, password)

    def is_authenticated(self):
        if isinstance(self, AnonymousUserMixin):
            return False
        else:
            return True

    def is_active(self):
        return True

    def is_anonymous(self):
        if isinstance(self, AnonymousUserMixin):
            return True
        else:
            return False

    def get_id(self):
        return str(self.id)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


if __name__ == '__main__':
    User.query.all()