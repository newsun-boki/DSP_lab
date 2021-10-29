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
#多项式贝叶斯分类模型建立
dtmodel = DecisionTreeClassifier(max_leaf_nodes=8) #最大叶数为8
#决策树
dtmodel.fit(energys,nums)

from sklearn.model_selection import cross_val_score
cross_val_score(dtmodel,energys,nums,cv=10)  #交叉验证10次

#测准确率
f = 0
t = 0
for i in range(len(energys)-2):
    result = dtmodel.predict(energys[i:i + 1])
    if(result == nums[i]):
        t = t + 1 
    else:
        f = f + 1
print("accuracy:" + str(t/(t+f)))