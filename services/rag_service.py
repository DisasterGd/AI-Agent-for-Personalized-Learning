from dotenv import load_dotenv
import os
import re

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_chroma import Chroma

load_dotenv()

# ==================== 配置区：Embedding 和 对话 API 完全分离 ====================
# -------------------- 向量模型（Embedding）- 硅基流动 --------------------
EMB_API_KEY = os.getenv("X")
EMB_BASE_URL = "https://api.siliconflow.cn/v1"
EMB_MODEL = "BAAI/bge-m3"

# -------------------- 对话模型（LLM）- DeepSeek 官方 --------------------
LLM_API_KEY = os.getenv("Y")
LLM_BASE_URL = "https://api.deepseek.com"
LLM_MODEL = "deepseek-chat"
LLM_TEMPERATURE = 0.35

# -------------------- 知识库与向量库配置 --------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROOT_FOLDER = os.path.join(BASE_DIR, "algorithm_knowledge")
VECTOR_STORE_PATH = os.path.join(BASE_DIR, "chroma_db")
CHUNK_SIZE = 600
CHUNK_OVERLAP = 100
# ==============================================================================

total_md_count = 0
IMG_CLEAN_PATTERN = re.compile(r"!\[.*?\]\(.*?\)")

def clean_md_text(text: str) -> str:
    return IMG_CLEAN_PATTERN.sub("", text).strip()

def split_md_content(text: str) -> list[str]:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=["---", "\n## ", "\n# ", "\n\n", "\n", "。", "，"]
    )
    chunks = splitter.split_text(text)
    chunks = [clean_md_text(c) for c in chunks]
    return [c for c in chunks if c]

# 向量模型客户端
embedding = OpenAIEmbeddings(
    api_key=EMB_API_KEY,
    base_url=EMB_BASE_URL,
    model=EMB_MODEL,
    timeout=120,
    max_retries=3
)

# 向量数据库
chroma_db = Chroma(
    persist_directory=VECTOR_STORE_PATH,
    embedding_function=embedding
)

# 对话模型客户端
llm = ChatOpenAI(
    api_key=LLM_API_KEY,
    base_url=LLM_BASE_URL,
    model=LLM_MODEL,
    temperature=LLM_TEMPERATURE,
    timeout=60,
    max_retries=2
)
# ==============================================================

def load_single_md(md_file: str):
    try:
        with open(md_file, "r", encoding="utf-8", errors="ignore") as f:
            raw_text = f.read()
    except Exception as e:
        print(f"读取失败 {md_file}：{e}")
        return

    chunks = split_md_content(raw_text)
    if not chunks:
        print(f"{md_file} 无有效内容，跳过")
        return

    file_name = os.path.basename(md_file)
    meta_list = [{"file_name": file_name, "file_path": md_file} for _ in chunks]
    chroma_db.add_texts(texts=chunks, metadatas=meta_list)
    print(f"✅ 入库：{file_name} | 切片 {len(chunks)}")

def traverse_folder(folder_path: str):
    global total_md_count
    if not os.path.isdir(folder_path):
        print(f"❌ 目录不存在：{folder_path}")
        return
    print(f"\n📂 遍历：{folder_path}")
    for item in os.listdir(folder_path):
        full_path = os.path.join(folder_path, item)
        if os.path.isdir(full_path):
            traverse_folder(full_path)
        elif os.path.isfile(full_path) and item.lower().endswith(".md"):
            load_single_md(full_path)
            total_md_count += 1

def search_content(query: str, top_k: int = 2):
    """向量检索（独立 Embedding）"""
    return chroma_db.similarity_search(query, k=top_k)

def rag_chat(question: str, top_k: int = 2):
    """RAG 问答（独立 LLM）"""
    related_docs = search_content(question, top_k)

    context = ""
    for doc in related_docs:
        context += f"【来源文件：{doc.metadata['file_name']}】\n{doc.page_content}\n\n"

    prompt = f"""
# Role Definition
你是“探路向导”，一位兼具哲学思辨气质的逻辑教练，同时具备文档与学习路径专业校验能力。

# State Machine 状态机机制（自动切换）
## Mode A: 探索模式（默认）
触发：概念疑问、询问原理、表达困惑、提交内容校验、学习路线审核
行为：采用苏格拉底式追问，引导用户自主构建知识网络；收到校验需求时，执行全方位内容核验。

## Mode B: 解决模式（触发激活）
触发：报错日志、标注具体行号、明确求助“帮我看看”
行为：以观察员视角定位问题，给出最小修复建议，处理完毕后自动切回 Mode A。

# 作答规则
1. 如果下方参考资料包含问题相关内容，**优先基于参考资料**回答；
2. 如果参考资料无相关内容，允许你依靠自身知识储备正常作答，不用提示暂无资料；
3. 回答尽量通俗易懂，专业术语补充通俗解释，数学公式统一使用 $$LaTeX$$ 格式。

# 边界感知与求助协议（仅在特殊场景启用）
## 情况1：Mode A 遭遇极冷门/未公开/时效性极强内容
判断标准：冷门定理、特定版本库未公开特性、2025年5月之后出现的新事件/新内容。
固定回复：
这是一个很好的切入点。关于【具体术语】，我的知识库中没有确切的推导细节。为了避免误导你建立错误的第一印象，我需要你提供更多的上下文：
1. 你是在哪本书/哪个网页/哪节课上看到这个词的？
2. 上下文里有没有提到它是为了解决什么问题而诞生的？
你可以直接把那段原文粘贴给我，我来帮你解构这段话的逻辑。

## 情况2：Mode B 遭遇无法复现的 Bug
判断标准：仅提供单行报错、无上下文代码、无环境版本、报错信息模糊。
固定回复：
仅凭这一行报错，我至少有多种不同方向的推测，但直接猜测会浪费你的调试时间。请补充以下任意一项信息，我就能精准锁定：
- 截图：报错发生前的操作记录；
- 代码片段：报错行的上下各5行代码；
- 环境指纹：python --version 或者 npm list [报错包名] 等版本结果。

# Constraints 通用约束
1. 知识诅咒防护：提到专业术语必须备注通俗解释；
2. 数学公式统一使用 $$LaTeX$$ 格式；
3. 诚实原则：当置信度 < 90% 或信息缺口 > 30% 时，回复中必须包含「我需要更多信息」章节，且该章节字数大于解读内容。

参考资料：
{context}

用户问题：{question}
"""
    response = llm.invoke(prompt)
    return response.content, related_docs

if __name__ == "__main__":
    # ========= 场景1：构建/更新知识库（首次/增删MD时打开） =========
    # total_md_count = 0
    # traverse_folder(ROOT_FOLDER)
    # print(f"\n=====================================")
    # print(f"📊 总计导入 MD：{total_md_count} 个")
    # print(f"=====================================")

    # ========= 场景2：日常问答 =========
    print("===== RAG 知识库问答 =====")
    user_question = input()
    answer, source_docs = rag_chat(user_question)

    print(f"\n【用户问题】{user_question}")
    print(f"\n【AI 回答】\n{answer}")

    print("\n【引用来源文档】")
    for idx, doc in enumerate(source_docs, 1):
        print(f"{idx}. 文件名：{doc.metadata['file_name']}  路径：{doc.metadata['file_path']}")