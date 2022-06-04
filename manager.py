import subprocess

class Manager:
	def __init__(self, module = None, own_processes = [], other_processes = []):
		self.own_processes = own_processes
		self.other_processes = other_processes
		self.module = module

	def start(self):
		module = getattr(self.module, '__name__', None) or self.module
		for name in self.own_processes:
			others = [p for p in self.own_processes if p != name] + self.other_processes
			subprocess.Popen(f'python chat.py {module} {name} {" ".join(others)}', creationflags=subprocess.CREATE_NEW_CONSOLE)