from collections.abc import Iterator
from enum import Enum
from typing import Any

from lextok.rules._pattern import (
    CONNECTOR,
    NUM_SYM,
    DigitLists,
    Label,
    Rule,
    _orth_in,
    _re,
)
from lextok.rules.abbreviations import Prov


class ProvisionNum(Enum):
    """A statute's text is divided into (sometimes hierarchical) provisions.
    This structure combines both the adjective division, e.g. `Sec.`, `Section`, `Bk.`, etc.
    (which may have different casing and abbreviations) with presumed valid serial numbers,
    e.g. `1`, `1-b`, `III`, etc.
    """

    abbreviated_Sec1 = list(Prov.set_abbvs())
    abbreviated_sec1 = list(Prov.set_abbvs(cased="lower"))
    abbreviated_SEC1 = list(Prov.set_abbvs(cased="upper"))
    Section1 = list(Prov.set_fulls())
    section1 = list(Prov.set_fulls(cased="lower"))
    SECTION1 = list(Prov.set_fulls(cased="upper"))

    @classmethod
    def generate(cls) -> Iterator[list[dict[str, Any]]]:
        specific_digits = _re("(" + "|".join(DigitLists.generate_options()) + ")")
        for member in cls:
            for end in [{"POS": "NUM"}, specific_digits]:
                start = [CONNECTOR]  # start
                if member.name.startswith("abbreviated_"):
                    yield start + [_orth_in(member.value), {"ORTH": "."}, end]
                    yield start + [_orth_in([f"{v}." for v in member.value]), end]
                yield start + [_orth_in(member.value), end]


special_clauses: list[dict[str, Any]] = [
    {"ENT_TYPE": "ORDINAL"},
    {"LOWER": {"IN": ["whereas"]}},
    {"LOWER": {"IN": ["clause", "clauses"]}},
]
provision_nums = Rule(
    label=Label.ProvisionNum, patterns=list(ProvisionNum.generate()) + [special_clauses]
)


generic_nums = Rule(
    label=Label.GenericNum,
    patterns=[[NUM_SYM, {"POS": "NUM"}]],
)
