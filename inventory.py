from flask import Flask, render_template, request, redirect, url_for, flash
#import pickle
from datetime import datetime
#import sqlite3
import sqlite3
import json5 as json
import psycopg2 as postgres
import webbrowser

transaction_password = 'papa'
connect = postgres.connect(dbname = 'utalmighty', user = 'postgres', password = 'utkarshin10')
#connect = sqlite3.connect(':memory:')

# cust_inst = ['RSCID', 'First_name','Last_name','Phone', 'Address', 'Shop_name', 'GST_No_adhar']
# inv_inst = ['RSGID','Name','Brand', 'HSN_CODE','Price','Date','Place', 'Size', 'Unit_of_Size', 'Quantity']
# bill_inst = ['bill_no', 'RSGID', 'Rate', 'Quantity', 'GST_rate', 'Item_Done']
# billinfo_inst = ['bill_no', 'RSCID', 'Date', 'Done', 'Additional_Cost', 'Transport_name', 'Transportation_Date', 'Bilty_No']
# trans_inst = ['transactionID','RSCID','Amount_Paid', 'Date', 'Mode', 'Description']
# untrans_inst = ['unsucessfultransactionID','RSCID','Amount_Paid', 'Date', 'Mode', 'Description']


xli = list(range(100))

def jsoncompilercust(names):
    ret = []
    for cust in names:
        di = {}
        di = {
            'name': cust[1]+' '+cust[2],
            'rscid': cust[0],
            'phone': cust[3],
            'address': cust[4],
            'shop': cust[5],
            'gst': cust[6]
        }
        ret.append(di)
    return ret
    
def jsoncompilergood(good):
    ret = []
    for cust in good:
        di = {}
        di = {
            'name': cust[1]+' '+cust[2],
            'rsgid': cust[0],
            'hsn': cust[3],
            'price': float(cust[4]),
            'size': str(cust[5]) + cust[6],
            'quantity': cust[7]
        }
        ret.append(di)
    return ret

def unpaids(unpaid):
    ret = []
    for item in unpaid:
        dic={}
        dic = {
            'rscid' : item[0],
            'name' : item[1],
            'phone' : item[2],
            'outstanding' : item[3],
        }
        ret.append(dic)
    return ret

def info(a):
    llist={
        'name': a[0][0]+" "+a[0][1],
        'phone': a[0][2],
        'address': a[0][3],
        'shop': a[0][4],
        'gst': a[0][5],
        'rscid': a[0][6]
    }
    return llist

def jsonpending(pend):
    ret = []
    for i in pend:
        dic = {
            'bill_no': i[0],
            'date': i[1],
            'name': i[2]+" "+i[3],
            'address': i[4]
        }
        ret.append(dic)
    return ret
    
def transjson(n):
    ret =[]
    for bill in n:
        di = {}
        di = {
            'bill_no': bill[1],
            'date': bill[0],
            'additional_cost': bill[2]
        }
        ret.append(di)
    return ret

def create(table_name, columns):
    ''' function for creating table. '''
    cols = ""
    for x in columns:
        cols = cols + x + ', '
    cols= cols[:-2]
    query = 'CREATE TABLE ' + table_name + ' (' + cols + ')'
    cur.execute(query)
    connect.commit()
    print('Table Created.')
    #return 'Table Created.'


def insert(table_name, columns, values):
    ''' Function for Inserting into Table. '''
    cols = ""
    for x in columns:
        cols = cols + x + ', '
    cols= cols[:-2]
    vals = ""
    for x in values:
        white = "'"
        if type(x)==int:
            x = str(x)
            white = ''
        vals = vals + white + x + white + ', '
    vals= vals[:-2]
    query = 'INSERT INTO ' + table_name + ' (' + cols + ') VALUES ' '(' + vals + ')'
    cur.execute(query)
    connect.commit()
    print('Insertion Sucessful.')

