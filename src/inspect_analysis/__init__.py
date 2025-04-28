import importlib.metadata

try:
    __version__ = importlib.metadata.version("inspect_analysis")
except importlib.metadata.PackageNotFoundError:
    __version__ = "unknown"
