import datetime

class Token():

    expirationTime = datetime.datetime.utcnow() + datetime.timedelta(hours=1)

    @classmethod
    def generateToken(self):
        pass
