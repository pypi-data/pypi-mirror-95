import math
from typing import Dict

from AoE2ScenarioParser.helper.datatype import DataType
from AoE2ScenarioParser.helper.retriever import Retriever
from AoE2ScenarioParser.helper.retriever_dependency import RetrieverDependency, DependencyAction, DependencyTarget, \
    DependencyEval
from AoE2ScenarioParser.pieces import aoe2_piece
from AoE2ScenarioParser.pieces.structs.terrain import TerrainStruct


class MapPiece(aoe2_piece.AoE2Piece):
    dependencies: Dict[str, Dict[str, RetrieverDependency]] = {
        "villager_force_drop": {
            "on_refresh": RetrieverDependency(
                DependencyAction.SET_REPEAT,
                DependencyTarget('FileHeaderPiece', 'version'),
                DependencyEval('1 if x in [\'1.37\', \'1.40\', \'1.41\'] else 0')
            ),
            "on_construct": RetrieverDependency(DependencyAction.REFRESH_SELF)
        },
        "block_humanity_team_change": {
            "on_refresh": RetrieverDependency(
                DependencyAction.SET_REPEAT,
                DependencyTarget('FileHeaderPiece', 'version'),
                DependencyEval('1 if x in [\'1.41\'] else 0')
            ),
            "on_construct": RetrieverDependency(DependencyAction.REFRESH_SELF)
        },
        "map_width": {
            "on_refresh": RetrieverDependency(
                DependencyAction.SET_VALUE,
                DependencyTarget("self", "terrain_data"),
                DependencyEval("int(sqrt(len(x)))", {'sqrt': math.sqrt})
            )
        },
        "map_height": {
            "on_refresh": RetrieverDependency(
                DependencyAction.SET_VALUE,
                DependencyTarget("self", "terrain_data"),
                DependencyEval("int(sqrt(len(x)))", {'sqrt': math.sqrt})
            )
        },
        "terrain_data": {
            "on_refresh": RetrieverDependency(
                DependencyAction.SET_REPEAT,
                DependencyTarget("self", "map_width"),
                DependencyEval("pow(x, 2)")
            ),
            "on_construct": RetrieverDependency(DependencyAction.REFRESH_SELF),
            "on_commit": RetrieverDependency(
                DependencyAction.REFRESH, DependencyTarget(["self", "self"], ["map_width", "map_height"])
            )
        },
        "script_name": {
            "on_commit": RetrieverDependency(
                DependencyAction.REFRESH, DependencyTarget("FilesPiece", "script_file_path")
            )
        },
    }

    def __init__(self, parser_obj=None, data=None, pieces=None):
        retrievers = [
            Retriever('separator_1', DataType("2")),
            Retriever('unknown_string', DataType("str16")),
            Retriever('separator_2', DataType("2")),
            Retriever('map_color_mood', DataType("str16")),
            Retriever('separator_3', DataType("2")),
            # [VERSION CHANGE] ADDED in 1.37 > 1.40
            Retriever('script_name', DataType("str16")),
            # [VERSION CHANGE] ADDED in 1.40 > 1.41
            Retriever('block_humanity_team_change', DataType("u8")),
            Retriever('collide_and_correct', DataType("u8")),
            # [VERSION CHANGE] ADDED in 1.36 > 1.37
            Retriever('villager_force_drop', DataType("u8")),
            # [VERSION CHANGE] ADDED in 1.37 > 1.40
            Retriever('unknown', DataType("128")),
            Retriever('player_1_camera_y', DataType("s32")),
            Retriever('player_1_camera_x', DataType("s32")),
            Retriever('ai_type', DataType("s8")),
            Retriever('map_width', DataType("s32")),
            Retriever('map_height', DataType("s32")),
            Retriever('terrain_data', DataType(TerrainStruct))
        ]

        super().__init__("Map", retrievers, parser_obj, data=data, pieces=pieces)

    @staticmethod
    def defaults(pieces):
        defaults = {
            'separator_1': b'`\n',
            'unknown_string': '',
            'separator_2': b'`\n',
            'map_color_mood': 'Empty',
            'separator_3': b'`\n',
            'script_name': '',
            'block_humanity_team_change': 0,
            'collide_and_correct': 0,
            'villager_force_drop': 0,
            'unknown': b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'
                       b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'
                       b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'
                       b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'
                       b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'
                       b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff',
            'player_1_camera_y': -559026163,
            'player_1_camera_x': 2,
            'ai_type': 1,
            'map_width': 120,
            'map_height': 120,
            'terrain_data': [TerrainStruct(data=list(TerrainStruct.defaults(pieces).values()), pieces=pieces) for _ in
                             range(120 * 120)],
        }
        return defaults
