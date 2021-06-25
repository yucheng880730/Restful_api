from flask_restful import Resource, reqparse
from flask import jsonify
import pymysql
import traceback
import pymysql.cursors

parser = reqparse.RequestParser()
parser.add_argument('balance')
parser.add_argument('account_number')
parser.add_argument('user_id')
parser.add_argument('deleted')

class Account(Resource):
    def db_init(self):
        db = pymysql.connect(host = 'localhost', user = 'root', password = '00000000', db ='api')
        cursor = db.cursor(pymysql.cursors.DictCursor)
        return db,cursor
    def get(self, user_id, id):
        db, cursor = self.db_init()
        sql = """ SELECT * FROM api.accounts WHERE id ='{}' and deleted is not True """.format(id)
        cursor.execute(sql)
        db.commit()
        accounts = cursor.fetchone()
        db.close()
        return jsonify({'data': accounts})
    
    def patch(self, user_id, id):
        db, cursor = self.db_init()
        arg = parser.parse_args()
        account = {
            'balance':arg['balance'],
            'account_number':arg['account_number'], 
            'user_id':arg['user_id'],
        }
        query = []
        for key, value in account.items():
            if value != None:
                query.append(key +" = " + " '{}' ".format(value))
        query = ",".join(query)
        sql = """
            UPDATE `crud_api`.`accounts` SET {} WHERE (`id` = '{}');
        """.format(query, id)
        response = {}
        try:
            cursor.execute(sql)
            response['msg'] = 'success'
        except:
            traceback.print_exc()
            response['msg'] = 'failed'
        
        db.commit()
        db.close()
        return jsonify(response)
    
    def delete(self, user_id, id):  
        db, cursor = self.db_init()
        sql = """ UPDATE `crud_api`.`accounts` SET deleted = True WHERE (`id` = '{}') """.format(id)
        response = {}
        try:
            cursor.execute(sql)
            response['msg'] = 'success'
        except:
            traceback.print_exc()
            response['msg'] = 'failed'

        db.commit()
        db.close()
        return jsonify(response)

    def post(self, id):
        db, cursor = self.db_init()
        arg = parser.parse_args()
        account = {
            'balance':arg['balance'] or 0,
            'account_number':arg['account_number'] ,
            'user_id':arg['user_id']
        }
        
        sql = """INSERT INTO api.accounts (balance, account_number , user_id) VALUES ('{}','{}','{}');
            """.format(account['balance'], account['account_number'], account['user_id'])

       

        response = {}
        try:
            cursor.execute(sql)
            response['msg'] = 'success'
        except:
            traceback.print_exc()
            response['msg'] = 'failed'

        db.commit()
        db.close()
        return jsonify(response)




class Accounts(Resource):
    def db_init(self):
        db = pymysql.connect(host = 'localhost', user = 'root', password = '00000000', db ='api')
        cursor = db.cursor(pymysql.cursors.DictCursor)
        return db,cursor

    def get(self, user_id):
        db, cursor = self.db_init()
        #arg = parser.parse_args()
        sql = 'SELECT * FROM api.accounts where user_id = {} and deleted is not True'.format(user_id)
        '''
        if arg['gender'] != None:
            sql += ' and gender = "{}" '.format(arg['gender'])
        '''
        cursor.execute(sql)
        db.commit()
        accounts = cursor.fetchall()
        db.close()
        return jsonify({'data':accounts}) 

    def post(self, user_id):
        db, cursor = self.db_init()
        arg = parser.parse_args()
        account = {
            'balance':arg['balance'] or 0,
            'account_number':arg['account_number'] ,
            'user_id':arg['user_id'],
        }
        sql = """INSERT INTO api.accounts (balance, account_number , user_id) VALUES ('{}','{}','{}');
            """.format(account['balance'], account['account_number'], account['user_id'])

        response = {}
        try:
            cursor.execute(sql)
            response['msg'] = 'success'
        except:
            traceback.print_exc()
            response['msg'] = 'failed'

        db.commit()
        db.close()
        return jsonify(response)
