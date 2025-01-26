# engine elements
import Engine

class Mash:
    def __init__(self, vao: 'Engine.graphic.VAO', material: 'Engine.objects.Material') -> None:
        """ Engine graphics heart """
        self.vao = vao
        self.material = material
