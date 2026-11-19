"""Generated from changes.lua by tools/lua2py.py. Do not edit."""
from babasim.luart import *  # noqa: F403


def load(G):
	def f_savechange(target=None, params=None, updateid_=None, *_):  # L1
		updateid = (_t1 if L_t(_t1 := updateid_) else 0)
		if (G['changes'][target] is None):
			G['changes'][target] = L_T()
		this = G['changes'][target]
		default = G['tileslist'][target]
		if (target == 'Editor_levelnum'):
			icon = params[1]
			file = params[2]
			root = params[3]
			if (file is not None):
				this[icon] = L_T()
				thisdat = this[icon]
				thisdat['file'] = file
				thisdat['root'] = root
			else:
				this[icon] = None
		else:
			name = params[1]
			image = params[2]
			colour = params[3]
			tiling = params[4]
			otype = params[5]
			unittype = params[6]
			activecolour = params[7]
			root_2 = params[8]
			layer = params[9]
			argtype = params[10]
			argextra = params[11]
			cobjects = params[12]
			if (name is not None):
				if (L_strlen(name) > 0):
					this['name'] = name
					if (name == default['name']):
						this['name'] = None
						if (G['unitreference'][name] is None):
							G['unitreference'][name] = target
					else:
						if (G['unitreference'][this['name']] is None):
							G['unitreference'][this['name']] = target
						elif ((G['unitreference'][default['name']] is not None) and (G['unitreference'][default['name']] == target)):
							olduid = (_t2 if L_t(_t2 := G['unitreference'][this['name']]) else 'nil')
							uid = G['unitreference'][default['name']]
							G['unitreference'][this['name']] = uid
							G['unitreference'][default['name']] = None
						elif ((G['unitreference'][this['name']] is not None) and (G['unitreference'][this['name']] != target)):
							pass
			if (image is not None):
				if (L_strlen(image) > 0):
					this['image'] = image
					if (image == default['sprite']):
						this['image'] = None
			if (colour is not None):
				if (L_strlen(colour) > 0):
					this['colour'] = colour
					dvalue = default['colour']
					compare = L_concat(L_tostring(dvalue[1]), ',', L_tostring(dvalue[2]))
					if (colour == compare):
						this['colour'] = None
						if ((G['objectcolours'][target] is not None) and (G['objectcolours'][target]['colour'] is not None)):
							G['objectcolours'][target]['colour'] = None
			if (activecolour is not None):
				if (L_strlen(activecolour) > 0):
					this['activecolour'] = activecolour
					dvalue_2 = default['active']
					compare_2 = ''
					if (dvalue_2 is not None):
						compare_2 = L_concat(L_tostring(dvalue_2[1]), ',', L_tostring(dvalue_2[2]))
						if (activecolour == compare_2):
							this['activecolour'] = None
							if ((G['objectcolours'][target] is not None) and (G['objectcolours'][target]['active'] is not None)):
								G['objectcolours'][target]['active'] = None
			if (tiling is not None):
				if (L_strlen(tiling) > 0):
					this['tiling'] = L_tonumber(tiling)
					if (tiling == default['tiling']):
						this['tiling'] = None
			if (otype is not None):
				if (L_strlen(otype) > 0):
					this['type'] = L_tonumber(otype)
					if (otype == default['type']):
						this['type'] = None
			if (unittype is not None):
				if (L_strlen(unittype) > 0):
					this['unittype'] = unittype
					if (unittype == default['unittype']):
						this['unittype'] = None
			if (root_2 is not None):
				this['root'] = root_2
				if (root_2 == default['sprite_in_root']):
					this['root'] = None
			if (layer is not None):
				if (L_strlen(layer) > 0):
					this['layer'] = L_tonumber(layer)
					if (layer == default['layer']):
						this['layer'] = None
			if (argtype is not None):
				if (L_strlen(argtype) > 0):
					parser = ''
					argtype_ = L_T()
					for i in L_range(1, L_strlen(argtype)):
						l = L_sub(argtype, i, i)
						if (l != ','):
							parser = L_concat(parser, l)
						else:
							L_insert(argtype_, L_tonumber(parser))
							parser = ''
						if (i == L_strlen(argtype)):
							L_insert(argtype_, L_tonumber(parser))
							parser = ''
					this['argtype'] = argtype_
					isdefault = True
					defaultargtype = (_t3 if L_t(_t3 := default['argtype']) else L_T([0]))
					if (L_len(argtype_) != L_len(defaultargtype)):
						isdefault = False
					else:
						for i_2, v in L_ipairs(argtype_):
							compare_3 = (_t4 if L_t(_t4 := defaultargtype[i_2]) else (-1))
							if (compare_3 != v):
								isdefault = False
					if (isdefault is not None and isdefault is not False):
						this['argtype'] = None
			if (argextra is not None):
				if (L_strlen(argextra) > 0):
					parser_2 = ''
					argextra_ = L_T()
					for i_3 in L_range(1, L_strlen(argextra)):
						l_2 = L_sub(argextra, i_3, i_3)
						if (l_2 != ','):
							parser_2 = L_concat(parser_2, l_2)
						else:
							L_insert(argextra_, parser_2)
							parser_2 = ''
						if (i_3 == L_strlen(argextra)):
							L_insert(argextra_, parser_2)
							parser_2 = ''
					this['argextra'] = argextra_
					isdefault_2 = True
					defaultargextra = (_t5 if L_t(_t5 := default['argextra']) else L_T())
					if (L_len(argextra_) != L_len(defaultargextra)):
						isdefault_2 = False
					else:
						for i_4, v_2 in L_ipairs(argextra_):
							compare_4 = (_t6 if L_t(_t6 := defaultargextra[i_4]) else '')
							if (compare_4 != v_2):
								isdefault_2 = False
					if (isdefault_2 is not None and isdefault_2 is not False):
						this['argextra'] = None
			if (cobjects is not None):
				if (L_strlen(cobjects) > 0):
					parser_3 = ''
					cobjects_ = L_T()
					for i_5 in L_range(1, L_strlen(cobjects)):
						l_3 = L_sub(cobjects, i_5, i_5)
						if (l_3 != ','):
							parser_3 = L_concat(parser_3, l_3)
						else:
							L_insert(cobjects_, parser_3)
							parser_3 = ''
						if (i_5 == L_strlen(cobjects)):
							L_insert(cobjects_, parser_3)
							parser_3 = ''
					this['customobjects'] = cobjects_
					isdefault_3 = True
					defaultcobjects = (_t7 if L_t(_t7 := default['customobjects']) else L_T())
					if (L_len(cobjects_) != L_len(defaultcobjects)):
						isdefault_3 = False
					else:
						for i_6, v_3 in L_ipairs(cobjects_):
							compare_5 = (_t8 if L_t(_t8 := defaultcobjects[i_6]) else '')
							if (compare_5 != v_3):
								isdefault_3 = False
					if (isdefault_3 is not None and isdefault_3 is not False):
						this['customobjects'] = None
						if (default['customobjects'] is not None):
							G['customobjects'][target] = L_T()
							for i_7, v_4 in L_ipairs(default['customobjects']):
								L_insert(G['customobjects'][target], v_4)
						else:
							G['customobjects'][target] = None
					else:
						G['customobjects'][target] = L_T()
						for i_8, v_5 in L_ipairs(cobjects_):
							L_insert(G['customobjects'][target], v_5)
			otype_2 = (_t9 if L_t(_t9 := this['type']) else default['type'])
			if ((otype_2 == 3) or (otype_2 == 7)):
				G['conditions'][target] = L_T()
				conddata = G['conditions'][target]
				conddata['arguments'] = False
				if (otype_2 == 7):
					conddata['arguments'] = True
					conddata['argtype'] = L_T()
					argtype_2 = (_t10 if L_t(_t10 := (_t11 if L_t(_t11 := this['argtype']) else default['argtype'])) else L_T([0]))
					for i_9, v_6 in L_ipairs(argtype_2):
						L_insert(conddata['argtype'], v_6)
					argextra_2 = (_t12 if L_t(_t12 := this['argextra']) else default['argextra'])
					if (argextra_2 is not None):
						conddata['argextra'] = L_T()
						for i_10, v_7 in L_ipairs(argextra_2):
							L_insert(conddata['argextra'], v_7)
			elif (G['conditions'][target] is not None):
				G['conditions'][target] = None
		if (updateid != 0):
			G['dochanges'](updateid)
		elif (target != 'Editor_levelnum'):
			G['MF_alert']('updateid == 0, changes.lua line 124')
	G['savechange'] = f_savechange
	def f_storechanges(*_):  # L351
		changedobjects = ''
		changedobjects_short = ''
		changedobjectlist = L_T()
		changelimit = 600
		icons = L_T()
		for target_2, this_2 in L_pairs(G['changes']):
			if (target_2 == 'Editor_levelnum'):
				for i_11, icondata in L_pairs(this_2):
					G['MF_store']('level', 'icons', L_concat(L_tostring(i_11), 'file'), icondata['file'])
					G['MF_store']('level', 'icons', L_concat(L_tostring(i_11), 'root'), icondata['root'])
					icons[(i_11 + 1)] = 1
			else:
				for i_12, thing in L_pairs(this_2):
					tostore = ''
					if (((i_12 != 'argtype') and (i_12 != 'argextra')) and (i_12 != 'customobjects')):
						tostore = thing
					else:
						for a, b in L_ipairs(thing):
							tostore = L_concat(tostore, b, ',')
					G['MF_store']('level', 'tiles', L_concat(target_2, '_', i_12), tostore)
				changedobjects = L_concat(changedobjects, target_2, ',')
				changedobjects_short = L_concat(changedobjects_short, L_sub(target_2, (-3)), ',')
				if (L_len(changedobjects) >= changelimit):
					L_insert(changedobjectlist, changedobjects)
					changedobjects = ''
		if (L_len(changedobjects) > 0):
			L_insert(changedobjectlist, changedobjects)
			changedobjects = ''
		for i_13 in L_range(1, G['generaldata2']['values'][G['ICONCOUNT']]):
			if (icons[i_13] is None):
				G['MF_store']('level', 'icons', L_concat(L_tostring((i_13 - 1)), 'file'), '')
				G['MF_store']('level', 'icons', L_concat(L_tostring((i_13 - 1)), 'root'), '')
		G['MF_store']('level', 'tiles', 'changed_count', L_tostring(L_len(changedobjectlist)))
		for i_14, v_8 in L_ipairs(changedobjectlist):
			id_ = 'changed'
			if (i_14 > 1):
				id_ = L_concat(id_, L_tostring(i_14))
			G['MF_store']('level', 'tiles', id_, v_8)
		G['editor']['strings'][G['CHANGEDOBJECTS']] = changedobjects_short
		G['MF_store']('level', 'tiles', 'changed_short', changedobjects_short)
	G['storechanges'] = f_storechanges
	def f_restoredefaults(*_):  # L422
		namesetups = L_T()
		for target_3, this_3 in L_pairs(G['changes']):
			if (target_3 == 'Editor_levelnum'):
				for i_15, icondata_2 in L_pairs(this_3):
					thisid = G['MF_create'](target_3)
					G['MF_defaultsprite'](thisid, 31, i_15, 'icon')
					G['MF_cleanremove'](thisid)
			else:
				thisid_2 = G['MF_create'](target_3)
				tiledata = G['tileslist'][target_3]
				root_3 = False
				if (tiledata['sprite_in_root'] is not None):
					root_3 = tiledata['sprite_in_root']
				if (G['objectcolours'][target_3] is not None):
					G['objectcolours'][target_3] = None
				if (this_3['name'] is not None):
					if (G['unitreference'][this_3['name']] is not None):
						uid_2 = G['unitreference'][this_3['name']]
						L_insert(namesetups, L_T([tiledata['name'], target_3]))
						G['unitreference'][tiledata['name']] = target_3
						G['unitreference'][this_3['name']] = None
				if ((this_3['argtype'] is not None) or (this_3['argextra'] is not None)):
					argtype__2 = this_3['argtype']
					argtype_3 = (_t1 if L_t(_t1 := tiledata['argtype']) else L_T([0]))
					argextra_3 = (_t2 if L_t(_t2 := tiledata['argextra']) else L_T())
					otype_3 = tiledata['type']
					if (G['conditions'][target_3] is not None):
						G['conditions'][target_3] = L_T()
						conddata_2 = G['conditions'][target_3]
						conddata_2['arguments'] = False
						if (otype_3 == 7):
							conddata_2['arguments'] = True
							conddata_2['argtype'] = L_T()
							for i_16, v_9 in L_ipairs(argtype_3):
								L_insert(conddata_2['argtype'], v_9)
							if (tiledata['argextra'] is not None):
								conddata_2['argextra'] = L_T()
								for i_17, v_10 in L_ipairs(argextra_3):
									L_insert(conddata_2['argextra'], v_10)
						elif (otype_3 != 3):
							G['conditions'][target_3] = None
				if (this_3['customobjects'] is not None):
					this_3['customobjects'] = None
					if (tiledata['customobjects'] is not None):
						G['customobjects'][target_3] = L_T()
						for i_18, v_11 in L_ipairs(tiledata['customobjects']):
							L_insert(G['customobjects'][target_3], v_11)
					else:
						G['customobjects'][target_3] = None
				G['MF_restoredefaults'](thisid_2, tiledata['sprite'], root_3)
				G['MF_cleanremove'](thisid_2)
		for i_19, v_12 in L_ipairs(namesetups):
			name_2 = v_12[1]
			uid_3 = v_12[2]
			G['unitreference'][name_2] = uid_3
		if (G['unitreference'] is not None):
			for i_20, v_13 in L_pairs(G['tileslist']):
				if (v_13['name'] is not None):
					name_3 = v_13['name']
					if (G['unitreference'][name_3] is None):
						G['unitreference'][name_3] = i_20
		G['changes'] = L_T()
		L_noop()
	G['restoredefaults'] = f_restoredefaults
	def f_dospritechanges(name_4=None, force_=None, *_):  # L535
		force = (_t1 if L_t(_t1 := force_) else False)
		if (G['tileslist'][name_4] is not None):
			thisid_3 = G['MF_create'](name_4)
			tiledata_2 = G['tileslist'][name_4]
			if (G['changes'][name_4] is not None):
				c = G['changes'][name_4]
				root_4 = False
				if (tiledata_2['sprite_in_root'] is not None):
					root_4 = tiledata_2['sprite_in_root']
				croot = root_4
				if (c['root'] is not None):
					croot = c['root']
				sprite = (_t2 if L_t(_t2 := (_t3 if L_t(_t3 := c['image']) else tiledata_2['sprite'])) else 'error')
				if ((c['image'] is not None) or (force is not None and force is not False)):
					G['MF_restoredefaults'](thisid_3, tiledata_2['sprite'], root_4)
					if (force is False):
						G['MF_changesprite'](thisid_3, c['image'], croot)
					else:
						G['MF_changesprite'](thisid_3, sprite, croot)
			G['MF_cleanremove'](thisid_3)
		else:
			L_noop(L_concat('No object with name ', name_4, ' (SPRITE)'))
	G['dospritechanges'] = f_dospritechanges
	def f_dochanges(unitid=None, *_):  # L574
		unit = G['mmf']['newObject'](unitid)
		realname = unit['className']
		name_5 = unit['strings'][G['UNITNAME']]
		name_ = ''
		if (G['changes'][realname] is not None):
			c_2 = G['changes'][realname]
			if (c_2['name'] is not None):
				name_5 = c_2['name']
				unit['strings'][G['UNITNAME']] = c_2['name']
				if (L_sub(c_2['name'], 1, 5) == 'text_'):
					name_ = L_sub(c_2['name'], 6)
				else:
					name_ = c_2['name']
				unit['strings'][G['NAME']] = name_
				G['unitreference'][name_5] = realname
			if (c_2['colour'] is not None):
				cutoff = 0
				for a_2 in L_range(1, L_strlen(c_2['colour'])):
					if (L_sub(c_2['colour'], a_2, a_2) == ','):
						cutoff = a_2
				if (cutoff > 0):
					c1 = L_sub(c_2['colour'], 1, (cutoff - 1))
					c2 = L_sub(c_2['colour'], (cutoff + 1))
					G['addobjectcolour'](realname, 'colour', c1, c2)
				else:
					L_noop('New object colour formatted wrong!')
			if (c_2['activecolour'] is not None):
				cutoff_2 = 0
				for a_3 in L_range(1, L_strlen(c_2['activecolour'])):
					if (L_sub(c_2['activecolour'], a_3, a_3) == ','):
						cutoff_2 = a_3
				if (cutoff_2 > 0):
					c1_2 = L_sub(c_2['activecolour'], 1, (cutoff_2 - 1))
					c2_2 = L_sub(c_2['activecolour'], (cutoff_2 + 1))
					G['addobjectcolour'](realname, 'active', c1_2, c2_2)
				else:
					L_noop('New object active colour formatted wrong!')
			if (c_2['tiling'] is not None):
				unit['values'][G['TILING']] = L_tonumber(c_2['tiling'])
			if (c_2['type'] is not None):
				unit['values'][G['TYPE']] = L_tonumber(c_2['type'])
			if (c_2['unittype'] is not None):
				unit['strings'][G['UNITTYPE']] = c_2['unittype']
			if (c_2['layer'] is not None):
				unit['values'][G['ZLAYER']] = L_tonumber(c_2['layer'])
	G['dochanges'] = f_dochanges
	def f_dochanges_allinstances(unitname=None, *_):  # L658
		for i_21, unit_2 in L_ipairs(G['units']):
			if (unit_2['className'] == unitname):
				G['dochanges'](unit_2['fixed'])
				G['updateunitcolour'](unit_2['fixed'], True)
	G['dochanges_allinstances'] = f_dochanges_allinstances
	def f_dochanges_full(name_6=None, *_):  # L667
		if (G['tileslist'][name_6] is not None):
			changedobjects_short_2 = ''
			for i_22, v_14 in L_pairs(G['changes']):
				changedobjects_short_2 = L_concat(changedobjects_short_2, L_sub(i_22, (-3)), ',')
			G['dospritechanges'](name_6)
			G['editor']['strings'][G['CHANGEDOBJECTS']] = changedobjects_short_2
			for i_23, unit_3 in L_ipairs(G['units']):
				if (unit_3['className'] == name_6):
					G['dochanges'](unit_3['fixed'], name_6)
					G['dynamic'](unit_3['fixed'])
		else:
			L_noop(L_concat('No object with name ', L_tostring(name_6), ' (FULL)'))
	G['dochanges_full'] = f_dochanges_full
	def f_resetchanges_objname(name_7=None, *_):  # L689
		unitid_2 = G['MF_create'](name_7)
		G['resetchanges'](unitid_2)
		G['MF_cleanremove'](unitid_2)
	G['resetchanges_objname'] = f_resetchanges_objname
	def f_resetchanges(unitid_3=None, *_):  # L697
		unit_4 = G['mmf']['newObject'](unitid_3)
		name_8 = unit_4['className']
		tiledata_3 = G['tileslist'][name_8]
		root_5 = False
		if (tiledata_3['sprite_in_root'] is not None):
			root_5 = tiledata_3['sprite_in_root']
		if (G['changes'][name_8] is not None):
			c_3 = G['changes'][name_8]
			if (c_3['name'] is not None):
				cname = c_3['name']
				rname = tiledata_3['name']
				G['unitreference'][cname] = None
				G['unitreference'][rname] = name_8
			if ((c_3['argtype'] is not None) or (c_3['argextra'] is not None)):
				argtype__3 = c_3['argtype']
				argtype_4 = (_t1 if L_t(_t1 := tiledata_3['argtype']) else L_T([0]))
				argextra_4 = (_t2 if L_t(_t2 := tiledata_3['argextra']) else L_T())
				otype_4 = tiledata_3['type']
				if (G['conditions'][name_8] is not None):
					G['conditions'][name_8] = L_T()
					conddata_3 = G['conditions'][name_8]
					conddata_3['arguments'] = False
					if (otype_4 == 7):
						conddata_3['arguments'] = True
						conddata_3['argtype'] = L_T()
						for i_24, v_15 in L_ipairs(argtype_4):
							L_insert(conddata_3['argtype'], v_15)
						if (tiledata_3['argextra'] is not None):
							conddata_3['argextra'] = L_T()
							for i_25, v_16 in L_ipairs(argextra_4):
								L_insert(conddata_3['argextra'], v_16)
					elif (otype_4 != 3):
						G['conditions'][name_8] = None
			if (c_3['customobjects'] is not None):
				c_3['customobjects'] = None
				if (tiledata_3['customobjects'] is not None):
					G['customobjects'][name_8] = L_T()
					for i_26, v_17 in L_ipairs(tiledata_3['customobjects']):
						L_insert(G['customobjects'][name_8], v_17)
				else:
					G['customobjects'][name_8] = None
			G['changes'][name_8] = None
		if (G['objectcolours'][name_8] is not None):
			G['objectcolours'][name_8] = None
		G['MF_restoredefaults'](unitid_3, tiledata_3['sprite'], root_5)
		G['getmetadata'](unit_4)
		G['updateunitcolour'](unitid_3, True)
		G['updatecolours'](True)
	G['resetchanges'] = f_resetchanges
	def f_addchange(unitid_4=None, *_):  # L781
		unit_5 = G['mmf']['newObject'](unitid_4)
		name_9 = unit_5['className']
		default_2 = G['tileslist'][name_9]
		things = L_T(['name', 'image', 'colour', 'tiling', 'type', 'unittype', 'activecolour', 'root', 'layer', 'argtype', 'argextra', 'customobjects'])
		allchanges = L_T()
		for i_27, v_18 in L_ipairs(things):
			result = ''
			data = G['MF_read']('level', 'tiles', L_concat(name_9, '_', v_18))
			if (L_strlen(data) > 0):
				result = data
			if (v_18 == 'root'):
				if (L_strlen(data) > 0):
					if (data == '1'):
						result = True
					elif (data == '0'):
						result = False
					else:
						G['MF_alert'](L_concat('Root contains garbage data in addchange() for ', default_2['name']))
				else:
					result = default_2['sprite_in_root']
			L_insert(allchanges, result)
		G['savechange'](name_9, allchanges, unitid_4)
	G['addchange'] = f_addchange
	def f_getactualdata(objectname=None, param_=None, *_):  # L819
		data_2 = (_t1 if L_t(_t1 := G['tileslist'][objectname]) else L_T())
		result_2 = None
		param = param_
		diffs = L_T([], {'sprite': 'image', 'sprite_in_root': 'root', 'active': 'activecolour'})
		if (data_2 is not None):
			result_2 = data_2[param]
			if ((param == 'active') and (data_2[param] is None)):
				result_2 = data_2['colour']
			if (G['changes'][objectname] is not None):
				c_4 = G['changes'][objectname]
				if (diffs[param] is not None):
					param = diffs[param]
				if ((param == 'activecolour') and (c_4[param] is None)):
					param = 'colour'
				if (c_4[param] is not None):
					if ((param == 'colour') or (param == 'activecolour')):
						result_2 = G['MF_parsestring'](c_4[param])
					else:
						result_2 = c_4[param]
		else:
			G['MF_alert'](L_concat('No data found for object ', L_tostring(objectname), ' (parameter ', L_tostring(param), ')'))
		return result_2
	G['getactualdata'] = f_getactualdata
	def f_getactualdata_objlist(objectname_2=None, param__2=None, *_):  # L864
		tileslistdata = (_t1 if L_t(_t1 := G['tileslist'][objectname_2]) else L_T())
		changesdata = (_t2 if L_t(_t2 := G['changes'][objectname_2]) else L_T())
		objlistdata = L_T()
		for i_28, obj in L_ipairs(G['editor_currobjlist']):
			if (obj['object'] == objectname_2):
				objid = (_t3 if L_t(_t3 := L_tonumber(obj['id'])) else obj['id'])
				objlistdata = G['editor_objlist'][objid]
				if (objlistdata is None):
					G['MF_alert'](L_concat('Objlistdata is nil for ', L_tostring(objid), ', ', objectname_2))
					objlistdata = L_T()
				break
		result_3 = None
		modded = False
		if (objlistdata is None):
			G['MF_alert'](L_concat('objlistdata is nil, ', objectname_2))
		param_2 = param__2
		changediffs = L_T([], {'sprite': 'image', 'sprite_in_root': 'root', 'active': 'activecolour'})
		changesparam = (_t4 if L_t(_t4 := changediffs[param_2]) else param_2)
		objlistdiffs = L_T([], {'active': 'colour_active'})
		objlistparam = (_t5 if L_t(_t5 := objlistdiffs[param_2]) else param_2)
		tileslistresult = tileslistdata[param_2]
		changesresult = changesdata[changesparam]
		objlistresult = objlistdata[objlistparam]
		if ((param_2 == 'sprite') and (objlistresult is None)):
			objlistresult = (_t6 if L_t(_t6 := objlistdata['name']) else None)
		if (((param_2 == 'colour') or (param_2 == 'active')) and (changesresult is not None)):
			changesresult = G['MF_parsestring'](changesresult)
		if (changesresult is None):
			if (tileslistresult is None):
				result_3 = objlistresult
			else:
				result_3 = tileslistresult
		else:
			result_3 = changesresult
			if ((param_2 != 'colour') and (param_2 != 'active')):
				modtest = objlistresult
				if (objlistresult is None):
					if (tileslistresult is not None):
						modtest = tileslistresult
					else:
						modtest = None
				if ((modtest is not None) and (L_tostring(L_type(modtest)) == L_tostring(L_type(changesresult)))):
					if (L_tostring(L_type(modtest)) != 'table'):
						if (changesresult != modtest):
							modded = True
					else:
						matching = True
						for i_29, v_19 in L_ipairs(modtest):
							if (changesresult[i_29] != v_19):
								matching = False
						if (matching is False):
							modded = True
		return (result_3, modded,)
		return ()
	G['getactualdata_objlist'] = f_getactualdata_objlist
	def f_editor_resetobject(unitid_5=None, tilename=None, objlistid_=None, *_):  # L965
		data_3 = None
		objlistid = (-1)
		for i_30, v_20 in L_pairs(G['editor_currobjlist']):
			if (v_20['object'] == tilename):
				data_3 = G['editor_objlist'][v_20['id']]
				objlistid = i_30
		if (data_3 is not None):
			G['resetchanges'](unitid_5)
			colourstring = '0,3'
			if (data_3['colour'] is not None):
				c_5 = data_3['colour']
				colourstring = L_concat(L_tostring(c_5[1]), ',', L_tostring(c_5[2]))
			c1_3 = G['MF_parsestring'](colourstring)
			activecolourstring = '0,3'
			if (data_3['colour_active'] is not None):
				c_6 = data_3['colour_active']
				activecolourstring = L_concat(L_tostring(c_6[1]), ',', L_tostring(c_6[2]))
			c2_3 = G['MF_parsestring'](activecolourstring)
			argtypestring = '0'
			if (data_3['argtype'] is not None):
				c_7 = data_3['argtype']
				argtypestring = G['gettablestring'](c_7)
			argextrastring = ''
			if (data_3['argextra'] is not None):
				c_8 = data_3['argextra']
				argextrastring = G['gettablestring'](c_8)
			customobjectsstring = ''
			if (data_3['customobjects'] is not None):
				c_9 = data_3['customobjects']
				customobjectsstring = G['gettablestring'](c_9)
			c_name = data_3['name']
			c_image = (_t1 if L_t(_t1 := data_3['sprite']) else data_3['name'])
			c_colour = colourstring
			c_tiling = (_t2 if L_t(_t2 := data_3['tiling']) else (-1))
			c_type = (_t3 if L_t(_t3 := data_3['type']) else 0)
			c_unittype = (_t4 if L_t(_t4 := data_3['unittype']) else 'object')
			c_activecolour = activecolourstring
			c_root = (_t5 if L_t(_t5 := data_3['sprite_in_root']) else True)
			c_layer = (_t6 if L_t(_t6 := data_3['layer']) else 10)
			c_argtype = argtypestring
			c_argextra = argextrastring
			c_customobjects = customobjectsstring
			changelist = L_T([c_name, c_image, c_colour, c_tiling, c_type, c_unittype, c_activecolour, c_root, c_layer, c_argtype, c_argextra, c_customobjects])
			G['savechange'](tilename, changelist, unitid_5)
			G['dochanges_allinstances'](tilename)
			G['dospritechanges'](tilename)
			c_ = c1_3
			if (c_unittype == 'text'):
				c_ = c2_3
			objlistdata_2 = G['editor_currobjlist'][objlistid]
			objlistdata_2['name'] = c_name
			if (objlistid_ is not None):
				G['MF_updateobjlistname_hack'](objlistid_, c_name)
			return (c_[1], c_[2], L_concat(c_image, '_0_1'), c_root, c_name,)
		else:
			G['MF_alert'](L_concat('No data found for ', tilename))
		return ()
	G['editor_resetobject'] = f_editor_resetobject
	def f_handleobjectchanges(*_):  # L1051
		changelists = (_t1 if L_t(_t1 := L_tonumber(G['MF_read']('level', 'tiles', 'changed_count'))) else 1)
		changelists = L_max(changelists, 1)
		for i_31 in L_range(1, changelists):
			id__2 = 'changed'
			if (i_31 > 1):
				id__2 = L_concat(id__2, L_tostring(i_31))
			changestring = G['MF_read']('level', 'tiles', id__2)
			if (L_len(changestring) > 0):
				for obj_2 in L_gmatch(changestring, '%w+'):
					if (((L_sub(obj_2, 1, 6) == 'object') and (L_strlen(obj_2) == 9)) and (L_tonumber(L_sub(obj_2, (-3))) is not None)):
						G['dochanges_full'](obj_2)
	G['handleobjectchanges'] = f_handleobjectchanges
