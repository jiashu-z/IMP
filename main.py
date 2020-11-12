import time

if __name__ == '__main__':
    start = time.time()
    i: int = 0
    while i < 1000000:
        if time.time() - start > 1:
            print(start)
            print(time.time())
            break
        print(i)
        i += 1
