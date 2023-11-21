from datetime import datetime, timedelta
from flask import Flask, render_template, request
import traceback
import sys
import os
import numpy as np
from cheltuieli.chelt_plan import CheltuieliPlanificate
from cheltuieli.masina import Masina

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    # print(sys._getframe().f_code.co_name, request.method)
    print('++++', request.method)
    # iniFile = None
    # form = iniFileCls()
    # if form.validate_on_submit():
    #     iniFile = form.iniFile.data
    #     # ttt = UPLOAD_PATH
    #     # print(iniFile)
    #     # print(UPLOAD_PATH)
    #     form.iniFile.data = ''
    # if request.method == 'POST':
    #     username = request.form['username']
    #     email = request.form['email']
    #     cur = mysql.connection.cursor()
    #     cur.execute('INSERT INTO users (name, email) VALUES (%s, %s)', (username, email))
    #     mysql.connection.commit()
    #     cur.close()
    # cur = mysql.connection.cursor()
    # users = cur.execute('SELECT * FROM aeroclub')
    # ini_file = r"D:\Python\MySQL\web_db.ini"
    # data_base_name = 'heroku_6ed6d828b97b626'
    # app = QApplication([])
    # iniFile, a = QFileDialog.getOpenFileName(None, 'Open data base configuration file', '',
    #                                          "data base config files (*.ini)")
    # dataBase = connect.DataBase(ini_file, data_base_name)
    # tableHead = ['name', 'value', 'myconto', 'freq', 'pay_day', 'valid_from', 'valid_to', 'auto_ext', 'post_pay']
    # all_chelt = []
    # for table in dataBase.tables:
    #     dataBase.active_table = table
    #     check = all(item in list(dataBase.active_table.columnsProperties.keys()) for item in tableHead)
    #     if check:
    #         vals = dataBase.active_table.returnColumns(tableHead)
    #         for row in vals:
    #             row = list(row)
    #             row.insert(0, table)
    #             all_chelt.append(row)
    #
    # newTableHead = ['table']
    # for col in tableHead:
    #     newTableHead.append(col)
    # params = config(iniFile)
    # print(params)
    # if users > 0:
    #     userDetails = cur.fetchall()
    # userDetails = {'ddd': 'ggg'}
    # user = os.environ.get('USERNAME')
    # user = os.getlogin()
    return render_template('index.html', iniFile='user', form='form')#, userDetails='all_chelt', database_name='heroku_6ed6d828b97b626'


@app.route('/cheltuieli', methods=['GET', 'POST'])
def cheltuieli():
    chelt_app = CheltuieliPlanificate('static/wdb.ini')
    # chelt_app = CheltuieliPlanificate('static/heroku.ini')
    dataFrom, dataBis = chelt_app.default_interval
    conto = 'all'

    if request.method == 'POST':
        month = request.form['month']
        conto = request.form['conto']
        dataFrom = request.form['dataFrom']
        dataBis = request.form['dataBis']
        if month != 'interval':
            dataFrom, dataBis = chelt_app.get_monthly_interval(month)
        elif month == 'interval' and (dataFrom == '' or dataBis == ''):
            dataFrom, dataBis = chelt_app.default_interval
        else:
            try:
                dataFrom = datetime.strptime(dataFrom, "%Y-%m-%d")
                dataBis = datetime.strptime(dataBis, "%Y-%m-%d")
                print(dataFrom.date(), dataBis.date())
            except:
                print(traceback.format_exc())
    try:
        chelt_app.prepareTablePlan(conto, dataFrom.date(), dataBis.date())
    except:
        print(traceback.format_exc())

    return render_template('cheltuieli.html',
                           expenses=chelt_app.expenses,
                           income=chelt_app.income,
                           tot_no_of_expenses_income=chelt_app.tot_no_of_expenses_income(),
                           tot_val_of_expenses_income=chelt_app.tot_val_of_expenses_income(),
                           tot_no_of_monthly_expenses=chelt_app.tot_no_of_monthly_expenses(),
                           tot_val_of_monthly_expenses=chelt_app.tot_val_of_monthly_expenses(),
                           tot_no_of_irregular_expenses=chelt_app.tot_no_of_irregular_expenses(),
                           tot_val_of_irregular_expenses=chelt_app.tot_val_of_irregular_expenses(),
                           tot_no_of_expenses=chelt_app.tot_no_of_expenses(),
                           tot_val_of_expenses=chelt_app.tot_val_of_expenses(),
                           tot_no_of_income=chelt_app.tot_no_of_income(),
                           tot_val_of_income=chelt_app.tot_val_of_income(),
                           dataFrom=dataFrom,
                           dataBis=dataBis
                           )


@app.route('/masina', methods=['GET', 'POST'])
def masina():
    print(sys._getframe().f_code.co_name, request.method)
    app_masina = Masina('static/wdb.ini')
    dataFrom, dataBis = app_masina.default_interval
    alim_type = None
    if request.method == 'POST':
        print(request.method)
        if "submit_request" in request.form:
            month = request.form['month']
            alim_type = request.form['type']
            if alim_type == 'all':
                alim_type = None
            dataFrom = request.form['dataFrom']
            dataBis = request.form['dataBis']
            if month != 'interval':
                dataFrom, dataBis = app_masina.get_monthly_interval(month)
            elif month == 'interval' and (dataFrom == '' or dataBis == ''):
                dataFrom, dataBis = app_masina.default_interval
            else:
                try:
                    dataFrom = datetime.strptime(dataFrom, "%Y-%m-%d")
                    dataBis = datetime.strptime(dataBis, "%Y-%m-%d")
                except:
                    print(traceback.format_exc())
        elif "add_alim" in request.form:
            print("add_alim")
            date = request.form['data']
            alim_type = request.form['type']
            brutto = request.form['brutto']
            amount = request.form['amount']
            km = request.form['km']

            ppu = round(float(brutto)/float(amount), 3)
            columns = ['data', 'type', 'brutto', 'amount', 'ppu', 'km']
            values = [date, alim_type, brutto, amount, ppu, km]
            app_masina.insert_new_alim(columns, values)
        else:
            print("AAAA")

    alimentari = app_masina.get_alimentari_for_interval_type(dataFrom, dataBis, alim_type)
    return render_template('masina.html',
                           userDetails=alimentari,
                           total=app_masina.total_money,
                           tot_el=app_masina.tot_electric,
                           tot_benz=app_masina.tot_benzina,
                           dataFrom=dataFrom.date(),
                           dataBis=dataBis.date(),
                           # tot_lm=tot_lm,
                           # lm_benz=lm_benz,
                           # lm_elec=lm_elec,
                           # date_from=date_from.date()
                           )


if __name__ == "__main__":
    app.run(debug=True)
