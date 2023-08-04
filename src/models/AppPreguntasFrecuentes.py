class AppPreguntasFrecuentes():

    def __init__(self, pregunta, detalle):
        self.pregunta = pregunta
        self.detalle = detalle

    def to_json(self):
        return {
            'pregunta': self.pregunta,
            'detalle': self.detalle
        }