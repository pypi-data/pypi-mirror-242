import time
from datetime import date
import mysql_rm
import connect

def main():
    script_start_time = time.time()
    selectedStartDate = date(2023, 11, 20)
    selectedEndDate = date(2023, 11, 30)

    ini_file = r"D:\Python\MySQL\mysqlquerys\src\mysqlquerys\local.ini"
    # ini_file = r"D:\Python\MySQL\mysqlquerys\src\mysqlquerys\heroku.ini"

    conf = connect.Config(ini_file)
    active_table = mysql_rm.Table(conf.credentials, 'asigurari')
    print(active_table.columnsProperties)
    print(active_table.columnsNames)

    scrip_end_time = time.time()
    duration = scrip_end_time - script_start_time
    duration = time.strftime("%H:%M:%S", time.gmtime(duration))
    print('run time: {}'.format(duration))

if __name__ == '__main__':
    main()
