"""Generated from syntax.lua by tools/lua2py.py. Do not edit."""
from babasim.luart import *  # noqa: F403


def load(G):
	def f_addunit(id_=None, undoing_=None, levelstart_=None, *_):  # L1
		unitid = (L_len(G['units']) + 1)
		G['units'][unitid] = L_T()
		G['units'][unitid] = G['mmf']['newObject'](id_)
		unit = G['units'][unitid]
		undoing = (_t1 if L_t(_t1 := undoing_) else False)
		levelstart = (_t2 if L_t(_t2 := levelstart_) else False)
		G['getmetadata'](unit)
		truename = unit['className']
		if (G['changes'][truename] is not None):
			G['dochanges'](id_)
		if (unit['values'][G['ID']] == (-1)):
			unit['values'][G['ID']] = G['newid']()
		if ((unit['values'][G['XPOS']] > 0) and (unit['values'][G['YPOS']] > 0)):
			G['addunitmap'](id_, unit['values'][G['XPOS']], unit['values'][G['YPOS']], unit['strings'][G['UNITNAME']])
		if (unit['values'][G['TILING']] == 1):
			L_insert(G['tiledunits'], unit['fixed'])
		if (unit['values'][G['TILING']] > 1):
			L_insert(G['animunits'], unit['fixed'])
		name = G['getname'](unit)
		name_ = unit['strings'][G['NAME']]
		name__ = unit['strings'][G['UNITNAME']]
		unit['originalname'] = unit['strings'][G['UNITNAME']]
		if (G['unitlists'][name] is None):
			G['unitlists'][name] = L_T()
		if (L_sub(name_, 1, 5) == 'text_'):
			unit['flags'][G['META']] = True
		L_insert(G['unitlists'][name], unit['fixed'])
		if (name != name__):
			if (G['unitlists'][name__] is None):
				G['unitlists'][name__] = L_T()
			L_insert(G['unitlists'][name__], unit['fixed'])
		if ((unit['strings'][G['UNITTYPE']] != 'text') or ((unit['strings'][G['UNITTYPE']] == 'text') and (unit['values'][G['TYPE']] == 0))):
			G['objectlist'][name_] = 1
		if (unit['strings'][G['UNITTYPE']] == 'text'):
			L_insert(G['codeunits'], unit['fixed'])
			G['updatecode'] = 1
			if (unit['values'][G['TYPE']] == 0):
				matname = L_sub(unit['strings'][G['UNITNAME']], 6)
				if (G['unitlists'][matname] is None):
					G['unitlists'][matname] = L_T()
			elif (unit['values'][G['TYPE']] == 5):
				L_insert(G['letterunits'], unit['fixed'])
		unit['colour'] = L_T()
		if ((unit['strings'][G['UNITNAME']] != 'level') and (unit['className'] != 'specialobject')):
			cc1, cc2 = L_adjust((*G['setcolour'](unit['fixed']),), 2)
			unit['colour'] = L_T([cc1, cc2])
		unit['back_init'] = 0
		unit['broken'] = 0
		if ((unit['className'] != 'path') and (unit['className'] != 'specialobject')):
			G['statusblock'](L_T([id_]), undoing)
			G['MF_animframe'](id_, G['math']['random'](0, 2))
		unit['active'] = False
		unit['new'] = True
		unit['colours'] = L_T()
		unit['currcolour'] = 0
		unit['followed'] = (-1)
		unit['holder'] = 0
		unit['xpos'] = unit['values'][G['XPOS']]
		unit['ypos'] = unit['values'][G['YPOS']]
		if ((G['spritedata']['values'][G['VISION']] == 1) and (undoing is False)):
			hasvision = G['hasfeature'](name, 'is', '3d', id_, unit['values'][G['XPOS']], unit['values'][G['YPOS']])
			if (hasvision is not None):
				L_insert(G['visiontargets'], id_)
			elif (G['spritedata']['values'][G['CAMTARGET']] == unit['values'][G['ID']]):
				G['visionmode'](0, 0, None, L_T([unit['values'][G['XPOS']], unit['values'][G['YPOS']], unit['values'][G['DIR']]]))
		if ((G['spritedata']['values'][G['VISION']] == 1) and (G['spritedata']['values'][G['CAMTARGET']] != unit['values'][G['ID']])):
			if (unit['values'][G['ZLAYER']] <= 15):
				if (unit['values'][G['ZLAYER']] > 10):
					G['setupvision_wall'](unit['fixed'])
				G['MF_setupvision_single'](unit['fixed'])
		if (L_t(G['generaldata']['flags'][G['LOGGING']]) and (G['generaldata']['flags'][G['RESTARTED']] is False)):
			if (levelstart is not None and levelstart is not False):
				G['dolog']('init_object', 'event', L_concat(unit['strings'][G['UNITNAME']], ':', L_tostring(unit['values'][G['XPOS']]), ':', L_tostring(unit['values'][G['YPOS']])))
			elif (undoing is False):
				G['dolog']('new_object', 'event', L_concat(unit['strings'][G['UNITNAME']], ':', L_tostring(unit['values'][G['XPOS']]), ':', L_tostring(unit['values'][G['YPOS']])))
	G['addunit'] = f_addunit
	def f_cleanup(*_):  # L127
		G['emptydata'] = L_T()
	G['cleanup'] = f_cleanup
	def f_command(key=None, player_=None, *_):  # L131
		keyid = (-1)
		if (G['keys'][key] is not None):
			keyid = G['keys'][key]
		else:
			L_noop('no such key')
			return None
		player = 1
		if (player_ is not None):
			player = player_
		G['do_mod_hook']('command_given', L_T([key, player]))
		if (keyid <= 4):
			if (G['generaldata5']['values'][G['AUTO_ON']] == 0):
				drs = G['ndirs'][(keyid + 1)]
				ox = drs[1]
				oy = drs[2]
				dir_ = keyid
				G['last_key'] = keyid
				if (G['auto_dir'][player] is None):
					G['auto_dir'][player] = 4
				G['auto_dir'][player] = keyid
				if ((G['spritedata']['values'][G['VISION']] == 1) and (dir_ == 3)):
					if (L_len(G['units']) > 0):
						G['changevisiontarget']()
					G['movecommand'](ox, oy, dir_, player, None, True)
					G['MF_update']()
				else:
					G['movecommand'](ox, oy, dir_, player)
					G['MF_update']()
			else:
				if (G['auto_dir'][player] is None):
					G['auto_dir'][player] = 4
				G['auto_dir'][player] = keyid
				if ((G['auto_dir'][1] is None) and (G['featureindex']['you2'] is None)):
					G['auto_dir'][1] = keyid
		if (keyid == 5):
			G['MF_restart'](False)
		elif (keyid == 8):
			G['MF_restart'](True)
		G['dolog'](key)
	G['command'] = f_command
	def f_command_auto(*_):  # L196
		moving = False
		firstp = (-1)
		secondp = (-1)
		if (G['auto_dir'][1] is not None):
			firstp = G['auto_dir'][1]
			moving = True
		else:
			firstp = 4
			moving = True
		if (G['auto_dir'][2] is not None):
			secondp = G['auto_dir'][2]
			moving = True
		else:
			secondp = 4
			moving = True
		G['do_mod_hook']('turn_auto', L_T([firstp, secondp, moving]))
		if ((moving is not None and moving is not False) and (G['generaldata5']['values'][G['AUTO_ON']] > 0)):
			for i in L_range(1, G['generaldata5']['values'][G['AUTO_ON']]):
				if (firstp != 4):
					G['last_key'] = firstp
				elif (secondp != 4):
					G['last_key'] = secondp
				else:
					G['last_key'] = 4
				drs_2 = G['ndirs'][(firstp + 1)]
				ox_2 = drs_2[1]
				oy_2 = drs_2[2]
				dir__2 = firstp
				if ((G['spritedata']['values'][G['VISION']] == 1) and (dir__2 == 3)):
					if (L_len(G['units']) > 0):
						G['changevisiontarget']()
					G['movecommand'](ox_2, oy_2, dir__2, 3, secondp, True)
				else:
					G['movecommand'](ox_2, oy_2, dir__2, 3, secondp)
			G['MF_update']()
		G['auto_dir'] = L_T()
	G['command_auto'] = f_command_auto
	def f_dolog(key_2=None, etype=None, details_=None, *_):  # L250
		if L_t(G['generaldata']['flags'][G['LOGGING']]):
			event = (_t1 if L_t(_t1 := etype) else 'input')
			details = (_t2 if L_t(_t2 := details_) else '')
			G['MF_log'](event, key_2, details)
	G['dolog'] = f_dolog
	def f_createall(matdata=None, x_=None, y_=None, id__2=None, dolevels_=None, leveldata_=None, *_):  # L259
		all = L_T()
		empty = False
		dolevels = (_t1 if L_t(_t1 := dolevels_) else False)
		leveldata = (_t2 if L_t(_t2 := leveldata_) else L_T())
		if (((x_ is None) and (y_ is None)) and (id__2 is None)):
			if ((matdata[1] != 'empty') and (G['findnoun'](matdata[1], G['nlist']['brief']) is False)):
				all = G['findall'](matdata)
			elif (matdata[1] == 'empty'):
				all = G['findempty'](matdata[2])
				empty = True
		test = L_T()
		if (((x_ is not None) and (y_ is not None)) and (id__2 is not None)):
			check = G['findtype'](matdata, x_, y_, id__2)
			if (L_len(check) > 0):
				for i_2, v in L_ipairs(check):
					if (v != 0):
						L_insert(test, v)
		if (L_len(all) > 0):
			for i_3, v_2 in L_ipairs(all):
				L_insert(test, v_2)
		if (dolevels is False):
			delthese = L_T()
			if (L_len(test) > 0):
				for i_4, v_3 in L_ipairs(test):
					if (empty is False):
						vunit = G['mmf']['newObject'](v_3)
						x, y, dir__3 = vunit['values'][G['XPOS']], vunit['values'][G['YPOS']], vunit['values'][G['DIR']]
						if (vunit['flags'][G['CONVERTED']] is False):
							for b, unit_2 in L_pairs(G['objectlist']):
								if ((G['findnoun'](b) is False) and (b != matdata[1])):
									protect = G['hasfeature'](matdata[1], 'is', L_concat('not ', b), v_3, x, y)
									if (protect is None):
										mat = G['findtype'](L_T([b]), x, y, v_3)
										if (L_len(mat) == 0):
											nunitid, ningameid = L_adjust((*G['create'](b, x, y, dir__3, None, None, None, None, leveldata),), 2)
											G['addundo'](L_T(['convert', matdata[1], mat, ningameid, vunit['values'][G['ID']], x, y, dir__3]))
											if ((matdata[1] == 'text') or (matdata[1] == 'level')):
												L_insert(delthese, v_3)
					else:
						x_2 = (v_3 % G['roomsizex'])
						y_2 = L_floor(L_div(v_3, G['roomsizex']))
						dir__4 = G['emptydir'](x_2, y_2)
						if (dir__4 == 4):
							dir__4 = G['fixedrandom'](0, 3)
						blocked = L_T()
						valid = True
						if (G['emptydata'][v_3] is not None):
							if ((G['emptydata'][v_3]['conv'] is not None) and L_t(G['emptydata'][v_3]['conv'])):
								valid = False
						if (valid is not None and valid is not False):
							if (G['featureindex']['empty'] is not None):
								for i_5, rules in L_ipairs(G['featureindex']['empty']):
									rule = rules[1]
									conds = rules[2]
									if (((rule[1] == 'empty') and (rule[2] == 'is')) and (L_sub(rule[3], 1, 4) == 'not ')):
										if L_t(G['testcond'](conds, 1, x_2, y_2)):
											target = L_sub(rule[3], 5)
											blocked[target] = 1
							if (blocked['all'] is None):
								for b_2, mat_2 in L_pairs(G['objectlist']):
									if ((G['findnoun'](b_2) is False) and (blocked[b_2] is None)):
										nunitid_2, ningameid_2 = L_adjust((*G['create'](b_2, x_2, y_2, dir__4, None, None, None, None, leveldata),), 2)
										G['addundo'](L_T(['convert', matdata[1], mat_2, ningameid_2, 2, x_2, y_2, dir__4]))
			for a, b_3 in L_ipairs(delthese):
				G['delete'](b_3)
		if ((matdata[1] == 'level') and (dolevels is not None and dolevels is not False)):
			blocked_2 = L_T()
			if (G['featureindex']['level'] is not None):
				for i_6, rules_2 in L_ipairs(G['featureindex']['level']):
					rule_2 = rules_2[1]
					conds_2 = rules_2[2]
					if (((rule_2[1] == 'level') and (rule_2[2] == 'is')) and (L_sub(rule_2[3], 1, 4) == 'not ')):
						if L_t(G['testcond'](conds_2, 1, G['x'], G['y'])):
							target_2 = L_sub(rule_2[3], 5)
							blocked_2[target_2] = 1
			if ((blocked_2['all'] is None) and ((matdata[2] is None) or L_t(G['testcond'](matdata[2], 1)))):
				for b_4, unit_3 in L_pairs(G['objectlist']):
					if ((((G['findnoun'](b_4, G['nlist']['brief']) is False) and (b_4 != 'empty')) and (b_4 != 'level')) and (blocked_2[G['target']] is None)):
						L_insert(G['levelconversions'], L_T([b_4, L_T()]))
	G['createall'] = f_createall
	def f_createall_single(unitid_2=None, conds_3=None, x__2=None, y__2=None, id__3=None, dolevels__2=None, leveldata__2=None, *_):  # L402
		all_2 = L_T()
		empty_2 = False
		dolevels_2 = (_t1 if L_t(_t1 := dolevels__2) else False)
		delthis = False
		leveldata_2 = (_t2 if L_t(_t2 := leveldata__2) else L_T())
		vunit_2 = None
		x_3, y_3, dir__5, name_2, id__4 = x__2, y__2, 4, '', id__3
		if (unitid_2 != 2):
			vunit_2 = G['mmf']['newObject'](unitid_2)
			x_3, y_3, dir__5, id__4 = vunit_2['values'][G['XPOS']], vunit_2['values'][G['YPOS']], vunit_2['values'][G['DIR']], vunit_2['values'][G['ID']]
			name_2 = G['getname'](vunit_2)
		else:
			name_2 = 'empty'
			dir__5 = G['emptydir'](x_3, y_3)
			if (dir__5 == 4):
				dir__5 = G['fixedrandom'](0, 3)
		for b_5, unit_4 in L_pairs(G['objectlist']):
			if ((G['findnoun'](b_5) is False) and (b_5 != name_2)):
				protect_2 = G['hasfeature'](name_2, 'is', L_concat('not ', b_5), unitid_2, x_3, y_3)
				if (protect_2 is None):
					mat_3 = G['findtype'](L_T([b_5]), x_3, y_3, unitid_2)
					if (L_len(mat_3) == 0):
						nunitid_3, ningameid_3 = L_adjust((*G['create'](b_5, x_3, y_3, dir__5, None, None, None, None, leveldata_2),), 2)
						G['addundo'](L_T(['convert', name_2, mat_3, ningameid_3, id__4, x_3, y_3, dir__5]))
						nunit = G['mmf']['newObject'](nunitid_3)
						if (unitid_2 != 2):
							nunit['originalname'] = vunit_2['originalname']
						else:
							nunit['originalname'] = 'empty'
						if ((name_2 == 'text') or (name_2 == 'level')):
							delthis = True
		if ((name_2 == 'level') and (dolevels_2 is not None and dolevels_2 is not False)):
			blocked_3 = L_T()
			if (G['featureindex']['level'] is not None):
				for i_7, rules_3 in L_ipairs(G['featureindex']['level']):
					rule_3 = rules_3[1]
					conds_4 = rules_3[2]
					if (((rule_3[1] == 'level') and (rule_3[2] == 'is')) and (L_sub(rule_3[3], 1, 4) == 'not ')):
						if L_t(G['testcond'](conds_4, 1, x_3, y_3)):
							target_3 = L_sub(rule_3[3], 5)
							blocked_3[target_3] = 1
			if ((blocked_3['all'] is None) and ((conds_3 is None) or L_t(G['testcond'](conds_3, 1)))):
				for b_6, unit_5 in L_pairs(G['objectlist']):
					if ((((G['findnoun'](b_6, G['nlist']['brief']) is False) and (b_6 != 'empty')) and (b_6 != 'level')) and (blocked_3[G['target']] is None)):
						L_insert(G['levelconversions'], L_T([b_6, L_T()]))
		return delthis
	G['createall_single'] = f_createall_single
	def f_setunitmap(*_):  # L482
		G['unitmap'] = L_T()
		G['unittypeshere'] = L_T()
		delthese_2 = L_T()
		limit = 6
		if ((G['generaldata']['strings'][G['WORLD']] == G['generaldata']['strings'][G['BASEWORLD']]) and ((G['generaldata']['strings'][G['CURRLEVEL']] == '89level') or (G['generaldata']['strings'][G['CURRLEVEL']] == '33level'))):
			limit = 3
		if ((G['generaldata']['strings'][G['WORLD']] == 'baba_m') and ((G['generaldata']['strings'][G['CURRLEVEL']] == '89level') or (G['generaldata']['strings'][G['CURRLEVEL']] == '33level'))):
			limit = 2
		for i_8, unit_6 in L_ipairs(G['units']):
			tileid = (unit_6['values'][G['XPOS']] + (unit_6['values'][G['YPOS']] * G['roomsizex']))
			valid_2 = True
			if (G['unitmap'][tileid] is None):
				G['unitmap'][tileid] = L_T()
				G['unittypeshere'][tileid] = L_T()
			uth = G['unittypeshere'][tileid]
			name_3 = unit_6['strings'][G['UNITNAME']]
			if (uth[name_3] is None):
				uth[name_3] = 0
			if (uth[name_3] < limit):
				uth[name_3] = (uth[name_3] + 1)
			elif (L_strlen(unit_6['strings'][G['U_LEVELFILE']]) == 0):
				L_insert(delthese_2, unit_6)
				valid_2 = False
			if (valid_2 is not None and valid_2 is not False):
				L_insert(G['unitmap'][tileid], unit_6['fixed'])
		for i_9, unit_7 in L_ipairs(delthese_2):
			x_4, y_4, dir__6, unitname = unit_7['values'][G['XPOS']], unit_7['values'][G['YPOS']], unit_7['values'][G['DIR']], unit_7['strings'][G['UNITNAME']]
			G['addundo'](L_T(['remove', unitname, x_4, y_4, dir__6, unit_7['values'][G['ID']], unit_7['values'][G['ID']], unit_7['strings'][G['U_LEVELFILE']], unit_7['strings'][G['U_LEVELNAME']], unit_7['values'][G['VISUALLEVEL']], unit_7['values'][G['COMPLETED']], unit_7['values'][G['VISUALSTYLE']], unit_7['flags'][G['MAPLEVEL']], unit_7['strings'][G['COLOUR']], unit_7['strings'][G['CLEARCOLOUR']], unit_7['followed'], unit_7['back_init'], unit_7['originalname'], unit_7['strings'][G['UNITSIGNTEXT']], unit_7['holder']]))
			G['delunit'](unit_7['fixed'])
			G['MF_remove'](unit_7['fixed'])
	G['setunitmap'] = f_setunitmap
	def f_setundo(this=None, *_):  # L535
		if (this is not None):
			if (this == 1):
				G['updateundo'] = True
			elif (this == 0):
				G['updateundo'] = False
		else:
			L_noop('undo is nil!')
			G['updateundo'] = True
	G['setundo'] = f_setundo
	def f_victory(*_):  # L548
		G['MF_win']()
	G['victory'] = f_victory
	def f_poscorrect(unitid_3=None, rotation=None, zoom=None, offset=None, *_):  # L552
		unit_8 = G['mmf']['newObject'](unitid_3)
		if ((G['spritedata']['values'][G['VISION']] == 0) or ((unit_8['values'][G['ZLAYER']] >= 21) and (G['spritedata']['values'][G['DOPOSCORRECT']] == 0))):
			if (unit_8 is not None):
				midpointx = (((G['roomsizex'] * G['tilesize']) * 0.5) * G['spritedata']['values'][G['TILEMULT']])
				midtilex = (L_floor((G['roomsizex'] * 0.5)) - 0.5)
				if ((G['roomsizex'] % 2) == 1):
					midtilex = L_floor((G['roomsizex'] * 0.5))
				midpointy = (((G['roomsizey'] * G['tilesize']) * 0.5) * G['spritedata']['values'][G['TILEMULT']])
				midtiley = (L_floor((G['roomsizey'] * 0.5)) - 0.5)
				if ((G['roomsizey'] % 2) == 1):
					midtiley = L_floor((G['roomsizey'] * 0.5))
				x_5, y_5 = unit_8['values'][G['XPOS']], unit_8['values'][G['YPOS']]
				dx = (x_5 - midtilex)
				dy = (y_5 - midtiley)
				dir__7 = ((0 - G['math']['atan2'](dy, dx)) + G['math']['rad'](rotation))
				dist = G['math']['sqrt']((L_pow(dy, 2) + L_pow(dx, 2)))
				newx = ((G['Xoffset'] + midpointx) + ((((G['math']['cos'](dir__7) * dist) * zoom) * G['tilesize']) * G['spritedata']['values'][G['TILEMULT']]))
				newy = ((G['Yoffset'] + midpointy) - ((((G['math']['sin'](dir__7) * dist) * zoom) * G['tilesize']) * G['spritedata']['values'][G['TILEMULT']]))
				if (unit_8['values'][G['FLOAT']] == 0):
					unit_8['x'] = newx
					unit_8['y'] = (newy + (offset * G['spritedata']['values'][G['TILEMULT']]))
				elif (unit_8['values'][G['FLOAT']] == 1):
					unit_8['x'] = newx
			else:
				G['MF_alert'](L_concat('Poscorrect: unitid ', L_tostring(unitid_3), " isn't valid!"))
	G['poscorrect'] = f_poscorrect
	def f_stringintable(this_2=None, data=None, *_):  # L594
		if (L_len(data) > 0):
			for i_10, v_4 in L_ipairs(data):
				if (this_2 == v_4):
					return True
		return False
	G['stringintable'] = f_stringintable
	def f_levelborder(absolute_=None, ox_=None, oy_=None, *_):  # L606
		G['edgetiles'] = L_T()
		l = G['map'][0]
		absolute = (_t1 if L_t(_t1 := absolute_) else False)
		ox_3, oy_3 = G['Xoffset'], G['Yoffset']
		if (absolute is not None and absolute is not False):
			ox_3 = ox_
			oy_3 = oy_
		for i_11 in L_range(0, (G['roomsizex'] - 1)):
			for j in L_range(0, (G['roomsizey'] - 1)):
				if ((((i_11 == 0) or (j == 0)) or (i_11 == (G['roomsizex'] - 1))) or (j == (G['roomsizey'] - 1))):
					unitid_4 = G['MF_create']('edge')
					unit_9 = G['mmf']['newObject'](unitid_4)
					L_insert(G['edgetiles'], unitid_4)
					unit_9['layer'] = 1
					unit_9['values'][G['ONLINE']] = 1
					unit_9['values'][G['XPOS']] = i_11
					unit_9['values'][G['YPOS']] = j
					unit_9['values'][G['POSITIONING']] = 20
					unit_9['x'] = ((ox_3 + ((i_11 * G['tilesize']) * G['spritedata']['values'][G['TILEMULT']])) + ((G['tilesize'] * 0.5) * G['spritedata']['values'][G['TILEMULT']]))
					unit_9['y'] = ((oy_3 + ((j * G['tilesize']) * G['spritedata']['values'][G['TILEMULT']])) + ((G['tilesize'] * 0.5) * G['spritedata']['values'][G['TILEMULT']]))
					unit_9['scaleX'] = (G['spritedata']['values'][G['SPRITEMULT']] * G['spritedata']['values'][G['TILEMULT']])
					unit_9['scaleY'] = (G['spritedata']['values'][G['SPRITEMULT']] * G['spritedata']['values'][G['TILEMULT']])
					L_invoke(l, 'set', i_11, j, 0, 0)
		c1, c2 = L_adjust((*G['getuicolour']('edge'),), 2)
		for i_12, unitid_5 in L_ipairs(G['edgetiles']):
			unit_10 = G['mmf']['newObject'](unitid_5)
			dynamicdir = L_first(G['dynamictile'](unitid_5, unit_10['values'][G['XPOS']], unit_10['values'][G['YPOS']], 'edge'))
			unit_10['direction'] = dynamicdir
			G['MF_setcolour'](unitid_5, c1, c2)
	G['levelborder'] = f_levelborder
	def f_updatescreen(x_6=None, y_6=None, *_):  # L654
		G['Xoffset'] = x_6
		G['Yoffset'] = y_6
	G['updatescreen'] = f_updatescreen
	G['HACK_ROOMSIZEUNDO'] = False
	G['HACK_ROOMSIZEUNDO_DELTHESE'] = L_T()
	def f_updateroomsize(tilesize_=None, roomsizex_=None, roomsizey_=None, *_):  # L662
		G['tilesize'] = tilesize_
		G['HACK_ROOMSIZEUNDO_DELTHESE'] = L_T()
		G['roomsizex'] = roomsizex_
		G['roomsizey'] = roomsizey_
		delthese_3 = L_T()
		for i_13, unit_11 in L_pairs(G['units']):
			if ((unit_11['values'][G['XPOS']] >= (G['roomsizex'] - 1)) or (unit_11['values'][G['YPOS']] >= (G['roomsizey'] - 1))):
				L_insert(delthese_3, unit_11['fixed'])
			else:
				G['MF_setsublayer'](0, unit_11['values'][G['XPOS']], unit_11['values'][G['YPOS']], unit_11['values'][G['LAYER']], unit_11['values'][G['DIR']])
		for i_14, v_5 in L_ipairs(delthese_3):
			unit_12 = G['mmf']['newObject'](v_5)
			if (G['generaldata']['values'][G['MODE']] == 5):
				G['removetile'](unit_12['fixed'], unit_12['values'][G['XPOS']], unit_12['values'][G['YPOS']])
			else:
				if (G['HACK_ROOMSIZEUNDO'] is False):
					G['delunit'](unit_12['fixed'])
				else:
					L_insert(G['HACK_ROOMSIZEUNDO_DELTHESE'], unit_12['fixed'])
		G['setunitmap']()
	G['updateroomsize'] = f_updateroomsize
	def f_checkerasesafety(text_=None, *_):  # L696
		text = L_sub(text_, 2, (L_strlen(text_) - 1))
		delete = True
		G['MF_alert'](L_concat(text_, ', ', text))
		if (((((L_sub(text, 1, 5) == 'baba_') or (L_sub(text, 1, 8) == 'new_adv_')) or (L_sub(text, 1, 7) == 'museum_')) and (L_sub(text, (-8)) == '_convert')) and (L_strlen(text) > 13)):
			delete = False
		sparethese = L_T([], {'baba': 1, 'baba_prize': 2, 'baba_clears': 3, 'baba_bonus': 4, 'baba_complete': 5, 'baba_converts': 6, 'baba_converts_single': 7, 'baba_end_single': 8, 'baba_done_single': 9, 'baba_m': 1, 'baba_m_prize': 2, 'baba_m_clears': 3, 'baba_m_bonus': 4, 'baba_m_complete': 5, 'baba_m_converts': 6, 'baba_m_converts_single': 7, 'baba_m_end_single': 8, 'baba_m_done_single': 9, 'new_adv': 1, 'new_adv_prize': 2, 'new_adv_clears': 3, 'new_adv_bonus': 4, 'new_adv_complete': 5, 'new_adv_converts': 6, 'new_adv_converts_single': 7, 'new_adv_end_single': 8, 'new_adv_done_single': 9, 'museum': 1, 'museum_prize': 2, 'museum_clears': 3, 'museum_bonus': 4, 'museum_complete': 5, 'museum_converts': 6, 'museum_converts_single': 7, 'museum_end_single': 8, 'museum_done_single': 9})
		if (sparethese[text] is not None):
			delete = False
		return (delete, text,)
		return ()
	G['checkerasesafety'] = f_checkerasesafety
	def f_fixedrandom(low=None, high=None, *_):  # L757
		if (G['Seedingtype'] > 0):
			G['Seed'] = G['math']['random'](0, 2147483647)
			G['math']['randomseed'](G['Fixedseed'])
		result = G['math']['random'](low, high)
		if (G['Seedingtype'] > 0):
			G['Fixedseed'] = G['math']['random'](0, 2147483647)
			G['math']['randomseed'](G['Seed'])
		return result
	G['fixedrandom'] = f_fixedrandom
	def f_setfixedrandom(text_2=None, *_):  # L773
		if (G['Seedingtype'] == 2):
			G['Fixedseed'] = (L_strlen(text_2) * L_len(G['units']))
		elif (G['Seedingtype'] == 1):
			G['Fixedseed'] = G['MF_random'](1, 2147483647)
	G['setfixedrandom'] = f_setfixedrandom
	def f_overrideundoseeding(*_):  # L781
		undob = G['undobuffer'][1]
		undob['fixedseed'] = G['Fixedseed']
	G['overrideundoseeding'] = f_overrideundoseeding
	def f_setseedingtype(t=None, *_):  # L786
		G['Seedingtype'] = t
	G['setseedingtype'] = f_setseedingtype
	def f_generatefreqs(*_):  # L790
		notes = L_T(['c', 'csharp', 'd', 'dsharp', 'e', 'f', 'fsharp', 'g', 'gsharp', 'a', 'asharp', 'b'])
		octaves = 3
		base = G['base_octave']
		step = L_pow(2, L_div(1, 12))
		basefreq = (24000 * L_pow(step, 3))
		freq = basefreq
		prev = 'b'
		for i_15, v_6 in L_ipairs(notes):
			G['play_data']['freqs'][v_6] = L_floor(freq)
			freq = (freq * step)
		freq = basefreq
		G['play_data']['freqs']['aflat'] = L_div(freq, step)
		for i_16, v_7 in L_ipairs(notes):
			if (L_sub(v_7, (-5)) != 'sharp'):
				name_4 = L_concat(v_7, 'flat')
				pair = L_concat(prev, 'sharp')
				if ((L_sub(name_4, 1, 1) == 'c') or (L_sub(name_4, 1, 1) == 'f')):
					pair = prev
				if (G['play_data']['freqs'][pair] is not None):
					G['play_data']['freqs'][name_4] = G['play_data']['freqs'][pair]
				prev = v_7
		G['play_data']['freqs']['bsharp'] = G['play_data']['freqs']['c']
		G['play_data']['freqs']['esharp'] = G['play_data']['freqs']['f']
		freq = basefreq
		for j_ in L_range(1, octaves):
			j_2 = (base + (j_ - 1))
			freq = ((basefreq * 0.5) * L_pow(2, j_))
			prev = 'b'
			for i_17, v_8 in L_ipairs(notes):
				name_5 = L_concat(v_8, L_tostring(j_2))
				G['play_data']['freqs'][name_5] = L_floor((freq * 0.5))
				freq = (freq * step)
			freq = ((basefreq * 0.5) * L_pow(2, j_))
			aflat = L_concat('aflat', L_tostring(j_2))
			G['play_data']['freqs'][aflat] = L_div(freq, step)
			for i_18, v_9 in L_ipairs(notes):
				if (L_sub(v_9, (-5)) != 'sharp'):
					name_6 = L_concat(v_9, 'flat', L_tostring(j_2))
					pair_2 = L_concat(prev, 'sharp', L_tostring(j_2))
					if ((L_sub(name_6, 1, 1) == 'c') or (L_sub(name_6, 1, 1) == 'f')):
						pair_2 = L_concat(prev, L_tostring(j_2))
					if ((G['play_data']['freqs'][pair_2] is not None) and (G['play_data']['freqs'][pair_2] < 100000)):
						G['play_data']['freqs'][name_6] = G['play_data']['freqs'][pair_2]
					prev = v_9
		G['play_data']['freqs']['bsharp4'] = G['play_data']['freqs']['c4']
		G['play_data']['freqs']['esharp4'] = G['play_data']['freqs']['f4']
		G['play_data']['freqs']['bsharp5'] = G['play_data']['freqs']['c5']
		G['play_data']['freqs']['esharp5'] = G['play_data']['freqs']['f5']
		G['play_data']['freqs']['esharp6'] = G['play_data']['freqs']['f6']
	G['generatefreqs'] = f_generatefreqs
	def f_setupnounlists(*_):  # L878
		G['nlist']['full'] = L_T(['group', 'all', 'text', 'empty', 'level'])
		G['nlist']['short'] = L_T(['group', 'all', 'text', 'empty'])
		G['nlist']['brief'] = L_T(['group', 'all'])
		G['nlist']['objects'] = L_T(['text', 'empty'])
		G['nlist']['conversions'] = L_T(['createall', 'empty', 'revert'])
	G['setupnounlists'] = f_setupnounlists
	def f_update_cleanup(*_):  # L886
		G['HACK_INFINITY'] = 0
	G['update_cleanup'] = f_update_cleanup
