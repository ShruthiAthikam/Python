#!/usr/bin/env python3

import csv
import sys

#Function to read money from the file
def readMoney():
    try:
        with open("money.txt",newline = "") as file:           
            rows = csv.reader(file)
            for row in rows:
                return row[0]
    except FileNotFoundError:
        print("File not found in the directory.")
        sys.exit()
    except Exception as e:
        print("An exception occured " + str(e))
        sys.exit()
      
#Function to write money to the file
def writeMoney(money):   
    with open("money.txt","w", newline = "") as file:
        writer = csv.writer(file)
        writer.writerows([[money]])

#For testing purpose
def main():
    writeMoney(250.80)
    money = readMoney()
    print(money)
    
if __name__ == "__main__":
    main()
