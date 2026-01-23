

# create_mapping_fixed.py
import os
import json

MY_DATA_ROOT = './my_data'
MAPPING_FILE = './my_data/model_mapping.json'

mapping = {"model_mapping": {}}

for model_id in os.listdir(MY_DATA_ROOT):
    model_dir = os.path.join(MY_DATA_ROOT, model_id)
    if not os.path.isdir(model_dir):
        continue

    # 模型文件：使用 normalized_model.obj
    model_file = os.path.join(model_dir, 'normalized_model.obj').replace('\\', '/')

    # **关键修改：纹理文件使用实际的 texture.png 而不是 {model_id}.png**
    texture_file = os.path.join(model_dir, 'texture.png').replace('\\', '/')

    if os.path.exists(model_file):
        mapping['model_mapping'][model_id] = {
            'model_path': model_file,
            'texture_path': texture_file
        }
        print('✓ Added: {}'.format(model_id))
    else:
        print('✗ Model file missing, skip: {}'.format(model_id))

# 保存新映射文件
with open(MAPPING_FILE, 'w', encoding='utf-8') as f:
    json.dump(mapping, f, indent=2, ensure_ascii=False)

print('\nFixed mapping file generated: {}'.format(MAPPING_FILE))
print('Total models added: {}'.format(len(mapping['model_mapping'])))