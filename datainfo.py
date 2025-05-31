from logicbase import (
Data, NumData, StrData, DictData
)

data_samples = [
    NumData("出勤次数", editable = False),
    NumData("通勤时间", editable = False),
    NumData("游玩时间", editable = False),
    DictData("交通方式", {"骑行": 0, "步行": 0, "公共交通": 0}),
    DictData("出装记录", {"大水": 0, "板子": 0, "手套": 0, "谷子": 0}, exclusive = False),
    StrData("上机必玩"),
    StrData("推分记录")
]

tips_samples = [
    "Stop in maimai",
    "奔跑的大国奏音.gif",
    "赏~你~吃~的~白~菜~怎~么~少~几~斤~嘞~",
    "提提提！大猩猩转圈.gif",
    "有一个人前来出勤",
    "...Who are you?",
    "XXXX是什么歌"
]