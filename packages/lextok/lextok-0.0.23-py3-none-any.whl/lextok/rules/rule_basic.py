from lextok.rules._pattern import CM, OF, Label, Rule, _orth_in, _re
from lextok.rules.abbreviations import abbv_months

date_as_entity = Rule(
    label=Label.DATE,
    patterns=[
        [
            CM | {"OP": "?"},
            {"LOWER": {"IN": ["s.", "series"]}},
            OF | {"OP": "?"},
            _re("\\d{4}"),
        ]
    ]
    + [
        [
            CM | {"OP": "?"},
            {"ORTH": month},
            _orth_in([f"{str(i)}" for i in range(1, 31)]),
            CM | {"OP": "?"},
            _re("\\d{4}"),
        ]
        for month_data in abbv_months
        for month in month_data.value.options
    ],
)
prefix_tits = _orth_in(["Atty.", "Hon.", "Engr.", "Dr.", "Dra."])
prefix_titled_person = Rule(
    label=Label.PERSON,
    patterns=[
        [prefix_tits, {"IS_TITLE": True, "OP": "+"}],
        [prefix_tits, {"ENT_TYPE": Label.PERSON.name}],
    ],
)
