# /// script
# requires-python = ">=3.12"
# dependencies = [
#    "fastapi",
#    "uvicorn",
#    "requests",
#    "python-dateutil",
#   "scikit-learn",
#    "numpy",
# ]
# ///

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse
import os, requests, json
from service import *
from tool_call_function import *
from typing import Dict, Callable

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
AIPROXY_TOKEN = os.getenv("AIPROXY_TOKEN")


def create_openai_url_request(task: str):
    url = "https://aiproxy.sanand.workers.dev/openai/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {AIPROXY_TOKEN}",
    }
    tools_fucntion_call = [
        run_script_func_def,
        formart_func_def,
        count_no_days_func_def,
        json_sort_func_def,
        text_extraction_func_def,
        process_and_write_logfiles_func_def,
        execute_query_and_write_result_func_def,
        create_index_from_files_func_def,
        extract_text_from_image,
        find_similar_texts_func_def,
    ]
    data = {
        "model": "gpt-4o-mini",
        "messages": [
            {
                "role": "system",
                "content": """You are an assistant who has to do a variety of task.
                If your task involves running a script, you can use the script_runner tool.
                If your task involves writing a code, you can use the task_runner tool.
                """,
            },
            {"role": "user", "content": task},
        ],
        "tools": tools_fucntion_call,
        "tool_choice": "auto",
    }
    response = requests.post(url=url, headers=headers, json=data)
    return response


function_to_Callable_map: Dict[str, Callable] = {
    "a1_run_script_with_url": a1_run_script_with_url,
    "a2_format_with_prettier": a2_format_with_prettier,
    "a3_count_weekdays_in_document": a3_count_weekdays_in_document,
    "a4_json_sort": a4_json_sort,
    "a5_process_and_write_logfiles": a5_process_and_write_logfiles,
    "a6_create_index_from_files": a6_create_index_from_files,
    "a7_text_extraction": a7_text_extraction,
    "a8_extract_text_from_image": a8_extract_text_from_image,
    "a9_find_similar_texts": a9_find_similar_texts,
    "a10_execute_query_and_write_result": a10_execute_query_and_write_result,
}


@app.get("/")
async def basic():
    return "Checking Basic Connectivity", 200


@app.get("/read", response_class=PlainTextResponse)
async def read_file(path: str):
    if not path or (not os.path.exists(path)):
        raise HTTPException(status_code=404, detail="File not found")
    path = path_verify(path, True)
    with open(path, "r") as file:
        content = file.read()
    return content


@app.post("/run")
async def run_task(task: str):
    if not task:
        raise HTTPException(status_code=400, detail="Task description is required")

    try:
        print("Inside the Post method")
        response = create_openai_url_request(task)
        print("Status code : ", response.status_code)
        if response.status_code == 200:
            print(response.json())
            message = response.json()["choices"][0]["message"]
            if message["tool_calls"]:
                for tool in message["tool_calls"]:
                    print("Inside loop ", tool.keys(), type(tool))
                    function = tool.get("function")
                    print(function)
                    function_name = function.get("name")
                    function_args = function.get("arguments")
                    if function_to_call := function_to_Callable_map.get(function_name):
                        print("Calling function:", function_name)
                        print("Arguments:", function_args)
                        tool_function_arguments = json.loads(function_args)
                        method_response = function_to_call(**tool_function_arguments)
                        print("Function output:", method_response)
                        return {
                            "status_code": 200,
                            "message": "Task executed Successfully",
                            "Method_Output": method_response,
                            "json": response.json(),
                        }
                    else:
                        print("Function", function_name, "not found")
        else:
            raise HTTPException(
                status_code=response.status_code, detail=response.json()
            )

    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