def itemsincart(items):
    li = []
    li.append({'date': items[0][6].date(),
                'additional': items[0][0]})
    for j,i in enumerate(items):
        dic = {
        'enum': j+1,
        'name': i[1]+" "+i[2]+" "+str(i[4])+" "+i[5],
        'hsn': i[3],
        'quantity': i[7],
        'rate': i[8],
        'gst': i[9],
        'rsgid': i[10]
        }
        li.append(dic)
    return(li)

def bill_number_generator():
    now = datetime.now()
    current_date = now.strftime("%Y%m")
    cur.execute('SELECT bill_no FROM Billinfo ORDER BY bill_no DESC LIMIT 1')
    n = str((cur.fetchone())[0])
    if n[-5:-3] != current_date[-2:]:
        bilno = int(current_date[2:]+'000')
    else:
        d = str(int((n)[4:])+1)
        bilno = int((n)[:-len(d)]+d)
    print('BILL NUMBER is = ', bilno)
    return bilno

cur = connect.cursor()

logged = 0
mess = 0
verify = 0
inv = Flask(__name__)
inv.secret_key = 'donotsharewithanyone.this is for cookies'

# # To run when first launch ===
#insert('Customer', cust_inst, ['RSC0000', 'Utkarsh', 'Jaiswal', 7309550287, 'Rakabganj', 'RS Traders', '09AACCB6672L1Z8'])
#insert('Inventory',  ['RSGID','Name','Brand', 'HSN_CODE','Price','Place', 'Size', 'Unit_of_Size', 'Quantity'] ,['RSG0000', 'Laptop', 'Asus', 8471 , 98000, 'Dunagga', 1, 'Qty', 1])
#bill number also. 


@inv.route('/')
@inv.route('/home')
def welcome():
    now = datetime.now()
    current_time = now. strftime("%H:%M")
    current_date = now.strftime("%d/%m/%Y")
    return render_template('welcome.html', current_date = current_date, current_time = current_time)


@inv.route('/Login', methods=['POST','GET'])
def login():
    global logged
    if logged == 1:
        return render_template('dashboard.html')
    else:
        
        if request.method == "POST":
            log = request.form.get('Login')
            pas = request.form.get('pass')
            wh = request.form.get('cars')
            if log == '1235' and pas == 'ok' and wh == 'Utkarsh':
                logged = 1
                return redirect(url_for('dashboard'))
            else:
                flash('Wrong Login ID/Password.')
        return render_template('login.html')


@inv.route('/Dashboard')
def dashboard():
    if logged == 1:
        cur.execute('Select * from Customer')
        names = cur.fetchall()
        
        li = jsoncompilercust(names)

        cur.execute("""Select bi.bill_no, bi.date, first_name, last_name, address from customer as cs
                        INNER JOIN billinfo as bi
                        On bi.rscid = cs.rscid
                        where bi.done='N'""")
        pend = cur.fetchall()
        taller = jsonpending(pend) 

        unpaid_query = '''Select outstand.customer_id, concat(first_name, ' ', last_name, ' ', address) as name, phone, outstand.outstanding from customer as c
                            inner join
                            (Select due.customer_id,due.total,due.total-coalesce(paid.total_paid,0) as outstanding from
                            (Select customer_id, sum(total) as total from 
                            (Select 
                            bi.bill_no as Bill_Number,
                            bi.rscid as Customer_ID, round(sum(b.rate*b.quantity+((b.gst/100)*(b.rate*b.quantity)))+bi.additional_cost,3) as total
                            from billinfo as bi 
                            inner Join bill as b
                            on bi.bill_no = b.bill_no
                            group by bi.bill_no) as tab
                            group by customer_id
                            order by total desc) as due
                            left join 
                            (Select rscid as Customer_ID, round(sum(amount_paid), 3) as Total_Paid from transactions Group By RSCID) as paid
                            on due.customer_id = paid.customer_id) as outstand
                            on rscid = customer_id
                            where outstanding >0
                            order by outstanding desc'''
        cur.execute(unpaid_query)
        unpaid = cur.fetchall()
        unpaidjson = unpaids(unpaid)

        return render_template('dashboard.html', li = li, ta = taller, un = unpaidjson)
    else:
        return redirect(url_for('login'))


