import os

from sklearn import svm, tree
from sklearn.datasets import make_gaussian_quantiles
from sklearn.ensemble import AdaBoostClassifier, RandomForestClassifier
from sklearn.externals.six.moves import zip
from sklearn.metrics import accuracy_score
from sklearn.tree import DecisionTreeClassifier

from data_loader import train_test, load_annotated_by_2


TRAIN_PERCENT = 80

OUTCOMES = {
    0: "ABSENT",
    1: "MILD",
    2: "MODERATE",
    3: "SEVERE"
}

def accuracy(y_hat, y_test, training_length):
    accuracy = 0
    for i in range(0,len(y_test)):
        if(int(y_test[i]) == int(y_hat[i])):
            accuracy = accuracy + 1

    accuracyPercentage = accuracy / float(len(y_test))
    print('Number of Training Samples = {}'.format(training_length))
    print('Total Number of samples = {}'.format(training_length + len(y_test)))
    print('accuracy = ' + str(accuracyPercentage))
    print('actual = ' + str(y_test))
    print('predicted = ' + str(y_hat))


x_training, y_training, x_test, y_test = train_test(
    load_annotated_by_2, train_percent=TRAIN_PERCENT
)

#feature selection based on variance
#from sklearn.feature_selection import VarianceThreshold
#m_VarianceThreshold = 0.3
#sel  =  VarianceThreshold(threshold = (m_VarianceThreshold * (1 - m_VarianceThreshold)))
#x = sel.fit_transform(x)


#model4 = svm.SVC(kernel = 'linear')
#model4.fit(x_training,y_training)
#predictedValues4 = model4.predict(x_test)
#accuracy(predictedValues4,y_test)


#model4 = svm.SVC(kernel = 'rbf')
#model4.fit(x_training,y_training)
#predictedValues4 = model4.predict(x_test)
#accuracy(predictedValues4,y_test)


#model5 = tree.DecisionTreeClassifier(criterion = 'entropy',random_state = 0)
#model5.fit(x_training,y_training)
#predictedValues5 = model5.predict(x_test)
#accuracy(predictedValues5,y_test)


#clf  =  RandomForestClassifier(n_estimators = 10)
#clf  =  clf.fit(x_training, y_training)
#predictedValues5 = clf.predict(x_test)
#accuracy(predictedValues5,y_test)

for i in [600]:
    bdt_real  =  AdaBoostClassifier( DecisionTreeClassifier(max_depth = 2),  n_estimators = i,  learning_rate = 1)

    #bdt_discrete  =  AdaBoostClassifier(    DecisionTreeClassifier(max_depth = 10),    n_estimators = 600,    learning_rate = 1.5,    algorithm = "SAMME")

    ada1 = bdt_real.fit(x_training, y_training)
    #ada2 = bdt_discrete.fit(x_training, y_training)
    adapredict1 = ada1.predict(x_test)
    for val in range(0,len(adapredict1)):
        outcome = OUTCOMES[adapredict1[val]]
        print("{},{}".format(OUTCOMES[y_test[val]], outcome))
    #adapredict2 = ada2.predict(x_test)
    accuracy(adapredict1, y_test, len(y_training))
    #accuracy(adapredict2,y_test)
