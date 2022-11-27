from atlassian import Bamboo as bamboo
from bamboo_access import BambooAccess

if __name__ == '__main__':
    bamboo = BambooAccess()
    bamboo.write_all_permissions_df_yaml('permissions.yaml')