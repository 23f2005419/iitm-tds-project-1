run_script_func_def = {
    "type": "function",
    "function": {
        "name": "a1_run_script_with_url",
        "description": "Install a package if required and run a script from a url with provided arguments",
        "parameters": {
            "type": "object",
            "properties": {
                "package": {
                    "type": "string",
                    "description": "The name of the package to install.",
                },
                "script_url": {
                    "type": "string",
                    "description": "The URL for which script to run.",
                },
                "args": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "List of arguments to pass to the script.",
                },
            },
            "required": ["package", "script_url", "args"],
            "additionalProperties": False,
        },
        "strict": True,
    },
}

formart_func_def = {
    "type": "function",
    "function": {
        "name": "a2_format_with_prettier",
        "description": "Format a file using Prettier with the given prettier version.",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "The path to the file which needs to be formatted.",
                },
                "prettier_version": {
                    "type": "string",
                    "description": "The version of Prettier to use.",
                },
            },
            "required": ["file_path", "prettier_version"],
            "additionalProperties": False,
        },
        "strict": True,
    },
}

count_no_days_func_def = {
    "type": "function",
    "function": {
        "name": "a3_count_weekdays_in_document",
        "description": "Count the occuerrence of the given weekday in the given file and write its output in the destination file.",
        "parameters": {
            "type": "object",
            "properties": {
                "source_path": {
                    "type": "string",
                    "description": "The path to the file which is to be used for counting.",
                },
                "weekday": {
                    "type": "string",
                    "description": "The day which needs to be counted in the document. (e.g., Wednesday)",
                },
                "dest_path": {
                    "type": "string",
                    "description": "The path of the file to which the results to be stored.",
                },
            },
            "required": ["source_path", "weekday", "dest_path"],
            "additionalProperties": False,
        },
        "strict": True,
    },
}

json_sort_func_def = {
    "type": "function",
    "function": {
        "name": "a4_json_sort",
        "description": "This function sort the json with the given key values. It may be more than one",
        "parameters": {
            "type": "object",
            "properties": {
                "source_path": {
                    "type": "string",
                    "description": "The path to the json file which is need to be sorted",
                },
                "dest_path": {
                    "type": "string",
                    "description": "The path of the file to which the results to be stored.",
                },
                "keys": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "List of keys in which the sorting to be taken care.",
                },
            },
            "required": ["source_path", "dest_path", "keys"],
            "additionalProperties": False,
        },
        "strict": True,
    },
}

process_and_write_logfiles_func_def = {
    "type": "function",
    "function": {
        "name": "a5_process_and_write_logfiles",
        "description": "This function is used to process the log files as per the given and write the output on the new file.",
        "parameters": {
            "type": "object",
            "properties": {
                "source_path": {
                    "type": "string",
                    "description": "The path to the folder or a file for which the processing needs to be taken care",
                },
                "dest_path": {
                    "type": "string",
                    "description": "The path to the file where the processed log files needs to written",
                },
                "logs_files": {
                    "type": "integer",
                    "description": "It denotes the number of files in the folder to be used for processing",
                },
                "num_of_lines": {
                    "type": "integer",
                    "description": "It denotes the number of lines in each log file needs to be read",
                },
            },
            "required": ["source_path", "dest_path", "logs_files", "num_of_lines"],
            "additionalProperties": False,
        },
        "strict": True,
    },
}

create_index_from_files_func_def = {
    "type": "function",
    "function": {
        "name": "a6_create_index_from_files",
        "description": "This function will identify all files with a specific extension in a directory and is used to extract particular content (e.g., the first occurrence of a header) with content_marker and create an index file mapping filenames to their extracted content for the given extension files (e.g .md)",
        "parameters": {
            "type": "object",
            "properties": {
                "source_path": {
                    "type": "string",
                    "description": "The path to the file in which the index is present",
                },
                "dest_path": {
                    "type": "string",
                    "description": "The path to the file where the index needs to written",
                },
                "extension": {
                    "type": "string",
                    "description": "The extension of the file to be filtered.",
                },
                "content_marker": {
                    "type": "string",
                    "description": "The content marker to extract from each file.",
                },
            },
            "required": ["source_path", "dest_path", "extension", "content_marker"],
            "additionalProperties": False,
        },
        "strict": True,
    },
}

text_extraction_func_def = {
    "type": "function",
    "function": {
        "name": "a7_text_extraction",
        "description": "This function is used to extract the text from the give source file. The text can be anything for (e.g, email)",
        "parameters": {
            "type": "object",
            "properties": {
                "source_path": {
                    "type": "string",
                    "description": "The path to the file in which the text extraction needs to be done",
                },
                "dest_path": {
                    "type": "string",
                    "description": "The path to the file where the extracted text needs to written",
                },
                "task": {
                    "type": "string",
                    "description": "What task needs to be carried out, it can be text which needs to extracted.",
                },
            },
            "required": ["source_path", "dest_path", "task"],
            "additionalProperties": False,
        },
        "strict": True,
    },
}

extract_text_from_image = {
    "type": "function",
    "function": {
        "name": "a8_extract_text_from_image",
        "description": "This function is used to extract the text from the given image file. The text can be anything for (e.g, email)",
        "parameters": {
            "type": "object",
            "properties": {
                "source_path": {
                    "type": "string",
                    "description": "The path to the image file in which the text extraction needs to be done",
                },
                "dest_path": {
                    "type": "string",
                    "description": "The path to the file where the extracted text needs to written",
                },
                "task": {
                    "type": "string",
                    "description": "What task needs to be carried out, it can be text which needs to extracted.",
                },
            },
            "required": ["source_path", "dest_path", "task"],
            "additionalProperties": False,
        },
        "strict": True,
    },
}


find_similar_texts_func_def = {
    "type": "function",
    "function": {
        "name": "a9_find_similar_texts",
        "description": "This function is used to find the most similar pair of texts in the given source path using embeddings and write the result in the specified location",
        "parameters": {
            "type": "object",
            "properties": {
                "source_path": {
                    "type": "string",
                    "description": "The path to the file in which contains the text for which the similarity needs to be found.",
                },
                "dest_path": {
                    "type": "string",
                    "description": "The path to the file where the resulted text needs to written",
                },
                "num_similar_texts": {
                    "type": "integer",
                    "description": "The number of similar texts to find.",
                },
            },
            "required": ["source_path", "dest_path", "num_similar_texts"],
            "additionalProperties": False,
        },
        "strict": True,
    },
}

execute_query_and_write_result_func_def = {
    "type": "function",
    "function": {
        "name": "a10_execute_query_and_write_result",
        "description": "This function is used to execute the database file which is given and wirte its output in a specified location.",
        "parameters": {
            "type": "object",
            "properties": {
                "source_path": {
                    "type": "string",
                    "description": "The path to the db file to read",
                },
                "dest_path": {
                    "type": "string",
                    "description": "The path to the file where the records are written",
                },
                "query": {
                    "type": "string",
                    "description": "It is SQL query which will ran to fetch the records from the database.",
                },
                "query_params": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "This is the list of query parameters which is used to filter the records.",
                },
            },
            "required": ["source_path", "dest_path", "query", "query_params"],
            "additionalProperties": False,
        },
        "strict": True,
    },
}
