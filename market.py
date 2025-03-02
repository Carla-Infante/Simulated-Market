# File: Project3.py
# Student: Carla Infante
# UT EID: cci344
# Course Name: CS303E
#
# Date Created: 11/30/2024
# Description of Program: Simulates a simple neighborhood grocery store with one checkout line. 


################################################################################
#                                                                              #
#                       Simulation of a Simple Market                          #
#                                                                              #
################################################################################

import random
import os.path

# The following function is useful and can be used as is;  there is no 
# reason to change it. 

def addCustomer( percent ):
    """This function returns True with a certain probability.  For
      example, if percent is 35, then this returns True 35% of the 
      times you call it and returns False 65% of the time. This is 
      a useful trick in a simulation. """
    return random.randint(0, 99) < percent

def generateEventsFile( N, perc, maxItems, fileName ):
    """Create a file of N lines to drive the simulation.  Each line in the
      file contains a single non-negative integer in range
      [0...maxItems].  Lines are non-zero perc percentage of the time.
      Use the function addCustomer( percent) to decide whether the
      item should be zero or a random integer between 1 and maxItems,
      inclusive.  The idea is that if a line is zero, no new customer
      has arrived during that clock tick.  Otherwise, a new customer
      has arrived at the cashier line with that many items in their
      basket.  Remember to close the file."""

    filehandle = open(fileName, "w")

    for i in range(N):
        if addCustomer(perc) == True:
            items = random.randint(1, maxItems)
            filehandle.write(str(items) + "\n")

        else:
            filehandle.write("0" + "\n")

    filehandle.close()

    
def generateEventListFromFile( filename ):
    """Given a filename containing events, generate a list of the events
       suitable for the simulateCheckoutLine function.  Be sure to
       check that the file exists and print an error message and exit
       if not."""

    
    filehandle = open(filename, "r")
    eventList = []
    line = filehandle.readline()
    while line:
        line = line.strip()
        eventList.append(int(line))

        line = filehandle.readline()

    filehandle.close()

    return eventList
            

    

############################## Customer Class ############################## 

class Customer:

    def __init__(self, custNum, itemCount):
        """A new customer is assigned a customer number and also a number of
        items in their basket.
        """
        self.__custNum = custNum
        self.__itemCount = itemCount
        

    def getCustomerNumber(self):
        """Getter for the customer's number."""
        return self.__custNum

    def getItemsCount(self):
        """Getter for the customer's current count of items."""
        return self.__itemCount

    def decrementItemsCount(self):
        """Ring up (remove) one item from this customer's basket. 
        Typically, we'll only call this on the first customer in line."""
        if self.__itemCount > 0:
            self.__itemCount -= 1
        

    def customerFinished(self):
        """Boolean function indicating that this customer will depart on 
        the current tick, i.e., there are zero items in their basket.  
        Typically we'll only call this on the first customer in line."""
        if self.__itemCount == 0:
            return True
        else:
            return False

    def __str__(self):
        """If this is customer n with k items in basket,
        return 'Cn(k)' """
        return "C" + str(self.__custNum) + "(" + str(self.__itemCount) + ")"

############################## CheckoutLine Class ############################## 

class CheckoutLine:
    """A checkout line is implemented as a list with customers added at the front
    (L[0]) and removed from the rear (L[-1]).  Customers enter and
    move through the line.  At each tick, one item is removed from the
    basket of the first customer in line.  When their basket becomes
    empty, the first customer departs the line."""

    def __init__(self):
        """ Open a new line, with no customers initially. """
        self.__line = []
    
    def __len__(self):
        """Return the current length of the line."""
        return len(self.__line)

    def firstInLine(self):
        """ Return the first customer in the line."""
        return self.__line[0]

    def customerJoinsLine(self, cust):
        """ Add a new customer at the rear of the line.  Print a
            message indicating that the customer joined. """
        print("Customer", "C" + str(cust.getCustomerNumber()), "joining line.")
        self.__line.insert(0,cust)
        
    def customerLeavesLine(self):
        """ The first customer in line departs.  Remove the customer
            from the line and print a message. """
        print("Customer", "C" + str(self.__line[-1].getCustomerNumber()),"leaving line.")
        self.__line.pop(-1)
        

    def advanceLine( self ):
        """ If the line is empty, don't change anything.  Otherwise,
            remove one item from the basket of the first customer in
            line.  If their basket becomes empty, they leave the
            line. (Use the previous methods to implement this.)"""
        if self.__line:
            self.__line[-1].decrementItemsCount()
            if self.__line[-1].customerFinished():
                self.customerLeavesLine() 
                

    def __str__(self):
        """ Return a string that shows the current state of the line. """
        currentState = "   Line: [ "
        for element in self.__line:
            currentState += str(element) + " "

        currentState += " ]"

        return currentState

############################## Driver for the Simulation ############################## 

# The following function takes a list of events (non-negative integers) and drives
# the simulation based on the items in this list. 

def simulateCheckoutLine( eventList ):

    """This is the driver program for this system.  We monitor the
        progress of customers in the checkout line.  The eventList
        decides when a new customer is added with how many items in
        their cart. Customers are numbered as they enter. At each tick
        of the simulator clock (each new item in eventList), the
        cashier processes one item in the basket of the first
        customer."""

    print("Simulating a simple market, with one cashier.")
    print()
    
    line = CheckoutLine()
    custNum = 1
    step = 1
    for items in eventList: 
        print("Step: ", step)
        step += 1
        if items > 0:
            line.advanceLine()
            line.customerJoinsLine(Customer(custNum, items))
            custNum += 1
        elif items == 0:
            line.advanceLine()
        
        print(line)
        print()



# You could write a main function to drive the simulation;  if so, comment it out before you
# submit.


#def main():
    # Accept a filename from the user.
    #filename = input("Enter a filename: ").strip()

    # Populate the file with 10 events (integers).  Approximately
    # 50 percent are non-zero.  Each is between [1..7] (items).
    # (Play with those parameters.)
    #generateEventsFile( 10, 50, 7, filename )
    
    # From the file, generate a list of events (integers)
   # eventlist = generateEventListFromFile( filename )
   # print("The eventlist:", eventlist)

    # Use the event list to simulate the market behavior.
   # simulateCheckoutLine( eventlist )

#main()
