import os
import json
import sys

from tqdm import tqdm
from dataclasses import dataclass
from typing import Type, Union, Optional, Dict, Any

from gptbuilder.config import OpenaiConfig, AzureConfig
from gptbuilder.logger import logger
from gptbuilder.utils import generate_save_file_path, generate_response_key, handle_token_limit, save_batch, save_output
from gptbuilder.api import BatchAPI

@dataclass
class JsonBuilder:
    #required
    config: Union[Type[OpenaiConfig], Type[AzureConfig]]
    input_file_path: str
    user_prompt: str
    user_format_dict: Dict[str, Any]

    #optional
    sys_prompt: Optional[str] = None
    sys_format_dict: Optional[dict] = None
    save_file_path : Optional[str] = None
    batch_size: Optional[int] = None
    save_batch: Optional[bool] = False
    response_key: Optional[str] = 'gpt_output'
    json_data_key: Optional[str] = None
    json_encoding: Optional[str] = 'utf-8-sig'

    def __post_init__(self):
        #config
        if not isinstance(self.config, (OpenaiConfig, AzureConfig)):
            raise TypeError("'config' should be an OpenaiConfig or AzureConfig.")
        #input file
        if not self.input_file_path.endswith(".json"):
            raise Exception("'input_file_path' should ends with .json")
        #user_prompt:
        if not isinstance(self.user_prompt, str):
            raise ValueError("'user_prompt' should be a string")
        #user_format_dict
        if not (isinstance(self.user_format_dict, dict) and 
                all(isinstance(k, str) for k in self.user_format_dict.keys())):
            raise ValueError("'user_format_dict' should be a Dict[str, Any].")
        try:
            self.user_prompt.format(**self.user_format_dict)
        except KeyError:
            raise Exception("The keys in 'user_format_dict' do not match the format field in 'user_prompt'")
        #sys_prompt
        if self.sys_prompt:
            if not type(self.sys_prompt) is str:
                raise ValueError("'user_prompt' should be a string or None")
            #sys_format_dict
            if self.sys_format_dict:
                if not (isinstance(self.user_format_dict, dict) and 
                    all(isinstance(k, str) for k in self.user_format_dict.keys())):
                    raise ValueError("'sys_format_dict' key should be should be a Dict[str, Any]")
                try:
                    self.sys_prompt.format(**self.sys_format_dict)
                except KeyError:
                    raise Exception("The keys in 'sys_format_dict' do not match the format field in the 'sys_prompt'.")
        #save file path
        if self.save_file_path == None:
            self.save_file_path = generate_save_file_path()
            logger.info(f"The save path has been generated randomly:'{self.save_file_path}'")
        else:
            self.save_file_path = os.path.abspath(self.save_file_path)
            directory, _ = os.path.split(self.save_file_path)
            if not os.path.exists(directory):
                os.mkdir(directory)
            if os.path.exists(self.save_file_path):
                raise FileExistsError("save_file_path already exists. Please specify some other path")
            if not self.save_file_path.endswith(".json"):
                raise ValueError("save_file_path must end with .json")
        #batch size
        if self.batch_size:
            if not isinstance(self.batch_size, int):
                raise ValueError("batch_size must be int type")
        #response_key
        if type(self.response_key)!=str:
            self.response_key = str(self.response_key)

    def _load_data(self):
        self.input_file_path = os.path.abspath(self.input_file_path)
        try:
            with open(self.input_file_path, 'r', encoding=self.json_encoding) as f:
                data = json.load(f)
        except:
            raise FileNotFoundError
        if self.json_data_key:
            data = data[self.json_data_key]
        if not (isinstance(data, list) and all(isinstance(item, dict) for item in data)):
            raise TypeError("The JSON data is not a list of dictionaries.")
        if not all(isinstance(data[0].get(k), str) for k in self.user_format_dict.values()):
            invalid_keys = [k for k in self.user_format_dict.values() if not isinstance(data[0].get(k), str)]
            raise ValueError(f"The values for these keys in 'user_format_dict' are not all strings in 'json data' items: {invalid_keys}")
        if self.sys_format_dict:
            if not all(isinstance(data[0].get(k), str) for k in self.sys_format_dict.values()):
                invalid_keys = [k for k in self.sys_format_dict.values() if not isinstance(data[0].get(k), str)]
                raise ValueError(f"The values for these keys in 'sys_format_dict' are not all strings in 'json data' items: {invalid_keys}")
        if self.response_key in data[0].keys():
            self.response_key = generate_response_key(self.response_key, data[0].keys())
            logger.info(f"response_key is {self.response_key}by random")
        #check token length:
        token_param = {
            "data": data,
            "sys": (self.sys_prompt, self.sys_format_dict),
            "user": (self.user_prompt, self.user_format_dict),
            "config": self.config.to_handel_token()
        }
        load_succeeded, load_failed = handle_token_limit(token_param) 
        if len(load_failed) > 0:
            logger.info(f"{len(load_failed)}data that exceed the {self.config.model} maximum token length")
        return load_succeeded, load_failed
    
    def _make_batch(self, data):
        if self.batch_size==None:
            self.batch_size = self.config.model_tpm//self.config.model_max_token
            logger.info(f"batch_size is {self.batch_size} by default(model_tpm//model_max_token)")
        batch_data = [data[i:i+self.batch_size] 
                    if i+self.batch_size <= len(data) else data[i:]
                    for i in range(0, len(data), self.batch_size)]
        return batch_data

    def run(self):
        load_succeeded, load_failed = self._load_data()
        batch_data = self._make_batch(load_succeeded)
        success = []
        failed = []
        for idx, data in tqdm(enumerate(batch_data), desc=f"Running {len(batch_data)} Batch", total=len(batch_data)):
            try:
                api = BatchAPI(
                    client = self.config.to_client(),
                    params = self.config.to_params(),
                    sys = (self.sys_prompt, self.sys_format_dict),
                    user = (self.user_prompt, self.user_format_dict),
                    response_key = self.response_key,
                    data = data
                )
                success.extend(api.request())
            except Exception as e:
                if idx==0:
                    logger.error(e)
                    sys.exit(1)
                else:
                    logger.error(e)
                    logger.info(f"Failed-{idx}th batch")
                    failed.extend(data)
            if self.save_batch:
                save_batch(success,  self.save_file_path, self.json_encoding)
        if len(failed)>0:
            logger.info(f"{len(failed)} failed data")
        #Save output
        save_config = {
                    "input_file_path": self.input_file_path,
                    "model": self.config.model,
                    "temperature": self.config.temperature,
                    "sys_prompt": self.sys_prompt,
                    "sys_format_dict": self.sys_format_dict,
                    "user_prompt": self.user_prompt,
                    "user_format_dict": self.user_format_dict,
                    "response_key": self.response_key
                    }
        save_output(self.save_file_path, self.json_encoding, save_config, load_failed, success, failed)
        logger.info(f"Saved Output: {self.save_file_path}")