from sklearn.neural_network import MLPClassifier
from plotcurve import plot_learning_curve
from sklearn.model_selection import ShuffleSplit
import numpy as np
import pickle
import matplotlib.pyplot as plt
#加载特征向量
energys = np.loadtxt("/home/newsun/DSP/DSP_lab/feature/energys_conv.txt")
nums = np.loadtxt("/home/newsun/DSP/DSP_lab/feature/nums.txt")
MLP = MLPClassifier().fit(energys,nums)
plt.xlabel("times")

plt.plot(MLP.loss_curve_)
plt.title("loss")
plt.show()
# title = r"Learning Curves (MNB)"
# cv = ShuffleSplit(n_splits=100, test_size=0.2, random_state=0)
# #画学习曲线
# plot_learning_curve(
#     MLP, title, energys, nums,  ylim=(0.7, 1.01), cv=cv, n_jobs=4
# )
# plt.show()
f = 0
t = 0
for i in range(len(energys)-2):
    result = MLP.predict(energys[i:i + 1])
    if(result == nums[i]):
        t = t + 1 
    else:
        f = f + 1
print("accuracy:" + str(t/(t+f)))