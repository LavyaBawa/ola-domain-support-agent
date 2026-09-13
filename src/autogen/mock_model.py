import json
from collections.abc import AsyncGenerator, Sequence
from typing import Any

from autogen_core import CancellationToken
from autogen_core.models import (
    ChatCompletionClient,
    CreateResult,
    ModelInfo,
    RequestUsage,
)


class MockAutoGenModel(ChatCompletionClient):

    def __init__(self):
        super().__init__()

    async def create(
        self,
        messages: Sequence[Any],
        *,
        tools=(),
        tool_choice="auto",
        json_output=None,
        extra_create_args=None,
        cancellation_token: CancellationToken | None = None,
    ) -> CreateResult:

        message_text = " ".join(str(message) for message in messages).lower()

        if json_output is not None:
            if "guaranteed a refund" in message_text:
                response_text = json.dumps({
                    "decision": "REVISE",
                    "final_response": (
                        "Critical tickets should receive an initial "
                        "response within 1 hour."
                    ),
                    "reason": (
                        "The refund claim is not supported by the "
                        "supplied context."
                    ),
                })
            else:
                response_text = json.dumps({
                    "decision": "APPROVE",
                    "final_response": (
                        "Critical tickets should receive an initial "
                        "response within 1 hour."
                    ),
                    "reason": (
                        "The draft is supported by the supplied context."
                    ),
                })
        else:
            if "guaranteed a refund" in message_text:
                response_text = (
                    "REVISE: The draft contains an unsupported "
                    "guaranteed refund claim."
                )
            else:
                response_text = (
                    "APPROVE: The draft is supported by the supplied context."
                )

        return CreateResult(
            finish_reason="stop",
            content=response_text,
            usage=RequestUsage(
                prompt_tokens=self.count_tokens(messages),
                completion_tokens=max(1, len(response_text) // 4),
            ),
            cached=False,
        )

    async def create_stream(
        self,
        messages: Sequence[Any],
        *,
        tools=(),
        tool_choice="auto",
        json_output=None,
        extra_create_args=None,
        cancellation_token: CancellationToken | None = None,
    ) -> AsyncGenerator[str | CreateResult, None]:

        result = await self.create(
            messages,
            tools=tools,
            tool_choice=tool_choice,
            json_output=json_output,
            extra_create_args=extra_create_args,
            cancellation_token=cancellation_token,
        )

        yield result.content

        yield result

    async def close(self) -> None:
        return None

    def actual_usage(self) -> RequestUsage:
        return RequestUsage(
            prompt_tokens=0,
            completion_tokens=0,
        )

    def total_usage(self) -> RequestUsage:
        return RequestUsage(
            prompt_tokens=0,
            completion_tokens=0,
        )

    def count_tokens(
        self,
        messages: Sequence[Any],
        *,
        tools=(),
    ) -> int:

        text = " ".join(str(message) for message in messages)

        return max(1, len(text) // 4)

    def remaining_tokens(
        self,
        messages: Sequence[Any],
        *,
        tools=(),
    ) -> int:

        return max(
            0,
            4096 - self.count_tokens(messages),
        )

    @property
    def capabilities(self) -> ModelInfo:
        return ModelInfo(
            vision=False,
            function_calling=False,
            json_output=True,
            family="unknown",
            structured_output=True,
            multiple_system_messages=False,
        )

    @property
    def model_info(self) -> ModelInfo:
        return ModelInfo(
            vision=False,
            function_calling=False,
            json_output=True,
            family="unknown",
            structured_output=True,
            multiple_system_messages=False,
        )
