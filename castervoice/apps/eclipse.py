from dragonfly import Key, Repeat, Dictation, Function, Choice, Paste, Pause

from castervoice.apps.eclipse_support import ec_con
from castervoice.lib.actions import Text
from castervoice.lib.ctrl.mgr.rule_details import RuleDetails
from castervoice.lib.merge.additions import IntegerRefST, Boolean
from castervoice.lib.merge.mergerule import MergeRule
from castervoice.lib.merge.state.short import R


class EclipseCCR(MergeRule):
    pronunciation = "eclipse jump"

    mapping = {
        #Line Ops
        "configure":
            R(Paste(ec_con.analysis_chars) +
                Key("left:2/5, c-f/20, backslash, rbracket, enter") +
                Function(ec_con.analyze_for_configure)),
        "jump in [<n>]":
            R(Key("c-f, a-o") + Paste(r"[\(\[\{\<]") + Function(ec_con.regex_on) +
                Key("enter:%(n)d/5, escape, right")),
        "jump out [<n>]":
            R(Key("c-f, a-o") + Paste(r"[\)\] \}\>]") + Function(ec_con.regex_on) +
                Key("enter:%(n)d/5, escape, right")),
        "jump back [<n>]":
            R(Key("c-f/5, a-b") + Paste(r"[\)\]\}\>]") + Function(ec_con.regex_on) +
                Key("enter:%(n)d/5, escape, left")),
        "[go to] line <n>":
            R(Key("c-l") + Pause("50") + Text("%(n)d") + Key("enter") + Pause("50")),
        "shackle <n> [<back>]":
            R(Key("c-l") + Key("right, cs-left") + Function(ec_con.lines_relative)),
    }
    extras = [
        Dictation("text"),
        IntegerRefST("n", 1, 1000),
        Boolean("back"),
    ]
    defaults = {"n": 1, "back": False}


def get_rule():
    return EclipseCCR, RuleDetails(executable="eclipse", title="Eclipse")
