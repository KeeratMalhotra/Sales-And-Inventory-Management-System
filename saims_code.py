import mysql.connector as con
import random

print('''
________________________________________________

WELCOME TO SALES AND INVENTORY MANAGEMENT SYSTEM 
________________________________________________

''')

mydb = con.connect(host = "localhost",passwd = "1234",user = "root")
if not mydb.is_connected():
    print("There is some error while connecting to mysql....")

#************************************creating prerequisites on mysql*****************************************
cur = mydb.cursor()
cur.execute("create database if not exists saims")
cur.execute("use saims")
cur.execute("create table if not exists login(password varchar(25) not null)")
#ADDED LINE
cur.execute('''create table if not exists purchase
(odate date not null,icode int(10) not null,iname varchar(25) not null,quantity int(10) not null,cname varchar(25) not null,amount int(10) not null) ''')
#*****************
cur.execute("create table if not exists stock(icode int(10),iname varchar(25) not null,quantity int(3) not null ,price int(10) not null,primary key(icode))")
mydb.commit()
cur.execute("select * from login;")
z=0
for i in cur :
    z=+1
if z==0 :
    cur.execute("insert into login values('123')")#DEFAULT ADMIN PASSWORD
    mydb.commit()


while True :
    print('''
1)ADMIN
2)CUSTOMER
3)EXIT
''')
    choice1 = input("Enter your choice: ")
    #*******************************************ADMIN**********************************************
    if choice1 == "1" :
        paswd = input("Enter the password : ")
        cur.execute("select * from login;")
        for i in cur :
            password, = i 
        if paswd == password :
            
            while True :
                choice2 = input('''
WOULD YOU LIKE TO :
1)ADD NEW ITEM
2)UPDATE PRICE
3)DELETE AN ITEM
4)DISPLAY ALL ITEMS
5)DISPLAY ALL PURCHASESS 
6)CHANGE THE PASSWORD
7)LOG OUT


'''
+"Enter your choice(ADMIN-WINDOW) : ")
                if choice2 == "1" :
                    while True :
                        itemcode = int(input("Enter Itemcode :"))
                        itemname = input("Enter Itemname : ")
                        quantity = int(input("Enter Quantity : "))
                        price = int(input("Enter item price : "))
                        cur.execute("insert into stock values({},'{}',{},{})".format(itemcode,itemname,quantity,price))
                        mydb.commit()
                        print("\n\n----------------ITEM ADDED SUCCESSFULLY----------------\n\n")
                        
                        c = input("\n-------------Want to add another item ?(y/n)\t")
                        if c == "n" :
                            break

                        
                elif choice2 == "2" :
                    while True :  

                        itemcode2 = int(input("Enter itemcode : "))
                        itemprice = int(input("Enter new price : "))
                        cur.execute("update stock set price = {} where icode = {}".format(itemprice,itemcode2))
                        print("\n--------PRICE SUCCESSFULLY UPDATED-------\n")
                        mydb.commit()
                        d = input("\n-------------Want to update price of any other item ?(y/n)\t")
                        if d == "n" :
                            break


                elif choice2 == "3" :
                    while True :

                        dltcode = input("Enter itemcode : ")
                        cur.execute("delete from stock where icode = {}".format(dltcode))
                        print("-------------ITEM SUCCESSFULLY DELETED-------------")
                        e = input("\n-------------Want to delete more items ?(y/n)\t")
                        if e == "n" :
                            break


                elif choice2 == "4" :
                        cur.execute("select * from stock")
                        print("\n\n||icode|iname|quantity|price||")
                        for i in cur :
                            print(i)
                        print("\n\n")

                elif choice2 == "5" :
                    cur.execute("select * from purchase")        
                    print("\n\n||order_date|item_code|item_name|quantity|cname|amount||")
                    for i in cur:
                        print(i)
                    print("\n\n")


                elif choice2 == "6" :
                    chk_pass = input("Enter current password : ")
                    cur.execute("select * from login")
                    for i in cur :
                        pswd, = i
                    if chk_pass == pswd:
                        new_pass = input("Enter new password : ")
                        cur.execute("delete from login")
                        cur.execute("insert into login values('{}')".format(new_pass))
                        mydb.commit()
                        print("\n-------------PASSWORD SUCCESSFULLY UPDATED-------------\n\n")
                    else :
                        print("\n-------ENTERED PASSWORD IS INCORRECT-------\n")
                elif choice2 == "7" :
                    break
                else :
                    ask = input("\n\n-------DO YOU WANT TO CONTINUE IN ADMIN TAB ?(Y/N)--------\n\n")
                    if ask == "n" :
                        break

        else :
            print("\n\n-------------Access Denied-------------\n\n")
            
