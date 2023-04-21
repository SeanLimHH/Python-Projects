import tkinter as tk
import socket
import threading

from cryptography.fernet import Fernet
#https://libraries.io/pypi/cryptography

CONNECTIONTIMEOUT = 3

def FernetEncrypt(key, messageInBytes):
    
    cipher = Fernet(key)
    return cipher.encrypt(messageInBytes)

class ChatClient:
    def __init__(self, master):
        self.host = ""
        self.port = ""
        self.sock = None
        self.master = master
        self.key = None

        master.title("Chat Client")

        self.name = tk.Label(master, text="Name:")
        self.name.grid(row = 0, column = 1, sticky ="E")
        self.name = tk.Entry(master)
        self.name.grid(row = 0, column = 2, sticky ="W")


        self.hostLabel = tk.Label(master, text="Host:")
        self.hostLabel.grid(row = 1, column = 1, sticky ="E")
        self.hostInput = tk.Entry(master)
        self.hostInput.insert(0, "localhost")
        self.hostInput.grid(row = 1, column = 2, sticky ="W")

        self.portLabel = tk.Label(master, text="Port:")
        self.portLabel.grid(row = 2, column = 1, sticky ="E")
        self.portInput = tk.Entry(master)
        self.portInput.insert(0, "8080")
        self.portInput.grid(row = 2, column = 2, sticky ="W")

        self.connectButton = tk.Button(master, text="Connect", command=self.connect)
        self.connectButton.grid(row = 1, column = 2)
        
        self.disconnectButton = tk.Button(master, text="Disconnect", command=self.disconnect)
        self.disconnectButton.grid(row = 2, column = 2)
        self.disconnectButton.config(state=tk.DISABLED)
        
        self.chatLabel = tk.Label(master, text="Chat:")
        self.chatLabel.grid(row = 3, column = 1, sticky ="NE")

        self.chatHistory = tk.Text(master, state=tk.DISABLED)
        self.chatHistory.grid(row = 3, columnspan = 2, column = 2)

        self.messageEntry = tk.Entry(master, state=tk.DISABLED)
        self.messageEntry.grid(row = 4,  column = 2, sticky ="W")
        self.messageEntry.bind("<Return>", self.send_message)

        self.send_button = tk.Button(master, text="Send", state=tk.DISABLED, command=self.send_message)
        self.send_button.grid(row = 4, column = 2, sticky ="S")

        self.connected = False

    def generateKey():
        key = Fernet.generate_key()
        return key
        

    def disconnect(self):
        if self.connected:
            self.connected = False
            self.chatHistory.configure(state=tk.NORMAL)
            self.chatHistory.insert(tk.END, f"\nDisconnected from server!\n\n")
            self.chatHistory.see(tk.END)
            self.chatHistory.configure(state=tk.DISABLED)
            self.messageEntry.configure(state=tk.DISABLED)
            self.send_button.configure(state=tk.DISABLED)
            self.disconnectButton.configure(state=tk.DISABLED)
            self.connectButton.configure(state=tk.NORMAL)
            self.sock.sendall("QUIT".encode())
        
    def onWindowClose(self):
        self.disconnect()
        self.master.destroy()
        

    def connect(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if not self.connected:
    
            host = self.hostInput.get()
            self.host = host
            
            try:
                port = int(self.portInput.get())
                self.port = port
            except ValueError:
                self.chatHistory.configure(state=tk.NORMAL)
                self.chatHistory.insert(tk.END, "Connection to server was unsuccessful.\nPlease enter a valid positive integer for the port number!\n\n")
                self.chatHistory.see(tk.END)
                self.chatHistory.configure(state=tk.DISABLED)
                print("Client: Please enter a valid positive integer for the port number!")
                return None
            
            try:
                self.sock.settimeout(CONNECTIONTIMEOUT)
                self.sock.connect((host, port))
                self.sock.settimeout(None)

            except TimeoutError:
                self.chatHistory.configure(state=tk.NORMAL)
                self.chatHistory.insert(tk.END, "Connection to server was unsuccessful. Server is not running currently.\nEnsure that server is running, then press button again!\n\n")
                self.chatHistory.see(tk.END)
                self.chatHistory.configure(state=tk.DISABLED)
                print("Client: Server is not running!")
                return None
            except OverflowError:
                self.chatHistory.configure(state=tk.NORMAL)
                self.chatHistory.insert(tk.END, "Connection to server was unsuccessful.\nPlease enter a integer between 0 to 65535 for the port number!\n\n")
                self.chatHistory.see(tk.END)
                self.chatHistory.configure(state=tk.DISABLED)
                print("Client: Please enter a integer between 0 to 65535 for the port number!")
                return None

            except ConnectionRefusedError:
                self.chatHistory.configure(state=tk.NORMAL)
                self.chatHistory.insert(tk.END, "Connection to server was unsuccessful. Server is not running.\nEnsure that server is running, then press button again!\n\n")
                self.chatHistory.see(tk.END)
                self.chatHistory.configure(state=tk.DISABLED)
                print("Client: Server is not running!")
                return None

            except socket.gaierror:
                self.chatHistory.configure(state=tk.NORMAL)
                self.chatHistory.insert(tk.END, "Connection to server was unsuccessful.\nHost name or IP address is not found!\n\n")
                self.chatHistory.see(tk.END)
                self.chatHistory.configure(state=tk.DISABLED)
                print("Client: Please enter a valid host name!")
                return None

            self.connected = True
            self.key = Fernet.generate_key()
            self.sock.send(self.key)

            self.chatHistory.configure(state=tk.NORMAL)
            self.chatHistory.insert(tk.END, "Connection to server was successful.\n\n")
            self.chatHistory.see(tk.END)
            self.chatHistory.configure(state=tk.DISABLED)
            
            print(f'Client: This device (Client) is connected. Client\'s IP address is: {self.sock.getsockname()[0]}:{self.sock.getsockname()[1]}')
            name = self.name.get()
            if name != "":
                self.sock.send(FernetEncrypt(self.key, self.name.get().encode()))
            else:
                self.chatHistory.configure(state=tk.NORMAL)
                self.chatHistory.insert(tk.END, "Name field is empty. Please enter your name in the message box!\n\n")
                self.chatHistory.configure(state=tk.DISABLED)
            self.messageEntry.configure(state=tk.NORMAL)
            self.send_button.configure(state=tk.NORMAL)
            self.disconnectButton.configure(state=tk.NORMAL)
            self.connectButton.configure(state=tk.DISABLED)

            self.receive_thread = threading.Thread(target=self.receive_messages)
            self.receive_thread.start()
            

    def send_message(self, event=None):
        if self.connected:
            message = self.messageEntry.get()
            self.messageEntry.delete(0, tk.END)
            
            self.sock.sendall(FernetEncrypt(self.key, message.encode()))
            
    def receive_messages(self):
        while self.connected:
            try:
                message = self.sock.recv(1024).decode() + "\n"
            except ConnectionResetError:
                self.connected = False
                print("Client: The server has shut down or is not running currently.")
                
                self.connectButton.configure(state=tk.NORMAL)
                self.disconnectButton.configure(state=tk.DISABLED)
                self.chatHistory.configure(state=tk.NORMAL)
                self.chatHistory.insert(tk.END, f"\nServer has shutdown.\nYou have been disconnected from the server!\n\n")
                self.chatHistory.see(tk.END)
                self.chatHistory.configure(state=tk.DISABLED)
                self.messageEntry.configure(state=tk.DISABLED)
                self.send_button.configure(state=tk.DISABLED)
                break
            self.chatHistory.configure(state=tk.NORMAL)
            self.chatHistory.insert(tk.END, message)
            self.chatHistory.configure(state=tk.DISABLED)
            self.chatHistory.see(tk.END)
        print(f'Client: This client has disconnected. Client socket will be closed.')
        
        self.sock.close()



root = tk.Tk()
client = ChatClient(root)
root.protocol("WM_DELETE_WINDOW", client.onWindowClose)
root.mainloop()
