import socket
import threading
import tkinter as tk
from tkinter import messagebox

openPorts = []
permissionErrorPorts = []

def scanPort(IPAddress, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(0.5)
    try:
        sock.connect((IPAddress, port))
        print(f"Port {port} is open")
        openPorts.append(port)
        sock.close()
    except PermissionError:
        permissionErrorPorts.append(port)

    except TimeoutError:
        pass

def multiThreadingScanAllPorts(IPAddress, startingPortNumber, endingPortNumber):
    
    root = tk.Tk() # Create new window and popup.
    root.title("Open Ports")

    windowWidth = 300
    windowHeight = 250
    screenWidth = root.winfo_screenwidth()
    screenHeight = root.winfo_screenheight()
    x = int((screenWidth / 2) - (windowWidth / 2))
    y = int((screenHeight / 2) - (windowHeight / 2))
    root.geometry(f"+{x}+{y}")

    activeThreads = []
    for port in range(startingPortNumber, endingPortNumber+1):
        t = threading.Thread(target=scanPort, args=(IPAddress, port))
        activeThreads.append(t)
        t.start()

    for t in activeThreads: 
        t.join()
    
    openPortsLabel = tk.Label(root, text="Open Ports:")
    openPortsLabel.pack(pady=10)

    for port in openPorts:
        openPortsLabel = tk.Label(root, text=f"Port {port} is open")
        openPortsLabel.pack()

    unauthorisedPortsLabel = tk.Label(root, text="Unauthorised Ports:")
    unauthorisedPortsLabel.pack(pady=10)

    for port in permissionErrorPorts:
        unauthorisedPortsLabel = tk.Label(root, text=f"Port {port} has a permission error!")
        unauthorisedPortsLabel.pack()

    root.mainloop()

def start_scan():
    IPAddress = IPAddressInput.get()
    try:
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((IPAddress, 1))

    except socket.gaierror:
        print("IP address does not exist! Please enter a valid IP address!")
        messagebox.showinfo("IP Address Error", "IP address does not exist! Please enter a valid IP address!")
        return None

    except ConnectionRefusedError:
        pass
    

    try:
        startingPortNumber = int(startingPortNumberInput.get())

        if not(startingPortNumber >= 0 and startingPortNumber <= 65535):
            print("Please enter a valid number for your starting port number! It should be a number from 0 to 65535")
            messagebox.showinfo("Starting port number out of range", "Please enter a valid number for your starting port number! It should be a number from 0 to 65535")
            return None
    except ValueError:
            print("Please enter a valid number for your starting port number!")
            messagebox.showinfo("Starting port number is not a number", "Please enter a valid number for your starting port number! It should be a number from 0 to 65535")
            return None
    try:
        endingPortNumber = int(endingPortNumberInput.get())

        if not(endingPortNumber >= 0 and endingPortNumber <= 65535):
            print("Please enter a valid number for your ending port number! It should be a number from 0 to 65535")
            messagebox.showinfo("Ending port number out of range", "Please enter a valid number for your ending port number! It should be a number from 0 to 65535")
            return None
        
        if endingPortNumber < startingPortNumber:
            print("Please enter an ending port number > starting port number!")
            messagebox.showinfo("Ending port greater than starting port number", "Please enter an ending port number > starting port number!")
            return None
        
    except ValueError:
            print("Please enter a valid number for your ending port number!")
            messagebox.showinfo("Ending port number is not a number", "Please enter a valid number for your ending port number! It should be a number from 0 to 65535")
            return None
    multiThreadingScanAllPorts(IPAddress, startingPortNumber, endingPortNumber)

root = tk.Tk()
root.title("Port Scanner")

IPAddressLabel = tk.Label(root, text="IP Address:")
IPAddressLabel.pack(pady=10)
IPAddressInput = tk.Entry(root, justify = "center")
IPAddressInput.insert(0, "localhost")
IPAddressInput.pack()

startingPortNumberLabel = tk.Label(root, text="Starting Port Number (inclusive):")
startingPortNumberLabel.pack(pady=10)
startingPortNumberInput = tk.Entry(root, justify = "center")
startingPortNumberInput.insert(0, "1")
startingPortNumberInput.pack()

endingPortNumberLabel = tk.Label(root, text="Ending Port Number (inclusive):")
endingPortNumberLabel.pack(pady=10)
endingPortNumberInput = tk.Entry(root, justify = "center")
endingPortNumberInput.insert(0, "65535")
endingPortNumberInput.pack()

beginScanButton = tk.Button(root, text="Scan", command=start_scan)
beginScanButton.pack(pady=10)

windowWidth = 300
windowHeight = 250
screenWidth = root.winfo_screenwidth()
screenHeight = root.winfo_screenheight()
x = int((screenWidth / 2) - (windowWidth / 2))
y = int((screenHeight / 2) - (windowHeight / 2))
root.geometry(f"{windowWidth}x{windowHeight}+{x}+{y}")

root.mainloop()