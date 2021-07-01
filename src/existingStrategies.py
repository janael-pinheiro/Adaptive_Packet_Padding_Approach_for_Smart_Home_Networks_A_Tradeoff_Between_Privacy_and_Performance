"""
It implements the main packet padding strategies in the literature. 
"""
from random import randint
import os
import math
import glob
import codecs

class ExistingPadding:
    def __init__(self):
        self.p = 0
        self.mtuNumberBytes = 1500

    def exponential(self, length):
        
        try:
            
            if int(length) < 1024:
                self.p = 2**(int(math.log(int(length), 2))+1) - int(length)
						
            elif int(length) >= 1024 and int(length) < self.mtuNumberBytes:
                self.p = self.mtuNumberBytes - int(length)
				
            self.modification = int(length) + self.p 
            return self.modification

        except ValueError as e:
            raise e

    def linear(self, length):
        
        try:
            self.threshold = 128

            if int(length) < 1408:

                for x in range(1,12):		
                    if int(length) < x * self.threshold:
                        self.p = x * self.threshold - int(length)
                        break	
            
            elif int(length) >= 1409 and int(length) < self.mtuNumberBytes:
                self.p = self.mtuNumberBytes - int(length)
                
            self.modification = int(length) + self.p
            return self.modification

        except ValueError as e:
            raise e

    def mouse_elephant(self, length):
        
        try:
            if int(length) < 100:
                self.p = 100 - int(length)
						
            elif int(length) >= 100 and int(length) < self.mtuNumberBytes:
                self.p = self.mtuNumberBytes - int(length)
				

            self.modification = int(length) + self.p
            return self.modification

        except ValueError as e:
            raise e

    def mtu(self, length):
        
        try:
            self.modification = length

            if int(length) < self.mtuNumberBytes:
                self.p = self.mtuNumberBytes - int(length)
                self.modification = int(length) + self.p

            return self.modification

        except ValueError as e:
            raise e

    def random255(self, length):
        try:
            self.modification = length

            if int(length) < self.mtuNumberBytes:
                self.p = randint(1,255)
                if self.p + int(length) >= self.mtuNumberBytes: 
                    self.p = self.mtuNumberBytes - int(length)	
			
                self.modification = int(length) + self.p 
            
            return self.modification

        except ValueError as e:
            raise e

    def random(self, length):
        
        try:
            self.modification = length

            if int(length) < self.mtuNumberBytes:
                self.le = self.mtuNumberBytes - int(length)
                self.p = randint(1, self.le)	
                self.modification = int(length) + self.p 

            return self.modification

        except ValueError as e:
            raise e
        
class Experiment:
    def __init__(self, csvFolder, outputFolder, paddingStrategy, packetLengthIndex):
        self.csvFolder = csvFolder
        self.outputFolder = outputFolder
        self.paddingStrategy = paddingStrategy
        self.packetLengthIndex = packetLengthIndex

    def writeFile(self, line, outputFile):
        with codecs.open(outputFile, "a", "ISO-8859-1") as fileWriter:
            fileWriter.write(line)

    def readFiles(self, paddingExecutor):
        for filepath in glob.glob(self.csvFolder+"*.csv"):
            filename = os.path.basename(filepath)
            self.inputFile = codecs.open(filepath, "r", "ISO-8859-1")
            self.outputFile = os.path.join(self.outputFolder, f"{filename}.csv")

            if self.paddingStrategy == "Exponential":
                self.levelExecutor = paddingExecutor.exponential
            elif self.paddingStrategy == "Linear":
                self.levelExecutor = paddingExecutor.linear
            elif self.paddingStrategy == "Mouse_elephant":
                self.levelExecutor = paddingExecutor.mouse_elephant
            elif self.paddingStrategy == "MTU":
                self.levelExecutor = paddingExecutor.mtu
            elif self.paddingStrategy == "Random":
                self.levelExecutor = paddingExecutor.random
            elif self.paddingStrategy == "Random255":
                self.levelExecutor = paddingExecutor.random255

            for line in self.inputFile.readlines():
                try:
                    self.length = line.split(",")[self.packetLengthIndex].replace('"',"")
                    self.modifiedLength = self.levelExecutor(self.length)
                    line = line.replace(self.length, str(self.modifiedLength))
                    self.writeFile(line, self.outputFile)
                except ValueError:
                    self.writeFile(line, self.outputFile)

if __name__ == "__main__":
    paddingStrategy = "MTU"
    padding = ExistingPadding()
    experiment = Experiment("../Data/Raw/", f"../Data/Processed/PaddingData/Existing/{paddingStrategy}", paddingStrategy, 5)
    experiment.readFiles(padding)