import wave
import pyaudio
from socket import *
import sys
from select import *

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
WAVE_OUTPUT_FILE = "server_out.wav"
WIDTH = 2
frames = []

# SOCKET setting
HOST = ''
PORT = 10001
BUFSIZE = 1024
ADDR = (HOST, PORT)

p = pyaudio.PyAudio()
stream = p.open(format = p.get_format_from_width(WIDTH),
               channels = CHANNELS,
               rate = RATE,
               output = True,
               frames_per_buffer = CHUNK)

serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(ADDR)

print("Server start")
serverSocket.listen(1)
clientSocket, client_addr = serverSocket.accept()
print('connected by', client_addr)

data = clientSocket.recv(CHUNK)

i = 1
print('data receive')
while data != '':
    stream.write(data)

    try:
        data = clientSocket.recv(CHUNK)
        #print('%d receive' %len(data))
    except Exception as e:
        print(e)
        clientSocket.close
        break
    
    if i % (int(RATE/1024*4*WIDTH)) == 0 :
        print( str(i/(int(RATE/1024))) +"sec")
        
        try:
            print("wave open")
            wf = wave.open("./wav/%03d_sec.wav"%((i/(int(RATE/1024)))),'wb')
            wf.setnchannels(CHANNELS)
            wf.setsampwidth(p.get_sample_size(FORMAT))
            wf.setframerate(RATE)
            wf.writeframes(b''.join(frames))
            print("wave closed")
            wf.close()
            # clientSocket.send("that is %d framse"%(i))
            frames =[]
        except Exception as e:
            print(e)
            clientSocket.close()
    i= i+1
    frames.append(data)

wf = wave.open(WAVE_OUTPUT_FILE,'wb')
wf.setnchannels(CHANNELS)
wf.setsampwidth(p.get_sample_size(FORMAT))
wf.setframerate(RATE)
wf.writeframes(b''.join(frames))
wf.close()

stream.stop_stream()
stream.close()
p.terminate()
clientSocket.close() #소켓 종료
serverSocket.close()

print('close')
