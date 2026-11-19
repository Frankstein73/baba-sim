"""Generated from update.lua by tools/lua2py.py. Do not edit."""
from babasim.luart import *  # noqa: F403


def load(G):
	def f_addaction(unitid=None, data=None, *_):  # L1
		unit = None
		name = ''
		if (((unitid is not None) and (unitid > 0)) and (unitid != 2)):
			unit = G['mmf']['newObject'](unitid)
		invalid = False
		if (unit is not None):
			invalid = unit['flags'][15]
			name = G['getname'](unit)
		action = L_T()
		if (unitid == 2):
			invalid = False
			name = 'empty'
		elif (unitid == 1):
			invalid = False
			name = 'level'
		if (invalid is False):
			L_insert(action, unitid)
			for i, v in L_ipairs(data):
				L_insert(action, v)
			action['name'] = name
			L_insert(G['updatelist'], action)
	G['addaction'] = f_addaction
	def f_doupdate(*_):  # L39
		if (L_len(G['updatelist']) > 0):
			for i_2, data_2 in L_pairs(G['updatelist']):
				if (L_len(G['wordunits']) > 0):
					for a, b in L_ipairs(G['wordunits']):
						if (b[1] == data_2[1]):
							G['updatecode'] = 1
				if (L_len(G['wordrelatedunits']) > 0):
					for a_2, b_2 in L_ipairs(G['wordrelatedunits']):
						if (b_2[1] == data_2[1]):
							G['updatecode'] = 1
				if (data_2[2] == 'update'):
					if ((data_2[3] is not None) and (data_2[4] is not None)):
						G['update'](data_2[1], data_2[3], data_2[4], data_2[5])
					else:
						L_noop(L_concat('No meaningful update data for object ', L_tostring(data_2[1]), ', ', data_2[2]))
				elif (data_2[2] == 'updatedir'):
					if (data_2[3] is not None):
						G['updatedir'](data_2[1], data_2[3])
					else:
						L_noop(L_concat('No meaningful update data for object ', L_tostring(data_2[1]), ', ', data_2[2]))
				elif ((data_2[2] == 'convert') or (data_2[2] == 'emptyconvert')):
					if (data_2[3] is not None):
						G['doconvert'](data_2)
					else:
						L_noop(L_concat('No meaningful update data for object ', L_tostring(data_2[1]), ', ', data_2[2]))
				elif (data_2[2] == 'createall'):
					if (data_2[3] is not None):
						dolevels = (_t1 if L_t(_t1 := data_2[4]) else False)
						G['createall'](data_2[3], None, None, None, dolevels)
					else:
						L_noop(L_concat('No meaningful update data for object ', L_tostring(data_2[1]), ', ', data_2[2]))
				elif (data_2[2] == 'dofloat'):
					if ((data_2[3] is not None) and (data_2[4] is not None)):
						unit_2 = G['mmf']['newObject'](L_tonumber(data_2[6]))
						unit_2['values'][G['FLOAT']] = L_tonumber(data_2[4])
						G['addundo'](L_T(['float', data_2[7], data_2[5], data_2[3], data_2[4]]))
						if ((unit_2['holder'] is not None) and (unit_2['holder'] != 0)):
							G['addundo'](L_T(['holder', unit_2['values'][G['ID']], unit_2['holder'], 0]), G['unitid'])
							unit_2['holder'] = 0
					else:
						L_noop(L_concat('No meaningful update data for object ', L_tostring(data_2[1]), ', ', data_2[2]))
		G['updatelist'] = L_T()
	G['doupdate'] = f_doupdate
	def f_findupdate(unitid_2=None, updatename=None, *_):  # L105
		result = L_T()
		if (L_len(G['updatelist']) > 0):
			for i_3, data_3 in L_ipairs(G['updatelist']):
				if (data_3[1] == unitid_2):
					if (data_3[2] == updatename):
						L_insert(result, data_3)
		return result
	G['findupdate'] = f_findupdate
