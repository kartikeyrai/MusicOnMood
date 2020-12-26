from sys import byteorder
from array import array
from struct import pack
import sys
import combine
import os
from pydub import AudioSegment
import speech_recognition as sr
from gtts import gTTS
import pyaudio
import wave
import facefinal
import ttI
import time
import json

THRESHOLD = 2000
CHUNK_SIZE = 1024
FORMAT = pyaudio.paInt16
RATE = 44100



# wd = os.getcwd()
# ss = os.path.join(wd, 'output.wav')
# print(ss)


def welcome():
    sound('C:\\Users\\ravida6d\\Desktop\\Darshan\\nes\\EmoTV\\sound_files\\welcome.wav')


def is_silent(snd_data):
    "Returns 'True' if below the 'silent' threshold"
    return max(snd_data) < THRESHOLD


def normalize(snd_data):
    "Average the volume out"
    MAXIMUM = 16384
    times = float(MAXIMUM)/max(abs(i) for i in snd_data)

    r = array('h')
    for i in snd_data:
        r.append(int(i*times))
    return r


def trim(snd_data):
    "Trim the blank spots at the start and end"
    def _trim(snd_data):
        snd_started = False
        r = array('h')

        for i in snd_data:
            if not snd_started and abs(i)>THRESHOLD:
                snd_started = True
                r.append(i)

            elif snd_started:
                r.append(i)
        return r

    snd_data = _trim(snd_data)

    snd_data.reverse()
    snd_data = _trim(snd_data)
    snd_data.reverse()
    return snd_data


def add_silence(snd_data, seconds):
    "Add silence to the start and end of 'snd_data' of length 'seconds' (float)"
    r = array('h', [0 for i in range(int(seconds*RATE))])
    r.extend(snd_data)
    r.extend([0 for i in range(int(seconds*RATE))])
    return r


def record():

    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT, channels=1, rate=RATE,
        input=True, output=True,
        frames_per_buffer=CHUNK_SIZE)

    num_silent = 0
    snd_started = False

    r = array('h')

    while 1:

        snd_data = array('h', stream.read(CHUNK_SIZE))
        if byteorder == 'big':
            snd_data.byteswap()
        r.extend(snd_data)

        silent = is_silent(snd_data)

        if silent and snd_started:
            num_silent += 1
        elif not silent and not snd_started:
            snd_started = True

        if snd_started and num_silent > 20:
            break

    sample_width = p.get_sample_size(FORMAT)
    stream.stop_stream()
    stream.close()
    p.terminate()

    # r = normalize(r)
    # r = trim(r)
    # r = add_silence(r, 0.5)
    return sample_width, r


def record_to_file(path):
    "Records from the microphone and outputs the resulting data to 'path'"
    sample_width, data = record()
    data = pack('<' + ('h'*len(data)), *data)

    wf = wave.open(path, 'wb')
    wf.setnchannels(1)
    wf.setsampwidth(sample_width)
    wf.setframerate(RATE)
    wf.writeframes(data)
    wf.close()


def stt(path):

    r = sr.Recognizer()
    harvard = sr.AudioFile(path)
    with harvard as source:
        audio = r.record(source)
    
    type(audio)
    txt3=r.recognize_google(audio, language="en-IN", show_all=True)

    if not txt3:
        # print('ddd')
        text = 'Sorry, Please try again.'
        speechf(text)
        return False
    if isinstance(txt3, dict):
        text = txt3['alternative'][0]['transcript']
        return text
    if type(txt3) is dict:
        text = txt3['alternative'][0]['transcript']
        return text
    else:
        return txt3

    # response = json.dumps(txt3, ensure_ascii=False).encode('utf8')
    # print(response)
    # return txt3
    #speech.func(txt3)


def speech(txt3):
    txt='Hello '
    txt2=' . please let me read your emotions'
    tts=gTTS(text=txt+txt3+txt2, lang='en')
    tts.save("C:\\Users\\ravida6d\\Desktop\\Darshan\\nes\\EmoTV\\sound_files\\good.mp3")
    if os.path.exists('C:\\Users\\ravida6d\\Desktop\\Darshan\\nes\\EmoTV\\sound_files\\output.wav'):
        os.remove('C:\\Users\\ravida6d\\Desktop\\Darshan\\nes\\EmoTV\\sound_files\\output.wav')
    spoken = AudioSegment.from_mp3("C:\\Users\\ravida6d\\Desktop\\Darshan\\nes\\EmoTV\\sound_files\\good.mp3")
    spoken.export('C:\\Users\\ravida6d\\Desktop\\Darshan\\nes\\EmoTV\\sound_files\\output.wav', format="wav")
    sound('C:\\Users\\ravida6d\\Desktop\\Darshan\\nes\\EmoTV\\sound_files\\output.wav')


def speechf(txt3):
    tts=gTTS(text=txt3, lang='en')
    tts.save("C:\\Users\\ravida6d\\Desktop\\Darshan\\nes\\EmoTV\\sound_files\\good.mp3")
    # os.remove("output.wav")
    # os.system("ffmpeg -i good.mp3 output.wav ")
    # sound('output.wav')
    if os.path.exists('C:\\Users\\ravida6d\\Desktop\\Darshan\\nes\\EmoTV\\sound_files\\output.wav'):
        os.remove('C:\\Users\\ravida6d\\Desktop\\Darshan\\nes\\EmoTV\\sound_files\\output.wav')
    spoken = AudioSegment.from_mp3("C:\\Users\\ravida6d\\Desktop\\Darshan\\nes\\EmoTV\\sound_files\\good.mp3")
    spoken.export('C:\\Users\\ravida6d\\Desktop\\Darshan\\nes\\EmoTV\\sound_files\\output.wav', format="wav")
    sound('C:\\Users\\ravida6d\\Desktop\\Darshan\\nes\\EmoTV\\sound_files\\output.wav')


