#! python2.7
'''
main Caster module
Created on Jun 29, 2014
'''

import time
from dragonfly import (Key, Function, Grammar, Playback, Dictation, Choice, Pause, MappingRule)

def _wait_for_wsr_activation():
    count = 1
    while True:
        try: 
            from caster.apps import firefox
            break
        except: 
            print("(%d) Attempting to load Caster -- WSR not loaded and listening yet..." % count)
            count += 1
            time.sleep(1)

_NEXUS = None

try:
    from caster.lib import settings# requires nothing
    settings.WSR = __name__ == "__main__"
    from caster.lib import utilities# requires settings
    if settings.WSR:
        _wait_for_wsr_activation()
    from caster.lib import control
    from caster.lib.dfplus.state.stack import CasterState# requires control
    _NEXUS = control.nexus()
    _NEXUS.inform_state(CasterState(_NEXUS))
    
    from caster.apps import *
    from caster.asynch import *
    from caster.lib import context
    import caster.lib.dev.dev
    from caster.asynch.sikuli import sikuli
    from caster.lib import navigation, password
    navigation.initialize_clipboard(_NEXUS)
    from caster.lib.pita import scanner, trainer
    from caster.lib.dfplus.state.short import R
    from caster.lib.dfplus.additions import IntegerRefST
    
    from caster.lib.dfplus.merge.ccrmerger import Inf
    from caster.lib.ccr import *
    from caster.lib.ccr.recording.again import Again
    from caster.lib.ccr.recording.alias import VanillaAlias
    from caster.lib.ccr.recording import history
    from caster.lib.dev import dev
    from caster.lib.dfplus.hint.nodes import css
    from caster.user.filters.examples import scen4, modkeysup
    from caster import user
    
except:
    print("\nAttempting to load CCR anyway...")
    from caster.lib import utilities
    from caster.lib import control
    from caster.lib.dfplus.state.stack import CasterState# requires control
    _NEXUS = control.nexus()
    _NEXUS.inform_state(CasterState(_NEXUS))
    
    utilities.simple_log()

        


def change_monitor():
    if settings.SETTINGS["miscellaneous"]["sikuli_enabled"]:
        Playback([(["monitor", "select"], 0.0)]).execute()
    else:
        print("This command requires SikuliX to be enabled in the settings file")

class MainRule(MappingRule):
    
    @staticmethod
    def generate_ccr_choices(nexus):
        choices = {}
        for ccr_choice in nexus.merger.global_rule_names():
            choices[ccr_choice] = ccr_choice
        return Choice("name", choices)
    @staticmethod
    def generate_sm_ccr_choices(nexus):
        choices = {}
        for ccr_choice in nexus.merger.selfmod_rule_names():
            choices[ccr_choice] = ccr_choice
        return Choice("name2", choices)
    
    mapping = {
    # Dragon NaturallySpeaking commands moved to dragon.py
    
    # hardware management
    "volume <volume_mode> [<n>]":   R(Function(navigation.volume_control, extra={'n', 'volume_mode'}), rdescript="Volume Control"),
    "change monitor":               R(Key("w-p") + Pause("100") + Function(change_monitor), rdescript="Change Monitor"),
    
    # window management
    'minimize':                     Playback([(["minimize", "window"], 0.0)]),
    'maximize':                     Playback([(["maximize", "window"], 0.0)]),
    "remax":                        R(Key("a-space/10,r/10,a-space/10,x"), rdescript="Force Maximize"),
        
    # passwords
    'hash password <text> <text2> <text3>':                    R(Function(password.hash_password), rdescript="Get Hash Password"),
    'get password <text> <text2> <text3>':                     R(Function(password.get_password), rdescript="Get Seed Password"),
    'get restricted password <text> <text2> <text3>':          R(Function(password.get_restricted_password), rdescript="Get Char-Restricted Password"),
    'quick pass <text> <text2> <text3>':                       R(Function(password.get_simple_password), rdescript="Get Crappy Password"),
    
    # mouse alternatives
    "legion [<monitor>]":           R(Function(navigation.mouse_alternates, mode="legion", nexus=_NEXUS), rdescript="Activate Legion"),
    "rainbow [<monitor>]":          R(Function(navigation.mouse_alternates, mode="rainbow", nexus=_NEXUS), rdescript="Activate Rainbow Grid"),
    "douglas [<monitor>]":          R(Function(navigation.mouse_alternates, mode="douglas", nexus=_NEXUS), rdescript="Activate Douglas Grid"),
    
    # symbol match
    "scan directory":               R(Function(scanner.scan_directory), rdescript="Scan Directory For PITA"),
    "rescan current":               R(Function(scanner.rescan_current_file), rdescript="Rescan Current File For PITA"),
    "begin symbol training":        R(Function(trainer.trainer_box), rdescript="Train From Scanned Directory") , 
    
    # ccr de/activation
    "<enable> <name>":              R(Function(_NEXUS.merger.global_rule_changer(), save=True), rdescript="Toggle CCR Module"),
    "<enable> <name2>":             R(Function(_NEXUS.merger.node_rule_changer(), save=True), rdescript="Toggle sm-CCR Module"),
    
    
    }
    extras = [
              IntegerRefST("n", 1, 50),
              Dictation("text"),
              Dictation("text2"),
              Dictation("text3"),
              Choice("enable",
                    {"enable": True, "disable": False
                    }),
              Choice("volume_mode",
                    {"mute": "mute", "up":"up", "down":"down"
                     }),
              generate_ccr_choices.__func__(_NEXUS),
              generate_sm_ccr_choices.__func__(_NEXUS),
              IntegerRefST("monitor", 1, 10)
             ]
    defaults = {"n": 1, "nnv": 1,
               "text": "", "volume_mode": "setsysvolume",
               "enable":-1
               }


grammar = Grammar('general')
grammar.add_rule(MainRule())
grammar.add_rule(Again(_NEXUS))
grammar.add_rule(VanillaAlias(name="vanilla alias"))
grammar.load()

_NEXUS.merger.update_config()
_NEXUS.merger.merge(Inf.BOOT)

if settings.SETTINGS["miscellaneous"]["status_window_enabled"]:
    print("\nWARNING: Status Window is an experimental feature, and there is a known freezing glitch with it.\n")
    utilities.launch_status()

print("*- Starting " + settings.SOFTWARE_NAME + " -*")


if settings.WSR:
    import pythoncom
    print("Windows Speech Recognition is garbage; it is " \
        +"recommended that you not run Caster this way. ")
    while True:
        pythoncom.PumpWaitingMessages()  # @UndefinedVariable
        time.sleep(.1)