"""Generated from mapcursor.lua by tools/lua2py.py. Do not edit."""
from babasim.luart import *  # noqa: F403


def load(G):
	def f_mapcursor_load(*_):  # L1
		ix = (_t1 if L_t(_t1 := L_tonumber(G['MF_read']('level', 'general', 'selectorX'))) else 0)
		iy = (_t2 if L_t(_t2 := L_tonumber(G['MF_read']('level', 'general', 'selectorY'))) else 0)
		G['generaldata4']['values'][G['MAINCURSOR']] = 0
		if ((ix > 0) and (iy > 0)):
			tileid = (ix + (iy * G['roomsizex']))
			createnew = True
			if ((G['unitmap'][tileid] is not None) and (L_len(G['unitmap'][tileid]) > 0)):
				for a, b in L_ipairs(G['unitmap'][tileid]):
					lunit = G['mmf']['newObject'](b)
					if (lunit['strings'][G['UNITNAME']] == 'cursor'):
						createnew = False
						G['generaldata4']['values'][G['MAINCURSOR']] = b
			if ((createnew is not None and createnew is not False) and (G['unitreference']['cursor'] is not None)):
				maincursorid = L_first(G['create']('cursor', ix, iy, 0, ix, iy, 0, True))
				G['generaldata4']['values'][G['MAINCURSOR']] = maincursorid
		cursors = G['getunitswitheffect']('select', True, None, None, True)
		for i, unit in L_ipairs(cursors):
			unit['values'][G['POSITIONING']] = 7
			G['editor']['values'][G['NAMEFLAG']] = 0
			something = False
			if (G['generaldata4']['values'][G['MAINCURSOR']] == 0):
				G['generaldata4']['values'][G['MAINCURSOR']] = unit['fixed']
			if (G['generaldata4']['values'][G['MAINCURSOR']] == unit['fixed']):
				parentlevel = G['MF_findlevelunit'](G['generaldata']['strings'][G['PARENT']])
				parent_ini = G['MF_read']('save', G['generaldata']['strings'][G['WORLD']], 'Previous')
				previous = G['generaldata2']['strings'][G['PREVIOUSLEVEL']]
				parentlevel_ini = L_T()
				previouslevel = L_T()
				if (parent_ini is not None):
					parentlevel_ini = G['MF_findlevelunit'](parent_ini)
				if (L_len(parentlevel) > 0):
					for a_2, b_2 in L_ipairs(parentlevel):
						lunit_2 = G['mmf']['newObject'](b_2)
						if ((lunit_2['values'][G['COMPLETED']] >= 2) and (lunit_2['flags'][G['DEAD']] is False)):
							unit['values'][G['XPOS']] = lunit_2['values'][G['XPOS']]
							unit['values'][G['YPOS']] = lunit_2['values'][G['YPOS']]
							unit['values'][G['CURSOR_ONLEVEL']] = b_2
							unit['x'] = lunit_2['x']
							unit['y'] = lunit_2['y']
							something = True
							break
				if (L_len(parentlevel_ini) > 0):
					for a_3, b_3 in L_ipairs(parentlevel_ini):
						lunit_3 = G['mmf']['newObject'](b_3)
						if ((lunit_3['values'][G['COMPLETED']] >= 2) and (lunit_3['flags'][G['DEAD']] is False)):
							unit['values'][G['XPOS']] = lunit_3['values'][G['XPOS']]
							unit['values'][G['YPOS']] = lunit_3['values'][G['YPOS']]
							unit['values'][G['CURSOR_ONLEVEL']] = b_3
							unit['x'] = lunit_3['x']
							unit['y'] = lunit_3['y']
							something = True
							break
				if (((G['generaldata']['strings'][G['WORLD']] != G['generaldata']['strings'][G['BASEWORLD']]) and (something is False)) and (L_len(previous) > 0)):
					previouslevel = G['MF_findlevelunit'](previous)
					for a_4, b_4 in L_ipairs(previouslevel):
						lunit_4 = G['mmf']['newObject'](b_4)
						if ((lunit_4['values'][G['COMPLETED']] >= 2) and (lunit_4['flags'][G['DEAD']] is False)):
							unit['values'][G['XPOS']] = lunit_4['values'][G['XPOS']]
							unit['values'][G['YPOS']] = lunit_4['values'][G['YPOS']]
							unit['values'][G['CURSOR_ONLEVEL']] = b_4
							unit['x'] = lunit_4['x']
							unit['y'] = lunit_4['y']
							something = True
							break
	G['mapcursor_load'] = f_mapcursor_load
	def f_mapcursor_idle(*_):  # L112
		cursors_2 = G['getunitswitheffect']('select', True)
		bestoption = 0
		maincursorfound = False
		for i_2, unit_2 in L_ipairs(cursors_2):
			if (unit_2['fixed'] == G['generaldata4']['values'][G['MAINCURSOR']]):
				maincursorfound = True
			elif (bestoption == 0):
				bestoption = unit_2['fixed']
			if (((unit_2['values'][G['CURSOR_ONLEVEL']] != 0) and (unit_2['values'][G['CURSOR_ONLEVEL']] != (-1))) and L_t(G['MF_findunit_fixed'](unit_2['values'][G['CURSOR_ONLEVEL']]))):
				lunit_5 = G['mmf']['newObject'](unit_2['values'][G['CURSOR_ONLEVEL']])
				unit_2['values'][G['XPOS']] = lunit_5['values'][G['XPOS']]
				unit_2['values'][G['YPOS']] = lunit_5['values'][G['YPOS']]
			elif (unit_2['values'][G['CURSOR_ONLEVEL']] == (-1)):
				G['editor']['values'][G['NAMEFLAG']] = 0
				targets = G['findallhere'](unit_2['values'][G['XPOS']], unit_2['values'][G['YPOS']], unit_2['fixed'], True)
				limiter = False
				for a_5, b_5 in L_ipairs(targets):
					lunit_6 = G['mmf']['newObject'](b_5)
					if ((lunit_6['values'][G['COMPLETED']] > 1) and L_t(lunit_6['visible'])):
						if ((L_strlen(lunit_6['strings'][G['U_LEVELFILE']]) == 0) and (limiter is False)):
							unit_2['values'][G['CURSOR_ONLEVEL']] = b_5
						elif (L_strlen(lunit_6['strings'][G['U_LEVELFILE']]) > 0):
							unit_2['values'][G['CURSOR_ONLEVEL']] = b_5
							limiter = True
			else:
				unit_2['values'][G['CURSOR_ONLEVEL']] = 0
				if (G['generaldata4']['values'][G['DISPLAYLEVEL']] == unit_2['fixed']):
					G['generaldata4']['values'][G['DISPLAYLEVEL']] = 0
					G['editor']['values'][G['NAMEFLAG']] = 0
			if (G['generaldata']['values'][G['MODE']] == 0):
				if ((G['generaldata']['values'][G['WINTIMER']] == 0) and ((G['generaldata2']['values'][G['UNLOCK']] < 2) or ((((G['generaldata2']['values'][G['MAPCLEAR']] == 0) and (G['matches'] is None)) and (G['generaldata2']['values'][G['UNLOCK']] >= 2)) and (G['generaldata2']['values'][G['UNLOCK']] <= 3)))):
					unit_2['visible'] = True
				else:
					unit_2['visible'] = False
		if ((G['generaldata']['strings'][G['WORLD']] != G['generaldata']['strings'][G['BASEWORLD']]) and (maincursorfound is False)):
			G['generaldata4']['values'][G['MAINCURSOR']] = bestoption
	G['mapcursor_idle'] = f_mapcursor_idle
	def f_mapcursor_move(ox_=None, oy_=None, mdir=None, *_):  # L171
		dir_ = (_t1 if L_t(_t1 := mdir) else 4)
		cursors_3 = G['getunitswitheffect']('select', True)
		for i_3, unit_3 in L_ipairs(cursors_3):
			x_, y_, dir__2 = unit_3['values'][G['XPOS']], unit_3['values'][G['YPOS']], unit_3['values'][G['DIR']]
			currlevel = unit_3['values'][G['CURSOR_ONLEVEL']]
			ox, oy = ox_, oy_
			if (G['featureindex']['reverse'] is not None):
				dir_, ox, oy = L_adjust((*G['reversecheck'](unit_3['fixed'], dir_, x_, y_, ox_, oy_),), 3)
			unitname = G['getname'](unit_3)
			still = G['cantmove'](unitname, unit_3['fixed'], dir_)
			x = (x_ + ox)
			y = (y_ + oy)
			unit_3['flags'][G['CURSOR_LIMITER']] = False
			levelfound = False
			moved = False
			if (still is False):
				targets_2 = G['findallhere'](x, y, unit_3['fixed'], True)
				for a_6, b_6 in L_ipairs(targets_2):
					lunit_7 = G['mmf']['newObject'](b_6)
					if ((L_t(lunit_7['visible']) and (lunit_7['flags'][G['DEAD']] is False)) and (lunit_7['values'][G['COMPLETED']] > 1)):
						G['editor']['values'][G['NAMEFLAG']] = 0
						moved = True
						if ((unit_3['flags'][G['CURSOR_LIMITER']] is False) and (L_strlen(lunit_7['strings'][G['U_LEVELFILE']]) == 0)):
							unit_3['values'][G['CURSOR_ONLEVEL']] = b_6
							break
						elif (L_strlen(lunit_7['strings'][G['U_LEVELFILE']]) > 0):
							unit_3['values'][G['CURSOR_ONLEVEL']] = b_6
							unit_3['flags'][G['CURSOR_LIMITER']] = True
							levelfound = True
							break
			if (moved is not None and moved is not False):
				unit_3['values'][G['XPOS']] = x
				unit_3['values'][G['YPOS']] = y
				unit_3['values'][G['DIR']] = dir_
				unit_3['values'][G['POSITIONING']] = 0
				G['addundo'](L_T(['mapcursor', currlevel, x_, y_, dir__2, unit_3['values'][G['CURSOR_ONLEVEL']], x, y, dir_, unit_3['values'][G['ID']]]))
				G['updateundo'] = True
				G['checkwordchanges'](unit_3['fixed'], unit_3['strings'][G['UNITNAME']])
				if (levelfound is False):
					G['editor']['values'][G['NAMEFLAG']] = 0
					unit_3['values'][G['CURSOR_ONLEVEL']] = 0
				if (unit_3['strings'][G['UNITTYPE']] == 'text'):
					G['updatecode'] = 1
				if (((G['generaldata5']['values'][G['AUTO_ON']] == 1) and (G['generaldata2']['strings'][G['TURNSOUND']] == '')) and (dir_ == 4)):
					G['generaldata2']['strings'][G['TURNSOUND']] = 'silent'
	G['mapcursor_move'] = f_mapcursor_move
	def f_mapcursor_enter(varsunitid=None, *_):  # L244
		cursors_4 = G['getunitswitheffect']('select', True)
		varsunit = G['mmf']['newObject'](varsunitid)
		entering = L_T()
		for i_4, unit_4 in L_ipairs(cursors_4):
			targetfound = G['MF_findunit_fixed'](unit_4['values'][G['CURSOR_ONLEVEL']])
			if (targetfound is not None and targetfound is not False):
				allhere = G['findallhere'](unit_4['values'][G['XPOS']], unit_4['values'][G['YPOS']], unit_4['fixed'])
				for a_7, b_7 in L_ipairs(allhere):
					lunit_8 = G['mmf']['newObject'](b_7)
					if ((((L_strlen(lunit_8['strings'][G['U_LEVELFILE']]) > 0) and (L_strlen(lunit_8['strings'][G['U_LEVELNAME']]) > 0)) and (G['generaldata']['values'][G['IGNORE']] == 0)) and (lunit_8['values'][G['COMPLETED']] > 1)):
						valid = True
						for c, d in L_ipairs(cursors_4):
							if (d['fixed'] == b_7):
								valid = False
								break
						if (valid is not None and valid is not False):
							L_insert(entering, L_T([b_7, lunit_8['strings'][G['U_LEVELNAME']], lunit_8['strings'][G['U_LEVELFILE']]]))
		if (L_len(entering) > 0):
			G['dolog']('end', 'event')
		if (L_len(entering) == 1):
			G['generaldata2']['values'][G['UNLOCK']] = 0
			G['generaldata2']['values'][G['UNLOCKTIMER']] = 0
			varsunit['values'][1] = entering[1][1]
			G['MF_loop']('enterlevel', 1)
		elif (L_len(entering) > 0):
			G['MF_menuselector_hack'](1)
			G['submenu']('enterlevel_multiple', entering)
			L_noop('Trying to enter multiple levels!')
	G['mapcursor_enter'] = f_mapcursor_enter
	def f_mapcursor_set(x_2=None, y_2=None, dir__3=None, id_=None, *_):  # L292
		unitid = G['getunitid'](id_)
		unit_5 = G['mmf']['newObject'](unitid)
		unit_5['values'][G['XPOS']] = x_2
		unit_5['values'][G['YPOS']] = y_2
		unit_5['values'][G['DIR']] = dir__3
		unit_5['values'][G['POSITIONING']] = 0
		unit_5['values'][G['CURSOR_ONLEVEL']] = (-1)
	G['mapcursor_set'] = f_mapcursor_set
	def f_mapcursor_hardset(lunitid=None, *_):  # L306
		lunit_9 = G['mmf']['newObject'](lunitid)
		cursors_5 = G['getunitswitheffect']('select', True, None, None, True)
		for i_5, unit_6 in L_ipairs(cursors_5):
			unit_6['values'][G['XPOS']] = lunit_9['values'][G['XPOS']]
			unit_6['values'][G['YPOS']] = lunit_9['values'][G['YPOS']]
			unit_6['values'][G['CURSOR_ONLEVEL']] = lunitid
			unit_6['x'] = lunit_9['x']
			unit_6['y'] = lunit_9['y']
			unit_6['values'][G['POSITIONING']] = 7
	G['mapcursor_hardset'] = f_mapcursor_hardset
	def f_mapcursor_levelstart(*_):  # L323
		cursors_6 = G['getunitswitheffect']('select', True, None, None, True)
		for i_6, unit_7 in L_ipairs(cursors_6):
			x_3, y_3 = unit_7['values'][G['XPOS']], unit_7['values'][G['YPOS']]
			targets_3 = G['findallhere'](x_3, y_3, unit_7['fixed'], True)
			for a_8, b_8 in L_ipairs(targets_3):
				lunit_10 = G['mmf']['newObject'](b_8)
				if (lunit_10['values'][G['COMPLETED']] > 1):
					unit_7['values'][G['CURSOR_ONLEVEL']] = b_8
					break
	G['mapcursor_levelstart'] = f_mapcursor_levelstart
	def f_mapcursor_displayname(*_):  # L342
		cursors_7 = G['getunitswitheffect']('select', True)
		for i_7, unit_8 in L_ipairs(cursors_7):
			if ((((unit_8['values'][G['CURSOR_ONLEVEL']] != 0) and (unit_8['values'][G['CURSOR_ONLEVEL']] != (-1))) and L_t(G['MF_findunit_fixed'](unit_8['values'][G['CURSOR_ONLEVEL']]))) and L_t(unit_8['visible'])):
				lunit_11 = G['mmf']['newObject'](unit_8['values'][G['CURSOR_ONLEVEL']])
				valid_2 = True
				for c_2, d_2 in L_ipairs(cursors_7):
					if (d_2['fixed'] == G['b']):
						valid_2 = False
						break
				if (((valid_2 is not None and valid_2 is not False) and (L_strlen(lunit_11['strings'][G['U_LEVELNAME']]) > 0)) and (lunit_11['values'][G['COMPLETED']] > 1)):
					G['editor']['values'][G['NAMEFLAG']] = 1
					G['generaldata4']['values'][G['DISPLAYLEVEL']] = unit_8['fixed']
					G['displaylevelname'](lunit_11['strings'][G['U_LEVELNAME']], lunit_11['strings'][G['U_LEVELFILE']], 2)
	G['mapcursor_displayname'] = f_mapcursor_displayname
	def f_idleblockcheck(*_):  # L368
		cursors_8 = G['getunitswitheffect']('select', True)
		for i_8, unit_9 in L_ipairs(cursors_8):
			if ((unit_9['values'][G['CURSOR_ONLEVEL']] != 0) and (unit_9['values'][G['CURSOR_ONLEVEL']] != (-1))):
				lunit_12 = G['mmf']['newObject'](unit_9['values'][G['CURSOR_ONLEVEL']])
				if (L_strlen(lunit_12['strings'][G['U_LEVELFILE']]) > 0):
					return True
		return False
	G['idleblockcheck'] = f_idleblockcheck
	def f_cursorcheck(*_):  # L384
		result = 0
		if (G['featureindex']['select'] is not None):
			cursors_9 = G['getunitswitheffect']('select', True)
			if (L_len(cursors_9) > 0):
				result = 1
		return result
	G['cursorcheck'] = f_cursorcheck
	def f_mapcursor_tofront(*_):  # L398
		if (G['spritedata']['values'][G['VISION']] == 0):
			cursors_10 = G['getunitswitheffect']('select', True)
			for i_9, unit_10 in L_ipairs(cursors_10):
				if (unit_10['strings'][G['UNITTYPE']] != 'text'):
					unit_10['moveToFront']()
	G['mapcursor_tofront'] = f_mapcursor_tofront
	def f_hidecursor(*_):  # L410
		cursors_11 = G['getunitswitheffect']('select', True)
		for i_10, unit_11 in L_ipairs(cursors_11):
			unit_11['visible'] = False
	G['hidecursor'] = f_hidecursor
	def f_mapcursor_setonlevel(value=None, *_):  # L418
		cursors_12 = G['getunitswitheffect']('select', True, None, None, True)
		for i_11, unit_12 in L_ipairs(cursors_12):
			unit_12['values'][G['CURSOR_ONLEVEL']] = value
	G['mapcursor_setonlevel'] = f_mapcursor_setonlevel
