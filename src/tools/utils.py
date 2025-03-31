# Standard Library Imports
import os
from pathlib import Path, PosixPath

# Third-party Imports
import pygame


def get_repo_path() -> PosixPath:
    """Returns absolute path of this repository as a string"""
    current_path = Path(os.path.abspath(".."))
    this_file_path = current_path / Path(__file__)
    return this_file_path.parent.parent.parent


def key_down(key_name: str) -> bool:
    key_input = pygame.key.get_pressed()
    key = getattr(pygame, f"K_{key_name}")
    if key_input[key]:
        return True
    return False
