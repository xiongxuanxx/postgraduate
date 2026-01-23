# create_mapping.py
import os
import json

# 1. 配置你的数据根目录
MY_DATA_ROOT = './my_data'
# 2. 配置映射文件的输出路径
MAPPING_FILE = './my_data/model_mapping.json'

mapping = {"model_mapping": {}}

# 3. 遍历数据目录
for model_id in os.listdir(MY_DATA_ROOT):
    model_dir = os.path.join(MY_DATA_ROOT, model_id)
    if not os.path.isdir(model_dir):
        continue

    # 定义预期的文件路径
    # 模型文件：假设使用 normalized_model.obj
    model_file = os.path.join(model_dir, 'normalized_model.obj').replace('\\', '/')
    # 纹理文件：假设你已经将 texture.png 重命名为 {model_id}.png
    texture_file = os.path.join(model_dir, 'texture.png').replace('\\', '/')

    # 检查文件是否存在
    if os.path.exists(model_file) and os.path.exists(texture_file):
        mapping['model_mapping'][model_id] = {
            'model_path': model_file,
            'texture_path': texture_file
        }
        print(f'✓ 已添加: {model_id}')
    else:
        print(f'✗ 文件缺失，跳过: {model_id}')
        print(f'  模型文件存在: {os.path.exists(model_file)} - {model_file}')
        print(f'  纹理文件存在: {os.path.exists(texture_file)} - {texture_file}')

# 4. 保存为JSON文件
with open(MAPPING_FILE, 'w', encoding='utf-8') as f:
    json.dump(mapping, f, indent=2, ensure_ascii=False)

print(f'\n映射文件已生成: {MAPPING_FILE}')
print(f'共添加了 {len(mapping["model_mapping"])} 个有效模型。')