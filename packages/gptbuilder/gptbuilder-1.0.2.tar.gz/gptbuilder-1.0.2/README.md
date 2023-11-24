# GPTBuilder
This package can be used to send batch requests with large amounts of data to OpenAI or AzureOpenAI.
It takes a **list** as input or accepts a **json file**, and saves the results as a **json file**.

## requirement
openai==1.2.4  
tdqm  
tiktoken  

## Usage
```python
from gptbuilder import JsonBuilder, OpenaiConfig, AzureConfig

#using openai
config = OpenaiConfig(
        model="gpt-3.5-turbo",
        api_key="api key",
        model_max_token=4096,
        model_tpm=90000,
        temperature = 0.1
)

#using azure
config = AzureConfig(
        model="gpt-4", #azure openai deployment name
        api_key="api key",
        api_version="version", #2023-07-01-preview
        azure_endpoint="end point url", #https://example.openai.azure.com/
        model_max_token=8192,
        model_tpm=40000,
        temperature = 0.01
)

system_prompt = "You are an AI assistant. You will be given a task. You must generate a detailed and long answer."
user_prompt = "{question}"
format_dict = {"question": "question"}
builder = JsonBuilder(config = config,
                      input_file_path = "C:/Users/Desktop/test.json",
                      response_key="response",
                      system_prompt = system_prompt,
                      user_prompt = user_prompt,
                      format_dict = format_dict,
                      save_batch = True,
                      batch_size=7)

builder.run()
```
## Precautions Before Use
OpenAI has a Tokens Per Minute (TPM) limit for the GPT model or on a per-account basis. Therefore, it is necessary to calculate the tokens of the input data and set the appropriate batch as a parameter. If the batch is not specified, the TPM divided by model max token specified in the config will be used as the batch parameter.

## Using in Jupyter Notebook
Because it uses asyncio, you need to add the following code before using it in a Jupyter Notebook.
```python
!pip install nest_asyncio

import nest_asyncio
nest_asyncio.apply()
```
## JSONBuilder
### required Attribute

- `config` : The configuration object that should be one of `OpenaiConfig` or `AzureConfig`.
- `input_file_path` : Path of input file.
- `user_prompt` : userprompt
- `user_format_dict` : dictonary to use formatting user_prompt, key: placeholder of 'user_prompt' , value: key for the string you want to format; the key refers to the key value within a list of dictionaries in JSON data.

## Optional Attribute

- `sys_prompt` : systemprompt
- `sys_format_dict` : same as `user_format_dict`
- `save_file_path` : file path to save the output. If set to None, the file is saved with a random filename in the directory where the Python code is executed. Defaults to `None`.
- `batch_size` : The size of batches to process. If set to None, the batch size is tpm//model_max_tokens. Defaults to `None`.
- `save_batch` : If True, results are overridden and saved for each batch in the same folder as the output file path. Defaults to `False`.
- `response_key` : Key to receive the API response as a value. Defaults to `'gpt_output'`.
- `json_data_key` : Key of List[Dict] if json_file is a dictonary type. Defaults to `None`.
- `json_encoding` : The encoding format for the JSON file. Defaults to `'utf-8-sig'`

### Method
- `run()` : method to run builder

