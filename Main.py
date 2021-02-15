import sys
import wave
import struct
import math
import os
import glob
from numpy import fromstring, int16
import speech_recognition as sr


def main(args=None):
    if len(args) < 2:
        print('No args')
        return
    else:
        print(args[1:])

    files = glob.glob(os.path.join(args[1], '*.wav'))

    for file in files:
        dir_path = split_sound(file, 60*1)
        text = create_text(dir_path)
        f = open(os.path.join(os.path.dirname(file), os.path.basename(file).split('.')[0] + '.txt'), 'a')
        try:
            f.write(text)
        except Exception as e:
            print(e)
        finally:
            print('writen to ' + f.name)
            f.close()


def create_text(dir_path):
    wfiles = glob.glob(os.path.join(dir_path, '*.wav'))
    print(wfiles)
    text = ''

    for wfile in wfiles:
        try:
            tmp = google_recgnition(wfile)
            print(tmp)
            text = text + tmp + '\r\n'
        except Exception as e:
            print(e)

    return text


def google_recgnition(file_path):
    text = ''

    print('process ' + file_path)
    r = sr.Recognizer()

    with sr.AudioFile(file_path) as source:
        print('record ' + file_path)
        audio = r.record(source)

    print('recognize_google ' + file_path)
    return r.recognize_google(audio, language='ja-JP')


def split_sound(file: str, split_time: int):
    if os.path.exists(file) is False:
        print('file not found ' + file)
        return ''
    elif os.path.isfile(file) is False:
        print(file + ' is not file')
        return ''

    dir_path = os.path.join(os.path.dirname(file), os.path.basename(file).split('.')[0])
    if os.path.exists(dir_path) is False:
        os.mkdir(dir_path)
        print('create ' + dir_path)
    elif os.path.isfile(dir_path) is True:
        print('can not create dir')
        return ''

    wr = wave.open(file, 'r')
    try:
        ch = wr.getnchannels()
        width = wr.getsampwidth()
        fr = wr.getframerate()
        fn = wr.getnframes()
        total_time = 1.0 * fn / fr
        t = int(split_time)  # 秒数[sec]
        frames = int(ch * fr * t)
        print('total time ' + str(total_time) + '[sec]')
        num_cut = int(math.floor(total_time) // split_time)+1
        print(str(total_time) + '//' + str(split_time) + '=>' + str(num_cut))
        data = wr.readframes(wr.getnframes())
    except Exception as e:
        print(e)
        return
    finally:
        wr.close()

    try:
        x = fromstring(data, dtype=int16)
        print(x)

        for i in range(num_cut):
            print(i)
            # 出力データを生成
            outf = os.path.join(dir_path, f'{i:04}' + '.wav')
            start_cut = i * frames
            end_cut = i * frames + frames
            print(start_cut)
            print(end_cut)
            y = x[start_cut:end_cut]
            outd = struct.pack("h" * len(y), *y)

            # 書き出し
            ww = wave.open(outf, 'w')
            ww.setnchannels(ch)
            ww.setsampwidth(width)
            ww.setframerate(fr)
            ww.writeframes(outd)
            ww.close()
    except Exception as e:
        print(e)
        return ''

    return dir_path


if __name__ == '__main__':
    main(sys.argv)
    print('finish')
