import scipy.io
from sklearn.metrics import accuracy_score
from sklearn.model_selection import KFold
from sklearn import svm
from skfeature.function.information_theoretical_based import FCBF


def main():
    # load data
    mat = scipy.io.loadmat('../data/colon.mat')
    X = mat['X']    # data
    X = X.astype(float)
    y = mat['Y']    # label
    y = y[:, 0]
    n_samples, n_features = X.shape    # number of samples and number of features

    # split data into 10 folds
    ss = KFold(n_splits=10, shuffle=True)

    # perform evaluation on classification task
    num_fea = 10    # number of selected features
    clf = svm.LinearSVC()    # linear SVM

    correct = 0
    for train, test in ss.split(X):
        # obtain the index of each feature on the training set
        for num_fea in range(10):
            idx = FCBF.fcbf(X[train], y[train])
            idx = idx[0]
            print(num_fea, len(idx), idx, n_features)
        # obtain the dataset on the selected features
        features = X[:, idx[0:num_fea]]

        # train a classification model with the selected features on the training dataset
        clf.fit(features[train], y[train])

        # predict the class labels of test data
        y_predict = clf.predict(features[test])

        # obtain the classification accuracy on the test data
        acc = accuracy_score(y[test], y_predict)
        correct = correct + acc

    # output the average classification accuracy over all 10 folds
    print 'Accuracy:', float(correct)/10

if __name__ == '__main__':
    main()
