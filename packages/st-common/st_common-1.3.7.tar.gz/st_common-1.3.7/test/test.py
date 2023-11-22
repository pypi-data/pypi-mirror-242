# example
from st_common import CommonBase
import shutil
path = r'C:\Users\Administrator\Desktop\tony_two'
commonbase = CommonBase(log_file="test.log")


all_files = commonbase.get_file(path)
destination_path = r"C:\Users\Administrator\Desktop\sales_growth_module_2"
for one_file in all_files:
    shutil.move(one_file, destination_path)
# print()
# 移动文件
            # shutil.move(file_path, destination_path)


# import argparse
# from datetime import datetime
# from st_common.commonbase import fn_timer
# from st_common.msgreport import ISZ_main_exception_report_args
# @ISZ_main_exception_report_args("Test")
# @fn_timer
# def main(args):
#     print(f"argument mode is {args.mod}")
#     print(datetime.now().strftime('%Y-%m-%d'))



# if __name__ == '__main__':
#     parser = argparse.ArgumentParser(description='tmp')
#     parser.add_argument('--mode', default="dev", choices=['dev', 'pro'],help="running mode")
#     args = parser.parse_args()
#     main(args=args)



# from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, DateTime, func,TIMESTAMP
# engine = create_engine('mysql+pymysql://rpaer:Rpaer2023!@192.168.6.253:3306/rpa_data?charset=utf8mb4')
# metadata = MetaData()
# new_table = Table('new_table', metadata,
#     Column('id', Integer, primary_key=True),
#     Column('update_at', TIMESTAMP, server_default=func.now(), onupdate=func.current_timestamp())
# )
# # 创建表
# metadata.create_all(engine)

# from sqlalchemy.sql import insert
# def insert_data(table, data):
#     """
#     Inserts data into a table.
    
#     :param table: The table to insert data into.
#     :param data: A dictionary where the keys are the column names and the values are the data to insert.
#     """
#     with engine.connect() as connection:
#         stmt = insert(table).values(data)
#         connection.execute(stmt)
# # 使用insert_data函数插入数据
# insert_data(new_table, {'id': 1})