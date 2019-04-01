# The MIT License (MIT)
#
# Copyright (c) 2017 Niklas Rosenstein
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to
# deal in the Software without restriction, including without limitation the
# rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
# sell copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
# IN THE SOFTWARE.
"""
This example displays the orientation, pose and RSSI as well as EMG data
if it is enabled and whether the device is locked or unlocked in the
terminal.

Enable EMG streaming with double tap and disable it with finger spread.
"""

from __future__ import print_function
from myo.utils import TimeInterval
import time
import myo
import sys
import math
from predictor import *

global predictor, dic
global indice, indice2

def quaternion_to_euler(x, y, z, w):

  t0 = +2.0 * (w * x + y * z)
  t1 = +1.0 - 2.0 * (x * x + y * y)
  X = math.degrees(math.atan2(t0, t1))

  t2 = +2.0 * (w * y - z * x)
  t2 = +1.0 if t2 > +1.0 else t2
  t2 = -1.0 if t2 < -1.0 else t2
  Y = math.degrees(math.asin(t2))

  t3 = +2.0 * (w * z + x * y)
  t4 = +1.0 - 2.0 * (y * y + z * z)
  Z = math.degrees(math.atan2(t3, t4))

  return X, Y, Z

class Listener(myo.DeviceListener):

  def __init__(self):
    self.interval = TimeInterval(None, 0.05)
    self.orientation = None
    self.pose = myo.Pose.rest
    self.emg_enabled = False
    self.locked = False
    self.rssi = None
    self.emg = None

  def output(self):
    global centre
    global indice, indice2
    if not self.interval.check_and_reset():
      return
    parts = []
    aux = list(quaternion_to_euler(self.orientation[0], self.orientation[1], self.orientation[2], self.orientation[3])) #wrist, y, x
    for i in range(len(aux)):
      aux[i]=aux[i]-centre[i]
      if aux[i]>180:
        aux[i]=aux[i]-360
      elif aux[i]<-180:
        aux[i]=360+aux[i]
    aux[2] = -aux[2]

    if self.pose == 1 and (aux[0] > 90 or aux[0] < -90):
        indice2 = 5
    else:
        indice2 = int(self.pose)-1

    if aux[2]>50 and aux[1]<aux[2]:
      indice = 3
      '''print("XD+\n")
      if self.pose == 1:
        print("puño arriba")
      elif self.pose == 2:
        print("wave in")
      elif self.pose == 3:
        print("wave out")
      elif self.pose == 4:
        print("hola")
      elif aux[0]>50:
        print("derrape derecha")
      elif aux[0]<-50:
        print("derrape izda")'''
    elif aux[2]<-50 and aux[1]>aux[2]:
      indice = 2
      '''print("XD-\n")
      if self.pose == 1:
        print("puño arriba")
      elif self.pose == 2:
        print("wave in")
      elif self.pose == 3:
        print("wave out")
      elif self.pose == 4:
        print("hola")
      elif aux[0]>50:
        print("derrape derecha")
      elif aux[0]<-50:
        print("derrape izda")'''
    elif aux[1]>30 and aux[2]<aux[1]:
      indice = 0
      '''print("Y:)\n")
      if self.pose == 1:
        print("puño arriba")
      elif self.pose == 2:
        print("wave in")
      elif self.pose == 3:
        print("wave out")
      elif self.pose == 4:
        print("hola")
      elif aux[0]>50:
        print("derrape derecha")
      elif aux[0]<-50:
        print("derrape izda")'''
    elif aux[1]<-30 and aux[2]>aux[1]:
      indice = 1
      '''print("Y:(\n")
      if self.pose == 1:
        print("puño arriba")
      elif self.pose == 2:
        print("wave in")
      elif self.pose == 3:
        print("wave out")
      elif self.pose == 4:
        print("hola")
      elif aux[0]>50:
        print("derrape derecha")
      elif aux[0]<-50:
        print("derrape izda")'''
    elif (aux[1] > -30 and aux[1] < 0) or (aux[2] > -50 and aux[2] < 50):
      indice = -1
    print(indice)
    print(indice2)
    if indice > -1:
      print(predictor.gesto_a_letra(indice, indice2))
      print(predictor.palabra_actual)
    else:
      if self.pose == 2:
        predictor.escuchar_palabra(str(predictor.palabra_actual))
        #predictor.escuchar_palabra("hola")
        #self.engine.say("hola")
        self.engine.runAndWait()
        predictor.palabra_actual = ""
      print("No te escucho\n")
    parts.append(aux)
    parts.append(str(self.pose).ljust(10))
    parts.append('E' if self.emg_enabled else ' ')
    print('\r' + ''.join('[{}]'.format(p) for p in parts), end='')
    sys.stdout.flush()

  def on_connected(self, event):
    event.device.request_rssi()

  def on_rssi(self, event):
    self.rssi = event.rssi

  def on_pose(self, event):
    global centre, flag
    self.pose = event.pose
    if self.pose == myo.Pose.fingers_spread:
      if flag:
        centre = quaternion_to_euler(self.orientation[0], self.orientation[1], self.orientation[2], self.orientation[3])
        flag=0
        print("Centrado")
    if self.pose != 0 and not flag:
      self.locked = True
      self.output()
      time.sleep(2.5)
      self.locked = False
      event.device.vibrate(myo.VibrationType.short)

  def on_orientation(self, event):
    self.orientation = event.orientation

  def on_emg(self, event):
    self.emg = event.emg

  def on_unlocked(self, event):
    self.locked = False

  def on_locked(self, event):
    self.locked = True


if __name__ == '__main__':
  global indice, indice2
  indice, indice2 = 0, 0
  myo.init()
  hub = myo.Hub()

  indice = 0
  listener = Listener()
  predictor = Principal()
  predictor.escuchar_palabra("vio ese culete")
  #dic = predictor.cargar_diccionario("./palabras_faciles.txt")
  centre=[0,0,0]
  flag = 1
  while hub.run(listener.on_event, 1000):
    pass
