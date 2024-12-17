class Circuito:
    def __init__(self, id_circuito, nome, tempo_descolcamento, KM, curvas, cones, local):
        self.id_circuito = id_circuito
        self.nome = nome
        self.tempo_descolcamento = tempo_descolcamento
        self.KM = KM
        self.curvas = curvas
        self.cones = cones
        self.local = local
        if id_circuito != None:
            self.caminho = "circuito" + str(id_circuito) + ".PNG"
    def modificar(self, nome, tempo_descolcamento, KM, curvas, cones, local):
        self.nome = nome
        self.tempo_descolcamento = tempo_descolcamento
        self.KM = KM
        self.curvas = curvas
        self.cones = cones
        self.local = local
