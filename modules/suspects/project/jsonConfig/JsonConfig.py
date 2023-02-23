'''Info Header Start
Name : JsonConfig
Author : Wieland@AMB-ZEPH15
Version : 0
Build : 3
Savetimestamp : 2023-02-23T17:52:45.228704
Saveorigin : Project.toe
Saveversion : 2022.28040
Info Header End'''
import config_module, os, json

class JsonConfig:
	"""
	JsonConfig description
	"""
	def __init__(self, ownerComp):
		# The component to which this extension is attached
		self.ownerComp = ownerComp
		self.filepath = "config.json"
		self.Refresh_File()

	def Refresh_File(self):
		self.Data = self.Load_From_Json( self.ownerComp.op("config_json").text or "{}")
		self.Save()

	def Save(self):
		self.ownerComp.op("config_json").text = self.Data.To_Json()
		

	def Load_From_Json(self, json_string):
		return self.Load_From_Dict( json.loads( json_string))

	def Load_From_Dict(self, datadict:dict):
		schema = config_module.Collection(
			self.ownerComp.op("callbackManager").Execute("GetConfigSchema")( config_module.ConfigValue, config_module.CollectionDict, config_module.CollectionList) 
		)
		data = config_module.Collection( schema )
		data.Set( datadict )
		return data