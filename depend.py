#Hello :)
import sqlite3
import random
from types import NoneType


con = sqlite3.connect("Main.db")
cur = con.cursor()
try:
    cur.execute('''CREATE TABLE products (plu INTEGER, ean INTEGER, category TEXT,name TEXT, price REAL, issale TEXT, saleprice REAL, stock INTEGER)''')
    cur.execute('''CREATE TABLE customers (ident INTEGER, firstname TEXT, lastname TEXT, phonenumber INTEGER, email TEXT, )''')
    
except:
    pass
    #cur.execute('''DROP TABLE products''')
    #cur.execute('''CREATE TABLE products (plu INTEGER, ean INTEGER, category TEXT,name TEXT, price REAL, issale TEXT, saleprice REAL, stock INTEGER)''')



class Product:
    #Okay so crazy idea, product is an abstraction of itself...
    ## What?
    # Yes
    def __init__(self,category,name,plu,price,stock,issale=False,saleprice=0,ean=0):
        cur.execute('''SELECT * FROM products WHERE plu={} AND ean={} AND ean != 0'''.format(plu,ean))
        test = cur.fetchone()
        if type(test) == NoneType:    
            self.__name = name
            self.__plu = plu
            self.__price = price
            self.__ean = ean
            self.__issale = issale
            self.__stock = stock
            self.__saleprice = saleprice

            cur.execute('''INSERT INTO products VALUES({},{},"{}","{}",{},"{}",{},{})'''.format(plu,ean,category,name,price,issale,saleprice,stock))
        else:
            return "PRODUCT CREATION ERROR, EAN OR PLU ALREADY IN USE"

    def __str__(self):
        cur.execute('''SELECT * FROM products WHERE plu={} AND ean={}'''.format(self.__plu,self.__ean))
        val = cur.fetchone()
        return "PLU: {} | EAN: {} | Category: {} -> {} | Price: {} | Is sale? {} Saleprice: {} | | Stock: {}".format(val[0],val[1],val[2],val[3],val[4],val[5],val[6],val[7])

    
    def update_price(plu,newprice):
        cur.execute('''UPDATE products SET price={} WHERE plu={}'''.format(newprice,plu))

    def get_price(ean="Null",plu="Null"):
        cur.execute('''SELECT * FROM products WHERE plu={} OR ean={}'''.format(plu,ean))
        val = cur.fetchone()
        if val[5] == "False":
            return val[4]
        else:
            return val[6]

    def get_stock(ean="Null",plu="Null"):
        cur.execute('''SELECT * FROM products WHERE plu={} OR ean={}'''.format(plu,ean))
        val = cur.fetchone()
        return val[7]

    def update_stock(stock,ean="Null",plu="Null"):
        # Funny story with this one eh? it took three days to realize i forgot to include stock, in the function params itself
        # To think I'm getting paid
        cur.execute('''UPDATE products SET stock={} WHERE plu={} OR ean={}'''.format(stock,plu,ean)) 

    def set_sale(issale=False,saleprice=None,plu=None,ean=None):
        if saleprice == None:
            saleprice = 0.00
        cur.execute('''UPDATE products SET issale={} saleprice = {} WHERE plu={} OR ean={}'''.format(issale,saleprice,plu,ean))

    #Returning indiv items

    def get(ean="Null",plu="Null"):
        cur.execute('''SELECT * FROM products WHERE plu={} OR ean={}'''.format(plu,ean))
        val = cur.fetchone()
        return "{},{},{},{},{},{},{},{}".format(val[2],val[3],val[0],val[4],val[7],val[5],val[6],val[1])

    def get_all():
        cur.execute('''SELECT * FROM products''')
        return cur.fetchall()

    def namesearch(name):
        cur.execute('''SELECT * FROM products WHERE name={}'''.format(name))
        return cur.fetchall()



class Customer:
    # Sus-tomer class ;)
    # Will hold everything in a nice n juicy sqlite3 table similarly to the product class
    def __init__(self,firstname,lastname,phonenumber,email="Null") -> None:
        randnum = random.randrange(10000,1000000)
        while cur.execute('''SELECT EXISTS(SELECT * FROM customers WHERE ident={})'''.format(randnum)).fetchone() == True:
            randnum = random.randrange(10000,1000000)
        if cur.execute('''SELECT * FROM customers WHERE phonenumber={}'''.format(phonenumber)).fetchone() != NoneType:
            return "Phone number already in system"
        if cur.execute('''SELECT * FROM customers WHERE email={}'''.format(email)).fetchone() != NoneType:
            return "Email address already in system"
        
        cur.execute('''INSERT INTO customers VALUES({},"{}","{}",{},"{}")'''.format(randnum,firstname,lastname,phonenumber,email))

    def search(firstname="Null",lastname="Null",phonenumber="Null",ident="Null"):
        return cur.execute('''SELECT * FROM customers WHERE ident={} OR firstname="{}" OR lastname="{}" OR phonenumber={}'''.format(ident,firstname,lastname,phonenumber)).fetchall()

    def phonesearch(phonenum):
        return cur.execute('''SELECT * FROM customers WHERE phonenumber={}'''.format(phonenum)).fetchone()


    def emailOptIn(phonenum,email):
        cur.execute('''UPDATE customers SET email="{}" WHERE phonenum={}'''.format(email,phonenum))

    def emailOptOut(phonenum):
        cur.execute('''UPDATE customers SET email="NULL" WHERE phonenum={}'''.format(phonenum))
        #Hell of a lot easier than clicking "unsubscribe" amirite?


       #('''CREATE TABLE customers (ident INTEGER, firstname TEXT, lastname TEXT, phonenumber INTEGER, email TEXT, )''')







'''
egg = Product("Meats","Egg",1234,12.99,50,True,saleprice=10,ean=1237472)
print(Product.get_price(plu=1234))

print(egg)
print("")

print(Product.get(plu=1234))'''