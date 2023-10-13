import datetime
import sys

filename = f"{str(datetime.datetime.now()).split('.')[0].replace(':', '-')}.log"
path = f"{sys.path[0]}/logs/{filename}"


def log(message):
    print(message)
    file_object = open(path, 'a')
    file_object.write(f"{datetime.datetime.now()}: {message}\n")
    file_object.close()
