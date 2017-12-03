'''
Steps:
    Input- Take time in 24hour format
    Process- Convert the 24 hour format to text
             hour
             minute
             am or pm
    Output- Give out in text format
    written by Paul Janson
'''
from inflect import engine
from word2number import w2n
import re,pyaudio,wave
number_converter = engine().number_to_words
CHUNK = 1024
def get_user_input():
    time_given = input('What is the time now? (Please give it in the form hh:mm) ')
    validity_regex = '^(([0-1][0-9])|(2[0-3])):[0-5][0-9]$'
    validity = re.search(validity_regex,time_given)
    if (bool(validity)):
       return time_given.split(':')
    else:
        print("Please enter valid value ")
        main()

def decide_time(time_data):
    hour = time_data[0] if int(time_data[0])<=12 and not(int(time_data[0])==0) else str(abs(int(time_data[0])-12))
    minute = time_data[1]
    am_or_pm = 'am' if int(time_data[0])<12 else 'pm'
    return hour,minute,am_or_pm

def print_time(time_tuple):
    hour,minute,am_or_pm = time_tuple
    if minute[0]=='0':
        if minute[1]=='0':
            name_of_minute = ' '
        else:
            name_of_minute = 'oh '+number_converter(int(minute[1]))
    else:
        name_of_minute = number_converter(int(minute)).replace('-',' ')
    if hour[0] == '0':
        name_of_hour = number_converter(int(hour[1]))
    else:
        name_of_hour = number_converter(int(hour))

    print('It\'s '+name_of_hour+' '+name_of_minute+' '+am_or_pm)
    return 'It\'s '+name_of_hour+' '+name_of_minute+' '+am_or_pm


def audio_output(wf):
    audio_player = pyaudio.PyAudio()
    stream = audio_player.open(format=audio_player.get_format_from_width(wf.getsampwidth()),
                channels=wf.getnchannels(),
                rate=wf.getframerate(),
                output=True)
    data = wf.readframes(CHUNK)
    while len(data) > 0:
        stream.write(data)
        data = wf.readframes(CHUNK)
    stream.stop_stream()
    stream.close()
    audio_player.terminate()

def play_audio(time_str):
    time_list = time_str.split()
    time_list[0] = time_list[0].replace('\'','').lower()
    am_or_pm = time_list[len(time_list)-1]
    time_list = [x for x in time_list if x not in [am_or_pm,'its']]
    its_file = wave.open('voices/its.wav','rb')
    audio_output(its_file)
    for time in time_list:
        if time == 'oh':
            file_name = 'voices/o.wav'
        else:
            file_name = 'voices/'+str(w2n.word_to_num(time))+'.wav'
        file_opened = wave.open(file_name,'rb')
        audio_output(file_opened)
    am_or_pm_file = wave.open('voices/'+am_or_pm+'.wav','rb')
    audio_output(am_or_pm_file)
def main():
    try:
        user_input = get_user_input()
        time_tuple = decide_time(user_input)
        text_tobe_spoken = print_time(time_tuple)
        play_audio(text_tobe_spoken)
    except:
        pass

if __name__ == '__main__':
    main()
