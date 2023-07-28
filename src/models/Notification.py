class Notification():
    
    def __init__(self, id ,id_usuario, fecha_generada, fecha_actualizada, detalle, leida, oculta, tipo, imei_vehiculo, identificador_tipo, contador_reenvios):
        self.id = id
        self.id_usuario = id_usuario
        self.fecha_generada = fecha_generada
        self.fecha_actualizada = fecha_actualizada
        self.detalle = detalle
        self.leida = leida
        self.oculta = oculta
        self.tipo = tipo
        self.imei_vehiculo = imei_vehiculo
        self.identificador_tipo = identificador_tipo
        self.contador_reenvios = contador_reenvios

    def to_json(self):
        return {
            'id': self.id,
            'id_usuario': self.id_usuario,
            'fecha_generada': self.fecha_generada,
            'fecha_actualizada': self.fecha_actualizada,
            'detalle': self.detalle,
            'leida': self.leida,
            'oculta': self.oculta,
            'tipo': self.tipo,
            'imei_vehiculo': self.imei_vehiculo,
            'identificador_tipo': self.identificador_tipo,
            'contador_reenvios': self.contador_reenvios,
        }