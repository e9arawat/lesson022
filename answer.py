
"""accounting system"""
import csv
from datetime import datetime
import random
import os

# ledger_file = "ledger.csv"
class Accounting:
    
    def __init__(self,name,ledger_file='ledger.csv'):
        self.ledger_file=ledger_file
        self.name=name
        self.current_path=os.getcwd()
        self.folder_path = self.current_path+ '/'+ self.name
        
        if not os.path.exists(self.folder_path):
            os.mkdir(self.folder_path)
        
    def get_last_entry(self,filename):
        """to get the last entry from ledger"""
        with open(filename, "r", newline="", encoding="utf-8") as file:
            reader = csv.reader(file)
            last_entry = list(reader)[-1]
        return last_entry


    def get_last_balance(self,filename):
        """to get the last balance from ledger"""
        last_entry = self.get_last_entry(filename)
        return float(last_entry[5])


    def credit(self,amount):
        """this is credit func"""
        last_entry = self.get_last_entry(self.ledger_file)
        new_balance = float(last_entry[1]) + amount
        self.ledger(
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            amount,
            "credit",
            "credit transaction",
            "Not_avail",
            new_balance,
        )
        return new_balance


    def debit(self,amount):
        """Func to debit amount"""
        last_entry = self.get_last_entry(self.ledger_file)
        new_balance = float(last_entry[1]) - amount
        self.ledger(
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            amount,
            "debit",
            "debit transaction",
            "Not_avail",
            new_balance,
        )
        return new_balance


    def transaction(self,amount, category, desc, mode_of_payment, credit=False):
        """Function to make a transaction"""

        if credit:
            credit(amount)
        else:
            self.debit(amount)
        return self.get_last_balance(self.ledger_file)


    def ledger(self,date, amount, category, desc, mode_of_payment, balance):
        """Function to store all information in ledger"""
        with open(self.ledger_file, "a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow([date, amount, category, desc, mode_of_payment, balance])


    def generate_category_report(self,filename):
        """Function to generate category report"""
        with open(filename, "r", newline="", encoding="utf-8") as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                cat_data=[]
                cat_data.append([row[0],row[2],row[1]])

            category_filename = self.folder_path +"/category.csv"
            with open(
                category_filename, "w", newline="", encoding="utf-8"
            ) as category_file:
                writer = csv.writer(category_file)
                writer.writerow(["date", "Category", "Amount"])
                writer.writerows(cat_data)


    def generate_payment_report(self,filename):
        """to generate payment report"""
        with open(filename, "r", newline="", encoding="utf-8") as file:
            reader = csv.reader(file)
            for row in reader:
                pay_data=[]
                pay_data.append([row[0],row[4],row[1]])

            payment_filename = self.folder_path +"/payment.csv"
            with open(payment_filename, "w", newline="", encoding="utf-8") as payment_file:
                writer = csv.writer(payment_file)
                writer.writerow(["date", "Mode Of Payment", "amount"])
                writer.writerows(pay_data)


    def print_reports(self):
        """print report"""
        categories = set()
        months = set()
        years=set()
        data = {}

        with open(self.ledger_file, "r", newline="", encoding="utf-8") as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                print(row)
                date = datetime.strptime(row[0], "%Y-%m-%d %H:%M:%S")
                month = date.strftime("%B")
                year=date.strftime("%Y")
                category = row[2]
                categories.add(category)
                months.add(month)
                years.add(year)     

                if category not in data:
                    data[category] = {}
                
                if 'Year' not in data[category]:
                    data[category]['Year'] = year
                if month not in data[category]:
                    data[category][month] = 0
                    data[category][month] += float(row[1])    
                    
                all_months = sorted(list(months))
                # print(data[category]['Year'])
        print("\t".join(["Category"] + ["Year"] + all_months))
        for category, month_data in data.items():
            values = [f"{month_data.get(month, 0):.2f}" for month in all_months]
            values = [data[category]['Year']] + values
            # print(values)
            print("\t".join([category] + values))

        return data


    def generate_txt(self,report_data):
        """to generate text file"""
        with open(self.folder_path +"/report.txt", "w", encoding="utf-8") as file:
            for cat, month in report_data.items():
                file.write(
                    cat
                    + "\t"
                    + "\t".join(f"{m}: {amount:.2f}" for m, amount in month.items())
                    + "\n"
                )


    def generate_random_data(self):
        """this creates random data for checking"""
        categories = ["Food", "Rent", "Utilities", "Entertainment", "Travel"]
        descriptions = ["Groceries", "Restaurant", "Internet", "Movie", "Flight"]
        modes_of_payment = ["Credit Card", "Debit Card", "Cash", "G-pay", "Paytm"]

        for _ in range(10):
            amount = round(random.randint(1000, 10000))
            category = random.choice(categories)
            desc = random.choice(descriptions)
            mode_of_payment = random.choice(modes_of_payment)
            credit_amount = random.choice([True, False])

            if credit_amount:
                self.credit(amount)
            else:
                self.debit(amount)

            self.ledger(
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                amount,
                category,
                desc,
                mode_of_payment,
                self.get_last_balance(self.ledger_file),
            )


if __name__ == "__main__":
    # acc_obj=Accounting('Gaurav')
    # acc_obj.generate_random_data()
    # report_data = acc_obj.print_reports()
    # acc_obj.print_reports()
    # acc_obj.generate_category_report('ledger.csv')
    # acc_obj.generate_payment_report('ledger.csv')
    # acc_obj.generate_txt(report_data)
    # print(acc_obj.credit(4000))
    # print(acc_obj.debit(2000))
    
    acc_obj1=Accounting('Akash')
    acc_obj1.generate_random_data()
    report_data = acc_obj1.print_reports()
    acc_obj1.print_reports()
    acc_obj1.generate_category_report('ledger.csv')
    acc_obj1.generate_payment_report('ledger.csv')
    acc_obj1.generate_txt(report_data)
    