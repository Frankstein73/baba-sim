"""Generated from metadata.lua by tools/lua2py.py. Do not edit."""
from babasim.luart import *  # noqa: F403


def load(G):
	def f_getmetadata(unit=None, *_):  # L1
		realname = unit['className']
		if (((realname != 'level') and (realname != 'path')) and (realname != 'specialobject')):
			if (G['tileslist'][realname] is not None):
				data = G['tileslist'][realname]
				name = (_t1 if L_t(_t1 := data['name']) else 'error')
				unittype = (_t2 if L_t(_t2 := data['unittype']) else 'object')
				type_ = (_t3 if L_t(_t3 := data['type']) else 0)
				tiling = (_t4 if L_t(_t4 := data['tiling']) else (-1))
				layer = (_t5 if L_t(_t5 := data['layer']) else 10)
				unit['strings'][G['UNITNAME']] = name
				unit['strings'][G['NAME']] = name
				if (L_sub(name, 1, 5) == 'text_'):
					name = L_sub(name, 6)
					unit['strings'][G['NAME']] = name
				unit['strings'][G['UNITTYPE']] = unittype
				unit['values'][G['TILING']] = tiling
				unit['values'][G['TYPE']] = type_
				unit['values'][G['ZLAYER']] = layer
			else:
				L_noop(L_concat('No metadata found for ', realname, '!'))
	G['getmetadata'] = f_getmetadata
