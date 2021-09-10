#!/usr/bin/env python3

#Name of the authors = Shruthi Priya Athikam (U71283931)
index = 0
def getIndex(lst, item):
    global index
    if index == len(lst):
        index = 0
        return -2
    elif lst[index] == item:
        value = index
        index = 0
        return value   
    else:
        index = index + 1
        return getIndex(lst,item) 


def main():
    lstTest = [22, -1, 0.09, 'apple', True, 5000, None, False, "present", "xyz", 90899, 777]
    print(lstTest)
    item1 = 6
    num1 = getIndex(lstTest,item1)   
    if num1 == -2:
        print(str(item1) + " doesn't exist in the list.")
    else:
        print(str(item1) + " has an index of " + str(num1))
    item2 = "present"
    num2 = getIndex(lstTest,item2)   
    if num2 == -2:
        print(str(item2) + " doesn't exist in the list.")
    else:
        print(str(item2) + " has an index of " + str(num2))
    

if __name__ == "__main__":
    main()
        
    
