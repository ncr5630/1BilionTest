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
import os
import json
import config as cons
from tree_service_model import TreeServiceModel

DB_HOST = cons.DB_HOST
DB_USER = cons.DB_USER
DB_PASSWORD = cons.DB_PASSWORD
DB_NAME = cons.DB_NAME
DB_PORT = cons.DB_PORT
TABLE_NAME = cons.TABLE_NAME
DATA_PATH = cons.DATA_PATH


class TreeServiceMange:
    level = 0
    pid = "0"

    def __init__(self):
        self.tree_main_oj = TreeServiceModel()

    def read_n_insert_data(self, file_name):
        cwd = os.getcwd()
        with open(cwd + "/" + DATA_PATH + '/' + file_name) as f:
            records = json.loads(f.read())
            f.close()
            return self.insert_tree_data(*records)

    def insert_tree_data(self, *records):
        if records:
            for data in records:
                insert_data = {}
                insert_data['pid'] = data.get("pid", 0)
                insert_data['name'] = data.get("name", "")
                insert_data['age'] = data.get("age", "")
                pid = self.tree_main_oj.common_routine_insert_dictionary_data_to_db(TABLE_NAME, **insert_data)
                if pid:
                    other_data = data.get("data", [])
                    for item in other_data:
                        item_list = list()
                        new_records = {}
                        new_records['pid'] = pid
                        new_records['name'] = item.get("name", "")
                        new_records['age'] = item.get("age", "")
                        new_records['data'] = item.get("data", [])
                        item_list.append(new_records)
                        self.insert_tree_data(*item_list)

    def create_tree_table(self):
        status = self.tree_main_oj.create_tree_tb(TABLE_NAME)
        return status

    def sorted_data(self, order="desc"):
        condition = 1
        field_data = ['age']
        result = self.tree_main_oj.get_result(TABLE_NAME, condition, *field_data)
        i = 0
        data_list = []
        for row in result:
            data_list.append(row[0])
            i += 1

        for i in range(len(data_list) - 1, 0, -1):
            for j in range(i):
                first_val = data_list[j] if order == "asc" else data_list[j + 1]
                second_val = data_list[j + 1] if order == "asc" else data_list[j]
                if first_val > second_val:
                    temp = data_list[j]
                    data_list[j] = data_list[j + 1]
                    data_list[j + 1] = temp
        return data_list

    def print_tree_product(self, id, *fields):
        result = []
        condition = f"pid='{id}'"
        result = self.tree_main_oj.get_result(TABLE_NAME, condition, *fields)
        for row in result:
            record_row = {}
            i = 0
            for key_val in fields:
                if "as" in key_val:
                    # "count(`source`) as val" Here need to add val as
                    # field name below lines for this converting
                    x = key_val.split(' as ')
                    key_val = x[1] if len(x) > 1 else key_val
                    key_val = key_val.strip()
                record_row[key_val] = row[i]
                i = i + 1

            for j in range(0, self.level):
                print(" -", end="")
            if self.level != 0:
                print(">", end="")
            else:
                print(u'\u2B24', end="")
            self.level += 1
            print(f" {record_row['name']}|{record_row['age']}")
            self.print_tree_product(record_row['id'], *fields)
            self.level -= 1
        return True


if __name__ == '__main__':
    obj_tree = TreeServiceMange()

    # Problem 1:
    # run table creation before run Q1
    # step1
    # obj_tree.create_tree_tb(TABLE_NAME)

    # Q1 answer
    # obj_tree.read_n_insert_data("problem1_q1.json")

    # Q2 answer
    data = obj_tree.sorted_data("desc")

    print(data)

    # Q3 answer
    data = obj_tree.sorted_data("asc")

    # Q4 answer
    fields = ['id', 'age', 'name']
    # data = obj_tree.print_tree_product(TABLE_NAME, "0", *fields)

    # Problem 2:
    # obj_tree.read_n_insert_data("problem_2.json")

    # fields = ['id', 'age', 'name']
    data = obj_tree.print_tree_product("0", *fields)

    print(data)
