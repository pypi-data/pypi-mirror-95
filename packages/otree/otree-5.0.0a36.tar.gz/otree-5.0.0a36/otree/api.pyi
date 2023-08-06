from typing import Union, List, Any, Optional, TypeVar
# this will show up as an error here, but it's OK since it's just a .pyi file.
# this file may be defined in the user's project, if they want better type hints.
import shared_out
from otree.currency import RealWorldCurrency, Currency


class Currency(Currency):
    '''
    PyCharm autocomplete seems to require that I explicitly define the class in this file
    (if I import, it says the reference to Currency is not found)
    '''

c = cu = Currency

def currency_range(first, last, increment) -> List[Currency]:
    pass


# mocking the public API for PyCharm autocomplete.
# one downside is that PyCharm doesn't seem to fully autocomplete arguments
# in the .pyi. It gives the yellow pop-up, but doesn't complete what you
# are typing. (2017-07-01: seems to work in PyCharm 2017.1.4?)
class models:

    '''
    The code in this class has nothing to do with implementation,
    but rather defines the interface for model fields,
    so that pyCharm autocompletes them properly.

    It defines their __init__ so that when instantiating the class,
    PyCharm suggests the right arguments.
    Apart from that, they can be used as the equivalent Python data type
    (e.g. BooleanField is a bool, CharField is str)

    Without inheriting from bool, str, etc., PyCharm flags certain usages in yellow,
    like:

        c(1) + c(1)

    Results in: "Currency does not define __add__, so the + operator cannot
    be used on its instances"

    If "a" is a CurrencyField, then
        self.a + c(1)

    PyCharm warns: 'Currency does not define __add__, so the + operator cannot
    be used on its instances'

        c(1) + 1

    'Expected type "int", got "Currency" instead'

        self.a + 1

    'Expected type "int", got "CurrencyField" instead'


    '''

    def __getattr__(self, item):
        pass
    class BooleanField(bool):
        def __init__(
            self,
            *,
            choices=None,
            widget=None,
            initial=None,
            label=None,
            doc='',
            blank=False,
            **kwargs
        ):
            pass
    class StringField(str):
        def __init__(
            self,
            *,
            choices=None,
            widget=None,
            initial=None,
            label=None,
            doc='',
            max_length=10000,
            blank=False,
            **kwargs
        ):
            pass
    class LongStringField(str):
        def __init__(
            self,
            *,
            initial=None,
            label=None,
            doc='',
            max_length=None,
            blank=False,
            **kwargs
        ):
            pass
    # need to copy-paste the __init__ between
    # Integer, Float, and Currency
    # because if I use inheritance, PyCharm doesn't auto-complete
    # while typing args
    class IntegerField(int):
        def __init__(
            self,
            *,
            choices=None,
            widget=None,
            initial=None,
            label=None,
            doc='',
            min=None,
            max=None,
            blank=False,
            **kwargs
        ):
            pass
    class FloatField(float):
        def __init__(
            self,
            *,
            choices=None,
            widget=None,
            initial=None,
            label=None,
            doc='',
            min=None,
            max=None,
            blank=False,
            **kwargs
        ):
            pass
    class CurrencyField(Currency):
        def __init__(
            self,
            *,
            choices=None,
            widget=None,
            initial=None,
            label=None,
            doc='',
            min=None,
            max=None,
            blank=False,
            **kwargs
        ):
            pass
    class Link:
        def __init__(self, to):
            pass

class widgets:
    def __getattr__(self, item):
        pass
    # don't need HiddenInput because you can just write <input type="hidden" ...>
    # and then you know the element's selector
    class CheckboxInput:
        pass
    class RadioSelect:
        pass
    class RadioSelectHorizontal:
        pass

class Session:

    config: shared_out.SessionConfig
    vars: shared_out.SessionVars
    num_participants: int
    def get_participants(self) -> List[Participant]:
        pass
    def get_subsessions(self) -> List[SubsessionTV]:
        pass

class Participant:

    session: Session
    vars: shared_out.ParticipantVars
    label: str
    id_in_session: int
    payoff: Currency
    def get_players(self) -> List[PlayerTV]:
        pass
    def payoff_plus_participation_fee(self) -> RealWorldCurrency:
        pass

