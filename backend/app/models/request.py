from pydantic import BaseModel


class TextNode(BaseModel):
    content: str
    font_size: float | None = None
    font_weight: str | None = None
    fill_color: str | None = None  # hex color


class FrameLayer(BaseModel):
    id: str
    name: str
    type: str  # "TEXT", "FRAME", "RECTANGLE", etc.
    visible: bool = True
    children: list["FrameLayer"] = []
    text: TextNode | None = None
    fill_color: str | None = None
    background_color: str | None = None


class Frame(BaseModel):
    id: str
    name: str
    width: float
    height: float
    layers: list[FrameLayer]


class DesignDataRequest(BaseModel):
    frames: list[Frame]
    guidelines: str | None = None  # Optional override
