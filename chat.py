from argparse import ArgumentParser
from importlib import import_module
import traceback

if(__name__ == '__main__'):
	try:
		parser = ArgumentParser()
		parser.add_argument('module', type=str, help='The name of the module that will be used.')
		parser.add_argument('own_address', type=str, help='The address of this participant.')
		parser.add_argument('participants', type=str, nargs='*', help='The addresses of the other participants.')
		args = parser.parse_args().__dict__

		Module = getattr(import_module(args['module']), args['module'])

		module = Module(args['own_address'])

		while(True):
			message = input()
			module.Send(args['participants'][0], message)
	except Exception as e:
		traceback.print_exc()
		input()