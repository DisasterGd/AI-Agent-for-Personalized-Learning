from services.rag_service import rag_chat

if __name__ == "__main__":
    answer, docs = rag_chat("Python 类是什么")
    print("=== 回答 ===")
    print(answer)
    print("\n=== 引用来源 ===")
    for doc in docs:
        print(doc.metadata.get('file_name', '未知'))