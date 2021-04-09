# Lukas Elsrode - classify.py (09/08/2020)

''' Applies a variety of supervised classification methods
'''

import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import CategoricalNB
from sklearn import tree
from sklearn.neighbors import KNeighborsClassifier


def make_confusion_matrix(class_names, y_test, y_pred):
        cnf_matrix = metrics.confusion_matrix(y_test, y_pred)
        _, ax = plt.subplots()
        tick_marks = np.arange(len(class_names))
        plt.xticks(tick_marks, labels=class_names)
        plt.yticks(tick_marks, labels=class_names)

        # create heatmap
        sns.heatmap(pd.DataFrame(cnf_matrix),annot=True, cmap="YlGnBu", fmt='g')
        ax.xaxis.set_label_position("top")
        plt.tight_layout()
        plt.title('Confusion matrix', y=1.1)
        plt.ylabel('Actual label')
        plt.xlabel('Predicted label')

        for i, c in enumerate(class_names):
            print(str(i) + ' - ' + c)
        plt.show()

def classify_by_d_tree(df,var, m_type='entropy'):
    # Create & Train Model
    dtree = tree.DecisionTreeClassifier(criterion=m_type)
    # Make some predictions
    dtree.fit(X_train, y_train)
    predictions = dtree.predict(X_test)
    # Eval the accuracy of the model
    print("Accuracy of Descision Tree Model:", metrics.accuracy_score(y_test, predictions))
    make_confusion_matrix(dtree.classes_, y_test, predictions)
    show_dtree(dtree, list(X_train.columns), dtree.classes_)
    return dtree

def show_dtree(model, fns, cns):
    fig, axes = plt.subplots(nrows=1, ncols=1, figsize=(4, 4), dpi=300)
    tree.plot_tree(model, feature_names=fns, class_names=cns, filled=True)
    plt.show()
    return

def classify_by_knn(df, nn=5):

    #Create KNN Classifier
    knn = KNeighborsClassifier(n_neighbors=nn)
    #Train the model using the training sets
    knn.fit(X_train, y_train)
    #Predict the response for test dataset
    y_pred = knn.predict(X_test)
    print("Accuracy of K-nearest nieghboor model:", metrics.accuracy_score(y_test, y_pred))
    make_confusion_matrix(knn.classes_,y_test,y_pred)

    return knn
