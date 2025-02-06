from promformat import format_query
import ast


class LogQLLinter:
    def __init__(self):
        pass

    @staticmethod
    def lint(query) -> str:
        if '|=' in query['query']:
            body = query['query'].split('|=')[0].strip()
        else:
            body = query['query']
        try:
            format_query(body)
            return query
        except ValueError as e:
            return f"Invalid LogQL Query {body}: {e}"
        except Exception as e:
            return f"An error occurred {body}: {e}"