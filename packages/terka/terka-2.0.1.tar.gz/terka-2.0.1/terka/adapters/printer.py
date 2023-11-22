import abc
from dataclasses import dataclass


@dataclass
class PrintOptions:
    show_tasks: bool = True
    show_history: bool = False
    show_commentaries: bool = False
    show_completed: bool = False
    show_epics: bool = True
    show_stories: bool = True
    show_notes: bool = True
    show_viz: bool = False
    columns: str = ""
    expand_table: bool = True

    @classmethod
    def from_kwargs(cls, **kwargs: dict) -> "PrintOptions":
        return cls(**{k: kwargs[k] for k in kwargs if k in cls.__match_args__})



class BasePrinter(abc.ABC):
    ...
