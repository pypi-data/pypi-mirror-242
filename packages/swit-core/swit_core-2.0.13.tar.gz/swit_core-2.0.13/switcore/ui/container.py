from pydantic import BaseModel

from switcore.ui.button import Button
from switcore.ui.select import Select
from switcore.ui.datepicker import DatePicker


class Container(BaseModel):
    type: str = "container"
    elements: list[Select | Button | DatePicker]

    class Config:
        smart_union = True
