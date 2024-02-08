from pysc2.agents import base_agent

from pysc2.env import sc2_env
from pysc2.lib import actions, features, units
from absl import app
import random


class StarAgent(base_agent.BaseAgent):
    def step(self, obs):
        super(StarAgent, self).step(obs)

        # Build Depot
        if build_depot(self, obs):
            x = random.randint(0, 83)
            y = random.randint(0, 83)
            return actions.FUNCTIONS.Build_SupplyDepot_screen('now', (x, y))

        # Build Barracks
        if build_barracks(self, obs):
            x = random.randint(0, 83)
            y = random.randint(0, 83)
            return actions.FUNCTIONS.Build_Barracks_screen('now', (x, y))

        # Train marine
        if train_marine(self, obs):
            return actions.FUNCTIONS.Train_Marine_quick('now')

        # Attack
        if attack(self, obs):
            return actions.FUNCTIONS.Attack_minimap(0, [19, 23])

        marines = [unit for unit in obs.observation['feature_units']
                    if unit.unit_type == units.Terran.Marine]
        if len(marines) > 5:
            marine = random.choice(marines)
            return actions.FUNCTIONS.select_point('select_all_type', (marine.x, marine.y))

        # select barracks
        barracks = [unit for unit in obs.observation['feature_units']
                    if unit.unit_type == units.Terran.Barracks]
        if len(barracks) > 0 :
            barrack = random.choice(barracks)
            return actions.FUNCTIONS.select_point('select_all_type', (barrack.x, barrack.y))

        # Select all SCV
        scvs = [unit for unit in obs.observation['feature_units']
                  if unit.unit_type == units.Terran.SCV]

        if len(scvs) > 0: # if SCV exists
            scv = random.choice(scvs) # select the unit randomly
            return actions.FUNCTIONS.select_point('select_all_type', (scv.x, scv.y))

        return actions.FUNCTIONS.no_op()

    def get_units_by_type(self, obs, unit_type):
        return [unit for unit in obs.observation.feature_units if units
                if unit.unit_type == unit_type]


    def unit_type_is_selected(self, obs, unit_type):
        if (len(obs.observation.single_select) > 0) and (obs.observation.single_select[0].unit_type == unit_type):
            return True

        if (len(obs.observation.multi_select) > 0 and (obs.observation.multi_select[0].unit_type == unit_type)):
            return True


# build Supply Depot
def build_depot(self, obs):
    depots = self.get_units_by_type(obs, units.Terran.SupplyDepot)
    if len(depots) == 0:
        if self.unit_type_is_selected(obs, units.Terran.SCV):
            if(actions.FUNCTIONS.Build_SupplyDepot_screen.id in obs.observation.available_actions):
                return True
            return False

# Build Barracks
def build_barracks(self, obs):
    barracks = self.get_units_by_type(obs, units.Terran.Barracks)
    if len(barracks) == 0:
        if self.unit_type_is_selected(obs, units.Terran.SCV):
            if(actions.FUNCTIONS.Build_Barracks_screen.id in obs.observation.available_actions):
                return True
            return False

# Train Marines
def train_marine(self, obs):
    marine = self.get_units_by_type(obs, units.Terran.Marine)
    if len(marine) <= 4:
        if self.unit_type_is_selected(obs, units.Terran.Barracks):
            if(actions.FUNCTIONS.Train_Marine_quick.id in obs.observation.available_actions):
                return True
        return False

# Attack
def attack(self, obs):
    marine = self.get_units_by_type(obs, units.Terran.Marine)
    if len(marine) > 5:
        if self.unit_type_is_selected(obs, units.Terran.Marine):
            if(actions.FUNCTIONS.Attack_screen.id in obs.observation.available_actions):
                return True
            return False