from json import JSONEncoder
import numpy
import json


class NewtonEncoder(JSONEncoder):
	def default(self, obj):
		if isinstance(obj, numpy.ndarray):
			return obj.tolist()
		return JSONEncoder.default(self, obj)


class NewtonJsonSerializer:

	@staticmethod
	def obj_type(obj):
		if isinstance(obj, numpy.ndarray):
			return 'numpy_array'
		return 'default'

	def serialize_output(self, obj):
		return json.dumps(
				{
					'data': obj,
					'type': self.obj_type(obj)
				}, cls=NewtonEncoder)

	@staticmethod
	def deserialize(serialized_text):
		deserialized_json = json.loads(serialized_text)
		if deserialized_json['type'] == 'numpy_array':
			return numpy.asarray(deserialized_json['data'])
		return deserialized_json['data']
