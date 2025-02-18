# Copyright contributors to the ITBench project. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import json
import logging
from typing import Any, Dict, Optional, Tuple

from openai import OpenAI

from .base import BaseLLMBackend

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


class OpenAILLMBackend(BaseLLMBackend):

    def __init__(self, model_name: str, base_url: str, api_key: str, temperature: float, seed: int, top_p: float, parameters: Any = None):
        super().__init__(model_name, base_url, api_key, temperature, seed, top_p, parameters)
        self.client = OpenAI(base_url=base_url, api_key=self.api_key)

    def inference(self, system_prompt: str, input: str) -> str:
        logger.info(f"OpenAI-Inference NL input received: {input}")
        print(f"OpenAI-Inference NL input received: {input}")

        logger.info(f"OpenAI-Inference NL input received: {input}")
        print(f"OpenAI-Inference NL input received: {input}")

        completion = self.client.chat.completions.create(model=self.model_name,
                                                         messages=[
                                                             {
                                                                 "role": "system",
                                                                 "content": system_prompt
                                                             },
                                                             {
                                                                 "role": "user",
                                                                 "content": input
                                                             },
                                                         ],
                                                         seed=self.seed,
                                                         top_p=self.top_p,
                                                         temperature=self.temperature)
        return completion.choices[0].message.content

    def function_calling_inference(self,
                                   system_prompt: str,
                                   input: str,
                                   tools: Optional[Dict] = None) -> Tuple[str, Dict]:
        logger.info(f"OpenAI-FunctionCallingInference NL input received: {input}")
        print(f"OpenAI-FunctionCallingInference NL input received: {input}")

        completion = self.client.chat.completions.create(model=self.model_name,
                                                         messages=[
                                                             {
                                                                 "role": "system",
                                                                 "content": system_prompt
                                                             },
                                                             {
                                                                 "role": "user",
                                                                 "content": input
                                                             },
                                                         ],
                                                         tools=tools,
                                                         seed=self.seed,
                                                         top_p=self.top_p,
                                                         temperature=self.temperature)
        finish_reason = completion.choices[0].finish_reason
        if finish_reason == "tool_calls":
            function_name, function_arguments = completion.choices[0].message.tool_calls[0].function.name, json.loads(
                completion.choices[0].message.tool_calls[0].function.arguments)
            logger.info(
                f"OpenAI-FunctionCallingInference function arguments identified are: {function_name} {function_arguments}"
            )
            print(
                f"OpenAI-FunctionCallingInference function arguments identified are: {function_name} {function_arguments}"
            )
            return function_name, function_arguments
        logger.info(f"OpenAI-FunctionCallingInference unsuccessful finish reason is: {finish_reason}")
        print(f"OpenAI-FunctionCallingInference unsuccessful finish reason is: {finish_reason}")
        return None, None
