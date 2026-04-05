"""Rule System: Horn clause rules for smart home automation."""

from typing import List, Tuple, Callable


class Rule:
    """Horn clause rule: (A ∧ B ∧ ...) → C with priority for conflict resolution."""
    
    def __init__(self, name: str, conditions: List[Tuple], conclusion: Tuple, priority: int = 0):
        self.name = name
        self.conditions = conditions
        self.conclusion = conclusion
        self.priority = priority
    
    def __repr__(self) -> str:
        cond_str = " ∧ ".join(str(c) for c in self.conditions)
        return f"Rule({self.name}: {cond_str} → {self.conclusion}, priority={self.priority})"
    
    def __str__(self) -> str:
        cond_str = " AND ".join(str(c) for c in self.conditions)
        return f"{self.name}: IF {cond_str} THEN {self.conclusion}"


def build_rule_set() -> List[Rule]:
    """Build 14 Horn clause rules for smart home (lighting, temp, ventilation).
    Priority: 10=safety, 5-8=comfort, 1-4=efficiency."""
    rules = []
    
    # Lighting rules
    rules.append(Rule(
        name="R1_Light_On_When_Present_And_Dark",
        conditions=[
            ("presence", "?room"),
            ("dark", "?room")
        ],
        conclusion=("turn_on_light", "?room"),
        priority=5
    ))
    
    rules.append(Rule(
        name="R2_Light_Off_When_No_Presence",
        conditions=[
            ("no_presence", "?room"),
            ("light_on", "?room")
        ],
        conclusion=("turn_off_light", "?room"),
        priority=5
    ))
    
    rules.append(Rule(
        name="R3_Light_On_At_Night_With_Presence",
        conditions=[
            ("night", "?room"),
            ("presence", "?room")
        ],
        conclusion=("turn_on_light", "?room"),
        priority=5
    ))
    
    # Temperature control rules
    rules.append(Rule(
        name="R4_AC_On_When_Temp_High",
        conditions=[
            ("temperature_high", "?room")
        ],
        conclusion=("turn_on_ac", "?room"),
        priority=5
    ))
    
    rules.append(Rule(
        name="R5_Heater_On_When_Temp_Low",
        conditions=[
            ("temperature_low", "?room")
        ],
        conclusion=("turn_on_heater", "?room"),
        priority=5
    ))
    
    rules.append(Rule(
        name="R6_Climate_Off_When_Temp_Moderate",
        conditions=[
            ("temperature_moderate", "?room")
        ],
        conclusion=("turn_off_climate", "?room"),
        priority=3
    ))
    
    # Ventilation rules
    rules.append(Rule(
        name="R7_Window_Open_When_Air_Bad",
        conditions=[
            ("air_bad", "?room")
        ],
        conclusion=("open_window", "?room"),
        priority=10  # Safety priority
    ))
    
    rules.append(Rule(
        name="R8_Fan_On_When_Air_Bad_And_Presence",
        conditions=[
            ("air_bad", "?room"),
            ("presence", "?room")
        ],
        conclusion=("turn_on_fan", "?room"),
        priority=8
    ))
    
    # Multi-condition rules
    rules.append(Rule(
        name="R9_AC_On_High_Temp_With_Presence",
        conditions=[
            ("temperature_high", "?room"),
            ("presence", "?room")
        ],
        conclusion=("turn_on_ac", "?room"),
        priority=7
    ))
    
    rules.append(Rule(
        name="R10_Light_Off_Night_No_Presence",
        conditions=[
            ("night", "?room"),
            ("no_presence", "?room"),
            ("light_on", "?room")
        ],
        conclusion=("turn_off_light", "?room"),
        priority=6
    ))
    
    rules.append(Rule(
        name="R11_Window_Close_Moderate_Good_Air",
        conditions=[
            ("temperature_moderate", "?room"),
            ("air_good", "?room"),
            ("window_open", "?room")
        ],
        conclusion=("close_window", "?room"),
        priority=2
    ))
    
    rules.append(Rule(
        name="R12_Heater_Off_When_Not_Cold",
        conditions=[
            ("temperature_moderate", "?room"),
            ("heater_on", "?room")
        ],
        conclusion=("turn_off_heater", "?room"),
        priority=4
    ))
    
    rules.append(Rule(
        name="R13_Fan_On_High_Temp_Window_Closed",
        conditions=[
            ("temperature_high", "?room"),
            ("window_closed", "?room")
        ],
        conclusion=("turn_on_fan", "?room"),
        priority=5
    ))
    
    rules.append(Rule(
        name="R14_Turn_Off_AC_No_Presence",
        conditions=[
            ("no_presence", "?room"),
            ("ac_on", "?room")
        ],
        conclusion=("turn_off_ac", "?room"),
        priority=3
    ))
    
    return rules
