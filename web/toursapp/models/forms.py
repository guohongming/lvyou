__author__ = 'Guo'

from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, EqualTo
from toursapp.models.models import User


class LoginForm(FlaskForm):
    username = StringField('用户名', [DataRequired(), Length(max=255)])
    password = PasswordField('密码', [DataRequired()])
    remember = BooleanField("记住我")
    submit = SubmitField('Submit')

    def validate(self):
        check_validate = super(LoginForm, self).validate()

        # 如果验证没有通过
        if not check_validate:
            return False

        # 检查是否存在拥有该用户名的用户
        user = User.query.filter_by(
            user_name=self.username.data
        ).first()

        if not user:
            self.username.errors.append(
                'Invalid username or password'
            )
            return False

        # 检查密码
        if not user.check_password(self.password.data):
            self.username.errors.append('Invalid username or password')
            return False

        return True


class RegisterForm(FlaskForm):
    username = StringField('Username', [DataRequired(), Length(max=255)])
    password = PasswordField('Password', [DataRequired(), Length(min=8)])
    confirm = PasswordField('Confirm Password', [
        DataRequired(),
        EqualTo('password')
    ])

    def validate(self):
        check_validate = super(RegisterForm, self).validate()

        # if our validators do not pass
        if not check_validate:
            return False

        user = User.query.filter_by(user_name=self.username.data).first()

        # Is the username already being used
        if user:
            self.username.errors.append("User with that name already exists")
            return False

        return True


if __name__ == '__main__':
    f = LoginForm()