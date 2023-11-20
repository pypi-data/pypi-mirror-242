# Yet Another PRocessing and Analyzing Kit

![PyPI - Version](https://img.shields.io/pypi/v/yaprak) ![PyPI - License](https://img.shields.io/pypi/l/yaprak)

This is a small package for simplifying batch data processing and analysis.

This project is licensed under the terms of the MIT license.

# Installation

```bash
    pip install yaprak
```

# Documentation 

[Documentation](https://github.com/arta-ns/yaprak/tree/main/src/yaprak/html/yaprak/index.html)

# Use Case

Yaprak can be used for running the same set of functions on a set of input files. For instance, when processing a dataset with multiple files each with time-series data, typically all the data should be preprocessed with the same set of filters before any other operation can be carried out. Similarly, the filtered data needs to be processed for a given application in a similar manner. 

# Use Example

To use yaprak, in addition to the input files, at least two more files are needed:
1. A Python file with a class derived from Yaprak.
2. A JSON file for configuring a run (file paths, methods to be called (_processes_), and parameters to pass to these methods (referred to as `process_spec` in the Python code, and any other user variables relevant to the use case)

## Class inheriting Yaprak
First, define a class derived from Yaprak (myClass in the example below). 4 methods **must** be defined in this class:
1. `__init__(self, config)`: The initialization method has one parameter `config`, which is the name of the JSON configuration file. This method should also call the initialization method for Yaprak.
2. `load(self, file)`: This method describes how to load one input file (`file`). This is specific to the use case. For instance, in the example below, there is only one integer value in each file, so the `load()` method implements the loading of the file and extracts the integer value from it. In another case, the input files can be `.csv` files or binary files, and the load function should implement the relevant load operation.
3. `save(self, file)`: Similar to load this method describes how to save the processed data to an output file, and it is specific to the application.
4. `report(self)`: If there is any information to be reported pertinent to the current file, the `report` function can be used for this purpose.

Any other method that is needed to process the data, should also be described in this class (or derived from another class, here). These methods should include only one parameter other than `self`, which is `process_spec`.

For instance, the `add(self, process_spec)` method below adds two numbers. One is from the process_spec (which is read from the parameter list for this method from the configuration file (`process_spec['a1']`)), and the other one is read from the input file (`self.file_input`).

To use the class, only two steps are needed:
1.  `yap = myClass('myconfig.json')`: Define an instance (`yap`) of the derived class (`myClass`) passing the configuration file name (`myconfig.json`) as the parameter.
2. `yap.run()`: Run the batch, which will sequentially read each file, execute all the processes described in the configuration file on each input file, report any information regarding the currently processed file, and save the output to an output file.

```python
from yaprak.yaprak import Yaprak

class myClass(Yaprak):
    def __init__(self, config):
        Yaprak.__init__(self, config)
        self.total = 0
        self.product = 0
        self.file_input = None

    def load(self, file):
        with open(file, 'r') as f:
            self.file_input = int(f.readline())
            print(self.file_input)


    def save(self, file):
        with open(file, 'w') as f:
            f.write("Sum is " + str(self.total) +"\n")		
            f.write("Product is " + str(self.product))		

    def report(self):
        print('Finished processing')

    def add(self, process_spec):
        self.total = process_spec['a1'] + int(str(self.file_input))

    def mul(self, process_spec):
        self.product = process_spec['m1'] * self.config['m_global'] 


yap = myClass('myconfig.json')
yap.run()
```

## JSON Configuration File

The configuration file below (`myconfig.json`) is a standard JSON file and consists of the following sections:

`processes`: This list has one entry for each process (i.e., method in the derived class) to be executed for all inputs. The processes in this list are executed in the given order. For each process, the key `process` should have the value of the name of the method (e.g. add, mul). The key `apply` is a Boolean and should be set to `true` for processes to be executed and `false` for processes to be skipped. Any other parameter (currently only numbers, and strings) to the method can also be passed as key-value pairs for each process. For instance, for the `add` process below, an integer parameter `a1` is given.

This approach of configuring processes has two features, which can be achieved without any changes to the Python code:
1. The order of the processes can be changed.
2. The parameter values of the processes can be changed.
3. The processes can be applied selectively.

In addition to the `processes` list, the following items **must** also exist in the JSON file:
1. A list of `IDs`, representing each file with an ID string (This could be the prefix of the file name for instance).
2. A list of all the input files in the list `inFileList`, and
3. A list of all the output files in the list `outFileList`.

The `inFileList` and `outFileList` may define absolute paths. Alternatively, paths for input files (`inPath` ) and output files (`outPath`) can be defined and the file names in the file lists can be relative.

Any other parameter useful to the application can be configured in this file as key-value pairs and can be accessed within the derived class from the `config` dictionary.

```json
{
    "processes": [
        {
            "process": "add",
            "a1": 10,
            "apply": true
        },
        {
            "process": "mul",
            "m1": 20,
            "apply": true
        }
    ],
    "m_global": 100,
    "inPath": "./inputs/",
    "outPath": "./outputs/",
    "IDs": [
        "1",
        "2",
        "3"
    ],
    "inFileList": [
        "1.dat",
        "2.dat",
        "3.dat"
    ],
    "outFileList": [
        "1.txt",
        "2.txt",
        "3.txt"
    ]
}
```
