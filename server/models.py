from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float
from sqlalchemy.orm import relationship
from sqlalchemy_serializer import SerializerMixin
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Bakery(db.Model, SerializerMixin):
    __tablename__ = 'bakeries'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

    baked_goods = relationship('BakedGood', backref='bakery', lazy='dynamic')

class BakedGood(db.Model, SerializerMixin):
    __tablename__ = 'baked_goods'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    price = Column(Float)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    bakery_id = Column(Integer, ForeignKey('bakeries.id'))

    def __repr__(self):
        return f'<Baked Good {self.name}, ${self.price}>'