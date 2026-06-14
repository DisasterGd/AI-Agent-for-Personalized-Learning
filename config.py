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

    # 读取数据库类型，没配置默认走SQLite
    DB_TYPE = os.getenv("DB_TYPE", "sqlite")

    if DB_TYPE == "mysql":
        # 从环境变量读取连接信息（注意：.env 中最后定义的 DB_HOST 等会覆盖前面的）
        DB_HOST = os.getenv("DB_HOST")
        DB_PORT = os.getenv("DB_PORT")
        DB_USER = os.getenv("DB_USER")
        DB_PASSWORD = os.getenv("DB_PASSWORD")
        DB_NAME = os.getenv("DB_NAME")

        # 构建基础 URI
        base_uri = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}?charset=utf8mb4"

        # TiDB 需要 SSL CA 证书（如果提供了证书路径则添加）
        tidb_ca_path = os.getenv("TIDB_CA_PATH")
        if tidb_ca_path and os.path.exists(tidb_ca_path):
            # 将反斜杠转换为正斜杠（避免转义问题）
            tidb_ca_path = tidb_ca_path.replace("\\", "/")
            SQLALCHEMY_DATABASE_URI = base_uri + f"&ssl_ca={tidb_ca_path}"
        else:
            # 本地 MySQL 或无需证书的情况
            SQLALCHEMY_DATABASE_URI = base_uri
    else:
        # 所有人默认SQLite，Python内置，无需安装任何数据库软件
        SQLALCHEMY_DATABASE_URI = "sqlite:///flask_project.db"

    # AI配置
    CHERRY_API_KEY = os.getenv("CHERRY_API_KEY")
    DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")

    # DeepSeek 配置（使用 OpenAI SDK 风格）
    DEEPSEEK_BASE_URL = "https://api.deepseek.com"           # SDK 的 base_url
    DEEPSEEK_MODEL_NAME = "deepseek-chat"                    # 有效模型：deepseek-chat 或 deepseek-reasoner

    # 兼容旧代码（如仍使用 requests 直接调用完整 URL 的情况，可保留；推荐使用上面的 DEEPSEEK_BASE_URL）
    DEEPSEEK_API_URL = f"{DEEPSEEK_BASE_URL}/v1/chat/completions"   # 完整接口地址

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
# import os
# from dotenv import load_dotenv
#
# # 加载项目根目录.env环境变量
# load_dotenv()
#
#
# class Config:
#     # 基础配置
#     SECRET_KEY = "software-cup-dev-secret-key"
#     SQLALCHEMY_TRACK_MODIFICATIONS = False
#
#     # 数据库配置
#     DB_HOST = os.getenv("DB_HOST") or "127.0.0.1"
#     DB_PORT = int(os.getenv("DB_PORT") or 3306)
#     DB_USER = os.getenv("DB_USER") or "root"
#     DB_PASSWORD = os.getenv("DB_PASSWORD") or "20100714"
#     DB_NAME = os.getenv("DB_NAME") or "flask_ai"
#
#     # # 数据库连接
#     # SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}?charset=utf8mb4"
#
#     # 读取数据库类型，没配置默认走SQLite
#     DB_TYPE = os.getenv("DB_TYPE", "sqlite")
#
#     if DB_TYPE == "mysql":
#         # 从环境变量读取连接信息（注意：.env 中最后定义的 DB_HOST 等会覆盖前面的）
#         DB_HOST = os.getenv("DB_HOST")
#         DB_PORT = os.getenv("DB_PORT")
#         DB_USER = os.getenv("DB_USER")
#         DB_PASSWORD = os.getenv("DB_PASSWORD")
#         DB_NAME = os.getenv("DB_NAME")
#
#         # 构建基础 URI
#         base_uri = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}?charset=utf8mb4"
#
#         # TiDB 需要 SSL CA 证书（如果提供了证书路径则添加）
#         tidb_ca_path = os.getenv("TIDB_CA_PATH")
#         if tidb_ca_path and os.path.exists(tidb_ca_path):
#             # 将反斜杠转换为正斜杠（避免转义问题）
#             tidb_ca_path = tidb_ca_path.replace("\\", "/")
#             SQLALCHEMY_DATABASE_URI = base_uri + f"&ssl_ca={tidb_ca_path}"
#         else:
#             # 本地 MySQL 或无需证书的情况
#             SQLALCHEMY_DATABASE_URI = base_uri
#     else:
#         # 所有人默认SQLite，Python内置，无需安装任何数据库软件
#         SQLALCHEMY_DATABASE_URI = "sqlite:///flask_project.db"
#
#     # 注：如果想切回MySQL
#     # 法一：.env文件内输入DB_TYPE=mysql（文件不是虚拟环境的文件夹）
#     # 法二：终端输入set DB_TYPE=mysql（单次生效）
#
#     # 数据迁移
#     # from app import app, db
#     # from models import User, ChatRecord, KnowledgeFile
#     #
#     # with app.app_context():
#     #     # 1. 自动在MySQL里生成全部数据表
#     #     db.create_all()
#     #     # 2. 循环把SQLite所有数据批量导入MySQL
#     #     all_models = [User, ChatRecord, KnowledgeFile]  # 你的所有模型按顺序填在这里
#     #     for model in all_models:
#     #         data_list = model.query.all()
#     #         db.session.bulk_save_objects(data_list)
#     #     db.session.commit()
#     #
#     # print("✅ SQLite 全部数据 成功迁移到MySQL！")
#
#     # AI配置
#     CHERRY_API_KEY = os.getenv("CHERRY_API_KEY")
#     DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
#     # 新增：DeepSeek V4 Pro 接口地址 + 满血版模型名
#     DEEPSEEK_API_URL = "https://api.deepseek.com/v1/chat/completions"
#     DEEPSEEK_MODEL_NAME = "deepseek-v4-pro"
#
#     ZHIPU_API_KEY = os.getenv("ZHIPU_API_KEY")
#
#     AI_TYPE = os.getenv("AI_TYPE", "deepseek")  # 默认改成deepseek
#     QWEN_API_KEY = os.getenv("QWEN_API_KEY")
#     QWEN_API_URL = "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation"
#
#     # 知识库 向量库
#     KNOWLEDGE_BASE_PATH = os.path.join(
#         os.path.dirname(os.path.abspath(__file__)),
#         "algorithm_knowledge"
#     )
#     VECTOR_DB_PATH = KNOWLEDGE_BASE_PATH
#
#     # 创建目录
#     @classmethod
#     def init_dir(cls):
#         if not os.path.exists(cls.KNOWLEDGE_BASE_PATH):
#             os.makedirs(cls.KNOWLEDGE_BASE_PATH)
#
#
# # 初始化目录
# Config.init_dir()

