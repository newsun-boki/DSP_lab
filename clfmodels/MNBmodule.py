from sklearn.svm import SVC
from sklearn.naive_bayes import MultinomialNB
from plotcurve import plot_learning_curve
from sklearn.model_selection import ShuffleSplit
import numpy as np
import pickle
import matplotlib.pyplot as plt

#加载特征向量
energys = np.loadtxt("/home/newsun/DSP/DSP_lab/feature/energys_conv.txt")
nums = np.loadtxt("/home/newsun/DSP/DSP_lab/feature/nums.txt")
MNBmodle = MultinomialNB()
# MNBmodle.fit(energys,nums)
title = r"Learning Curves (MNB)"
cv = ShuffleSplit(n_splits=100, test_size=0.2, random_state=0)
#画学习曲线
plot_learning_curve(
    MNBmodle, title, energys, nums,  ylim=(0.7, 1.01), cv=cv, n_jobs=4
)
plt.show()
f = 0
t = 0
for i in range(len(energys)-2):
    result = MNBmodle.predict(energys[i:i + 1])
    if(result == nums[i]):
        t = t + 1 
    else:
        f = f + 1
print("accuracy:" + str(t/(t+f)))