################################################################################
#                                                                              #
#  __  __ _____ ____   ____                 _                                  #
# |  \/  |  ___|  _ \ / ___| __ _ _ __ ___ (_)_ __   __ _                      #
# | |\/| | |_  | | | | |  _ / _` | '_ ` _ \| | '_ \ / _` |                     #
# | |  | |  _| | |_| | |_| | (_| | | | | | | | | | | (_| |                     #
# |_|  |_|_|   |____/ \____|\__,_|_| |_| |_|_|_| |_|\__, |                     #
#                                                    |___/                     #
# Copyright 2021 MFDGaming                                                     #
#                                                                              #
# Permission is hereby granted, free of charge, to any person                  #
# obtaining a copy of this software and associated documentation               #
# files (the "Software"), to deal in the Software without restriction,         #
# including without limitation the rights to use, copy, modify, merge,         #
# publish, distribute, sublicense, and/or sell copies of the Software,         #
# and to permit persons to whom the Software is furnished to do so,            #
# subject to the following conditions:                                         #
#                                                                              #
# The above copyright notice and this permission notice shall be included      #
# in all copies or substantial portions of the Software.                       #
#                                                                              #
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR   #
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,     #
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE  #
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER       #
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING      #
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS #
# IN THE SOFTWARE.                                                             #
#                                                                              #
################################################################################

from copy import copy
import os
from praknet import handler
from praknet import packets
import socket
import struct

options = {
    "name": "MCCPP;Demo;Default PRakNet motd",
    "ip": "0.0.0.0",
    "port": 19132,
    "server_guid": struct.unpack(">Q", os.urandom(8))[0],
    "custom_handler": lambda data, addr: 0,
    "accepted_raknet_protocols": [5],
    "debug": False
}

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
connections = {}

def add_connection(address):
    token = str(address[0]) + ":" + str(address[1])
    connections[token] = {
        "mtu_size": 0,
        "address": address,
        "is_connected": False,
        "sent_packets": [],
        "sequence_number": 0
    }

def remove_connection(address):
    token = str(address[0]) + ":" + str(address[1])
    if token in connections:
        body = bytes([packets.connection_closed["id"]])
        packet = copy(packets.frame)
        packet["reliability"] = 0
        packet["body"] = body
        send_frame(packet, address)
        del connections[token]

def get_connection(address):
    token = str(address[0]) + ":" + str(address[1])
    if token in connections:
        return connections[token]

def get_last_packet(address):
    connection = get_connection(address)
    queue = connection["sent_packets"]
    if len(queue) > 0:
        return queue[-1]
    
def send_frame(packet, address):
    connection = get_connection(address)
    new_packet = copy(packets.frame_set)
    new_packet["sequence_number"] = connection["sequence_number"]
    new_packet["frame"] = packet
    server_socket.sendto(packets.write_frame_set(new_packet), address)
    connection["sent_packets"].append(packet)
    connection["sequence_number"] += 1

def broadcast_frame(packet):
    for connection in connections.values():
        send_frame(packet, connection["address"])
    
def packet_handler(data, address):
    identifier = data[0]
    connection = get_connection(address)
    if connection != None:
        if identifier == packets.nack["id"]:
            send_frame(get_last_packet(address), address)
        elif 0x80 <= identifier <= 0x8f:
            frame_set = packets.read_frame_set(data)
            new_packet = copy(packets.ack)
            new_packet["packets"].append(frame_set["sequence_number"])
            server_socket.sendto(packets.write_acknowledgement(new_packet), address)
            frame = frame_set["frame"]
            identifier = frame["body"][0]
            if options["debug"]:
                print("Received frame -> " + str(hex(identifier)))
            if identifier < 0x80:
                if not connection["is_connected"]:
                    if identifier == packets.connection_request["id"]:
                        body = handler.handle_connection_request(frame["body"], address)
                        packet = copy(packets.frame)
                        packet["reliability"] = 0
                        packet["body"] = body
                        send_frame(packet, address)
                    elif identifier == packets.new_connection["id"]:
                        packet = packets.read_new_connection(frame["body"])
                        if options["debug"]:
                            print(packet)
                        connection["is_connected"] = True
                elif identifier == packets.connection_closed["id"]:
                    remove_connection(address)
                elif identifier == packets.connected_ping["id"]:
                    body = handler.handle_connected_ping(frame["body"])
                    packet = copy(packets.frame)
                    packet["reliability"] = 0
                    packet["body"] = body
                    send_frame(packet, address)
            if connection["is_connected"]:
                options["custom_handler"](frame, address)
    elif identifier == packets.unconnected_ping["id"]:
        server_socket.sendto(handler.handle_unconnected_ping(data), address)
    elif identifier == packets.unconnected_ping_open_connections["id"]:
        server_socket.sendto(handler.handle_unconnected_ping(data), address)
    elif identifier == packets.open_connection_request_1["id"]:
        server_socket.sendto(handler.handle_open_connection_request_1(data), address)
    elif identifier == packets.open_connection_request_2["id"]:
        server_socket.sendto(handler.handle_open_connection_request_2(data, address), address)

def run():
    try:
        server_socket.bind((options["ip"], options["port"]))
    except socket.error as e:
        raise Exception("Failed to bind!\n" + str(e))
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    while True:
        recv = server_socket.recvfrom(65535)
        if recv != None:
            data, address = recv
            packet_handler(data, address)
