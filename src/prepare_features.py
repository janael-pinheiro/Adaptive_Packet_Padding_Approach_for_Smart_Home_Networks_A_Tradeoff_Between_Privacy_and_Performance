'''
This script reads the CSV files, in which padding was applied or not, and generates the files with the statistics used in the paper 'Adaptive Packet Padding Approach for Smart Home Networks: A Tradeoff Between Privacy and Performance'.
'''
import pandas as pd
import os
import glob
import json

class Features:
	def __init__(self, csvFolder, outputFolder): 
		self.csvFolder = csvFolder
		self.outputFolder = outputFolder

		self.devices ={"d0:52:a8:00:67:5e":0,"44:65:0d:56:cc:d3":1,"70:ee:50:18:34:43":2,"f4:f2:6d:93:51:f1":3,"00:16:6c:ab:6b:88":4,"30:8c:fb:2f:e4:b2":5,"00:62:6e:51:27:2e":6,"00:24:e4:11:18:a8":7,"ec:1a:59:79:f4:89":8,"50:c7:bf:00:56:39":9,"74:c6:3b:29:d7:1d":10,"ec:1a:59:83:28:11":11,"18:b4:30:25:be:e4":12,"70:ee:50:03:b8:ac":13,"00:24:e4:1b:6f:96":14,"74:6a:89:00:2e:25":15,"00:24:e4:20:28:c6":16,"d0:73:d5:01:83:08":17,"18:b7:9e:02:20:44":18,"e0:76:d0:33:bb:85":19,"70:5a:0f:e4:9b:c0":20}

	def encodeLabels(self, dataset):
		"""
		Converts the MAC address of IoT devices into integer labels. 

		Parameters:
		dataset: dataset with IoT traffic.

		Returns:
		a dataset with MAC addresses of IoT devices mapped to integer labels.
		"""
		for device in self.devices:
			dataset["src_mac"].replace(device, self.devices[device], inplace=True)

		return dataset

	def filterIoTDevices(self, dataset):
		"""
		Selects only the IoT devices present in the analyzed data.

		Parameters:
		dataset: dataset with IoT traffic.

		Returns:
		a dataset that contains only samples coming from IoT devices. 
		"""
		return dataset[dataset['src_mac'].astype(str).str.isdigit()]

	def removeTemporaryFiles(self):
		"""
		Discards temporary files.  
		"""
		for filename in ["length_avg.csv", "length_std.csv", "length_sum.csv"]:
			os.remove(filename)

	def saveFile(self, dataset, filepath):
		"""
		Stores calculated features in a file. 

		Parameters:
		dataset: dataset with IoT traffic.
		filepath: path to the CSV file where the data will be stored. 
		"""
		self.filename = os.path.basename(filepath)
		dataset.to_csv(os.path.join(self.outputFolder, f"{self.filename}_features.csv"), sep=",", index=False)

	def groupSamplesPerSecond(self, dataset):
		"""
		Calculates the average, standard deviation, and number of bytes statistics for the packet length grouped at one-second intervals. 

		Parameters:
		dataset: dataset with IoT traffic.
		"""

		dataset["Length"] = dataset["Length"].astype('int')
		
		self.g = dataset.groupby(by=["src_mac","Time"])
		self.g.mean()["Length"].to_csv("length_avg.csv",sep=",", header=False)
		self.g.sum()["Length"].to_csv("length_sum.csv",sep=",", header=False)
		self.g.std()["Length"].to_csv("length_std.csv",sep=",", header=False)

	def readDataset(self, filename):
		""""
		Loads a CSV file containing the IoT traffic in the following format: each measurement corresponds to seconds from the start of capture. 
		At a minimum, the following columns must be present in the datasets: source MAC address, frame/packet size and time instant when the capture was performed. 

		Parameters:
		filename: name of the CSV file that stores the data to be loaded. 
		"""
		return pd.read_csv(filename, low_memory=False, encoding="iso-8859-1")[["src_mac","Time","Length"]]

	def createFeatures(self):
		"""
		Builds a dataset from statistics calculated based on packet length. 
		"""		
		self.features = pd.DataFrame()
		self.features["avg"] = pd.read_csv("length_avg.csv", names=["label","Time","Length"])["Length"]
		self.features["std"] = pd.read_csv("length_std.csv", names=["label","Time","Length"])["Length"]
		self.features["total"] = pd.read_csv("length_sum.csv", names=["label","Time","Length"])["Length"]
		self.features["label"] = pd.read_csv("length_avg.csv", names=["label","Time","Length"])["label"]

		return self.features

class Experiment:
	def loadConfiguration(self, filepath):
		return json.load(open(filepath, mode="r"))

if __name__ == "__main__":
	configurationFile = os.path.join("..","Data","Configuration","experimentConfiguration.json")
	experiment = Experiment()
	setup = experiment.loadConfiguration(configurationFile)
	
	if setup["padding"] != "None" and setup["paddingStrategy"] != "None":
		paddingStrategy = setup["paddingStrategy"]
		csvFolder = os.path.join("../Data/Processed/PaddingData/", setup["padding"], f"{paddingStrategy}/")
		outputFolder = os.path.join("../Data/Processed/paddingFeatures/", paddingStrategy)
		
	else:
		csvFolder = "../Data/Raw/"
		outputFolder = "../Data/Processed/groundTruthFeatures/"

	features = Features(csvFolder, outputFolder)
	
	for filename in glob.glob(csvFolder+"*.csv"):
		dataset = features.readDataset(filename)
		dataset = features.encodeLabels(dataset)
		dataset = features.filterIoTDevices(dataset)
		dataset.drop(dataset["Length"][dataset["Length"] == "None"].index, inplace=True)
		features.groupSamplesPerSecond(dataset)		
		IoTFeatures = features.createFeatures()
		IoTFeatures.dropna(inplace=True)
		features.saveFile(IoTFeatures, filename)
			
	features.removeTemporaryFiles()