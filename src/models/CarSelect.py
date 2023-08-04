class CarSelect():

    def __init__(self, name, plate_number, lat, lat_lng, speed, imei, angle, odometer, active, comando_corte, protocol, ip, port, params, alertas, comandos, last_posi, geocerca_imei):
        self.name = name
        self.plate_number = plate_number
        self.lat = lat
        self.lat_lng = lat_lng
        self.speed = speed
        self.imei = imei
        self.angle = angle
        self.odometer = odometer
        self.active = active
        self.comando_corte = comando_corte
        self.protocol = protocol
        self.ip = ip
        self.port = port
        self.params = params
        self.alertas = alertas
        self.comandos = comandos
        self.last_posi = last_posi
        self.geocerca_imei = geocerca_imei

    def to_json(self):
        return {
            'name': self.name,
            'plate_number': self.plate_number,
            'lat': self.lat,
            'lat_lng': self.lat_lng,
            'speed': self.speed,
            'imei': self.imei,
            'angle': self.angle,
            'odometer': self.odometer,
            'active': self.active,
            'comando_corte': self.comando_corte,
            'protocol': self.protocol,
            'ip': self.ip,
            'port': self.port,
            'params': self.params,
            'alertas': self.alertas,
            'comandos': self.comandos,
            'last_posi': self.last_posi,
            'geocerca_imei': self.geocerca_imei,
        }
