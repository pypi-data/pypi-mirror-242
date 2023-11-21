import chelt_plan
import masina
from mysqlquerys import connect
from datetime import date
import time


def main():
    script_start_time = time.time()
    selectedStartDate = date(2023, 1, 1)
    selectedEndDate = date(2023, 1, 31)

    ini_file = r"D:\Python\MySQL\mysqlquerys\src\mysqlquerys\local.ini"
    # ini_file = r"D:\Python\MySQL\mysqlquerys\src\mysqlquerys\heroku.ini"

    app = chelt_plan.CheltuieliPlanificate(ini_file)
    # app.get_all_sql_vals()
    # print('FINISH')
    app.prepareTablePlan('all', selectedStartDate, selectedEndDate)
    # print(app.expenses)
    print(app.tot_val_of_irregular_expenses())
    print(app.tot_no_of_irregular_expenses())

    # app = masina.Masina(ini_file)
    # # app.prepareTablePlan('EC', selectedStartDate, selectedEndDate)
    # print(app.default_interval)
    # print(app.db_pass)

    scrip_end_time = time.time()
    duration = scrip_end_time - script_start_time
    duration = time.strftime("%H:%M:%S", time.gmtime(duration))
    print('run time: {}'.format(duration))

if __name__ == '__main__':
    main()
