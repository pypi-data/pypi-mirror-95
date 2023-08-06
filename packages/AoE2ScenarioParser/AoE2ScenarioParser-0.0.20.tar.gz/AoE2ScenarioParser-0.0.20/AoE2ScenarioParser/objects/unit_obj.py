from __future__ import annotations

import math

from AoE2ScenarioParser.datasets import units, buildings
from AoE2ScenarioParser.datasets.players import Player
from AoE2ScenarioParser.helper import helper
from AoE2ScenarioParser.helper.helper import Tile
from AoE2ScenarioParser.helper.retriever_object_link import RetrieverObjectLink
from AoE2ScenarioParser.objects.aoe2_object import AoE2Object


class UnitObject(AoE2Object):
    _link_list = [
        RetrieverObjectLink("player", retrieve_history_number=0),
        RetrieverObjectLink("x", "UnitsPiece", "players_units[__index__].units[__index__].x"),
        RetrieverObjectLink("y", "UnitsPiece", "players_units[__index__].units[__index__].y"),
        RetrieverObjectLink("z", "UnitsPiece", "players_units[__index__].units[__index__].z"),
        RetrieverObjectLink("reference_id", "UnitsPiece", "players_units[__index__].units[__index__].reference_id"),
        RetrieverObjectLink("unit_const", "UnitsPiece", "players_units[__index__].units[__index__].unit_const"),
        RetrieverObjectLink("status", "UnitsPiece", "players_units[__index__].units[__index__].status"),
        RetrieverObjectLink("rotation", "UnitsPiece", "players_units[__index__].units[__index__].rotation"),
        RetrieverObjectLink("initial_animation_frame", "UnitsPiece",
                            "players_units[__index__].units[__index__].initial_animation_frame"),
        RetrieverObjectLink("garrisoned_in_id", "UnitsPiece",
                            "players_units[__index__].units[__index__].garrisoned_in_id"),
    ]

    def __init__(self,
                 player: Player,
                 x: float,
                 y: float,
                 z: float,
                 reference_id: int,
                 unit_const: int,
                 status: int,
                 rotation: float,
                 initial_animation_frame: int,
                 garrisoned_in_id: int
                 ):

        self._player: Player = Player(player)
        """
        PLEASE NOTE: This is an internal (read-only) value for ease of access. It accurately represent the actual 
        player controlling the unit but is not directly connected to it. Changing this value will have no impact to your
        scenario.
        To change which player controls this unit, use:
            unit_manager.change_ownership(UnitObject, to_player)
        """
        self.x: float = x
        self.y: float = y
        self.z: float = z
        self.reference_id: int = reference_id
        self.unit_const: int = unit_const
        self.status: int = status
        self.rotation: float = rotation
        self.initial_animation_frame: int = initial_animation_frame
        self.garrisoned_in_id: int = garrisoned_in_id

        super().__init__()

    @property
    def player(self) -> Player:
        """
        PLEASE NOTE: This is an internal (read-only) value for ease of access. It DOES accurately represent the actual
        player controlling the unit BUT IT IS NOT directly connected to it. Changing this value will have no impact to
        your scenario.
        To change which player controls this unit, use:
            unit_manager.change_ownership(UnitObject, to_player)
        """
        return self._player

    @property
    def rotation(self) -> float:
        return self._rotation

    @rotation.setter
    def rotation(self, rotation: float) -> None:
        self._rotation = rotation

    @property
    def tile(self) -> Tile:
        return Tile(math.floor(self.x), math.floor(self.y))
        # Floor x and y as location (0.9, 0.9) is still Tile[x=0, y=0]

    @tile.setter
    def tile(self, tile: Tile) -> None:
        self.x = tile.x
        self.y = tile.y

    @property
    def name(self) -> str:
        try:
            return helper.pretty_print_name(units.unit_names[self.unit_const])
        except KeyError:  # Object wasn't a unit, maybe a building?
            return helper.pretty_print_name(buildings.building_names[self.unit_const])
