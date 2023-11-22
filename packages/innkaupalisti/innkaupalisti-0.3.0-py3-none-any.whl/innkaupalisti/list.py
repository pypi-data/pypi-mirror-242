import urllib.parse
from flask import request
from flask_restful import Resource
from sqlalchemy.exc import NoResultFound
from innkaupalisti import store
from innkaupalisti.app import db
from innkaupalisti.auth import token_required


class Lists(Resource):
    method_decorators = [token_required]

    def get(self, user):
        return [list.as_dict() for list in user.lists]
        # TODO: list per user...

    def post(self, user):
        # TODO: prevent duplicates
        list_json = request.get_json()
        new_list = store.List(name=list_json['name'], items=[])
        user.lists.append(new_list)
        db.session.commit()
        return (new_list.as_dict(),
                201,
                {'location': urllib.parse.quote(
                    f'{request.path}/{new_list.name}')})


class List(Resource):
    method_decorators = [token_required]

    def get(self, user, name):
        try:
            return ([li for li in user.lists if li.name == name][0].as_dict(),
                    200)
        except IndexError:
            return '', 404

    def delete(self, user, name):
        try:
            list = [li for li in user.lists if li.name == name][0]
        except IndexError:
            return '', 404
        db.session.delete(list)
        db.session.commit()
        return '', 204


class ListItems(Resource):
    method_decorators = [token_required]

    def get(self, user, name):
        try:
            shopping_list = store.get_list(name)
            return [item.as_dict() for item in shopping_list.items], 200
        except NoResultFound:
            return '', 404

    def post(self, user, name):
        try:
            list = [li for li in user.lists if li.name == name][0]
        except IndexError:
            return '', 404

        item_json = request.get_json()

        try:
            item_exists = [i for i in list.items
                           if i.name == item_json['name']][0]
            return item_exists.as_dict(), 409
        except IndexError:
            pass

        item = store.Item(
                list=list,
                name=item_json['name'],
                quantity=item_json['quantity'],
                unit=item_json['unit'])
        list.items.append(item)
        db.session.commit()
        return (item.as_dict(),
                201,
                {'location': urllib.parse.quote(
                    f'{request.path}/{item.name}')})


class ListItem(Resource):
    method_decorators = [token_required]

    def get(self, user, list_name, item_name):
        try:
            list = [li for li in user.lists if li.name == list_name][0]
            item = [i for i in list.items if i.name == item_name][0]
            return item.as_dict(), 200
        except IndexError:
            return '', 404

    def delete(self, user, list_name, item_name):
        try:
            list = [li for li in user.lists if li.name == list_name][0]
            if item_name in [i.name for i in list.items]:
                list.items = [i for i in list.items if i.name != item_name]
                db.session.commit()
                return '', 204
            else:
                return '', 404
        except IndexError:
            return '', 404

    def put(self, user, list_name, item_name):
        try:
            item = store.get_list_item(list_name, item_name)
        except NoResultFound:
            return '', 404
        for k, v in request.get_json().items():
            match k:
                case 'quantity':
                    item.quantity = v
                case 'unit':
                    item.unit = v
        db.session.commit()
        return '', 204
