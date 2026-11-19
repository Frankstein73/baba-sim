"""Generated from colours.lua by tools/lua2py.py. Do not edit."""
from babasim.luart import *  # noqa: F403


def load(G):
	def f_setcolour(unitid=None, value_=None, *_):  # L1
		unit = G['mmf']['newObject'](unitid)
		name = unit['className']
		dir_ = unit['values'][G['DIR']]
		unitinfo = G['tileslist'][name]
		cc1, cc2 = (-1), (-1)
		value = (_t1 if L_t(_t1 := value_) else 'colour')
		if ((name != 'level') and (name != 'path')):
			if (G['objectcolours'][name] is not None):
				c = G['objectcolours'][name]
				if (c[value] is not None):
					cc = c[value]
					cc1, cc2 = cc[1], cc[2]
				elif (((value == 'colour') or (unitinfo is None)) or (unitinfo[value] is None)):
					if (c['colour'] is not None):
						cc_2 = c['colour']
						cc1, cc2 = cc_2[1], cc_2[2]
			if ((cc1 == (-1)) or (cc2 == (-1))):
				if ((unitinfo is not None) and (unitinfo[value] is not None)):
					cc_3 = unitinfo[value]
					unit['colour'] = L_T([cc_3[1], cc_3[2]])
					G['MF_setcolour'](unitid, cc_3[1], cc_3[2])
					cc1 = cc_3[1]
					cc2 = cc_3[2]
				elif ((unitinfo is not None) and (unitinfo['colour'] is not None)):
					cc_4 = unitinfo['colour']
					unit['colour'] = L_T([cc_4[1], cc_4[2]])
					G['MF_setcolour'](unitid, cc_4[1], cc_4[2])
					cc1 = cc_4[1]
					cc2 = cc_4[2]
				else:
					cc1, cc2 = 0, 3
					unit['colour'] = L_T([0, 3])
					G['MF_defaultcolour'](unitid)
			else:
				unit['colour'] = L_T([cc1, cc2])
				G['MF_setcolour'](unitid, cc1, cc2)
		return (cc1, cc2,)
		return ()
	G['setcolour'] = f_setcolour
	def f_getcolour(unitid_2=None, value__2=None, *_):  # L54
		unit_2 = G['mmf']['newObject'](unitid_2)
		name_2 = unit_2['className']
		name_ = unit_2['strings'][G['UNITNAME']]
		unitinfo_2 = G['tileslist'][name_2]
		defaultcolour = G['colours']['default']
		value_2 = (_t1 if L_t(_t1 := value__2) else 'colour')
		if (G['objectcolours'][name_2] is not None):
			c_2 = G['objectcolours'][name_2]
			if (c_2[value_2] is not None):
				cc_5 = c_2[value_2]
				return (cc_5[1], cc_5[2],)
			elif (((value_2 == 'colour') or (unitinfo_2 is None)) or (unitinfo_2[value_2] is None)):
				if (c_2['colour'] is not None):
					cc_6 = c_2['colour']
					return (cc_6[1], cc_6[2],)
		if (unitinfo_2 is None):
			return (defaultcolour[1], defaultcolour[2],)
		else:
			if (unitinfo_2[value_2] is None):
				if (unitinfo_2['colour'] is None):
					return (defaultcolour[1], defaultcolour[2],)
				else:
					colour = unitinfo_2['colour']
					return (colour[1], colour[2],)
			else:
				colour_2 = unitinfo_2[value_2]
				return (colour_2[1], colour_2[2],)
		return (defaultcolour[1], defaultcolour[2],)
		return ()
	G['getcolour'] = f_getcolour
	def f_getuicolour(which=None, subwhich=None, *_):  # L98
		bcolour = L_T()
		if ((subwhich is None) or (subwhich == '')):
			bcolour = G['colours'][which]
		else:
			bcolour = G['colours'][which][subwhich]
		if (bcolour is None):
			bcolour = G['colours']['default']
		return (bcolour[1], bcolour[2],)
		return ()
	G['getuicolour'] = f_getuicolour
	def f_updatecolours(edit_=None, *_):  # L114
		edit = False
		if (edit_ is not None):
			edit = edit_
		G['MF_setbackcolour']()
		for i, unit_3 in L_ipairs(G['units']):
			if (unit_3['strings'][G['UNITNAME']] != 'level'):
				if (unit_3['strings'][G['UNITTYPE']] != 'text'):
					G['setcolour'](unit_3['fixed'])
				else:
					if (edit is not None and edit is not False):
						G['setcolour'](unit_3['fixed'], 'active')
					else:
						G['setcolour'](unit_3['fixed'])
			else:
				G['MF_updatelevelcolour'](unit_3['fixed'])
		G['updatecode'] = 1
		G['code']()
	G['updatecolours'] = f_updatecolours
	def f_addobjectcolour(name_3=None, dir__2=None, c1=None, c2=None, *_):  # L143
		if (G['objectcolours'][name_3] is None):
			G['objectcolours'][name_3] = L_T()
		oc = G['objectcolours'][name_3]
		oc[dir__2] = L_T([c1, c2])
	G['addobjectcolour'] = f_addobjectcolour
	def f_getobjectcolour(unitid_3=None, c_3=None, *_):  # L153
		unit_4 = G['mmf']['newObject'](unitid_3)
		name_4 = unit_4['className']
		unitinfo_3 = (_t1 if L_t(_t1 := G['tileslist'][name_4]) else L_T())
		c1_2, c2_2 = (-1), (-1)
		if (G['objectcolours'][name_4] is not None):
			oc_2 = G['objectcolours'][name_4]
			if (oc_2[c_3] is not None):
				c1_2 = oc_2[c_3][1]
				c2_2 = oc_2[c_3][2]
		if ((c1_2 == (-1)) or (c2_2 == (-1))):
			if (unitinfo_3[c_3] is not None):
				c1_2 = unitinfo_3[c_3][1]
				c2_2 = unitinfo_3[c_3][2]
		return (c1_2, c2_2,)
		return ()
	G['getobjectcolour'] = f_getobjectcolour
	def f_updateunitcolour(unitid_4=None, edit__2=None, *_):  # L180
		edit_2 = False
		if (edit__2 is not None):
			edit_2 = edit__2
		unit_5 = G['mmf']['newObject'](unitid_4)
		if (unit_5['strings'][G['UNITNAME']] != 'level'):
			if (unit_5['strings'][G['UNITTYPE']] != 'text'):
				G['setcolour'](unit_5['fixed'])
			else:
				if (edit_2 is not None and edit_2 is not False):
					G['setcolour'](unit_5['fixed'], 'active')
				else:
					G['setcolour'](unit_5['fixed'])
	G['updateunitcolour'] = f_updateunitcolour
	def f_updateallcolours(*_):  # L202
		for i_2, unit_6 in L_ipairs(G['units']):
			G['updateunitcolour'](unit_6['fixed'], True)
			data = G['tileslist'][unit_6['className']]
			unit_6['values'][G['ZLAYER']] = data['layer']
	G['updateallcolours'] = f_updateallcolours
	def f_setthisuicolour(unitid_5=None, colourid=None, colourid2=None, *_):  # L211
		data_2 = G['colours'][colourid]
		if (colourid2 is not None):
			data_2 = G['colours'][colourid][colourid2]
		if (data_2 is None):
			L_noop(L_concat('No colour at ', L_tostring(colourid), ', ', L_tostring(colourid2)))
		G['MF_setcolour'](unitid_5, data_2[1], data_2[2])
	G['setthisuicolour'] = f_setthisuicolour
	def f_setbackcolour(*_):  # L225
		G['MF_setbackcolour']()
	G['setbackcolour'] = f_setbackcolour
