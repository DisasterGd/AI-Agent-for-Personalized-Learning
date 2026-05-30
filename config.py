import os
from dotenv import load_dotenv

# 加载项目根目录.env环境变量
load_dotenv()


class Config:
    # 基础配置
    SECRET_KEY = "software-cup-dev-secret-key"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # 数据库配置
    DB_HOST = os.getenv("DB_HOST") or "127.0.0.1"
    DB_PORT = int(os.getenv("DB_PORT") or 3306)
    DB_USER = os.getenv("DB_USER") or "root"
    DB_PASSWORD = os.getenv("DB_PASSWORD") or "20100714"
    DB_NAME = os.getenv("DB_NAME") or "flask_ai"

    # # 数据库连接
    # SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}?charset=utf8mb4"

    # 读取数据库类型，没配置默认走SQLite（队友默认不用MySQL）
    DB_TYPE = os.getenv("DB_TYPE", "sqlite")

    if DB_TYPE == "mysql":
        # 你本地开发：沿用原来你的MySQL环境变量配置
        SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}?charset=utf8mb4"
    else:
        # 所有人默认SQLite，Python内置，无需安装任何数据库软件
        SQLALCHEMY_DATABASE_URI = "sqlite:///flask_project.db"

    # 注：如果想切回MySQL
    # 法一：.env文件内输入DB_TYPE=mysql（文件不是虚拟环境的文件夹）
    # 法二：终端输入set DB_TYPE=mysql（单次生效）

    # 数据迁移
    # # migrate.py 完整一键迁移代码
    # from app import app, db
    # # 这里导入你项目所有的数据模型表
    # from models import User, ChatRecord, KnowledgeFile, XXX  # 替换成你自己所有模型
    #
    # with app.app_context():
    #     # 1. 自动在MySQL里生成全部数据表
    #     db.create_all()
    #     # 2. 循环把SQLite所有数据批量导入MySQL
    #     all_models = [User, ChatRecord, KnowledgeFile]  # 你的所有模型按顺序填在这里
    #     for model in all_models:
    #         data_list = model.query.all()
    #         db.session.bulk_save_objects(data_list)
    #     db.session.commit()
    #
    # print("✅ SQLite 全部数据 成功迁移到MySQL！")

    # AI配置
    CHERRY_API_KEY = os.getenv("CHERRY_API_KEY")
    DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
    # 新增：DeepSeek V4 Pro 接口地址 + 满血版模型名
    DEEPSEEK_API_URL = "https://api.deepseek.com/v1/chat/completions"
    DEEPSEEK_MODEL_NAME = "deepseek-v4-pro"

    ZHIPU_API_KEY = os.getenv("ZHIPU_API_KEY")

    AI_TYPE = os.getenv("AI_TYPE", "deepseek")  # 默认改成deepseek
    QWEN_API_KEY = os.getenv("QWEN_API_KEY")
    QWEN_API_URL = "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation"

    # 知识库 向量库
    KNOWLEDGE_BASE_PATH = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "algorithm_knowledge"
    )
    VECTOR_DB_PATH = KNOWLEDGE_BASE_PATH

    # 创建目录
    @classmethod
    def init_dir(cls):
        if not os.path.exists(cls.KNOWLEDGE_BASE_PATH):
            os.makedirs(cls.KNOWLEDGE_BASE_PATH)


# 初始化目录
Config.init_dir()

