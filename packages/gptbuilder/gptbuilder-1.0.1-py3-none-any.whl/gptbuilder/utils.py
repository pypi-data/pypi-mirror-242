import tiktoken
import json
import os
import copy
import re
import math
from typing import List


def generate_save_file_path()->str:
    num = 1
    cwd = os.getcwd()
    random_save_file = os.path.join(cwd, f"output_{num}.json")
    while os.path.exists(random_save_file):
        num += 1
        random_save_file = os.path.join(cwd, f"output_{num}.json")
    return random_save_file

def generate_response_key(response_key: str, dict_keys: List[str])->str:
    num = 1
    while response_key in dict_keys:
        response_key = response_key+str(num)
        num += 1
    return response_key

def count_token(prompts: List[str], start_token_length=0)->int:
    encoding = tiktoken.get_encoding("cl100k_base")
    token_length = sum([int(len(encoding.encode(prompt))) for prompt in prompts if isinstance(prompt, str)])
    token_length += start_token_length
    return token_length

def save_batch(data, file_path, json_encoding):
    directory, file_name = os.path.split(file_path)
    file_path = os.path.join(directory, "batch_"+file_name)
    with open(file_path, 'w', encoding=json_encoding) as f:
        json.dump(data, f,indent=4, ensure_ascii=False)

def save_output(file_path, json_encoding, save_config, load_failed, succes, failed):
    output = dict()
    meta_data = copy.deepcopy(save_config)
    meta_data["num_token_exceed"] = len(load_failed)
    meta_data["num_success_data"] = len(succes)
    meta_data["num_failed_data"] = len(failed)
    output["meta_data"] = meta_data
    output["success_data"] = succes
    if len(load_failed) > 0:
        output["token_exceed_data"] = load_failed
    if len(failed) > 0:
        output["failed_data"] = failed
    with open(file_path, 'w', encoding=json_encoding) as f:
        json.dump(output, f,indent=4, ensure_ascii=False)

def format_prompt(data, prompt, format_dict):
    if format_dict:
        format_dict_ = {}
        for key, value in format_dict.items():
            format_dict_[key] = str(data[value])
        return prompt.format(**format_dict_)
    else:
        return prompt

def parse_wait_time(error_message: str, default: int)->int:
    pattern = r"Please try again in (\d+(\.\d+)?)(ms|s)"
    match = re.search(pattern, error_message)
    if match:
        time_value, _, time_unit = match.groups() 
        wait_time = float(time_value)
        if time_unit == 'ms':
            wait_time = wait_time / 1000
        wait_time = int(math.ceil(wait_time))
    else:
        wait_time = default
    return  wait_time
 
def handle_token_limit(token_param):
    sys_prompt, sys_format_dict = token_param["sys"]
    user_prompt, user_format_dict = token_param["user"]
    base_token_length = count_token(prompts=[sys_prompt, user_prompt])
    if token_param["config"]["output_max_length"]:
        token_threshold = token_param["config"]["model_max_token"] - (base_token_length+token_param["config"]["output_max_length"])
    else:
        token_threshold = token_param["config"]["model_max_token"] - (base_token_length+300)
    succeeded = []
    failed = []
    for d in token_param["data"]:
        prompts_length = count_token([d[v] for v in user_format_dict.values()])
        if sys_format_dict:
            prompts_length += count_token([d[v] for v in sys_format_dict.values()])
        if prompts_length < token_threshold:
            d_copy = copy.deepcopy(d)
            succeeded.append(d_copy)
        else:
            d_copy = copy.deepcopy(d)
            d_copy["token_length"] = prompts_length
            failed.append(d_copy)

    return succeeded, failed