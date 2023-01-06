import json

from flask import Flask, jsonify, abort
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import UniqueConstraint
from dataclasses import dataclass
import requests
from sqlalchemy.exc import IntegrityError

from producer import publish

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql://root:root@db/main'
CORS(app)

db = SQLAlchemy(app)

#Produt mit ID, Titel und Image
@dataclass
class Product(db.Model):
    id: int
    title: str
    image: str

    #Deklaration in DB
    id = db.Column(db.Integer, primary_key=True, autoincrement=False)
    title = db.Column(db.String(200))
    image = db.Column(db.String(200))


#Welcher User hat welches Produkt geliked?
@dataclass
class ProductUser(db.Model):
    #Deklaration in DB
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    product_id = db.Column(db.Integer)

    #Eindeutiger Constraint für Benutzer-ID und Produkt-ID
    __table_args__ = (UniqueConstraint('user_id', 'product_id', name='user_product_unique'),)

#Auflistung aller Produkte
@app.route('/api/products')
def index():
    return jsonify(Product.query.all())


#Hinzufügen eines Likes für ein Produkt
@app.route('/api/products/<int:id>/like', methods=['POST'])
def like(id):
    req = requests.get('http://host.docker.internal:8000/api/user') #ID des Benutzers erhalten
    json = req.json()

    #Wenn User das Produkt noch nicht geliked hat -> Produkt liken
    try:
        productUser = ProductUser(user_id=json['id'], product_id=id) #Datenbankeintrag
        db.session.add(productUser)
        db.session.commit()

        publish('product_liked', id) #Nachricht an RabbitMQ-Queue

    #Wenn User das Produkt schon geliked hat -> Produkt nicht liken
    except IntegrityError:
        db.session.rollback()
        abort(400, 'You already liked this product')

    return jsonify({
        'message': 'success'
    })


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')