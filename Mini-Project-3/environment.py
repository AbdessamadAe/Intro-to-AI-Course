"""Smart home environment simulator: tracks room states and applies actions."""

from typing import Dict, List, Tuple, Set
import random


class RoomState:
    """Room state: environmental conditions + device states."""
    
    def __init__(self, name: str):
        self.name = name
        
        self.presence = False
        self.light_level = "moderate"
        self.temperature = "moderate"
        self.air_quality = "good"
        self.time_of_day = "day"
        
        self.light_on = False
        self.ac_on = False
        self.heater_on = False
        self.fan_on = False
        self.window_open = False
    
    def __repr__(self) -> str:
        return (f"Room({self.name}: presence={self.presence}, "
                f"temp={self.temperature}, light={self.light_level})")


class SmartHomeEnvironment:
    """Multi-room smart home: generates facts, applies actions, simulates changes."""
    
    def __init__(self, room_names: List[str]):
        self.rooms: Dict[str, RoomState] = {}
        for name in room_names:
            self.rooms[name] = RoomState(name)
        
        self.time_step = 0
    
    def generate_facts(self) -> Set[Tuple]:
        """Generate facts from current environment state."""
        facts = set()
        
        for room_name, room in self.rooms.items():
            if room.presence:
                facts.add(("presence", room_name))
            else:
                facts.add(("no_presence", room_name))
            
            if room.light_level == "dark":
                facts.add(("dark", room_name))
            elif room.light_level == "bright":
                facts.add(("bright", room_name))
            
            if room.temperature == "high":
                facts.add(("temperature_high", room_name))
            elif room.temperature == "low":
                facts.add(("temperature_low", room_name))
            elif room.temperature == "moderate":
                facts.add(("temperature_moderate", room_name))
            
            if room.air_quality == "good":
                facts.add(("air_good", room_name))
            else:
                facts.add(("air_bad", room_name))
            
            if room.time_of_day == "night":
                facts.add(("night", room_name))
            else:
                facts.add(("day", room_name))
            
            if room.light_on:
                facts.add(("light_on", room_name))
            
            if room.ac_on:
                facts.add(("ac_on", room_name))
            
            if room.heater_on:
                facts.add(("heater_on", room_name))
            
            if room.fan_on:
                facts.add(("fan_on", room_name))
            
            if room.window_open:
                facts.add(("window_open", room_name))
            else:
                facts.add(("window_closed", room_name))
        
        return facts
    
    def apply_actions(self, facts: Set[Tuple]) -> List[str]:
        """Apply inferred actions to update device states. Returns list of changes."""
        actions_taken = []
        
        for fact in facts:
            if len(fact) != 2:
                continue
            
            action, room_name = fact
            
            if room_name not in self.rooms:
                continue
            
            room = self.rooms[room_name]
            
            if action == "turn_on_light" and not room.light_on:
                room.light_on = True
                actions_taken.append(f"Turned ON light in {room_name}")
            
            elif action == "turn_off_light" and room.light_on:
                room.light_on = False
                actions_taken.append(f"Turned OFF light in {room_name}")
            
            elif action == "turn_on_ac" and not room.ac_on:
                room.ac_on = True
                room.heater_on = False  # Mutually exclusive
                actions_taken.append(f"Turned ON AC in {room_name}")
            
            elif action == "turn_off_ac" and room.ac_on:
                room.ac_on = False
                actions_taken.append(f"Turned OFF AC in {room_name}")
            
            elif action == "turn_on_heater" and not room.heater_on:
                room.heater_on = True
                room.ac_on = False  # Mutually exclusive
                actions_taken.append(f"Turned ON heater in {room_name}")
            
            elif action == "turn_off_heater" and room.heater_on:
                room.heater_on = False
                actions_taken.append(f"Turned OFF heater in {room_name}")
            
            elif action == "turn_off_climate":
                if room.ac_on or room.heater_on:
                    room.ac_on = False
                    room.heater_on = False
                    actions_taken.append(f"Turned OFF climate control in {room_name}")
            
            elif action == "turn_on_fan" and not room.fan_on:
                room.fan_on = True
                actions_taken.append(f"Turned ON fan in {room_name}")
            
            elif action == "turn_off_fan" and room.fan_on:
                room.fan_on = False
                actions_taken.append(f"Turned OFF fan in {room_name}")
            
            elif action == "open_window" and not room.window_open:
                room.window_open = True
                actions_taken.append(f"Opened window in {room_name}")
            
            elif action == "close_window" and room.window_open:
                room.window_open = False
                actions_taken.append(f"Closed window in {room_name}")
        
        return actions_taken
    
    def update_environment(self):
        """Simulate environmental changes (random)."""
        self.time_step += 1
        
        for room in self.rooms.values():
            if random.random() < 0.3:
                room.presence = not room.presence
            
            if random.random() < 0.2:
                room.temperature = random.choice(["low", "moderate", "high"])
            
            if random.random() < 0.15:
                room.air_quality = random.choice(["good", "bad"])
            
            if random.random() < 0.25:
                room.light_level = random.choice(["dark", "moderate", "bright"])
            
            # Toggle day/night every 2 steps
            if self.time_step % 2 == 0:
                room.time_of_day = "night" if room.time_of_day == "day" else "day"
    
    def get_state_summary(self) -> str:
        """Return readable summary of environment state."""
        lines = [f"\n{'='*60}"]
        lines.append(f"ENVIRONMENT STATE - Time Step {self.time_step}")
        lines.append('='*60)
        
        for room_name, room in sorted(self.rooms.items()):
            lines.append(f"\n{room_name.upper()}:")
            lines.append(f"  Presence: {'YES' if room.presence else 'NO'}")
            lines.append(f"  Light Level: {room.light_level}")
            lines.append(f"  Temperature: {room.temperature}")
            lines.append(f"  Air Quality: {room.air_quality}")
            lines.append(f"  Time: {room.time_of_day}")
            
            devices = []
            if room.light_on:
                devices.append("light")
            if room.ac_on:
                devices.append("AC")
            if room.heater_on:
                devices.append("heater")
            if room.fan_on:
                devices.append("fan")
            if room.window_open:
                devices.append("window")
            
            lines.append(f"  Active Devices: {', '.join(devices) if devices else 'none'}")
        
        lines.append('='*60)
        return '\n'.join(lines)
