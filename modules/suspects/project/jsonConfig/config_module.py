'''Info Header Start
Name : config_module
Author : Wieland@AMB-ZEPH15
Version : 0
Build : 4
Savetimestamp : 2023-02-24T13:08:58.964998
Saveorigin : Project.toe
Saveversion : 2022.28040
Info Header End'''
class ConfigValue:
    def _to_json(self):
        return self.Value

    def __repr__(self) -> str:
        return str( self.value.val )
    
    def __init__(self, default = "", validator = lambda value: True, comment = "", parser = None):
        
        self.comment = comment
        self.validator = validator
        self.value = tdu.Dependency(None)
        self.parser = parser or type(default)
        self.Set( default )

    def Set(self, value):
        parsed_value = self.parser( value )
        if not self.validator( parsed_value ): return False
        self.value.val = parsed_value
        self.value.modified()

    @property
    def Dependency(self):
        return self.value
    
    @property
    def Value(self):
        return self.value.val


class CollectionDict(dict):
    def __init__(self, items:dict = None, comment = ""):
        self.comment = comment
        if items: self.update( items )
        
    def __getattr__(self, key):
        return self.get( key )
    
    def Set(self, data):
        for key, item in data.items():
            if key in self: self[key].Set( item )

import copy

class CollectionList(list):
    def __init__(self,items:list = None, default_member = None, comment = ""):
        self.comment = comment
        self.default_member = default_member or ConfigValue()
        if items: self.Set( items )

    def Set(self, data:list):
        self.clear()
        
        for index, item in enumerate( data ):
            value = None
            if isinstance( item, dict): value = CollectionDict( item )
            if isinstance( item, list): value = CollectionList( item )
            else: 
                value = copy.deepcopy( self.default_member )
                value.Set( item )
            self.append( value )
    

import json

class Collection(CollectionDict):
    def __init__(self, items: dict = None):
        super().__init__(items)
    
    def To_Json(self, indent = 4):
        def default( data ):
            if hasattr( data, "_to_json"): return data._to_json()
            return json.JSONEncoder.default(self, o)
        return json.dumps( self, default=default, indent = indent)
    
    def From_Json(self, jsonstring:str):
        data = json.loads( jsonstring )
        self.Set( data )
    
