from socket import *                        # Library yang digunakan untuk membuat socket server dan menghubungakannya dengan html.
import sys                                  # Library yang digunakan untuk mengehentikan program.
serverSocket = socket(AF_INET, SOCK_STREAM) # Membuat socket server baru dengan menggunakan protokol IPv4 (AF_INET) dan protokol TCP (SOCK_STREAM).
serverName = '127.0.0.1'            # Menetapkan IP Address yang digunakan.
serverPort = 80                     # Menetapkan Nomor port yang digunakan.
serverSocket.bind((serverName, serverPort)) # Menetapkan nomor port dan IP address ke socket server,
serverSocket.listen(1)              # Socket server menunggu permintaan koneksi dari klien, parameter 1 menandakan jumlah koneksi maksimum yang dapat diterima oleh server.
while True:                         # Program akan beroperasi sembari menunggu koneksi dari klien.
    print('Ready to Serve...')      # Jika koneksi berhasil terhubung, keluarkan output 
    connectionSocket, addr = serverSocket.accept()      # Koneksi yang diterima ditangani socket baru yang dibuat server (connectionSocket) dan menyimpan alamat ip dan nomor port di variabel addr.
    try:                                                # Cek data dari klient
        message = connectionSocket.recv(1024).decode()  # Socket menerima data dari klien yang di konversi ke string dengan metode (.decode), data disimpan di varaibel message.
        filename = message.split()[1]                   # variable message di parsing, dan bagian dari indeks pertama (file/path) disimpan di variable filename. 
        f = open(filename[1:], 'rb')                    # Membuka file yang diminta oleh klien dengan metode open, karakter pertama dari nama file tidak dipanggil karena tidak dibutuhkan ('/'), sedangkan parameter rb digunakan untuk membuka file dalam mode binary
        outputdata = f.read()                           # Membaca isi file dengan metode .read, dan menyimpan isinya ke variabel outputdata
        status_line = "HTTP/1.1 200 OK\r\n"                     # HTTP response dari server jika permintaan klien berhasil diproses oleh server
        if filename.endswith('.jpg') or filename.endswith('.jpeg'): # Cek jika filename yang dibuka merupakan file jpg atau jpeg
            content_type = "Content-Type: image/jpeg\r\n\r\n"  # HTTP response dari server menandakan jenis kontent yang dikirim adalah image/jpeg
        elif filename.endswith('.png'):                             # Cek jika filename yang dibuka merupakan file png
            content_type = "Content-Type: image/png\r\n\r\n"   # HTTP response dari server menandakan jenis kontent yang dikirim adalah image/png
        else:
            content_type = "Content-Type: text/html\r\n\r\n"   # HTTP response dari server menandakan jenis kontent yang dikirim adalah text/html
        response = status_line+content_type                # Kedua variabel tersebut merupakan bagian header dari HTTP Response
        connectionSocket.send(response.encode())           # Response di konversi menjadi tipe data byte string, dan kemudian dikirimkan ke klien melalui connectionSocket
        for i in range(0, len(outputdata)):                # Melakukan iterasi pada isi file yang berada di variable outputdata
            connectionSocket.send(outputdata[i:i+1])       # Mengirim isi file ke klien pada indeks i sampai indeks i+1 melalui connectionSocket
        connectionSocket.send("\r\n".encode())             # Mengirim string escape sequence (\r\n) melalui connectionSocket ketika loop berakhir
    except IOError:                 # Jika data yang dikirim berbeda dengan yang telah didefinisikan
        error = "HTTP/1.1 404 NOT FOUND\r\nContent-Type: text/html\r\n\r\n" # HTTP response dari server jika permintaan klien tidak ditemukan oleh server    
        connectionSocket.send(error.encode())                               # response dikirim ke klien melalui connectionSocket
        connectionSocket.send("<html><head><link rel='stylesheet' href='style.css'></head><body><div class='section-A'><h1>404 NOT FOUND</h1></div></body></html>".encode())  # Mengirimkan pesan informasi (dalam bentuk html) ke klien
    connectionSocket.close()        # Hentikan koneksi socket; memperbolehkan ada koneksi baru
serverSocket.close()                # Hentikan socket server; memutus koneksi antar klien dan server
sys.exit()                          # Exit program
