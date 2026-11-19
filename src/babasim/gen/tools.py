"""Generated from tools.lua by tools/lua2py.py. Do not edit."""
from babasim.luart import *  # noqa: F403


def load(G):
	if (G['fixed_to_str'] is None):
		G['fixed_to_str'] = G['tostring']
	def f_rotate(dir_=None, *_):  # L5
		rot = L_T([2, 3, 0, 1, 4])
		return rot[(dir_ + 1)]
	G['rotate'] = f_rotate
	def f_isthis(lookup=None, rule=None, *_):  # L11
		for i, rules in L_ipairs(lookup):
			baserule = rules[1]
			if ((baserule[3] == rule) and (baserule[2] == 'is')):
				return True
		return False
	G['isthis'] = f_isthis
	def f_xthis(lookup_2=None, name=None, rule_2=None, *_):  # L23
		result = L_T()
		for i_2, rules_2 in L_ipairs(lookup_2):
			baserule_2 = rules_2[1]
			if ((baserule_2[1] == name) and (baserule_2[2] == rule_2)):
				L_insert(result, baserule_2[3])
		return result
	G['xthis'] = f_xthis
	def f_findall(name_=None, ignorebroken_=None, just_testing_=None, *_):  # L37
		result_2 = L_T()
		name_2 = name_[1]
		meta = True
		checklist = G['unitlists'][name_2]
		if (name_2 == 'text'):
			checklist = G['codeunits']
			meta = False
		ignorebroken = (_t1 if L_t(_t1 := ignorebroken_) else False)
		just_testing = (_t2 if L_t(_t2 := just_testing_) else False)
		if (checklist is not None):
			for i_3, unitid in L_ipairs(checklist):
				unit = G['mmf']['newObject'](unitid)
				unitname = G['getname'](unit, meta)
				oldbroken = unit['broken']
				if (ignorebroken is not None and ignorebroken is not False):
					unit['broken'] = 0
				if (unitname == name_2):
					if L_t(G['testcond'](name_[2], unitid)):
						L_insert(result_2, unitid)
						if (just_testing is not None and just_testing is not False):
							return result_2
				unit['broken'] = oldbroken
		return result_2
	G['findall'] = f_findall
	def f_delunit(unitid_2=None, *_):  # L79
		unit_2 = G['mmf']['newObject'](unitid_2)
		if (unit_2 is not None):
			name_3 = G['getname'](unit_2)
			x, y = unit_2['values'][G['XPOS']], unit_2['values'][G['YPOS']]
			unitlist = G['unitlists'][name_3]
			unitlist_ = (_t1 if L_t(_t1 := G['unitlists'][unit_2['strings'][G['UNITNAME']]]) else L_T())
			unittype = unit_2['strings'][G['UNITTYPE']]
			if (unittype == 'text'):
				G['updatecode'] = 1
			x = L_floor(x)
			y = L_floor(y)
			if (unitlist is not None):
				for i_4, v in L_pairs(unitlist):
					if (v == unitid_2):
						v = L_T()
						L_remove(unitlist, i_4)
						break
			if (unitlist_ is not None):
				for i_5, v_2 in L_pairs(unitlist_):
					if (v_2 == unitid_2):
						v_2 = L_T()
						L_remove(unitlist_, i_5)
						break
			tileid = (x + (y * G['roomsizex']))
			if (G['unitmap'][tileid] is not None):
				for i_6, v_3 in L_pairs(G['unitmap'][tileid]):
					if (v_3 == unitid_2):
						v_3 = L_T()
						L_remove(G['unitmap'][tileid], i_6)
				if (L_len(G['unitmap'][tileid]) == 0):
					G['unitmap'][tileid] = None
			if (G['unittypeshere'][tileid] is not None):
				uth = G['unittypeshere'][tileid]
				n = unit_2['strings'][G['UNITNAME']]
				if (uth[n] is not None):
					uth[n] = (uth[n] - 1)
					if (uth[n] == 0):
						uth[n] = None
			if ((unit_2['strings'][G['UNITTYPE']] == 'text') and (G['codeunits'] is not None)):
				for i_7, v_4 in L_pairs(G['codeunits']):
					if (v_4 == unitid_2):
						v_4 = L_T()
						L_remove(G['codeunits'], i_7)
				if (unit_2['values'][G['TYPE']] == 5):
					for i_8, v_5 in L_pairs(G['letterunits']):
						if (v_5 == unitid_2):
							v_5 = L_T()
							L_remove(G['letterunits'], i_8)
			if ((unit_2['values'][G['TILING']] > 1) and (G['animunits'] is not None)):
				for i_9, v_6 in L_pairs(G['animunits']):
					if (v_6 == unitid_2):
						v_6 = L_T()
						L_remove(G['animunits'], i_9)
			if ((unit_2['values'][G['TILING']] == 1) and (G['tiledunits'] is not None)):
				for i_10, v_7 in L_pairs(G['tiledunits']):
					if (v_7 == unitid_2):
						v_7 = L_T()
						L_remove(G['tiledunits'], i_10)
			if (((L_len(G['wordunits']) > 0) and (unit_2['values'][G['TYPE']] == 0)) and (unit_2['strings'][G['UNITTYPE']] != 'text')):
				for i_11, v_8 in L_pairs(G['wordunits']):
					if (v_8[1] == unitid_2):
						currentundo = G['undobuffer'][1]
						L_insert(currentundo['wordunits'], unit_2['values'][G['ID']])
						G['updatecode'] = 1
						v_8 = L_T()
						L_remove(G['wordunits'], i_11)
			if (L_len(G['wordrelatedunits']) > 0):
				for i_12, v_9 in L_pairs(G['wordrelatedunits']):
					if (v_9[1] == unitid_2):
						currentundo_2 = G['undobuffer'][1]
						L_insert(currentundo_2['wordrelatedunits'], unit_2['values'][G['ID']])
						G['updatecode'] = 1
						v_9 = L_T()
						L_remove(G['wordrelatedunits'], i_12)
			if (L_len(G['visiontargets']) > 0):
				for i_13, v_10 in L_pairs(G['visiontargets']):
					if (v_10 == unitid_2):
						currentundo_3 = G['undobuffer'][1]
						v_10 = L_T()
						L_remove(G['visiontargets'], i_13)
		else:
			G['MF_alert'](L_concat('delunit(): no object found with id ', L_tostring(unitid_2), ' (delunit)'))
		for i_14, v_11 in L_ipairs(G['units']):
			if (v_11['fixed'] == unitid_2):
				v_11 = L_T()
				L_remove(G['units'], i_14)
		for i_15, data in L_pairs(G['updatelist']):
			if ((data[1] == unitid_2) and (data[2] != 'convert')):
				data[2] = 'DELETED'
	G['delunit'] = f_delunit
	def f_findtype(typedata=None, x_2=None, y_2=None, unitid_=None, just_testing__2=None, *_):  # L236
		result_3 = L_T()
		unitid_3 = 0
		tileid_2 = (x_2 + (y_2 * G['roomsizex']))
		name_4 = typedata[1]
		conds = typedata[2]
		just_testing_2 = (_t1 if L_t(_t1 := just_testing__2) else False)
		if (unitid_ is not None):
			unitid_3 = unitid_
		if (G['unitmap'][tileid_2] is not None):
			for i_16, v_12 in L_ipairs(G['unitmap'][tileid_2]):
				if (v_12 != unitid_3):
					unit_3 = G['mmf']['newObject'](v_12)
					if ((unit_3['strings'][G['UNITNAME']] == name_4) or ((unit_3['strings'][G['UNITTYPE']] == 'text') and (name_4 == 'text'))):
						if L_t(G['testcond'](conds, v_12)):
							L_insert(result_3, v_12)
							if (just_testing_2 is not None and just_testing_2 is not False):
								return result_3
		return result_3
	G['findtype'] = f_findtype
	def f_findobstacle(x_3=None, y_3=None, *_):  # L270
		if L_t(G['inbounds'](x_3, y_3)):
			layer = G['map'][0]
			tile = L_invoke(layer, 'get_x', x_3, y_3)
			result_4 = L_T()
			tileid_3 = (x_3 + (y_3 * G['roomsizex']))
			if (tile != 255):
				L_insert(result_4, (-1))
			if (G['unitmap'][tileid_3] is not None):
				for i_17, v_13 in L_ipairs(G['unitmap'][tileid_3]):
					unit_4 = G['mmf']['newObject'](v_13)
					if (unit_4['flags'][G['DEAD']] is False):
						L_insert(result_4, v_13)
					else:
						G['MF_alert'](L_concat('Unitmap: found removed unit ', unit_4['strings'][G['UNITNAME']]))
			return result_4
		else:
			return L_T([(-1)])
	G['findobstacle'] = f_findobstacle
	def f_update(unitid_4=None, x_4=None, y_4=None, dir__2=None, *_):  # L299
		if (unitid_4 is not None):
			unit_5 = G['mmf']['newObject'](unitid_4)
			unitname_2 = unit_5['strings'][G['UNITNAME']]
			dir__3, olddir = unit_5['values'][G['DIR']], unit_5['values'][G['DIR']]
			tiling = unit_5['values'][G['TILING']]
			unittype_2 = unit_5['strings'][G['UNITTYPE']]
			oldx, oldy = unit_5['values'][G['XPOS']], unit_5['values'][G['YPOS']]
			if (dir__2 is not None):
				dir__3 = dir__2
			if (((x_4 != oldx) or (y_4 != oldy)) or (dir__3 != olddir)):
				G['updateundo'] = True
				G['addundo'](L_T(['update', unitname_2, oldx, oldy, olddir, x_4, y_4, dir__3, unit_5['values'][G['ID']]]), unitid_4)
				ox, oy = (x_4 - oldx), (y_4 - oldy)
				if (((abs(ox) + abs(oy)) == 1) and (unit_5['values'][G['MOVED']] == 0)):
					unit_5['x'] = (unit_5['x'] + ((((ox * G['tilesize']) * G['spritedata']['values'][G['TILEMULT']]) * G['generaldata2']['values'][G['ZOOM']]) * 0.25))
					unit_5['y'] = (unit_5['y'] + ((((oy * G['tilesize']) * G['spritedata']['values'][G['TILEMULT']]) * G['generaldata2']['values'][G['ZOOM']]) * 0.25))
				unit_5['values'][G['XPOS']] = x_4
				unit_5['values'][G['YPOS']] = y_4
				unit_5['values'][G['DIR']] = dir__3
				unit_5['values'][G['MOVED']] = 1
				unit_5['values'][G['POSITIONING']] = 0
				G['updateunitmap'](unitid_4, oldx, oldy, x_4, y_4, unit_5['strings'][G['UNITNAME']])
				if (tiling == 1):
					G['dynamic'](unitid_4)
					G['dynamicat'](oldx, oldy)
				if (unittype_2 == 'text'):
					G['updatecode'] = 1
				if (G['featureindex']['word'] is not None):
					G['checkwordchanges'](unitid_4, unitname_2)
		else:
			G['MF_alert']('Tried to update a nil unit')
	G['update'] = f_update
	def f_updatedir(unitid_5=None, dir__4=None, noundo_=None, *_):  # L351
		if (unitid_5 is not None):
			unit_6 = G['mmf']['newObject'](unitid_5)
			x_5, y_5 = unit_6['values'][G['XPOS']], unit_6['values'][G['YPOS']]
			unitname_3 = unit_6['strings'][G['UNITNAME']]
			unittype_3 = unit_6['strings'][G['UNITTYPE']]
			olddir_2 = unit_6['values'][G['DIR']]
			noundo = (_t1 if L_t(_t1 := noundo_) else False)
			if (dir__4 != olddir_2):
				if (noundo is False):
					G['updateundo'] = True
					G['addundo'](L_T(['update', unitname_3, x_5, y_5, olddir_2, x_5, y_5, dir__4, unit_6['values'][G['ID']]]), unitid_5)
				unit_6['values'][G['DIR']] = dir__4
				if (unittype_3 == 'text'):
					G['updatecode'] = 1
		else:
			G['MF_alert']('Tried to updatedir a nil unit')
	G['updatedir'] = f_updatedir
	def f_findtext(x_6=None, y_6=None, *_):  # L377
		result_5 = L_T()
		tileid_4 = (x_6 + (y_6 * G['roomsizex']))
		if (G['unitmap'][tileid_4] is not None):
			for i_18, v_14 in L_ipairs(G['unitmap'][tileid_4]):
				unit_7 = G['mmf']['newObject'](v_14)
				if (unit_7['strings'][G['UNITTYPE']] == 'text'):
					L_insert(result_5, v_14)
		return result_5
	G['findtext'] = f_findtext
	def f_findallhere(x_7=None, y_7=None, exclude_=None, fpaths_=None, *_):  # L394
		result_6 = L_T()
		exclude = 0
		if (exclude_ is not None):
			exclude = exclude_
		fpaths = False
		if (fpaths_ is not None):
			fpaths = fpaths_
		tileid_5 = (x_7 + (y_7 * G['roomsizex']))
		if (G['unitmap'][tileid_5] is not None):
			for i_19, unitid_6 in L_ipairs(G['unitmap'][tileid_5]):
				if (unitid_6 != exclude):
					L_insert(result_6, unitid_6)
		if (fpaths is not None and fpaths is not False):
			pathshere = G['MF_findpaths'](x_7, y_7)
			if (L_len(pathshere) > 0):
				for i_20, v_15 in L_ipairs(pathshere):
					L_insert(result_6, v_15)
		return result_6
	G['findallhere'] = f_findallhere
	def f_findempty(conds_=None, checkonly_=None, *_):  # L430
		result_7 = L_T()
		array = L_T()
		layer_2 = G['map'][0]
		conds_2 = (_t1 if L_t(_t1 := conds_) else L_T())
		checkonly = False
		if (checkonly_ is not None):
			checkonly = checkonly_
		for i_21, unit_8 in L_ipairs(G['units']):
			x_8, y_8 = unit_8['values'][G['XPOS']], unit_8['values'][G['YPOS']]
			arrayid = (x_8 + (y_8 * G['roomsizex']))
			if (array[arrayid] is None):
				array[arrayid] = L_T()
				L_insert(array[arrayid], unit_8['fixed'])
		for i_22 in L_range(0, (G['roomsizex'] - 1)):
			for j in L_range(0, (G['roomsizey'] - 1)):
				empty = 1
				tile_2 = L_invoke(layer_2, 'get_x', i_22, j)
				arrayid_2 = (i_22 + (j * G['roomsizex']))
				if ((tile_2 != 255) or (array[arrayid_2] is not None)):
					empty = 0
				if (empty == 1):
					if ((L_len(conds_2) == 0) or ((L_len(conds_2) > 0) and L_t(G['testcond'](conds_2, 2, i_22, j)))):
						L_insert(result_7, (i_22 + (j * G['roomsizex'])))
						if (checkonly is not None and checkonly is not False):
							return result_7
		return result_7
	G['findempty'] = f_findempty
	def f_handleinside(unitid_7=None, x_=None, y_=None, *_):  # L477
		unit_9 = L_T()
		x_9, y_9, dir__5 = 0, 0, 4
		unitname_4 = ''
		insidename = ''
		leveldata = L_T()
		if (unitid_7 != 2):
			unit_9 = G['mmf']['newObject'](unitid_7)
			x_9, y_9, dir__5 = unit_9['values'][G['XPOS']], unit_9['values'][G['YPOS']], unit_9['values'][G['DIR']]
			unitname_4 = unit_9['strings'][G['UNITNAME']]
			insidename = G['getname'](unit_9)
		else:
			x_9, y_9 = x_, y_
			unitname_4 = 'empty'
			insidename = 'empty'
		x_9 = L_floor(x_9)
		y_9 = L_floor(y_9)
		if L_t(G['inbounds'](x_9, y_9, 1)):
			if (unitid_7 == 2):
				dir__5 = G['emptydir'](x_9, y_9)
			else:
				leveldata = L_T([unit_9['strings'][G['U_LEVELFILE']], unit_9['strings'][G['U_LEVELNAME']], unit_9['flags'][G['MAPLEVEL']], unit_9['values'][G['VISUALLEVEL']], unit_9['values'][G['VISUALSTYLE']], unit_9['values'][G['COMPLETED']], unit_9['strings'][G['COLOUR']], unit_9['strings'][G['CLEARCOLOUR']]])
			G['inside'](insidename, x_9, y_9, dir__5, unitid_7, leveldata)
	G['handleinside'] = f_handleinside
	def f_delete(unitid_8=None, x__2=None, y__2=None, total_=None, noinside_=None, *_):  # L509
		total = (_t1 if L_t(_t1 := total_) else False)
		noinside = (_t2 if L_t(_t2 := noinside_) else False)
		check = unitid_8
		if (unitid_8 == 2):
			check = ((200 + x__2) + (y__2 * G['roomsizex']))
		if (G['deleted'][check] is None):
			unit_10 = L_T()
			x_10, y_10, dir__6 = 0, 0, 4
			unitname_5 = ''
			insidename_2 = ''
			if (unitid_8 != 2):
				unit_10 = G['mmf']['newObject'](unitid_8)
				x_10, y_10, dir__6 = unit_10['values'][G['XPOS']], unit_10['values'][G['YPOS']], unit_10['values'][G['DIR']]
				unitname_5 = unit_10['strings'][G['UNITNAME']]
				insidename_2 = G['getname'](unit_10)
			else:
				x_10, y_10 = x__2, y__2
				unitname_5 = 'empty'
				insidename_2 = 'empty'
			x_10 = L_floor(x_10)
			y_10 = L_floor(y_10)
			if (((total is False) and L_t(G['inbounds'](x_10, y_10, 1))) and (noinside is False)):
				leveldata_2 = L_T()
				if (unitid_8 == 2):
					dir__6 = G['emptydir'](x_10, y_10)
				else:
					leveldata_2 = L_T([unit_10['strings'][G['U_LEVELFILE']], unit_10['strings'][G['U_LEVELNAME']], unit_10['flags'][G['MAPLEVEL']], unit_10['values'][G['VISUALLEVEL']], unit_10['values'][G['VISUALSTYLE']], unit_10['values'][G['COMPLETED']], unit_10['strings'][G['COLOUR']], unit_10['strings'][G['CLEARCOLOUR']]])
				G['inside'](insidename_2, x_10, y_10, dir__6, unitid_8, leveldata_2)
			if (unitid_8 != 2):
				if (G['spritedata']['values'][G['CAMTARGET']] == unit_10['values'][G['ID']]):
					G['changevisiontarget'](unit_10['fixed'])
				G['addundo'](L_T(['remove', unitname_5, x_10, y_10, dir__6, unit_10['values'][G['ID']], unit_10['values'][G['ID']], unit_10['strings'][G['U_LEVELFILE']], unit_10['strings'][G['U_LEVELNAME']], unit_10['values'][G['VISUALLEVEL']], unit_10['values'][G['COMPLETED']], unit_10['values'][G['VISUALSTYLE']], unit_10['flags'][G['MAPLEVEL']], unit_10['strings'][G['COLOUR']], unit_10['strings'][G['CLEARCOLOUR']], unit_10['followed'], unit_10['back_init'], unit_10['originalname'], unit_10['strings'][G['UNITSIGNTEXT']], unit_10['holder']]), unitid_8)
				unit_10 = L_T()
				G['delunit'](unitid_8)
				G['MF_remove'](unitid_8)
				if L_t(G['inbounds'](x_10, y_10, 1)):
					G['dynamicat'](x_10, y_10)
			G['deleted'][check] = 1
		else:
			G['MF_alert']('already deleted')
	G['delete'] = f_delete
	def f_writerules(parent=None, name_5=None, x__3=None, y__3=None, *_):  # L574
		basex = x__3
		basey = y__3
		linelimit = 12
		maxcolumns = 4
		x_11, y_11 = basex, basey
		if (L_len(G['visualfeatures']) > 0):
			G['writetext'](G['langtext']('rules_colon'), 0, x_11, y_11, name_5, True, 2, True)
		i_ = 1
		count = 0
		allrules = L_T()
		custom = G['MF_read']('level', 'general', 'customruleword')
		for i_23, rules_3 in L_ipairs(G['visualfeatures']):
			text = ''
			rule_3 = rules_3[1]
			if (L_len(custom) == 0):
				text = L_concat(text, rule_3[1], ' ')
			else:
				text = L_concat(text, custom, ' ')
			conds_3 = rules_3[2]
			ids = rules_3[3]
			tags = rules_3[4]
			fullinvis = True
			for a, b in L_ipairs(ids):
				for c, d in L_ipairs(b):
					dunit = G['mmf']['newObject'](d)
					if L_t(dunit['visible']):
						fullinvis = False
						break
			for a_2, b_2 in L_ipairs(tags):
				if ((L_sub(b_2, 1, 12) == 'mimicparent_') and (G['featureindex']['mimic'] is not None)):
					id_ = L_tonumber(L_sub(b_2, (-1)))
					parent_2 = G['featureindex']['mimic'][id_]
					if (parent_2 is not None):
						ids_ = parent_2[3]
						finvis = True
						for a_3, b_ in L_ipairs(ids_):
							for c_2, d_2 in L_ipairs(b_):
								dunit_2 = G['mmf']['newObject'](d_2)
								if L_t(dunit_2['visible']):
									finvis = False
									break
						if (finvis is not None and finvis is not False):
							fullinvis = True
					break
			if (fullinvis is False):
				if (L_len(conds_3) > 0):
					for a_4, cond in L_ipairs(conds_3):
						middlecond = True
						if ((cond[2] is None) or ((cond[2] is not None) and (L_len(cond[2]) == 0))):
							middlecond = False
						if (middlecond is not None and middlecond is not False):
							if (L_len(custom) == 0):
								target = cond[1]
								isnot = L_sub(target, 1, 4)
								target_ = target
								if (isnot == 'not '):
									target_ = L_sub(target, 5)
								else:
									isnot = ''
								if (G['word_names'][target_] is not None):
									target = L_concat(isnot, G['word_names'][target_])
								text = L_concat(text, target, ' ')
							else:
								text = L_concat(text, custom, ' ')
							if (cond[2] is not None):
								if (L_len(cond[2]) > 0):
									for c_3, d_3 in L_ipairs(cond[2]):
										if (L_len(custom) == 0):
											target_2 = d_3
											isnot_2 = L_sub(target_2, 1, 4)
											target__2 = target_2
											if (isnot_2 == 'not '):
												target__2 = L_sub(target_2, 5)
											else:
												isnot_2 = ''
											if (G['word_names'][target__2] is not None):
												target_2 = L_concat(isnot_2, G['word_names'][target__2])
											text = L_concat(text, target_2, ' ')
										else:
											text = L_concat(text, custom, ' ')
										if ((L_len(cond[2]) > 1) and (c_3 != L_len(cond[2]))):
											text = L_concat(text, '& ')
							if (a_4 < L_len(conds_3)):
								text = L_concat(text, '& ')
						else:
							if (L_len(custom) == 0):
								text = L_concat(cond[1], ' ', text)
							else:
								text = L_concat(custom, ' ', text)
				target_3 = rule_3[3]
				isnot_3 = L_sub(target_3, 1, 4)
				target__3 = target_3
				if (isnot_3 == 'not '):
					target__3 = L_sub(target_3, 5)
				else:
					isnot_3 = ''
				if (G['word_names'][target__3] is not None):
					target_3 = L_concat(isnot_3, G['word_names'][target__3])
				if (L_len(custom) == 0):
					text = L_concat(text, rule_3[2], ' ', target_3)
				else:
					text = L_concat(text, custom, ' ', custom)
				for a_5, b_3 in L_ipairs(tags):
					if (b_3 == 'mimic'):
						text = L_concat(text, ' (mimic)')
				if (allrules[text] is None):
					allrules[text] = 1
					count = (count + 1)
				else:
					allrules[text] = (allrules[text] + 1)
				i_ = (i_ + 1)
		columns = L_min(maxcolumns, (L_floor(L_div((count - 1), linelimit)) + 1))
		columnwidth = L_div(L_min((G['screenw'] - (G['f_tilesize'] * 2)), ((columns * G['f_tilesize']) * 10)), columns)
		i_ = 1
		maxlimit = (4 * linelimit)
		for i_24, v_16 in L_pairs(allrules):
			text_2 = i_24
			if (i_ <= maxlimit):
				currcolumn = (L_floor(L_div((i_ - 1), linelimit)) - (columns * 0.5))
				x_11 = ((basex + (columnwidth * currcolumn)) + (columnwidth * 0.5))
				y_11 = (basey + (((((i_ - 1) % linelimit) + 1) * G['f_tilesize']) * 0.8))
			if (i_ <= (maxlimit - 1)):
				if (v_16 == 1):
					G['writetext'](text_2, 0, x_11, y_11, name_5, True, 2, True)
				elif (v_16 > 1):
					G['writetext'](L_concat(L_tostring(v_16), ' x ', text_2), 0, x_11, y_11, name_5, True, 2, True)
			i_ = (i_ + 1)
		if (i_ > (maxlimit - 1)):
			G['writetext'](L_concat('(+ ', L_tostring((i_ - maxlimit)), ')'), 0, x_11, y_11, name_5, True, 2, True)
	G['writerules'] = f_writerules
	def f_mapcells(*_):  # L788
		count_2 = 0
		for i_25, v_17 in L_pairs(G['unitmap']):
			if (L_len(v_17) > 0):
				count_2 = (count_2 + 1)
		return count_2
	G['mapcells'] = f_mapcells
	def f_copy(unitid_9=None, x_12=None, y_12=None, *_):  # L800
		for i_26, unit_11 in L_ipairs(G['units']):
			if (unit_11['fixed'] == unitid_9):
				oldx_2, oldy_2, dir__7, name_6, float_ = unit_11['values'][G['XPOS']], unit_11['values'][G['YPOS']], unit_11['values'][G['DIR']], unit_11['strings'][G['UNITNAME']], unit_11['values'][G['FLOAT']]
				leveldata_3 = L_T([unit_11['strings'][G['U_LEVELFILE']], unit_11['strings'][G['U_LEVELNAME']], unit_11['flags'][G['MAPLEVEL']], unit_11['values'][G['VISUALLEVEL']], unit_11['values'][G['VISUALSTYLE']], unit_11['values'][G['COMPLETED']], unit_11['strings'][G['COLOUR']], unit_11['strings'][G['CLEARCOLOUR']]])
				this = L_first(G['create'](name_6, x_12, y_12, dir__7, oldx_2, oldy_2, float_, None, leveldata_3))
				return this
	G['copy'] = f_copy
	def f_create(name_7=None, x_13=None, y_13=None, dir__8=None, oldx_=None, oldy_=None, float__2=None, skipundo_=None, leveldata_=None, *_):  # L813
		oldx_3, oldy_3, float__3 = x_13, y_13, 0
		tileid_6 = (x_13 + (y_13 * G['roomsizex']))
		if (oldx_ is not None):
			oldx_3 = oldx_
		if (oldy_ is not None):
			oldy_3 = oldy_
		if (float__2 is not None):
			float__3 = float__2
		skipundo = (_t1 if L_t(_t1 := skipundo_) else False)
		unitname_6 = G['unitreference'][name_7]
		if (unitname_6 is None):
			unitname_6 = 'error'
			G['MF_alert'](L_concat("Couldn't find object for ", L_tostring(name_7), '!'))
		newunitid = G['MF_emptycreate'](unitname_6, oldx_3, oldy_3)
		newunit = G['mmf']['newObject'](newunitid)
		id__2 = G['newid']()
		newunit['values'][G['ONLINE']] = 1
		newunit['values'][G['XPOS']] = x_13
		newunit['values'][G['YPOS']] = y_13
		newunit['values'][G['DIR']] = dir__8
		newunit['values'][G['ID']] = id__2
		newunit['values'][G['FLOAT']] = float__3
		newunit['flags'][G['CONVERTED']] = True
		if ((leveldata_ is not None) and (L_len(leveldata_) > 0)):
			newunit['strings'][G['U_LEVELFILE']] = leveldata_[1]
			newunit['strings'][G['U_LEVELNAME']] = leveldata_[2]
			newunit['flags'][G['MAPLEVEL']] = leveldata_[3]
			newunit['values'][G['VISUALLEVEL']] = leveldata_[4]
			newunit['values'][G['VISUALSTYLE']] = leveldata_[5]
			newunit['values'][G['COMPLETED']] = leveldata_[6]
			newunit['strings'][G['COLOUR']] = leveldata_[7]
			newunit['strings'][G['CLEARCOLOUR']] = leveldata_[8]
			if (newunit['className'] == 'level'):
				if (L_len(leveldata_[1]) > 0):
					newunit['values'][G['COMPLETED']] = L_max(leveldata_[6], 2)
				else:
					newunit['values'][G['COMPLETED']] = L_max(leveldata_[6], 1)
				if ((L_len(leveldata_[7]) == 0) or (L_len(leveldata_[8]) == 0)):
					newunit['strings'][G['COLOUR']] = '1,2'
					newunit['strings'][G['CLEARCOLOUR']] = '1,3'
					G['MF_setcolour'](newunitid, 1, 2)
				else:
					c_4 = G['MF_parsestring'](leveldata_[7])
					G['MF_setcolour'](newunitid, c_4[1], c_4[2])
			elif (L_len(leveldata_[7]) > 0):
				c_5 = G['MF_parsestring'](leveldata_[7])
				G['MF_setcolour'](newunitid, c_5[1], c_5[2])
		newunit['flags'][9] = True
		if (skipundo is False):
			G['addundo'](L_T(['create', name_7, id__2, (-1), 'create', x_13, y_13, dir__8]))
		G['addunit'](newunitid)
		G['addunitmap'](newunitid, x_13, y_13, newunit['strings'][G['UNITNAME']])
		G['dynamic'](newunitid)
		testname = G['getname'](newunit)
		if (G['hasfeature'](testname, 'is', 'word', newunitid, x_13, y_13) is not None):
			G['updatecode'] = 1
		return (newunit['fixed'], id__2,)
		return ()
	G['create'] = f_create
	def f_getunitid(id__3=None, *_):  # L901
		style = (_t1 if L_t(_t1 := G['style_']) else '')
		for i_27, unit_12 in L_ipairs(G['units']):
			if (unit_12['values'][G['ID']] == id__3):
				return unit_12['fixed']
		G['MF_alert'](L_concat('No valid unitid found for this ID: ', L_tostring(id__3)))
		return 0
	G['getunitid'] = f_getunitid
	def f_newid(*_):  # L914
		result_8 = G['generaldata']['values'][G['CURRID']]
		G['generaldata']['values'][G['CURRID']] = (G['generaldata']['values'][G['CURRID']] + 1)
		return result_8
	G['newid'] = f_newid
	def f_addunitmap(id__4=None, x_14=None, y_14=None, name_8=None, *_):  # L920
		doadd = True
		tileid_7 = (x_14 + (y_14 * G['roomsizex']))
		if (G['unitmap'][tileid_7] is None):
			G['unitmap'][tileid_7] = L_T()
		else:
			for a_6, b_4 in L_ipairs(G['unitmap'][tileid_7]):
				if (b_4 == id__4):
					doadd = False
		if (G['unittypeshere'][tileid_7] is None):
			G['unittypeshere'][tileid_7] = L_T()
		uth_2 = G['unittypeshere'][tileid_7]
		if (uth_2[name_8] is None):
			uth_2[name_8] = 0
		if (doadd is not None and doadd is not False):
			L_insert(G['unitmap'][tileid_7], id__4)
			uth_2[name_8] = (uth_2[name_8] + 1)
	G['addunitmap'] = f_addunitmap
	def f_updateunitmap(id__5=None, oldx_4=None, oldy_4=None, x_15=None, y_15=None, name_9=None, *_):  # L950
		tileid_8 = (x_15 + (y_15 * G['roomsizex']))
		oldtileid = (oldx_4 + (oldy_4 * G['roomsizex']))
		if (G['unitmap'][oldtileid] is not None):
			for i_28, v_18 in L_ipairs(G['unitmap'][oldtileid]):
				if (v_18 == id__5):
					L_remove(G['unitmap'][oldtileid], i_28)
		if (G['unittypeshere'][oldtileid] is not None):
			uth_3 = G['unittypeshere'][oldtileid]
			if (uth_3[name_9] is not None):
				uth_3[name_9] = (uth_3[name_9] - 1)
				if (uth_3[name_9] == 0):
					uth_3[name_9] = None
		G['addunitmap'](id__5, x_15, y_15, name_9)
	G['updateunitmap'] = f_updateunitmap
	def f_inside(name_10=None, x_16=None, y_16=None, dir__9=None, unitid_10=None, leveldata__2=None, *_):  # L977
		ins = L_T()
		tileid_9 = (x_16 + (y_16 * G['roomsizex']))
		maptile = (_t1 if L_t(_t1 := G['unitmap'][tileid_9]) else L_T())
		dir__10 = dir__9
		leveldata_4 = (_t2 if L_t(_t2 := leveldata__2) else L_T())
		if (dir__10 == 4):
			dir__10 = G['fixedrandom'](0, 3)
		if (G['featureindex'][name_10] is not None):
			for i_29, rule_4 in L_ipairs(G['featureindex'][name_10]):
				baserule_3 = rule_4[1]
				conds_4 = rule_4[2]
				target_4 = baserule_3[1]
				verb = baserule_3[2]
				object = baserule_3[3]
				if (((target_4 == name_10) and (verb == 'has')) and (L_t(G['findnoun'](object, G['nlist']['short'])) or (G['unitreference'][object] is not None))):
					L_insert(ins, L_T([object, conds_4]))
		if (L_len(ins) > 0):
			for i_30, v_19 in L_ipairs(ins):
				object_2 = v_19[1]
				conds_5 = v_19[2]
				if L_t(G['testcond'](conds_5, unitid_10, x_16, y_16)):
					if (object_2 != 'text'):
						for a_7, mat in L_pairs(G['objectlist']):
							if ((a_7 == object_2) and (object_2 != 'empty')):
								if ((object_2 != 'all') and (L_sub(object_2, 1, 5) != 'group')):
									G['create'](object_2, x_16, y_16, dir__10, None, None, None, None, leveldata_4)
								elif (object_2 == 'all'):
									G['createall'](v_19, x_16, y_16, unitid_10, None, leveldata_4)
					else:
						G['create'](L_concat('text_', name_10), x_16, y_16, dir__10, None, None, None, None, leveldata_4)
	G['inside'] = f_inside
	def f_animate(*_):  # L1027
		camdir = 0
		if (G['spritedata']['values'][G['VISION']] > 0):
			camdir = (L_floor(G['spritedata']['values'][G['CAMDIR']]) - 1)
		for i_31, unitid_11 in L_ipairs(G['animunits']):
			unit_13 = G['mmf']['newObject'](unitid_11)
			name_11 = unit_13['strings'][G['UNITNAME']]
			sleep = G['hasfeature'](name_11, 'is', 'sleep', unitid_11)
			u_camdir = camdir
			if (unit_13['values'][G['ZLAYER']] >= 21):
				u_camdir = 0
			camtarget = False
			if (((G['spritedata']['values'][G['VISION']] == 1) and (unit_13['values'][G['ID']] == G['spritedata']['values'][G['CAMTARGET']])) and (unit_13['values'][G['ZLAYER']] < 21)):
				camtarget = True
			if (camtarget is False):
				if (unit_13['values'][G['TILING']] == 4):
					if (sleep is None):
						if (unit_13['values'][G['VISUALDIR']] != (-1)):
							unit_13['values'][G['VISUALDIR']] = ((unit_13['values'][G['VISUALDIR']] + 1) % 4)
						else:
							G['MF_particles']('destroy', unit_13['values'][G['XPOS']], unit_13['values'][G['YPOS']], 1, 3, 1, 3, 1)
							unit_13['values'][G['VISUALDIR']] = 0
						unit_13['direction'] = ((unit_13['values'][G['VISUALDIR']] + 32) % 32)
					else:
						unit_13['direction'] = ((unit_13['values'][G['VISUALDIR']] + 32) % 32)
				if (unit_13['values'][G['TILING']] == 3):
					if (sleep is None):
						if (unit_13['values'][G['VISUALDIR']] != (-1)):
							unit_13['values'][G['VISUALDIR']] = ((unit_13['values'][G['VISUALDIR']] + 1) % 4)
						else:
							G['MF_particles']('destroy', unit_13['values'][G['XPOS']], unit_13['values'][G['YPOS']], 1, 3, 1, 3, 1)
							unit_13['values'][G['VISUALDIR']] = 0
						unit_13['direction'] = (((((unit_13['values'][G['DIR']] - u_camdir) * 8) + unit_13['values'][G['VISUALDIR']]) + 32) % 32)
					else:
						unit_13['direction'] = (((((unit_13['values'][G['DIR']] - u_camdir) * 8) + unit_13['values'][G['VISUALDIR']]) + 32) % 32)
				if (unit_13['values'][G['TILING']] == 2):
					if (sleep is None):
						if (unit_13['values'][G['VISUALDIR']] == (-1)):
							G['MF_particles']('destroy', unit_13['values'][G['XPOS']], unit_13['values'][G['YPOS']], 1, 3, 1, 3, 1)
							unit_13['values'][G['VISUALDIR']] = 0
						unit_13['direction'] = (((((unit_13['values'][G['DIR']] - u_camdir) * 8) + unit_13['values'][G['VISUALDIR']]) + 32) % 32)
					else:
						unit_13['values'][G['VISUALDIR']] = (-1)
						unit_13['direction'] = (((((unit_13['values'][G['DIR']] - u_camdir) * 8) + unit_13['values'][G['VISUALDIR']]) + 32) % 32)
	G['animate'] = f_animate
	def f_updateanimations(targetdir=None, force_=None, *_):  # L1098
		force = (_t1 if L_t(_t1 := force_) else False)
		if ((G['spritedata']['values'][G['VISION']] > 0) or (force is not None and force is not False)):
			cdir = (_t2 if L_t(_t2 := targetdir) else G['spritedata']['values'][G['CAMDIR']])
			camdir_2 = (L_floor(cdir) - 1)
			for i_32, unit_14 in L_ipairs(G['units']):
				u_camdir_2 = camdir_2
				if (unit_14['values'][G['ZLAYER']] >= 21):
					u_camdir_2 = 0
				camtarget_2 = False
				if (((G['spritedata']['values'][G['VISION']] == 1) and (unit_14['values'][G['ID']] == G['spritedata']['values'][G['CAMTARGET']])) and (unit_14['values'][G['ZLAYER']] < 21)):
					camtarget_2 = True
				if (camtarget_2 is False):
					if (unit_14['values'][G['TILING']] == 0):
						unit_14['direction'] = ((((unit_14['values'][G['DIR']] - u_camdir_2) * 8) + 32) % 32)
					if (unit_14['values'][G['TILING']] == 3):
						unit_14['direction'] = (((((unit_14['values'][G['DIR']] - u_camdir_2) * 8) + unit_14['values'][G['VISUALDIR']]) + 32) % 32)
					if (unit_14['values'][G['TILING']] == 2):
						unit_14['direction'] = (((((unit_14['values'][G['DIR']] - u_camdir_2) * 8) + unit_14['values'][G['VISUALDIR']]) + 32) % 32)
	G['updateanimations'] = f_updateanimations
	def f_issolid(unitid_12=None, *_):  # L1133
		unit_15 = G['mmf']['newObject'](unitid_12)
		name_12 = unit_15['strings'][G['UNITNAME']]
		if (unit_15['strings'][G['UNITTYPE']] == 'text'):
			pass
		ispush = G['hasfeature'](name_12, 'is', 'push', unitid_12)
		ispull = G['hasfeature'](name_12, 'is', 'pull', unitid_12)
		ismove = G['hasfeature'](name_12, 'is', 'move', unitid_12)
		isyou = (_t1 if L_t(_t1 := (_t2 if L_t(_t2 := G['hasfeature'](name_12, 'is', 'you', unitid_12)) else G['hasfeature'](name_12, 'is', 'you2', unitid_12))) else G['hasfeature'](name_12, 'is', '3d', unitid_12))
		if ((((ispush is not None) or (ispull is not None)) or (ismove is not None)) or (isyou is not None)):
			return True
		return False
	G['issolid'] = f_issolid
	def f_isgone(unitid_13=None, *_):  # L1153
		if (G['issafe'](unitid_13) is False):
			unit_16 = G['mmf']['newObject'](unitid_13)
			x_17, y_17, name_13 = unit_16['values'][G['XPOS']], unit_16['values'][G['YPOS']], unit_16['strings'][G['UNITNAME']]
			if (unit_16['strings'][G['UNITTYPE']] == 'text'):
				pass
			isyou_2 = (_t1 if L_t(_t1 := (_t2 if L_t(_t2 := G['hasfeature'](name_13, 'is', 'you', unitid_13, x_17, y_17)) else G['hasfeature'](name_13, 'is', 'you2', unitid_13, x_17, y_17))) else G['hasfeature'](name_13, 'is', '3d', unitid_13, x_17, y_17))
			ismelt = G['hasfeature'](name_13, 'is', 'melt', unitid_13, x_17, y_17)
			isweak = G['hasfeature'](name_13, 'is', 'weak', unitid_13, x_17, y_17)
			isshut = G['hasfeature'](name_13, 'is', 'shut', unitid_13, x_17, y_17)
			isopen = G['hasfeature'](name_13, 'is', 'open', unitid_13, x_17, y_17)
			ismove_2 = G['hasfeature'](name_13, 'is', 'move', unitid_13, x_17, y_17)
			ispush_2 = G['hasfeature'](name_13, 'is', 'push', unitid_13, x_17, y_17)
			ispull_2 = G['hasfeature'](name_13, 'is', 'pull', unitid_13, x_17, y_17)
			eat = G['findfeatureat'](None, 'eat', name_13, x_17, y_17)
			if (eat is not None):
				for i_33, v_20 in L_ipairs(eat):
					if (v_20 != unitid_13):
						return True
			issink = G['findfeatureat'](None, 'is', 'sink', x_17, y_17)
			if (issink is not None):
				for i_34, v_21 in L_ipairs(issink):
					if ((v_21 != unitid_13) and L_t(G['floating'](v_21, unitid_13, x_17, y_17))):
						return True
			if (isyou_2 is not None):
				isdefeat = G['findfeatureat'](None, 'is', 'defeat', x_17, y_17)
				if (isdefeat is not None):
					for i_35, v_22 in L_ipairs(isdefeat):
						if L_t(G['floating'](v_22, unitid_13, x_17, y_17)):
							return True
			if (ismelt is not None):
				ishot = G['findfeatureat'](None, 'is', 'hot', x_17, y_17)
				if (ishot is not None):
					for i_36, v_23 in L_ipairs(ishot):
						if L_t(G['floating'](v_23, unitid_13, x_17, y_17)):
							return True
			if (isshut is not None):
				isopen_ = G['findfeatureat'](None, 'is', 'open', x_17, y_17)
				if (isopen_ is not None):
					for i_37, v_24 in L_ipairs(isopen_):
						if L_t(G['floating'](v_24, unitid_13, x_17, y_17)):
							return True
			if (isopen is not None):
				isshut_ = G['findfeatureat'](None, 'is', 'shut', x_17, y_17)
				if (isshut_ is not None):
					for i_38, v_25 in L_ipairs(isshut_):
						if L_t(G['floating'](v_25, unitid_13, x_17, y_17)):
							return True
			if (isweak is not None):
				things = G['findallhere'](x_17, y_17)
				if (things is not None):
					for i_39, v_26 in L_ipairs(things):
						if ((v_26 != unitid_13) and L_t(G['floating'](v_26, unitid_13, x_17, y_17))):
							return True
		return False
	G['isgone'] = f_isgone
	def f_floating(id1=None, id2=None, x1_=None, y1_=None, x2_=None, y2_=None, *_):  # L1254
		empty1, empty2 = False, False
		x1 = (_t1 if L_t(_t1 := x1_) else 0)
		y1 = (_t2 if L_t(_t2 := y1_) else 0)
		x2 = (_t3 if L_t(_t3 := x2_) else x1)
		y2 = (_t4 if L_t(_t4 := y2_) else y1)
		float1, float2 = (-1), (-1)
		if (id1 != 2):
			unit1 = G['mmf']['newObject'](id1)
			float1 = unit1['values'][G['FLOAT']]
		else:
			emptyfloat = G['hasfeature']('empty', 'is', 'float', 2, x1, y1)
			if (emptyfloat is not None):
				float1 = 1
			else:
				float1 = 0
		if (id2 != 2):
			unit2 = G['mmf']['newObject'](id2)
			float2 = unit2['values'][G['FLOAT']]
		else:
			emptyfloat_2 = G['hasfeature']('empty', 'is', 'float', 2, x2, y2)
			if (emptyfloat_2 is not None):
				float2 = 1
			else:
				float2 = 0
		if (float1 == float2):
			return True
		return False
	G['floating'] = f_floating
	def f_floating_level(id__6=None, x__4=None, y__4=None, *_):  # L1294
		levelfloat = G['findfeature']('level', 'is', 'float')
		valid = 0
		unitfloat = (-1)
		x_18 = (_t1 if L_t(_t1 := x__4) else 0)
		y_18 = (_t2 if L_t(_t2 := y__4) else 0)
		if (id__6 != 2):
			unit_17 = G['mmf']['newObject'](id__6)
			unitfloat = unit_17['values'][G['FLOAT']]
		else:
			if ((x__4 is None) or (y__4 is None)):
				emptyfloat_3 = L_first(G['findallfeature']('empty', 'is', 'float'))
				if (L_len(emptyfloat_3) > 0):
					unitfloat = 1
				else:
					unitfloat = 0
			else:
				emptyfloat_4 = G['hasfeature']('empty', 'is', 'float', 2, x_18, y_18)
				if (emptyfloat_4 is not None):
					unitfloat = 1
				else:
					unitfloat = 0
		if (levelfloat is not None):
			for i_40, v_27 in L_ipairs(levelfloat):
				if L_t(G['testcond'](v_27[2], 1)):
					valid = 1
		if (unitfloat == valid):
			return True
		return False
	G['floating_level'] = f_floating_level
	def f_emptydir(x_19=None, y_19=None, cconds=None, *_):  # L1339
		dir__11 = 4
		followcheck = False
		if (G['featureindex']['empty'] is not None):
			for a_8, b_5 in L_ipairs(G['featureindex']['empty']):
				rule_5 = b_5[1]
				econds = b_5[2]
				if (rule_5[1] == 'empty'):
					if (rule_5[2] == 'is'):
						if (G['issleep'](2, x_19, y_19) is False):
							if ((rule_5[3] == 'right') and L_t(G['testcond'](econds, 2, x_19, y_19, L_T(['facing', 'seeing']), None, cconds))):
								dir__11 = 0
							elif ((rule_5[3] == 'up') and L_t(G['testcond'](econds, 2, x_19, y_19, L_T(['facing', 'seeing']), None, cconds))):
								dir__11 = 1
							elif ((rule_5[3] == 'left') and L_t(G['testcond'](econds, 2, x_19, y_19, L_T(['facing', 'seeing']), None, cconds))):
								dir__11 = 2
							elif ((rule_5[3] == 'down') and L_t(G['testcond'](econds, 2, x_19, y_19, L_T(['facing', 'seeing']), None, cconds))):
								dir__11 = 3
					elif ((((rule_5[2] == 'follow') and (rule_5[3] != 'all')) and (rule_5[3] != 'empty')) and (rule_5[3] != 'level')):
						distance = 9999
						targetdir_2 = (-1)
						checkthese = L_T()
						if (L_sub(rule_5[3], 1, 5) != 'group'):
							checkthese = L_T([rule_5[3]])
						else:
							checkthese = G['findgroup'](rule_5[3])
						for c_6, name_14 in L_ipairs(checkthese):
							if ((((followcheck is False) and (G['issleep'](2, x_19, y_19) is False)) and (G['objectlist'][name_14] is not None)) and (G['unitlists'][name_14] is not None)):
								if L_t(G['testcond'](econds, 2, x_19, y_19, L_T(['facing', 'seeing']))):
									for i_41, v_28 in L_ipairs(G['unitlists'][name_14]):
										funit = G['mmf']['newObject'](v_28)
										fx, fy = funit['values'][G['XPOS']], funit['values'][G['YPOS']]
										xdir = (fx - x_19)
										ydir = (fy - y_19)
										dist = (abs(xdir) + abs(ydir))
										fdir = (-1)
										if (abs(xdir) <= abs(ydir)):
											if (ydir >= 0):
												fdir = 3
											else:
												fdir = 1
										else:
											if (xdir > 0):
												fdir = 0
											else:
												fdir = 2
										if ((dist <= distance) and (dist > 0)):
											distance = dist
											targetdir_2 = fdir
											followcheck = True
							if (targetdir_2 != (-1)):
								dir__11 = targetdir_2
								break
		return dir__11
	G['emptydir'] = f_emptydir
	def f_issafe(unitid_14=None, x_20=None, y_20=None, *_):  # L1421
		G['name'] = ''
		if ((unitid_14 != 1) and (unitid_14 != 2)):
			unit_18 = G['mmf']['newObject'](unitid_14)
			G['name'] = unit_18['strings'][G['UNITNAME']]
		elif (unitid_14 == 1):
			G['name'] = 'level'
		else:
			G['name'] = 'empty'
		safe = G['hasfeature'](G['name'], 'is', 'safe', unitid_14, x_20, y_20)
		if (safe is not None):
			return True
		return False
	G['issafe'] = f_issafe
	def f_issleep(unitid_15=None, x__5=None, y__5=None, *_):  # L1442
		name_15 = ''
		if ((unitid_15 != 1) and (unitid_15 != 2)):
			unit_19 = G['mmf']['newObject'](unitid_15)
			name_16 = unit_19['strings'][G['UNITNAME']]
		elif (unitid_15 == 2):
			name_15 = 'empty'
		elif (unitid_15 == 1):
			name_15 = 'level'
		x_21 = (_t1 if L_t(_t1 := x__5) else 0)
		y_21 = (_t2 if L_t(_t2 := y__5) else 0)
		sleep_2 = G['hasfeature'](name_15, 'is', 'sleep', unitid_15, x_21, y_21)
		if (sleep_2 is not None):
			return True
		return False
	G['issleep'] = f_issleep
	def f_isstill(unitid_16=None, x_22=None, y_22=None, *_):  # L1466
		G['name'] = ''
		if ((unitid_16 != 1) and (unitid_16 != 2)):
			unit_20 = G['mmf']['newObject'](unitid_16)
			G['name'] = unit_20['strings'][G['UNITNAME']]
		elif (unitid_16 == 1):
			G['name'] = 'level'
		else:
			G['name'] = 'empty'
		still = G['hasfeature'](G['name'], 'is', 'still', unitid_16, x_22, y_22)
		if (still is not None):
			return True
		return False
	G['isstill'] = f_isstill
	def f_isstill_or_locked(unitid_17=None, x_23=None, y_23=None, dir__12=None, *_):  # L1487
		G['name'] = ''
		if ((unitid_17 != 1) and (unitid_17 != 2)):
			unit_21 = G['mmf']['newObject'](unitid_17)
			G['name'] = unit_21['strings'][G['UNITNAME']]
		elif (unitid_17 == 1):
			G['name'] = 'level'
		else:
			G['name'] = 'empty'
		still_2 = G['cantmove'](G['name'], unitid_17, dir__12, x_23, y_23)
		return still_2
	G['isstill_or_locked'] = f_isstill_or_locked
	def f_getmat(m=None, *_):  # L1504
		found = False
		for i_42, v_29 in L_pairs(G['objectlist']):
			if (i_42 == m):
				found = True
		if (found is not None and found is not False):
			return m
		else:
			return None
	G['getmat'] = f_getmat
	def f_getmat_text(name_17=None, *_):  # L1520
		base = G['unitreference'][name_17]
		changed = G['objectpalette'][name_17]
		if (G['generaldata']['strings'][G['WORLD']] != G['generaldata']['strings'][G['BASEWORLD']]):
			return (changed is not None)
		else:
			return (base is not None)
		return False
	G['getmat_text'] = f_getmat_text
	def f_destroylevel(special_=None, *_):  # L1533
		G['destroylevel_check'] = True
		G['destroylevel_style'] = (_t1 if L_t(_t1 := special_) else '')
		if ((G['destroylevel_style'] == 'infinity') or (G['destroylevel_style'] == 'toocomplex')):
			G['setsoundname']('removal', 2)
		elif ((G['destroylevel_style'] != 'empty') and (G['destroylevel_style'] != 'bonus')):
			G['setsoundname']('removal', 1)
		G['MF_musicstate'](1)
		G['generaldata2']['values'][G['NOPLAYER']] = 1
	G['destroylevel'] = f_destroylevel
	def f_destroylevel_do(*_):  # L1548
		if ((G['generaldata']['values'][G['MODE']] != 5) and L_t(G['destroylevel_check'])):
			G['MF_musicstate'](1)
			G['generaldata2']['values'][G['NOPLAYER']] = 1
			G['destroylevel_check'] = False
			special = (_t1 if L_t(_t1 := G['destroylevel_style']) else '')
			G['destroylevel_style'] = ''
			dellist = L_T()
			for i_43, unit_22 in L_ipairs(G['units']):
				L_insert(dellist, unit_22['fixed'])
			if (L_len(dellist) > 0):
				for i_44, unitid_18 in L_ipairs(dellist):
					unit_23 = G['mmf']['newObject'](unitid_18)
					c1, c2 = L_adjust((*G['getcolour'](unitid_18),), 2)
					pmult, sound = L_adjust((*G['checkeffecthistory']('destroylevel'),), 2)
					if (((special != 'infinity') and (special != 'empty')) and (special != 'bonus')):
						G['MF_particles']('bling', unit_23['values'][G['XPOS']], unit_23['values'][G['YPOS']], (10 * pmult), c1, c2, 1, 1)
					elif (special == 'bonus'):
						G['MF_particles']('win', unit_23['values'][G['XPOS']], unit_23['values'][G['YPOS']], (10 * pmult), 4, 1, 1, 1)
					G['delete'](unitid_18, None, None, True)
			if (special == 'infinity'):
				if (G['HACK_INFINITY'] >= 200):
					G['writetext'](G['langtext']('ingame_infiniteloop'), 0, ((G['screenw'] * 0.5) - 12), ((G['screenh'] * 0.5) + 60), 0, True, 3, True, L_T([4, 1]), 3)
					G['HACK_INFINITY'] = 0
					G['MF_playsound']('infinity')
					isignid = G['MF_specialcreate']('Special_infinity')
					isign = G['mmf']['newObject'](isignid)
					isign['x'] = (G['screenw'] * 0.5)
					isign['y'] = ((G['screenh'] * 0.5) - 36)
					isign['layer'] = 2
					G['MF_setcolour'](isignid, 4, 1)
			elif (special == 'toocomplex'):
				G['writetext'](G['langtext']('ingame_toocomplex'), 0, ((G['screenw'] * 0.5) - 12), (G['screenh'] * 0.5), 0, True, 3, True, L_T([4, 1]), 3)
				G['HACK_INFINITY'] = 0
				G['MF_playsound']('infinity')
			elif (special == 'bonus'):
				G['MF_playsound']('bonus')
			G['MF_removeblockeffect'](0)
			G['updatecode'] = 1
			G['features'] = L_T()
			G['featureindex'] = L_T()
			G['visualfeatures'] = L_T()
			G['notfeatures'] = L_T()
			L_noop()
		elif (G['generaldata']['values'][G['MODE']] == 5):
			G['timedmessage']('Destroylevel() called from editor. Report this!')
	G['destroylevel_do'] = f_destroylevel_do
	def f_findunitat(name_18=None, x_24=None, y_24=None, *_):  # L1614
		id__7 = (x_24 + (y_24 * G['roomsizex']))
		result_9 = L_T()
		if (G['unitmap'][id__7] is not None):
			for i_45, v_30 in L_ipairs(G['unitmap'][id__7]):
				unit_24 = G['mmf']['newObject'](v_30)
				if ((unit_24['strings'][G['UNITNAME']] == name_18) or (name_18 is None)):
					L_insert(result_9, v_30)
		return result_9
	G['findunitat'] = f_findunitat
	def f_checkwordchanges(unitid_19=None, unitname_7=None, *_):  # L1632
		if (L_len(G['wordunits']) > 0):
			for i_46, v_31 in L_ipairs(G['wordunits']):
				if (v_31[1] == unitid_19):
					G['updatecode'] = 1
					return None
		if (L_len(G['wordrelatedunits']) > 0):
			for i_47, v_32 in L_ipairs(G['wordrelatedunits']):
				if (v_32[1] == unitid_19):
					G['updatecode'] = 1
					return None
	G['checkwordchanges'] = f_checkwordchanges
	def f_getpath(root=None, *_):  # L1652
		world = G['generaldata']['strings'][G['WORLD']]
		if (root == 1):
			return 'Data/'
		else:
			return L_concat('Data/Worlds/', world, '/')
	G['getpath'] = f_getpath
	def f_append(t1=None, t2=None, *_):  # L1662
		result_10 = L_T()
		for i_48, v_33 in L_ipairs(t1):
			L_insert(result_10, v_33)
		for i_49, v_34 in L_ipairs(t2):
			L_insert(result_10, v_34)
		return result_10
	G['append'] = f_append
	def f_getname(unit_25=None, meta_=None, *_):  # L1676
		result_11 = unit_25['strings'][G['UNITNAME']]
		meta_2 = (_t1 if L_t(_t1 := meta_) else False)
		if ((meta_2 is False) and (unit_25['strings'][G['UNITTYPE']] == 'text')):
			result_11 = 'text'
		return result_11
	G['getname'] = f_getname
	def f_getemptytiles(*_):  # L1687
		pos = L_T()
		for i_50 in L_range(1, (G['roomsizex'] - 2)):
			for j_2 in L_range(1, (G['roomsizey'] - 2)):
				tileid_10 = (i_50 + (j_2 * G['roomsizex']))
				if (G['unitmap'][tileid_10] is None):
					L_insert(pos, L_T([i_50, j_2]))
				else:
					if (L_len(G['unitmap'][tileid_10]) == 0):
						L_insert(pos, L_T([i_50, j_2]))
		return pos
	G['getemptytiles'] = f_getemptytiles
	def f_setsoundname(type_=None, id__8=None, short=None, *_):  # L1707
		result_12 = ''
		if (id__8 > 0):
			sound_2 = G['soundnames'][id__8]
			if (sound_2 is not None):
				result_12 = sound_2['name']
				if (sound_2['count'] is not None):
					rnd = G['math']['random'](1, sound_2['count'])
					result_12 = L_concat(result_12, L_tostring(rnd))
		if (short is not None):
			result_12 = L_concat(result_12, short)
		if (type_ == 'removal'):
			G['generaldata2']['strings'][G['REMOVALSOUND']] = result_12
		elif (type_ == 'turn'):
			G['generaldata2']['strings'][G['TURNSOUND']] = result_12
		return result_12
	G['setsoundname'] = f_setsoundname
	def f_checkturnsound(*_):  # L1738
		if ((G['generaldata2']['strings'][G['TURNSOUND']] == '') and (G['editor']['strings'][G['MENU']] == 'ingame')):
			if L_t(G['updateundo']):
				G['setsoundname']('turn', 8)
	G['checkturnsound'] = f_checkturnsound
	def f_getlevelsurrounds(levelid=None, *_):  # L1746
		level = G['mmf']['newObject'](levelid)
		dirids = L_T(['r', 'u', 'l', 'd', 'dr', 'ur', 'ul', 'dl', 'o'])
		x_25, y_25, dir__13 = level['values'][G['XPOS']], level['values'][G['YPOS']], level['values'][G['DIR']]
		result_13 = L_concat(L_tostring(dir__13), ',')
		for i_51, v_35 in L_ipairs(G['dirs_diagonals']):
			result_13 = L_concat(result_13, dirids[i_51], ',')
			ox_2, oy_2 = v_35[1], v_35[2]
			tileid_11 = ((x_25 + ox_2) + ((y_25 + oy_2) * G['roomsizex']))
			if (G['unitmap'][tileid_11] is not None):
				if (L_len(G['unitmap'][tileid_11]) > 0):
					for a_9, b_6 in L_ipairs(G['unitmap'][tileid_11]):
						if (b_6 != levelid):
							unit_26 = G['mmf']['newObject'](b_6)
							name_19 = G['getname'](unit_26)
							result_13 = L_concat(result_13, name_19, ',')
				else:
					result_13 = L_concat(result_13, '-', ',')
			else:
				result_13 = L_concat(result_13, '-', ',')
		G['generaldata2']['strings'][G['LEVELSURROUNDS']] = result_13
	G['getlevelsurrounds'] = f_getlevelsurrounds
	def f_parsesurrounds(*_):  # L1782
		surrounds = G['MF_parsestring'](G['generaldata2']['strings'][G['LEVELSURROUNDS']])
		result_14 = L_T()
		stage = 0
		dirids_2 = L_T(['r', 'u', 'l', 'd', 'dr', 'ur', 'ul', 'dl', 'o'])
		for i_52, v_36 in L_ipairs(surrounds):
			if (i_52 == 1):
				result_14['dir'] = L_tonumber(v_36)
			else:
				if (v_36 == dirids_2[(stage + 1)]):
					stage = (stage + 1)
				else:
					dir__14 = dirids_2[stage]
					if (result_14[dir__14] is None):
						result_14[dir__14] = L_T()
					L_insert(result_14[dir__14], v_36)
		return result_14
	G['parsesurrounds'] = f_parsesurrounds
	def f_copytable(t1_2=None, t2_2=None, *_):  # L1810
		result_15 = L_T()
		for i_53, v_37 in L_ipairs(t2_2):
			L_insert(result_15, v_37)
		L_insert(t1_2, result_15)
		return t1_2
	G['copytable'] = f_copytable
	def f_copysubtable(t1_3=None, t2_3=None, *_):  # L1822
		for i_54, v_38 in L_ipairs(t2_3):
			result_16 = L_T()
			for a_10, b_7 in L_ipairs(v_38):
				L_insert(result_16, b_7)
			L_insert(t1_3, result_16)
		return t1_3
	G['copysubtable'] = f_copysubtable
	def f_copyconds(target_5=None, conds_6=None, *_):  # L1834
		if ((conds_6 is not None) and (L_len(conds_6) > 0)):
			for a_11, cond_2 in L_ipairs(conds_6):
				condtype = cond_2[1]
				params = (_t1 if L_t(_t1 := cond_2[2]) else L_T())
				L_insert(target_5, L_T([condtype, L_T()]))
				for c_7, param in L_ipairs(params):
					L_insert(target_5[L_len(target_5)][2], param)
		return target_5
	G['copyconds'] = f_copyconds
	def f_concatenate(t1_4=None, t2_=None, *_):  # L1851
		result_17 = L_T()
		for i_55, v_39 in L_ipairs(t1_4):
			if (L_type(v_39) != 'table'):
				L_insert(result_17, v_39)
			else:
				subtable = G['concatenate'](v_39, L_T())
				L_insert(result_17, subtable)
		t2_4 = (_t1 if L_t(_t1 := t2_) else L_T())
		for i_56, v_40 in L_ipairs(t2_4):
			if (L_type(v_40) != 'table'):
				L_insert(result_17, v_40)
			else:
				subtable_2 = G['concatenate'](v_40, L_T())
				L_insert(result_17, subtable_2)
		return result_17
	G['concatenate'] = f_concatenate
	def f_checkeffecthistory(id__9=None, *_):  # L1879
		result_18 = False
		sound_3 = ''
		mult = 1
		if (G['effecthistory'][id__9] is not None):
			result_18 = True
			mult = 0.5
			G['effecthistory'][id__9] = (G['effecthistory'][id__9] + 1)
			if ((G['effecthistory'][id__9] % 1) > 0):
				sound_3 = '_short'
			if (G['effecthistory'][id__9] > 5):
				mult = 0.2
		else:
			G['effecthistory'][id__9] = 2
		return (mult, sound_3, result_18,)
		return ()
	G['checkeffecthistory'] = f_checkeffecthistory
	def f_updateeffecthistory(*_):  # L1903
		for i_57, v_41 in L_pairs(G['effecthistory']):
			if (v_41 > 1.5):
				G['effecthistory'][i_57] = 1.5
			else:
				G['effecthistory'][i_57] = None
	G['updateeffecthistory'] = f_updateeffecthistory
	def f_reseteffecthistory(*_):  # L1913
		G['effecthistory'] = L_T()
	G['reseteffecthistory'] = f_reseteffecthistory
	def f_genflowercolour(*_):  # L1917
		result_19 = ''
		c_8 = G['colours']['flowers']
		rnd_2 = G['math']['random'](1, L_len(c_8))
		colour = c_8[rnd_2]
		c1_2, c2_2 = colour[1], colour[2]
		result_19 = L_concat(L_tostring(c1_2), ',', L_tostring(c2_2))
		return (result_19, c1_2, c2_2,)
		return ()
	G['genflowercolour'] = f_genflowercolour
	def f_gettiledata(id__10=None, data_2=None, *_):  # L1931
		tiledata = G['tileslist'][id__10]
		changedata = (_t1 if L_t(_t1 := G['changes'][id__10]) else L_T())
		result_20 = ''
		datapairs = L_T([], {'name': 'name'})
		if (tiledata[data_2] is not None):
			result_20 = tiledata[data_2]
			pairing = (_t2 if L_t(_t2 := datapairs[data_2]) else 'null')
			if (G['changes'][pairing] is not None):
				result_20 = G['changes'][pairing]
		else:
			G['MF_alert'](L_concat('No tiledata found for ', id__10, ' with name ', data_2))
		return result_20
	G['gettiledata'] = f_gettiledata
	def f_displaybigtext(text_=None, colour_2=None, translated_=None, offsetx_=None, offsety_=None, *_):  # L1956
		translated = (_t1 if L_t(_t1 := translated_) else False)
		text_3 = text_
		if (translated is not None and translated is not False):
			text_3 = G['langtext'](text_)
		ox_3 = (_t2 if L_t(_t2 := offsetx_) else 0)
		oy_3 = (_t3 if L_t(_t3 := offsety_) else 0)
		c1_3 = L_T([colour_2[1], colour_2[2]])
		c2_3 = L_T([colour_2[3], colour_2[4]])
		G['writetext'](text_3, 0, ((G['screenw'] * 0.5) + ox_3), (((G['screenh'] * 0.5) + oy_3) + 4), 0, True, 3, True, c2_3, 4)
		G['writetext'](text_3, 0, ((G['screenw'] * 0.5) + ox_3), ((G['screenh'] * 0.5) + oy_3), 0, True, 3, True, c1_3, 4)
	G['displaybigtext'] = f_displaybigtext
	def f_gettablestring(t=None, *_):  # L1974
		result_21 = ''
		for i_58, v_42 in L_ipairs(t):
			result_21 = L_concat(result_21, L_tostring(v_42))
			if (i_58 < L_len(t)):
				result_21 = L_concat(result_21, ',')
		return result_21
	G['gettablestring'] = f_gettablestring
	def f_pickoption(opts=None, opt=None, *_):  # L1988
		return opts[opt]
	G['pickoption'] = f_pickoption
	def f_getpathdetails(obj=None, style_=None, gate_=None, req_=None, *_):  # L1992
		name_20 = (_t1 if L_t(_t1 := L_first(G['getactualdata_objlist'](obj, 'name'))) else 'unknown')
		styles = L_T(['hidden', 'visible'])
		gates = L_T(['', 'levels', 'clears', 'bonuses', 'local levels'])
		style_2 = (_t2 if L_t(_t2 := styles[(style_ + 1)]) else 'error')
		gate = (_t3 if L_t(_t3 := gates[(gate_ + 1)]) else 'error')
		gatetext = ''
		if ((gate_ > 0) and (req_ > 0)):
			gatetext = L_concat(', ', L_tostring(req_), ' ', gate)
		result_22 = L_concat(name_20, ' (', style_2, gatetext, ')')
		return result_22
	G['getpathdetails'] = f_getpathdetails
	def f_getnamegivingtitle(id__11=None, *_):  # L2011
		textcode = G['namegivingtitles'][id__11]
		result_23, filters = '', 'lower,maxlen24'
		if (textcode is not None):
			result_23 = G['langtext'](textcode[1], True)
			if (textcode[2] is not None):
				filters = textcode[2]
		return (result_23, filters,)
		return ()
	G['getnamegivingtitle'] = f_getnamegivingtitle
	def f_findunits(name_21=None, db=None, conds_7=None, *_):  # L2026
		result_24 = (_t1 if L_t(_t1 := db) else L_T())
		if ((name_21 != 'empty') and (name_21 != 'all')):
			checkthese_2 = L_T()
			if (L_sub(name_21, 1, 5) != 'group'):
				checkthese_2 = L_T([name_21])
			else:
				checkthese_2 = G['findgroup'](name_21)
			for a_12, b_8 in L_ipairs(checkthese_2):
				if (G['unitlists'][b_8] is not None):
					for i_59, v_43 in L_ipairs(G['unitlists'][b_8]):
						L_insert(result_24, L_T([v_43, conds_7]))
		return result_24
	G['findunits'] = f_findunits
	def f_flipnot(text_4=None, *_):  # L2049
		result_25 = ''
		if (L_sub(text_4, 1, 4) == 'not '):
			result_25 = L_sub(text_4, 5)
		else:
			result_25 = L_concat('not ', text_4)
		return result_25
	G['flipnot'] = f_flipnot
	def f_inbounds(x_26=None, y_26=None, style__2=None, *_):  # L2061
		style_3 = (_t1 if L_t(_t1 := style__2) else 0)
		if (style_3 == 1):
			return ((y_26 < (G['roomsizey'] - 1)) if L_t(_t2 := ((x_26 < (G['roomsizex'] - 1)) if L_t(_t3 := ((y_26 > 0) if (x_26 > 0) else False)) else _t3)) else _t2)
		else:
			return ((y_26 < G['roomsizey']) if L_t(_t4 := ((x_26 < G['roomsizex']) if L_t(_t5 := ((y_26 >= 0) if (x_26 >= 0) else False)) else _t5)) else _t4)
	G['inbounds'] = f_inbounds
	def f_findfears(unitid_20=None, feartargets=None, x__6=None, y__6=None, *_):  # L2071
		result_26, resultdir = False, 4
		amount = 0
		ox_4, oy_4 = 0, 0
		x_27, y_27 = 0, 0
		name_22 = ''
		dir__15 = 4
		if (unitid_20 != 2):
			unit_27 = G['mmf']['newObject'](unitid_20)
			x_27, y_27 = unit_27['values'][G['XPOS']], unit_27['values'][G['YPOS']]
			name_22 = G['getname'](unit_27)
			dir__15 = unit_27['values'][G['DIR']]
		else:
			x_27, y_27 = x__6, y__6
			name_22 = 'empty'
			dir__15 = G['emptydir'](x_27, y_27)
		feardirs = L_T()
		maxfear = 0
		for j_3 in L_range(0, 3):
			i_60 = ((((dir__15 + 2) + j_3) % 4) + 1)
			ndrs = G['ndirs'][i_60]
			ox_4 = ndrs[1]
			oy_4 = ndrs[2]
			dirfound = False
			diramount = 0
			if (L_len(feartargets) > 0):
				for a_13, v_44 in L_ipairs(feartargets):
					foundfears = L_T()
					if (v_44 != 'empty'):
						foundfears = G['findtype'](L_T([v_44, None]), (x_27 + ox_4), (y_27 + oy_4), unitid_20)
					else:
						tileid_12 = ((x_27 + ox_4) + ((y_27 + oy_4) * G['roomsizex']))
						if ((G['unitmap'][tileid_12] is None) or (L_len(G['unitmap'][tileid_12]) == 0)):
							foundfears = L_T(['a', 'b'])
					if (L_len(foundfears) > 0):
						dirfound = True
						result_26 = True
						resultdir = G['rotate']((i_60 - 1))
						diramount = (diramount + 1)
			if (dirfound is not None and dirfound is not False):
				feardirs[i_60] = diramount
				maxfear = L_max(maxfear, diramount)
			else:
				feardirs[i_60] = 0
		totalfeardirs = 0
		for i_61, v_45 in L_ipairs(feardirs):
			if (v_45 >= maxfear):
				totalfeardirs = (totalfeardirs + 1)
			else:
				feardirs[i_61] = 0
		if (totalfeardirs > 0):
			amount = maxfear
		if (totalfeardirs > 1):
			resultdir = dir__15
			searching = True
			tests = 0
			while (searching is not None and searching is not False):
				problems = False
				if (feardirs[(resultdir + 1)] == 1):
					problems = True
				else:
					ndrs_2 = G['ndirs'][(resultdir + 1)]
					ox_5, oy_5 = ndrs_2[1], ndrs_2[2]
					obs = L_first(G['check'](unitid_20, x_27, y_27, resultdir))
					obsresult = 0
					for i_62, v_46 in L_ipairs(obs):
						if ((v_46 == 1) or (v_46 == (-1))):
							obsresult = 1
							break
						elif ((v_46 != 0) and (obsresult == 0)):
							obsresult = v_46
					if (obsresult == 1):
						problems = True
					elif (obsresult != 0):
						ndrs_3 = G['ndirs'][(resultdir + 1)]
						ox_6, oy_6 = ndrs_3[1], ndrs_3[2]
						obsresult_ = G['trypush'](obsresult, ox_6, oy_6, resultdir, False, x_27, y_27, 'fear', unitid_20)
						if (obsresult_ != 0):
							problems = True
				if (problems is False):
					searching = False
				else:
					if (tests == 0):
						resultdir = (((resultdir - 1) + 4) % 4)
					elif (tests == 1):
						resultdir = (((resultdir + 2) + 4) % 4)
					elif (tests == 2):
						resultdir = (((resultdir + 1) + 4) % 4)
					elif (tests == 3):
						resultdir = (((resultdir - 2) + 4) % 4)
					tests = (tests + 1)
				if (tests >= 4):
					searching = False
					result_26 = False
					resultdir = 4
		return (result_26, resultdir, amount,)
		return ()
	G['findfears'] = f_findfears
	def f_getlettermultiplier(*_):  # L2214
		result_27 = 0
		if (G['generaldata']['strings'][G['BUILD']] == 'm'):
			if (G['generaldata']['strings'][G['LANG']] == 'en'):
				result_27 = 1
			else:
				customfont = G['generaldata4']['values'][G['CUSTOMFONT']]
				if (customfont == 0):
					result_27 = 0.33
				else:
					result_27 = 0.9
		return result_27
	G['getlettermultiplier'] = f_getlettermultiplier
	def f_isitbroken(name_23=None, id__12=None, x_28=None, y_28=None, checkedconds=None, *_):  # L2234
		if (G['hasfeature'](name_23, 'is', 'broken', id__12, x_28, y_28, checkedconds, True) is not None):
			return 1
		return 0
	G['isitbroken'] = f_isitbroken
	def f_getinputcount(listid=None, *_):  # L2242
		data_3 = (_t1 if L_t(_t1 := G['controlnames'][listid]) else L_T())
		return L_len(data_3)
	G['getinputcount'] = f_getinputcount
	def f_cantmove(name_24=None, unitid_21=None, dir__16=None, x_29=None, y_29=None, *_):  # L2248
		still_3 = G['hasfeature'](name_24, 'is', 'still', unitid_21, x_29, y_29)
		levelhold = G['hasfeature']('level', 'is', 'hold', 1, x_29, y_29)
		if ((levelhold is not None) and ((unitid_21 != 1) and L_t(G['floating_level'](unitid_21, x_29, y_29)))):
			return True
		if (still_3 is not None):
			return True
		if ((dir__16 is not None) and (dir__16 != 4)):
			opts_2 = L_T(['lockedright', 'lockedup', 'lockedleft', 'lockeddown'])
			checkdir = dir__16
			if (G['featureindex']['reverse'] is not None):
				checkdir = L_first(G['reversecheck'](unitid_21, dir__16, x_29, y_29))
			opt_2 = opts_2[(checkdir + 1)]
			if (opt_2 is not None):
				still_3 = G['hasfeature'](name_24, 'is', opt_2, unitid_21, x_29, y_29)
				if (still_3 is not None):
					return True
		if (((unitid_21 != 2) and (unitid_21 != 1)) and (G['featureindex']['grab'] is not None)):
			unit_28 = G['mmf']['newObject'](unitid_21)
			if ((unit_28['grabbed'] is not None) and (unit_28['grabbed'] != 0)):
				return True
		return False
	G['cantmove'] = f_cantmove
	def f_findnoun(noun=None, list_=None, *_):  # L2288
		list__2 = (_t1 if L_t(_t1 := list_) else G['nlist']['full'])
		for i_63, v_47 in L_ipairs(list__2):
			if ((v_47 == noun) or ((v_47 == 'group') and (L_sub(noun, 1, 5) == 'group'))):
				return True
		return False
	G['findnoun'] = f_findnoun
	def f_findgroup(grouptype_=None, invert_=None, limit_=None, checkedconds_=None, *_):  # L2300
		result_28 = L_T()
		limit = (_t1 if L_t(_t1 := limit_) else 0)
		invert = (_t2 if L_t(_t2 := invert_) else False)
		grouptype = (_t3 if L_t(_t3 := grouptype_) else 'group')
		found_2 = L_T()
		alreadyused = L_T()
		limit = (limit + 1)
		idstring = ''
		currmembers = L_T()
		handlerecursion = False
		for i_64, v_48 in L_ipairs(G['groupmembers']):
			name_25 = v_48[1]
			conds_8 = v_48[2]
			gtype = v_48[3]
			recursion = v_48[4]
			if (gtype == grouptype):
				if (L_t(G['hasconds'](v_48)) and (G['unitlists'][name_25] is not None)):
					if (recursion is False):
						for a_14, b_9 in L_ipairs(G['unitlists'][name_25]):
							unit_29 = G['mmf']['newObject'](b_9)
							x_30, y_30 = unit_29['values'][G['XPOS']], unit_29['values'][G['YPOS']]
							if L_t(G['testcond'](conds_8, b_9, x_30, y_30, None, limit, checkedconds_)):
								L_insert(result_28, name_25)
								L_insert(currmembers, name_25)
								found_2[name_25] = 1
								idstring = L_concat(idstring, name_25)
								break
					else:
						handlerecursion = True
				elif (G['hasconds'](v_48) is False):
					L_insert(result_28, name_25)
					L_insert(currmembers, name_25)
					found_2[name_25] = 1
					idstring = L_concat(idstring, name_25)
		reclimit = 0
		curridstring = idstring
		while ((handlerecursion is not None and handlerecursion is not False) and (reclimit < 10)):
			newidstring = idstring
			newmembers = L_T()
			for i_65, v_49 in L_ipairs(result_28):
				L_insert(newmembers, v_49)
			for i_66, v_50 in L_ipairs(G['groupmembers']):
				name_26 = v_50[1]
				conds_9 = v_50[2]
				gtype_2 = v_50[3]
				recursion_2 = v_50[4]
				if ((recursion_2 is not None and recursion_2 is not False) and (gtype_2 == grouptype)):
					if (L_t(G['hasconds'](v_50)) and (G['unitlists'][name_26] is not None)):
						for a_15, b_10 in L_ipairs(G['unitlists'][name_26]):
							unit_30 = G['mmf']['newObject'](b_10)
							x_31, y_31 = unit_30['values'][G['XPOS']], unit_30['values'][G['YPOS']]
							if L_t(G['testcond'](conds_9, b_10, x_31, y_31, None, limit, checkedconds_, None, currmembers)):
								L_insert(newmembers, name_26)
								newidstring = L_concat(newidstring, name_26)
								break
					elif (G['hasconds'](v_50) is False):
						L_insert(newmembers, name_26)
						newidstring = L_concat(newidstring, name_26)
			if (newidstring != curridstring):
				currmembers = L_T()
				for i_67, v_51 in L_ipairs(newmembers):
					L_insert(currmembers, v_51)
				curridstring = newidstring
				reclimit = (reclimit + 1)
			else:
				for i_68, v_52 in L_ipairs(currmembers):
					found_2[v_52] = 1
					idstring = L_concat(idstring, v_52)
					L_insert(result_28, v_52)
				handlerecursion = False
		if (reclimit >= 10):
			G['HACK_INFINITY'] = 200
			G['destroylevel']('infinity')
			return None
		if (invert is not None and invert is not False):
			actualresult = L_T()
			for a_16, mat_2 in L_pairs(G['objectlist']):
				if (((found_2[a_16] is None) and (alreadyused[a_16] is None)) and (G['findnoun'](a_16, G['nlist']['short']) is False)):
					L_insert(actualresult, a_16)
					alreadyused[a_16] = 1
			return actualresult
		return result_28
	G['findgroup'] = f_findgroup
	def f_hasconds(rule_6=None, *_):  # L2424
		conds_10 = rule_6[2]
		if (conds_10 is None):
			return False
		else:
			if (L_type(conds_10) != 'table'):
				G['MF_alert'](L_concat('Warning! Conditionals of ', rule_6[1][1], ' ', rule_6[1][2], ' ', rule_6[1][3], " aren't in a table!"))
				return False
			elif (L_len(conds_10) == 0):
				return False
			elif (((L_len(conds_10) == 1) and (conds_10[1][1] is not None)) and (L_strlen(conds_10[1][1]) == 0)):
				return False
		return True
	G['hasconds'] = f_hasconds
	def f_groupcheck(*_):  # L2443
		if (L_len(G['groupmembers']) > 0):
			groups = L_T()
			for i_69, v_53 in L_pairs(G['objectlist']):
				if (L_sub(i_69, 1, 5) == 'group'):
					L_insert(groups, i_69)
			for i_70, v_54 in L_ipairs(groups):
				G['findgroup'](v_54)
	G['groupcheck'] = f_groupcheck
	def f_reversedir(dir__17=None, *_):  # L2459
		dir__18 = dir__17
		if (dir__18 != 4):
			dir__18 = (((dir__18 + 4) + 2) % 4)
		return dir__18
	G['reversedir'] = f_reversedir
	def f_reversecheck(unitid_22=None, dir__19=None, x_32=None, y_32=None, ox_=None, oy_=None, *_):  # L2469
		result_29 = dir__19
		name_27 = ''
		ox_7 = (_t1 if L_t(_t1 := ox_) else 0)
		oy_7 = (_t2 if L_t(_t2 := oy_) else 0)
		if ((unitid_22 != 2) and (unitid_22 != 1)):
			unit_31 = G['mmf']['newObject'](unitid_22)
			name_27 = G['getname'](unit_31)
		elif (unitid_22 == 2):
			name_27 = 'empty'
		elif (unitid_22 == 1):
			name_27 = 'level'
		if ((G['hasfeature_count'](name_27, 'is', 'reverse', unitid_22, x_32, y_32) % 2) == 1):
			result_29 = G['reversedir'](dir__19)
			if ((ox_7 != 0) or (oy_7 != 0)):
				ox_7 = (0 - ox_)
				oy_7 = (0 - oy_)
		return (result_29, ox_7, oy_7,)
		return ()
	G['reversecheck'] = f_reversecheck
	def f_simplecheck(x_33=None, y_33=None, noempty_=None, checkc=None, *_):  # L2496
		obs_2 = G['findobstacle'](x_33, y_33)
		noempty = (_t1 if L_t(_t1 := noempty_) else False)
		if (L_len(obs_2) > 0):
			for i_71, id__13 in L_ipairs(obs_2):
				if (id__13 == (-1)):
					return (-1)
				else:
					obsunit = G['mmf']['newObject'](id__13)
					obsname = G['getname'](obsunit)
					if (((((G['hasfeature'](obsname, 'is', 'stop', id__13, x_33, y_33, checkc) is not None) or (G['hasfeature'](obsname, 'is', 'push', id__13, x_33, y_33, checkc) is not None)) or (G['hasfeature'](obsname, 'is', 'pull', id__13, x_33, y_33, checkc) is not None)) and (G['hasfeature'](obsname, 'is', 'hide', id__13, x_33, y_33, checkc) is None)) and (G['hasfeature'](obsname, 'is', 'phantom', id__13, x_33, y_33, checkc) is None)):
						return 1
		elif (noempty is False):
			if (((((G['hasfeature']('empty', 'is', 'stop', 2, x_33, y_33, checkc) is not None) or (G['hasfeature']('empty', 'is', 'push', 2, x_33, y_33, checkc) is not None)) or (G['hasfeature']('empty', 'is', 'pull', 2, x_33, y_33, checkc) is not None)) and (G['hasfeature']('empty', 'is', 'phantom', 2, x_33, y_33, checkc) is None)) and (G['hasfeature']('empty', 'is', 'hide', 2, x_33, y_33, checkc) is None)):
				return 2
		return 0
	G['simplecheck'] = f_simplecheck
