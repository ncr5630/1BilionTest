# -*- coding: utf-8 -*-
# !/usr/bin/python
'''
*************************************************************************************
* @developer        :   Nihal Chandrasiri
* @developer email  :   ncr5630@gmail.com
* @licence          :   GNU/GPL
* @product          :   1billion Technology Test
* @date             :   Feb 2023
* ************************************************************************************ *
'''
import json
import os
import traceback
import mysql.connector
from common_logger import CommonLogger
import config as cons

DB_HOST = cons.DB_HOST
DB_USER = cons.DB_USER
DB_PASSWORD = cons.DB_PASSWORD
DB_NAME = cons.DB_NAME
DB_PORT = cons.DB_PORT


class TreeServiceModel:
    class_name = os.path.basename(__file__)

    def __init__(self) -> object:
        self.common_logger = CommonLogger()
        self.mydb = None
        try:
            self.mydb = mysql.connector.connect(
                host=DB_HOST,
                user=DB_USER,
                passwd=DB_PASSWORD,
                database=DB_NAME,
                port=DB_PORT)
        except Exception as error:
            logs_dic = {
                'level': "error",
                'cus_message': "Database login error",
                'sys_message': "%s" % error,
                'class_name': __name__
            }
            self.common_logger.manage_logger(**logs_dic)

    @classmethod
    def get_class_name(cls):
        return cls.class_name

    def execute_mysql_query(self, query_str):

        try:
            # call mysql connection and select db
            cursor = self.mydb.cursor()

            # Below line is hide your warning
            cursor.execute("SET sql_notes = 0; ")
            # execute query
            cursor.execute(query_str)

            return True
        except Exception as error:
            logs_dic = {
                'level': "error",
                'cus_message': "Query executing error : %s" % error,
                # 'sys_message': "%s" % traceback.format_exc(),
                'class_name': __name__
            }
            self.common_logger.manage_logger(**logs_dic)
            return traceback.format_exc()

        finally:
            self.mydb.commit()
            self.mydb.close()

    def create_tree_tb(self, table_name):
        # create tree table
        sql = '''CREATE TABLE IF NOT EXISTS `%s` (            
        `id` int(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
        `pid` int(11) NOT NULL,
        `name` varchar(200) NOT NULL,
        'age' int(11) NOT NULL) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci 
        ''' % table_name
        return self.execute_mysql_query(sql)

    def delete_record(self, table_name, condition=1):
        # Delete record for given condition
        try:
            sql = "DELETE FROM %s WHERE %s" % (table_name, condition)
            self.execute_mysql_query(sql)
            return True
        except Exception as Error:
            print(Error)
            return False

    def common_routine_insert_dictionary_data_to_db(self, table_name=None, **insert_data):
        if not table_name:
            logs_dic = {
                'level': "critical",
                'cus_message': "Database 'table name' is missing in the CRUD operation",
            }
            self.common_logger.manage_logger(**logs_dic)
            return False
        else:
            try:
                cursor = self.mydb.cursor()
            except Exception as error:
                logs_dic = {
                    'level': "error",
                    'cus_message': f"mysql connection error : {error}",
                }
                self.common_logger.manage_logger(**logs_dic)
                # prepare values in the string for mysql
            # copy the original dictionary to working
            insert_data_working_dic = insert_data.copy()

            for dic_key in list(insert_data_working_dic):
                # This is to check if there is a dictionary within a dictionary
                # This only works by checking value of the key pair
                temp_value = insert_data_working_dic[dic_key]
                if isinstance(temp_value, (dict, list)):
                    # We will use json.dumpt to qualify the incoming data
                    json_val = json.dumps(insert_data_working_dic[dic_key], ensure_ascii=False)
                    # validate it
                    isValid = self.json_validator(json_val)
                    del (insert_data_working_dic[dic_key])
                    # now insert back JSon format to the dictionary
                    insert_data_working_dic.update({dic_key: json_val})
            # add %s for every columns names as placeholders
            query_placeholders = ', '.join(['%s'] * len(insert_data_working_dic))
            # add ',' between every columns
            query_columns = ', '.join(insert_data_working_dic)
            query_columns = query_columns.replace('nan', '')
            # create values list
            list_of_values = [insert_data_working_dic[key] for key in insert_data_working_dic]
            # generate query with given details
            query = ''' INSERT INTO %s (%s) VALUES (%s) ''' % (table_name, query_columns, query_placeholders)
            last_insert_id = None
            try:
                cursor.execute(query, list_of_values)
                self.mydb.commit()
                last_insert_id = cursor.lastrowid
            except Exception as error:
                logs_dic = {
                    'level': "error",
                    'cus_message': f"Records inserting error: {error}",
                }
                self.common_logger.manage_logger(**logs_dic)
            return last_insert_id

    def json_validator(self, data):
        try:
            json.loads(data)
            return True
        except ValueError as error:
            logs_dic = {
                'level': "critical",
                'cus_message': "invalid json: %s" % error
            }
            self.common_logger.manage_logger(**logs_dic)
            return False

    def get_result(self, table_name, condition, *fields):
        try:
            query_columns = ', '.join(fields)
            query = f"SELECT {query_columns} FROM {table_name} WHERE {condition} ORDER BY name"
            my_cursor = self.mydb.cursor()
            my_cursor.execute(query)
            result = my_cursor.fetchall()
            return result
        except Exception as Error:
            logs_dic = {
                'level': "error",
                'cus_message': f"message {Error}",
                'class_name': __name__,
            }
            self.common_logger.manage_logger(**logs_dic)
