# 语音数字信号处理实验(DSP)

## 环境配置

我是在ubuntu18.04上运行的，Windows系统应该也问题不大

```python
pip install -r requirements.txt
```

## 文件结构
```
.
├── clfmodels  不同的分类模型   
├── corpus     给定的语料
├── energy     短时能量的输出
├── feature     用于分类器的特征向量
├── output      截取出人声的音频
├── __pycache__     缓存文件
├── utils       一些工具
└── zeroCrossingRate    过零率的输出
```
## 使用方法
### quick start
+ 直接运行 `lab1.py`
```python
python lab1.py
```
这会打开一个类似的交互式代码，你可以使用这个交互式的代码按照提示得到截取出的人声

### Train

#### 1. 获取特征向量
  
```python 
python get_feature.py
```

可以通过line11:`wav_path = "/home/newsun/DSP/DSPyuyin"`更改你的训练集的路径。
训练集为0至9单个数字，需按照以下格式排列。

```
DSPyuyin
    ├── 0
    |   ├── [2021-10-23][13-02-37].wav
    │   ├── [2021-10-23][13-02-42].wav
    |    ...
    ├── 1
    ├── 2
    ├── 3
    ├── 4
    ├── 5
    ├── 6
    ├── 7
    ├── 8
    └── 9
```
运行后会在`feature`当中生成

```
feature
├── energys_conv.txt 由短时能量构成的特征向量
└── nums.txt    标签
```
上述特征向量就是你要训练的输入。

#### 2.使用不同方法训练
在clfmodels中有各种不同的分类器模型
```
clfmodels
├── dtmodel.py  决策树  
├── dtmodel_pca.py  决策树加主成分分析
├── MNBmodule.py    贝叶斯分类器
├── rfcmodel.py     随机森林
├── svm_pca.py  支持向量机加主成分分析
└── svm.py      支持向量机
└── mlp.py      多层感知机
└── plotcurve.py      绘制学习曲线
```
可以简单的通过运行文件得到结果。s
**例如：使用支持向量机**
```python
cd clfmodels
python svm.py
```
在此之前需要改变在svm.py中改变路径
```python 
energys = np.loadtxt("/home/newsun/DSP/DSP_lab/feature/energys_conv.txt")
nums = np.loadtxt("/home/newsun/DSP/DSP_lab/feature/nums.txt")
```
将其路径改为之前所提取出的特征向量以及标签的路径。
得到输出：
```bash
accuracy:0.8266871165644172
```
即为准确率。
~~这里其实使用测试集当训练集，你也可以自己split一下。~~

| 模型 | 准确率(%) |
|---|---|
| SVM | 76.82 |
| SVM+PCA | 88.61 |
| MVBmodule | 59.96 |
| rfcmodel | 90.13 |
| dtmodel | 59.20 |
| dtmodel+PCA | 50.13 |
| MLP | 82.1 |