def is_sushu(number):
    for item in range(2,number):
        if number%item==0:
            return False
    return True

if __name__=="__main__":
    for i in range(101,201):
        if is_sushu(i):
            print i