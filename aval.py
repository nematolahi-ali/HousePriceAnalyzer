def is_prime(n):
    if n <= 1:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True
#commit
user_input = input("ایده عدد صحیح را وارد کنید: ")
try:
    number_to_check = int(user_input)
    if is_prime(number_to_check):
        print(f"{number_to_check} عدد اول است.")
    else:
        print(f"{number_to_check} عدد اول نیست.")
except ValueError:
    print("واحد وارد شده‌ای که با یک عدد صحیح نیست. لطفا یک عدد صحیح وارد کنید.")
