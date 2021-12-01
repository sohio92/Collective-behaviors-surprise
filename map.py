from utils import *
from agents import Agent

class Map:
    """
    The map containing the agents
    """

    def __init__(self) -> None:
        self.agents = []
        self.agent_to_pos = {}
    
    def _init_agent_position(self, new_agent:Agent):
        """
        Initialize a new agent's position in the map, 
        Returns its position
        """

        raise NotImplementedError("Overriden by other topologies")

    def _move_agent(self, agent:Agent):
        """
        Moves an agent on the map
        Returns its position
        """

        raise NotImplementedError("Overriden by other topologies")
    
    def _detect_others(self, agent:Agent, pos_to_agent:dict):
        """
        Updates the agent's sensor based on the others' positions
        """

        raise NotImplementedError("Overriden by other topologies")

    def add_agent(self, new_agent:Agent):
        """
        Add an agent to the map
        """

        if new_agent not in self.agents:
            self.agents.append(new_agent)

            new_position = self._init_agent_position(new_agent)
            self.agent_to_pos[new_agent] = new_position

    def _step(self):
        """
        Run a step of the environment
        """

        # The agents take their decision
        for agent in self.agents:
            agent.take_decision()

        # The map updates the agents' position
        for agent in self.agents:
            new_position = self._move_agent(agent)
            self.agent_to_pos[agent] = new_position

        # Checking the agents' sensors
        pos_to_agent = reverse_dict_with_repeat(self.agent_to_pos)
        for agent in self.agents:
            self._detect_others(agent, pos_to_agent)

    def run(self, length:int):
        """
        Run the environment for a given length
        """
        for _ in range(length):
            self._step()