@inv.route('/logout')        
def logout():
    global logged
    global verify
    verify = 0
    logged = 0
    return redirect(url_for('login'))


@inv.route('/inventory')
def inventory():
    if logged == 1:
        return render_template('inventory.html')
    else:
        return redirect(url_for('login'))


@inv.route('/leadger')
def leadger():
    if logged == 1:
        return render_template('leadger.html')
    else:
        return redirect(url_for('login'))

@inv.route('/tally=<string:billno>', methods = ['POST', 'GET'])
def tally(billno):
    if logged == 1:
        first = """SELECT First_name, last_name, Phone, address, shop_name, gst_no_adhar as gst, bi.rscid from customer as cus
                Inner Join billinfo as bi
                on bi.rscid = cus.rscid
                where bi.bill_no = '"""+ billno +"""'"""
        cur.execute(first)
        a = cur.fetchall()
        cust = info(a)

        query = """select pqr.ad, ina.name, ina.brand, ina.hsn_code, ina.size, ina.unit_of_size ,pqr.date,  pqr.qty,pqr.rate, pqr.gst, rsgid from inventory as ina
                    Inner Join
                    (SELECT   bi.rscid as rs, bi.date as date, bi.additional_cost as ad , b.rsgid as idp ,b.quantity as qty, b.rate as rate, b.gst as gst
                    from bill as b
                    Inner Join billinfo as bi 
                    on b.bill_no = bi.bill_no
                    where bi.bill_no = '"""+ billno +"""') as pqr
                    on pqr.idp = ina.rsgid"""
        cur.execute(query)
        items = cur.fetchall()
        cart = itemsincart(items)# 0 innex has additinal cost and date of bill.
        
        got = request.form.get('iamhere')
        tally = []
        try:
            got = got[1:-3]
            y=got.split('}, {')
            for x in y:
                new = '{'+x+'}'
                tally.append(new)
        except Exception as e:
            print(e)

        if (len(tally)>0):
            for i in tally:
                x = json.loads(i)
                rsg = x['rsgid']
                print(rsg)
                num = x['quantity']
                print(num)
                query = "update bill set item_done = '"+ num +"' where bill_no = '"+ billno +"' and rsgid = '"+ rsg +"'"
                cur.execute(query)
                connect.commit()
                query2 = "update billinfo set done = 'Y' where bill_no = '"+ billno +"'"
                cur.execute(query2)
                connect.commit()

        return render_template('tally.html', cust = cust, cart= cart, billno=billno)
    else:
        return redirect(url_for('login'))


@inv.route('/order', methods = ['POST', 'GET'])
def order():
    if logged == 1:
        cur.execute('Select * from Customer')
        names = cur.fetchall()
        
        li = jsoncompilercust(names)
        
        cur.execute('Select RSGID, Name,Brand, HSN_CODE, Price ,Size, Unit_of_Size, Quantity from Inventory')
        goods = cur.fetchall()

        gli= jsoncompilergood(goods)

        got = request.form.get('sender')
        print('this is', got)
        order_list= []
        try:
            got = got[1:-3]
            y=got.split('}, {')
            for x in y:
                new = '{'+x+'}'
                order_list.append(new)
        
        except Exception:
            print(Exception)

        if(len(order_list)>0):
            bilno = bill_number_generator()

            billdts = order_list[-1] # as the last one contains the customer id and transport name
            billdts = json.loads(billdts)

            insert('billinfo', ['bill_no', 'RSCID', 'Transport_name', 'additional_cost'], [bilno, billdts['customer_id'], billdts['transport'], billdts['additional_cost']])

            for j in order_list[:-1]:# inserting order into database.
                i = json.loads(j)
                l= list(i.keys())
                l.append('bill_no')
                l1=list(i.values())
                l1.append(bilno)
                insert('bill', l, l1) 
        return render_template('order.html', li = li, good =gli)
    else:
        return redirect(url_for('login'))


