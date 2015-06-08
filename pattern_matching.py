#!/usr/bin/env python3
import re

filename = 'block-2/_-5VZ_/_-6N3.class.asasm'

trait_pattern = 'trait slot QName\(PrivateNamespace\("(.*)"\), "(.*)"\) type QName\(PackageNamespace\("(.*)"\), "(.*)"\) end'
trait_inj = '\n  trait slot QName(PrivateNamespace("{0}"), "_-uid") type QName(PackageNamespace(""), "Number") end\n'

init_pattern = 'initproperty[\s]+QName\(PrivateNamespace\("(.*)"\), ".*"\)'
init_inj = '''\n     getlocal0
     findpropstrict      QName(PackageNamespace("flash.utils"), "getTimer")
     callproperty        QName(PackageNamespace("flash.utils"), "getTimer"), 0
     initproperty        QName(PrivateNamespace("{0}"), "_-uid")\n
'''

#getproperty         QName(PrivateNamespace("_-5Qc"), " null")
getid_pattern = '(getproperty[\s]+QName\(PrivateNamespace\("{0}"\), "{1}"\))'

reader_pattern = 'callproperty[\s]+QName\(PackageNamespace\(""\), "(.*)"\), 0'
reader_inj = '''\n      setlocal1
      getlex              QName(PackageNamespace("flash.external"), "ExternalInterface")
      pushstring          "Trafficker.logIncoming"
      getlocal0
      getproperty         QName(PrivateNamespace("{0}"), "_-uid")
      getlocal1
      callpropvoid        QName(PackageNamespace(""), "call"), 3
      getlocal1\n
'''

filetext = ''
inits = []
traits = []

with open(filename) as f:
	text = f.read()
	trait_matches = re.finditer(trait_pattern, text)
	init_match = re.search(init_pattern, text)
	reader_matches = re.finditer(reader_pattern, text)

	match_found = False
	m = None
	for m in trait_matches:
		match_found = True
		traits.append({ 'namespace' : m.group(1), 'name' : m.group(2), 'type_namespace': m.group(3), 'type': m.group(4) })
		pass

	print (traits)

	if match_found:
		text = text[1:m.end()] + trait_inj.format(traits[0].get('namespace')) + text[(m.end()+1):]

	if init_match:
		text = text[1:init_match.end()] + init_inj.format(traits[0].get('namespace')) + text[(init_match.end()+1):]
		pass

	for trait in traits:
		if trait.get('type') == 'int':
			print (trait)
			getid_match = re.search(getid_pattern.format(trait.get('namespace'), trait.get('name')), text)
			if getid_match:
				text = text[1:getid_match.end()] + reader_inj.format(trait.get('namespace')) + text[(getid_match.end()+1):]

	match_found = False
	m = None
	for m in reader_matches:
		match_found = True

	print(text)
