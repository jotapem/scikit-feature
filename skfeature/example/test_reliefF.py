import scipy.io
from sklearn.model_selection import KFold
from sklearn import svm
from sklearn.metrics import accuracy_score
from skfeature.function.similarity_based import reliefF


def main():
    # load data
    mat = scipy.io.loadmat('../data/COIL20.mat')
    X = mat['X']    # data
    X = X.astype(float)
    y = mat['Y']    # label
    y = y[:, 0]
    n_samples, n_features = X.shape    # number of samples and number of features

    # split data into 10 folds
    ss = KFold(n_splits=10, shuffle=True)

    # perform evaluation on classification task
    num_fea = 100    # number of selected features
    clf = svm.LinearSVC()    # linear SVM

    correct = 0
    for train, test in ss.split(X):
        # obtain the score of each feature on the training set
        score = reliefF.reliefF(X[train], y[train])

        # rank features in descending order according to score
        idx = reliefF.feature_ranking(score)
        # print(idx)
        assert len(idx) == n_features # OPTIMIZATION POINT

        # obtain the dataset on the selected features
        selected_features = X[:, idx[0:num_fea]]
        print(selected_features)

        # train a classification model with the selected features on the training dataset
        clf.fit(selected_features[train], y[train])

        # predict the class labels of test data
        y_predict = clf.predict(selected_features[test])

        # obtain the classification accuracy on the test data
        acc = accuracy_score(y[test], y_predict)
        correct = correct + acc

    # output the average classification accuracy over all 10 folds
    print 'Accuracy:', float(correct)/10

if __name__ == '__main__':
    main()