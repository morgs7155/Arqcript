import customtkinter as ctk
import tkinter as tk
import os
from PIL import Image
import cryptography
from tkinter import filedialog
from cryptography.fernet import Fernet
from tkinter import messagebox

class Encript():
    def __init__(self, master):
        self.master = master
        self.master.bind('<Configure>', self.on_resize)
        self.Setup()
        
    def Setup(self):
        self.Frames()
        self.Icons()
        self.Labels()
        self.Generate_key()
        self.Load_key()
        self.Buttons()
        
    def Frames(self):
        self.f_screen = ctk.CTkFrame(self.master, fg_color='#f4f4f4', width=screen.winfo_screenwidth(), height=screen.winfo_screenheight())
        self.f_screen.pack(side=tk.TOP, expand=True)
        
    def Icons(self):
        try:
            self.icon_cypher_open = Image.open("assepts/icons/file-protection.png")
            self.icon_cypher = ctk.CTkImage(self.icon_cypher_open, size=(100, 100))
        except:
            messagebox.showerror("Erro", "Erro ao abrir a imagem")
            
    def Labels(self):
        self.label_widgets = []
        self.l_icon = ctk.CTkLabel(self.f_screen, image=self.icon_cypher, text='')
        self.l_icon.place(relx=0.10, y=0.5)
        
        self.l_title = ctk.CTkLabel(self.f_screen, text="ARQRIPT", font=("Fixedsys", 52, "bold"))
        self.l_title.place(relx=0.30, rely=0.1)
        
        self.l_title = ctk.CTkLabel(self.f_screen, text=f"quer manter seu arquivo seguro?\ncriptografe seus arquivos com o Arqcript", font=("Arial", 12, "bold"))
        self.l_title.place(relx=0.26, rely=0.3)
    
    def Buttons(self):
        self.btn_widget = []
        self.btn_select = ctk.CTkButton(self.f_screen, text='Selecionar Arquivo', fg_color='blue', text_color='white',hover_color='#87CEFA', width=150, height=50, command=self.Select_file)
        self.btn_select.place(relx=0.35, rely=0.4)

        self.btn_encript = ctk.CTkButton(self.f_screen, text='ENCRIPTAR', fg_color='red', text_color='white',hover_color='#FA7B7C', width=150, height=50, command=self.Encript, state="disabled")
        self.btn_encript.place(relx=0.35, rely=0.6)

        self.btn_descript = ctk.CTkButton(self.f_screen, text='DESENCRIPTAR', fg_color='red', text_color='white',hover_color='#FA7B7C', width=150, height=50, command=self.Desencript, state="disabled")
        self.btn_descript.place(relx=0.35, rely=0.8)

    def Select_file(self):
        self.file_path = filedialog.askopenfilename(title='Selecione o arquivo', filetypes=(("Arquivos", "*.*"), ("Todos os arquivos", "*.*")))
        if self.file_path:
            messagebox.showinfo("Arquivo Selecionado", f"Arquivo selecionado:\n{self.file_path}")
            self.btn_select.configure(state="disabled")
            self.btn_encript.configure(state="normal")
            self.btn_descript.configure(state="normal")

        
    def on_resize(self, event): 
        for idx, label in enumerate(self.label_widgets): 
            label.place_configure(relx=0.10, rely=0.1 + idx*0.2) 
        
        for idx, btn in enumerate(self.btn_widget): 
            btn.place_configure(relx=0.10 + idx*0.5, rely=0.1 + idx*0.5, relwidth=0.50)
    
    def Generate_key(self):
        if not os.path.exists("key.key"):
            key = Fernet.generate_key()
            with open("key.key", "wb") as key_file:
                key_file.write(key)

        
    def Load_key(self):
        return open("key.key", "rb").read()
    
    def Config_encript(self, file_name):
        key = self.Load_key() 
        fernet = Fernet(key) 
        with open(file_name, "rb") as file:
            file_data = file.read()
            encrypted_data = fernet.encrypt(file_data)
        
        with open(file_name, "wb") as file: 
            file.write(encrypted_data) 
    
    def Config_desencript(self, file_name):
        try:
            key = self.Load_key() 
            fernet = Fernet(key) 
            with open(file_name, "rb") as file:
                encrypted_data = file.read()
            
            # Tenta descriptografar
            decrypted_data = fernet.decrypt(encrypted_data)
            
            with open(file_name, "wb") as file:
                file.write(decrypted_data) 
            
        except FileNotFoundError:
            messagebox.showerror("Erro", "Arquivo não encontrado!")
            
        except cryptography.fernet.InvalidToken:
            messagebox.showerror("Erro", "O arquivo não pode ser descriptografado. A chave pode estar incorreta ou o arquivo foi alterado.")
        
        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro: {e}")

    def Encript(self):
        try:
            self.Config_encript(self.file_path)   
            messagebox.showinfo("encript", "O arquivo foi encriptado com sucesso!")
            self.btn_select.configure(state="normal")
            
        except FileNotFoundError as e:
            messagebox.showerror("Erro ao abrir arquivo", "Arquivo não encontrado")
            
        except FileExistsError as e:
            messagebox.showerror("Erro ao abrir arquivo", "Arquivo não encontrado")
            
        except Exception as e:
            messagebox.showerror("Erro ao abrir arquivo", f"erro: {e}")
    
    def Desencript(self):
        try:
            self.Config_desencript(self.file_path)
            messagebox.showinfo("descript", "O arquico foi desencripitado com sucesso!")
            
        except FileNotFoundError as e:
            messagebox.showerror("Erro ao abrir arquivo", "Arquivo não encontrado")
        
        except Exception as e:
            messagebox.showerror("Erro ao abrir arquivo", f"erro: {e}")
    
if __name__ == '__main__':
    screen = ctk.CTk()
    app = Encript(screen)
    screen.title("Arqript")
    screen.geometry("500x500")
    screen.minsize(400, 400)
    screen.maxsize(600,600)
    screen.mainloop()