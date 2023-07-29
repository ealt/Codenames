# Codenames

This is an implementation of the game codenames

## Game Overview

Codenames is turn based game played by competing teams of players divided into
two roles, clue giver and guesser. There game setup consists of several agents
with codenames known by all players as well as secret identities which only the
clue givers know. The identities can correspond to one of the player teams,
neutral, or fatal. The objective of each teams is to be the first to identify
all of their team's agents without revealing fatal agents. Gameplay involves
turns in which the clue giver for the currently active team provides a clue
consisting of a single word and a quantity. Using information revealed by the
clue givers, the guessers from the active team then have the opportunity to
reveal the identities of unkown agents one at a time until they either reveal
an agent that is not aligned with their team or they exceed the quantity given
by the clue giver for the turn.