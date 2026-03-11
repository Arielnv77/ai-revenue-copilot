"""
Query Engine — Translates natural-language questions into pandas operations via LLM.
"""

import ast
import logging
import re
import threading
from typing import Any, Optional

import pandas as pd

from src.nlp.prompts import QUERY_TEMPLATE, SYSTEM_PROMPT

logger = logging.getLogger(__name__)


class QueryEngine:
    """
    Natural language query engine that uses an LLM to answer
    questions about a pandas DataFrame.
    """

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key
        self._client = None
        self._df: Optional[pd.DataFrame] = None
        self._context: str = ""

    def load_data(self, df: pd.DataFrame) -> None:
        """Load a DataFrame for querying."""
        self._df = df
        self._context = self._build_context(df)
        logger.info(f"Query engine loaded data: {df.shape}")

    def ask(self, question: str) -> dict[str, Any]:
        """
        Ask a natural-language question about the loaded data.

        Args:
            question: User's question in natural language.

        Returns:
            Dict with: answer, code, chart_data (optional).
        """
        if self._df is None:
            raise RuntimeError("No data loaded. Call load_data() first.")

        # Build the prompt
        system = SYSTEM_PROMPT.format(
            columns=list(self._df.columns),
            dtypes=self._df.dtypes.to_dict(),
            sample=self._df.head(3).to_string(),
        )
        user_msg = QUERY_TEMPLATE.format(question=question)

        # Call the LLM
        response = self._call_llm(system, user_msg)

        # Parse the response
        result = self._parse_response(response)

        # Try to execute the code safely
        if result.get("code"):
            try:
                exec_result = self._safe_execute(result["code"])
                result["execution_result"] = str(exec_result)
            except Exception as e:
                result["execution_error"] = str(e)
                logger.warning(f"Code execution failed: {e}")

        logger.info(f"Query answered: {question[:50]}...")
        return result

    def _call_llm(self, system: str, user_message: str) -> str:
        """Call the OpenAI API."""
        try:
            from openai import OpenAI

            if self._client is None:
                self._client = OpenAI(api_key=self.api_key)

            response = self._client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": system},
                    {"role": "user", "content": user_message},
                ],
                temperature=0.2,
                max_tokens=1000,
            )
            return response.choices[0].message.content or ""

        except ImportError:
            logger.error("OpenAI package not installed")
            return "Error: OpenAI package not available. Install with: pip install openai"
        except Exception as e:
            logger.error(f"LLM call failed: {e}")
            return f"Error calling LLM: {e}"

    def _parse_response(self, response: str) -> dict[str, Any]:
        """Parse the LLM response into structured output."""
        result = {
            "raw_response": response,
            "answer": "",
            "code": "",
            "insight": "",
        }

        # Extract code block
        code_match = re.search(r"```python\s*(.*?)\s*```", response, re.DOTALL)
        if code_match:
            result["code"] = code_match.group(1).strip()

        # Extract answer
        answer_match = re.search(r"\*\*Answer:\*\*\s*(.*?)(?:\*\*|$)", response, re.DOTALL)
        if answer_match:
            result["answer"] = answer_match.group(1).strip()
        else:
            # Fallback: use the whole response minus code blocks
            answer = re.sub(r"```.*?```", "", response, flags=re.DOTALL).strip()
            result["answer"] = answer

        # Extract insight
        insight_match = re.search(r"\*\*Insight:\*\*\s*(.*?)$", response, re.DOTALL)
        if insight_match:
            result["insight"] = insight_match.group(1).strip()

        return result

    def _safe_execute(self, code: str) -> Any:
        """
        Safely execute pandas code on the loaded DataFrame.

        Validates via AST before execution (more robust than string matching)
        and enforces a 10-second timeout via a daemon thread.
        """
        # --- AST validation ---
        try:
            tree = ast.parse(code, mode="exec")
        except SyntaxError as e:
            raise ValueError(f"Invalid Python syntax: {e}") from e

        _BLOCKED_NODES = (
            ast.Import,
            ast.ImportFrom,
            ast.FunctionDef,
            ast.AsyncFunctionDef,
            ast.ClassDef,
            ast.Delete,
            ast.Global,
            ast.Nonlocal,
        )
        _BLOCKED_ATTRS = {
            "to_csv", "to_pickle", "to_sql", "to_parquet", "to_excel",
            "to_feather", "to_hdf", "to_json",
            "__class__", "__subclasses__", "__globals__", "__builtins__",
        }

        for node in ast.walk(tree):
            if isinstance(node, _BLOCKED_NODES):
                raise ValueError(f"Blocked statement type: {type(node).__name__}")
            if isinstance(node, ast.Attribute) and node.attr in _BLOCKED_ATTRS:
                raise ValueError(f"Blocked attribute access: .{node.attr}")

        # --- Timeout execution ---
        namespace: dict[str, Any] = {"df": self._df.copy(), "pd": pd}
        container: dict[str, Any] = {}

        def _run() -> None:
            exec(code, {"__builtins__": {}}, namespace)  # noqa: S102
            container["value"] = namespace.get("result", "Code executed successfully")

        thread = threading.Thread(target=_run, daemon=True)
        thread.start()
        thread.join(timeout=10)

        if thread.is_alive():
            raise TimeoutError("Code execution exceeded 10-second limit")
        if "value" not in container:
            raise RuntimeError("Execution produced no result")

        return container["value"]

    def _build_context(self, df: pd.DataFrame) -> str:
        """Build context string for the LLM."""
        return (
            f"Shape: {df.shape}\n"
            f"Columns: {list(df.columns)}\n"
            f"Types: {df.dtypes.to_dict()}\n"
            f"Sample:\n{df.head(3).to_string()}"
        )
