import logging

from dotenv import load_dotenv

from lumyn.llm_backends.get_default_backend import get_llm_backend_for_tools
from lumyn.tools.code_generation.nl2script import NL2ScriptCustomTool

# Load environment variables from the .env file
load_dotenv()

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


def test_nl2script():
    # Instantiate the tool
    tool = NL2ScriptCustomTool(llm_backend=get_llm_backend_for_tools())

    # Define a natural language query
    nl_query = """1. Increase memory limits for the adservice to accommodate traffic peaks.
2. Monitor adservice performance after adjusting memory limits.
3. Investigate frontend service logs to identify specific error causes.
4. Scale frontend services horizontally if resource constraints are identified.
5. Review and correct query parameters in the observability setup.
6. Ensure observability tools are properly configured to report necessary metrics.
7. Validate that observability data is being collected and analyzed correctly.
8. Test the system under peak load conditions to confirm stability and performance improvements."""

    # Call the tool's _run method to test it
    result = tool._run(nl_query)
    logger.info(f"Result from the tool: \n{result}")

if __name__ == "__main__":
    test_nl2script()