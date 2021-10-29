from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.tree import export_graphviz
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import MultinomialNB
import numpy as np
import pickle
#加载特征向量
energys = np.loadtxt("/home/newsun/DSP/DSP_lab/feature/energys_conv.txt")
nums = np.loadtxt("/home/newsun/DSP/DSP_lab/feature/nums.txt")

#随机森林
rfcmodel = RandomForestClassifier()
rfcmodel.fit(energys,nums)
f = 0
t = 0
for i in range(len(energys)-2):
    result =rfcmodel.predict(energys[i:i + 1])
    if(result == nums[i]):
        t = t + 1 
    else:
        f = f + 1
print("accuracy:" + str(t/(t+f)))