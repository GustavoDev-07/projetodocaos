from --- import ---

class Usuario:
    def __init__(self, nome, email, idade, senha):
        self.nome = nome
        self.email = email
        self.senha = senha
        self.idade = idade

    def cadastrar(self, db: MySQL):
        query = """
        INSERT INTO cadastro_de_pessoas (
            nome,
            email,
            idade,
            senha
            )
            VALUES (
                %s, %s, %s, %s, %s
            )
        """
        values = (
            self.nome,
            self.email,
            self.senha,
            self.idade
        )
        
        return db.execute_query(query, values)
    
    def listar(db: MySQL):
        query = """
            SELECT 
                id,
                nome,
                email,
                idade,
                senha
            FROM
                cadastro_de_pessoas
        """
        return db.execute_query(query)
    
    def editar(self):
        pass