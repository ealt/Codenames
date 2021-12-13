from typing import Optional
from codenames.data.codenames_pb2 import (CommonInformation, SharedAction,
                                          SharedClue, Turn)


def update_information_with_clue(common_information: CommonInformation,
                                 shared_clue: SharedClue) -> None:
    common_information.turn_history.append(Turn(clue=shared_clue))


def update_informaiton_with_action(common_information: CommonInformation,
                                   shared_action: SharedAction) -> None:
    try:
        common_information.turn_history[-1].actions.append(shared_action)
    except IndexError:
        update_information_with_clue(common_information, SharedClue())
        update_informaiton_with_action(common_information, shared_action)


def get_last_clue(
        common_information: CommonInformation) -> Optional[SharedClue]:
    try:
        return common_information.turn_history[-1].clue
    except IndexError:
        return None


def get_last_action(
        common_information: CommonInformation) -> Optional[SharedAction]:
    try:
        return common_information.turn_history[-1].actions[-1]
    except IndexError:
        return None