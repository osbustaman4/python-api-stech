class ObjectData:

    def __init__(self, dt_server, dt_tracker, lat, lng, altitude, angle, speed, params, overpass) -> None:
        self.dt_server = dt_server
        self.dt_tracker = dt_tracker
        self.lat = lat
        self.lng = lng
        self.altitude = altitude
        self.angle = angle
        self.speed = speed
        self.params = params
        self.overpass = overpass


    def to_json(self):
        return {
            'dt_server': self.dt_server,
            'dt_tracker': self.dt_tracker,
            'lat': self.lat,
            'lng': self.lng,
            'altitude': self.altitude,
            'angle': self.angle,
            'speed': self.speed,
            'params': self.params,
            'overpass': self.overpass,
        }