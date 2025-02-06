import logging

from lumyn.llm_backends.get_default_backend import get_llm_backend_for_tools
from lumyn.tools.grafana.nl2metrics import NL2MetricsCustomTool

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


def test_nl2metrics():
    tool = NL2MetricsCustomTool(llm_backend=get_llm_backend_for_tools())
    nl_query = "get the cpu utilization of pods in the front deployment."
    result = tool._run(nl_query)
    logger.info(f"Result from the tool: \n{result}")
    print(result)

if __name__ == "__main__":
    test_nl2metrics()
