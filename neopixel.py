#!/usr/bin/env python3

import time
import board
import neopixel
import os.path
import signal
import sys

pixel_pin = board.D21

num_pixels = 24

ORDER = neopixel.GRB

statepath = "/tmp/neopixel.state"

version = 1.1

if len(sys.argv) > 1:
    if sys.argv[1] == "-v":
        print(version)
        exit()

if not os.path.isfile(statepath):
    with open(statepath, "w") as file:
        file.write("S")
    os.chown(statepath, 1000, 1000)


pixels = neopixel.NeoPixel(
    pixel_pin, num_pixels, brightness=0.2, auto_write=False, pixel_order=ORDER
)

prevstate = None

class GracefulKiller:
  kill_now = False
  def __init__(self):
    signal.signal(signal.SIGINT, self.signal_handler)
    signal.signal(signal.SIGTERM, self.signal_handler)

  def signal_handler(self,signum, frame):
    self.kill_now = True

gc = GracefulKiller()


def wheel(pos):
    if pos < 0 or pos > 255:
        r = g = b = 0
    elif pos < 85:
        r = int(pos * 3)
        g = int(255 - pos * 3)
        b = 0
    elif pos < 170:
        pos -= 85
        r = int(255 - pos * 3)
        g = 0
        b = int(pos * 3)
    else:
        pos -= 170
        r = 0
        g = int(pos * 3)
        b = int(255 - pos * 3)
    return (r, g, b) if ORDER in (neopixel.RGB, neopixel.GRB) else (r, g, b, 0)


def rainbow_cycle(j):
    for i in range(num_pixels):
        pixel_index = (i * 256 // num_pixels) + j
        pixels[i] = wheel(pixel_index & 255)
    pixels.show()

j = 0

while(not gc.kill_now):
    with open(statepath, "r") as file:
        state = file.read().rstrip()
    if (state == "F"):
        pixels.fill((255,255,255))
        pixels.show()
    if (state == "N"):
        pixels.fill((255,255,255))
        pixels[5] = (0,0,0)
        pixels[11] = (0,0,0)
        pixels[17] = (0,0,0)
        pixels[23] = (0,0,0)
        pixels.show()
    if (state == "P"):
        pixels.fill((255,255,255))
        pixels[5] = (0,255,0)
        pixels[11] = (0,255,0)
        pixels[17] = (0,255,0)
        pixels[23] = (0,255,0)
        pixels.show()
    if (state == "L"):
        pixels.fill((255,255,255))
        pixels[5] = (255,0,0)
        pixels[11] = (255,0,0)
        pixels[17] = (255,0,0)
        pixels[23] = (255,0,0)
        pixels.show()
    if (state == "S"):
        j += 1
        if j == 256:
            j = 0;
        rainbow_cycle(j)
    time.sleep(0.1)

pixels.fill((0,0,0))
pixels.show()