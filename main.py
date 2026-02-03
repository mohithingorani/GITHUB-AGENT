from flask import Flask, request, jsonify
from flask_jwt_extended import (
    JWTManager,
    create_access_token,
    jwt_required,
    get_jwt_identity
)
from config import Config
from models import db, User, Chat

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

jwt = JWTManager(app)

with app.app_context():
    db.create_all()


@app.route("/signup",methods=["POST"])
def signup():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"Error":"Email and Password Required"}), 400
    
    if User.query.filter_by(email=email).first():
        return jsonify({"Error":"User already exists"}), 409
    
    user = User(email=email)
    user.set_password(password)

    db.session.add(user)
    db.session.commit()

    return jsonify({"message":"User created successfully"}), 201



@app.route("/signin",methods=["POST"])
def signin():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error":"Email and Password Required"}),400
    
    user = User.query.filter(email=email).first()

    if not user or not user.check_password():
        return jsonify({"error":"Invalid Credentials"}),401
    
    token = create_access_token(identity=user.id)

    return jsonify({
        "access_token" :token
    }),200


