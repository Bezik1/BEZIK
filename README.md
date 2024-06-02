# BEZIK model
 User AI assistant made using pytorch

## Structure
- [Operator](#operator)
- [Executor](#executor)
- [Listener](#listener)

## Operator
Operator is a seq-to-seq transformer, made using pytorch. It converts text instructions of what you want computer to do, to instructions that are being later executed by Executor class.

### Development Files Tools
Necessary files for training and development of model
- operator_train.py - this file trains model, you can adjust it by changing hyperparameters and data sets

### Training Data
Data folder containing training, test and validation sets is placed in: "./data/operator folder"

- train.csv
- test.csv
- valid.csv


## Executor
Executor is a class that execute list of commands received from the operator module.

### List of commands:
- open [program]
- webdriver [mode] [url] [parameters]
    - search
- excel [column_names] [column_values]
- write [program] [code]