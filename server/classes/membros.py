class Membros:
    def __init__(self, email, senha, nome, subgrupo) ->None:
        self.email = email
        self.senha = senha
        self.nome = nome
        self.subgrupo = subgrupo

    def modifica(self, nome, subgrupo, senha) -> None:
        self.nome = nome
        self.subgrupo = subgrupo
        if senha != None:
            self.senha = senha
