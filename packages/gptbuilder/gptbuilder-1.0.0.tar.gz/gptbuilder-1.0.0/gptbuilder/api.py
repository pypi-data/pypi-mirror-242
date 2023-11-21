import asyncio
import copy

import openai
from openai import AsyncOpenAI, AsyncAzureOpenAI
from typing import List, Dict, Type, Union, Tuple, Optional
from dataclasses import dataclass

from gptbuilder.utils import parse_wait_time, format_prompt

@dataclass
class BatchAPI:
    client: Union[Type[AsyncOpenAI], Type[AsyncAzureOpenAI]]
    params: dict
    sys: Tuple[Optional[str], Optional[Dict[str, str]]]
    user: Tuple[str, Dict[str, str]]
    response_key: str
    data: List[dict]
        
    def _merge_params(self):
        sys_prompt, sys_format_dict = self.sys
        user_prompt, user_format_dict = self.user
        params_list = []
        for data in self.data:
            messages = [{"role": "user", "content": format_prompt(data, user_prompt, user_format_dict)}]
            if sys_prompt:
                sys_message = {"role": "system", "content": format_prompt(data, sys_prompt, sys_format_dict)}
                messages.insert(0, sys_message)
            params = self.params
            params["messages"] = messages
            params_list.append(params)
        return params_list
    
    async def _async_generate(self, params):
        try:
            response = await self.client.chat.completions.create(**params)
        except openai.RateLimitError as error:
            wait_time = parse_wait_time(error.message, 3)
            await asyncio.sleep(wait_time)
            while True:
                try:
                    response = await self.client.chat.completions.create(**params)
                    break
                except openai.RateLimitError as error:
                    wait_time = parse_wait_time(error.message, 3)
                    await asyncio.sleep(wait_time)
        return response.choices[0].message.content
    
    async def _generate_concurrently(self):
        params_list = self._merge_params() 
        tasks = [asyncio.create_task(self._async_generate(params)) for params in params_list]
        responses = await asyncio.gather(*tasks)
        outputs = copy.deepcopy(self.data)
        for i, output in enumerate(outputs):
            output[self.response_key] = responses[i]
        return outputs

    def request(self):
        result = asyncio.run(self._generate_concurrently())
        return result
