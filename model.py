from typing import Optional, List
from pydantic import BaseModel, validator


class MomotalkContent(BaseModel):
    """momotalk对话"""
    MessageGroupId: int
    Id: int
    CharacterId: int
    MessageCondition: str
    ConditionValue: int
    PreConditionGroupId: int
    PreConditionFavorScheduleId: int
    FavorScheduleId: int
    NextGroupId: int
    FeedbackTimeMillisec: int
    MessageType: str
    ImagePath: str
    MessageKR: str = ""
    MessageJP: str = ""
    MessageCN: str = ""
    MessageEN: str = ""
    MessageTH: str = ""
    MessageTW: str = ""

    @validator("MessageCondition")
    def validate_message_condition(cls, v):
        if not v in ['None', 'FavorRankUp', 'Answer', 'Feedback']:
            raise ValueError(f"{v} not in {['None', 'FavorRankUp', 'Answer', 'Feedback']}")
        return v

    @validator("MessageType")
    def validate_message_type(cls, v):
        if not v in ['Text', 'Image', 'None']:
            raise ValueError(f"{v} not in {['Text', 'Image', 'None']}")
        return v

class FavorScenarioContent(BaseModel):
    """好感剧情内容"""
    GroupId: int
    SelectionGroup: int
    BGMId: int
    Sound: str
    Transition: int
    BGName: int
    BGEffect: int
    PopupFileName: str
    ScriptKr: str
    TextJp: str = ""
    TextCn: str = ""
    TextKr: str = ""
    TextEn: str = ""
    TextTh: str = ""
    TextTw: str = ""
    VoiceJp: str

class FavorSchedule(BaseModel):
    """学生好感剧情（回忆大厅选择）"""
    GroupId: int
    FavorScheduleId: int
    CharacterId: int
    TextJp: str = ""
    TextCn: str = ""
    TextKr: str = ""
    TextEn: str = ""
    TextTh: str = ""
    TextTw: str = ""


class MomotalkOutput(BaseModel):
    """以 CharacterId 为单位的 Momotalk 导出"""
    CharacterId: int
    translator: str = ""
    title: List[FavorSchedule] = []
    content: List[MomotalkContent] = []

class FavorScenarioOutput(BaseModel):
    """以 GroupId 为单位的好感剧情导出"""
    GroupId: int
    translator: str = ""
    content: List[FavorScenarioContent] = []