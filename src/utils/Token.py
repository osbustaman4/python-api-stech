import jwt
import datetime


class Token():

    expirationTime = datetime.datetime.utcnow() + datetime.timedelta(hours=1)

    @classmethod
    def __generateToken(self, secretKey):

        # Payload del token (información adicional si es necesario)
        payload = {
            'exp': self.expirationTime,  # Tiempo de expiración del token
            'datos': 'Informacion adicional si es necesario'
        }

        # Generamos el token JWT
        token = jwt.encode(payload, secretKey, algorithm='HS256')

        return payload, token