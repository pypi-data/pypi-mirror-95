from .scram import Scram
from mindsdb.utilities.config import Config

class Session():
    def __init__(self, config):
        self.config = config

    def init_scram(self):
        user = self.config['api']['mongodb'].get('user', '')
        password = self.config['api']['mongodb'].get('password', '')
        self.scram = Scram(user, password)
