"""Generated from undo.lua by tools/lua2py.py. Do not edit."""
from babasim.luart import *  # noqa: F403


def load(G):
	def f_newundo(*_):  # L1
		if ((G['updateundo'] is False) or (G['doundo'] is False)):
			L_remove(G['undobuffer'], 1)
		else:
			G['generaldata2']['values'][G['UNDOTOOLTIPTIMER']] = 0
		L_insert(G['undobuffer'], 1, L_T())
		thisundo = G['undobuffer'][1]
		thisundo['key'] = G['last_key']
		thisundo['fixedseed'] = G['Fixedseed']
		if (thisundo is not None):
			thisundo['wordunits'] = L_T()
			thisundo['wordrelatedunits'] = L_T()
			thisundo['visiontargets'] = L_T()
			if (L_len(G['wordunits']) > 0):
				for i, v in L_ipairs(G['wordunits']):
					wunit = G['mmf']['newObject'](v[1])
					L_insert(thisundo['wordunits'], wunit['values'][G['ID']])
			if (L_len(G['visiontargets']) > 0):
				for i_2, v_2 in L_ipairs(G['visiontargets']):
					wunit_2 = G['mmf']['newObject'](v_2)
					L_insert(thisundo['visiontargets'], wunit_2['values'][G['ID']])
			if (L_len(G['wordrelatedunits']) > 0):
				for i_3, v_3 in L_ipairs(G['wordrelatedunits']):
					if (v_3[1] != 2):
						wunit_3 = G['mmf']['newObject'](v_3[1])
						L_insert(thisundo['wordrelatedunits'], wunit_3['values'][G['ID']])
					else:
						pass
		G['updateundo'] = False
	G['newundo'] = f_newundo
	def f_addundo(line=None, uid_=None, *_):  # L52
		uid = L_tostring(uid_)
		if L_t(G['doundo']):
			currentundo = G['undobuffer'][1]
			text = L_concat(L_tostring(L_len(G['undobuffer'])), ', ')
			L_insert(currentundo, 1, L_T())
			currentundo[1] = L_T()
			for i_4, v_4 in L_ipairs(line):
				L_insert(currentundo[1], v_4)
				text = L_concat(text, L_tostring(v_4), ', ')
			text = L_concat(text, uid)
			ename = line[1]
			if (L_t(G['generaldata']['flags'][G['LOGGING']]) and L_t(G['logevents'])):
				details = ''
				if (ename == 'update'):
					details = L_concat(line[2], ':', L_tostring(line[6]), ':', L_tostring(line[7]), ':', L_tostring(line[8]))
				elif (ename == 'remove'):
					details = L_concat(line[2], ':', L_tostring(line[3]), ':', L_tostring(line[4]), ':', L_tostring(line[5]))
				elif (ename == 'create'):
					details = L_concat(line[2], ':', L_tostring(line[6]), ':', L_tostring(line[7]), ':', L_tostring(line[8]))
				elif (ename == 'float'):
					details = L_concat(line[2], ':', L_tostring(line[4]), ':', L_tostring(line[5]))
				elif (ename == 'levelupdate'):
					details = L_concat(L_tostring(line[4]), ':', L_tostring(line[5]))
				elif (ename == 'maprotation'):
					details = L_concat(L_tostring(line[3]), ':', L_tostring(line[4]))
				elif (ename == 'mapcursor'):
					details = L_concat(L_tostring(line[8]), ':', L_tostring(line[9]), ':', L_tostring(line[10]))
				elif (ename == 'broken'):
					details = L_concat(L_tostring(line[4]), ':', L_tostring(line[2]))
				elif (ename == 'followed'):
					details = L_concat(L_tostring(line[5]), ':', L_tostring(line[3]))
				G['dolog'](ename, 'change', details)
	G['addundo'] = f_addundo
	def f_undo(*_):  # L100
		result = 0
		G['HACK_INFINITY'] = 0
		G['logevents'] = False
		if (L_len(G['undobuffer']) > 1):
			result = 1
			currentundo_2 = G['undobuffer'][2]
			G['do_mod_hook']('undoed')
			G['last_key'] = (_t1 if L_t(_t1 := currentundo_2['key']) else 0)
			G['Fixedseed'] = (_t2 if L_t(_t2 := currentundo_2['fixedseed']) else 100)
			if (currentundo_2 is not None):
				for i_5, line_2 in L_ipairs(currentundo_2):
					style = line_2[1]
					if (style == 'update'):
						uid_2 = line_2[9]
						if (G['paradox'][uid_2] is None):
							unitid = G['getunitid'](line_2[9])
							unit = G['mmf']['newObject'](unitid)
							oldx, oldy = unit['values'][G['XPOS']], unit['values'][G['YPOS']]
							x, y, dir_ = line_2[3], line_2[4], line_2[5]
							unit['values'][G['XPOS']] = x
							unit['values'][G['YPOS']] = y
							unit['values'][G['DIR']] = dir_
							unit['values'][G['POSITIONING']] = 0
							G['updateunitmap'](unitid, oldx, oldy, x, y, unit['strings'][G['UNITNAME']])
							G['dynamic'](unitid)
							G['dynamicat'](oldx, oldy)
							if (G['spritedata']['values'][G['CAMTARGET']] == uid_2):
								G['MF_updatevision'](dir_)
							ox = abs((oldx - x))
							oy = abs((oldy - y))
							if (((ox + oy) == 1) and (unit['values'][G['TILING']] == 2)):
								unit['values'][G['VISUALDIR']] = (((unit['values'][G['VISUALDIR']] - 1) + 4) % 4)
								unit['direction'] = ((unit['values'][G['DIR']] * 8) + unit['values'][G['VISUALDIR']])
							if (unit['strings'][G['UNITTYPE']] == 'text'):
								G['updatecode'] = 1
							undowordunits = currentundo_2['wordunits']
							undowordrelatedunits = currentundo_2['wordrelatedunits']
							if (L_len(undowordunits) > 0):
								for a, b in L_pairs(undowordunits):
									if (b == line_2[9]):
										G['updatecode'] = 1
							if (L_len(undowordrelatedunits) > 0):
								for a_2, b_2 in L_pairs(undowordrelatedunits):
									if (b_2 == line_2[9]):
										G['updatecode'] = 1
						else:
							G['particles']('hot', line_2[3], line_2[4], 1, L_T([1, 1]))
					elif (style == 'remove'):
						uid_3 = line_2[6]
						baseuid = (_t3 if L_t(_t3 := line_2[7]) else (-1))
						if ((G['paradox'][uid_3] is None) and (G['paradox'][baseuid] is None)):
							x_2, y_2, dir__2, levelfile, levelname, vislevel, complete, visstyle, maplevel, colour, clearcolour, followed, back_init, ogname, signtext, holder = line_2[3], line_2[4], line_2[5], line_2[8], line_2[9], line_2[10], line_2[11], line_2[12], line_2[13], line_2[14], line_2[15], line_2[16], line_2[17], line_2[18], line_2[19], line_2[20]
							name = line_2[2]
							unitname = ''
							unitid_2 = 0
							unitname = G['unitreference'][name]
							if ((name == 'level') and (G['unitreference'][name] != 'level')):
								unitname = 'level'
								G['unitreference']['level'] = 'level'
								G['MF_alert']('ALERT! Unitreference for level was wrong!')
							unitid_2 = G['MF_emptycreate'](unitname, x_2, y_2)
							unit_2 = G['mmf']['newObject'](unitid_2)
							unit_2['values'][G['ONLINE']] = 1
							unit_2['values'][G['XPOS']] = x_2
							unit_2['values'][G['YPOS']] = y_2
							unit_2['values'][G['DIR']] = dir__2
							unit_2['values'][G['ID']] = line_2[6]
							unit_2['flags'][9] = True
							unit_2['strings'][G['U_LEVELFILE']] = levelfile
							unit_2['strings'][G['U_LEVELNAME']] = levelname
							unit_2['flags'][G['MAPLEVEL']] = maplevel
							unit_2['values'][G['VISUALLEVEL']] = vislevel
							unit_2['values'][G['VISUALSTYLE']] = visstyle
							unit_2['values'][G['COMPLETED']] = complete
							unit_2['strings'][G['COLOUR']] = colour
							unit_2['strings'][G['CLEARCOLOUR']] = clearcolour
							unit_2['strings'][G['UNITSIGNTEXT']] = (_t4 if L_t(_t4 := signtext) else '')
							if (unit_2['className'] == 'level'):
								G['MF_setcolourfromstring'](unitid_2, colour)
							G['addunit'](unitid_2, True)
							G['addunitmap'](unitid_2, x_2, y_2, unit_2['strings'][G['UNITNAME']])
							G['dynamic'](unitid_2)
							unit_2['followed'] = followed
							unit_2['back_init'] = back_init
							unit_2['originalname'] = ogname
							unit_2['holder'] = holder
							if (unit_2['strings'][G['UNITTYPE']] == 'text'):
								G['updatecode'] = 1
							if (G['spritedata']['values'][G['VISION']] == 1):
								unit_2['x'] = (-24)
								unit_2['y'] = (-24)
							undowordunits_2 = currentundo_2['wordunits']
							undowordrelatedunits_2 = currentundo_2['wordrelatedunits']
							if (L_len(undowordunits_2) > 0):
								for a_3, b_3 in L_ipairs(undowordunits_2):
									if (b_3 == line_2[6]):
										G['updatecode'] = 1
							if (L_len(undowordrelatedunits_2) > 0):
								for a_4, b_4 in L_ipairs(undowordrelatedunits_2):
									if (b_4 == line_2[6]):
										G['updatecode'] = 1
						else:
							G['particles']('hot', line_2[3], line_2[4], 1, L_T([1, 1]))
					elif (style == 'create'):
						uid_4 = line_2[3]
						baseid = line_2[4]
						source = line_2[5]
						if (G['paradox'][uid_4] is None):
							unitid_3 = G['getunitid'](line_2[3])
							unit_3 = G['mmf']['newObject'](unitid_3)
							unitname_2 = unit_3['strings'][G['UNITNAME']]
							x_3, y_3 = unit_3['values'][G['XPOS']], unit_3['values'][G['YPOS']]
							unittype = unit_3['strings'][G['UNITTYPE']]
							unit_3 = L_T()
							G['delunit'](unitid_3)
							G['MF_remove'](unitid_3)
							G['dynamicat'](x_3, y_3)
							if (unittype == 'text'):
								G['updatecode'] = 1
							undowordunits_3 = currentundo_2['wordunits']
							undowordrelatedunits_3 = currentundo_2['wordrelatedunits']
							if (L_len(undowordunits_3) > 0):
								for a_5, b_5 in L_ipairs(undowordunits_3):
									if (b_5 == line_2[3]):
										G['updatecode'] = 1
							if (L_len(undowordrelatedunits_3) > 0):
								for a_6, b_6 in L_ipairs(undowordrelatedunits_3):
									if (b_6 == line_2[3]):
										G['updatecode'] = 1
					elif (style == 'backset'):
						uid_5 = line_2[3]
						if (G['paradox'][uid_5] is None):
							unitid_4 = G['getunitid'](line_2[3])
							unit_4 = G['mmf']['newObject'](unitid_4)
							unit_4['back_init'] = line_2[4]
					elif (style == 'done'):
						unitid_5 = line_2[7]
						unit_5 = G['mmf']['newObject'](unitid_5)
						unit_5['values'][G['FLOAT']] = line_2[8]
						unit_5['angle'] = 0
						unit_5['values'][G['POSITIONING']] = 0
						unit_5['values'][G['A']] = 0
						unit_5['values'][G['VISUALLEVEL']] = 0
						unit_5['flags'][G['DEAD']] = False
						G['addunit'](unitid_5, True)
						unit_5['originalname'] = line_2[9]
						if (unit_5['values'][G['TILING']] == 1):
							G['dynamic'](unitid_5)
					elif (style == 'float'):
						uid_6 = line_2[3]
						if (G['paradox'][uid_6] is None):
							unitid_6 = G['getunitid'](line_2[3])
							if ((unitid_6 is not None) and (unitid_6 != 0)):
								unit_6 = G['mmf']['newObject'](unitid_6)
								unit_6['values'][G['FLOAT']] = L_tonumber(line_2[4])
					elif (style == 'levelupdate'):
						G['MF_setroomoffset'](line_2[2], line_2[3])
						G['mapdir'] = line_2[6]
					elif (style == 'maprotation'):
						G['maprotation'] = line_2[2]
						G['MF_levelrotation'](G['maprotation'])
					elif (style == 'mapdir'):
						G['mapdir'] = line_2[2]
					elif (style == 'mapcursor'):
						G['mapcursor_set'](line_2[3], line_2[4], line_2[5], line_2[10])
						undowordunits_4 = currentundo_2['wordunits']
						undowordrelatedunits_4 = currentundo_2['wordrelatedunits']
						unitid_7 = G['getunitid'](line_2[10])
						if ((unitid_7 is not None) and (unitid_7 != 0)):
							unit_7 = G['mmf']['newObject'](unitid_7)
							if (unit_7['strings'][G['UNITTYPE']] == 'text'):
								G['updatecode'] = 1
						if (L_len(undowordunits_4) > 0):
							for a_7, b_7 in L_pairs(undowordunits_4):
								if (b_7 == line_2[10]):
									G['updatecode'] = 1
						if (L_len(undowordrelatedunits_4) > 0):
							for a_8, b_8 in L_pairs(undowordrelatedunits_4):
								if (b_8 == line_2[10]):
									G['updatecode'] = 1
					elif (style == 'colour'):
						unitid_8 = G['getunitid'](line_2[2])
						G['MF_setcolour'](unitid_8, line_2[3], line_2[4])
						unit_8 = G['mmf']['newObject'](unitid_8)
						unit_8['values'][G['A']] = line_2[5]
					elif (style == 'broken'):
						unitid_9 = G['getunitid'](line_2[3])
						unit_9 = G['mmf']['newObject'](unitid_9)
						unit_9['broken'] = (1 - line_2[2])
					elif (style == 'bonus'):
						style_2 = (1 - line_2[2])
						G['MF_bonus'](style_2)
					elif (style == 'followed'):
						unitid_10 = G['getunitid'](line_2[2])
						unit_10 = G['mmf']['newObject'](unitid_10)
						unit_10['followed'] = line_2[3]
					elif (style == 'startvision'):
						target = line_2[2]
						if ((line_2[2] != 0) and (line_2[2] != 0.5)):
							target = G['getunitid'](line_2[2])
						G['visionmode'](0, target, True)
					elif (style == 'stopvision'):
						target_2 = line_2[2]
						if ((line_2[2] != 0) and (line_2[2] != 0.5)):
							target_2 = G['getunitid'](line_2[2])
						G['visionmode'](1, target_2, True, L_T([line_2[3], line_2[4], line_2[5]]))
					elif (style == 'visiontarget'):
						unitid_11 = G['getunitid'](line_2[2])
						if ((G['spritedata']['values'][G['VISION']] == 1) and (unitid_11 != 0)):
							unit_11 = G['mmf']['newObject'](unitid_11)
							G['MF_updatevision'](unit_11['values'][G['DIR']])
							G['MF_updatevisionpos'](unit_11['values'][G['XPOS']], unit_11['values'][G['YPOS']])
							G['spritedata']['values'][G['CAMTARGET']] = line_2[2]
					elif (style == 'holder'):
						unitid_12 = G['getunitid'](line_2[2])
						unit_12 = G['mmf']['newObject'](unitid_12)
						unit_12['holder'] = line_2[3]
					else:
						G['undocall'](style, line_2)
			nextundo = G['undobuffer'][1]
			nextundo['wordunits'] = L_T()
			nextundo['wordrelatedunits'] = L_T()
			nextundo['visiontargets'] = L_T()
			nextundo['fixedseed'] = G['Fixedseed']
			for i_6, v_5 in L_ipairs(currentundo_2['wordunits']):
				L_insert(nextundo['wordunits'], v_5)
			for i_7, v_6 in L_ipairs(currentundo_2['wordrelatedunits']):
				L_insert(nextundo['wordrelatedunits'], v_6)
			if (L_len(currentundo_2['visiontargets']) > 0):
				G['visiontargets'] = L_T()
				for i_8, v_7 in L_ipairs(currentundo_2['visiontargets']):
					L_insert(nextundo['visiontargets'], v_7)
					fix = G['MF_getfixed'](v_7)
					if (fix is not None):
						L_insert(G['visiontargets'], fix)
			L_remove(G['undobuffer'], 2)
		G['do_mod_hook']('undoed_after')
		G['logevents'] = True
		return result
	G['undo'] = f_undo
	def f_undostate(state=None, *_):  # L469
		if (state is not None):
			G['doundo'] = state
	G['undostate'] = f_undostate
