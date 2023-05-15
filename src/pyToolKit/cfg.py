from os.path import join, realpath
import configparser, pathlib
from contextlib import suppress


class ini:
	def new(*a, delimiter=":", **k):
		"""
		create an empty configparser with: extended interpolation, : for delimiter and allowing empty value's for keys
		:return: configerparser obj.
		"""
		cfg = configparser.ConfigParser(
			interpolation=configparser.ExtendedInterpolation(),
			delimiters=f"{delimiter}",
			allow_no_value=True,
		)  # create empty config
		cfg.optionxform = lambda option: option
		return cfg

	def readfile(name, path, delimiter=":", conf="") -> configparser:
		"""
		Reads config from [p|path]/[n|name] [INI|conf]-like file
		:param k: [n|name],[p|path],[c|conf]
		:keyword n|name: path to [name]
		:keyword p|path: path to [name]
		:keyword c|conf: (optional) config parser object, ini.new() if ommitted
		:return: config parser object
		"""
		conf = conf or ini.new(delimiter=delimiter)
		file = join(path, name)
		conf.read(file)
		return conf

	def readfiles(names, path, delimiter=":", conf="") -> configparser:
		"""
		Reads config from [p|path]/[n|name] [INI|conf]-like file
		:param k: [n|name],[p|path],[c|conf]
		:keyword n|name: path to [name]
		:keyword p|path: path to [name]
		:keyword c|conf: (optional) config parser object, ini.new() if ommitted
		:return: config parser object
		"""
		files = []
		conf = conf or ini.new(delimiter=delimiter)
		for name in names:
			files += [join(path, name)]
		conf.read(files)
		return conf

	def NestedtoDict(conf, *a, **k):
		"""
		Converts Configparser Obj to Nested dict
		:param k: [c|conf]
		:keyword c|conf: config parser object, ini.new() if omitted
		:return: dict
		"""
		for key in conf["Layout"]:
			section = {
				key: {
					**conf[key],
					"Sub": {
						subkey: {**conf[subkey]}
						for subkey in conf["Layout"][key].split(",")
					},
				}
			}
			pTree(section)

	def toQDict(conf):

		from QLib.QTypes import QDict

		qdict = QDict()

		for section in conf.sections():

			qdict[section] = {}
			for key in conf[section].keys():
				val = conf[section][key]

				qdict[section][key] = val
				with suppress(TypeError):
					with suppress(NameError):
						qdict[section][key] = eval(val)
					with suppress(ValueError):
						qdict[section][key] = int(val)

		return qdict

	def saveFile(name, conf, path) -> None:
		"""
		writes the configparser config to a file.
		:param k: keywords:f,file,c,conf
		:keyword f|file: file to save the config to
		:keyword c|conf: config(configparser) to be saved
		:return:
		"""
		file = join(realpath(path), name)
		with open(file, "w") as f:
			conf.write(f)

	#

	def set_key(name, path, conf, file, section, key, val) -> configparser:
		"""
		:keyword key:
		:keyword val:
		:keyword section:
		:keyword file:
		:return: config
		"""
		if s := conf.get(section):
			s[key] = str(val)
		return conf

	def save_key(**k) -> configparser:
		k["c"] = (conf := ini.set_key(**k))
		ini.saveFile(**k)
		return conf

	def set_dict(**k) -> configparser:
		"""
		:param dct: dictionary where the first two key:val pairs are file:filename and section within the file
		:return:
		"""
		dct = k.get("d", k.get("dct"))
		sect = k.get("s", k.get("section"))
		conf = k.get("c", k.get("config"))
		for key, val in dct.items():
			conf = ini.set_key(key=key, val=val, section=sect, conf=conf)
		return conf

	def save_dict(**k) -> None:
		k["c"] = (conf := ini.set_dict(**k))
		ini.saveFile(**k)
