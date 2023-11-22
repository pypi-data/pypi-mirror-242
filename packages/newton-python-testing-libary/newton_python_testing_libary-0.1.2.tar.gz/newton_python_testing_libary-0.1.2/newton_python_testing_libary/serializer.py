from json import JSONEncoder
import numpy
import json


class NewtonEncoder(JSONEncoder):
	def default(self, obj):
		if isinstance(obj, numpy.nd):
			return obj.tolist()
		return JSONEncoder.default(self, obj)


class NewtonJsonSerializer:

	@staticmethod
	def serialize_output(obj):
		return json.dumps(obj, cls=NewtonEncoder)
