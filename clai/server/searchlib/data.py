#
# Copyright (C) 2020 IBM. All Rights Reserved.
#
# See LICENSE.txt file in the root directory
# of this source tree for licensing information.
#

import os
import configparser
from collections import OrderedDict
from pathlib import Path
from typing import List, Dict

from . import StackExchange, KnowledgeCenter, Manpages

class Datastore:
    # Instance data members
    apis:OrderedDict = {}
    
    def __init__(self):
        config = configparser.ConfigParser()
        config.read(os.path.join(str(Path(__file__).parent.absolute()), 'config.ini'))
        
        # Get a list of APIs defined in the config file
        for section in config.sections():
            if section == "stack_exchange":
                self.apis[section] = StackExchange("Unix StackExchange forums", config[section])
            elif section == "ibm_kc":
                self.apis[section] = KnowledgeCenter("IBM KnowledgeCenter", config[section])
            elif section == "manpages":
                self.apis[section] = Manpages("manpages", config[section])
            else:
                raise AttributeError(f"Unsupported service type: '{section}'")

    def getAPIs(self) -> OrderedDict:
        return self.apis

    def search(self, query, service='stack_exchange', size=10) -> List[Dict]:
        supportedServices = self.apis.keys()
        
        if service in supportedServices:
            serviceProvider = self.apis[service]
            res = serviceProvider.call(query, size)
        else:
            raise AttributeError(f"service must be one of: {str(supportedServices)}")

        return res
