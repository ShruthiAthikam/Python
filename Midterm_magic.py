magicDigit = "7"

def isMagic(inputString):
    if ("-" not in inputString) and (magicDigit in inputString):
        return True
    else:
        return False

#for testing purpose
def main():
    print(isMagic("070-45"))
    
if __name__ == "__main__":
    main()
    
