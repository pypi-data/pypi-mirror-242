from abc import ABC, abstractmethod
from typing import Any, Dict, List, Union

from playwright.async_api import BrowserContext

from bananalyzer.data.schemas import Example

AgentResult = Union[Dict[str, Any], List[Dict[str, Any]], str]


class AgentRunner(ABC):
    """
    Wrapper class clients must implement to run an agent against the evaluations
    """

    @abstractmethod
    async def run(
        self,
        browser_context: BrowserContext,
        eval_context: Example,
    ) -> AgentResult:
        pass
