import os
import pymupdf  # PyMuPDF


def classify_pdfs(input_dir, text_dir, scan_dir, threshold=100):
    """
    threshold: 每一页平均字符数少于该值则判定为扫描件
    """
    if not os.path.exists(text_dir): os.makedirs(text_dir)
    if not os.path.exists(scan_dir): os.makedirs(scan_dir)

    for filename in os.listdir(input_dir):
        if not filename.lower().endswith(".pdf"):
            continue

        file_path = os.path.join(input_dir, filename)
        is_scan = True

        try:
            doc = pymupdf.open(file_path)
            text_content = ""
            # 检查前 3 页即可判定
            for page in doc[:3]:
                text_content += page.get_text()

            # 如果平均每页字符数超过阈值，视为纯文字版
            if len(text_content) / min(len(doc), 3) > threshold:
                is_scan = False
            doc.close()
        except Exception as e:
            print(f"处理文件 {filename} 时出错: {e}")
            continue

        # 移动文件
        target_dir = scan_dir if is_scan else text_dir
        os.rename(file_path, os.path.join(target_dir, filename))
        print(f"[{'扫描件' if is_scan else '文字版'}] -> {filename}")


if __name__ == "__main__":
    # 使用 r"" (Raw String) 前缀，原封不动地保留 Windows 的反斜杠和中文字符
    input_directory = r"E:\Desktop\计算机文档\9、组成原理&底层"     # 实际运行过程中可按需修改路径
    text_directory = r"E:\Desktop\PDFOutput\文字版"
    scan_directory = r"E:\Desktop\PDFOutput\扫描件"

    # 运行前加一个安全检查，防止找不到文件夹报错
    if not os.path.exists(input_directory):
        print(f"⚠️ 找不到文件夹: {input_directory}")
        print("请去资源管理器里确认一下这个文件夹是否真的存在，并且放了 PDF 进去！")
    else:
        print(f"🚀 开始扫描目录: {input_directory}")
        classify_pdfs(input_directory, text_directory, scan_directory)
        print("✅ 全部分类完成！")