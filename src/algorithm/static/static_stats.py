import pandas as pd

class permissions_stats():
    def __init__(self, type :str) -> None:
        self.data_file = "./out/"+type+'/permissions.csv' # csv file with permissions. Use default name.
        self.output_file = './out/'+type+'/static.csv'
        pd.set_option('display.float_format','{:.0f}'.format)
        self.permissions_quantity = pd.DataFrame({'Quantity':[]})
        self.permissions_limit = 50
        self.df_permissions = pd.DataFrame({'Permission':[],
                                        'Times':[]})
        self.__read_permission_list__()

    def __get_permission_count__(self,permissions) -> None:
        for permission in permissions:
            permission = permission.rstrip()
            permission_empty = self.df_permissions[self.df_permissions['Permission']==permission]
            if permission_empty.empty:
                self.df_permissions = pd.concat([self.df_permissions,pd.DataFrame({'Permission':[permission],
                                                                        'Times':1})], ignore_index=True)
            else:
                index = self.df_permissions.index[self.df_permissions['Permission'] == permission][0]
                self.df_permissions.at[index,'Times'] = self.df_permissions.at[index,'Times'] + 1

    def __read_permission_list__(self) -> None:
        with open(self.data_file,'r') as permissions:
            for row in permissions:
                permissions = row.split(",")
                permissions_len = len(permissions)
                if(permissions_len >= 1 and permissions_len < self.permissions_limit):
                    self.permissions_quantity = pd.concat([self.permissions_quantity,pd.DataFrame({'Quantity':[permissions_len]})], 
                                            ignore_index=True)
                    self.__get_permission_count__(permissions)
        self.df_permissions = self.df_permissions.sort_values(by=['Times'],ascending=False)
        self.df_permissions['Permission'].head(15).to_csv(self.output_file, index=False, header=False)

    def get_output_file(self) -> str:
        return self.output_file