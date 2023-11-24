from enum import Enum
from typing import Any

from lextok.rules._pattern import CM, OPT_NUMS, Label, Rule, _multi


class ReporterNum(Enum):
    scra = ["SCRA"]
    phil = ["Phil.", "Phil"]
    og = ["OG", "O.G.", "Off. Gaz."]


reporter_nums = Rule(
    label=Label.ReporterNum,
    patterns=[
        [{"LIKE_NUM": True}, {"ORTH": style}, {"LIKE_NUM": True}]
        for member in ReporterNum
        for style in member.value
    ],
)


stat = {
    "ENT_TYPE": {
        "IN": [
            Label.StatuteNamed.name,
            Label.StatuteNum.name,
            Label.DocketNum.name,
        ]
    }
}

opt_comma_plus = {"ORTH": {"IN": ["of", "the", ","]}, "OP": "*"}

linker = {"ORTH": {"IN": ["or", "and", ",", "&"]}, "OP": "+"}

multi_linked_statute_pattern = _multi([linker, stat], 10)  # type: ignore
for linked_list in multi_linked_statute_pattern:
    linked_list.insert(0, stat)
as_amended: list[dict[str, Any]] = [
    {"ORTH": ",", "IS_PUNCT": True, "OP": "?"},
    {"LOWER": "as", "OP": "?"},
    {"LOWER": "amended"},
    {"LOWER": "by", "OP": "?"},
]

linked_statutes = Rule(
    label=Label.StatutoryLink,
    patterns=multi_linked_statute_pattern + [[stat] + as_amended + [stat]],
)
"""Connect statutory numbers together: `RA 141, RA 4124, RA 5325`"""

statutory_provisions = Rule(
    label=Label.StatutoryProvision,
    patterns=[
        [{"ENT_TYPE": Label.ProvisionNum.name, "OP": "+"}, opt_comma_plus, stat],
        [{"ENT_TYPE": Label.ProvisionNum.name, "OP": "+"}, opt_comma_plus, stat],
        [stat, opt_comma_plus, {"ENT_TYPE": Label.ProvisionNum.name, "OP": "+"}],
    ],
)
"""Connect statutes with provisions: `Art. 2, Civil Code`"""

decision_citations = Rule(
    label=Label.DecisionCitation,
    patterns=[
        [
            Label.DocketNum.node,
            OPT_NUMS,
            Label.DATE.node,
            CM | {"OP": "?"},
            Label.ReporterNum.node,
        ],
        [
            Label.DocketNum.node,
            OPT_NUMS,
            Label.DATE.node,
        ],
        [
            Label.ReporterNum.node,
            OPT_NUMS,
            CM | {"OP": "?"},
            Label.DATE.node,
        ],
    ],
)
"""Connect decision names, docket citations, date, and/or reporter numbers: `X v. Y, GR No. 3425, Jan. 1, 2000, 14 SCRA 14`"""
