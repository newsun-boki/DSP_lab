from sklearn.svm import SVC
import numpy as np
import pickle
#加载特征向量
energys = np.loadtxt("./feature/energys_conv.txt")
nums = np.loadtxt("./feature/nums.txt")

#训练
clf = SVC(kernel='rbf',decision_function_shape='ovo').fit(energys,nums)

#保存模型
with open('svm.pickle','wb') as fw:
    pickle.dump(clf,fw)

#导入模型
with open('svm.pickle','rb') as fr:
    svm_clf = pickle.load(fr)

#测准确率
f = 0
t = 0
for i in range(len(energys)-2):
    result = svm_clf.predict(energys[i:i + 1])
    if(result == nums[i]):
        t = t + 1 
    else:
        f = f + 1
print("accuracy:" + str(t/(t+f)))