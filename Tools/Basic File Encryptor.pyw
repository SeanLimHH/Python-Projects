import tkinter as tk

def encrypt(filename, key): # Caesar cipher variant

    with open(filename, "rb") as file:
        contents = file.read()

    encryptedBytes = bytearray()

    for byte in contents:

        if byte != 0:
            encryptedByte = (byte + key) % 256
            encryptedBytes.append(encryptedByte)

        else:
            encryptedBytes.append(byte)

    encryptedFilename = f"{filename}.encrypted"

    with open(encryptedFilename, 'wb') as file:
        file.write(encryptedBytes)


    return encryptedFilename

def decrypt(filename, key): # Caesar cipher variant

    with open(filename, "rb") as file:
        contents = file.read()

    decryptedBytes = bytearray()

    for byte in contents:

        # Only decrypt non-empty bytes
        if byte != 0:
            decryptedByte = (byte - key) % 256
            decryptedBytes.append(decryptedByte)
        else:
            decryptedBytes.append(byte)

    decryptedFilename = filename[:-10]
    
    with open(decryptedFilename, 'wb') as file:
        file.write(decryptedBytes)


    return decryptedFilename


class BasicTextFileEncrypt(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title("Caesar Cipher File Encryptor/Decryptor")
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        # File name input field
        windowWidth = 500
        windowHeight = 200
        screenWidth = root.winfo_screenwidth()
        screenHeight = root.winfo_screenheight()
        x = int((screenWidth / 2) - (windowWidth / 2))
        y = int((screenHeight / 2) - (windowHeight / 2))
        root.geometry(f"{windowWidth}x{windowHeight}+{x}+{y}")

        self.fileName = tk.Label(self, text="Enter file name (with extension):")
        self.fileName.pack()
        self.fileNameInput = tk.Entry(self)
        self.fileNameInput.pack()

        # Encryption key input field
        self.keyLabel = tk.Label(self, text="Enter an encryption/decryption key (0-50):")
        self.keyLabel.pack()
        self.keyInput = tk.Entry(self)
        self.keyInput.pack()

        # Encrypt button
        self.encryptButton = tk.Button(self, text="Encrypt", command=self.encrypt)
        self.encryptButton.pack()

        # Decrypt button
        self.decryptButton = tk.Button(self, text="Decrypt", command=self.decrypt)
        self.decryptButton.pack()

        # Status label
        self.statusLabel = tk.Label(self, text="")
        self.statusLabel.pack()

    def encrypt(self):
        
        filename = self.fileNameInput.get()
        
        try:
            key = int(self.keyInput.get())
            if not(key >= 0 and key <= 50):
                print("Please enter a valid number for your key! It should be a number from 0 to 50")
                self.statusLabel.config(text="Encryption failed. Please enter a valid number for your key!\nIt should be a number from 0 to 50!")
                return None

        except ValueError:
            self.statusLabel.config(text="Encryption failed. Please enter a valid number for the key!")
            return None
        
        try:
            success = encrypt(filename, key)
        except FileNotFoundError:
            self.statusLabel.config(text="Encryption failed. File does not exist!")
            return None
        
        if success:
            self.statusLabel.config(text="Encryption successful.")
        else:
            self.statusLabel.config(text="Encryption failed. An error occurred during the encryption process.")

    def decrypt(self):
        
        filename = self.fileNameInput.get()

        try:
            key = int(self.keyInput.get())
        except ValueError:
            self.statusLabel.config(text="Decryption failed. Please enter a valid number for the key!")
            return None

        try:
            success = decrypt(filename, key)

        except FileNotFoundError:
            self.statusLabel.config(text="Decryption failed. File does not exist!")
            return None

        if success:
            self.statusLabel.config(text="Decryption key applied. File may or may not be decrypted correctly!")
        else:
            self.statusLabel.config(text="Decryption failed. An error occurred during the decryption process.")


root = tk.Tk()
app = BasicTextFileEncrypt(master=root)
app.mainloop()