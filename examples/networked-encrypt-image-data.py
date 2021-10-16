from Crypto.Cipher import AES
import socket as socket
import sys
import ftplib
import io

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
ftp_server.connect('192.168.1.13',21)
ftp_server.login('user','password')

file_name = "runtime_compressed.dat.gz"
key_file = "key_file.bin"
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
    f = io.BytesIO(ciphertext)
    ftp_server.storbinary('STOR data_' + str(i) + '.dat', f)
    # Store updated tag file to be used for decryption
    # NOTE THIS MUST BE DONE ONCE IN YOUR ENVIRONMENT FOR DECRYPT TO WORK
    t_file = open('tag_' + str(i), 'wb')
    t_file.write(tag)
    t_file.close()
    
    i = i + 1