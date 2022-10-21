import time

t_end = 0
c_time = -1


while time.time() < t_end:
    print ("contando segundos: " + str(time.time()))
print("test timer: ")
while True:
    if c_time >= t_end:
        print("Passou 5 segundos")
        c_time = -1
        t_end = 0
    if c_time == -1:
        t_end = time.time() + 5
    c_time = time.time()
    #print(c_time)

    time.time()