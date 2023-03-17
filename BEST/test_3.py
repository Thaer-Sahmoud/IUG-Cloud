# # import pandas as pd
# # import time
# # memCacheStatus = pd.DataFrame()
# #
# #
# # def hit_sql (key, val,HitBool):
# #     if HitBool == True:
# #         new_row = {'key': 'Saanvi', 'value': 96, 'hit': True, 'time': 90}
# #         AA = [1,2,3,4]
# #         memCacheStatus.append( AA, ignore_index=True)
# #     else:
# #         memCacheStatus.loc[len(memCacheStatus)+1] = new_row
# #     print(memCacheStatus)
# #
# # for i in range (10):
# #     hit_sql(1, 5, True)
# #
# # print(memCacheStatus.head())
#
#
# import pandas as pd
#
# # Create an empty dataframe
# df = pd.DataFrame()
#
# # Define the new row data as a dictionary
# new_row = {'col1': 10, 'col2': 20, 'col3': 30}
#
# # Append the new row to the dataframe
# df = df.append(new_row, ignore_index=True)
#
# # Print the updated dataframe
# print(df)