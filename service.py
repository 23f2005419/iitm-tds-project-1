import subprocess
import glob
import sqlite3, requests
import json
import os
from dateutil import parser
from pathlib import Path
import itertools
import numpy as np
from typing import List, Optional
from sklearn.metrics.pairwise import cosine_similarity
import base64, re

AIPROXY_TOKEN = os.getenv("AIPROXY_TOKEN")


def path_verify(path: str, input_file: bool):
    if os.path.exists(path):
        return Path(path).resolve()
    elif input_file:
        raise FileNotFoundError("File not found")
    else:
        return Path(path).resolve()


def create_openai_url_request_specfictask(user_input: str, task: str):
    print("Inside Specific task")
    url = "https://aiproxy.sanand.workers.dev/openai/v1/chat/completions"
    response = requests.post(
        url=url,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {AIPROXY_TOKEN}",
        },
        json={
            "model": "gpt-4o-mini",
            "messages": [
                {
                    "role": "system",
                    "content": "DO ONLY WHAT IS ASKED\n YOUR output is part of a program, using tool functions "
                    + task,
                },
                {"role": "user", "content": user_input},
            ],
        },
    )
    return response.json()


def fetch_text_embeddings(texts: List[str]):
    print("Inside fetching text embeddings...")
    url = "https://aiproxy.sanand.workers.dev/openai/v1/embeddings"
    headers = {"Authorization": f"Bearer {AIPROXY_TOKEN}"}
    data = {"model": "text-embedding-3-small", "input": texts}
    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()

        data = response.json().get("data")
        print(len(data))
        embeddings = np.array([each["embedding"] for each in data])
        return embeddings
    except requests.RequestException as e:
        print(f"An error occurred in embedding: {e}")
        raise Exception(e)


def rewrite_task(task: str):
    task_lower = task.lower()
    rewrite_map = {
        "credit card": "longest numerical sequence",
        "cvv": "3-digit number near another number",
        "bank account": "second longest numerical sequence",
        "routing number": "a series of numbers used for banking",
        "password": "text following 'Password:'",
        "ip address": "numbers which having . in between",
    }
    for keyword, replacement in rewrite_map.items():
        if keyword in task_lower:
            return re.sub(keyword, replacement, task, flags=re.IGNORECASE)
    return task


def fetch_text_from_image(image_path: str, task: str):
    print("Inside the fetch text from image....")
    print(image_path)
    image_format = image_path.split(".")[-1]
    print(image_format)
    clean_task = rewrite_task(task)
    with open(image_path, "rb") as file:
        base64_image = base64.b64encode(file.read()).decode("utf-8")

    response = requests.post(
        url="https://aiproxy.sanand.workers.dev/openai/v1/chat/completions",
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {AIPROXY_TOKEN}",
        },
        json={
            "model": "gpt-4o-mini",
            "messages": [
                {
                    "role": "system",
                    "content": "Given the image extract the data what is asked by the user. Make the output as short as possible, one word if possible.",
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": f"Extract {clean_task} from the image",
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/{image_format};base64,{base64_image}"
                            },
                        },
                    ],
                },
            ],
        },
    )
    response.raise_for_status()
    return response.json()


def a1_run_script_with_url(package: str, script_url: str, args: list):
    try:
        print("Inside script run")
        package_installed = False
        script_ran = False
        if package:
            if package == "uvicorn":
                subprocess.run(["pip", "install", "uv"])
            else:
                subprocess.run(["pip", "install", package])
            package_installed = True

        if script_url and args:
            command_prompt = ["uv", "run", script_url, args[0]]
            print("-" * 100)
            response = subprocess.run(
                command_prompt, cwd=os.getcwd(), capture_output=True, text=True
            )
            if response.stdout:
                print("Sysout ", response.stdout)
                script_ran = True
            else:
                raise Exception(response.stderr)
        return {"Package Installed": package_installed, "Script_ran": script_ran}
    except Exception as e:
        print("Error Occured due to ", e)
        raise Exception(e)


def a2_format_with_prettier(file_path: str, prettier_version: str):
    if file_path and os.path.exists(file_path):
        print("Path exisit - will perform prettier")
        input_file = path_verify(file_path, True)
        print(input_file)
        install_prettier = subprocess.run(["curl", "npm","install","-g",f"prettier@{prettier_version}"],shell=True)
        print(install_prettier)
        response = subprocess.run(
            ["npx", f"prettier@{prettier_version}", "--write", input_file],
            capture_output=True,
            text=True,
            shell=True
        )
        if response.stdout:
            return response.stdout
        else:
            return response.stderr
    else:
        raise FileNotFoundError("File Not Found")


def a3_count_weekdays_in_document(source_path: str, weekday: str, dest_path: str):
    weekday = weekday.lower()
    print("Inside weekday func")
    days_mapping = {
        "sunday": 6,
        "monday": 0,
        "tuesday": 1,
        "wednesday": 2,
        "thursday": 3,
        "friday": 4,
        "saturday": 5,
    }

    if weekday not in days_mapping:
        pass

    day_index = days_mapping[weekday]
    with open(source_path, "r") as file:
        dates = file.readlines()

    count = sum(
        1 for date in dates if parser.parse(date.strip()).weekday() == day_index
    )
    output_file = dest_path

    with open(output_file, "w") as file:
        file.write(str(count))
    return f"Counted {count} {weekday}s and wrote to {output_file}."


