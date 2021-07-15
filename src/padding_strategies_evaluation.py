from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
import pandas as pd
import numpy as np
from sklearn.metrics import accuracy_score, recall_score, f1_score
from sklearn.model_selection import StratifiedKFold
import os

class Experiment:
	def __init__(self, paddingStrategy, groundTruthFolderFeatures, paddingFolderFeatures):
		"""
		Initializes the variables used throughout the experiment. 
		
		Parameters:
		paddingStrategy: padding strategy evaluated (can take the following values: 100, 500, 700, 900, Exponential, Linear, Mouse_elephant, Random, Random255, and MTU).
		groundTruthFolderFeatures: folder where files with IoT traffic features are located;
		paddingFolderFeatures: folder where the files with traffic features modified by the padding strategy are located.
		"""
		self.filenames = ['16-09-25.csv','16-09-26.csv','16-09-27.csv','16-09-28.csv','16-09-29.csv','16-09-30.csv','16-10-01.csv','16-10-02.csv','16-10-03.csv','16-10-04.csv','16-10-05.csv','16-10-06.csv','16-10-07.csv','16-10-08.csv','16-10-09.csv','16-10-10.csv','16-10-11.csv','16-10-12.csv']
		self.paddingStrategy = paddingStrategy
		self.groundTruthFolderFeatures = groundTruthFolderFeatures
		self.paddingFolderFeatures = paddingFolderFeatures 

		self.rfc = RandomForestClassifier()
		self.svc = SVC()
		self.dtc = DecisionTreeClassifier()
		self.knn = KNeighborsClassifier(n_neighbors = 5)
		self.skf = StratifiedKFold(n_splits=10)

		self.rfc_dict = [[], [], []]
		self.svc_dict = [[], [], []]
		self.dtc_dict = [[], [], []]
		self.knn_dict = [[], [], []]

		self.classifiers = {self.rfc:self.rfc_dict, self.svc:self.svc_dict, self.dtc:self.dtc_dict, self.knn:self.knn_dict}

	def computeClassifierPerformance(self):
		"""
		Calculates accuracy, recall, and F1-score metric values. 
		"""
		self.accuracy = accuracy_score(self.y_test, self.y_pred)
		self.recall = recall_score(self.y_test, self.y_pred, average='micro')
		self.f1Score = f1_score(self.y_test, self.y_pred, average='micro')

		return self.accuracy, self.recall, self.f1Score

	def writeFile(self, classifier, trafficFilename, filename):
		"""
		Write the values of the accuracy, recall, and F1-score metrics in a text file.  

		Parameters:
		classifier: classifier name.
		trafficFilename: name of the CSV file that stores the data coming from the IoT traffic. 
		filename: file name in which accuracy, recall, and F1-score metric values are written.
		"""
		with open(filename, mode='a') as fileWriter:
			fileWriter.write(f"{trafficFilename} ------ {classifier}.\n")
			fileWriter.write(f"accuracy: {self.accuracy}.\n")
			fileWriter.write(f"recall: {self.recall}.\n")
			fileWriter.write(f"f1_score: {self.f1Score}.\n")
			fileWriter.write("\n\n######################################")
	
	def updateClassifiersPerformance(self, classifier):
		"""
		Stores the accuracy, recall and F1-score for each classifier evaluated in each analyzed dataset. 

		Parameters:
		classifier: name of the evaluated classifier. 
		""" 
		self.classifiers[classifier][0].append(self.accuracy)
		self.classifiers[classifier][1].append(self.recall)
		self.classifiers[classifier][2].append(self.f1Score)
	
	def saveClassifiersPerformanceToFile(self, filename):
		"""
		It stores the average, minimum and maximum values of accuracy, recall and F1-score metrics for each evaluated classifier in a file. 

		Parameters:
		filename: name of the file in which the results obtained in the experiment will be stored. 
		"""
		for classifier in self.classifiers:
			with open(filename, mode='a') as fileWriter:
				fileWriter.write("\n\n\n")
				fileWriter.write(f"{classifier}.\n")
				fileWriter.write("Average accuracy: %s\n"%(np.mean(self.classifiers[classifier][0])))
				fileWriter.write("Min accuracy: %s\n"%(np.min(self.classifiers[classifier][0])))
				fileWriter.write("Max accuracy: %s\n"%(np.max(self.classifiers[classifier][0])))
				fileWriter.write("Average recall: %s\n"%(np.mean(self.classifiers[classifier][1])))
				fileWriter.write("Min recall: %s\n"%(np.min(self.classifiers[classifier][1])))
				fileWriter.write("Max recall: %s\n"%(np.max(self.classifiers[classifier][1])))
				fileWriter.write("Average f1_score: %s\n"%(np.mean(self.classifiers[classifier][2])))
				fileWriter.write("Min f1_score: %s\n"%(np.min(self.classifiers[classifier][2])))
				fileWriter.write("Max f1_score: %s\n"%(np.max(self.classifiers[classifier][2])))
	
	def runTrainTestSplit(self):
		"""
		It performs an experiment in which classifiers are trained with features calculated from the original IoT traffic, while testing these models with features calculated from the traffic changed by padding strategy. 
		"""
		for filename in self.filenames:
			self.trainData = pd.read_csv(os.path.join(self.groundTruthFolderFeatures,f"{filename}_features.csv"))
			self.testData = pd.read_csv(os.path.join(self.paddingFolderFeatures, self.paddingStrategy, f"{filename}.csv_features.csv"))

			self.X_train = self.trainData[['avg','std','total']]
			self.y_train = self.trainData['label']

			self.X_test = self.testData[['avg','std','total']]
			self.y_test = self.testData['label']

			for classifier in self.classifiers:
				classifier.fit(self.X_train, self.y_train)

			for classifier in self.classifiers:
				self.y_pred = classifier.predict(self.X_test)
				self.accuracy, self.recall, self.f1Score = self.computeClassifierPerformance()
				
				self.updateClassifiersPerformance(classifier)
				self.writeFile(classifier, filename, f"{self.paddingStrategy}_train_test_split.txt")

		self.saveClassifiersPerformanceToFile(f"{self.paddingStrategy}_train_test_split.txt")

	def runCrossValidation(self):
		"""
		Evaluates classifiers only on the attributes of traffic changed by padding strategies. 
		Models are trained and tested on the same datasets using the cross-validation technique. 
		"""
		for filename in self.filenames:
			self.testData = pd.read_csv(os.path.join(self.paddingFolderFeatures, self.paddingStrategy, f"{filename}.csv_features.csv"))

			self.X = self.testData[['avg','std','total']].values	
			self.y = self.testData['label'].values

			for train_index, test_index in self.skf.split(self.X, self.y):
				self.X_train, self.X_test = self.X[train_index], self.X[test_index]
				self.y_train, self.y_test = self.y[train_index], self.y[test_index]

				for classifier in self.classifiers:
					classifier.fit(self.X_train, self.y_train)

				for classifier in self.classifiers:
					self.y_pred = classifier.predict(self.X_test)
					self.accuracy, self.recall, self.f1Score = self.computeClassifierPerformance()
					
					self.updateClassifiersPerformance(classifier)
					self.writeFile(classifier, filename, f"{self.paddingStrategy}_cross_validation.txt")

		self.saveClassifiersPerformanceToFile(f"{self.paddingStrategy}_cross_validation.txt")


if __name__ == "__main__":
	paddingStrategies = ["100", "500", "700", "900", "MTU", "Exponential", "Linear", "Mouse_elephant", "Random", "Random255"]

	for strategy in paddingStrategies:
		experiment = Experiment(paddingStrategy=strategy, groundTruthFolderFeatures="../Data/Processed/groundTruthFeatures", paddingFolderFeatures="../Data/Processed/paddingFeatures")
		experiment.runTrainTestSplit()
		experiment = Experiment(paddingStrategy=strategy, groundTruthFolderFeatures="../Data/Processed/groundTruthFeatures", paddingFolderFeatures="../Data/Processed/paddingFeatures")
		experiment.runCrossValidation()