class BaseConstants:
    pass

class BaseSubsession:

    session: Session
    round_number: int
    def get_groups(self) -> List[GroupTV]:
        pass
    def get_group_matrix(self) -> List[List[int]]:
        pass
    def set_group_matrix(
        self, group_matrix: Union[List[List[PlayerTV]], List[List[int]]]
    ):
        pass
    def get_players(self) -> List[PlayerTV]:
        pass
    def in_previous_rounds(self) -> List[SubsessionTV]:
        pass
    def in_all_rounds(self) -> List[SubsessionTV]:
        pass
    def in_round(self, round_number) -> SubsessionTV:
        pass
    def in_rounds(self, first, last) -> List[SubsessionTV]:
        pass
    def group_like_round(self, round_number: int):
        pass
    def group_randomly(self, fixed_id_in_group: bool = False):
        pass


# Using TypeVar instead of the BaseSubsession seems to make PyCharm
# allow BaseSubsession be passed to a function marked as taking a Subsession arg
SubsessionTV = TypeVar('SubsessionTV', bound=BaseSubsession)


class BaseGroup:

    session: Session
    subsession: BaseSubsession
    round_number: int
    id_in_subsession: int
    def get_players(self) -> List[PlayerTV]:
        pass
    def get_player_by_role(self, role) -> PlayerTV:
        pass
    def get_player_by_id(self, id_in_group) -> PlayerTV:
        pass
    def in_previous_rounds(self) -> List[GroupTV]:
        pass
    def in_all_rounds(self) -> List[GroupTV]:
        pass
    def in_round(self, round_number) -> GroupTV:
        pass
    def in_rounds(self, first: int, last: int) -> List[GroupTV]:
        pass


GroupTV = TypeVar('GroupTV', bound=BaseGroup)


class BasePlayer:

    id_in_group: int
    payoff: Currency
    participant: Participant
    session: Session
    group: GroupTV
    subsession: BaseSubsession
    round_number: int
    role: str
    def in_previous_rounds(self) -> List[PlayerTV]:
        pass
    def in_all_rounds(self) -> List[PlayerTV]:
        pass
    def get_others_in_group(self) -> List[PlayerTV]:
        pass
    def get_others_in_subsession(self) -> List[PlayerTV]:
        pass
    def in_round(self, round_number) -> PlayerTV:
        pass
    def in_rounds(self, first, last) -> List[PlayerTV]:
        pass


PlayerTV = TypeVar('PlayerTV', bound=BasePlayer)


class ExtraModel:
    pass

class WaitPage:

    wait_for_all_groups = False
    group_by_arrival_time = False
    title_text: str
    body_text: str
    template_name: str
    after_all_players_arrive: str

    round_number: int
    participant: Participant
    session: Session

    @staticmethod
    def is_displayed(player: Player):
        pass

    @staticmethod
    def js_vars(player: Player):
        pass

    @staticmethod
    def vars_for_template(player: Player):
        pass

    @staticmethod
    def app_after_this_page(player: Player, upcoming_apps):
        pass

class Page:

    round_number: int
    template_name: str
    timeout_seconds: int
    timer_text: str
    participant: Participant
    session: Session
    form_model: str
    form_fields: List[str]

    @staticmethod
    def live_method(player: Player, data):
        pass


    @staticmethod
    def get_form_fields(player: Player):
        pass

    @staticmethod
    def vars_for_template(player: Player):
        pass

    @staticmethod
    def js_vars(player: Player):
        pass

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        pass

    @staticmethod
    def is_displayed(player: Player):
        pass

    @staticmethod
    def error_message(player: Player, values):
        pass

    @staticmethod
    def get_timeout_seconds(player: Player):
        pass

    @staticmethod
    def app_after_this_page(player: Player, upcoming_apps):
        pass


class Bot:
    html: str
    case: Any
    cases: List
    participant: Participant
    session: Participant
    round_number: int
    player: PlayerTV
    group: GroupTV
    subsession: SubsessionTV


def Submission(
    PageClass, post_data: dict = {}, *, check_html=True, timeout_happened=False
):
    pass

def SubmissionMustFail(
    PageClass, post_data: dict = {}, *, check_html=True, error_fields=[]
):
    pass

def expect(*args):
    pass
