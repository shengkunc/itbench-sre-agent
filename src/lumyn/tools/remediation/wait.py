import logging
import os
from typing import Any, Dict, Optional, Type

from crewai.tools.base_tool import BaseTool
from pydantic import BaseModel, Field
import time 

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


class WaitCustomToolInput(BaseModel):
    seconds: float = Field(
        title="Seconds",
        description="Number of seconds to wait.",
    )

class WaitCustomTool(BaseTool):
    name: str = "Wait Tool."
    description: str = ("Wait for enviroment to stabilize.")
    args_schema: Type[BaseModel] = WaitCustomToolInput

    def _run(self, seconds: float) -> None:
        try:
            time.sleep(seconds)
            logger.info(f"WaitCustomTool NL prompt received: {seconds}")
            print(f"WaitCustomTool NL prompt received: {seconds}")
            return None
        except Exception as e:
            print(f"WaitCustomTool error: {str(e)}")
            logger.error(f"WaitCustomTool error: {str(e)}")
            return None