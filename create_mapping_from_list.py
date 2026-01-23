# create_mapping_from_list.py
import os
import json

# ============ 【请根据你的实际情况修改以下三个变量】============
# 1. 你的模型列表文件路径
LIST_FILE = './my_data/my_model_list1.txt'
# 2. 你的模型数据根目录（存放所有模型文件夹的地方）
MY_DATA_ROOT = './my_data'
# 3. 要生成的映射文件路径
MAPPING_FILE = './my_data/model_mapping1.json'
# =======================================================

def create_mapping():
    """根据列表文件创建映射"""
    
    # 1. 读取模型列表
    if not os.path.exists(LIST_FILE):
        print(f"错误：列表文件不存在 - {LIST_FILE}")
        return
    
    with open(LIST_FILE, 'r', encoding='utf-8') as f:
        # 读取所有非空行，去掉首尾空格
        model_ids = [line.strip() for line in f if line.strip()]
    
    if not model_ids:
        print("列表文件中没有找到有效的模型ID。")
        return
    
    print(f"从列表文件中读取到 {len(model_ids)} 个模型ID。")
    
    # 2. 为每个ID创建映射条目
    mapping = {"model_mapping": {}}
    valid_count = 0
    
    for model_id in model_ids:
        model_dir = os.path.join(MY_DATA_ROOT, model_id)
        
        # 检查模型目录是否存在
        if not os.path.isdir(model_dir):
            print(f"警告：目录不存在，跳过 - {model_dir}")
            continue
        
        # 定义预期的文件路径（使用正斜杠保证跨平台兼容）
        # 假设模型文件名为 'normalized_model.obj'
        model_file = os.path.join(model_dir, 'normalized_model.obj').replace('\\', '/')
        # 假设纹理文件已重命名为 {model_id}.png
        texture_file = os.path.join(model_dir, 'texture.png').replace('\\', '/')
        
        # 检查必需文件是否存在
        model_exists = os.path.exists(model_file)
        texture_exists = os.path.exists(texture_file)
        
        if not model_exists:
            print(f"警告：模型文件不存在 - {model_file}")
            # 可以尝试寻找其他可能的模型文件名
            possible_files = [f for f in os.listdir(model_dir) if f.endswith('.obj')]
            if possible_files:
                print(f"  目录中存在以下OBJ文件: {possible_files}")
        
        if not texture_exists:
            print(f"警告：纹理文件不存在 - {texture_file}")
            # 可以尝试寻找其他可能的纹理文件名
            possible_textures = [f for f in os.listdir(model_dir) 
                               if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
            if possible_textures:
                print(f"  目录中存在以下纹理文件: {possible_textures}")
        
        # 如果两个文件都存在，则添加到映射
        if model_exists and texture_exists:
            mapping['model_mapping'][model_id] = {
                'model_path': model_file,
                'texture_path': texture_file
            }
            valid_count += 1
            print(f"✓ 已添加: {model_id}")
        else:
            print(f"✗ 文件不完整，跳过: {model_id}")
    
    # 3. 保存映射文件
    if valid_count > 0:
        # 确保输出目录存在
        os.makedirs(os.path.dirname(MAPPING_FILE), exist_ok=True)
        
        with open(MAPPING_FILE, 'w', encoding='utf-8') as f:
            json.dump(mapping, f, indent=2, ensure_ascii=False)
        
        print(f"\n成功！映射文件已生成: {MAPPING_FILE}")
        print(f"总计: {valid_count}/{len(model_ids)} 个模型被成功映射。")
        
        # 打印摘要
        print("\n映射摘要:")
        for mid in mapping['model_mapping'].keys():
            print(f"  - {mid}")
    else:
        print("\n错误：没有有效的模型可以映射。请检查文件路径和名称。")

if __name__ == '__main__':
    create_mapping()