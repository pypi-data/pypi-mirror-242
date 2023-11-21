from pydantic import BaseModel

from switcore.ui.button import Button
from switcore.ui.image import Image


class ContextMenuItem(BaseModel):
    label: str
    action_id: str


class Header(BaseModel):
    title: str
    subtitle: str | None = None
    context_menu: list[ContextMenuItem] | None = None
    buttons: list[Button] | None = None


class AttachmentHeader(BaseModel):
    title: str
    subtitle: str | None = None
    app_id: str
    icon: Image | None = None
