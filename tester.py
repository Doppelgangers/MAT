# import time
#
# from data_base import sql_db
#
#
# sql_db.sql_start()
#
# while True:
#     print('\n'*20)
#     print(sql_db.get_proxy())
#     time.sleep(1)

data = 'usefulleafnode1:up5r9ercuh:sashasolovyovsno@hotmail.com\nusefulleafnode1:up5r9ercuh:sashasolovyovsno@hotmail.com'


twits = data.strip().replace("\r", '').split( '\n' )

for twit in twits:
    username ,password , mail = twit.split(':')
    print(username ,password , mail)

