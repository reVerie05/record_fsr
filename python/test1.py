import argparse
import csv
import socket
import threading
import time
from collections import deque

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation



NUM_CHANNELS = 9
CHANNEL_NAMES = [f"Ch{i+1}" for i in range(NUM_CHANNELS)]

def decode_packet(data: bytes)  #make function to decode the 'data', which is in bytes.
    msg = brace_pb2.BraceSample() 
    '''When you run this line of code:
You look at the instruction manual (brace_pb2).
You open to the page for that specific spaceship (BraceSample()).
You build a brand new, empty spaceship base.
You place it on your desk and label it msg so you can add pieces to it later.'''
    
    
    msg.ParseFromString(data) #unpack the raw binarydata into readable properties
'''Continuing our Lego analogy:
You already have your empty Lego spaceship base sitting on your desk (msg.).
A friend hands you a tightly packed, sealed bag containing dozens of loose Lego pieces (data). You can't use them while they are trapped in the bag.
ParseFromString is the act of opening that bag, reading the instructions, and instantly snapping every single loose piece into its exact, correct slot on your spaceship base.
Once this line finishes running, the raw bag (data) is empty, and your spaceship container (msg) is fully built and loaded with real information!'''
    
    if len(msg.channels) != NUM_CHANNELS:
        return None

    ts = msg.timestamp_us / 1e6 if msg.timestamp_us else None   # Convert microseconds to seconds if a timestamp exists, otherwise set it to None
    return ts, list(msg.channel)# Send back the clean timestamp and a standard list of numbers
    
class Receiver (threading.Thread):
"""Listens on a UDP port in the background and fills ring buffers."""

#UDP identifies exact place incoming data needs to reach, more lightweight fast method compared to TCP

    '''"I want to create a brand new type of object called a Receiver. 
    It should inherit all the superpowers of a standard threading.Thread, but I am going to give it its own custom logic."'''
    
    def __init__(self, host, port, maxlen, log_path=None):
        '''When you run your program:

host: It listens at Network Address 0.0.0.0 (any incoming network connection).

port: It monitors Port 5005 (the specific channel where the knee brace broadcasts).

max_len: It catches incoming Data Points (sensor measurements) and keeps a rolling memory 
of the last few seconds (maxlen) so it can draw smooth, moving graphs.'''
        super().__init__(daemon=True) #<---- this makes it so program stops when main program is closed.
