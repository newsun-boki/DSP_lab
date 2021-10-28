from lab1 import calEnergy
from lab1 import calZeroCrossingRate, endPointDetect
import os
import numpy as np
import wave
from sklearn.svm import SVC 
import pickle
from tqdm import tqdm

if __name__=="__main__":
    wav_path = "/home/newsun/DSP/DSPyuyin"
    energys = []
    nums = []
    num = 0
    wav_nums = os.listdir(wav_path)
    wav_nums.sort()
    for wav_num in wav_nums:
        wav_num = os.path.join(wav_path,wav_num)
        if os.path.isdir(wav_num):
            wavs = os.listdir(wav_num)
            #从wav中读取
            for wav in tqdm(wavs):
                wav = os.path.join(wav_num,wav)
                f = wave.open(wav,"rb")
                params = f.getparams()
                #  nframes 采样点数目， nchannels=声道数， sampwidth=采样位数, framerate=采样频率, 
                nchannels, sampwidth, framerate, nframes = params[:4]
                if nframes == 0:
                    continue
                # readframes() 按照采样点读取数据
                str_data = f.readframes(nframes)            # str_data 是二进制字符串
                # 以上可以直接写成 str_data = f.readframes(f.getnframes())
                #  转成二字节数组形式（每个采样点占两个字节）
                wave_data = np.fromstring(str_data, dtype = np.short)
                f.close()
                energy = calEnergy(wave_data)
                energy = np.array(energy)
                h=[-0.00032717554443494 , 0.000315432808236797 , 0.00455729159944888,0.0143209901661670	,0.0261158778506968 ,0.0292691154282450	,0.0125015834368943	,-0.0227058733290686,	-0.0534400932508640	,-0.0441531674028067,	0.0274284124139710,	0.145818266022673,	0.257982511029660,	0.304080234860976,	0.257982511029660,	0.145818266022673,	0.0274284124139710	,-0.0441531674028067	,-0.0534400932508640	,-0.0227058733290686,0.0125015834368943,0.0292691154282450,0.0261158778506968,0.0143209901661670,0.00455729159944888,0.000315432808236797,-0.000327175544434946]
                after_conv = np.convolve(energy,h,mode = 'same')
                zeroCrossingRate = calZeroCrossingRate(wave_data)
                N = endPointDetect(wave_data, after_conv, zeroCrossingRate)
                if len(N) < 2 or len(N) % 2 == 1:
                    continue
                i = 0
                while i < len(N):
                    if N[i+1] - N[i] > 50:
                        break
                    i = i + 2
                if i >= len(N) - 1:
                    continue
                after_conv = after_conv[N[i]:N[i + 1]]
                after_conv = (after_conv - min(after_conv))/(max(after_conv) - min(after_conv))
                #使用最近邻法使特征向量让after_conv定长127
                step = len(after_conv)/130
                t = 0
                reduced_after_conv = []
                times = 0
                while t < len(after_conv) - 1:
                    reduced_after_conv.append(after_conv[round(t)])
                    t = t + step
                    times = times + 1
                while len(reduced_after_conv) >= 128:
                    reduced_after_conv.pop()
                energys.append(reduced_after_conv)
                nums.append(num)
            print("num："+str(num) + " finished")
            num = num + 1
            
    with open("./feature/energys_conv.txt","w") as f:
        for energy in energys:
            for e in energy:
                f.write(str(e) + " ")
            f.write("\n")
    with open("./feature/nums.txt","w") as f:
        for num in nums:
            f.write(str(num) + "\n")