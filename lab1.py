# -*- coding: utf-8 -*-
import wave
import os
import numpy as np
import utils.color as color
import utils.Recorder as R
import utils.Player as P
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm, rcParams
def sgn(data):
    if data >= 0 :
        return 1
    else :
        return 0

# 计算每一帧的能量 256个采样点为一帧
def calEnergy(wave_data) :
    energy = []
    sum = 0
    for i in range(len(wave_data)) :
        sum = sum + (int(wave_data[i]) * int(wave_data[i]))
        if (i + 1) % 256 == 0 :
            energy.append(sum)
            sum = 0
        elif i == len(wave_data) - 1 :
            energy.append(sum)
    return energy

#计算过零率
def calZeroCrossingRate(wave_data) :
    zeroCrossingRate = []
    sum = 0
    for i in range(len(wave_data)) :
        if i % 256 == 0:
            continue
        sum = sum + np.abs(sgn(wave_data[i]) - sgn(wave_data[i - 1]))
        if (i + 1) % 256 == 0 :
            zeroCrossingRate.append(float(sum) / 255)
            sum = 0
        elif i == len(wave_data) - 1 :
            zeroCrossingRate.append(float(sum) / 255)
    return zeroCrossingRate

# 利用短时能量，短时过零率，使用双门限法进行端点检测
def endPointDetect(wave_data, energy, zeroCrossingRate) :
    sum = 0
    energyAverage = 0
    for en in energy :
        sum = sum + en
    energyAverage = sum / len(energy)

    sum = 0
    for en in energy[:5] :
        sum = sum + en
    ML = sum / 5                        
    MH = energyAverage / 4              #较高的能量阈值
    ML = (ML + MH) / 4    #较低的能量阈值
    sum = 0
    for zcr in zeroCrossingRate[:5] :
        sum = float(sum) + zcr             
    Zs = sum / 5                     #过零率阈值

    A = []
    B = []
    C = []

    # 首先利用较大能量阈值 MH 进行初步检测
    flag = 0
    for i in range(len(energy)):
        if len(A) == 0 and flag == 0 and energy[i] > MH :
            A.append(i)
            flag = 1
        elif flag == 0 and energy[i] > MH and i - 21 > A[-1]:
            A.append(i)
            flag = 1
        elif flag == 0 and energy[i] > MH and i - 21 <= A[-1]:
            A = A[:-1]
            flag = 1

        if flag == 1 and energy[i] < MH :
            A.append(i)
            flag = 0
    # print("较高能量阈值，计算后的浊音A:" + str(A))

    # 利用较小能量阈值 ML 进行第二步能量检测
    for j in range(len(A)) :
        i = A[j]
        if j % 2 == 1 :
            while i < len(energy) and energy[i] > ML :
                i = i + 1
            B.append(i)
        else :
            while i > 0 and energy[i] > ML :
                i = i - 1
            B.append(i)
    # print("较低能量阈值，增加一段语言B:" + str(B))

    # 利用过零率进行最后一步检测
    for j in range(len(B)) :
        i = B[j]
        if j % 2 == 1 :
            while i < len(zeroCrossingRate) and zeroCrossingRate[i] >= 3 * Zs :
                i = i + 1
            C.append(i)
        else :
            while i > 0 and zeroCrossingRate[i] >= 3 * Zs :
                i = i - 1
            C.append(i)
    # print("过零率阈值，最终语音分段C:" + str(C))
    return C

def pcm2wav(pcm_file, wav_file, channels=1, sampwidth=16, sample_rate=16000):
    # 打开 PCM 文件
    pcmf = open(pcm_file, 'rb')
    pcmdata = pcmf.read()
    pcmf.close()
    
    # 打开将要写入的 WAVE 文件
    wavfile = wave.open(wav_file, 'wb')
    # 设置声道数
    wavfile.setnchannels(channels)
    # 设置采样位宽
    wavfile.setsampwidth(sampwidth)
	# 设置采样率
    wavfile.setframerate(sample_rate)
    # 写入 data 部分
    wavfile.writeframes(pcmdata)
    wavfile.close()
    




if __name__ == "__main__":
    color.Print.yellow('==============================welcome to use audio analysis system================================')
    wav_path = "/home/newsun/DSP/DSPyuyin/4/[2021-10-23][14-02-15].wav"
    retry_flag = 1
    while retry_flag == 1:
        # if input('record now(print 0) or read from wav(print 1) : ') == '0' :
        #     r = R.Recorder()
        #     times = int(input('please input how many seconds you wanna record :'))
        #     print(type(times))
        #     r.settime(times)
        #     r.record()
        #     r.savewav(wav_path)
        # else :
        #     wav_path = input('Please input path of .wav : ')
        # if not os.path.exists(wav_path):
        #     color.Print.red("No Such File")
        #     exit()
        
        #播放器相关模块
        player = P.Player(wav_path)
        color.Print.green('playing your wav now')
        player.play()
        if input('Are you sure about that? (input yes or retry)') == 'retry' :
            retry_flag = 1
        else:
            retry_flag = 0
    
    #从wav中读取
    f = wave.open(wav_path,"rb")
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

    time = np.arange(0,nframes)*(1.0/framerate)
    plt.subplot(2,  1,  1)  
    plt.rcParams['font.sans-serif']=['SimHei'] #显示中文标签
    plt.rcParams['axes.unicode_minus']=False   
    plt.plot(range(len(wave_data)),wave_data)
    plt.xlabel('time')

    #计算短时能量
    energy = calEnergy(wave_data)
    output_index = input("please input output index : ")
    with open("./energy/"+ output_index +  "_en.txt", "w") as f :
        for en in energy :
            f.write(str(en) + "\n")
    #计算过零率
    zeroCrossingRate = calZeroCrossingRate(wave_data)
    with open("./zeroCrossingRate/" + output_index + "_zero.txt","w") as f :
        for zcr in zeroCrossingRate :
            f.write(str(zcr) + "\n")
    np.fft.fft
    #进行端点检测
    N = endPointDetect(wave_data, energy, zeroCrossingRate)
    i=0
    while i < len(N):
        if N[i+1] - N[i] > 10:
            break
        i = i + 2
    if i >= len(N) - 1:
        exit(0)

    energy = energy[N[i]:N[i + 1]]
    plt.subplot(2,  1,  2) 
    plt.plot(len(energy),energy)
    plt.show()
    
    # 输出为 pcm 格式
    with open("./output/"+ output_index + "_test.pcm", "wb") as f :
        i = 0
        while i < len(N) :
            for num in wave_data[N[i] * 256 : N[i+1] * 256] :
                f.write(num)
            i = i + 2
    
    #pcm转wav
    pcm2wav("./output/"+ output_index + "_test.pcm","./output/"+ output_index + "_test.wav",nchannels,sampwidth,framerate)
    color.Print.green('playing the result wav now')
    player = P.Player("./output/"+ output_index + "_test.wav")
    player.play()
    

    #SVM分类器
    