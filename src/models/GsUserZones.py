class GsUserZones():

    def __init__(self, zone_vertices, imei):
        self.zone_vertices = zone_vertices
        self.imei = imei

    def to_json(self):
        return {
            'zone_vertices': self.zone_vertices,
            'imei': self.imei
        }