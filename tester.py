import json
import time

from data_base import sql_db


sql_db.sql_start()
print( sql_db.disable_task(2)  )
# #
# while True:
#     task = sql_db.get_tasks()
#     if task:
#         array_task = json.loads( task[0][1] )
#         print( array_task['function'] , '\n' , array_task['arguments'] )
#         sql_db.del_task_for_id(task[0][0])
#         break
#     time.sleep(1)




# proxys_list = [['01'], ['02'] , ['03'] , ['04']]
# twitters_list  = [[1], [2], [3], [4], [5], [6], [7], [8], [9], [10], [11], [12], [13], [14], [15], [16], [17]]
# count_pars = 5
# i_may = len(twitters_list) // count_pars
# real = len(proxys_list) - i_may
# if real > 0:
#     use = i_may
# else:
#     use = len(proxys_list)
#
# do  =  0
# for pr in range(use):
#     for tw in range(count_pars):
#         print (proxys_list[pr], twitters_list[pr * count_pars + tw])
#         do += 1
#
# offset = twitters_list[do:]
# print(offset)
# print(use)




