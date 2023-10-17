from hmac import compare_digest

from flask import Flask
from flask import jsonify
from flask import request
from flask_sqlalchemy import SQLAlchemy

from flask_restx import Api, Resource, fields

from flask_jwt_extended import create_access_token
from flask_jwt_extended import current_user
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager

app = Flask(__name__)
api = Api(app)

app.config["JWT_SECRET_KEY"] = "super-secret"  # Change this!
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite://"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


jwt = JWTManager(app)
db = SQLAlchemy(app)


class User(db.Model):
    """User 클래스"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text, nullable=False, unique=True)
    full_name = db.Column(db.Text, nullable=False)

    # NOTE: In a real application make sure to properly hash and salt passwords
    def check_password(self, password):
        """패스워드를 비교하는 루틴"""
        return compare_digest(password, "password")


# Register a callback function that takes whatever object is passed in as the
# identity when creating JWTs and converts it to a JSON serializable format.
@jwt.user_identity_loader
def user_identity_lookup(user):
    return user.id


# Register a callback function that loads a user from your database whenever
# a protected route is accessed. This should return any python object on a
# successful lookup, or None if the lookup failed for any reason (for example
# if the user has been deleted from the database).
@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return User.query.filter_by(id=identity).one_or_none()


@api.route("/login")
class Login(Resource):
    """로그인을 수행하는 기능"""
    def get(self):
        """no response"""
        return ''

    def post(self):
        """로그인 요청"""
        username = request.json.get("username", None)
        password = request.json.get("password", None)

        user = User.query.filter_by(username=username).one_or_none()
        if not user or not user.check_password(password):
            return jsonify("Wrong username or password"), 401

        # Notice that we are passing in the actual sqlalchemy user object here
        access_token = create_access_token(identity=user)

        return jsonify(access_token=access_token)


@api.route("/whoami")
class WhoAmI(Resource):
    """내 자격 증명 확인"""
    @jwt_required()
    def get(self):
        ''' We can now access our sqlalchemy User object via `current_user`.'''
        return jsonify(
            id=current_user.id,
            full_name=current_user.full_name,
            username=current_user.username,
        )

    @jwt_required()
    def post(self):
        """no response"""


@api.route('/users')
class Users(Resource):
    """유저를 관리하는 기능으로 생성, 조회, 삭제, 수정 기능을 포함"""
    @jwt_required()
    def post(self):
        """유저 생성"""
        data = request.json

        full_name = data['full_name']
        username = data['username']
        with app.app_context():
            db.session.add(User(full_name=full_name, username=username))
            db.session.commit()

        return jsonify({'message': 'User created successfully'})

    @jwt_required()
    def get(self):
        """유저 조회"""
        users = User.query.all()

        results = []
        for user in users:
            results.append({
                'id': user.id,
                'full_name': user.full_name,
                'username': user.username,
            })

        return jsonify({'users': results})

    @jwt_required()
    def put(self):
        """유저 수정"""

    @jwt_required()
    def delete(self, _id):
        """유저 삭제"""
        user = User.query.get(_id)
        user.delete()

        return jsonify({'message': 'User deleted successfully'})


with app.app_context():
    db.create_all()
    db.session.add(User(full_name="Bruce Wayne", username="batman"))
    db.session.add(User(full_name="Ann Takamaki", username="panther"))
    db.session.add(User(full_name="admin", username="admin"))
    db.session.commit()

if __name__ == "__main__":
    app.run()
