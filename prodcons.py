import threading
import time
import random

# Initialize semaphore
mutex = threading.Semaphore(1)  
empty = threading.Semaphore(5)  
full = threading.Semaphore(0)   

buffer = []

num_items = 20


def producer():
    for _ in range(num_items):
        item = random.randint(1, 100)
        empty.acquire()  # decrement empty count
        mutex.acquire()  # acquire mutex lock
        if len(buffer) < 5: 
            buffer.append(item)
            print(f'Produced item {item}. Buffer: {buffer}')
            mutex.release()  # release mutex lock
            full.release()   # increment full count
        else:
            print("Buffer is full. Producer waiting...")
            mutex.release() 
            full.acquire()   
        time.sleep(random.uniform(0.1, 0.5))  #

# Consumer function
def consumer():
    for _ in range(num_items):
        full.acquire()   # decrement full count
        mutex.acquire()  # acquire mutex lock
        if len(buffer) > 0:  
            item = buffer.pop(0)
            print(f'Consumed item {item}. Buffer: {buffer}')
            mutex.release()  # release mutex lock
            empty.release()  # increment empty count
        else:
            print("Buffer is empty. Consumer waiting...")
            mutex.release()  # release mutex lock
            empty.acquire()  # wait until buffer is not empty
        time.sleep(random.uniform(0.1, 0.5)) 


producer_thread = threading.Thread(target=producer)
consumer_thread = threading.Thread(target=consumer)


producer_thread.start()
consumer_thread.start()


producer_thread.join()
consumer_thread.join()

print("Production and Consumption finished.")
