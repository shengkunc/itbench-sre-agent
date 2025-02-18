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


from typing import Any, Dict, Optional


class BaseLLMBackend:

    def __init__(self, model_name: str, base_url: str, api_key: str, api_version: str = None, temperature: float = 0.0, seed: int = 42, top_p: float = 0.0, parameters: Any = None):
        self.model_name = model_name
        self.base_url = base_url
        self.api_key = api_key
        self.api_version = api_version
        self.temperature = temperature
        self.seed = seed
        self.top_p = top_p
        self.parameters = parameters

    def inference(self, prompt: str) -> str:
        raise NotImplementedError("This method should be overridden by subclasses")

    def function_calling_inference(self, system_prompt: str, input: str, tools: Optional[Dict] = None) -> str:
        raise NotImplementedError("This method should be overridden by subclasses")
