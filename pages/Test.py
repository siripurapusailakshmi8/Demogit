import time
def execution_time(func):
    def wrapper(*args,**kwargs):
        start = time.time()
        func(*args,**kwargs)
        end = time.time()
        result = end-start
        print("execution tme", result)
        print("after the function this is for git demo purpose")
        print("this is for gitstuff repo")
        print("the code was pulled and doing my changes now")
    return wrapper

@execution_time
def main():
    for i in range(1000):
        print(i)
main()