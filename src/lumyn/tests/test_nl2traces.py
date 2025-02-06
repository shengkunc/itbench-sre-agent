import logging

from lumyn.llm_backends.get_default_backend import get_llm_backend_for_tools
from lumyn.tools.grafana.nl2traces import NL2TracesCustomTool

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


# def test_nl2traces():
#     nl2traces_tool = NL2TracesCustomTool(llm_backend=get_llm_backend_for_tools())
#     nl_query = "get traces from the frontend service in the last hour."
#     result = nl2traces_tool._run(nl_query)
#     logger.info(f"Result from NL2Traces tool: \n{result}")
#     print(result)

# if __name__ == "__main__":
#     test_nl2traces()


