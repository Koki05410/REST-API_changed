from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.review import ReviewModel

class Review(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('score',
        type=float,
        required=True,
        help="This field cannot be left blank!"
    )
    parser.add_argument('sentence',
        type=str,
        required=False,
        help="This field can be left blank!"
    )
    parser.add_argument('target',
        type=int,
        required=True,
        help="This field cannot be left blank!"
    )
    parser.add_argument('user_id',
        type=int,
        required=True,
        help="This field cannot be left blank!"
    )
    parser.add_argument('store_id',
        type=int,
        required=True,
        help="Every review needs a store id."
    )

    @jwt_required()
    def get(self, review_id):
        review = ReviewModel.find_by_review_id(review_id)
        if review:
            return review.json()
        return {'message': 'review not found'}, 404

    def post(self, review_id):
        if ReviewModel.find_by_review_id(review_id):
            return {'message': "A review with review_id '{}' already exists.".format(review_id)}, 400

        data = Review.parser.parse_args()

        review = ReviewModel(review_id, **data)

        try:
            review.save_to_db()
        except:
            return {"message": "An error occurred inserting the review."}, 500

        return review.json(), 201

    def delete(self, review_id):
        review = ReviewModel.find_by_review_id(review_id)
        if review:
            review.delete_from_db()

        return {'message': 'review deleted'}

    def put(self, review_id):
        data = Review.parser.parse_args()

        review = ReviewModel.find_by_review_id(review_id)

        if review is None:
            review = ReviewModel(review_id, **data)
        else:
            review.score = data['score']
            review.sentence = data['sentence']
            review.target = data['target']

        review.save_to_db()

        return review.json()


class ReviewList(Resource):
    def get(self):
        return {'dataset': [x.json() for x in ReviewModel.query.all()]}
