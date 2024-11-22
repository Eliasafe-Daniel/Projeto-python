import tkinter as tk
from tkinter import messagebox
from pymongo import MongoClient

#Conexão LOCAL com o MongoDB
#cliente = MongoClient("localhost", 27017)
#bd = cliente["bancodados"]
#tabela_usuario = bd["usuarios"]

#Substituir com os dados do MongoDB Atlas
connection_string = "mongodb+srv://<db_user>:<db_password>@<cluster>.f7ads.mongodb.net/?retryWrites=true&w=majority&appName=<cluster>"
cliente = MongoClient(connection_string)
bd = cliente["bancodados"]
tabela_usuario = bd["usuarios"]

def loginadmin():
        usuario = entrada_nome_adm.get()
        senha = entrada_senha_adm.get()
        
        user = tabela_usuario.find_one({"nomeusuario": usuario})
        if user and user["senha"] == senha and user["nomeusuario"] == "admin":
                messagebox.showinfo("Sucesso", "Admin logado com sucesso!")               
                def registrar():
                    usuario = entrada_usuario.get()
                    senha = entrada_senha.get()
                    
                    if tabela_usuario.find_one({"nomeusuario": usuario}):
                        messagebox.showerror("Erro", "Usuário já existe!")
                    else:
                        tabela_usuario.insert_one({"nomeusuario": usuario, "senha": senha})
                        messagebox.showinfo("Sucesso", "Registro feito com sucesso!")

                registro_frame = tk.Toplevel(app)
                registro_frame.title("Cadastrar Usuário")
                tk.Label(registro_frame, text="Registrar", font=("Arial", 16)).pack()
                entrada_usuario = tk.Entry(registro_frame, width=30)
                entrada_usuario.insert(0, "Usuário")
                entrada_usuario.pack(pady=5)
                entrada_senha = tk.Entry(registro_frame, width=30, show="*")
                entrada_senha.insert(0, "Senha")
                entrada_senha.pack(pady=5)
                registro_botao = tk.Button(registro_frame, text="Registrar", command=registrar)
                registro_botao.pack(pady=10)
                centralizarJanela(registro_frame, 300, 150) 
        else:
            messagebox.showerror("Erro", "Usuário ou senha incorretos!")

def login():
        usuario = entrada_nome_usuario.get()
        senha = entrada_senha_usuario.get()
        
        user = tabela_usuario.find_one({"nomeusuario": usuario})
        if user and user["senha"] == senha:
            messagebox.showinfo("Success", "Login feito com sucesso!")
            global usuario_atual
            usuario_atual = usuario
            app.destroy()
            iniciarmain()
        else:
            messagebox.showerror("Error", "Usuário ou senha incorretos!")

def iniciarmain():
     import main
     main.iniciar(usuario_atual)

def centralizarJanela(janela, largura, altura):
    largura_tela = janela.winfo_screenwidth()
    altura_tela = janela.winfo_screenheight()
    x = (largura_tela // 2) - (largura // 2)
    y = (altura_tela // 2) - (altura // 2)

    janela.geometry(f"{largura}x{altura}+{x}+{y}")

app = tk.Tk()
centralizarJanela(app, 600, 600) 
app.title("Estoque de Produtos")
app.geometry("300x400")

login_frame = tk.Frame(app)
login_frame.pack(pady=20)

tk.Label(login_frame, text="Login", font=("Arial", 16)).pack()
entrada_nome_usuario = tk.Entry(login_frame, width=30)
entrada_nome_usuario.insert(0, "Usuário")
entrada_nome_usuario.pack(pady=5)
entrada_senha_usuario = tk.Entry(login_frame, width=30, show="*")
entrada_senha_usuario.insert(0, "Senha")
entrada_senha_usuario.pack(pady=5)
login_botao = tk.Button(login_frame, text="Login", command=login)
login_botao.pack(pady=10)

loginadm_frame = tk.Frame(app)
loginadm_frame.pack(pady=20)

tk.Label(loginadm_frame, text="Admin Login", font=("Arial", 16)).pack()
entrada_nome_adm = tk.Entry(loginadm_frame, width=30)
entrada_nome_adm.pack(pady=5)
entrada_senha_adm = tk.Entry(loginadm_frame, width=30, show="*")
entrada_senha_adm .pack(pady=5)
login_adm_botao = tk.Button(loginadm_frame, text="Admin Login", command=loginadmin)
login_adm_botao.pack(pady=10)

app.mainloop()
