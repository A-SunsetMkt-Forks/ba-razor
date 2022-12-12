import os
import json
import yaml

from colorama import Fore, Back, Style
from typing import Optional, List, Iterable
from pathlib import Path
from itertools import groupby, chain
from operator import itemgetter, getitem
from pydantic import BaseModel, validator
from icecream import ic

from model import FavorScenario, FavorSchedule, MomotalkOutput, MomotalkContent
from utils import Localizer
