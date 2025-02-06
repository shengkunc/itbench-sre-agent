import json
import time
from typing import Dict, List, Optional

from pydantic import BaseModel, ValidationError


class ArgumentsModel(BaseModel):
    service: str
    start_time: int
    end_time: int
    limit: int
    error_traces_only: Optional[bool] = False
    operation: Optional[str] = None


class JaegerLinter:
    def __init__(self):
        pass

    def lint(self, arguments, services, operations, current_time: int):
        # alert_generation_time: int = int(time.time_ns() / 1000),
        # threshold_for_golden_period: int = 1800000) -> str:
        try:
            args = ArgumentsModel.model_validate_json(json.dumps(arguments))
            lint_message = str()

            if args.start_time == args.end_time:
                lint_message += "Invalid start time. start time and end time cannot be the same."
            if args.end_time - args.start_time > 43200000000:
                lint_message += "Invalid start time. start time should be within 12 hours of end time."
            if not (1 <= args.limit <= 10):
                lint_message += "Invalid limit. Limit should be between 1 and 10."
            # if not (alert_generation_time - threshold_for_golden_period <= args.end_time <= current_time):
            # lint_message += f"Invalid end time. End time should be between {alert_generation_time - threshold_for_golden_period} and {current_time}."
            if args.service not in services:
                lint_message += f"{args.service} is an Invalid service name, Valid service names are {services}."
            if args.operation not in operations and args.operation is not None:
                lint_message += f"Invalid operation, Valid operations are {operations} or None to use all operations."

            if lint_message:
                return lint_message
            else:
                return arguments

        except ValidationError as e:
            return f"Argument validation error: {e}"
        except ValueError as e:
            return f"Invalid Jaeger Query: {e}"
        except Exception as e:
            return f"An error occurred: {e}"
