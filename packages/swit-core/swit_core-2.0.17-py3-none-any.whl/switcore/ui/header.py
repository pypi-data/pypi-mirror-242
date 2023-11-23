from switcore.pydantic_base_model import SwitBaseModel
from switcore.ui.button import Button
from switcore.ui.image import Image


class ContextMenuItem(SwitBaseModel):
    label: str
    action_id: str


class Header(SwitBaseModel):
    title: str
    subtitle: str | None = None
    context_menu: list[ContextMenuItem] | None = None
    buttons: list[Button] | None = None


class AttachmentHeader(SwitBaseModel):
    title: str
    subtitle: str | None = None
    app_id: str
    icon: Image | None = None
