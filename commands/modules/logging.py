import datetime
import sys

filename = f"{str(datetime.datetime.now()).split('.')[0].replace(':', '-')}.log"
path = f"{sys.path[0]}/logs/{filename}"


file_object = open(path, 'a')

def log(message):
    print(message)
    file_object.write(f"{datetime.datetime.now()}: {message}\n")