class GsUserObjects():
    
    def __init__(self, object_id ,user_id, imei, group_id, driver_id, trailer_id, velocidad_alerta, alerta_enviada):
        self.object_id = object_id
        self.user_id = user_id
        self.imei = imei
        self.group_id = group_id
        self.driver_id = driver_id
        self.trailer_id = trailer_id
        self.velocidad_alerta = velocidad_alerta
        self.alerta_enviada = alerta_enviada

    def to_json(self):
        return {
            'object_id': self.object_id,
            'user_id': self.user_id,
            'imei': self.imei,
            'group_id': self.group_id,
            'driver_id': self.driver_id,
            'trailer_id': self.trailer_id,
            'velocidad_alerta': self.velocidad_alerta,
            'alerta_enviada': self.alerta_enviada,
        }