#!/usr/bin/env python
# SPDX-FileCopyrightText: © 2023 N. Sertac Artan <artans.github@gmail.com>
# SPDX-License-Identifier: MIT

import json        
import os
from abc import ABC, abstractmethod

class Yaprak(ABC):
    """Base class for the yaprak package."""
    def __init__(self, config = None):
        '''
            The yaprak class initializes with empty local variables. If a
            configuration file name is given as an argument, this will trigger
            the loading of a configuration file via the self.readConfig()
            method.

            Args:
                config (str): (Optional) configuration filename. If given, the 
                    self.readConfig() method will be called.
        '''
        self.config = {}
        self.current_iteration = {}
        self.globals = {}
        self.__IDs = []
        self.__processes = []
        self.__inFileList = []
        self.__outFileList = []
        self.__outPath = None
        if config:
            self.readConfig(config)
            self.globals = {'outPath': self.__outPath}

    def run(self):
        '''
            The main method to call to go through all the input files, execute
            all the processes, populate the output files, and report anything 
            pertinent to each input file.

            This method runs for all instances (defined as an ID, an input file,
            and an output file). If any of the parameters don't exist, the
            operation stops.

            For each process a process_spec is given (probably read from the 
            configuration file. This process_spec will be passed to the method,
            and executed. The process_spec can include basic parameters such as 
            numbers, booleans, and strings, which the json file supports.

            The process will be skipped if the process_spec does not have the
            apply property. This way, processes can be disabled quickly by just
            removing the apply property.

            Args:
                None

            Returns:
                None
        '''
        for instances in zip(self.__IDs, self.__inFileList, self.__outFileList):
            self.current_iteration = {'ID': instances[0], 'inFile': instances[1],
                                      'outFile': instances[2]}
            self.load(instances[1])
            for process_spec in self.__processes:
                if process_spec['apply']:
                    function = getattr(self, process_spec['process'])
                    function(process_spec)
            self.save(instances[2])
            self.report()

    @abstractmethod
    def load(self, file):
        '''
            An abstract method as a placeholder for the file load function. The
            child class must implement this function.

            Args:
                file (str): Name of the file to load

            Returns:
                None
        '''
        raise NotImplementedError("The load method in Yaprak is abstract\
        and should be implemented in the child class")

    @abstractmethod
    def save(self, file):
        '''
            An abstract method as a placeholder for the file save function. The
            child class must implement this function.

            Args:
                file (str): Name of the file to save

            Returns:
                None
        '''
        raise NotImplementedError("The save method in Yaprak is abstract\
        and should be implemented in the child class")

    @abstractmethod
    def report(self):
        '''
            An abstract method as a placeholder for the report function. The
            child class must implement this function.

            Args:
                None: 

            Returns:
                None
        '''
        raise NotImplementedError("The report method in Yaprak is abstract\
        and should be implemented in the child class")

    # Config
    def readConfig(self, file): 
        '''
            Reads the json configuration file. The IDs, input file list, and
            output file lists will be populated with full paths to the files, if
            they exist in the configuration file. If output path is defined and
            non-existing, the output path will be created. Processes will also
            be populated if they are listed in the configuration file. 

            This function will be called automatically in __init__() if the
            configuration file is given to __init__().

            Args:
                file (str): Name of the configuration file to load 

            Returns:
                None
        '''
        self.config = load_json_file(file)
        if "IDs" in self.config:
            self.__IDs = self.config['IDs'] 
        if "inFileList" in self.config:
            self.__inFileList = fullPathFileList(self.config, 'in')
        if "outFileList" in self.config:
            self.__outFileList = fullPathFileList(self.config, 'out')
        if "outPath" in self.config:
            self.__outPath = self.config['outPath'] 
            mkdir_p(self.__outPath)
        if "processes" in self.config:
            self.__processes = [x for x in self.config['processes']]

    def setConfig(self, config):
        self.config = config

    def getConfig(self):
        return self.config

    def generateConfig(self):
        pass 

    # IDs
    def setIDs(self, IDs):
        self.__IDs = IDs

    def getIDs(self):
        return self.__IDs 

    def generateIDs(self):
        pass 

    # File Lists
    def setInFileList(self, fileList):
        self.__inFileList = fileList

    def getInFileList(self):
        return self.__inFileList 

    def setOutFileList(self, fileList):
        self.__outFileList = fileList

    def getOutFileList(self):
        return self.__outFileList 

    # Processes
    def setProcesses(self, processes):
        self.__processes = processes

    def getProcesses(self):
        return self.__processes 

    def generateProcesses(self):
        pass 

