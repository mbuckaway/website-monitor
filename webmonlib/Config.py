from dotenv import dotenv_values
import os

class Config:
    '''
    Configuration class. All configuration information is stored here. By default,
    we read from the environment, but allow it to be overriden with a .env file.
    '''
    def __init__(self, envfile=".env"):
        '''
        Initialize our configuration from the environment and optionally an .env file
        '''
        requiredItems = [
            'DATABASE_HOST',
            'DATABASE_PORT',
            'DATABASE_DB',
            'DATABASE_USER',
            'DATABASE_PASSWD',
            'KAFKA_HOST',
            'KAFKA_TOPIC',
            'KAFKA_USER',
            'KAFKA_CAFILE',
            'KAFKA_CERTFILE',
            'KAFKA_KEYFILE',
        ]
        # Load our config from the .env file overriding with existing env vars
        config = {
            **dotenv_values(envfile),
            **os.environ,
        }

        # Validate we have our complete config
        for key in requiredItems:
            if not config[key]:
                raise ValueError(f"Config variable {key} required and is missing")

        # Load our config
        self.property_database_host=config['DATABASE_HOST']
        self.property_database_port=int(config['DATABASE_PORT'])
        self.property_database_db=config['DATABASE_DB']
        self.property_database_user=config['DATABASE_USER']
        self.property_database_passwd=config['DATABASE_PASSWD']
        self.property_database_host=config['DATABASE_HOST']
        self.property_kafka_host=config['KAFKA_HOST']
        self.property_kafka_topic=config['KAFKA_TOPIC']
        self.property_kafka_user=config['KAFKA_USER']
        self.property_kafka_cafile=config['KAFKA_CAFILE']
        self.property_kafka_certfile=config['KAFKA_CERTFILE']
        self.property_kafka_keyfile=config['KAFKA_KEYFILE']

    @property
    def DATABASE_HOST(self) -> str:
        return self.property_database_host

    @property
    def DATABASE_PORT(self) -> int:
        return self.property_database_port

    @property
    def DATABASE_DB(self) -> str:
        return self.property_database_db

    @property
    def DATABASE_USER(self) -> str:
        return self.property_database_user

    @property
    def DATABASE_PASSWD(self) -> str:
        return self.property_database_passwd

    @property
    def DATABASE_HOST(self) -> str:
        return self.property_database_host

    @property
    def KAFKA_HOST(self) -> str:
        return self.property_kafka_host

    @property
    def KAFKA_TOPIC(self) -> str:
        return self.property_kafka_topic

    @property
    def KAFKA_USER(self) -> str:
        return self.property_kafka_user

    @property
    def KAFKA_CAFILE(self) -> str:
        return self.property_kafka_cafile

    @property
    def KAFKA_CERTFILE(self) -> str:
        return self.property_kafka_certfile

    @property
    def KAFKA_KEYFILE(self) -> str:
        return self.property_kafka_keyfile
