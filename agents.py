import random
import torch

from copy import deepcopy
from utils import *
from neural_network import ActionNetwork, PredictionNetwork


class Agent:
    """
    A single agent able to move in a map, unaware of its current state
    """

    id = 0

    def __init__(self, action_network:ActionNetwork, prediction_network:PredictionNetwork, sensor_range_0:float, sensor_range_1:float, speed:float, noise) -> None:
        self.id = Agent.id
        Agent.id += 1

        self.sensor_range_0 = sensor_range_0
        self.sensor_0 = [False, False]
        self.sensor_0_prediction = [None, None]
        self.sensor_0_activation_count = [0, 0] # Used for entropy calculation

        self.sensor_range_1 = sensor_range_1
        self.sensor_1 = [False, False]
        self.sensor_1_prediction = [None, None]
        self.sensor_1_activation_count = [0, 0] # Used for entropy calculation

        self.speed = speed
        self.noise = noise

        self.direction = random.choice([-1, 1])
        self.position = None

        self.action_network = deepcopy(action_network)
        self.prediction_network = deepcopy(prediction_network)

        self.score = 0 # The sum of correct predictions over the existence of the agent
        self.position_history = [] # The history of the agent's positions
    
    def reset(self) -> None:
        """
        Reset the agent
        """

        self.reset_sensors()
        self.direction = random.choice([-1, 1])

        self.score = 0
        self.distance_traveled = 0
        self.position_history = []

        self.sensor_0_activation_count = [0, 0]
        self.sensor_1_activation_count = [0, 0]        

    def reset_sensors(self) -> None:
        """
        Reset the agent's sensors
        """

        self.sensor_0 = [False, False]
        self.sensor_1 = [False, False]   

    def compute_score(self) -> None:
        """
        Adds the number of correct predictions to the agent's score
        """

        score_0 = sum([self.sensor_0[i] == self.sensor_0_prediction[i] for i in range(2)])
        score_1 = sum([self.sensor_1[i] == self.sensor_1_prediction[i] for i in range(2)])

        self.score += score_0 + score_1

    def take_decision(self) -> None:
        """
        Changes the agent's direction based on its action network
        """

        nn_input = torch.Tensor([self.direction > 0, *self.sensor_0, *self.sensor_1])
        nn_output = self.action_network.forward(nn_input)

        self.direction = int(torch.round(2 * nn_output - 1))
    
    def predict_sensors(self) -> None:
        """
        Predicts the state of the sensors with the prediction network
        """

        nn_input = torch.Tensor([self.direction > 0, *self.sensor_0, *self.sensor_1])[None, None, :]
        nn_output = torch.squeeze(self.prediction_network.forward(nn_input))
        
        self.sensor_0_prediction = [bool(pred) for pred in torch.round(nn_output)[:2]]
        self.sensor_1_prediction = [bool(pred) for pred in torch.round(nn_output)[2:]]
        
    def __str__(self):
        return "Agent {}:\tposition: {}\tdirection: {}\tsensors 0: {}\tsensors 1: {}".format(self.id, self.position, self.direction, self.sensor_0, self.sensor_1)