from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
import pandas as pd
import numpy as np
from sklearn.metrics import accuracy_score, recall_score, f1_score
from sklearn.model_selection import StratifiedKFold
import os
import json

from typing import Tuple
from os.path import join

from adaptive_padding.experiment.evaluation import ExperimentConfiguration


class Experiment:
	def __init__(self, padding_strategy, ground_truth_folder_features, padding_folder_features):
		"""
		Initializes the variables used throughout the experiment. 
		
		Parameters:
		paddingStrategy: padding strategy evaluated (can take the following values: 100, 500, 700, 900, Exponential, Linear, Mouse_elephant, Random, Random255, and MTU).
		groundTruthFolderFeatures: folder where files with IoT traffic features are located;
		paddingFolderFeatures: folder where the files with traffic features modified by the padding strategy are located.
		"""
		self.filenames = ['16-09-25.csv', '16-09-26.csv','16-09-27.csv','16-09-28.csv','16-09-29.csv','16-09-30.csv','16-10-01.csv','16-10-02.csv','16-10-03.csv','16-10-04.csv','16-10-05.csv','16-10-06.csv','16-10-07.csv','16-10-08.csv','16-10-09.csv','16-10-10.csv','16-10-11.csv','16-10-12.csv']
		self.__padding_strategy = padding_strategy
		self.__ground_truth_folder_features = ground_truth_folder_features
		self.__padding_folder_features = padding_folder_features

		self.rfc = RandomForestClassifier()
		self.svc = SVC()
		self.dtc = DecisionTreeClassifier()
		self.knn = KNeighborsClassifier(n_neighbors = 5)
		self.skf = StratifiedKFold(n_splits=10)

		self.rfc_dict = [[], [], []]
		self.svc_dict = [[], [], []]
		self.dtc_dict = [[], [], []]
		self.knn_dict = [[], [], []]

		self.classifiers = {
			self.rfc: self.rfc_dict,
			self.svc: self.svc_dict,
			self.dtc: self.dtc_dict,
			self.knn: self.knn_dict}

	def compute_classifier_performance(self) -> Tuple[float, float, float]:
		"""
		Calculates accuracy, recall, and F1-score metric values. 
		"""
		self.accuracy = accuracy_score(self.y_test, self.y_pred)
		self.recall = recall_score(self.y_test, self.y_pred, average='micro')
		self.f1_measurement = f1_score(self.y_test, self.y_pred, average='micro')
		return self.accuracy, self.recall, self.f1_measurement

	def write_file(self, classifier, traffic_filename, filename):
		"""
		Write the values of the accuracy, recall, and F1-score metrics in a text file.  

		Parameters:
		classifier: classifier name.
		trafficFilename: name of the CSV file that stores the data coming from the IoT traffic. 
		filename: file name in which accuracy, recall, and F1-score metric values are written.
		"""
		with open(filename, mode='a') as file_writer:
			file_writer.write(f"{traffic_filename} ------ {classifier}.\n")
			file_writer.write(f"accuracy: {self.accuracy}.\n")
			file_writer.write(f"recall: {self.recall}.\n")
			file_writer.write(f"f1_score: {self.f1_measurement}.\n")
			file_writer.write("\n\n######################################")
	
	def update_classifiers_performance(self, classifier):
		"""
		Stores the accuracy, recall and F1-score for each classifier evaluated in each analyzed dataset. 

		Parameters:
		classifier: name of the evaluated classifier. 
		""" 
		self.classifiers[classifier][0].append(self.accuracy)
		self.classifiers[classifier][1].append(self.recall)
		self.classifiers[classifier][2].append(self.f1_measurement)
	
	def save_classifiers_performance_to_file(self, filename: str):
		"""
		It stores the average, minimum and maximum values of accuracy, recall and F1-score metrics for each evaluated classifier in a file. 

		Parameters:
		filename: name of the file in which the results obtained in the experiment will be stored. 
		"""
		for classifier in self.classifiers:
			with open(filename, mode='a') as file_writer:
				file_writer.write("\n\n\n")
				file_writer.write(f"{classifier}.\n")
				file_writer.write("Average accuracy: %s\n"%(np.mean(self.classifiers[classifier][0])))
				file_writer.write("Min accuracy: %s\n"%(np.min(self.classifiers[classifier][0])))
				file_writer.write("Max accuracy: %s\n"%(np.max(self.classifiers[classifier][0])))
				file_writer.write("Average recall: %s\n"%(np.mean(self.classifiers[classifier][1])))
				file_writer.write("Min recall: %s\n"%(np.min(self.classifiers[classifier][1])))
				file_writer.write("Max recall: %s\n"%(np.max(self.classifiers[classifier][1])))
				file_writer.write("Average f1_score: %s\n"%(np.mean(self.classifiers[classifier][2])))
				file_writer.write("Min f1_score: %s\n"%(np.min(self.classifiers[classifier][2])))
				file_writer.write("Max f1_score: %s\n"%(np.max(self.classifiers[classifier][2])))
	
	def run_train_test_split(self):
		"""
		It performs an experiment in which classifiers are trained with features calculated from the original IoT traffic, while testing these models with features calculated from the traffic changed by padding strategy. 
		"""
		for filename in self.filenames:
			self.train_data = pd.read_csv(os.path.join(self.__ground_truth_folder_features, f"{filename}_features.csv"))
			self.test_data = pd.read_csv(os.path.join(self.__padding_folder_features, self.__padding_strategy, f"{filename}.csv_features.csv"))

			self.X_train = self.train_data[['avg', 'std', 'total']]
			self.y_train = self.train_data['label']

			self.X_test = self.test_data[['avg', 'std', 'total']]
			self.y_test = self.test_data['label']

			for classifier in self.classifiers:
				classifier.fit(self.X_train, self.y_train)

			for classifier in self.classifiers:
				self.y_pred = classifier.predict(self.X_test)
				self.accuracy, self.recall, self.f1_measurement = self.compute_classifier_performance()
				
				self.update_classifiers_performance(classifier)
				self.write_file(classifier, filename, f"{self.__padding_strategy}_train_test_split.txt")

		self.save_classifiers_performance_to_file(f"{self.__padding_strategy}_train_test_split.txt")

	def run_cross_validation(self):
		"""
		Evaluates classifiers only on the attributes of traffic changed by padding strategies. 
		Models are trained and tested on the same datasets using the cross-validation technique. 
		"""
		for filename in self.filenames:
			self.test_data = pd.read_csv(os.path.join(self.__padding_folder_features, self.__padding_strategy, f"{filename}.csv_features.csv"))

			self.X = self.test_data[['avg', 'std', 'total']].values
			self.y = self.test_data['label'].values

			for train_index, test_index in self.skf.split(self.X, self.y):
				self.X_train, self.X_test = self.X[train_index], self.X[test_index]
				self.y_train, self.y_test = self.y[train_index], self.y[test_index]

				for classifier in self.classifiers:
					classifier.fit(self.X_train, self.y_train)

				for classifier in self.classifiers:
					self.y_pred = classifier.predict(self.X_test)
					self.accuracy, self.recall, self.f1_measurement = self.compute_classifier_performance()
					
					self.update_classifiers_performance(classifier)
					self.write_file(classifier, filename, f"{self.__padding_strategy}_cross_validation.txt")

		self.save_classifiers_performance_to_file(f"{self.__padding_strategy}_cross_validation.txt")


if __name__ == "__main__":
	configuration_file = os.path.join("Data", "Configuration", "experiment_configuration.json")
	experiment_configuration = ExperimentConfiguration()
	setup = experiment_configuration.load_configuration(configuration_file)
	strategy = setup["paddingStrategy"]
	experiment = Experiment(
		padding_strategy=strategy,
		ground_truth_folder_features=join("Data", "Processed", "ground_truth_features"),
		padding_folder_features=join("Data", "Processed", "padding_features"))
	experiment.run_train_test_split()