class Summary(Yaprak):
    """Summary class for the yaprak package."""
    def __init__(self, config = None):
        '''
            The summary class is similar to the base yaprak class. The primary
            difference is that the Summary class saves the output to a single
            output file, and individual files. This class is not intended to be
            used as a way to aggregate many output files into a single file. 
            Instead, this class is aimed for the use cases, where some basic 
            information is collected from each file (e.g. statistics, or
            feature vectors), and summarized in the single output file.

            Args:
                config (str): (Optional) configuration filename. If given, the 
                    self.readConfig() method will be called.
        '''
        Yaprak.__init__(self, config)
        self.outSummaryFile = None
        self.readAdditionalConfig(config)

    # Config
    def readAdditionalConfig(self, config): 
        '''
            Reads the global information from the configuration file, that is
            the name of the output summary file, if it exists.

            Args:
                config (str): Name of the configuration file to load 

            Returns:
                None
        '''
        if "outSummaryFile" in self.config:
            self.outSummaryFile = fullPathFile(self.config, 'outSummary')

    def run(self):
        '''
            This method is similar to the base class' run method in that it
            loads all the input files, run the processes, and report the
            pertinent information. The main difference is that in this class 
            only one output file is generated, which consolidates outputs from 
            all the input files.

            Args:
                None: 

            Returns:
                None
        '''
        IDs = self.getIDs()
        inFileList = self.getInFileList()
        processes = self.getProcesses()
        for instances in zip(IDs, inFileList):
            self.current_iteration = {'ID': instances[0], 
                                      'inFile': instances[1]}
            self.load(instances[1])
            for process_spec in processes:
                if process_spec['apply']:
                    function = getattr(self, process_spec['process'])
                    function(process_spec)
        self.summarize()
        self.report()

    @abstractmethod
    def summarize(self):
        '''
            An abstract method as a placeholder for the summarize function. The
            child class must implement this function.

            Args:
                None: 

            Returns:
                None
        '''
        raise NotImplementedError("The summarize method in Yaprak is abstract\
        and should be implemented in the child class")

def fullPathFile(config, type):
        pathName = type + "Path"
        fileName = type + "File"
        fullPathFileOutput = None 
        # Path and filename separate
        if pathName in config and fileName in config:
            path = config[pathName] 
            fileName = config[fileName]
            fullPathFileOutput = path + fileName
        # Full path
        elif fileName in config: 
            fullPathFileOutput = config[fileName] 
        return fullPathFileOutput 

def fullPathFileList(config, type):
        pathName = type + "Path"
        fileListName = type + "FileList"
            
        # Grab file info from config.
        fullPathFileListOutput = []
        # Path and filename separate
        if pathName in config and fileListName in config:
            path = config[pathName] 
            fileList = config[fileListName]
            fullPathFileListOutput = [path + file for file in fileList]
        # Full path
        elif fileListName in config: 
            fullPathFileListOutput = config[fileListName] 
        return fullPathFileListOutput 

def load_json_file(fileName):
    """
        Loads a json file as config 
        
        Args:
            fileName (str): Name of input json file.

        Returns:
            dict: Json data as key-value pairs dictionary 
    """
    with open(fileName) as json_file:
        json_data = json.load(json_file)
    return json_data

def mkdir_p(path):
    """
        Creates the directory path if it doesn't exist
        
        Args:
            path (str): Full path of the directory to be created 

        Returns:
            int: 0 if directory exists, 1 if directory does not exist. If the
            latter, this function creates the new library.
    """
    if os.path.exists(path):
        print("Output directory exists, overwrites are possible.")
        return 0
    print("Creating new directory " + path + ".")
    os.makedirs(path)
    return 1


