import json
import logging
import os
import re
from typing import Any, Dict, Optional, Tuple

from langchain_ibm import ChatWatsonx

from .base import BaseLLMBackend
from .function_calling_templates import FOR_NON_NATIVE_FUNCTION_CALLING

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


class WatsonxLLMBackend(BaseLLMBackend):

    def __init__(self, model_name: str, base_url: str, api_key: str,
                 temperature: float, seed:int, top_p:float, parameters: Any, project_id: str):
        super().__init__(model_name, base_url, api_key, api_version=None, temperature=temperature, seed=seed, top_p=top_p,
                         parameters=parameters)
        
        
        
        self.is_function_calling_supported = os.getenv("IS_NATIVE_FUNCTION_CALLING_SUPPORTED", "True") == "True"

        


        self.client = ChatWatsonx(
            model_id=self.model_name,
            url=self.base_url,
            project_id=project_id,
        )

    def inference(self, system_prompt: str, input: str) -> str:
        logger.info(f"WatsonX.AI-Inference NL input received: {input}")
        print(f"WatsonX.AI-Inference NL input received: {input}")

        completion = self.client.invoke([
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": input
            },
        ],
                                        params=self.parameters)
        return completion.content

    def function_calling_inference(
            self,
            system_prompt: str,
            input: str,
            tools: Optional[Dict] = None) -> Tuple[str, Dict]:
        logger.info(
            f"WatsonX.AI-FunctionCallingInference NL input received: {input}")
        print(
            f"WatsonX.AI-FunctionCallingInference NL input received: {input}")

        if self.is_function_calling_supported:
            if tools is not None:
                self.client = self.client.bind_tools(tools=tools)

        # if self.is_function_calling_supported:
        system_prompt += system_prompt + "\n" + FOR_NON_NATIVE_FUNCTION_CALLING

        completion = self.client.invoke([
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": input
            },
        ],
                                        params=self.parameters)
        finish_reason = completion.response_metadata["finish_reason"]
        if finish_reason == "tool_calls":
            function_name, function_arguments = completion.tool_calls[0][
                "name"], completion.tool_calls[0]["args"]
            logger.info(
                f"WatsonX.AI-FunctionCallingInference function arguments via tool_calls identified are: {function_name} {function_arguments}"
            )
            print(
                f"WatsonX.AI-FunctionCallingInference function arguments via tool_calls identified are: {function_name} {function_arguments}"
            )
            return function_name, function_arguments
        elif finish_reason == "stop":
            function_name, function_arguments = self.parse_tool_response(
                completion.content)
            if function_name is not None and function_arguments is not None:
                logger.info(
                    f"WatsonX.AI-FunctionCallingInference function arguments via stop identified are: {function_name} {function_arguments}"
                )
                print(
                    f"WatsonX.AI-FunctionCallingInference function arguments via stop identified are: {function_name} {function_arguments}"
                )
                return function_name, function_arguments
        else:
            pass
        logger.info(
            f"WatsonX.AI-FunctionCallingInference unsuccessful finish reason is: {finish_reason}"
        )
        print(
            f"WatsonX.AI-FunctionCallingInference unsuccessful finish reason is: {finish_reason}"
        )
        logger.info(
            f"WatsonX.AI-FunctionCallingInference unsuccessful response: {completion}"
        )
        print(
            f"WatsonX.AI-FunctionCallingInference unsuccessful response: {completion}"
        )
        return None, None

    def parse_tool_response(self, response: str):
        function_regex = r"<function=(\w+)>(.*?)</function>"
        match = re.search(function_regex, response)

        if match:
            function_name, args_string = match.groups()
            try:
                args = json.loads(args_string)
                return function_name, args
            except json.JSONDecodeError as error:
                print(f"Error parsing function arguments: {error}")
                return None, None
        return None, None
