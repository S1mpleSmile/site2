from shop import db, bcrypt, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# класс, реализующий пользователелй, должен иметь 4 обязательных
# метода, которые можно унаследовать от UserMixin
# подробнее: https://flask-login.readthedocs.io/en/latest/
class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=25), nullable=False, unique=True)
    email = db.Column(db.String(length=256), nullable=False, unique=True)
    password_hash = db.Column(db.String(length=70), nullable=False)
    budget = db.Column(db.Integer(), nullable=False, default=0)
    products = db.relationship('Product', backref='owned_user', lazy=True)

    @property
    def password(self):
        return self.password

    @password.setter
    def password(self, regular_password):
        self.password_hash = bcrypt.generate_password_hash(regular_password).decode('utf-8')

    def correct_password(self, attempt_password):
        return bcrypt.check_password_hash(self.password_hash, attempt_password)

    def can_buy(self, product_obj):
        return self.budget >= product_obj.price

    def can_sell(self, product_obj):
        return product_obj in self.products


class Product(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(length=25), nullable=False, unique=True)
    price = db.Column(db.Integer(), nullable=False)
    article = db.Column(db.String(length=11), nullable=False, unique=True)
    description = db.Column(db.String(length=2048), nullable=False, unique=True)
    owner = db.Column(db.Integer(), db.ForeignKey('user.id'))

    def __repr__(self):
        return f'Product {self.name}'

    def buy(self, user):
        self.owner = user.id
        user.budget -= self.price
        db.session.commit()

    def sell(self, user):
        self.owner = None
        user.budget += self.price
        db.session.commit()
