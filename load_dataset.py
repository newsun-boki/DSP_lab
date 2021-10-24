from lab1 import calEnergy
import os
import numpy as np
import wave
from sklearn.svm import SVC 
import pickle
from sklearn.decomposition import PCA
if __name__=="__main__":
    wav_path = "/home/newsun/DSP/DSPyuyin"
    energys = []
    nums = []
    num = 0
    wav_nums = os.listdir(wav_path)
    wav_nums.sort()
    print(wav_nums)
    for wav_num in wav_nums:
        wav_num = os.path.join(wav_path,wav_num)
        if os.path.isdir(wav_num):
            wavs = os.listdir(wav_num)
            print(wavs)
            #从wav中读取
            for wav in wavs:
                wav = os.path.join(wav_num,wav)
                f = wave.open(wav,"rb")
                params = f.getparams()
                #  nframes 采样点数目， nchannels=声道数， sampwidth=采样位数, framerate=采样频率, 
                nchannels, sampwidth, framerate, nframes = params[:4]
                # readframes() 按照采样点读取数据
                str_data = f.readframes(nframes)            # str_data 是二进制字符串
                # 以上可以直接写成 str_data = f.readframes(f.getnframes())
                # 转成二字节数组形式（每个采样点占两个字节）
                wave_data = np.fromstring(str_data, dtype = np.short)
                print( "采样点数目：" + str(len(wave_data)))          #输出应为采样点数目
                f.close()
                energy = calEnergy(wave_data)
                energys.append(energy)
                nums.append(num)
            num = num + 1

#SVM
    clf = SVC(kernel='rbf',decision_function_shape='ovo').fit(energys,nums)
    with open('svm.pickle','wb') as fw:
        pickle.dump(clf,fw)

    #load model
    # with open('svm.pickle','rb') as fr:
    #     svm_clf = pickle.load(fr)
    # print(clf.predict_proba(energys[0:1]))