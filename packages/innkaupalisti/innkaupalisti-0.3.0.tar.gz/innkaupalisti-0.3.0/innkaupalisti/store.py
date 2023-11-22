from sqlalchemy.sql.expression import select, and_
from sqlalchemy.exc import NoResultFound
from werkzeug.security import generate_password_hash, check_password_hash
from innkaupalisti.app import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    password_hash = db.Column(db.String(100), nullable=False)
    lists = db.relationship(
            'List', order_by='List.name', backref='user')

    def create(self, username, password):
        self.username = username
        self.password_hash = generate_password_hash(password)
        db.session.add(self)
        db.session.commit()

    def get_by_username(self, username):
        return db.session.execute(
                select(User).filter_by(username=username)).scalar_one()

    def login(self, username, password):
        try:
            user = self.get_by_username(username)
            if check_password_hash(user.password_hash, password):
                return user
        except NoResultFound:
            return


class List(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    items = db.relationship(
            'Item', order_by='Item.name', backref='list')

    def __repr__(self):
        return f'<List {self.name}>'

    def __eq__(self, other):
        return self.name == other.name and self.items == other.items

    def as_dict(self):
        return {
                'name': self.name,
                'items': [item.as_dict() for item in self.items],
                }


def get_list(name):
    return db.session.execute(
            select(List).filter_by(name=name)).scalar_one()


def all_lists():
    return db.session.scalars(select(List)).all()


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    unit = db.Column(db.String(100))
    list_id = db.Column(db.Integer, db.ForeignKey('list.id'))

    def __repr__(self):
        return f'<Item {self.name}>'

    def __eq__(self, other):
        return (self.name == other.name
                and self.quantity == other.quantity
                and self.unit == other.unit)

    def as_dict(self):
        return {
                'name': self.name,
                'quantity': self.quantity,
                'unit': self.unit,
                }


def get_list_item(list_name, item_name):
    return db.session.execute(
            select(Item)
            .join(List)
            .where(and_(
                List.name == list_name,
                Item.name == item_name))).scalar_one()


def delete_item(list_name, item_name):
    item = get_list_item(list_name, item_name)
    db.session.delete(item)
    db.session.commit()
