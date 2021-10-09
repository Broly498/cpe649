#import matplotlib.pyplot as plt
#import numpy as np
#import gzip as gz
#from io import BytesIO
from Crypto.Cipher import AES
import socket as socket
import sys

compSocket = socket.socket()
compSocket.bind(('localhost',55556))
compSocket.listen(1)
print("Waiting for client to connect...")
client_socket, client_address = compSocket.accept()


# Factor and clip used to increase visibility for plotting
factor=3.5/255
clip_range=(0, 1)

file_name = "runtime_compressed.dat.gz"
encrypted_file_name = "runtime_encrypted.bin"
key_file = "key_file.bin"
tag_file = "tag_file.bin"

data_end = b'TRANSMISSION_STOP'

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

    # Optional test, uncompress and display image
    #uncompressed_data = BytesIO(gz.decompress(compressed_data))
    #print("Data uncompressed: " + str(sys.getsizeof(uncompressed_data)))
    #uncompressed_image_data = np.load(uncompressed_data, allow_pickle=True)
    #imgplot = plt.imshow(np.clip(uncompressed_image_data * factor, *clip_range))
    #plt.show()

    # Encrypt and store result
    keyfile = open(key_file, "rb")
    key = keyfile.read()
    cipher = AES.new(key, AES.MODE_SIV)
    ciphertext, tag = cipher.encrypt_and_digest(compressed_data)
    file = open(encrypted_file_name, 'wb')
    file.write(ciphertext)
    file.close()

    # Store updated tag file to be used for decryption
    # NOTE THIS MUST BE DONE ONCE IN YOUR ENVIRONMENT FOR DECRYPT TO WORK
    t_file = open(tag_file, 'wb')
    t_file.write(tag)
    t_file.close()