def a4_json_sort(source_path: str, dest_path: str, keys: list):
    print(source_path, dest_path, keys)
    input_file = path_verify(source_path, True)
    output_file = path_verify(dest_path, False)
    try:
        with open(input_file, "r") as file:
            data = json.load(file)
        print("Sort the data")
        sorted_data = sorted(data, key=lambda x: tuple(x[key] for key in keys))
        with open(output_file, "w") as file:
            json.dump(sorted_data, file)
        return "Successfuly sorted the given file and written in the specified location"
    except Exception as e:
        print("File error", e)
        raise Exception(e)


def a5_process_and_write_logfiles(
    source_path: str, dest_path: str, logs_files: int = 10, num_of_lines: int = 1
):
    print("Inside processing log files")
    input_file = path_verify(source_path, True)
    output_file = path_verify(dest_path, False)
    log_files = glob.glob(os.path.join(input_file, "*.log"))
    if not log_files:
        print("No log files found in the specified directory.")
        raise FileNotFoundError("Log Files not found")

    log_files.sort(key=os.path.getmtime, reverse=True)
    recent_logs = log_files[:logs_files]

    with open(output_file, "w") as outfile:
        for log_file in recent_logs:
            with open(log_file, "r") as infile:
                lines = itertools.islice(infile, num_of_lines)
                outfile.writelines(lines)

    print(f"Processed and wrote logs to {output_file}")
    return "Successfully processed log files and Written to the specified file"


def a6_create_index_from_files(
    source_path: str, dest_path: str, extension: str, content_marker: str
):
    try:
        input_dir = path_verify(source_path, True)
        output_file = path_verify(dest_path, False)

        files = glob.glob(
            os.path.join(input_dir, "**", f"*{extension}"), recursive=True
        )

        index = {}
        for ext_file in files:
            title = None
            with open(ext_file, "r", encoding="utf-8") as file:
                for line in file:
                    if line.startswith(content_marker):
                        title = line.lstrip(content_marker).strip()
                        break
            relative_path = os.path.relpath(ext_file, input_dir)
            index[relative_path] = title if title else ""

        with open(output_file, "w", encoding="utf-8") as json_file:
            json.dump(index, json_file, indent=2, sort_keys=True)

        print(f"Index created and written to {output_file}")
        return "Successfully creaded the Index and written to the file."
    except Exception as e:
        print("Exception is ", e)
        raise Exception(e)


def a7_text_extraction(source_path: str, dest_path: str, task: str):
    try:
        input_file = path_verify(source_path, True)
        print("input file ", input_file)
        with open(input_file, "r") as file:
            print("Inside the read input file")
            text_info = file.read()
        response = create_openai_url_request_specfictask(text_info, task)
        print("Response for specific task ", response)
        output_file = path_verify(dest_path, False)
        print("output file", output_file)
        with open(output_file, "w") as file:
            file.write(response["choices"][0]["message"]["content"])
        return "Success, File created"
    except Exception as e:
        print("Exception is ", e)
        raise Exception(e)


def a8_extract_text_from_image(source_path: str, dest_path: str, task: str):
    try:
        if os.path.exists(source_path):
            response = fetch_text_from_image(source_path, task)
        else:
            raise FileNotFoundError("File Not Found")

        output_file = path_verify(dest_path, False)
        print(response["choices"][0]["message"])
        with open(output_file, "w") as file:
            file.write(response["choices"][0]["message"]["content"].replace(" ", ""))
        return "Successfuly extracted the data from the image and written in the file."
    except Exception as e:
        print("Exception ", e)
        raise Exception(e)


def a9_find_similar_texts(source_path: str, dest_path: str):
    input_file = path_verify(source_path, True)
    output_file = path_verify(dest_path, False)

    try:
        with open(input_file, "r") as file:
            documents = file.readlines()

        documents = [comment.strip() for comment in documents]

        line_embeddings = fetch_text_embeddings(documents)
        similarity_matrix = cosine_similarity(line_embeddings)

        np.fill_diagonal(similarity_matrix, -1)
        most_similar_indices = np.unravel_index(
            np.argmax(similarity_matrix), similarity_matrix.shape
        )

        print("most similarities ", most_similar_indices)
        similar_texts = []
        for i in range(len(most_similar_indices)):
            similar_texts.append(documents[most_similar_indices[i]])

        with open(output_file, "w") as file:
            for text in similar_texts:
                file.write(text + "\n")

        print(f"Similar texts written to {output_file}")
        return "Successfully found the similarities."
    except Exception as e:
        print(f"An error occurred: {e}")
        raise Exception(e)


def a10_execute_query_and_write_result(
    source_path: str, dest_path: str, query: str, query_params: list
):
    db_file = path_verify(source_path, True)
    output_file = path_verify(dest_path, False)

    try:
        with sqlite3.connect(db_file) as conn:
            cursor = conn.cursor()
            cursor.execute(query, query_params)
            result = cursor.fetchone()

            if result:
                output_data = result[0]
            else:
                output_data = "Data Not Found in the specified in database file."

            with open(output_file, "w") as file:
                file.write(str(output_data))
            return "Successfully Written the records in the file."
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
