
import pandas as pd

def ordinal_numerals_ending(val):
    """
    function returns ordinal numerals text ending for respective numbers
    """
    if str(val)[-1] == "1" and str(val)[-2:] != "11":
        return "st"
    elif str(val)[-1] == "2" and str(val)[-2:] != "12":
        return "nd"
    elif str(val)[-1] == "3" and str(val)[-2:] != "13":
        return "rd"
    else:
        return "th"

class Order():

    def __init__(self, id, order, type, price, quantity):
        self.id = id
        self.order = order
        self.type = type
        self.price = price
        self.quantity = quantity

class Storage():

    def __init__(self, *args):
        self.df = pd.DataFrame(columns=["Id","Order","Type","Price","Quantity"])
        for arg in args:
            if (len(arg.id) != 3 or isinstance(arg.id,str)==False or 
                arg.order not in ["Buy","Sell"] or arg.type not in ["Add","Remove"] or 
                isinstance(arg.price, (int,float)) ==False or  arg.price <0 or 
                isinstance(arg.quantity, (int,float)) ==False or  arg.quantity <0):
                print("Invalid Order!")
            else:
                self.update_table(arg)
                    
    def update_table(self, obj):
        new_row = pd.Series({'Id':obj.id, 'Order':obj.order, 
        'Type':obj.type, 'Price':obj.price, 'Quantity':obj.quantity})
        self.df = pd.concat([self.df, new_row.to_frame().T], ignore_index = True)

    def remove_opposite_position(self):

        """
        once there are two orders with identical id, price, 
        order and quantitiy and the opposite type,
        they should be removed from the considered list of orders as it is the situation 
        when market participant withdrew from his initially taken position
        """

        for i in self.df.iterrows():
            for j in self.df.iterrows():
                if (i[1][0] == j[1][0] and i[1][1] == j[1][1] and i[1][2] != j[1][2] and
                    i[1][3] == j[1][3] and i[1][4] == j[1][4]):
                    self.df = self.df.drop(labels = [j[0],i[0]], axis=0)
                    self.df = self.df.reset_index(drop=True)
                    return self.remove_opposite_position()
        return self.df

    def show_best_orders(self):

        """
        assumptions:
        best "Sell" order -> highest price
        best "Buy" order -> lowest price
        sum of orders -> sum of all shares (quantities) of 
        the same price (min and max respectively for 'Buy' and 'Sell')
        """

        sell_orders = self.df[self.df["Order"] == "Sell" ]
        buy_orders = self.df[self.df["Order"] == "Buy" ]
        steps_counter = 0
        while sell_orders.empty == False or buy_orders.empty == False:
            if sell_orders.empty:
                steps_counter +=1
                print ("{}{} best orders: 'Buy' -> {} shares for {}, no 'Sell' offers left.".format(
                    steps_counter, ordinal_numerals_ending(steps_counter),
                    buy_orders.loc[buy_orders["Price"] == min(buy_orders["Price"]), 
                    'Quantity'].sum() , min(buy_orders["Price"])
                    ))
                buy_orders = buy_orders[buy_orders["Price"] != min(buy_orders["Price"])]
            elif buy_orders.empty:
                steps_counter +=1
                print ("{}{} best orders: 'Sell' -> {} shares for {}, no 'Buy' offers left.".format(
                    steps_counter, ordinal_numerals_ending(steps_counter),
                    sell_orders.loc[sell_orders["Price"] == max(sell_orders["Price"]), 'Quantity'].sum() , max(sell_orders["Price"])))
                sell_orders = sell_orders[sell_orders["Price"] != max(sell_orders["Price"])]
            else:
                steps_counter +=1
                print ("{}{} best orders: 'Sell' -> {} shares for {}:  'Buy' -> {} shares for {}".format(
                    steps_counter, ordinal_numerals_ending(steps_counter),
                    sell_orders.loc[sell_orders["Price"] == max(sell_orders["Price"]),'Quantity'].sum() , max(sell_orders["Price"]),
                    buy_orders.loc[buy_orders["Price"] == min(buy_orders["Price"]),
                    'Quantity'].sum() , min(buy_orders["Price"])))
                buy_orders = buy_orders[buy_orders["Price"] != min(buy_orders["Price"])]
                sell_orders = sell_orders[sell_orders["Price"] != max(sell_orders["Price"])]
            

order1 = Order("001", "Buy", "Add", 20.0, 100)
order2 = Order("002", "Sell", "Add", 25.0, 200)
order3 = Order("003", "Buy", "Add", 23.0, 50)
order4 = Order("004", "Buy", "Add", 23.0, 70)
order5 = Order("003", "Buy", "Remove", 23.0, 50)
order6 = Order("005", "Sell", "Add", 28, 100)


storage1 = Storage(order1, order2, order3, order4, order5, order6)
storage1.df
storage1.remove_opposite_position()
storage1.show_best_orders()

