from logicbase import (
Data, NumData, StrData, DictData
)

data_samples = [
    NumData("出勤次数", editable = False),
    NumData("通勤时间", editable = False),
    NumData("游玩时间", editable = False),
    DictData("交通方式", {"骑行": 0, "步行": 0, "公共交通": 0}),
    DictData("出装记录", {"大水": 0, "板子": 0, "手套": 0, "谷子": 0}, exclusive = False),
    StrData("推分记录")
]