from typing import List, Dict, Union
import random
import re
import numpy as np

from .base import Environment, TimeStep
from ..message import Message, MessagePool
from ..agent import SIGNAL_END_OF_CONVERSATION
from ..config import EnvironmentConfig

from ...chatarena.pgm import PGM_List
from ...utils.view_template import *
from ...utils.pgm_calculator import PGM

DEFAULT_TOPIC_CODES = {
    "Fruits": [
        "Apple",
        "Banana",
        "Orange",
        "Grape",
        "Strawberry",
        "Pineapple",
        "Mango",
        "Watermelon",
    ],
    "Animals": [
        "Lion",
        "Elephant",
        "Giraffe",
        "Monkey",
        "Zebra",
        "Tiger",
        "Bear",
        "Kangaroo",
    ],
    "Sports": [
        "Soccer",
        "Basketball",
        "Tennis",
        "Baseball",
        "Swimming",
        "Cycling",
        "Volleyball",
        "Golf",
    ],
    "Countries": [
        "United States",
        "Canada",
        "Brazil",
        "United Kingdom",
        "France",
        "Germany",
        "Japan",
        "Australia",
    ],
}


class Chameleon_PGM_Cal(Environment):
    type_name = "chameleon_pgm_cal"

    def __init__(self, player_names: List[str], topic_codes: Dict[str, List[str]] = None, **kwargs):
        super().__init__(player_names=player_names, topic_codes=topic_codes, **kwargs)

        if topic_codes is None:
            topic_codes = DEFAULT_TOPIC_CODES
        self.topic_codes = topic_codes

        # The "state" of the environment is maintained by the message pool
        self.message_pool = MessagePool()

        # Randomly sample a topic, code and chameleon player
        self.topic = None
        self.code = None
        self.chameleon_name = None
        self.non_chameleon_names = None

        # Game states
        self._current_turn = 0
        self._next_player_idx = 0
        self._current_phase = "give clues"  # "give clues", "accuse", "guess"
        self._players_votes = None
        self._initialized = False
        self._num_players = len(self.player_names)
        self._view_templ = templ_1
        self._clue_templ = clue_templ

        self.reset()  # To initialize the game (select topic, code, chameleon)

    def get_next_player(self) -> str:
        """
        get the next player
        """
        if self._current_phase != "guess":
            return self.player_names[self._next_player_idx]
        else:
            return self.chameleon_name

    def reset(self):
        """
        sample topic, code and chameleon code
        """
        self.topic = random.choice(list(self.topic_codes.keys()))
        self.code = random.choice(self.topic_codes[self.topic])
        self.chameleon_name = random.choice(self.player_names)
        self.chameleon_idx = self.player_names.index(self.chameleon_name)
        # self.topic = "Fruits"
        # self.code = "Banana"
        # self.chameleon_name = "Player 2"
        self.non_chameleon_names = [name for name in self.player_names if name != self.chameleon_name]



        self._current_turn = 0
        self._next_player_idx = 0
        # self._current_phase = "give clues"

        self.message_pool.reset()
        with open("results/human_pgm_1.txt") as f:
            self._human_pgm_demo = f.read()
        self._moderator_speak(f"")

        # self._moderator_speak(f"To help you better undertstand how to play the game, I will give you one example:\n{self._human_pgm_demo}")
 
        self._moderator_speak(f"Now the game starts! The topic is: {self.topic}")
        self._moderator_speak(f"You are not chameleon. The word is: {self.code}",
                              visible_to=self.non_chameleon_names)
        self._moderator_speak(f"You are the chameleon!", visible_to=self.chameleon_name)
        
        # self._moderator_speak("Next you give your clues one by one but never include the secret word in the clue.\n"
        #                       "Each time after a player giving a clue, every player needs to update their PGM by themselves one by one.\n"
        #                       "The criteria to update the PGM:\n"
        #                       "If you think one player is more suspicious to be an chameleon according to their clue, you need to increase his or her probability.\n"
        #                       "Your PGM is only visible to yourselves.")
        self._current_phase = "give clues" 
        self._moderator_speak(f"Now {self.player_names[0]}, we can start from you to give the clue. Never inclue secret word.")
        self._current_turn = 1

        self._players_votes = {name: 0 for name in self.player_names}
        self._player_pgm_dict = PGM_List(self.player_names, self.chameleon_name)
        self._finish_clue = False
        self._initialized = True
        self._pgm_list = []
        for pi in range(self._num_players):
            is_chameleon = (pi==self.chameleon_idx)
            self._pgm_list.append(PGM(is_chameleon, self._num_players, pi))

        init_timestep = TimeStep(observation=self.get_observation(),
                                 reward=self.get_zero_rewards(),
                                 terminal=False)

        return init_timestep

    def print(self):
        self.message_pool.print()

    def get_observation(self, player_name=None) -> List[Message]:
        """
        get observation for the player
        """
        if player_name is None:
            return self.message_pool.get_all_messages()
        else:
            return self.message_pool.get_visible_messages(player_name, turn=self._current_turn)
    # def get_pgm_conditions(self, player_name):
    #     pgm = self.PGM_List[player_name]
    #     self.clues[-1]

    def _text2change(self, text):
        """
        convert text to change on chameleon.
        """
        # print(text)
        lines = text.split("\n")
        factor = []
        changes = {"no change":0, "more suspicious":1, "less suspicious":-1}
        for line in lines:
            if line.startswith("Player"):
                for c in changes:
                    if line.find(c) >=0:
                        factor.append(changes[c]) 
        if len(factor) < self._num_players*self._num_players: # if the player didn't give evaluation from all perspectives
            for _ in range(len(factor), self._num_players*self._num_players):
                factor.append(0)

        factor = np.array(factor).reshape(self._num_players, self._num_players)
        
        return factor

    def _cal_vote(self):
        votes = [pgm._to_vote() for pgm in self._pgm_list]
        print("According to PGM:")
        for vi, v in enumerate(votes):
            print(f"{self.player_names[vi]} vote {self.player_names[v]}.")
        vote_dict = {}
        even_note = False
        for v in votes:
            if v not in vote_dict:
                vote_dict[v] = 0
            vote_dict[v] += 1
        max_vote_idx = max(vote_dict, key=vote_dict.get)
        for v, n in vote_dict.items():
            if v != max_vote_idx and n == vote_dict[max_vote_idx]:
                even_note = True
        accuse_correct  = False
        if max_vote_idx == self.chameleon_idx:
            accuse_correct = True
        return max_vote_idx, accuse_correct, even_note, vote_dict
 

    def _text2vote(self, text) -> str:
        """
        convert text to vote, return a player's name
        """
        # lower = text.lower().replace("[", "").replace("]", "").replace(".", "")
        text = text.lower()
        for name in self.player_names:
            candidates = [name.lower(), name.lower().replace(" ", ""), name.lower().replace(" ", "_")]
            if any([candidate in text for candidate in candidates]):
                return name
        return ""

    def _is_true_code(self, text) -> bool:
        """
        Check whether the text is the true code
        """
        # Get the word enclosed by quote marks with regex
        pattern = r"\"(.+?)\""
        match = re.search(pattern, text)
        if match:
            return match.group(1).lower().replace(" ", "") == self.code.lower().replace(" ", "")
        else:
            # if no quote marks, check whether the last k words match the code
            words = text.split()
            if len(words) >= len(self.code.split()):
                guessed_term = "".join(words[-len(self.code.split()):]).lower().replace(".", "")
                return guessed_term == self.code.lower().replace(" ", "").replace(".", "")
            else:
                return False

    def _moderator_speak(self, text: str, visible_to: Union[str, List[str]] = "all", is_show=True):
        """
        moderator say something
        """
        message = Message(agent_name="Moderator", content=text, turn=self._current_turn, visible_to=visible_to, is_show=is_show)
        self.message_pool.append_message(message)

    def get_rewards(self, chameleon_win: bool) -> Dict[str, float]:
        """
        get rewards for each player
        """
        rewards = {}
        for name in self.player_names:
            # The winner gets 1, the loser gets 0
            rewards[name] = float((name == self.chameleon_name) == chameleon_win)

        return rewards

    def is_terminal(self) -> bool:
        """
        check if the conversation is over
        """
        # If the last message is the signal, then the conversation is over
        if self.message_pool.last_message.content.startswith(SIGNAL_END_OF_CONVERSATION):
            return True

        

    def step(self, player_name: str, action: str) -> TimeStep:
        """
        step function that is called by the arena
        Args:
            player_name: the name of the player that takes the action
            action: the action that the agents wants to take
        """
        # If not initialized, reset the environment
        if not self._initialized:
            self.reset()

        # self.message_pool.print()
        # print(f"Chameleon: {self.chameleon_name}, Code: {self.code}, Topic: {self.topic}")
        assert player_name == self.get_next_player(), f"Wrong player! It is {self.get_next_player()} turn."
        if self._current_phase == "give clues":
            message = Message(agent_name=player_name, content=action, turn=self._current_turn)
            self.message_pool.append_message(message)
            # Update the counters
            
            if self._next_player_idx < len(self.player_names) - 1:
                self._next_clue_player_idx = self._next_player_idx + 1
            else:
                self._finish_clue = True
            self._current_phase = "pgm"
            self._next_player_idx = 0

            self._moderator_speak(self._view_templ.replace("<PLAYER>", self.player_names[self._next_player_idx])
                                  , visible_to=[self.player_names[self._next_player_idx]], is_show=False)  

            self._current_turn += 1

            timestep = TimeStep(observation=self.get_observation(),
                                reward=self.get_zero_rewards(),
                                terminal=False)  # Return all the messages

        elif self._current_phase == "accuse":
            
            message = Message(agent_name=player_name, content=action, turn=self._current_turn,
                              visible_to=[player_name])
            self.message_pool.append_message(message)
            vote = self._text2vote(action)
            if vote in self.player_names:
                self._players_votes[vote] += 1

            if self._next_player_idx < len(self.player_names) - 1:
                self._next_player_idx += 1
                rewards = self.get_zero_rewards()
                terminal = False
            else:
                # print(self._players_votes)
                accuse_correct, even_vote = True, False
                max_vote_player = max(self._players_votes, key=self._players_votes.get)
                # detach if other players has the same number of votes
                for name, vote in self._players_votes.items():
                    if name != max_vote_player and vote == self._players_votes[max_vote_player]:
                        accuse_correct, even_vote = False, True
                if max_vote_player != self.chameleon_name:
                    accuse_correct = False

                if not accuse_correct:
                    if even_vote:
                        self._moderator_speak(f"There are even votes. The accusation does not stand. "
                                              f"{self.chameleon_name} is the chameleon. {self.chameleon_name} won the game!")
                    else:
                        self._moderator_speak(
                            f"The most-voted player is {max_vote_player}. The accusation is incorrect. "
                            f"{self.chameleon_name} is the chameleon. {self.chameleon_name} won the game!"
                        )
                    rewards = self.get_rewards(chameleon_win=True)
                    terminal = True
                else:
                    self._moderator_speak(f"The accusation is correct! {self.chameleon_name} is the chameleon! "
                                          f"Now {self.chameleon_name} can guess the secret code. "
                                          "You should say: I guess the code is \"...\"")
                    self._current_phase = "guess"
                    rewards = self.get_zero_rewards()
                    terminal = False
                # show result of PGM 
                cal_max_vote, cal_accuse_correct, cal_even_note, _ = self._cal_vote()
                if not cal_accuse_correct:
                    if cal_even_note:
                        print(f"There are even notes. The chameleon {self.chameleon_name} wins.")
                    else:
                        print(f"The most-voted player is {self.player_names[cal_max_vote]}. The accusation is incorrect. "
                              f"{self.chameleon_name} is the chameleon. {self.chameleon_name} won the game!")
                else:
                    print(f"The accusation is correct! {self.chameleon_name} is the chameleon! "
                                          f"Now {self.chameleon_name} can guess the secret code. "
                                          "You should say: I guess the code is \"...\"")

                self._current_turn += 1

            timestep = TimeStep(observation=self.get_observation(), reward=rewards, terminal=terminal)
        elif self._current_phase == "guess":
            message = Message(agent_name=player_name, content=action, turn=self._current_turn,
                              visible_to=player_name)
            self.message_pool.append_message(message)
            if self._is_true_code(action):
                self._moderator_speak(f"{player_name} guessed the code correctly! The secret word is {self.code}. "
                                      f"{self.chameleon_name} won!")
                rewards = self.get_rewards(chameleon_win=True)
            else:
                self._moderator_speak(f"{player_name} guessed the code wrong! The secret word is {self.code}. "
                                      f"{self.non_chameleon_names} won!")
                rewards = self.get_rewards(chameleon_win=False)
            timestep = TimeStep(observation=self.get_observation(),
                                reward=rewards,
                                terminal=True)
    
        elif self._current_phase == "pgm":
            # generate PGM
            message = Message(agent_name=player_name, content=action, turn=self._current_turn,
                              visible_to=[player_name])
            self.message_pool.append_message(message)
            print("Before")
            self._pgm_list[self.player_names.index(player_name)].print()
            factor = self._text2change(action)
            self._pgm_list[self.player_names.index(player_name)].update(factor)
            print(player_name, factor)
            self._pgm_list[self.player_names.index(player_name)].print()

        
            if self._next_player_idx < len(self.player_names) - 1:
                self._next_player_idx += 1
                self._current_phase = "pgm" 
                self._moderator_speak(self._view_templ.replace("<PLAYER>", self.player_names[self._next_player_idx])
                                  , visible_to=[self.player_names[self._next_player_idx]], is_show=False)   

            else:
                self._next_player_idx = self._next_clue_player_idx
                if self._finish_clue:
                    self._current_phase = "accuse"
                    self._next_player_idx = 0
                    self._moderator_speak("Now vote which of the other players (excluding yourself) is the chameleon.  You should vote like: I vote Player xx as the chameleon."
                                         "You cannot vote for yourself.\n")
                else:
                    self._current_phase = "give clues"
                    target_player_idx = self._pgm_list[self._next_clue_player_idx].get_target()
                    self._moderator_speak(self._clue_templ.replace("<PLAYER>", self.player_names[target_player_idx]), visible_to=[self.player_names[self._next_clue_player_idx]])
                    self._moderator_speak(f"Now {self.player_names[self._next_clue_player_idx]}, please give your text clue. Never include the secret word.", visible_to=[self.player_names[self._next_clue_player_idx]])
            
            self._current_turn += 1
            timestep = TimeStep(observation=self.get_observation(),
                                reward=self.get_zero_rewards(),
                                terminal=False)  # Return all the messages
            
        else:
            raise ValueError(f"Unknown phase: {self._current_phase}")

        # Check if the player signals the end of the conversation
        if self.is_terminal():
            timestep.terminal = True

        return timestep
