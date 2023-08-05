import json
import logging

import aiohttp

from .authentication import HomePlusOAuth2Async
from .homepluslight import HomePlusLight
from .homeplusmodule import HomePlusModule
from .homeplusplug import HomePlusPlug
from .homeplusremote import HomePlusRemote

PLANT_TOPOLOGY_BASE_URL='https://api.developer.legrand.com/hc/api/v1.0/plants/'
""" API endpoint for the Home+ plant information. """

PLANT_TOPOLOGY_RESOURCE='/topology'
""" Path to the Home+ plant topology information. """

class HomePlusPlant:
    """Class representing a "plant", i.e a Home or Environment containing Home+ devices
    
    Attributes:
        id (str): Unique identifier of the plant.
        name (str): Name of the plant.
        country (str): Two-letter country code where the plant is located.
        oauth_client (HomePlusOAuth2Async): Authentication client to make request to the REST API.
        modules (dict): Dictionary containing the information of all modules in the plant.
        topology (dict): JSON representation of the plant's topology as returned by the API
        module_status (dict): JSON representation of the plant modules' status as returned by the API
    """

    def __init__(self, id, name, country, oauth_client: HomePlusOAuth2Async):
        """ HomePlusPlant Constructor 
        
        Args:
            id (str): Unique identifier of the plant.
            name (str): Name of the plant.
            country (str): Two-letter country code where the plant is located.
            oauth_client (HomePlusOAuth2Async): Authentication client to make request to the REST API.
        """
        self.id = id
        self.name = name
        self.country = country
        self.oauth_client = oauth_client
        self.modules = {}
        self.topology = json.loads('{"plant": { } }')
        self.module_status = json.loads('{"modules": { } }')

    def __str__(self):
        """ Return the string representing this plant """
        return f'Home+ Plant: name->{self.name}, id->{self.id}, country->{self.country}'

    @property
    def logger(self):
        """Return logger of the plant."""
        return logging.getLogger(__name__)

    async def refresh_topology(self):
        """ Makes a call to the API to refresh the topology information of the plant into attribute `topology`.
        The topology provides information about the plants ambients/rooms and the modules within them.

        At this time, the plant topology is only used to extract the module data.
        TODO: Handle ambients/rooms
        """        
        try:        
             response = await self.oauth_client.get_request(PLANT_TOPOLOGY_BASE_URL + self.id + PLANT_TOPOLOGY_RESOURCE)
        except aiohttp.ClientResponseError as err:
            self.logger.error("HTTP client response error when refreshing plant topology")
        else:
            self.topology = await response.json()

    async def refresh_module_status(self):
        """ Makes a call to the API to refresh the status of all modules in the plant into attribute `module_status`.
        The module status provides information about the modules current status, eg. reachability, on/off, battery, consumption.

        TODO: Handle consumptions
        """    
        try:        
             response = await self.oauth_client.get_request(PLANT_TOPOLOGY_BASE_URL + self.id)
        except aiohttp.ClientResponseError as err:
            self.logger.error("HTTP client response error when refreshing module status")
        else:
            self.module_status = await response.json()

    async def update_topology(self):
        """ Convenience method that first refreshes the plant's topology information through an API call
        and then parses the modules contained in that topology into the object's inner map.

        This method call on its own will not refresh the status of the modules.
        """
        await self.refresh_topology()
        self._parse_topology()

    async def update_module_status(self):
        """ Convenience method that first refreshes the information of the modules' status through an API call
        and then parses the status information into the modules of the object's inner map.

        This method call on its own will not refresh the module topology of the plant so modules that are no longer
        present in the plant will remain with their last known status, while new modules that may have been added
        to the topology will not be reflected in it just yet.
        """
        await self.refresh_module_status()
        self._parse_module_status()

    async def update_topology_and_modules(self):
        """ Convenience method that first refreshes the plant's topology information and then refreshes
        the status of all modules in that topology.

        This implies 2 API calls and will produce an up-to-date view of the plant in the inner map of modules.
        """
        await self.refresh_topology()
        await self.refresh_module_status()
        self._parse_topology_and_modules()

    def _parse_topology(self):
        """ Auxiliary method to parse the topology data returned by the API. 
        
        It is assumed that this data has been previously refreshed into the object's attribute: self.topology.
        """
        # Extract the plant's modules from the topology data structure.
        # The plant modules come from two distinct elements of the topology - the ambients and the modules.
        flat_modules = []
        for ambient in self.topology['plant']['ambients']:
            for module in ambient['modules']:
                flat_modules.append(module)

        for module in self.topology['plant']['modules']:
            flat_modules.append(module)

        input_module_ids = []
        for module in flat_modules:
            input_module_ids.append(module['id'])
            # Check if the module already exists in the module dict of this plant
            if module['id'] in self.modules:
                self._update_module(module)
            else:
                self._create_module(module)

        # Check if any module should no longer be in this plant's dict
        modules_to_pop = []
        for existing_id in self.modules.keys():
            if existing_id in input_module_ids:
                continue
            modules_to_pop.append(existing_id)

        for m in modules_to_pop:           
            self.modules.pop(m, None)            

    def _parse_module_status(self):
        """ Auxiliary method to parse the module status data returned by the API. 
        
        It is assumed that this data has been previously refreshed into the object's attribute: self.module_status.
        It is also assumed that the plant topology is up to date - this method will only search for the module status
        of those modules that have been parsed in the topology data.
        """
        # With the modules identified in the module_status information, 
        # we update their status into the modules map of this plant object
        # TODO: refactor all this repeated code
        input_module_ids = []
        for m in self.module_status['modules'].get('lights', []):
            module_id = m['sender']['plant']['module']['id']
            input_module_ids.append(module_id)
            if module_id in self.modules:
                self._update_module_base_status(module_id, m)
                self._update_interactive_module_status(module_id, m)

        for m in self.module_status['modules'].get('plugs', []):
            module_id = m['sender']['plant']['module']['id']
            input_module_ids.append(module_id)
            if module_id in self.modules:
                self._update_module_base_status(module_id, m)
                self._update_interactive_module_status(module_id, m)

        for m in self.module_status['modules'].get('remotes', []):
            module_id = m['sender']['plant']['module']['id']
            input_module_ids.append(module_id)
            if module_id in self.modules:
                self._update_module_base_status(module_id, m)
                self._update_remote_status(module_id, m)

        # Check whether any existing modules in the topology have no module status info
        # and if that is the case, then we mark them as unreachable
        for existing_id in self.modules.keys():
            if existing_id in input_module_ids:
                continue
            self.modules[existing_id].reachable = False 

    def _parse_topology_and_modules(self):
        """ Auxiliary method that parses the data returned by the API and converts it into a dictionary
        of modules that is stored in the attribute `modules`.
        """
        # Parse the topology first
        self._parse_topology()

        # Next we update their status from the module_status property
        self._parse_module_status()
        
    def _create_module(self, input_module):
        """ 'Factory' method of specific Home+ Control modules depending on their type that adds the new module to the attribute `modules`.
        
        Args:
            input_module (dict): Dictionary representing the JSON structure of a module as returned by the API.
        """
        if input_module['device'] == 'light':
            self.modules[input_module['id']] = HomePlusLight(plant=self, id=input_module['id'], device=input_module['device'], name=input_module['name'], hw_type=input_module['hw_type'])
        elif input_module['device'] == 'plug':
            self.modules[input_module['id']] = HomePlusPlug(plant=self, id=input_module['id'], device=input_module['device'], name=input_module['name'], hw_type=input_module['hw_type'])
        elif input_module['device'] == 'remote':
            self.modules[input_module['id']] = HomePlusRemote(plant=self, id=input_module['id'], device=input_module['device'], name=input_module['name'], hw_type=input_module['hw_type'])
        else:
            self.modules[input_module['id']] = HomePlusModule(plant=self, id=input_module['id'], device=input_module['device'], name=input_module['name'], hw_type=input_module['hw_type'])

    def _update_module(self, input_module):
        """ Update the information of an existing module instance in the plant, based on the latest input data.

        Args:
            input_module (dict): Dictionary representing the JSON structure of a module as returned by the API. This 
                                 contains the latest module data that will be updated into the existing module instance.            
        """
        u_module = self.modules[input_module['id']]
        u_module.device = input_module['device']
        u_module.name = input_module['name']
        u_module.hw_type = input_module['hw_type']

    def _update_module_base_status(self, curr_module_id, input_module):
        """ Update the basic information of an existing module instance in the plant.

        Args:
            curr_module_id (str): Identifier of the existing module that is to be updated.
            input_module (dict): Dictionary representing the JSON structure of a module as returned by the API. This 
                                 contains the latest module data that will be updated into the existing module instance.            
        """
        u_module=self.modules[curr_module_id]
        u_module.fw = input_module['fw']
        u_module.reachable = input_module['reachable'] == True

    def _update_interactive_module_status(self, curr_module_id, input_module):
        """ Update the information of an existing interactive module instance in the plant.
        This method basically updates the status (on or off) of the interactive module.

        Args:
            curr_module_id (str): Identifier of the existing interactive module that is to be updated.
            input_module (dict): Dictionary representing the JSON structure of a module as returned by the API. This 
                                 contains the latest module data that will be updated into the existing module instance.            
        """
        u_module=self.modules[curr_module_id]
        u_module.status = input_module['status']

    def _update_remote_status(self, curr_module_id, input_module):
        """ Update the information of an existing remote module instance in the plant.
        This method basically updates the battery status of the remote module.

        Args:
            curr_module_id (str): Identifier of the existing remote module that is to be updated.
            input_module (dict): Dictionary representing the JSON structure of a module as returned by the API. This 
                                 contains the latest module data that will be updated into the existing module instance.            
        """
        u_module=self.modules[curr_module_id]
        u_module.battery = input_module['battery']