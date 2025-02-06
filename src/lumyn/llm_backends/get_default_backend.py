import json
import os

from crewai import LLM
from dotenv import load_dotenv
from langchain_ibm import WatsonxLLM

from .open_ai import OpenAILLMBackend
from .open_ai_azure import OpenAILLMBackendAzure
from .watsonx_ai import WatsonxLLMBackend

load_dotenv()

global LLM_MODEL_NAME, LLM_BASE_URL, LLM_API_KEY, LLM_SEED, LLM_TOP_P, LLM_API_VERSION, LLM_TEMPERATURE, LLM_PROJECT_ID, IS_WATSONX, IS_AZURE

try:
    LLM_MODEL_NAME = os.environ["LLM_MODEL_NAME"]
except KeyError:
    LLM_MODEL_NAME = "gpt-4o-2024-08-06"
    print(f"Unable to find environment variable - LLM_MODEL_NAME. Defaulting to {LLM_MODEL_NAME}.")

try:
    LLM_BASE_URL = os.environ["LLM_BASE_URL"].rstrip("/")
except KeyError:
    LLM_BASE_URL = "https://api.openai.com/v1"
    print(f"Unable to find environment variable - LLM_BASE_URL. Defaulting to {LLM_BASE_URL}.")

try:
    LLM_API_KEY = os.environ["LLM_API_KEY"]
except KeyError:
    print("Unable to find environment variable - LLM_API_KEY.")
    raise

try:
    LLM_SEED = int(os.environ["LLM_SEED"])
except KeyError:
    LLM_SEED = 42
    print(f"Unable to find environment variable - LLM_SEED. Defaulting to {LLM_SEED}.")

try:
    LLM_TOP_P = float(os.environ["LLM_TOP_P"])
except KeyError:
    LLM_TOP_P = 0.0000001
    print(f"Unable to find environment variable - LLM_TOP_P. Defaulting to {LLM_TOP_P}.")

try:
    LLM_TEMPERATURE = float(os.environ["LLM_TEMPERATURE"])
except KeyError:
    LLM_TEMPERATURE = 0.0
    print(f"Unable to find environment variable - LLM_TEMPERATURE. Defaulting to {LLM_TEMPERATURE}.")
except ValueError as e:
    print("Incorrect LLM_TEMPERATURE value:", e)
    raise

IS_WATSONX = os.getenv("IS_WATSONX", "False") == "True"
if IS_WATSONX or "ibm" in LLM_BASE_URL:
    IS_WATSONX = True
    os.environ["WATSONX_APIKEY"] = LLM_API_KEY
    # For LiteLLM
    os.environ["WATSONX_URL"] = LLM_BASE_URL

    try:
        LLM_PROJECT_ID = os.environ["LLM_PROJECT_ID"]
        # For LiteLLM
        os.environ["WATSONX_PROJECT_ID"] = LLM_PROJECT_ID
    except KeyError:
        print("Unable to find environment variable - LLM_PROJECT_ID.")
        raise

    try:
        LLM_CONFIGURATION_PARAMETERS = json.loads(os.environ["LLM_CONFIGURATION_PARAMETERS"])
    except KeyError:
        LLM_CONFIGURATION_PARAMETERS = {"temperature": LLM_TEMPERATURE}
        print(
            f"Unable to determine environment variable - LLM_CONFIGURATION_PARAMETERS. Defaulting to {LLM_CONFIGURATION_PARAMETERS}."
        )

IS_AZURE = os.getenv("IS_AZURE", "False") == "True"
try:
    LLM_API_VERSION = os.environ["LLM_API_VERSION"]
except KeyError:
    print("Unable to find environment variable - LLM_API_VERSION. Using default instead.")
    LLM_API_VERSION = "2024-09-01-preview"

if IS_AZURE or "microsoft" in LLM_BASE_URL:
    os.environ["AZURE_API_KEY"] = LLM_API_KEY
    os.environ["AZURE_API_BASE"] = LLM_BASE_URL
    os.environ["AZURE_API_VERSION"] = LLM_API_VERSION


def get_llm_backend_for_agents():
    llm = None
    if IS_WATSONX:
        llm = LLM(model="watsonx_text/" + LLM_MODEL_NAME,
                  base_url=LLM_BASE_URL,
                  api_key=LLM_API_KEY,
                  **LLM_CONFIGURATION_PARAMETERS)
    elif IS_AZURE:
        llm = LLM(model="azure/" + LLM_MODEL_NAME,
                  base_url=LLM_BASE_URL,
                  seed=LLM_SEED,
                  top_p=LLM_TOP_P,
                  api_key=LLM_API_KEY,
                  temperature=LLM_TEMPERATURE)
    else:
        llm = LLM(model= "hosted_vllm/" + LLM_MODEL_NAME,
                  base_url=LLM_BASE_URL,
                  api_key=LLM_API_KEY,
                  seed=LLM_SEED,
                  top_p=LLM_TOP_P,
                  temperature=LLM_TEMPERATURE)
    return llm


def get_llm_backend_for_tools():
    if IS_WATSONX:
        return WatsonxLLMBackend(model_name=LLM_MODEL_NAME,
                                 base_url=LLM_BASE_URL,
                                 api_key=LLM_API_KEY,
                                 temperature=None,
                                 seed=None,
                                 top_p=None,
                                 parameters=LLM_CONFIGURATION_PARAMETERS,
                                 project_id=LLM_PROJECT_ID)
    elif IS_AZURE:
        return OpenAILLMBackendAzure(model_name=LLM_MODEL_NAME,
                                     base_url=LLM_BASE_URL,
                                     api_key=LLM_API_KEY,
                                     seed=LLM_SEED,
                                     top_p=LLM_TOP_P,
                                     api_version=LLM_API_VERSION,
                                     temperature=LLM_TEMPERATURE)
    else:
        return OpenAILLMBackend(model_name=LLM_MODEL_NAME,
                                base_url=LLM_BASE_URL,
                                api_key=LLM_API_KEY,
                                seed=LLM_SEED,
                                top_p=LLM_TOP_P,
                                temperature=LLM_TEMPERATURE)
