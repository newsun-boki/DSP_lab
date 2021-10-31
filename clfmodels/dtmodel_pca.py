from sklearn.tree import DecisionTreeClassifier
from plotcurve import plot_learning_curve
from sklearn.model_selection import ShuffleSplit
import numpy as np
import pickle
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA

#加载特征向量
energys = np.loadtxt("/home/newsun/DSP/DSP_lab/feature/energys_conv.txt")
nums = np.loadtxt("/home/newsun/DSP/DSP_lab/feature/nums.txt")
#多项式贝叶斯分类模型建立
energys= PCA(n_components=20).fit_transform(energys)
dtmodel = DecisionTreeClassifier(max_leaf_nodes=8) #最大叶数为8
title = r"Learning Curves (Decision Tree + PCA)"
cv = ShuffleSplit(n_splits=100, test_size=0.2, random_state=0)
#画学习曲线
plot_learning_curve(
    dtmodel, title, energys, nums,  ylim=(0.7, 1.01), cv=cv, n_jobs=4
)
plt.show()


# #测准确率
# f = 0
# t = 0
# for i in range(len(energys)-2):
#     result = dtmodel.predict(energys[i:i + 1])
#     if(result == nums[i]):
#         t = t + 1 
#     else:
#         f = f + 1
# print("accuracy:" + str(t/(t+f)))