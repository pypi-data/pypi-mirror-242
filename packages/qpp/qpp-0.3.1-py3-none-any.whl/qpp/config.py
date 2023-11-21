
from pathlib import Path
try:
    from tomllib import load as load_toml
except ModuleNotFoundError:
    from tomli import load as load_toml


# Loading config options will come later.
#
# CONFIG_PATH = Path.home() / '.config'
# CONFIG_FILE = CONFIG_PATH / 'qpp.toml'
#
# config_file = CONFIG_PATH / CONFIG_FILE
# if config_file.exists():
#     with open(config_file, "rb") as f:
#         data = load_toml(f)
#
#     BROWSER_CMD = data['browser']['command']
# else:
#     pass