@inv.route('/transaction/<string:rscid>', methods = ['POST', 'GET'])
def transaction(rscid):
    if logged == 1:
        query = "Select * from Customer where RSCID = '"+ rscid + "'"
        cur.execute(query)
        names = cur.fetchall()
        li = jsoncompilercust(names)

        query = """SELECT abc.bill_no, billinfo.date as Bill_Date, '-' as paid,Concat(' ',abc.total + billinfo.additional_cost) as billamount from
        (select bill_no, sum(amount) as total from (
        SELECT bi.bill_no, b.quantity*rate+(gst*.01*quantity*rate) as amount
        from bill as b
        Inner Join billinfo as bi 
        on b.bill_no = bi.bill_no
        where bi.rscid = '"""+ rscid +"""') AS xyz
        group by bill_no)as abc
        INNER JOIN billinfo
        on abc.bill_no = billinfo.bill_no
        UNION 
        SELECT concat('T',transactionid), date, Concat(' ',amount_paid) as paid, '-' as billamount from transactions where RSCID = '"""+rscid+"""'
        Order BY bill_date;"""
        cur.execute(query)
        table = cur.fetchall()

        if request.method == "POST":
            cons=['rscid']
            consvar = [rscid]
            amount = request.form.get('amountname')
            if amount:
                cons.append('amount_paid')
                consvar.append(amount)
            mode = request.form.get('selectmode')
            if mode:
                cons.append('mode')
                consvar.append(mode)
            des = request.form.get('descriptionname')
            if des:
                cons.append('Description')
                consvar.append(des)
            print(amount, mode, des)
            password = request.form.get('passwordname')
            if(password == transaction_password):
                insert('transactions', cons, consvar)
            else:
                insert('unsucessfultransactions', cons, consvar)
                flash('Error, no changes were made to database, please try again!')
        return render_template('transaction.html', li = li, table = table)
    else:
        return redirect(url_for('login'))


@inv.route('/quickbill', methods = ['POST', 'GET'])
def quickbill():
    if logged == 1:
        return render_template('quickbill.html')
    else:
        return redirect(url_for('login'))

@inv.route('/invoice=<string:billno>')
def invoice(billno):
    if logged == 1:
        first = """SELECT First_name, last_name, Phone, address, shop_name, gst_no_adhar as gst, bi.rscid from customer as cus
                Inner Join billinfo as bi
                on bi.rscid = cus.rscid
                where bi.bill_no = '"""+ billno +"""'"""
        cur.execute(first)
        a = cur.fetchall()
        cust = info(a)

        query = """select pqr.ad, ina.name, ina.brand, ina.hsn_code, ina.size, ina.unit_of_size ,pqr.date,  pqr.qty,pqr.rate, pqr.gst, rsgid from inventory as ina
                    Inner Join
                    (SELECT   bi.rscid as rs, bi.date as date, bi.additional_cost as ad , b.rsgid as idp ,b.quantity as qty, b.rate as rate, b.gst as gst
                    from bill as b
                    Inner Join billinfo as bi 
                    on b.bill_no = bi.bill_no
                    where bi.bill_no = '"""+ billno +"""') as pqr
                    on pqr.idp = ina.rsgid"""
        cur.execute(query)
        items = cur.fetchall()
        cart = itemsincart(items)# 0 has additinal cost and date of bill.

        return render_template('invoice.html', cust = cust, cart= cart, billno=billno)
    else:
        return redirect(url_for('login'))


