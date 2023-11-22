import argparse
from abc import ABC
from http import HTTPStatus
from typing import Set, List, Optional

import uvicorn
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from sentence_transformers import SentenceTransformer
from starlette.responses import JSONResponse
from transformers import PreTrainedTokenizerFast, PreTrainedTokenizer

from bixi.api.protocol import EmbeddingsRequest, EmbeddingsResponse, UsageInfo, ErrorResponse, ChatCompletionRequest, \
    CompletionRequest

app = FastAPI()


async def check_model(
        request: [ChatCompletionRequest, CompletionRequest],
        model_names: set) -> Optional[JSONResponse]:
    if request.model in model_names:
        return
    ret = create_error_response(
        HTTPStatus.NOT_FOUND,
        f"The model `{request.model}` does not exist.",
    )
    return ret


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):  # pylint: disable=unused-argument
    return create_error_response(HTTPStatus.BAD_REQUEST, str(exc))


def create_error_response(
        status_code: HTTPStatus,
        message: str) -> JSONResponse:
    return JSONResponse(
        ErrorResponse(
            message=message,
            code=status_code.value
        )
        .dict(),
        status_code=status_code.value)

class EmbeddingModelWorker(ABC):
    def __init__(
            self,
            model_names: Set[str],
            limit_worker_concurrency: int,
            executor: SentenceTransformer,
            tokenizer: [PreTrainedTokenizerFast, PreTrainedTokenizer]
    ):
        self.model_names = model_names
        self.limit_worker_concurrency = limit_worker_concurrency
        self.executor = executor
        self.tokenizer = tokenizer

    async def encode(self, inputs: List[str], batch_size: Optional[int] = 128):
        return self.executor.encode(
            sentences=inputs,
            normalize_embeddings=True,
            batch_size=batch_size
        )

    async def decode(self, inputs: List[List[int]]):
        pass


@app.post("/v1/embeddings")
async def create_embeddings(request: EmbeddingsRequest):
    error_check_ret = await check_model(request, worker.model_names)
    if error_check_ret is not None:
        return error_check_ret

    inputs = []
    if isinstance(request.input, str):
        inputs.append(request.input)
    else:
        inputs += request.input
    token_number = 0
    for input_str in inputs:
        input_id = worker.tokenizer.encode(input_str)
        token_number += len(input_id)
    result = await worker.encode(request.input, request.batch_size)
    data = []
    for index, value in enumerate(result):
        value_list = value.tolist()
        data.append(
            {
                "object": "embedding",
                "embedding": value_list,
                "index": index,
            }
        )
    usage = UsageInfo(
        prompt_tokens=token_number,
        total_tokens=token_number,
    )

    return EmbeddingsResponse(
        data=data,
        model=request.model,
        usage=usage
    )

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", type=str, default="0.0.0.0")
    parser.add_argument("--port", type=int, default=8000)
    parser.add_argument("--model-path", type=str, default="/workspace/models/bge-large-en-v1.5")
    parser.add_argument(
        "--model-names",
        type=lambda s: s.split(","),
        default="text-embedding-ada-002, bge-large-en",
        help="Optional display comma separated names",
    )
    parser.add_argument("--limit-worker-concurrency", type=int, default=1024)
    parser.add_argument("--num-gpus", type=int, default=1)
    parser.add_argument("--trust_remote_code", type=bool, default=True)

    args = parser.parse_args()
    model = SentenceTransformer(args.model_path)
    worker = EmbeddingModelWorker(
        model_names=set(args.model_names),
        limit_worker_concurrency=args.limit_worker_concurrency,
        executor=model,
        tokenizer=model.tokenizer
    )
    uvicorn.run(app, host=args.host, port=args.port, log_level="info")