### Example Input file format
json file in the form of a list[dict], below is example
```json
[
    {
        "source": "huggingface",
        "context_id": "flan.564327",
        "question": "Generate an approximately fifteen-word sentence that describes all this data: Midsummer House eatType restaurant; Midsummer House food Chinese; Midsummer House priceRange moderate; Midsummer House customer rating 3 out of 5; Midsummer House near All Bar One"
    },
    {
        "source": "huggingface",
        "context_id": "fla.1875913",
        "question": "What happens next in this paragraph? She then rubs a needle on a cotton ball then pushing it onto a pencil and wrapping thread around it. She then holds up a box of a product and then pouring several liquids into a bowl. she Choose your answer from: A. adds saucepan and shakes up the product in a grinder. B. pinches the thread to style a cigarette, and then walks away. C. then dips the needle in ink and using the pencil to draw a design on her leg, rubbing it off with a rag in the end. D. begins to style her hair and cuts it several times before parting the ends of it to show the hairstyle she has created."
    }
]
```
If the format of the json file is like the following dict type:
`json_data_key`='datset'
```json
{
    "date" : "2023.11,21",
    "dataset":[
                {
                    "source": "huggingface",
                    "context_id": "flan.564327",
                    "question": "Generate an approximately fifteen-word sentence that describes all this data: Midsummer House eatType restaurant; Midsummer House food Chinese; Midsummer House priceRange moderate; Midsummer House customer rating 3 out of 5; Midsummer House near All Bar One"
                },
                {
                    "source": "huggingface",
                    "context_id": "fla.1875913",
                    "question": "What happens next in this paragraph? She then rubs a needle on a cotton ball then pushing it onto a pencil and wrapping thread around it. She then holds up a box of a product and then pouring several liquids into a bowl. she Choose your answer from: A. adds saucepan and shakes up the product in a grinder. B. pinches the thread to style a cigarette, and then walks away. C. then dips the needle in ink and using the pencil to draw a design on her leg, rubbing it off with a rag in the end. D. begins to style her hair and cuts it several times before parting the ends of it to show the hairstyle she has created."
                }
            ]
}
```

## ListBuilder
### required Attribute

- `config` : The configuration object that should be one of `OpenaiConfig` or `AzureConfig`.
- `input_list` : List[Dict]
- `user_prompt` : userprompt
- `user_format_dict` : dictonary to use formatting user_prompt, key: placeholder of 'user_prompt' , value: key for the string you want to format; the key refers to the key value within a list of dictionaries in JSON data.

### Optional Attribute

- `sys_prompt` : systemprompt
- `sys_format_dict` : same as `user_format_dict`
- `save_file_path` : file path to save the output. If set to None, the file is saved with a random filename in the directory where the Python code is executed. Defaults to `None`.
- `batch_size` : The size of batches to process. If set to None, the batch size is tpm//model_max_tokens. Defaults to `None`.
- `save_batch` : If True, results are overridden and saved for each batch in the same folder as the output file path. Defaults to `False`.
- `response_key` : Key to receive the API response as a value. Defaults to `'gpt_output'`.
- `json_encoding` : The encoding format for the JSON file. Defaults to `'utf-8-sig'`

### Method
- `run()` : method to run builder

## Output of GPTBuilder
output is json file, below is example.  

```json
{
  "meta_data": {},
  "success_data": [
    {
        "source": "huggingface",
        "context_id": "flan.564327",
        "question": "Generate an approximately fifteen-word sentence that describes all this data: Midsummer House eatType restaurant; Midsummer House food Chinese; Midsummer House priceRange moderate; Midsummer House customer rating 3 out of 5; Midsummer House near All Bar One",
        "gpt_output": "Midsummer House is a moderately priced Chinese restaurant with a 3/5 customer rating, located near All Bar One."
    },
    {
        "source": "huggingface",
        "context_id": "fla.1875913",
        "question": "What happens next in this paragraph? She then rubs a needle on a cotton ball then pushing it onto a pencil and wrapping thread around it. She then holds up a box of a product and then pouring several liquids into a bowl. she Choose your answer from: A. adds saucepan and shakes up the product in a grinder. B. pinches the thread to style a cigarette, and then walks away. C. then dips the needle in ink and using the pencil to draw a design on her leg, rubbing it off with a rag in the end. D. begins to style her hair and cuts it several times before parting the ends of it to show the hairstyle she has created.",
        "gpt_output": "Midsummer House is a moderately priced Chinese restaurant with a 3/5 customer rating, located near All Bar One."
    }
  ],
  "token_exceed_data": [],
  "failed_data": []
}
```
- [meta_data] - It is the metadata of the GPT builder and includes configurations.
- [success_data] - successful data from an API request
- [failed_data] - failed data from an API request
- [token_exceed_data] - data that exceeds the token limit of the GPT model
  
if [failed_data] and [token_exceed_data] do not exist, they are not present as key values.