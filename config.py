class Config:
    DEBUG = False
    REGION = "us-west-2"
    KNOWLEDGE_BASE = "your_secret_key"
    OPENSEARCH_HOST = "sqlite:///database.db"
    USER_TABLE_NAME = "ai_users"


class ProductionConfig(Config):
    DEBUG = False


class DevelopmentConfig(Config):
    DEBUG = True
    OPENSEARCH_HOST = "sqlite:///dev_database.db"
