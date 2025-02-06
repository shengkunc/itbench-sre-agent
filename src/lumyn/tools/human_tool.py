import logging
import os
from typing import Any

from crewai.tools.base_tool import BaseTool
from pydantic import BaseModel, Field

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


class HumanCustomTool(BaseTool):
    name: str = "human"
    description: str = ("Allows a human user to provide input")

    def _run(self) -> str:
        return input()