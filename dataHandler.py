

import sys
import os
import re

# data store meta
class Meta:
    captureDate: str
    dataRead: int
    dataWrite: int

    def __init__(self, dataRead = 0, dataWrite = 0, captureDate = "") -> None:
        self.dataRead = dataRead
        self.dataWrite = dataWrite
        self.captureDate = captureDate
    def __str__(self) -> str:
        return self.captureDate + " Read:" + str(self.dataRead) + " Write:" + str(self.dataWrite)

metaArr = []

def prepare():    
    # data path
    pathNowDir = os.getcwd()
    files = os.listdir(pathNowDir + "/data")

    # regularExp to match result
    readRe = re.compile(r"^Data Units Read:[ |0-9|,]*\[([0-9]*) GB\]$")
    writeRe = re.compile(r"^Data Units Written:[ |0-9|,]*\[([0-9]*) GB\]$")
    
    for file in files:
        if not os.path.isdir(file):
            meta = Meta()
            meta.captureDate = file[0:len(file) - 4]
            for line in open(pathNowDir + "/data/" + file):
                if line.find("Data Units Read") != -1:
                    result = re.match(readRe, line)
                    if result.group(1):
                        meta.dataRead = int(result.group(1))
                        # print(result.group(1))
                if line.find("Data Units Written") != -1:
                    result = re.match(writeRe, line)
                    if result.group(1):
                        # print(result.group(1))
                        meta.dataWrite = int(result.group(1))
            metaArr.append(meta)

    metaArr.sort(key = lambda meta: meta.captureDate, reverse=False)


def calc():
    readSum = 0
    writeSum = 0
    for i in range(1, len(metaArr)):        
        readSum += metaArr[i].dataRead - metaArr[i - 1].dataRead
        writeSum += metaArr[i].dataWrite - metaArr[i - 1].dataWrite

    le = len(metaArr) - 1
    if le == 0:
        return []
    return [
        [1.0 * readSum / le, 1.0 * writeSum / le],
        [readSum / (le / 7.0), writeSum / (le / 7.0)],
        [readSum / (le / 30.0), writeSum / (le / 30.0)]
    ]

prepare()
data = calc()


with open('./data.txt', 'w') as f:
    f.write("磁盘读写量(单位:GB)\n")
    if data != []:
        f.write("日均数据 -- read:{0}  write:{1}\n".format(data[0][0], data[0][1]))
        f.write("周均数据 -- read:{0}  write:{1}\n".format(data[1][0], data[1][1]))
        f.write("月均数据 -- read:{0}  write:{1}\n".format(data[2][0], data[2][1]))

    
