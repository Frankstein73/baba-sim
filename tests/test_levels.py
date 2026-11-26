"""Levels by name, the level packs, and what a level file redefines."""

import json

import pytest

from babasim.api import Game
from babasim.runtime import DATA, Engine, campaign, level_name, level_stem

PACKS = sorted(p.stem.removeprefix("campaign_") for p in DATA.glob("campaign_*.json"))


def test_a_level_is_found_by_its_name_or_its_file():
    assert level_stem("baba", "baba is you") == level_stem("baba", "Baba Is You") == level_stem("baba", "0level") == "0level"
    assert level_name("baba", "0level") == "baba is you"
    game = Game("prison (Neon City)", "disappearance")  # two levels of that pack are called "prison"
    assert (game.level, game.file) == ("prison (Neon City)", "63level")
    with pytest.raises(FileNotFoundError):
        level_stem("baba", "no such level")


@pytest.mark.parametrize("world", PACKS)
def test_campaign_names_are_unique_and_every_level_starts(world):
    listed = campaign(world)
    assert len({each["name"].casefold() for each in listed}) == len(listed) > 0
    engine = Engine(world)
    for each in listed:
        engine.load(each["level"])
        assert engine.G["units"].arr, each


def test_objects_a_level_redefines_take_their_new_name_and_kind():
    engine = Engine()
    engine.load("20level")  # the lake: the fungus slot is a jelly here
    names = {unit[0] for unit in engine.state()}
    assert "jelly" in names and "text_jelly" in names and "fungus" not in names
    engine = Engine("repose")
    engine.load("205level")  # a text slot redefined as a plain object fills the background
    assert sum(unit[0] == "pixel" for unit in engine.state()) == 221 and engine.G["unitreference"]["pixel"] == "object028"


def test_a_rule_with_two_conditions_is_evaluated():
    game = Game("import to microcosm", "perennial")  # used to fail on the second condition of a rule
    for action in ["right", "up", "left", "down"] * 3:
        if game.status != "playing":
            break
        game.step(action)
    assert json.dumps(game.observe())
