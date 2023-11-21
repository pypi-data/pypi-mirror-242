from dataclasses import dataclass
from enum import IntEnum
import os
import re
import sqlite3
from typing import Final, List, Optional, Union
import warnings

try:
    from typing import Dict
except:
    Dict = dict
from platformdirs import user_data_dir
import requests


def ensure_dir(path: str) -> None:
    os.makedirs(path, exist_ok=True)


MODULE_NAME: Final[str] = "libchecker"
MODULE_AUTHOR: Final[str] = "Young-Lord"
DATA_DIR: Final[str] = user_data_dir(MODULE_NAME, MODULE_AUTHOR)
RULE_URL: Final[
    str
] = "https://github.com/LibChecker/LibChecker-Rules/raw/master/cloud/rules/v3/rules.db"
RULE_FILENAME: Final[str] = "rules.db"
RULE_FILE: Final[str] = os.path.join(DATA_DIR, RULE_FILENAME)
ensure_dir(DATA_DIR)


def update(no_init_rules: bool = False) -> None:
    r = requests.get(RULE_URL)
    with open(os.path.join(DATA_DIR, RULE_FILENAME), "wb") as f:
        f.write(r.content)
    if not no_init_rules:
        init_rules()


if not os.path.isfile(RULE_FILE):
    warnings.warn("Rules for LibChecker not found, downloading...")
    update(no_init_rules=True)


class RuleType(IntEnum):
    SO = 0
    SERVICE = 1
    ACTIVITY = 2
    RECEIVER = 3
    PROVIDER = 4
    CLASS = 5  # androidx.recyclerview unknown
    PACKAGE_NAME = 6  # com.google.android.trichromelibrary only


@dataclass
class Rule:
    _id: int
    name: str
    label: str
    type: RuleType
    iconIndex: int
    isRegexRule: int
    regexName: Optional[str]

    def __init__(
        self,
        _id: int,
        name: str,
        label: str,
        type: Union[RuleType, int],
        iconIndex: int,
        isRegexRule: int,
        regexName: Optional[str],
    ) -> None:
        self._id = _id
        self.name = name
        self.label = label
        self.type = RuleType(type)
        self.iconIndex = iconIndex
        self.isRegexRule = isRegexRule
        self.regexName = regexName


conn = sqlite3.connect(RULE_FILE, check_same_thread=False)
cur = conn.cursor()
rules: Dict[str, List[Rule]] = {}
regex_rules: List[Rule] = []


def init_rules():
    global rules, regex_rules
    rules = {}
    regex_rules = []
    cur.execute(
        "SELECT _id, name, label, type, iconIndex, isRegexRule, regexName FROM rules_table"
    )
    for row in cur.fetchall():
        rule = Rule(*row)
        if rule.isRegexRule:
            regex_rules.append(rule)
        else:
            rules.setdefault(rule.name, []).append(rule)


init_rules()


def query(name: str) -> List[Rule]:
    response: List[Rule] = []
    for regex_rule in regex_rules:
        if re.match(regex_rule.name, name):
            response.append(regex_rule)
    response.extend(rules.get(name, []))
    return response
