import json

# 读取原始文件
with open('all_arcades_code.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# 添加 index 字段
for i, arcade in enumerate(data):
    arcade['index'] = i

# 写入新的文件（或覆盖原文件）
with open('all_arcades_code_indexed.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)