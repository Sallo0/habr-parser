from dataclasses import dataclass
from environs import Env

env = Env()
env.read_env()


@dataclass
class Settings:
    DB_USER: str = env('DB_USER')
    DB_PASSWORD: str = env('DB_PASSWORD')
    DB_NAME: str = env('DB_NAME')
    DB_HOST: str = env('DB_HOST')
    DB_PORT: int = env.int('DB_PORT')

    @property
    def DB_URL(self):
        return (f'postgresql+asyncpg://{self.DB_USER}:'
                f'{self.DB_PASSWORD}@{self.DB_HOST}:'
                f'{self.DB_PORT}/{self.DB_NAME}')


settings = Settings()
