#Pebis

from math import prod
from platform import freedesktop_os_release
from unicodedata import east_asian_width



class Category():
    
    def __init__(self,name) -> None:
        self.__name = name
        self.__products = []

    def __str__(self) -> str:
        return self.__name
    def add_product(self,product) -> None:
        self.__products.append(product)

    def remove_product(self,product) -> None:
        self.__products.remove(product)

    def get_products(self) -> list:
        return self.__products

    def __repr__(self) -> str:
        return "Category({})".format(self.__name) 
    




class Product():
    __pluInUse = []
    __eanInUse = []
    __products = []
    def __init__(self,plu,name,category,price,sale=(bool(False)),saleprice=(float(0.00)),ean=None,stock=0) -> None:
        if ean in Product.__eanInUse or plu in Product.__pluInUse:
            return "Product Excep, EAN or PLU in use"
        else:
            self.__name = name
            self.__plu = int(plu)
            self.__ean = int(ean)
            self.__price = float(price)
            self.__category = category
            self.__issale = sale
            self.__saleprice = saleprice
            self.__stock = stock
            self.__pluInUse.append(int(plu))
            self.__eanInUse.append(int(ean))
            self.__products.append(self)
            category.add_product(str(self))

    def __repr__(self) -> str:
        return "Product({},{},{},{},{},{},{},{})".format(self.__plu,self.__name,self.__price,self.__issale,self.__saleprice,self.__ean,self.__stock)
    def __str__(self) -> str:
        return "Cat: {}->{} ({}, EAN:{})  | Price:{} | Is on sale: {}, Normal price:{}".format(str(self.__category),self.__name,self.__plu,self.__ean,self.get_price(),self.__issale,self.__price)

    def get_name(self) -> int:
        return self.__name

    def get_plu(self) -> int:
        return self.__plu

    def get_ean(self) -> int:
        return self.__ean

    def get_stock(self):
        return self.__stock
    
    def add_stock(self,amount):
        self.__stock += amount

    def remove_stock(self,amount):
        self.__stock -= amount


    def get_price(self) -> int:
        if self.__issale == True:
            return self.__saleprice
        return self.__price

    def get_category(self) -> int:
        return self.__category

    def issale(self) -> bool:
        return self.__issale

    def sale(self,newstate,newprice=None) -> None:
        self.__category.remove_product(str(self))
        self.__issale = newstate
        self.__saleprice = newprice
        self.__category.add_product(str(self))


    def get_product(ean=None,plu=None):
        if ean != None:
            for x in Product.__products:
                if x.get_ean() == ean:
                    return x
        elif plu != None:
            for x in Product.__products:
                if x.get_plu() == plu:
                    return x
        else:
            return None


class WarehouseObj():
    __warehouse = []

    def __init__(self,product,stock) -> None:
        if product.get_plu() in WarehouseObj.__warehouse:
            return "Product Excep, Product in warehouse"
        self.__product = product
        self.__stock = int(stock)
        self.__plu = product.get_plu()
        WarehouseObj.__warehouse.append(self)


        



class shoppingCart():
    def __init__(self) -> None:
        self.__products = []

    def add_product(self,inp):
        if len(str(inp)) > 4:
            ean = inp
            plu = None
        else:
            plu = inp
            ean = None
        self.__products.append(Product.get_product(ean,plu))

    def remove_product(self,inp):
        if len(str(inp)) > 4:
            ean = inp
            plu = None
        else:
            plu = inp
            ean = None
        try:
            self.__products.remove(Product.get_product(ean,plu))
        except:
            return "Product could not be removed, invalid PLU, EAN or not in cart"

    def get_total(self):
        total = 0
        for x in self.__products:
            total += x.get_price()
        return total

    def clear_cart(self):
        self.__products = []

    def get_prods(self) -> list:
        prods = []
        for x in self.__products:
            prods.append(str(x))
        return prods




#------------------------------------------



Fresh = Category("Fresh")
Meats = Category("Meats")
egg = Product(0000,"Egg 12 pack",Fresh,1.99,ean=12345)
milk = Product(1,"Milk",Fresh,5.99,ean=155523)
steak = Product(3222,"6. Oz Steak x4",Meats,50.99,ean=124125)

print(Fresh.get_products())
print(Meats.get_products())


steak.sale(True,40.99)
print(steak.issale())
print(steak.get_price())

print(Meats.get_products())
steak.sale(False)
print(steak.get_price())
print(Meats.get_products())

print("----------")
print(Product.get_product(ean=None,plu=3222))
print("----------")
cart = shoppingCart()

cart.add_product(0000)
cart.add_product(12345)
cart.add_product(124125)
cart.remove_product(0000)
cart.remove_product(124125)
cart.remove_product(124125)
print(cart.get_prods())
print(cart.get_total())
