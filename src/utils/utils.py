# import json
# from shared import CFG_DIR

# with open(CFG_DIR) as config_file:
#     DATA = json.load(config_file)

import os
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())
TOKEN = os.getenv("DISCORD_TOKEN")
