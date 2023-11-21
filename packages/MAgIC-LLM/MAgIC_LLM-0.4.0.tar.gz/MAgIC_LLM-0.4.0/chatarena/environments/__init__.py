from .base import Environment, TimeStep
from .conversation import Conversation, ModeratedConversation
from .chameleon_competition import Chameleon_Competition
from .chameleon_competition_pgm import Chameleon_Competition_PGM

from .chameleon import Chameleon
from .chameleon_inter import Chameleon_Inter
from .chameleon_iter import Chameleon_Iter
from .chameleon_pgm_cal import Chameleon_PGM_Cal
from .chameleon_pgm_cal_active import Chameleon_PGM_Cal_Active
from .chameleon_pgm_cal_active_fewshot import Chameleon_PGM_Cal_Active_Fewshot
from .chameleon_pgm import Chameleon_PGM
from .pettingzoo_chess import PettingzooChess
from .pettingzoo_tictactoe import PettingzooTicTacToe
from .undercover_competition import Undercover_Competition
from .undercover_competition_pgm import Undercover_Competition_PGM
from .chameleon_competition_wmetric import Chameleon_Competition_WMetric
from .undercover_competition_wmetric import Undercover_Competition_WMetric

from .airportfee import Airport_Fee_Allocation
from .airportfee_pgm import Airport_Fee_Allocation_PGM

from .prisoner import Prinsoner_Dilemma
from .prisoner_pgm import Prinsoner_Dilemma_PGM

from .public_good import Public_Good
from .public_good_pgm import Public_Good_PGM


from ..config import EnvironmentConfig

ALL_ENVIRONMENTS = [
    Conversation,
    ModeratedConversation,
    Chameleon,
    Chameleon_Inter,
    Chameleon_Iter,
    Chameleon_PGM_Cal,
    Chameleon_PGM,
    PettingzooChess,
    PettingzooTicTacToe,
    Chameleon_PGM_Cal_Active,
    Chameleon_PGM_Cal_Active_Fewshot,
    Chameleon_Competition,
    Chameleon_Competition_PGM,
    Undercover_Competition,
    Undercover_Competition_PGM,
    Airport_Fee_Allocation,
    Airport_Fee_Allocation_PGM,
    Prinsoner_Dilemma,
    Prinsoner_Dilemma_PGM,
    Public_Good,
    Public_Good_PGM,
    Chameleon_Competition_WMetric,
    Undercover_Competition_WMetric
]

ENV_REGISTRY = {env.type_name: env for env in ALL_ENVIRONMENTS}

print(ENV_REGISTRY)
# Load an environment from a config dictionary
def load_environment(config: EnvironmentConfig):
    try:
        env_cls = ENV_REGISTRY[config["env_type"]]
    except KeyError:
        raise ValueError(f"Unknown environment type: {config['env_type']}")
    print(config)
    env = env_cls.from_config(config)
    return env
