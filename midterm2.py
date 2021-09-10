import sys
sys.path.append('..\question2_2')
import magic as m



def main():
    number = int(input("Enter an integer positive or negative or zero:\t"))

    if m.isMagic(str(number)):
        print(number, " is a magic number")
    else:
        print(number, " is NOT a magic number")

    


if __name__ == "__main__":
    main()
