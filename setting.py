from pydantic import BaseSettings


class Settings(BaseSettings):
    db_name: str
    db_user: str
    db_password: str
    db_url: str
    slack_token: str
    naver_client_id: str
    naver_secret_key: str
    init_user: str
    init_pwd: str
    jwt_secret: str
    jwt_algorithm: str
    graph_path: str

    class Config:
        env_file = ".env"  # .env 파일 로드


settings = Settings()
