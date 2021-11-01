from Crypto.Cipher import AES
import socket as socket
import sys
import ftplib
import io
import os
import time

clientIpAddress = '0.0.0.0'
clientPort = 55556
ftpIpAddress = 'localhost'
ftpPort = 21
ftpUsername = 'user'
ftpPassword = 'password'

if len(sys.argv) > 1:
    clientIpAddress = sys.argv[1]

if len(sys.argv) > 2:
    ftpIpAddress = sys.argv[2]

if len(sys.argv) > 3:
    ftpPort = int(sys.argv[3])

compSocket = socket.socket()
compSocket.bind((clientIpAddress, clientPort))
compSocket.listen(1)
print("Start time for encryption: " + str(time.time_ns()))
print("Waiting for client to connect on " + clientIpAddress + ":" + str(clientPort) + "...", flush=True)
client_socket, client_address = compSocket.accept()
print("Client connected.", flush=True)

ftp_server = ftplib.FTP()
# Note: You will need to modify ip/port/credentials for 
# whatever FTP server you configure. Also remember to 
# create a mount point for the virtual path '/'.
# Also also remember you will probably have to disable
# windows defender firewall for FTP server on windows.
ftp_server.connect(ftpIpAddress, ftpPort)
ftp_server.login(ftpUsername, ftpPassword)

file_path = os.path.dirname(os.path.realpath(__file__)) + "/"

file_name = file_path + "runtime_compressed.dat.gz"
key_file = file_path + "key_file.bin"
data_end = b'TRANSMISSION_STOP'
i = 1

while True:
    # Wait for transmission of compressed file
    print("Waiting for compressed data to be transmitted", flush=True)
    total_data = []
    data = ''
    while True:
        data = client_socket.recv(4096)
        if data_end in data:
            print("Terminating sequence found", flush=True)
            total_data.append(data[:data.find(data_end)])
            break
        total_data.append(data)
        if len(total_data) > 1:
            last_pair = total_data[-2]+total_data[-1]
            if data_end in last_pair:
                print("Terminating sequence found split across packets", flush=True)
                total_data[-2] = last_pair[:last_pair.find(data_end)]
                total_data.pop()
                break

    compressed_data = bytearray()
    compressed_data = b''.join(total_data)
    print("Compressed data received: " + str(sys.getsizeof(compressed_data)), flush=True)
    print("Time Compressed data received :" + str(time.time_ns()))
    # Encrypt and store result
    keyfile = open(key_file, "rb")
    key = keyfile.read()
    cipher = AES.new(key, AES.MODE_SIV)
    ciphertext, tag = cipher.encrypt_and_digest(compressed_data)
    # Store encrypted data and tag on ftp
    f_cipher = io.BytesIO(ciphertext)
    ftp_server.storbinary('STOR data_' + str(i) + '.dat', f_cipher)
    f_tag = io.BytesIO(tag)
    ftp_server.storbinary('STOR tag_' + str(i), f_tag)

    i = i + 1
