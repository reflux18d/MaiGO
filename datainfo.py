from logicbase import (
Data, NumData, StrData, DictData
)

data_samples = [
    DictData("交通方式", {"骑行": 0, "步行": 0, "公共交通": 0}),
    StrData("推分记录"),
    NumData("通勤时间", editable = False),
    NumData("游玩时间", editable = False)
]