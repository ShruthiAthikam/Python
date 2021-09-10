##def calculate(base,exponent):
##    if exponent == 0:
##        return 1
##    elif exponent%2 == 0:
##        return calculate(base*base,exponent/2)
##    else:
##        return base*calculate(base,exponent-1)
##
##print(calculate(8,3))



from datetime import datetime
birthday = datetime(1998,2,8)
birthday = birthday.strftime("%B+%d+%Y+%A")
print(birthday)


car = "PORSCHE"
color = "red"
print(car.join(color))

message = "01233333"
print(message[:3])
