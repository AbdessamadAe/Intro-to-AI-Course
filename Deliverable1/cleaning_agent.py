import random
from typing import List, Tuple


class Environment:
    
    def __init__(self, num_rooms: int):

        self.num_rooms = num_rooms
        # Room state: 0 = clean, 1-5 = dirty with dirtiness level
        self.rooms = [0] * num_rooms
        
    def set_room_dirtiness(self, room_index: int, dirtiness: int):
        if 0 <= room_index < self.num_rooms:
            self.rooms[room_index] = dirtiness
    
    def get_room_state(self, room_index: int) -> Tuple[bool, int]:
        """
        Get the state of a room.
        
        Returns:
            Tuple of (is_dirty, dirtiness_level)
        """
        dirtiness = self.rooms[room_index]
        return (dirtiness > 0, dirtiness)
    
    def clean_room(self, room_index: int):
        self.rooms[room_index] = 0
    
    def randomize_initial_state(self):
        for i in range(self.num_rooms):
            if random.random() < 0.5:  # 50% chance of being dirty initially
                self.rooms[i] = random.randint(1, 5)
    
    def update_environment(self):
        """
            clean rooms have 10% chance to become dirty.
        """
        for i in range(self.num_rooms):
            if self.rooms[i] == 0: 
                if random.random() < 0.1:  # 10% chance
                    self.rooms[i] = random.randint(1, 5)
    
    def is_all_clean(self) -> bool:
        return all(dirtiness == 0 for dirtiness in self.rooms)
    
    def get_state_summary(self) -> str:
        return str(self.rooms)


class Agent:
    
    # Action costs
    MOVE_COST = 2
    
    def __init__(self, num_rooms: int):

        self.position = 0  # Start at room 0
        self.initial_energy = 2.5 * num_rooms
        self.energy = self.initial_energy
        self.num_rooms = num_rooms
        self.actions_taken = []
        self.rooms_cleaned_count = 0
        
    def perceive(self, environment: Environment) -> dict:
        is_dirty, dirtiness_level = environment.get_room_state(self.position)
        return {
            'room_index': self.position,
            'is_dirty': is_dirty,
            'dirtiness_level': dirtiness_level,
            'remaining_energy': self.energy
        }
    
    def can_suck(self, dirtiness_level: int) -> bool:
        return self.energy >= dirtiness_level
    
    def can_move(self) -> bool:
        return self.energy >= self.MOVE_COST
    
    def suck(self, environment: Environment, dirtiness_level: int):
        if self.can_suck(dirtiness_level):
            environment.clean_room(self.position)
            self.energy -= dirtiness_level
            self.actions_taken.append(f"Suck(room={self.position}, cost={dirtiness_level})")
            self.rooms_cleaned_count += 1
    
    def move_left(self):
        if self.position > 0 and self.can_move():
            self.position -= 1
            self.energy -= self.MOVE_COST
            self.actions_taken.append(f"MoveLeft(to room={self.position})")
    
    def move_right(self):
        if self.position < self.num_rooms - 1 and self.can_move():
            self.position += 1
            self.energy -= self.MOVE_COST
            self.actions_taken.append(f"MoveRight(to room={self.position})")
    
    def decide_action(self, percept: dict, environment: Environment) -> bool:
        """
        Decide and execute the next action based on basic behavior.
        
        Basic behavior:
        - If current room is dirty and energy allows → Suck
        - Else, move right (or left at boundary) if enough energy
        
        Returns:
            True if an action was taken, False otherwise
        """
        if percept['is_dirty'] and self.can_suck(percept['dirtiness_level']):
            self.suck(environment, percept['dirtiness_level'])
            return True
        
        if self.can_move():
            if self.position >= self.num_rooms - 1:
                self.move_left()
                return True
            else:
                self.move_right()
                return True
        
        # No action possible
        return False
    
    def get_energy_consumed(self) -> float:
        return self.initial_energy - self.energy


def run_simulation(num_rooms: int, max_timesteps: int, randomize_initial: bool = True) -> dict:

    environment = Environment(num_rooms)
    if randomize_initial:
        environment.randomize_initial_state()
    agent = Agent(num_rooms)
    
    print(f"=== Cleaning Agent Simulation ===")
    print(f"Number of rooms: {num_rooms}")
    print(f"Initial energy: {agent.initial_energy}")
    print(f"Max timesteps: {max_timesteps}")
    print(f"Initial room states: {environment.get_state_summary()}\n")
    
    timestep = 0
    while timestep < max_timesteps:
        timestep += 1
        
        percept = agent.perceive(environment)
        action_taken = agent.decide_action(percept, environment)
                
        if environment.is_all_clean() and not percept['is_dirty']:
            print(f"\n[Timestep {timestep}] All rooms are clean. Simulation complete.")
            break
        
        if not action_taken and agent.energy < min(1, agent.MOVE_COST):
            print(f"\n[Timestep {timestep}] Agent out of usable energy. Simulation complete.")
            break
        
        environment.update_environment()
    
    if timestep >= max_timesteps:
        print(f"\n[Timestep {timestep}] Maximum timesteps reached.")
    
    results = {
        'final_room_states': environment.rooms.copy(),
        'rooms_cleaned': agent.rooms_cleaned_count,
        'energy_consumed': agent.get_energy_consumed(),
        'energy_remaining': agent.energy,
        'actions_sequence': agent.actions_taken.copy(),
        'timesteps_elapsed': timestep,
        'all_clean': environment.is_all_clean()
    }
    
    return results


def print_results(results: dict):
    """Print simulation results in a formatted manner."""
    print("\n=== Simulation Results ===")
    print(f"Final room states: {results['final_room_states']}")
    print(f"Number of rooms cleaned: {results['rooms_cleaned']}")
    print(f"Total energy consumed: {results['energy_consumed']:.2f}")
    print(f"Final remaining energy: {results['energy_remaining']:.2f}")
    print(f"Timesteps elapsed: {results['timesteps_elapsed']}")
    print(f"All rooms clean: {results['all_clean']}")
    print(f"\nSequence of actions ({len(results['actions_sequence'])} total):")
    for i, action in enumerate(results['actions_sequence'], 1):
        print(f"  {i}. {action}")


if __name__ == "__main__":
    
    N = 10
    T = 100
    
    results = run_simulation(
        num_rooms=N,
        max_timesteps=T,
        randomize_initial=True,
    )
    
    print_results(results)
