"""
Query Engine — Translates natural-language questions into pandas operations via LLM.

Supports two providers:
  - "openai" : GPT-4o-mini  (requires OPENAI_API_KEY)
  - "groq"   : llama-3.1-70b-versatile (requires GROQ_API_KEY, groq package)
"""

import ast
import logging
import re
import threading
from typing import Any, Literal, Optional

import pandas as pd

from src.nlp.prompts import QUERY_TEMPLATE, SYSTEM_PROMPT

logger = logging.getLogger(__name__)

Provider = Literal["openai", "groq"]


class QueryEngine:
    """
    Natural language query engine that uses an LLM to answer
    questions about a pandas DataFrame.

    Args:
        api_key:  API key for the chosen provider.
        provider: "openai" (default) or "groq".
    """

    # Default models per provider
    _MODELS: dict[str, str] = {
        "openai": "gpt-4o-mini",
        "groq":   "llama-3.3-70b-versatile",
    }
    _GROQ_FALLBACK_MODELS: tuple[str, ...] = (
        "llama-3.3-70b-versatile",
        "llama-3.1-8b-instant",
    )

    def __init__(
        self,
        api_key: Optional[str] = None,
        provider: Provider = "openai",
    ):
        self.api_key  = api_key
        self.provider = provider
        self._client  = None
        self._df: Optional[pd.DataFrame] = None
        self._context: str = ""

    # ──────────────────────────────────────────────────────────────────────────
    # Public interface
    # ──────────────────────────────────────────────────────────────────────────
    def load_data(self, df: pd.DataFrame) -> None:
        """Load a DataFrame for querying."""
        self._df = df
        self._context = self._build_context(df)
        logger.info("Query engine loaded data: %s  provider=%s", df.shape, self.provider)

    def ask(self, question: str) -> dict[str, Any]:
        """
        Ask a natural-language question about the loaded data.

        Returns:
            Dict with: answer, code, insight, execution_result (optional).
        """
        if self._df is None:
            raise RuntimeError("No data loaded. Call load_data() first.")

        system  = SYSTEM_PROMPT.format(
            columns=list(self._df.columns),
            dtypes=self._df.dtypes.to_dict(),
            sample=self._df.head(3).to_string(),
        )
        user_msg = QUERY_TEMPLATE.format(question=question)
        response = self._call_llm(system, user_msg)
        result   = self._parse_response(response)

        if result.get("code"):
            try:
                exec_result = self._safe_execute(result["code"])
                result["execution_result"] = str(exec_result)
                # Inject actual value into the answer text
                result["answer"] = self._inject_result(result["answer"], exec_result)
            except Exception as e:
                result["execution_error"] = str(e)
                logger.warning("Code execution failed: %s", e)

        logger.info("Query answered: %s…", question[:50])
        return result

    # ──────────────────────────────────────────────────────────────────────────
    # Provider dispatch
    # ──────────────────────────────────────────────────────────────────────────
    def _call_llm(self, system: str, user_message: str) -> str:
        """Dispatch to the selected LLM provider."""
        if self.provider == "groq":
            return self._call_groq(system, user_message)
        return self._call_openai(system, user_message)

    def _call_openai(self, system: str, user_message: str) -> str:
        """Call the OpenAI API (gpt-4o-mini)."""
        try:
            from openai import OpenAI

            if self._client is None:
                self._client = OpenAI(api_key=self.api_key)

            response = self._client.chat.completions.create(
                model=self._MODELS["openai"],
                messages=[
                    {"role": "system",  "content": system},
                    {"role": "user",    "content": user_message},
                ],
                temperature=0.2,
                max_tokens=1000,
            )
            return response.choices[0].message.content or ""

        except ImportError:
            logger.error("openai package not installed")
            return "Error: openai package not available. Run: pip install openai"
        except Exception as e:
            logger.error("OpenAI call failed: %s", e)
            return f"Error calling OpenAI: {e}"

    def _call_groq(self, system: str, user_message: str) -> str:
        """Call the Groq API (llama-3.1-70b-versatile).

        Groq's Python client follows the same OpenAI-compatible interface,
        so we only change the base_url and model name.
        """
        try:
            from groq import Groq  # type: ignore[import-untyped]

            if self._client is None:
                self._client = Groq(api_key=self.api_key)

            last_error: Exception | None = None
            for model_name in self._GROQ_FALLBACK_MODELS:
                try:
                    response = self._client.chat.completions.create(
                        model=model_name,
                        messages=[
                            {"role": "system",  "content": system},
                            {"role": "user",    "content": user_message},
                        ],
                        temperature=0.2,
                        max_tokens=1000,
                    )
                    return response.choices[0].message.content or ""
                except Exception as model_error:
                    last_error = model_error
                    logger.warning("Groq model '%s' failed: %s", model_name, model_error)
                    continue

            raise RuntimeError(f"All Groq fallback models failed: {last_error}")

        except ImportError:
            logger.error("groq package not installed")
            return "Error: groq package not available. Run: pip install groq"
        except Exception as e:
            logger.error("Groq call failed: %s", e)
            return f"Error calling Groq: {e}"

    # ──────────────────────────────────────────────────────────────────────────
    # Response parsing
    # ──────────────────────────────────────────────────────────────────────────
    def _parse_response(self, response: str) -> dict[str, Any]:
        """Parse the LLM response into structured output."""
        result: dict[str, Any] = {
            "raw_response": response,
            "answer": "",
            "code":   "",
            "insight": "",
        }

        code_match = re.search(r"```python\s*(.*?)\s*```", response, re.DOTALL)
        if code_match:
            result["code"] = code_match.group(1).strip()

        answer_match = re.search(r"\*\*Answer:\*\*\s*(.*?)(?:\*\*|$)", response, re.DOTALL)
        if answer_match:
            result["answer"] = answer_match.group(1).strip()
        else:
            result["answer"] = re.sub(r"```.*?```", "", response, flags=re.DOTALL).strip()

        insight_match = re.search(r"\*\*Insight:\*\*\s*(.*?)$", response, re.DOTALL)
        if insight_match:
            result["insight"] = insight_match.group(1).strip()

        return result

    # ──────────────────────────────────────────────────────────────────────────
    # Safe execution sandbox
    # ──────────────────────────────────────────────────────────────────────────
    def _safe_execute(self, code: str) -> Any:
        """
        Safely execute pandas code on the loaded DataFrame.

        Validates via AST (blocks imports, deletes, class defs, etc.) then
        executes in a sandboxed namespace with a 10-second daemon-thread timeout.
        """
        try:
            tree = ast.parse(code, mode="exec")
        except SyntaxError as e:
            raise ValueError(f"Invalid Python syntax: {e}") from e

        _BLOCKED_NODES = (
            ast.Import, ast.ImportFrom, ast.FunctionDef,
            ast.AsyncFunctionDef, ast.ClassDef, ast.Delete,
            ast.Global, ast.Nonlocal,
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

    # ──────────────────────────────────────────────────────────────────────────
    # Result injection
    # ──────────────────────────────────────────────────────────────────────────
    def _format_value(self, value: Any) -> str:
        """Format an execution result as a human-readable string."""
        if value is None:
            return "N/A"
        if isinstance(value, float):
            return f"{value:,.2f}"
        if isinstance(value, (int,)):
            return f"{value:,}"
        if isinstance(value, pd.DataFrame):
            if len(value) <= 15:
                return f"\n{value.to_string()}"
            return f"\n{value.head(10).to_string()}\n… ({len(value)} rows)"
        if isinstance(value, pd.Series):
            if len(value) <= 15:
                return f"\n{value.to_string()}"
            return f"\n{value.head(10).to_string()}\n… ({len(value)} items)"
        return str(value)

    def _inject_result(self, answer: str, exec_result: Any) -> str:
        """Replace [RESULT] placeholder and fallback phrases with the actual value."""
        formatted = self._format_value(exec_result)

        # Primary: explicit [RESULT] placeholder the prompt tells the model to use
        if "[RESULT]" in answer:
            return answer.replace("[RESULT]", f"**{formatted}**")

        # Fallback: replace common placeholder phrases the model might use anyway
        _PLACEHOLDER_PATTERNS = [
            r"the result of the above code",
            r"the result of the code above",
            r"the result of the code",
            r"the code above",
            r"the above code",
            r"the result above",
            r"approximately the result",
            r"as calculated above",
            r"as computed above",
            r"shown in the code",
            r"computed by the code",
            r"the calculated value",
            r"the computed value",
        ]
        import re as _re
        result = answer
        for pat in _PLACEHOLDER_PATTERNS:
            new = _re.sub(pat, f"**{formatted}**", result, flags=_re.IGNORECASE)
            if new != result:
                result = new
                break  # only replace the first match

        # Last resort: if no replacement happened AND the value isn't already
        # visible in the answer, append it
        if result == answer and exec_result is not None:
            # Don't append if value is already clearly present
            if str(exec_result) not in answer and formatted.strip() not in answer:
                trimmed = answer.rstrip(". ")
                if formatted.startswith("\n"):
                    result = trimmed + ":\n" + formatted.strip()
                else:
                    result = trimmed + f": **{formatted}**."

        return result

    # ──────────────────────────────────────────────────────────────────────────
    def _build_context(self, df: pd.DataFrame) -> str:
        return (
            f"Shape: {df.shape}\n"
            f"Columns: {list(df.columns)}\n"
            f"Types: {df.dtypes.to_dict()}\n"
            f"Sample:\n{df.head(3).to_string()}"
        )
