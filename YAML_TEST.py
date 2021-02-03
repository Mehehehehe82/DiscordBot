'''Ignore this, I'm just making sure my default config.yml is valid'''
import yaml


with open('config.yml') as f:
	data = yaml.load(f, Loader=yaml.FullLoader)
	print(yaml.dump(data))
	print(data)
