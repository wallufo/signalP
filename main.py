from threading import Thread
import numpy as np
import sounddevice as sd
import time, pygame
from pygame.locals import *
pygame.init()

def listen():
    global data, ind
    stream = sd.InputStream(samplerate=rate, channels=1, dtype=np.int16)
    stream.start()

    while running:
        data[:] = stream.read(chunk)[0].reshape(chunk)

        f = np.fft.fft(data, n=rate)
        f = np.abs(f[:len(f)//2])
        q = np.percentile(f, 98).max()

        x = np.argmax(f[xfreq])
        y = np.argmax(f[yfreq])

        if f[xfreq[x]] < q or f[yfreq[y]] < q:
            ind = None
        else:
            ind = x*3 + y


keys = (np.arange(12) + 1).astype(str)
keys[9:] = ['*', '0', '#']

xfreq = np.array([697, 770, 852, 941])
yfreq = np.array([1209, 1336, 1477])

freq = np.zeros((4,3,2))
freq[:,:,0] = xfreq.reshape(4, 1)
freq[:,:,1] = yfreq.reshape(1, 3)

freq = freq.reshape(12, 2)

ind = None
running = True
rate = 44100
dur = .1
chunk = int(rate * dur)
data = np.zeros((chunk,), dtype=np.int16)

thr = Thread(target=listen)
thr.start()

W = 500
disp = pygame.display.set_mode((W,W))
clock = pygame.time.Clock()
font = pygame.font.Font(None, 500)

while running:
    for e in pygame.event.get():
        if e.type == QUIT:
            running = False
            break

    text = "?" if ind is None else keys[ind]
    col = (255,0,0) if text == '?' else (0,255,0)
    rect = font.render(text, True, col)
    w, h = rect.get_size()

    disp.fill((0,0,0))
    disp.blit(rect, ((W-w)//2, (W-h)//2))
    pygame.display.update()
    clock.tick(20)

time.sleep(.2)
pygame.quit()
