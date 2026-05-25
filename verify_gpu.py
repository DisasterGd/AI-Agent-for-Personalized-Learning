import torch
print(f"CUDA 是否可用: {torch.cuda.is_available()}")
print(f"当前 GPU 设备: {torch.cuda.get_device_name(0)}")