def songplay(emo, txt):

    if emo == 'Happy' or emo == 'happy':
        speechf(txt)
        speechf(', You seem to be happy.   Let me play a song for you ')
        sound('C:\\Users\\ravida6d\\Desktop\\Darshan\\nes\\EmoTV\\sound_files\\happy.wav')

    elif emo == 'Sad' or emo == 'sad':
        speechf(txt)
        speechf(', You seem to be sad .     Let me play a song for you ')
        sound('C:\\Users\\ravida6d\\Desktop\\Darshan\\nes\\EmoTV\\sound_files\\sad.wav')

    elif emo == 'Surprised' or emo == 'surprised':
        speechf(txt)
        speechf(', You seem to be surprised .  Let me play a song for you ')
        sound('C:\\Users\\ravida6d\\Desktop\\Darshan\\nes\\EmoTV\\sound_files\\surprised.wav')

    elif emo == 'Fearful' or emo == 'fearful':
        speechf(txt)
        speechf(', You seem to be in Fear.  Let me play a song for you ')
        sound('C:\\Users\\ravida6d\\Desktop\\Darshan\\nes\\EmoTV\\sound_files\\fear.wav')

    elif emo == 'Angry' or emo == 'angry':
        speechf(txt)
        speechf(', You seem to be angry .  Let me play a song for you ')
        sound('C:\\Users\\ravida6d\\Desktop\\Darshan\\nes\\EmoTV\\sound_files\\angry.wav')

    elif emo == 'Disgusted' or emo == 'disgusted':
        speechf(txt)
        speechf(', You seem to be in a disgusting mood.  Let me play a song for you ')
        sound('C:\\Users\\ravida6d\\Desktop\\Darshan\\nes\\EmoTV\\sound_files\\disgust.wav')

    elif emo == 'Neutral' or emo == 'neutral':
        speechf(txt)
        speechf(', You do not seem to show any emotion.  Let me play a song for you ')
        sound('C:\\Users\\ravida6d\\Desktop\\Darshan\\nes\\EmoTV\\sound_files\\surprisedf.wav')


def sound(path):
    chunk = 1024
    f = wave.open(path,"rb")
    p = pyaudio.PyAudio()
    stream = p.open(format = p.get_format_from_width(f.getsampwidth()),  
                    channels = f.getnchannels(),  
                    rate = f.getframerate(),  
                    output = True)  
    data = f.readframes(chunk)
    while data:
        stream.write(data)
        data = f.readframes(chunk)
    stream.stop_stream()
    stream.close() 
    p.terminate()


def prediction():
    emo = facefinal.TakeSnapshotAndSave()
    return emo


def show(txt):
    from PIL import Image
    img = Image.open('C:\\Users\\ravida6d\\Desktop\\Darshan\\nes\\EmoTV\\final_emodec_images\\joined_images.jpg')
    img.show()


def ask(txt3, emo):
    txt=txt3+', Would you prefer to take a snapshot on our interactive emodec?, reply with yes or no '
    speechf(txt)
    print('Reply with Yes or No')
    #wait(1)
    record_to_file('C:\\Users\\ravida6d\\Desktop\\Darshan\\nes\\EmoTV\\sound_files\\dem.wav')
    txt2=stt('C:\\Users\\ravida6d\\Desktop\\Darshan\\nes\\EmoTV\\sound_files\\dem.wav')

    while (txt2 not in ['yes', 'no']):
        if txt2 != False:
            text = 'Sorry, Please try again.'
            speechf(text)
        print('Reply with Yes or No !!!')
        record_to_file('C:\\Users\\ravida6d\\Desktop\\Darshan\\nes\\EmoTV\\sound_files\\dem.wav')
        txt2 = stt('C:\\Users\\ravida6d\\Desktop\\Darshan\\nes\\EmoTV\\sound_files\\dem.wav')

    if txt2=='yes' or txt2=='Yes':
        print('Your reply is Yes, take a look at your Snapshot')
        show('C:\\Users\\ravida6d\\Desktop\\Darshan\\nes\\EmoTV\\final_emodec_images\\joined_images.jpg')
        time.sleep(2)
        songplay(emo, txt3)

    elif txt2 == 'No' or txt2 == 'no':
        print('Your reply is No')
        text = 'Thank you' + txt3 + 'for using our interactive emodec. Come again and try later.'
        speechf(text)












if __name__ == '__main__':
    #print("please speak a word into the microphone")
    welcome()
    print('Please say your name')
    # record_to_file_new('demo.wav')
    record_to_file('C:\\Users\\ravida6d\\Desktop\\Darshan\\nes\\EmoTV\\sound_files\\demo.wav')
    txt3=stt('C:\\Users\\ravida6d\\Desktop\\Darshan\\nes\\EmoTV\\sound_files\\demo.wav')

    while (txt3 == False):
        # welcome()
        print('Please say your name again!')
        record_to_file('C:\\Users\\ravida6d\\Desktop\\Darshan\\nes\\EmoTV\\sound_files\\demo.wav')
        txt3 = stt('C:\\Users\\ravida6d\\Desktop\\Darshan\\nes\\EmoTV\\sound_files\\demo.wav')

    print('Hello '+txt3)

    speech(txt3)
    emo=prediction()
    print('Your current emotion is detected as:', emo)
    ttI.ttI(txt3)
    combine.create(emo)
    ask(txt3, emo)
    #print("done - result written to demo.wav")
