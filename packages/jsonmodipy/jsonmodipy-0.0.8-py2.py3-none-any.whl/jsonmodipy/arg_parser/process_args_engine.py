"""Processes API arguments stores the LLM engine and communication channel."""
import os
from argparse import Namespace
from typing import Dict, Tuple

from typeguard import typechecked

from jsonmodipy.file_parsing import load_config
from jsonmodipy.Hardcoded import Hardcoded


# pylint: disable=R0903
class Llm_and_coms:
    """Stores the LLM communication target and method. E.g. which engine, and
    whether to use API, browser or other communication channel.

    Attributes:
        engine (str): The name of the LLM model/engine that is to be used.
        channel (str): The chosen communication method with the LLM model.
    """

    @typechecked
    def __init__(
        self,
        engine: str,
        channel: str,
    ):
        """Initializes LLM model target and communication method.

        Args:
            engine (str): The name of the LLM model/engine that is to be used.
            channel (str): The chosen communication method with the LLM model.
        """

        if engine == "chatgpt3.5":
            self.engine: str = engine
            if channel == "browser":
                self.channel: str = channel
            else:
                raise NotImplementedError(
                    f"Error, using official API for LLM:{engine} is not yet"
                    + " implemented."
                )
        else:
            raise NotImplementedError(
                f"Error, LLM:{engine} is not yet implemented."
            )


@typechecked
def process_api_args_engine(
    *,
    args: Namespace,
) -> Tuple[Llm_and_coms, Dict[str, Dict[str, str]]]:
    """Stores the LLM communication target and method.

    E.g. which engine, and whether to use API, browser or other
    communication channel.
    """
    coms: Llm_and_coms = Llm_and_coms(
        engine=args.engine,
        channel=args.channel,
    )
    loaded_config: Dict[str, Dict[str, str]]
    # Check if config file exists, at default path, and if yes, load it.
    hardcoded: Hardcoded = Hardcoded()
    if os.path.isfile(hardcoded.config_filepath):
        loaded_config = load_config(
            config_filepath=hardcoded.config_filepath,
            coms=coms,
        )
    elif (args.config_filepath is not None) and (
        os.path.isfile(args.config_filepath)
    ):
        loaded_config = load_config(
            config_filepath=args.config_filepath,
            coms=coms,
        )
    else:
        raise FileNotFoundError(
            "Error, could not find your login credentials "
            "for the LLM. Please include: --config-filepath"
            "<the filepath to your config file>"
        )
    if coms.engine not in loaded_config.keys():
        raise KeyError(
            f"Error, your config file does not contain credentials "
            f"for the LLM: {coms.engine}. Please add them to your "
            f"config file: {args.config_filepath}"
        )

    return coms, loaded_config
