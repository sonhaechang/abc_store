import json

def change_meta_to_json(meta):
	replace_meta = meta.replace("None", "null").replace("False", "false").replace("True", "true").replace("'","\"")
	return json.loads(replace_meta)