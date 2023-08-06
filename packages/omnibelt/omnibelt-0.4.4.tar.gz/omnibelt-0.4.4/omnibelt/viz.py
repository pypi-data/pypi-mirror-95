

try:
	import uuid
	from IPython.display import display_javascript, display_html
	import json
except ImportError:
	pass

class render_dict(object):
	def __init__(self, json_data):
		if isinstance(json_data, dict):
			self.json_str = json.dumps(json_data)
		else:
			self.json_str = json_data
		self.uuid = str(uuid.uuid4())

	def _ipython_display_(self):
		display_html('<div id="{}" style="height: 100px; width:100%;"></div>'.format(self.uuid), raw=True)
		display_javascript("""
		require(["https://rawgit.com/caldwell/renderjson/master/renderjson.js"], function() {
		document.getElementById('%s').appendChild(renderjson(%s))
		});
		""" % (self.uuid, self.json_str), raw=True)
