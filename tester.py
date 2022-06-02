import time

from data_base import sql_db


sql_db.sql_start()
#
# while True:
#     print('\n'*20)
#     print(sql_db.get_proxy())
#     time.sleep(1)

sql_db.lin_proxy_for_twitters()

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




