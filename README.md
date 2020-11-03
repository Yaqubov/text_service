# Text Service

Text Service is a program that messages coming from client are changed or encoded by the server.You can encode or decode messages with key or change the words in a sentence according to json file.

## Installation

Use following command to get files

```bash
git clone https://github.com/Yaqubov/text_service
```

After, install packages with:

```bash
pip install requirements.txt
```

## Usage

If you want to change words in sentences according to json file:

```bash
python3 text_service.py [mode] chance_text my_source_file.txt my_json_file.json
```

If you want to encode or decode messages with key:

```bash
python3 text_service [mode] encode_decode my_source_file.txt my_key.txt
```

Example:

```bash
python3 text_service.py server change_text source_file.txt my_json_file.json
python3 text_service.py client encode_decode source_file.txt my_key.txt
```
