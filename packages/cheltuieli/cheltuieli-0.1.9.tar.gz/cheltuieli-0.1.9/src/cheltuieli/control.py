import chelt_plan
import masina
from mysqlquerys import connect
from datetime import date


def main():
    selectedStartDate = date(2023, 11, 15)
    selectedEndDate = date(2023, 11, 30)

    ini_file = r"D:\Python\MySQL\mysqlquerys\src\mysqlquerys\local.ini"
    ini_file = r"D:\Python\MySQL\mysqlquerys\src\mysqlquerys\heroku.ini"

    # app = chelt_plan.CheltuieliPlanificate()
    # app.prepareTablePlan('EC', selectedStartDate, selectedEndDate)
    # print(app.expenses)

    app = masina.Masina(ini_file)
    # app.prepareTablePlan('EC', selectedStartDate, selectedEndDate)
    print(app.default_interval)
    print(app.db_pass)

if __name__ == '__main__':
    main()
