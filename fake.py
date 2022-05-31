import random
import string

def generate_random_string(length):
    letters = string.ascii_lowercase
    rand_string = ''.join(random.choice(letters) for i in range(length))
    return rand_string


with open("proxyss.txt" , "w") as file:
    for i in range(100):
        log = generate_random_string(6)
        pas = generate_random_string(6)
        ip = f'{random.randint(10,255)}.{random.randint(10,255)}.{random.randint(10,255)}.{random.randint(10,255)}'
        port = random.randint(1,8) * 1000
        file.write(log+':'+pas+'@'+ip+':'+str(port)+'\n')

with open('twits.txt' , 'w') as file:
    for i in range(500):
        log = generate_random_string(8)
        pas = generate_random_string(12)
        emails = generate_random_string(9)
        emails +='@gmail.com'
        file.write(f"{log}:{pas}:{emails}\n")
