import logging

from lumyn.llm_backends.get_default_backend import get_llm_backend_for_tools
from lumyn.tools.grafana.nl2logs import NL2LogsCustomTool

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


def test_nl2logs():
    tool = NL2LogsCustomTool(llm_backend=get_llm_backend_for_tools())
    nl_query = """{'query': '{namespace="hotel-reservations"} |= "frontend"', 'start': '1732241453839725000', 'end': '1732245053839725000'}"""
    result = tool._run(nl_query)
    logger.info(f"Result from the tool: \n{result}")
    print(result)

if __name__ == "__main__":
    test_nl2logs()



# http://ae7c6d28762e740078adc383da232663-218958276.us-east-2.elb.amazonaws.com/prometheus/api/datasources/proxy/uid/be4ju54qc7j0ga/loki/api/v1/labels
# 
# 