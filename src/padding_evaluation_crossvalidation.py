from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, recall_score, f1_score
from imblearn.metrics import geometric_mean_score, specificity_score
from sklearn.model_selection import StratifiedKFold
import pandas as pd
import numpy as np
import sys

class Experiment:
	def __init__(self, paddingStrategy, groundTruthFolderFeatures, paddingFolderFeatures):
		"""
		Inicializa as variáveis usadas por esta classe.
		
		Parameters:
		- paddingStrategy:  (can assume the folliwing values: 100, 500, 700, 900, Exponential, Linear, Mouse_elephant, Random, Random255, and MTU).
		- groundTruthFolderFeatures: pasta onde estão os arquivos com os atributos do tráfego IoT;
		- paddingFolderFeatures: pasta onde estão os arquivos com atributos do tráfego modificado pelas estrátegia de padding.
		"""
		self.filenames = ['16-09-25.csv','16-09-26.csv','16-09-27.csv','16-09-28.csv','16-09-29.csv','16-09-30.csv','16-10-01.csv','16-10-02.csv','16-10-03.csv','16-10-04.csv','16-10-05.csv','16-10-06.csv','16-10-07.csv','16-10-08.csv','16-10-09.csv','16-10-10.csv','16-10-11.csv','16-10-12.csv']
		self.paddingStrategy = paddingStrategy
		self.paddingFolderFeatures = paddingFolderFeatures 
		self.groundTruthFolderFeatures = groundTruthFolderFeatures

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

def updateClassifiersPerformance(self, classifier): 
		self.classifiers[classifier][0].append(self.accuracy)
		self.classifiers[classifier][1].append(self.recall)
		self.classifiers[classifier][2].append(self.f1Score)
	
def saveClassifiersPerformanceToFile():

	for classifier in self.classifiers:
		with open(f"{self.paddingStrategy}_results.txt", mode='a') as fileWriter:
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

def run(self):
	for filename in self.filenames:
		
		self.testData = pd.read_csv(os.path.join(self.paddingFolderFeatures, self.paddingStrategy, f"{filename}.csv_features.csv"))

		self.X = self.testData[['avg','std','total']].values	
		self.y = self.testData['label'].values

		
		for train_index, test_index in skf.split(self.X,self.y):
			self.X_train, self.X_test = X[train_index], X[test_index]
			self.y_train, self.y_test = y[train_index], y[test_index]

			#train
			'''rfc.fit(self.X_train, self.y_train)
			dtc.fit(self.X_train, self.y_train)
			knn.fit(self.X_train, self.y_train)
			svc.fit(self.X_train, self.y_train)
			
			
			#test
			self.y_rfc = rfc.predict(self.X_test)
			self.y_dtc = dtc.predict(self.X_test)
			self.y_knn = knn.predict(self.X_test)
			self.y_svc = svc.predict(self.X_test)
			'''

			for classifier in self.classifiers:
				classifier.fit(self.X_train, self.y_train)

			for classifier in self.classifiers:
				self.y_pred = classifier.predict(self.X_test)
				self.accuracy, self.recall, self.f1Score = computeClassifierPerformance()
				
				updateClassifiersPerformance(classifier)
				writeFile(classifier, filename)

			for classifier in clas:
				results[classifierName][0].append(accuracy_score(self.y_test, self.y_rfc))
				results[classifierName][1].append(recall_score(self.y_test, self.y_rfc, average="micro"))
				results[classifierName][2].append(f1_score(y_test, y_rfc, average="micro"))
				results[classifierName][3].append(specificity_score(y_test, y_rfc, average="micro"))
				results[classifierName][4].append(geometric_mean_score(y_test, y_rfc, average="micro"))	
		
			results['RandomForestClassifier'][0].append(accuracy_score(y_test, y_rfc))
			results['RandomForestClassifier'][1].append(recall_score(y_test, y_rfc, average="micro"))
			results['RandomForestClassifier'][2].append(f1_score(y_test, y_rfc, average="micro"))
			results['RandomForestClassifier'][3].append(specificity_score(y_test, y_rfc, average="micro"))
			results['RandomForestClassifier'][4].append(geometric_mean_score(y_test, y_rfc, average="micro"))

			results['DecisionTreeClassifier'][0].append(accuracy_score(y_test, y_dtc))
			results['DecisionTreeClassifier'][1].append(recall_score(y_test, y_dtc, average="micro"))
			results['DecisionTreeClassifier'][2].append(f1_score(y_test, y_dtc, average="micro"))
			results['DecisionTreeClassifier'][3].append(specificity_score(y_test, y_dtc, average="micro"))
			results['DecisionTreeClassifier'][4].append(geometric_mean_score(y_test, y_dtc, average="micro"))

			results['KNeighborsClassifier'][0].append(accuracy_score(y_test, y_knn))
			results['KNeighborsClassifier'][1].append(recall_score(y_test, y_knn, average="micro"))
			results['KNeighborsClassifier'][2].append(f1_score(y_test, y_knn, average="micro"))
			results['KNeighborsClassifier'][3].append(specificity_score(y_test, y_knn, average="micro"))
			results['KNeighborsClassifier'][4].append(geometric_mean_score(y_test, y_knn, average="micro"))

			results['SVC'][0].append(accuracy_score(y_test, y_svc))
			results['SVC'][1].append(recall_score(y_test, y_svc, average="micro"))
			results['SVC'][2].append(f1_score(y_test, y_svc, average="micro"))
			results['SVC'][3].append(specificity_score(y_test, y_svc, average="micro"))
			results['SVC'][4].append(geometric_mean_score(y_test, y_svc, average="micro"))
			
	with open(f"{paddingStrategy}_classifiers_performance.txt", mode="a") as fileWriter:
		for classifierName in results.keys():
			fileWriter.write(f"{classifierName}\n")
			fileWriter.write(f"cross-validation accuracy: {results[classifierName][0]}\n")
			fileWriter.write(f"cross-validation precision: {results[classifierName][1]}\n")))
			fileWriter.write(f"cross-validations recall: {results[classifierName][2]}\n")))
			fileWriter.write(f"cross-validations f1: {results[classifierName][3]}\n")))
			fileWriter.write(f"cross-validations specificity: {results[classifierName][4]}\n")))
			fileWriter.write(f"cross-validations geometric mean: {results[classifierName][5]}\n")))


			fileWriter.write(f"mean cross-validations accuracy: {np.mean(results[classifierName][0])}")
			fileWriter.write(f"mean cross-validations precision: {np.mean(results[classifierName][1])}")
			fileWriter.write(f"mean cross-validations recall: {np.mean(results[classifierName][2])}")
			fileWriter.write(f"mean cross-validations f1: {np.mean(results[classifierName][3])}")
			fileWriter.write(f"mean cross-validations specifity: {np.mean(results[classifierName][4])}")
			fileWriter.write(f"mean cross-validations geometric mean: {np.mean(results[classifierName][5])}")