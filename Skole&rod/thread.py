import threading
import time

def function1 (bogstav):
    for n in range(50):
        print(bogstav, end ="")
        time.sleep(0.05)
        
if __name__ == "__main__":
    
    t1 = threading.Thread(target=function1, args=("T",))
    t2 = threading.Thread(target=function1, args=("Q",))
    t1.start()
    t2.start()
    
    #t1.join()
    for n in range(50):
        print("M", end ="")
        time.sleep(0.05)
        
    
    
    
