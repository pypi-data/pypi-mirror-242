<div align="center"><h1>&nbsp;Break the Sequential Dependency of LLM Inference Using Lookahead Decoding</h1></div>

<p align="center">
| <a href="https://lmsys.org/blog/2023-11-21-lookahead-decoding/"><b>Blog</b></a> | 
</p>

## Introduction 
We introduce Lookahead Decoding, 

## Contents
- [Introduction](#introduction)
- [Contents](#contents)
- [Installation](#installation)
  - [Install From The Source](#install-from-source)
  - [Inference](#inference)
  - [Use In Your Own Code](#inference-plugin)
- [Citation](#citation)
- [Guidance](#guidance)


## Installation
### Install from the source
```bash
git clone https://github.com/hao-ai-lab/LookaheadDecoding.git
cd LookaheadDecoding
pip install -r requirements.txt
pip install -e .
```

### Inference With Lookahead decoding
You can run the minimal example to see the speedup that Lookahead decoding brings.
```bash
python minimal.py #no Lookahead decoding
USE_LADE=1 LOAD_LADE=1 python minimal.py #use Lookahead decoding, 1.6x speedup
```

You can also enjoy chatting with your own chatbots with Lookahead decoding.
```bash
USE_LADE=1 python applications/chatbot.py  --model_path meta-llama/Llama-2-7b-chat-hf --debug --chat #chat, with lookahead 
USE_LADE=0 python applications/chatbot.py  --model_path meta-llama/Llama-2-7b-chat-hf --debug --chat #chat, without lookahead


USE_LADE=1 python applications/chatbot.py  --model_path meta-llama/Llama-2-7b-chat-hf --debug #no chat, with lookahead
USE_LADE=0 python applications/chatbot.py  --model_path meta-llama/Llama-2-7b-chat-hf --debug #no chat, without lookahead
```

### Use Lookahead decoding in your own code
You can import and use Lookahead decoding in your own code in three LoCs. You also need to set ```USE_LADE=1``` in command line or set ```os.environ["USE_LADE"]="1"``` in Python script. Note that Lookahead decoding only support LLaMA and Greedy Search yet.

```python
import lade
lade.augment_all()
lade.config_pading(LEVEL=5, WINDOW_SIZE=7, GUESS_SET_SIZE=7, DEBUG=0)
```
## Citation
```bibtex
@misc{fu2023lookahead,
    title = {Breaking the Sequential Dependency of LLM Inference Using Lookahead Decoding},
    url = {https://lmsys.org/blog/2023-11-21-lookahead-decoding/},
    author = {Yichao Fu and Peter Bailis and Ion Stoica and Hao Zhang},
    month = {November},
    year = {2023}
}
```
## Guidance
The core implementation is in decoding.py. Lookahead decoding requires an adaptation for each specific model. An example is in models/llama.py.

