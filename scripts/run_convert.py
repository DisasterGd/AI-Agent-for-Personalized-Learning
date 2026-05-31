import os
import subprocess

# 你的输入和输出路径（实际运行中可修改）
input_root = r"E:\Desktop\PDFOutput\文字版"
output_root = r"E:\Desktop\MarkdownOutput\文字版"

# 获取目录下所有的子文件夹
# sub_folders = [f for f in os.listdir(input_root) if os.path.isdir(os.path.join(input_root, f))]

# print(f"检测到 {len(sub_folders)} 个分类文件夹，准备开始批量转换...")
#
# for folder in sub_folders:
#     in_path = os.path.join(input_root, folder)
#     out_path = os.path.join(output_root, folder)

#     print(f"\n>>> 正在处理文件夹: {folder}")

# 自动创建输出目录
os.makedirs(output_root, exist_ok=True)

# 获取所有 PDF 文件
pdf_files = [f for f in os.listdir(input_root) if f.lower().endswith(".pdf")]

print(f"检测到 {len(pdf_files)} 个 PDF 文件，准备开始转换...")

for pdf_file in pdf_files:

    pdf_path = os.path.join(input_root, pdf_file)

    # 每个 PDF 建立单独输出文件夹
    file_name = os.path.splitext(pdf_file)[0]
    out_path = os.path.join(output_root, file_name)

    os.makedirs(out_path, exist_ok=True)

    print(f"\n>>> 正在处理: {pdf_file}")


    # 纯净版命令：去掉了报错的 --languages 参数
    command = [
        "marker_single",
        pdf_path,          # in_path,
        "--output_dir",
        out_path,
    ]

    try:
        # 运行转换命令
        subprocess.run(command, check=True)
        print(f"--- 文件夹 {pdf_file} 转换完成 ---")

    except Exception as e:
        print(f"!!! 文件夹 {pdf_file} 转换出错: {e}")

print("\n🎉 所有任务处理完毕！")