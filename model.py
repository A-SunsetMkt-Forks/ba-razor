from typing import Optional, List
from pydantic import BaseModel, validator

class Amendable:
    def amend(self, other: "Amendable"):
        raise NotImplementedError()

class AmendableOutput(Amendable):
    def amend(self, other: "AmendableOutput"):
        raise NotImplementedError()

class I18Message(BaseModel, Amendable):
    MessageKR: str = ""
    MessageJP: str = ""
    MessageCN: str = ""
    MessageEN: str = ""
    MessageTH: str = ""
    MessageTW: str = ""

    def amend(self, other: "I18Message"):
        self.MessageKR = other.MessageKR if other.MessageKR else self.MessageKR
        self.MessageJP = other.MessageJP if other.MessageJP else self.MessageJP
        self.MessageCN = other.MessageCN if other.MessageCN else self.MessageCN
        self.MessageEN = other.MessageEN if other.MessageEN else self.MessageEN
        self.MessageTH = other.MessageTH if other.MessageTH else self.MessageTH
        self.MessageTW = other.MessageTW if other.MessageTW else self.MessageTW

class I18Text(BaseModel, Amendable):
    TextJp: str = ""
    TextCn: str = ""
    TextKr: str = ""
    TextEn: str = ""
    TextTh: str = ""
    TextTw: str = ""

    def amend(self, other: "I18Text"):
        self.TextJp = other.TextJp if other.TextJp else self.TextJp
        self.TextCn = other.TextCn if other.TextCn else self.TextCn
        self.TextKr = other.TextKr if other.TextKr else self.TextKr
        self.TextEn = other.TextEn if other.TextEn else self.TextEn
        self.TextTh = other.TextTh if other.TextTh else self.TextTh
        self.TextTw = other.TextTw if other.TextTw else self.TextTw

class MomotalkContent(I18Message):
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

class ScenarioContent(I18Text):
    """剧情内容"""
    GroupId: int
    SelectionGroup: int
    BGMId: int
    Sound: str
    Transition: int
    BGName: int
    BGEffect: int
    PopupFileName: str
    ScriptKr: str
    VoiceJp: str

class FavorSchedule(I18Text):
    """学生好感剧情（回忆大厅选择）"""
    GroupId: int
    FavorScheduleId: int
    CharacterId: int

class MomotalkOutput(BaseModel, AmendableOutput):
    """以 CharacterId 为单位的 Momotalk 导出"""
    CharacterId: int
    translator: str = ""
    title: List[FavorSchedule] = []
    content: List[MomotalkContent] = []

    def amend(self, other: "MomotalkOutput"):
        assert self.CharacterId == other.CharacterId
        for self_title in self.title:
            for other_title in other.title:
                if self_title.GroupId == other_title.GroupId:
                    self_title.amend(other_title)
                    break
        for self_content in self.content:
            for other_content in other.content:
                if self_content.Id == other_content.Id:
                    self_content.amend(other_content)
                    break


class ScenarioOutput(BaseModel, AmendableOutput):
    """以 GroupId 为单位的剧情导出"""
    GroupId: int
    translator: str = ""
    content: List[ScenarioContent] = []

    def amend(self, other: "ScenarioOutput"):
        assert self.GroupId == other.GroupId
        for self_content in self.content:
            for other_content in other.content:
                if (
                    self_content.VoiceJp == other_content.VoiceJp 
                    and self_content.TextJp == other_content.TextJp 
                    and self_content.ScriptKr == other_content.ScriptKr
                ):
                    self_content.amend(other_content)
                    break

