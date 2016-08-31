#scikit
from sklearn.externals.six.moves import zip

#import matplotlib.pyplot as plt

from sklearn.datasets import make_gaussian_quantiles
from sklearn.ensemble import AdaBoostClassifier
from sklearn.metrics import accuracy_score
from sklearn.tree import DecisionTreeClassifier



from sklearn.ensemble import AdaBoostClassifier
from sklearn import svm
from sklearn import tree

def accuracy(yHat,y_test):
	accuracy=0
	for i in  range(0,len(y_test)):
		if(int(y_test[i])==int(yHat[i])):
			accuracy=accuracy+1

	accuracyPercentage=accuracy/float(len(y_test))
	print('Number of Training Samples='+str(TRAINING))
	print('Total Number of samples='+str(len(data)))
	print('accuracy='+str(accuracyPercentage))
	print('actual='+str(y_test))
	print('predicted='+str(yHat))


fp=open('dataAnnotatedBy2_v15.csv')
data=fp.readlines()
y=[]
x=[]
for line in data[2:]:
	line=line.split(',')
	y.append(int(line[1]))
	x.append(map(int,line[2:]))

#feature selection based on variance
#from sklearn.feature_selection import VarianceThreshold
#m_VarianceThreshold=0.3
#sel = VarianceThreshold(threshold=(m_VarianceThreshold * (1 - m_VarianceThreshold)))
#x=sel.fit_transform(x)
#print('Number of features selected:'+str(len(x[0])))

from sklearn.ensemble import RandomForestClassifier

TRAINING=300

y_training=y[0:TRAINING]
x_training=x[0:TRAINING]

fp_test=open('test_file.csv')
new_test_data=fp_test.readlines()

x_test=[]
label=[]
for line in new_test_data[1:]:
        line=line.split(',')
        #y.append(int(line[1]))
        x_test.append(map(int,line[2:]))
	label.append(line[0])


#y_test=y[TRAINING+1:]
#x_test=x[TRAINING+1:]

#model4=svm.SVC(kernel='linear')
#model4.fit(x_training,y_training)
#predictedValues4=model4.predict(x_test)
#accuracy(predictedValues4,y_test)


#model4=svm.SVC(kernel='rbf')
#model4.fit(x_training,y_training)
#predictedValues4=model4.predict(x_test)
#accuracy(predictedValues4,y_test)


#model5=tree.DecisionTreeClassifier(criterion='entropy',random_state=0)
#model5.fit(x_training,y_training)
#predictedValues5=model5.predict(x_test)
#accuracy(predictedValues5,y_test)


#clf = RandomForestClassifier(n_estimators=10)
#clf = clf.fit(x_training, y_training)
#predictedValues5=clf.predict(x_test)
#accuracy(predictedValues5,y_test)

for i in [600]:
	bdt_real = AdaBoostClassifier( DecisionTreeClassifier(max_depth=2),  n_estimators=i,  learning_rate=1)

	#bdt_discrete = AdaBoostClassifier(    DecisionTreeClassifier(max_depth=10),    n_estimators=600,    learning_rate=1.5,    algorithm="SAMME")

	ada1=bdt_real.fit(x_training, y_training)
	#ada2=bdt_discrete.fit(x_training, y_training)
	adapredict1=ada1.predict(x_test)
	for val in range(0,len(adapredict1)):
		if(adapredict1[val]==0):
			outcome="ABSENT"
		if(adapredict1[val]==1):
                        outcome="MILD"
		if(adapredict1[val]==2):
                        outcome="MODERATE"
		if(adapredict1[val]==3):
                        outcome="SEVERE"


		print(label[val]+','+outcome)
	#adapredict2=ada2.predict(x_test)
	#accuracy(adapredict1,y_test)
	#accuracy(adapredict2,y_test)






