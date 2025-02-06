from promformat import format_query


class PromQLLinter:
    def __init__(self):
        pass

    @staticmethod
    def lint(query: str) -> str:
        try:
            format_query(query)
            return query
        except ValueError as e:
            return f"Invalid PromQL Query: {e}"
        except Exception as e:
            return f"An error occurred: {e}"