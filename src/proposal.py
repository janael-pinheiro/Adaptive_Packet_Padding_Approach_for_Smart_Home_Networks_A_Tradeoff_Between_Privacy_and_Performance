"""
Implements the packet padding proposal presented in the paper "Adaptive Packet Padding Approach for Smart Home Networks: A Tradeoff Between Privacy and Performance".
"""
from random import randint
import os
import glob
import codecs
import json

class invalidPaddingLevel(Exception):
    pass

class AdaptivePadding:
    def __init__(self, threshold):
        self.threshold = threshold
        self.p = 0
        self.mtuNumberBytes = 1500

    def padding100(self, length):
        
        try:
            if int(length) < self.threshold:
                self.p = self.threshold - int(length)

            elif int(length) >= self.threshold and int(length) < 200:
                self.p = 200 - int(length)

            elif int(length) >= 200 and int(length) < 300:
                self.p = 300 - int(length)
            
            elif int(length) >= 300 and int(length) < 999:
                le = 1000 - int(length)
                self.p = randint(1,le)


            elif int(length) >= 999 and int(length) <= 1399:
                le = 1400 - int(length)
                self.p = randint(1,le)

            elif int(length) >= 1400 and int(length) < self.mtuNumberBytes:
                self.p = self.mtuNumberBytes - int(length)

            self.modification = int(length) + self.p
            return self.modification

        except ValueError as e:
            raise e

    def padding500(self, length):
        try:
            if int(length) < self.threshold:
                self.p = self.threshold - int(length)

            elif int(length) >= self.threshold and int(length) < 999:
                le = 1000 - int(length)
                self.p = randint(1,le)

            elif int(length) >= 999 and int(length) <= 1399:
                le = 1400 - int(length) 
                self.p = randint(1,le)

            elif int(length) >= 1400 and int(length) < self.mtuNumberBytes:
                self.p = self.mtuNumberBytes - int(length)

            modification = int(length) + self.p
            return modification 
        
        except ValueError as e:
            raise e

    def padding700(self, length):
        try:

            if int(length) < self.threshold:
                self.p = self.threshold - int(length)

            elif int(length) >= self.threshold and int(length) < 999:
                le = 1000 - int(length)
                self.p = randint(1,le)

            elif int(length) >= 999 and int(length) <= 1399:
                le = 1400 - int(length)
                self.p = randint(1,le)

            elif int(length) >= 1400 and int(length) < self.mtuNumberBytes:
                self.p = self.mtuNumberBytes - int(length)

            self.modification = int(length) + self.p
            return self.modification
        
        except ValueError as e:
            raise e

    def padding900(self, length):
        try:
            if int(length) < self.mtuNumberBytes: 
                if int(length) < self.threshold:
                    self.p = self.threshold - int(length)

                elif int(length) > self.threshold and int(length) < 999:
                    le = 1000 - int(length)
                    self.p = randint(1,le)

                elif int(length) >= 999 and int(length) <= 1399:
                    le = 1400 - int(length)
                    self.p = randint(1,le)

                elif int(length) >= 1400:
                    self.p = self.mtuNumberBytes - int(length)

                self.modification = int(length) + self.p

                return self.modification

        except ValueError as e:
            raise e

class Experiment:
    def __init__(self, csvFolder, outputFolder, paddingLevel, packetLengthIndex):
        self.csvFolder = csvFolder
        self.outputFolder = outputFolder
        self.paddingLevel = paddingLevel
        self.packetLengthIndex = packetLengthIndex

    def writeFile(self, line, outputFile):
        """
        Write the line with information for each packet in a text file. 
        """
        with codecs.open(outputFile, "a", "ISO-8859-1") as fileWriter:
            fileWriter.write(line)

    def readFiles(self, paddingExecutor):
        """
        Loads CSV files present in a specific folder. Reads all files present in this folder and applies the specified padding strategy. 
        Each line of a file contains attributes of a packet, such as IP and MAC addresses, transport layer port and length.   
        """
        for filepath in glob.glob(self.csvFolder+"*.csv"):
            filename = os.path.basename(filepath)
            self.inputFile = codecs.open(filepath, "r", "ISO-8859-1")
            self.outputFile = os.path.join(self.outputFolder, f"{filename}.csv")

            if self.paddingLevel == 100:
                self.levelExecutor = paddingExecutor.padding100
            elif self.paddingLevel == 500:
                self.levelExecutor = paddingExecutor.padding500
            elif self.paddingLevel == 700:
                self.levelExecutor = paddingExecutor.padding700
            elif self.paddingLevel == 900:
                self.levelExecutor = paddingExecutor.padding900
            else:
                raise invalidPaddingLevel(f"{self.paddingLevel} is an invalid padding level. Please specify one of the following options: 100, 500, 700 or 900.")

            for line in self.inputFile.readlines():
                try:
                    self.length = line.split(",")[self.packetLengthIndex].replace('"',"")
                    self.modifiedLength = self.levelExecutor(self.length)
                    line = line.replace(self.length, str(self.modifiedLength))
                    self.writeFile(line, self.outputFile)
                except ValueError:
                    self.writeFile(line, self.outputFile)

class ExperimentConfiration:
	def loadConfiguration(self, filepath):
		return json.load(open(filepath, mode="r"))

if __name__ == "__main__":
    configurationFile = os.path.join("..","Data","Configuration","experimentConfiguration.json")
    experimentConfiration = ExperimentConfiration()
    setup = experimentConfiration.loadConfiguration(configurationFile)

    paddingLevel = int(setup["paddingStrategy"])
    padding = AdaptivePadding(paddingLevel)
    experiment = Experiment("../Data/Raw/", f"../Data/Processed/PaddingData/Proposal/{paddingLevel}", paddingLevel, 5)
    experiment.readFiles(padding)