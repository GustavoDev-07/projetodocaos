#substituir "modules.mysql pela pasta onde esta o arquivo e o nome do arquivo respectivamente" substituir "MySql" pela classe do banco
from modules.mysql import MySQL

class cadastro_livros:
    def __init__(self, livros, genero, autor, ano, idade, sinopse, imagem):
        self.livros = livros
        self.genero = genero
        self.autor = autor
        self.ano = ano
        self.idade = idade
        self.sinopse = sinopse
        self.imagem = imagem

    def cadastrar(self, db=MySQL()):
#substituir todos os "alunos" daqui pra baixo pelo nome do banco
        query = """
            INSERT INTO alunos(
            livros,genero,autor,ano,idade,sinopse,imagem
        ) VALUES(
            %s,%s,%s,%s,%s,%s,%s
        )
        """
        
        values = (
            self.livros,
            self.genero,
            self.autor,
            self.ano,
            self.idade,
            self.sinopse,
            self.imagem,
        )
        return db.execute_query(query, values)
    
    def listar(db:MySQL):
        query = """
            SELECT  
                livros,
                genero,
                autor,
                ano,
                idade,
                sinopse,
                imagem
            FROM 
                alunos
        """
        return db.execute_query(query)
    
    def editar(self):
        pass
    
    def transferir(self):
        pass