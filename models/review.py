from db import db

class ReviewModel(db.Model):
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    #name = db.Column(db.String(80))
    review_id = db.Column(db.Integer)
    score = db.Column(db.Float(precision=2))
    sentence = db.Column(db.String)
    target = db.Column(db.Integer)
    user_id = db.Column(db.Integer)

    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'))
    store = db.relationship('StoreModel')

    def __init__(self, review_id, score, sentence, store_id, target, user_id):
        self.review_id = review_id
        self.score = score
        self.store_id = store_id
        self.sentence = sentence
        self.target = target
        self.user_id = user_id

    def json(self):
        return {'review_id': self.review_id, 'score': self.score, 'sentence':self.sentence, 'target':self.target, 'user_id':self.user_id}

    @classmethod
    def find_by_review_id(cls, review_id):
        return cls.query.filter_by(review_id=review_id).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
