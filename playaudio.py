import wave
import pyaudio

def printWaveInfo(wf):
    """获取WAVE文件信息""" 
    print ("打印通道数:", wf.getnchannels())                       
    print ("采样宽度:", wf.getsampwidth())                         
    print ("采样频率:", wf.getframerate())                    
    print ("帧数:", wf.getnframes())                          
    print ("参数:", wf.getparams())
    print ("长度秒:", float(wf.getnframes()) / wf.getframerate())
    
if __name__ == '__main__':
    wf = wave.open("E:/signalP/test.wav", "r")

    printWaveInfo(wf)

    # 打开一个流
    p = pyaudio.PyAudio()
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)

    # 以块的形式输出到流并播放音频
    chunk = 1024
    data = wf.readframes(chunk)
    while data != '':
        stream.write(data)
        data = wf.readframes(chunk)
    stream.close()
    p.terminate()