#**************************************CUSTOMER************************************************
           
    elif choice1 == "2" :
        while True :
            
            choice3 = input('''

WOULD YOU LIKE TO :

1)ADD ITEMS TO BUCKET
2)VIEW TOTAL AMOUNT
3)VIEW ITEMS IN BUCKET
4)GO BACK

'''
+"Enter your choice(CUSTOMER-WINDOW) : ")
            if choice3 == "1" :
                cname = input("Enter customer name : ")
                randno = random.randint(100000,999999)
                table_name = cname + str(randno)
                cur.execute("use saims ")
                cur.execute('''create table {} (item_code int(10) not null,item_name varchar(25) not null,
                quantity int(10) not null,amount int(10) not null)'''.format(table_name))
                mydb.commit()
                while True :
                    #printing items to consumer**********
                    cur.execute("select icode,iname,price from stock")
                    print("\n\n||item-code|item-name|price||\n")
                    for i in cur:
                        cd,nm,prs = i
                        print("||",cd,"|",nm,"|",prs,"||\n")
                    #************************************************
                    itmcode = input("\nEnter item's code you want : ")
                    quantity_required = int(input("\nEnter item quantity : "))
                    #selecting consumer item details*****************
                    cur.execute("select * from stock where icode = {}".format(itmcode))
                    for i in cur :
                        ico,inam,quant,pris = i
                    amount = pris*quantity_required
                    rmning = quant-quantity_required
                    amount2 = pris*quant
                    #************************************************
                    if quant == 0 :
                        print("\n------------Currently the item isn't available-------------\n")
                    else:
                        if quant < quantity_required  :
                            print("\n\nWe went out of stock, but we provided you with",quant,inam)
                            cur.execute("insert into purchase values(now(),{},'{}',{},'{}',{})".format(itmcode,inam,quant,cname,amount2))#ADDED LINE
                            cur.execute("update stock set quantity = quantity - {} where icode = {}".format(quant,itmcode))
                            cur.execute("insert into {} values({},'{}',{},{})".format(table_name,itmcode,inam,quant,amount2))
                            mydb.commit()
                            
                        elif quant>=quantity_required :
                            cur.execute("insert into purchase values(now(),{},'{}',{},'{}',{})".format(itmcode,inam,quantity_required,cname,amount))#ADDED LINE
                            cur.execute("update stock set quantity = quantity - {} where icode = {}".format(quantity_required,itmcode))
                            cur.execute("insert into {} values({},'{}',{},{})".format(table_name,itmcode,inam,quantity_required,amount))
                            mydb.commit()

                    f = input("\n------Do you want to add more items ?(y/n) : ")
                    if f == "n" :
                        print("\n\n*****************YOUR ASSIGNED BUCKET PASSWORD IS : ",table_name)
                        break
                        
            elif choice3 == "2" :
                tname = input("Enter you assigned bucket password : ")
                cur.execute("select sum(amount) from {} ".format(tname))
                for i in cur :
                    final_amount, = i
                print("\n\nYOUR PAYABLE AMOUNT IS : ",final_amount)
            
            elif choice3 == "3" :
                tname = input("Enter your assigned bucket password : ")
                cur.execute("select item_name,quantity from {} ".format(tname))
                print("\n||ITEM_NAME|QUANTITY||\n")
                for i in cur :
                    i_n,qua = i
                    print("||",i_n,"|",qua,"||"+"\n\n")
                    

            elif choice3 == "4" :
                break
            else :
                print("\n\n------------ENTER A VALID CHOICE-------------\n\n")
#****************************************************************************************************************************
    elif choice1 == "3" :
        break
    else :
        print("\n\n-------Put a valid choice-------\n\n")