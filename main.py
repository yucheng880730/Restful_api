from flask import Flask, request, jsonify, render_template
from flask_restful import Api
from resources.user import Users, User
from resources.account import Accounts, Account
import pymysql
import traceback
import jwt #jsonwebtoken
import time #ms
#from server import app


app = Flask(__name__)
api = Api(app)

api.add_resource(Users,'/users')
api.add_resource(User,'/user/<id>')
#api.add_resource(Accounts,'/accounts')
#api.add_resource(Account,'/account/<id>')
api.add_resource(Accounts,'/user/<user_id>/accounts')
api.add_resource(Account,'/user/<user_id>/account/<id>')


@app.before_request
def auth():
    token = request.headers.get('auth') 
    data = request.get_json()
    #print(data)
    user_id = data['user_id']
    valid_token = jwt.encode({'user_id': user_id, 'timestamp':int(time.time())}, 'password', algorithm='HS256').decode('utf-8')
    print(jwt.encode({'user_id': user_id, 'timestamp':int(time.time())}, 'password', algorithm='HS256'))
    print(valid_token)
    if token == valid_token:
        pass
    else:
        return{
            'msg':'invalid token'
        }


@app.route('/')
def index():
    return 'Hello world'

@app.route('/user/<user_id>/account/<id>/deposit',methods=['POST'])
def deposit(user_id, id):
    db, cursor, account = get_account(id)
    money = request.get_json()['money'] 
    balance = account['balance'] + int(money)
    sql = 'UPDATE api.accounts SET balance = {} WHERE id = {} and deleted is not true'.format(balance, id)
    response = {}
    try:
        cursor.execute(sql)
        response['msg'] = 'success'
    except:
        traceback.print_exc()
        response['msg'] ='failed'
    #提交修改
    db.commit()
    #關閉連線
    db.close()
    return jsonify(response)

@app.route('/user/<user_id>/account/<id>/withdraw',methods=['POST'])
def withdraw(user_id, id):
    db, cursor, account = get_account(id)
    money = request.get_json()['money']
    balance = account['balance'] - int(money)
    sql = 'update api.accounts Set balance = {} where id = {} and deleted is not true'.format(balance, id)
    response = {}
    try:
        cursor.execute(sql)
        response['msg'] = 'success'
    except:
        traceback.print_exc()
        response['msg'] = 'failed'
    db.commit()
    db.close
    return jsonify(response)

def get_account(id):
    db = pymysql.connect(host = 'localhost', user = 'root', password = '00000000', db ='api')
    cursor = db.cursor(pymysql.cursors.DictCursor)
    sql = """ SELECT * FROM api.accounts WHERE id = '{}' and deleted is not True """.format(id)
    cursor.execute(sql)
    return db, cursor, cursor.fetchone()   



if __name__ == '__main__':
    app.debug = True
    app.run(host = '127.0.0.1',port = 5000)
    #app.run(host = "localhost", port = 443, ssl_context = ('rootCA-key.pem','rootCA.pem'))
