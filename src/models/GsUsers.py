class GsUsers():

    def __init__(self, id, email, username, tipo_user, info, timezone, activo):
        self.id = id
        self.email = email
        self.username = username
        self.tipo_user = tipo_user
        self.info = info
        self.timezone = timezone
        self.activo = activo

    def to_json(self):
        return {
            'id': self.id,
            'email': self.email,
            'username': self.username,
            'tipo_user': self.tipo_user,
            'info': self.info,
            'timezone': self.timezone,
            'activo': self.activo,
        }