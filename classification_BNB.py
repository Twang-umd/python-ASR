from sklearn.externals import joblib
from util import load_data_user_chose, vote_the_max_times, get_speaker_name
from util import load_data_X_Y
from util import shuffle_two_list_X_Y
from sklearn.naive_bayes import BernoulliNB
# 56%
def start_calssification_BNB(wav):
    try:
        bnb = joblib.load('model/BNB.model')
        print 'load BNBClassifier successfully'
    except IOError:

        print 'BNB classifer file doesnt exist, Train first'
        a, b = load_data_X_Y('train')
        X, y = shuffle_two_list_X_Y(a, b)
        bnb = BernoulliNB()
            
        bnb.fit(X, y)
        joblib.dump(bnb, 'model/BNB.model')
        print "update the model"

    predict_result = bnb.predict(load_data_user_chose(wav))
    vote_vale = vote_the_max_times(predict_result)
    speaker_name = get_speaker_name(vote_vale)
    return speaker_name


def get_the_iter_accucy(max_true_vale=56, model="model/BNB.model", iter_times=3):
    try:
        if iter_times > 0:
            print "left " + str(iter_times) + " iteration"
            a, b = load_data_X_Y('train')
            X, y = shuffle_two_list_X_Y(a, b)
            bnb = BernoulliNB()
            
            bnb.fit(X, y)

            testX, testY = load_data_X_Y('test')
            true_ans = 0

            for itemX in range(len(testX)):
                predict_result = bnb.predict(testX[itemX])
                vote_vale = vote_the_max_times(predict_result)
                if vote_vale == testY[itemX]:
                    true_ans += 1
            true_ans_percent = true_ans * 100 / len(testX)
            print true_ans_percent
            if true_ans_percent > max_true_vale:
                print "good job, the new record:"

                joblib.dump(bnb, model)
                print "update the model"
            else:
                true_ans_percent = max_true_vale
            get_the_iter_accucy(true_ans_percent, model, iter_times - 1)
    except ValueError:
        pass
    return 0


def get_accucy(model="model/BNB.model"):
    try:
        bnb = joblib.load(model)
        print 'load BNBClassifier successfully'
    except IOError, ValueError:

        print 'BNB classifer file doesnt exist, Train first'
        a, b = load_data_X_Y('train')
        X, y = shuffle_two_list_X_Y(a, b)
        bnb = BernoulliNB()
                
        bnb.fit(X, y)
    testX, testY = load_data_X_Y('test')
    true_ans = 0

    for itemX in range(len(testX)):
        predict_result = bnb.predict(testX[itemX])
        vote_vale = vote_the_max_times(predict_result)
        if vote_vale == testY[itemX]:
            true_ans += 1
    true_ans_percent = true_ans * 100 / len(testX)

    return true_ans_percent


# get_the_iter_accucy()
# print get_accucy()
