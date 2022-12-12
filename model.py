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
    MessageKR: Optional[str] = ""
    MessageJP: Optional[str] = ""
    MessageCN: Optional[str] = ""
    MessageEN: Optional[str] = ""
    MessageTH: Optional[str] = ""
    MessageTW: Optional[str] = ""

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


class FavorScenario(BaseModel):
    """学生好感剧情"""
    GroupId: int
    FavorScheduleId: int
    CharacterId: int
    TextJp: Optional[str]
    TextCn: Optional[str]
    TextKr: Optional[str]
    TextEn: Optional[str]
    TextTh: Optional[str]
    TextTw: Optional[str]


# new
class FavorSchedule(BaseModel):
    """学生好感剧情(new)"""
    GroupId: int
    FavorScheduleId: int
    CharacterId: int
    TextJp: Optional[str]
    TextCn: Optional[str]
    TextKr: Optional[str]
    TextEn: Optional[str]
    TextTh: Optional[str]
    TextTw: Optional[str]


class MomotalkOutput(BaseModel):
    CharacterId: int
    translator: str
    title: List[FavorScenario] = []
    content: List[MomotalkContent] = []
