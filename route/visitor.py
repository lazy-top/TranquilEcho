from flask import Blueprint
from flask_jwt_extended import create_access_token
from utils import CustomResponse,siwa
visitorbp = Blueprint('visitor', __name__,url_prefix='/visitor')
@visitorbp.route('/login',methods=['POST'])
@siwa.doc(tags=['visitor'])
def login():
    access_token = create_access_token(identity='visitor')
    return CustomResponse(
        data={
            'access_token':access_token
            },
        message='success',
        status=200
    )