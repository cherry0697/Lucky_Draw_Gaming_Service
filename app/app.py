from flask import Flask,render_template,request
from flask_apscheduler import APScheduler

import datetime

import random

from random import *

from datetime import date,time

import sqlite3 as sql

app = Flask(__name__)
scheduler = APScheduler()

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/enternew')
def new_user():
    return render_template('register.html')

@app.route('/addrec',methods=['POST','GET'])
def addrec():
    if request.method == 'POST':
        msg = ""
        try:
            nm=request.form['nm']
            ads=request.form['ads']
            pas=request.form['pas']

            with sql.connect("User_Details.db") as conn:

                curr = conn.cursor()

                all_users = curr.execute('select * from info;').fetchall()

                flag=0

                for x in all_users:
                    if(x[1]==ads):
                        flag=1
                        break;

                if flag == 0:
                    curr.execute("insert into info (Name,Username,Password) values (?,?,?)",(nm,ads,pas))
                    conn.commit()
                    msg = "Record Successfully Added"
                else:
                    msg = "Username Already Exists"

        except:
            conn.rollback()
            msg = "Error in Inserting Data"

        finally:
            return render_template("result.html",msg=msg)
            conn.close()

@app.route('/buy')
def buy_tickets():
    return render_template('purchase.html')

@app.route('/purchase',methods=['POST','GET'])
def purchase():
    if request.method == 'POST':
        msg=""
        try:
            tic=request.form['tic']
            ads=request.form['ads']
            pas=request.form['pas']

            with sql.connect("User_Details.db") as conn:

                curr = conn.cursor()

                all_users = curr.execute('select * from info;').fetchall()

                flag=0

                name = ""

                for x in all_users:
                    if(x[1]==ads and x[2]==pas):
                        name=x[1]
                        flag=1
                        break

                if flag==0:
                    msg = "Username or Password doesn't match"
                    return render_template("result.html",msg=msg)
                else:
                    with sql.connect("Ticket_Details.db") as conn1:

                        curr1 = conn1.cursor()

                        all_tickets = curr1.execute('select * from info;').fetchall()

                        flag1=0

                        for x in all_tickets:
                            if(x[0]==tic):
                                flag1=1
                                break

                        if flag1==1:
                            msg = "This Ticket is already purchased"
                            return render_template("result.html",msg=msg)
                        else:
                            curr1.execute("insert into info (Number,Username,used) values (?,?,?)",(tic,ads,0))
                            conn1.commit()
                            msg = "Ticket Purchased Successfully"
                            return render_template("result.html",msg=msg)

        except:
            conn.rollback()
            msg = "Error"

        finally:
            conn.close()

@app.route('/part')
def participate():
    return render_template('participate.html')

@app.route('/parevent',methods=['POST','GET'])
def parevent():
    if request.method == 'POST':
        msg=""
        try:
            tic=request.form['tic']
            ads=request.form['ads']
            pas=request.form['pas']

            with sql.connect("User_Details.db") as conn:

                curr = conn.cursor()

                all_users = curr.execute('select * from info;').fetchall()

                flag=0

                name = ""

                for x in all_users:
                    if(x[1]==ads and x[2]==pas):
                        name=x[1]
                        flag=1
                        break

                if flag==0:
                    msg = "Username or Password doesn't match"
                    return render_template("result.html",msg=msg)
                else:
                    with sql.connect("Ticket_Details.db") as conn1:

                        curr1 = conn1.cursor()

                        all_tickets = curr1.execute('select * from info;').fetchall()

                        flag1=0

                        for x in all_tickets:
                            if(x[0]==tic and x[1]==ads and x[2]==0):
                                flag1=1
                                break

                        if flag1==0:
                            msg = "This Ticket can't be used"
                            return render_template("result.html",msg=msg)
                        else:
                            curr1.execute("update info set used=? where Number=?",(1,tic))
                            conn1.commit()

                            with sql.connect("Part_Details.db") as conn2:
                                curr2 = conn2.cursor()
                                curr2.execute("insert into info (Number,Username) values (?,?)",(tic,ads))

                            msg = "Successfully Registered for Next Event"
                            return render_template("result.html",msg=msg)

        except:
            conn.rollback()
            msg = "Error"

        finally:
            conn.close()

@app.route('/winner')
def winner():
    with sql.connect("Winners.db") as conn:

        curr = conn.cursor()

        rows = curr.execute('select * from info;').fetchall()
        rows.reverse()

        cnt=0

        ans = []

        for x in rows:
            if cnt < 7:
                ans.append(x)
            else:
                break
            cnt = cnt + 1

        return render_template("show_winners.html",rows=ans)

def schedule():
    with sql.connect("Event_Details.db") as conn:
        curr = conn.cursor()

        prize = ["Washing Machine","Television","Refrigerator","i Phone","AC"]

        today = date.today()
        tommorrow = today+datetime.timedelta(days=1)

        time = "00:00 AM"

        ind = randint(0,4)
        p = prize[ind]

        curr.execute("insert into info (Date,Time,Prize,Used) values (?,?,?,?)",(tommorrow,time,p,0))
        conn.commit()

def game():
    with sql.connect("Event_Details.db") as conn:
        curr = conn.cursor()

        result = curr.execute("select * from info where date=? and used=?",(date.today(),0)).fetchall()

        if result:
            data = []
            for x in result:
                if x[0] == str(date.today()) and x[3] == 0:
                    data.append(str(x[2]))
                    break

            curr.execute("update info set used=? where date=? and used=?",(1,date.today(),0))
            with sql.connect("Part_Details.db") as conn1:

                curr1 = conn1.cursor()

                result1 = curr1.execute("select * from info;").fetchall()

                n=0

                for x in result1:
                    n=n+1

                ind = randint(0,n-1)

                n=-1

                for x in result1:
                    n=n+1
                    if n==ind:
                        data.append(str(x[1]))
                        break

                curr1.execute("delete from info")
                conn1.commit()

                with sql.connect("Winners.db") as conn2:

                    curr2 = conn2.cursor()

                    curr2.execute("insert into info (Username,Prize) values (?,?)",(data[0],data[1]))
                    conn2.commit()

@app.route('/event')
def event():
    with sql.connect("Event_Details.db") as conn:

        curr = conn.cursor()

        rows = curr.execute('select * from info;').fetchall()

        cnt=0

        ans = []

        for x in rows:
            if cnt < 1 and x[3] == 0:
                ans.append(x)
            else:
                break
            cnt = cnt + 1

        return render_template("show_event.html",rows=ans)


if __name__ == '__main__':
    scheduler.add_job(id='schedule_event',func=schedule,trigger='interval',days=1)
    scheduler.add_job(id='schedule_game',func=game,trigger='interval',days=1)
    scheduler.start()

    app.run(debug=True)
