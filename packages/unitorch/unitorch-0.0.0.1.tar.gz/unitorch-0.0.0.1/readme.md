<h1 align="Center"> <p> unitorch </p> </h1>

## Introduction

unitorch provides efficient implementation of popular unified NLU / NLG models with PyTorch. It automatically optimizes training / inference speed based on pupular NLP toolkits (transformers, fairseq, fastseq, etc) without accuracy loss. All these can be easily done (no need to change any code/model/data if using our command line tool, or simply add one-line code ` import unitorch` if using source code).

## Installation

```bash
pip3 install unitorch
```

### Requirements

- Python version >= 3.6
- configparser
- [datasets](https://github.com/huggingface/datasets)
- [fairseq](https://github.com/pytorch/fairseq) == 0.10.2
- fire
- pyarrow == 2.0.0
- pyparsing
- scipy
- sklearn
- [torch](http://pytorch.org/) >= 1.4.0
- [transformers](https://github.com/huggingface/transformers) == 4.3.2

## Usage

### Use source code

```python
# import unitorch at the beginning of your program
import unitorch

# use as general package
from unitorch.generation.unilm import UnilmForGeneration
unilm_model = UnilmForGeneration("path/to/unilm/config.json")

# use auto mode which need a config file for lib init
from unitorch import core_configure_parser
cfg = core_configure_parser("path/to/config.ini")

# init all groups in unitorch, including model, task, process, dataset, etc.
unitorch.init_core_group(cfg)

# only init model group
unitorch.init_core_model_group(cfg)

# get inited model
unilm_model = unitorch.core_model.get('core/model/unilm_for_generation')

# train inited task
unitorch.core_task.get('core/auto/supervised_task').train()

```

### Use unitorch cli
```bash
# only use config
unitorch-auto-train path/to/config.ini \
	--core/model/bert@config_name_or_file bert-large-uncased

# run custom code using unitorch auto mode (like fairseq-cli)
unitorch-auto-train path/to/code/directory \
	--core/model/bert@config_name_or_file bert-large-cased
```
