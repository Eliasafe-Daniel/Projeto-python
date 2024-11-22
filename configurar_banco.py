from pymongo import MongoClient

#Conexão local com o MongoDB
#cliente = MongoClient("localhost", 27017)
#bd = cliente["bancodados"]
#tabela_usuario = bd["usuarios"]
#coluna1 = bd["Produto"]

#Conexão com o MongoDB Atlas
connection_string = "mongodb+srv://<db_user>:<db_password>@<cluster>.f7ads.mongodb.net/?retryWrites=true&w=majority&appName=<cluster>"
cliente = MongoClient(connection_string)
bd = cliente["bancodados"]
tabela_usuario = bd["usuarios"]
coluna1 = bd["Produto"]


cadastrar_admin = {"nomeusuario": "admin", "senha": "admin"}
tabela_usuario.insert_one(cadastrar_admin)
print("Admin cadastrado")

cadastrar_produto = {"nome": "Refrigerante 1L", "preco": 5.50, "quantidade": 0, "usuario": "admin"}
coluna1.insert_one(cadastrar_produto)
print("Produto cadastrado")
