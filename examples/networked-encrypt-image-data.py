# This script accepts two command-line argument.
# argv1 = ftpServerIpAddress
# argv2 = ftpServerPort

from Crypto.Cipher import AES
import socket as socket
import sys
import ftplib
import io
import os

numberOfCommandLineArguments = len(sys.argv) - 1

if numberOfCommandLineArguments != 2:
    print(numberOfCommandLineArguments)
    raise Exception("Two command-line arguments must be specified (argv1 = FTP Server IP Address, argv2 = FTP Server Socket)...")

compSocket = socket.socket()
compSocket.bind(('localhost',55556))
compSocket.listen(1)
print("Waiting for client to connect...")
client_socket, client_address = compSocket.accept()

ftp_server = ftplib.FTP()
# Note: You will need to modify ip/port/credentials for 
# whatever FTP server you configure. Also remember to 
# create a mount point for the virtual path '/'.
# Also also remember you will probably have to disable
# windows defender firewall for FTP server on windows.

# Parse FTP Server IP Address and Port
ftpServerIpAddress = sys.argv[1]
ftpServerPort = int(sys.argv[2])

ftp_server.connect(ftpServerIpAddress,ftpServerPort)
ftp_server.login('user','password')

file_path = os.path.dirname(os.path.realpath(__file__)) + "/"

file_name = file_path + "runtime_compressed.dat.gz"
key_file = file_path + "key_file.bin"
data_end = b'TRANSMISSION_STOP'
i = 1

while True:
    # Wait for transmission of compressed file
    print("Waiting for compressed data to be transmitted")
    total_data = []
    data = ''
    while True:
        data = client_socket.recv(4096)
        if data_end in data:
            print("Terminating sequence found")
            total_data.append(data[:data.find(data_end)])
            break
        total_data.append(data)
        if len(total_data) > 1:
            last_pair = total_data[-2]+total_data[-1]
            if data_end in last_pair:
                print("Terminating sequence found split across packets")
                total_data[-2] = last_pair[:last_pair.find(data_end)]
                total_data.pop()
                break

    compressed_data = bytearray()
    compressed_data = b''.join(total_data)
    print("Compressed data received: " + str(sys.getsizeof(compressed_data)))

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
