def show_starts_increment(number):
    for i in range(number):
        counter = 1
        starts = '*'
        while counter <= i:
            starts += '*'
            counter  = counter +1

        print(starts)

def show_starts_decrement(number):
    for i in range(number):
        counter = number
        starts = ''
        while i < counter:
            starts += '*'
            counter  = counter - 1

        print(starts)
def show_starts_increment_center(number):
    for i in range(number):
        counter = 1
        starts = '*'

        while counter <= i:
            starts += '*'
            counter  = counter +1

        spaces = ((number - len(starts)) / 2)
        if spaces.is_integer():
            message = ''
            for j in range(int(spaces)):
                message += ' '
            print(message + starts)

def show_starts_decrement_center(number):
    for i in range(number):
        counter = number
        starts = ''
        while i < counter:
            starts += '*'
            counter = counter - 1

        spaces = ((number - len(starts)) / 2)
        if spaces.is_integer():
            message = ''
            for j in range(int(spaces)):
                message += ' '
            print(message + starts)

show_starts_increment_center(15)
show_starts_decrement_center(15)