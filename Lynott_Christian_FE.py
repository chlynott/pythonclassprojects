from datetime import date, datetime

class Customer: 
    def __init__(self):
        self.custid = None
        self.name = None
        self.dob = None
        self.phone = None
        self.currentassigned = None

    def get_age(self):
        today = date.today()
        return today.year - self.dob.year - ((today.month, today.day) < (self.dob.month, self.dob.day))
    
    def is_eligble(self):
        return self.get_age() >= 25   

class Vehicles:
    def __init__(self):
        self.make = "Ford"
        self.model = "Explorer"
        self.year = "2018" 
        self.vin = "Vin: 12354678910"
    
    def __str__(self):
        return "Vehicle Assigned:\n {0} {1}\n {2} ".format(self.make, self.model, self.vin)
    
    def assign_vehicle(self, customer):
        if customer.is_eligble():
            self.customer = customer
        else:
            raise ValueError()

def maintest():
    mycust = Customer()
    mycust.custid = input("Please enter the customers Id: ")
    mycust.name = input("Please enter the customers name: ")
    mycust.dob = datetime.strptime(input("Please enter customer dob (mm/dd/yyyy): "), '%m/%d/%Y')
    mycust.phone = input("Please enter the customers phone number: ")
    mycust.currentassigned = input("Please enter the vehicle currently assigned to customer: ")

    print("Customer Information:")
    print("Id:             ", mycust.custid)
    print("Name:           ", mycust.name)
    print("Phone Number:   ", mycust.phone)
    print("Current Vehicle:", mycust.currentassigned)
    print("Date of Birth:  ", mycust.dob)

    try:
        vehicle = Vehicles()
        vehicle.assign_vehicle(mycust)
        print ("Customer Name:", mycust.name)
        print ("Customer ID:  ", mycust.custid)
        print(vehicle)
    except ValueError:
        print("Customer is not eligible to rent a vehicle")

if __name__ == "__main__":
    maintest()
    