from sklearn.svm import SVC
from plotcurve import plot_learning_curve
from sklearn.model_selection import ShuffleSplit
import matplotlib.pyplot as plt
import numpy as np
import pickle
from sklearn.decomposition import PCA

#加载特征向量
energys = np.loadtxt("/home/newsun/DSP/DSP_lab/feature/energys_conv.txt")
nums = np.loadtxt("/home/newsun/DSP/DSP_lab/feature/nums.txt")

#训练
cv = ShuffleSplit(n_splits=100, test_size=0.2, random_state=0)
energys_pca = PCA(n_components=20).fit_transform(energys)
clf = SVC(kernel='rbf',decision_function_shape='ovo')
title = r"Learning Curves (SVM+PCA)"
#画学习曲线
plot_learning_curve(
    clf, title, energys_pca, nums,  ylim=(0.7, 1.01), cv=cv, n_jobs=4
)
plt.show()
# with open('svm_pca.pickle','wb') as fw:
#     pickle.dump(clf,fw)

# #导入模型
# with open('svm_pca.pickle','rb') as fr:
#     svm_pca_clf = pickle.load(fr)

# #测准确率
# f = 0
# t = 0
# for i in range(len(energys)-2):
#     result = svm_pca_clf.predict(energys_pca[i:i + 1])
#     if(result == nums[i]):
#         t = t + 1 
#     else:
#         f = f + 1
# print("accuracy:" + str(t/(t+f)))