from tkinter import messagebox
from pymongo import MongoClient
import tkinter as tk
from tkinter import ttk

#Conexão LOCAL com o MongoDB
#cliente = MongoClient("localhost", 27017)
#bd = cliente["bancodados"]
#coluna1 = bd["Produto"]

#Substituir com os dados do MongoDB Atlas
connection_string = "mongodb+srv://<db_user>:<db_password>@<cluster>.f7ads.mongodb.net/?retryWrites=true&w=majority&appName=<cluster>"
cliente = MongoClient(connection_string)
bd = cliente["bancodados"]
coluna1 = bd["Produto"]


user = ""
def iniciar(usuario_atual):
    global user
    user = usuario_atual
    print("login feito por:", user)
    root.mainloop()

def centralizarJanela(janela, largura, altura):
    largura_tela = janela.winfo_screenwidth()
    altura_tela = janela.winfo_screenheight()
    x = (largura_tela // 2) - (largura // 2)
    y = (altura_tela // 2) - (altura // 2)

    janela.geometry(f"{largura}x{altura}+{x}+{y}")

def listarProdutos():
    
    for item in tabela.get_children():
        tabela.delete(item)

    for produto in coluna1.find():
        tabela.insert(
            "", "end",
            values=(
                produto.get("nome", "N/A"), 
                produto.get("preco", 0.0), 
                produto.get("quantidade", 0),
                produto.get("nomeusuario")
            )
        )

def abrirTelaAdicionar():    
    def adicionarNovoProduto():
        try:
            nomeproduto = nomeProdutoEntrada.get()
            precoproduto = precoProdutoEntrada.get()
           
            dic_produto = {
                "nome": nomeproduto,
                "preco": float(precoproduto),
                "quantidade": 0,
                "nomeusuario": user
            }

            
            coluna1.insert_one(dic_produto)
            messagebox.showwarning("Alerta", "Produto adicionado com sucesso!")
            
            listarProdutos()

            adicionarJanela.destroy()
        except ValueError:
            messagebox.showwarning("Alerta", "Erro: Preço deve ser numérico.")

    adicionarJanela = tk.Toplevel(root)
    adicionarJanela.title("Cadastrar Produto")
    
    nomeProdutoTitulo = tk.Label(adicionarJanela, text="Nome:")
    nomeProdutoEntrada = tk.Entry(adicionarJanela,width=50)
    precoProdutoTitulo = tk.Label(adicionarJanela, text="Preço:")
    precoProdutoEntrada = tk.Entry(adicionarJanela,width=50)

    enviarBotao = tk.Button(adicionarJanela, text="Adicionar", command=adicionarNovoProduto)

    nomeProdutoTitulo.grid(row=0, column=0, padx=5, pady=5)
    nomeProdutoEntrada.grid(row=0, column=1, padx=5, pady=5)
    precoProdutoTitulo.grid(row=1, column=0, padx=5, pady=5)
    precoProdutoEntrada.grid(row=1, column=1, padx=5, pady=5)
    enviarBotao.grid(row=3, column=0, columnspan=2, pady=10)
    centralizarJanela(adicionarJanela,400,100)

def abriTelaFuncoesEstoque():
    def atualizarEstoque():
        novaQuantidade = int(quantidade)
        novaQuantidade = novaQuantidade + int(quantidadeVar.get())
        
        if novaQuantidade < 0:
            novaQuantidade = 0

        coluna1.update_one(
            {"nome":nome},
            {"$set":{"quantidade":novaQuantidade,"usuario":user}}
        )

        messagebox.showinfo("Sucesso", "Estoque atualizado com sucesso!")
        adicionarJanela.destroy()
        listarProdutos()
        
    linhaSelecionada = tabela.selection()

    if not linhaSelecionada:
        messagebox.showwarning("Alerta", "Nenhuma linha foi selecionada")
        return
    
    valores = tabela.item(linhaSelecionada[0], "values")
    nome,preco,quantidade,nomeusuario = valores
    adicionarJanela = tk.Toplevel(root)
    adicionarJanela.title("Funções do Estoque")

    nomeVar = tk.StringVar(value=nome)
    quantidadeVar = tk.StringVar(value=int(quantidade))
    
    nomeProdutoTitulo = tk.Label(adicionarJanela, text="Nome:")
    nomeProdutoEntrada = tk.Entry(adicionarJanela, textvariable=nomeVar, width=30)
    precoProdutoTitulo = tk.Label(adicionarJanela, text="Quantidade:")
    precoProdutoEntrada = tk.Entry(adicionarJanela,textvariable=(quantidadeVar), width=30)
    botaoAtualizarEstoque = tk.Button(adicionarJanela,text="Atualizar Estoque", command=atualizarEstoque)

    nomeProdutoTitulo.grid(row=0, column=0, padx=5, pady=5)
    nomeProdutoEntrada.grid(row=0, column=1, padx=5, pady=5)
    precoProdutoTitulo.grid(row=1, column=0, padx=5, pady=5)
    precoProdutoEntrada.grid(row=1, column=1, padx=5, pady=5)
    botaoAtualizarEstoque.grid(row=2, column=1, padx=5, pady=5)

    centralizarJanela(adicionarJanela,400,100)

def abrirTelaDeletarProduto():
    def deletarProduto():
        coluna1.delete_one({"nome":nome})
        messagebox.showinfo("Sucesso", "Produto deletado com sucesso!")
        adicionarJanela.destroy()
        listarProdutos()

    linhaSelecionada = tabela.selection()

    if not linhaSelecionada:
        messagebox.showwarning("Alerta", "Nenhuma linha foi selecionada")
        return

    valores = tabela.item(linhaSelecionada[0], "values")
    nome,preco,quantidade,nomeusuario = valores

    adicionarJanela = tk.Toplevel(root)
    adicionarJanela.title("Deletar Produto")

    texto = tk.Label(adicionarJanela, text=f"Tem certeza que deseja deletar o prduto {nome}?", wraplength=400)

    botaoDeletarProduto = tk.Button(adicionarJanela,text="Deletar Produto", command=deletarProduto)
    botaoCancelar = tk.Button(adicionarJanela, text="Cancelar", command=adicionarJanela.destroy)

    texto.grid(row=0,column=0,columnspan=2, padx=10,pady=10)
    botaoDeletarProduto.grid(row=1, column=0, padx=10, pady=10)
    botaoCancelar.grid(row=1, column=1, padx=10, pady=10)

    centralizarJanela(adicionarJanela,400,150)
    
root = tk.Tk()
centralizarJanela(root, 1000, 400) 
root.title("Estoque de Produtos")

tabela = ttk.Treeview(root, columns=("nome", "preco", "quantidade","nomeusuario"), show="headings")
tabela.heading("nome", text="Nome")
tabela.heading("preco", text="Preço")
tabela.heading("quantidade", text="Quantidade")
tabela.heading("nomeusuario", text="Responsável")
tabela.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

frameBotoes = tk.Frame(root)
frameBotoes.pack(pady = 10)

#Adicionar novo produto
adicionarbotaoNovoProduto = tk.Button(frameBotoes, text="Cadastrar Produto", command = abrirTelaAdicionar)
adicionarbotaoNovoProduto.grid(row = 0, column = 1, padx = 5)

#Atualizar Estoque
atualizarEstoque = tk.Button(frameBotoes, text="Atualizar Estoque", command = abriTelaFuncoesEstoque)
atualizarEstoque.grid(row = 0, column = 2, padx = 5)

#Deletar Produto
deletarProduto = tk.Button(frameBotoes, text="Deletar Produto", command = abrirTelaDeletarProduto)
deletarProduto.grid(row = 0, column = 3, padx = 5)

listarProdutos()
