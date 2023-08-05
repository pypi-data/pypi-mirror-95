import pathlib
with pathlib.Path(__file__).parent.joinpath('resources/version').open('r') as f:
    __version__ = f.read()