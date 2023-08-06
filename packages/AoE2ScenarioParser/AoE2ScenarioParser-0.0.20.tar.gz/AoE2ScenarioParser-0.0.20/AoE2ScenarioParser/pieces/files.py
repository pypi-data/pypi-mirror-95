from typing import Dict

from AoE2ScenarioParser.helper.datatype import DataType
from AoE2ScenarioParser.helper.retriever import Retriever
from AoE2ScenarioParser.helper.retriever_dependency import RetrieverDependency, DependencyAction, DependencyTarget, \
    DependencyEval
from AoE2ScenarioParser.pieces import aoe2_piece
from AoE2ScenarioParser.pieces.structs.ai2 import AI2Struct


class FilesPiece(aoe2_piece.AoE2Piece):
    dependencies: Dict[str, Dict[str, RetrieverDependency]] = {
        "script_file_path": {
            "on_refresh": RetrieverDependency(
                DependencyAction.SET_VALUE, DependencyTarget("MapPiece", "script_name"),
                DependencyEval("x + ('.xs' if len(x) > 0 else '')")
            ),
        },
        "ai_files_present": {
            "on_refresh": RetrieverDependency(
                DependencyAction.SET_VALUE, DependencyTarget("self", "number_of_ai_files"),
                DependencyEval('0 if x == 0 else 1')
            ),
        },
        "number_of_ai_files": {
            "on_construct": RetrieverDependency(
                DependencyAction.SET_REPEAT, DependencyTarget("self", "ai_files_present"),
            ),
            "on_refresh": [
                # RetrieverDependency(
                #     DependencyAction.SET_VALUE, DependencyTarget("self", "ai_files"), DependencyEval('len(x)')
                # ),
                RetrieverDependency(
                    DependencyAction.SET_REPEAT, DependencyTarget("self", "ai_files"),
                    DependencyEval('1 if len(x) > 0 else 0')
                ),
            ],
            "on_commit": RetrieverDependency(
                DependencyAction.REFRESH, DependencyTarget("self", "ai_files_present")
            )
        },
        "ai_files": {
            "on_refresh": RetrieverDependency(
                DependencyAction.SET_REPEAT, DependencyTarget("self", "number_of_ai_files"),
                DependencyEval('0 if x == [] else x')  # x is a list because of the SET_REPEAT present
            ),
            "on_construct": RetrieverDependency(DependencyAction.REFRESH_SELF),
            "on_commit": RetrieverDependency(
                DependencyAction.REFRESH, DependencyTarget("self", "number_of_ai_files")
            )
        },
    }

    def __init__(self, parser_obj=None, data=None, pieces=None):
        retrievers = [
            Retriever("unknown_2", DataType("4")),
            Retriever("script_file_path", DataType("str16")),
            Retriever("script_file_content", DataType("str32")),
            Retriever("ai_files_present", DataType("u32")),
            Retriever("unknown_4", DataType("4")),
            Retriever("number_of_ai_files", DataType("u32"), possibly_list=False),
            Retriever("ai_files", DataType(AI2Struct)),
            Retriever("__END_OF_FILE_MARK__", DataType("1")),
        ]

        super().__init__("Files", retrievers, parser_obj, data=data, pieces=pieces)

    @staticmethod
    def defaults(pieces):
        defaults = {
            'unknown_2': b'\x00' * 4,
            'script_name': "",
            'script_file_content': "",
            'ai_files_present': 0,
            'unknown_4': b'\x00' * 4,
            'number_of_ai_files': [],
            'ai_files': [],
            '__END_OF_FILE_MARK__': b'',
        }
        return defaults
