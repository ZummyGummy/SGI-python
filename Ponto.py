class Ponto(object):
    def __init__(self, _x, _y, _nome):
        self.x = _x
        self.y = _y
        self.nome = _nome

    def get_attributes(self):
        return str(self), self.nome

    def __str__(self):
        return 'Ponto'


