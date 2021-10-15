#!/usr/bin/python
# encoding:utf-8

import pyaudio
import wave

class Player :
    def __init__(self,wav_path):
        self.CHUNK = 1024
        # 从目录中读取语音
        self.wf = wave.open(wav_path, 'rb')
        # read data
        self.data = self.wf.readframes(self.CHUNK)
        # 创建播放器
        p = pyaudio.PyAudio()
        # 获得语音文件的各个参数
        FORMAT = p.get_format_from_width(self.wf.getsampwidth())
        CHANNELS = self.wf.getnchannels()
        RATE = self.wf.getframerate()
        # print('FORMAT: {} \nCHANNELS: {} \nRATE: {}'.format(FORMAT, CHANNELS, RATE))
        # 打开音频流， output=True表示音频输出
        self.stream = p.open(format=FORMAT,

                        channels=CHANNELS,
                        rate=RATE,
                        frames_per_buffer=self.CHUNK,
                        output=True)
    def play(self): 
        # play stream (3) 按照1024的块读取音频数据到音频流，并播放
        while len(self.data) > 0:
            self.stream.write(self.data)
            self.data = self.wf.readframes(self.CHUNK)