from typing import Optional
from codenames.data.codenames_pb2 import (
    CommonInformation, SharedAction, SharedClue, Turn
)
from codenames.data.data_validation import validate_teams
from codenames.data.types import (
    Codename, NullTeam, Quantity, Team, UnknownTeam, Unlimited
)


def update_information_with_clue(
    common_information: CommonInformation, shared_clue: SharedClue
) -> None:
    common_information.turn_history.append(Turn(clue=shared_clue))


def update_information_with_action(
    common_information: CommonInformation, shared_action: SharedAction
) -> None:
    try:
        common_information.turn_history[-1].actions.append(shared_action)
    except IndexError:
        update_information_with_clue(
            common_information, SharedClue(team=UnknownTeam)
        )
        update_information_with_action(common_information, shared_action)
    guess = Codename(shared_action.action.guess)
    identity = Team(shared_action.action_outcome.identity)
    if identity != NullTeam:
        common_information.identity_counts[identity] -= 1
        common_information.agent_sets[UnknownTeam].remove(guess)
        common_information.agent_sets[identity].append(guess)


def get_last_clue(
    common_information: CommonInformation
) -> Optional[SharedClue]:
    try:
        return common_information.turn_history[-1].clue
    except IndexError:
        return None


def get_last_action(
    common_information: CommonInformation
) -> Optional[SharedAction]:
    try:
        return common_information.turn_history[-1].actions[-1]
    except IndexError:
        return None


def get_n_teams(common_information: CommonInformation) -> int:
    teams = (
        set(common_information.identity_counts)
        | set(common_information.agent_sets)
    )
    if not validate_teams(teams):
        raise ValueError
    return max(teams)


def get_guesses_remaining(common_information: CommonInformation) -> Quantity:
    last_clue = get_last_clue(common_information)
    if last_clue is None:
        return Quantity(0)
    clue_guesses = last_clue.quantity
    if clue_guesses == Unlimited:
        return Unlimited
    guesses_made = len(common_information.turn_history[-1].actions)
    return Quantity(clue_guesses - guesses_made)


def get_active_team(common_information: CommonInformation) -> Team:
    last_clue = get_last_clue(common_information)
    if last_clue is None or last_clue.team in (NullTeam, UnknownTeam):
        return UnknownTeam
    last_active_team = last_clue.team
    guesses_remaining = get_guesses_remaining(common_information)
    if guesses_remaining == 0:
        n_teams = get_n_teams(common_information)
        return ((last_active_team + 1) % n_teams) + 1
    else:
        return last_active_team