@inv.route('/verifier',  methods=['POST','GET'])
def verifier():
    global verify  
    if logged == 1:  
        if request.method == "POST":
            log = request.form.get('Login')
            pas = request.form.get('pass')
            wh = request.form.get('cars')
            if log == '1235' and pas == 'ok' and wh == 'Utkarsh':
                verify = 1
                return redirect(url_for('devmode'))
            else:
                return render_template('verify.html', mess = 2)
        return render_template('verify.html', mess = 0)
    else:
         return redirect(url_for('login'))


@inv.route('/devmode')
def devmode():
    global verify
    if logged == 1:
        if verify == 1:
            verify = 0
            return render_template('devmode.html')
        else:
            return redirect(url_for('verifier'))
    else:
        return redirect(url_for('login'))
                

@inv.route('/New_Customer', methods= ['POST','GET'])
def newcust():
    cons = []
    consvar = []
    if logged == 1:
        if request.method == "POST":
            First_name = request.form.get('First')
            if First_name:
                cons.append('First_name')
                consvar.append(First_name.title())
            Last_name = request.form.get('Last')
            if Last_name:
                Last_name.title()
                cons.append('Last_name')
                consvar.append(Last_name.title())
            Phone = request.form.get('phone')
            if Phone:
                cons.append('Phone')
                consvar.append(Phone)
            Shop_name = request.form.get('shop')
            if Shop_name:
                cons.append('Shop_name')
                consvar.append(Shop_name.title())
            Address = request.form.get('Address')
            if Address:
                cons.append('Address')
                consvar.append(Address.title())
            GST_No_adhar = request.form.get('gst')
            if GST_No_adhar:
                cons.append('GST_No_adhar')
                consvar.append(GST_No_adhar.upper())
            cur.execute('SELECT RSCID from Customer ORDER BY RSCID DESC LIMIT 1')
            now = cur.fetchone()
            x= str(int((now[0])[3:])+1)
            RSCID=(now[0])[:-len(x)]+x
            cons.append('RSCID')
            consvar.append(RSCID)
            insert('Customer', cons, consvar)
            flash('Customer Added.', 'addcustomer')
            print(cons)
            print(consvar)
        return render_template('newcust.html')
    else:
        return redirect(url_for('login'))


@inv.route('/New_Item', methods= ['POST','GET'])
def newitem():
    cons = []
    consvar = []
    if logged == 1:
        if request.method == "POST":
            Name = request.form.get('name')
            if Name:
                cons.append('Name')
                consvar.append(Name.title())
            Brand = request.form.get('Brand')
            if Brand:
                cons.append('Brand')
                consvar.append(Brand.title())
            HSN_CODE = request.form.get('hsn')
            if HSN_CODE:
                cons.append('HSN_CODE')
                consvar.append(HSN_CODE)
            Price = request.form.get('Price')
            if Price:
                cons.append('Price')
                consvar.append(Price)
            Place = request.form.get('Place')
            if Place:
                cons.append('Place')
                consvar.append(Place.title())
            Size = request.form.get('size')
            if Size:
                cons.append('Size')
                consvar.append(Size)
            Unit_of_Size = request.form.get('unit')
            if Unit_of_Size:
                cons.append('Unit_of_Size')
                consvar.append(Unit_of_Size)
            Quantity = request.form.get('Quantity')
            if Quantity:
                cons.append('Quantity')
                consvar.append(Quantity)
            cur.execute('SELECT RSGID from Inventory ORDER BY RSGID DESC LIMIT 1')
            now = cur.fetchone()
            x= str(int((now[0])[3:])+1)
            RSGID=(now[0])[:-len(x)]+x
            cons.append('RSGID')
            consvar.append(RSGID)
            insert('Inventory', cons, consvar)
            flash('Item Added', 'item')
            print(cons)
            print(consvar)
        return render_template('new_item.html')
    else:
        return redirect(url_for('login'))


@inv.route('/search')
def search():
    if logged == 1:
        return render_template('search.html')
    else:
        return redirect(url_for('login'))


if __name__ == '__main__':
    inv.run(host =  '192.168.1.9',debug = True)