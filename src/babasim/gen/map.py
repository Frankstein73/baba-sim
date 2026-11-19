"""Generated from map.lua by tools/lua2py.py. Do not edit."""
from babasim.luart import *  # noqa: F403


def load(G):
	G['leveltree'] = L_T()
	G['leveltree_id'] = L_T()
	def f_sublevel(name=None, lnum=None, ltype=None, *_):  # L4
		G['MF_alert'](L_concat('sublevel ', name, ', ', L_tostring(lnum), ', ', L_tostring(ltype)))
		id_ = (L_len(G['leveltree']) + 1)
		parentid = L_len(G['leveltree'])
		oldnum = ''
		oldparent = (_t1 if L_t(_t1 := G['leveltree'][parentid]) else '')
		delafterthis = 0
		G['generaldata2']['strings'][G['PREVIOUSLEVEL']] = oldparent
		G['MF_store']('save', G['generaldata']['strings'][G['WORLD']], 'Previous', name)
		if (parentid > 0):
			treechanged = False
			removethis = L_T()
			for i, v in L_pairs(G['leveltree']):
				if (v == name):
					delafterthis = i
					id_ = i
					parentid = (i - 1)
					oldnum = G['leveltree_id'][i]
				if ((delafterthis > 0) and (i > delafterthis)):
					L_insert(removethis, i)
					treechanged = True
			for i_2, v_2 in L_ipairs(removethis):
				G['MF_alert'](L_concat('Removed ', L_tostring(v_2), ' from leveltree. (', L_tostring(G['leveltree'][v_2]), ', ', L_tostring(G['leveltree_id'][v_2])))
				G['leveltree'][v_2] = None
				G['leveltree_id'][v_2] = None
			if (treechanged is not None and treechanged is not False):
				G['MF_store']('save', G['generaldata']['strings'][G['WORLD']], 'Previous', oldparent)
		G['generaldata']['strings'][G['CURRLEVEL']] = name
		G['leveltree'][id_] = name
		if (oldnum == ''):
			if (lnum is not None):
				G['leveltree_id'][id_] = G['getlevelid'](lnum, ltype, name)
				G['latestleveldetails']['lnum'] = lnum
				G['latestleveldetails']['ltype'] = ltype
			else:
				G['leveltree_id'][id_] = 'dummy'
		else:
			G['leveltree_id'][id_] = oldnum
		if (oldparent is not None):
			G['generaldata']['strings'][G['PARENT']] = oldparent
		else:
			G['generaldata']['strings'][G['PARENT']] = ''
		G['generaldata']['strings'][G['LEVELNUMBER_NAME']] = G['getlevelnumber']()
	G['sublevel'] = f_sublevel
	def f_uplevel(*_):  # L81
		id__2 = L_len(G['leveltree'])
		parentid_2 = (L_len(G['leveltree']) - 1)
		oldlevel = G['generaldata']['strings'][G['CURRLEVEL']]
		G['generaldata2']['strings'][G['PREVIOUSLEVEL']] = oldlevel
		G['MF_store']('save', G['generaldata']['strings'][G['WORLD']], 'Previous', oldlevel)
		G['latestleveldetails'] = L_T([], {'lnum': (-1), 'ltype': (-1)})
		if (id__2 == 0):
			G['MF_alert']('Already at map root')
			if ((G['generaldata']['strings'][G['WORLD']] != G['generaldata']['strings'][G['BASEWORLD']]) and (G['editor']['values'][G['INEDITOR']] == 0)):
				G['MF_end_single']()
				G['MF_credits'](1)
		if (parentid_2 > 1):
			G['generaldata']['strings'][G['PARENT']] = G['leveltree'][(parentid_2 - 1)]
		else:
			G['generaldata']['strings'][G['PARENT']] = ''
		if (id__2 > 1):
			G['generaldata']['strings'][G['CURRLEVEL']] = G['leveltree'][parentid_2]
		else:
			G['generaldata']['strings'][G['CURRLEVEL']] = ''
		L_remove(G['leveltree'], id__2)
		L_remove(G['leveltree_id'], id__2)
		return oldlevel
	G['uplevel'] = f_uplevel
	def f_changelevel(newlevel=None, lnum_2=None, ltype_2=None, resetleveltree_=None, *_):  # L117
		id__3 = L_len(G['leveltree'])
		parentid_3 = (L_len(G['leveltree']) - 1)
		oldlevel_2 = G['generaldata']['strings'][G['CURRLEVEL']]
		resetleveltree = (_t1 if L_t(_t1 := resetleveltree_) else False)
		if (resetleveltree is not None and resetleveltree is not False):
			G['leveltree'] = L_T()
			G['leveltree_id'] = L_T()
			id__3 = 1
			parentid_3 = 0
		if (id__3 == 0):
			G['MF_alert']('Already at map root')
		if (id__3 > 0):
			G['leveltree'][id__3] = newlevel
			G['leveltree_id'][id__3] = G['getlevelid'](lnum_2, ltype_2, newlevel)
			G['latestleveldetails']['lnum'] = lnum_2
			G['latestleveldetails']['ltype'] = ltype_2
		G['generaldata']['strings'][G['CURRLEVEL']] = newlevel
		return oldlevel_2
	G['changelevel'] = f_changelevel
	def f_handlecustomparent(levelid=None, *_):  # L150
		id__4 = L_len(G['leveltree'])
		if (id__4 > 1):
			G['uplevel']()
		oldlevel_3 = G['changelevel'](levelid, 0, 0)
		return oldlevel_3
	G['handlecustomparent'] = f_handlecustomparent
	def f_collapseleveltree(*_):  # L162
		id__5 = L_len(G['leveltree'])
		clevel = G['leveltree'][id__5]
		clevelname = G['leveltree_id'][id__5]
		G['leveltree'] = L_T()
		G['leveltree_id'] = L_T()
		L_insert(G['leveltree'], clevel)
		L_insert(G['leveltree_id'], clevelname)
		G['generaldata']['strings'][G['CURRLEVEL']] = clevel
		G['generaldata']['strings'][G['PARENT']] = ''
		G['generaldata']['strings'][G['LEVELNUMBER_NAME']] = ''
	G['collapseleveltree'] = f_collapseleveltree
	def f_resetleveltree(*_):  # L181
		G['leveltree'] = L_T()
		G['leveltree_id'] = L_T()
		G['generaldata']['strings'][G['CURRLEVEL']] = ''
		G['generaldata']['strings'][G['PARENT']] = ''
		G['generaldata']['strings'][G['LEVELNUMBER_NAME']] = ''
	G['resetleveltree'] = f_resetleveltree
	def f_rebuildleveltree(tree=None, tree_id=None, *_):  # L190
		G['leveltree'] = L_T()
		G['leveltree_id'] = L_T()
		for i_3, v_3 in L_ipairs(tree):
			L_insert(G['leveltree'], v_3)
		for i_4, v_4 in L_ipairs(tree_id):
			L_insert(G['leveltree_id'], v_4)
		G['generaldata']['strings'][G['CURRLEVEL']] = G['leveltree'][L_len(G['leveltree'])]
		G['generaldata']['strings'][G['PARENT']] = ''
		if (L_len(G['leveltree']) > 1):
			G['generaldata']['strings'][G['PARENT']] = G['leveltree'][(L_len(G['leveltree']) - 1)]
		G['generaldata']['strings'][G['LEVELNUMBER_NAME']] = G['getlevelnumber']()
	G['rebuildleveltree'] = f_rebuildleveltree
	def f_refreshleveltree(*_):  # L212
		if (L_len(G['leveltree']) > 0):
			for i_5, v_5 in L_ipairs(G['leveltree']):
				text = (_t1 if L_t(_t1 := G['langtext'](v_5)) else 'not found!')
				lnum_3 = None
				ltype_3 = 0
				if ((G['latestleveldetails']['lnum'] is not None) and (G['latestleveldetails']['lnum'] >= 0)):
					lnum_3 = G['latestleveldetails']['lnum']
				if ((G['latestleveldetails']['ltype'] is not None) and (G['latestleveldetails']['ltype'] >= 0)):
					ltype_3 = G['latestleveldetails']['ltype']
				G['leveltree_id'][i_5] = G['getlevelid'](lnum_3, ltype_3, v_5)
				if (G['generaldata']['strings'][G['LEVELFILE']] == v_5):
					G['generaldata']['strings'][G['LEVELNAME']] = text
			G['generaldata']['strings'][G['LEVELNUMBER_NAME']] = G['getlevelnumber']()
	G['refreshleveltree'] = f_refreshleveltree
	def f_storeleveltree(tree_2=None, tree_id_2=None, *_):  # L239
		G['leveltree'] = L_T()
		G['leveltree_id'] = L_T()
		for i_6, v_6 in L_ipairs(tree_2):
			L_insert(G['leveltree'], v_6)
			G['MF_alert'](L_concat(L_tostring(L_len(tree_2)), ', ', L_tostring(L_len(tree_id_2)), ', ', L_tostring(tree_id_2[i_6])))
			L_insert(G['leveltree_id'], tree_id_2[i_6])
		current = G['leveltree'][L_len(G['leveltree'])]
		parent = ''
		if (L_len(G['leveltree']) > 1):
			parent = G['leveltree'][(L_len(G['leveltree']) - 1)]
		G['generaldata']['strings'][G['CURRLEVEL']] = current
		G['generaldata']['strings'][G['PARENT']] = parent
		levelsurrounds = (_t1 if L_t(_t1 := G['MF_read']('save', G['generaldata']['strings'][G['WORLD']], 'levelsurrounds')) else '')
		G['generaldata2']['strings'][G['LEVELSURROUNDS']] = levelsurrounds
	G['storeleveltree'] = f_storeleveltree
	def f_getlevelnumber(*_):  # L265
		result = ''
		nothing = False
		id__6 = G['leveltree_id'][L_len(G['leveltree_id'])]
		id2 = (_t1 if L_t(_t1 := G['leveltree_id'][(L_len(G['leveltree_id']) - 1)]) else '')
		if (id2 == '<empty>'):
			id2 = ''
		if (L_len(G['leveltree_id']) == 1):
			if ((id__6 == '???') or (id__6 == 'baba')):
				result = L_concat(result, id__6)
		elif (L_len(G['leveltree_id']) == 2):
			if ((id2 == '???') or (id2 == 'baba')):
				result = L_concat(result, id2, '-')
			result = L_concat(result, id__6)
		elif (L_strlen(id2) > 0):
			result = L_concat(result, id2, '-', id__6)
		else:
			result = L_concat(result, id__6)
		if (id__6 == '<empty>'):
			nothing = True
		if (L_strlen(result) > 0):
			result = L_concat(G['langtext']('level'), ' ', result)
		else:
			result = G['langtext']('level')
		if (nothing is not None and nothing is not False):
			result = ' '
		return result
	G['getlevelnumber'] = f_getlevelnumber
	def f_getlevelid(lnum_4=None, ltype_4=None, level=None, *_):  # L309
		result_2 = ''
		world = G['generaldata']['strings'][G['WORLD']]
		G['MF_setfile']('level', L_concat('Data/Worlds/', world, '/', level, '.ld'))
		customid = G['MF_read']('level', 'general', 'mapid')
		langcustomid = ''
		if (world == G['generaldata']['strings'][G['BASEWORLD']]):
			langcustomid = G['MF_read']('lang', 'texts', L_concat(level, '_mapid'))
		else:
			langcustomid = G['MF_read']('lang', 'texts', L_concat(world, '_', level, '_mapid'))
		if (L_strlen(langcustomid) > 0):
			customid = langcustomid
		else:
			G['MF_alert'](L_concat(world, '_', level, "_mapid doesn't exist"))
		if (L_strlen(customid) == 0):
			if (ltype_4 == 1):
				lookup = 'abcdefghijklmnopqrstuvwxyz'
				result_2 = L_sub(lookup, (lnum_4 + 1), (lnum_4 + 1))
			elif (ltype_4 == 2):
				result_2 = L_concat(G['langtext']('mapid_extra'), ' ', L_tostring((lnum_4 + 1)))
			else:
				result_2 = L_tostring((_t1 if L_t(_t1 := lnum_4) else ''))
		else:
			result_2 = customid
		G['MF_setfile']('level', L_concat('Data/Worlds/', G['generaldata']['strings'][G['WORLD']], '/', G['generaldata']['strings'][G['CURRLEVEL']], '.ld'))
		return result_2
	G['getlevelid'] = f_getlevelid
	def f_unlockeffect(dataid=None, *_):  # L348
		data = G['mmf']['newObject'](dataid)
		if (G['hiddenmap'] is None):
			cursors = G['getunitswitheffect']('select', None, None, None, True)
			cx, cy = 0, 0
			if (L_len(cursors) > 0):
				cursorunit = cursors[1]
				cx = cursorunit['values'][G['XPOS']]
				cy = cursorunit['values'][G['YPOS']]
			G['hiddenmap'] = L_T()
			G['hiddenmap']['unlocks'] = L_T()
			G['hiddenmap']['start'] = L_T([cx, cy])
		start = G['hiddenmap']['start']
		x = start[1]
		y = start[2]
		data['values'][G['UNLOCKTIMER']] = (data['values'][G['UNLOCKTIMER']] + 1)
		timer = data['values'][G['UNLOCKTIMER']]
		unlock = data['values'][G['UNLOCK']]
		if (unlock == 2):
			if (timer == 10):
				G['MF_playsound']('roll')
			if (((timer > 10) and (timer < 80)) and ((timer % 2) == 0)):
				G['particles']('unlock', x, y, 2, L_T([2, 4]))
			if (timer == 70):
				G['generaldata']['values'][G['SHAKE']] = 15
				if (data['values'][G['MAPCLEAR']] == 0):
					G['generaldata']['values'][G['IGNORE']] = 0
				G['particles']('smoke', x, y, 20, L_T([0, 3]))
				prizeid = G['MF_specialcreate']('Prize')
				prize = G['mmf']['newObject'](prizeid)
				prize['layer'] = 2
				prize['values'][G['ONLINE']] = 1
				prize['values'][G['XPOS']] = ((G['Xoffset'] + ((x * G['tilesize']) * G['spritedata']['values'][G['TILEMULT']])) + ((G['tilesize'] * 0.5) * G['spritedata']['values'][G['TILEMULT']]))
				prize['values'][G['YPOS']] = ((G['Yoffset'] + ((y * G['tilesize']) * G['spritedata']['values'][G['TILEMULT']])) + ((G['tilesize'] * 0.5) * G['spritedata']['values'][G['TILEMULT']]))
				prize['values'][G['YVEL']] = (-20)
				prize['scaleX'] = 0.1
				prize['scaleY'] = 0.1
				if (data['values'][G['MAPCLEAR']] == 1):
					G['MF_playsound']('clear')
				else:
					G['MF_playsound']('winnery_fast')
				G['MF_playsound']('pop3')
				G['MF_stopsound']('roll')
				if (data['values'][G['MAPCLEAR']] == 1):
					winid1 = G['MF_specialcreate']('Victorytext')
					winid2 = G['MF_specialcreate']('Victorytext_back')
					wintext1 = G['mmf']['newObject'](winid1)
					wintext2 = G['mmf']['newObject'](winid2)
					wintext2['layer'] = 2
					wintext1['layer'] = 2
					G['MF_setcolour'](winid1, 0, 3)
					G['MF_setcolour'](winid2, 1, 1)
					wintext1['x'] = (G['screenw'] * 0.5)
					wintext1['y'] = (G['screenh'] * 0.5)
					wintext1['direction'] = 1
					wintext2['x'] = (G['screenw'] * 0.5)
					wintext2['y'] = ((G['screenh'] * 0.5) + 4)
					wintext2['direction'] = 1
					if ((G['generaldata4']['values'][G['CUSTOMFONT']] == 0) and (G['generaldata']['strings'][G['LANG']] != 'en')):
						wintext1['visible'] = False
						wintext2['visible'] = False
						G['displaybigtext']('ingame_clear', L_T([0, 3, 1, 3]), True)
			if (timer == 110):
				hidden, hiddenmap_ = L_adjust((*G['checkhidden'](x, y),), 2)
				if (hidden is not None and hidden is not False):
					G['hiddenmap'] = hiddenmap_
					G['hiddenmap']['unlocks'] = L_T()
					G['hiddenmap']['start'] = L_T([x, y])
					data['values'][G['UNLOCK']] = 3
					data['values'][G['UNLOCKTIMER']] = (-25)
					return None
			upoint = 130
			ox, oy = 0, 0
			opensound = L_concat('whoosh_alt', L_tostring(G['math']['random'](1, 5)))
			if (G['matches'] is not None):
				opensound = L_concat('intro_flower_', L_tostring(G['math']['random'](1, 7)))
			if (timer == upoint):
				ox = 0
				oy = (-1)
				unlockables = G['findallhere']((x + ox), (y + oy))
				found = False
				if (L_len(unlockables) > 0):
					for i_7, unitid in L_ipairs(unlockables):
						unit = G['mmf']['newObject'](unitid)
						pgate, preq = 0, 0
						pathid = G['MF_findpath_id'](unitid)
						if (pathid is not None):
							path = G['mmf']['newObject'](pathid)
							pgate = path['values'][G['PATH_GATE']]
							preq = path['values'][G['PATH_REQUIREMENT']]
						if (((unit['values'][G['COMPLETED']] == 1) and ((pgate == 0) or (preq <= 0))) and (unit['flags'][G['LEVEL_JUSTCONVERTED']] is False)):
							unit['values'][G['COMPLETED']] = 2
							found = True
				if (found is not None and found is not False):
					G['particles']('hot', (x + ox), (y + oy), 10, L_T([0, 3]))
					G['MF_playsound'](opensound)
				else:
					timer = (timer + 15)
			if (timer == (upoint + 15)):
				ox = (-1)
				oy = 0
				unlockables_2 = G['findallhere']((x + ox), (y + oy))
				found_2 = False
				if (L_len(unlockables_2) > 0):
					for i_8, unitid_2 in L_ipairs(unlockables_2):
						unit_2 = G['mmf']['newObject'](unitid_2)
						pgate_2, preq_2 = 0, 0
						pathid_2 = G['MF_findpath_id'](unitid_2)
						if (pathid_2 is not None):
							path_2 = G['mmf']['newObject'](pathid_2)
							pgate_2 = path_2['values'][G['PATH_GATE']]
							preq_2 = path_2['values'][G['PATH_REQUIREMENT']]
						if (((unit_2['values'][G['COMPLETED']] == 1) and ((pgate_2 == 0) or (preq_2 <= 0))) and (unit_2['flags'][G['LEVEL_JUSTCONVERTED']] is False)):
							unit_2['values'][G['COMPLETED']] = 2
							found_2 = True
				if (found_2 is not None and found_2 is not False):
					G['particles']('hot', (x + ox), (y + oy), 10, L_T([0, 3]))
					G['MF_playsound'](opensound)
				else:
					timer = (timer + 15)
			if (timer == (upoint + 30)):
				ox = 0
				oy = 1
				unlockables_3 = G['findallhere']((x + ox), (y + oy))
				found_3 = False
				if (L_len(unlockables_3) > 0):
					for i_9, unitid_3 in L_ipairs(unlockables_3):
						unit_3 = G['mmf']['newObject'](unitid_3)
						pgate_3, preq_3 = 0, 0
						pathid_3 = G['MF_findpath_id'](unitid_3)
						if (pathid_3 is not None):
							path_3 = G['mmf']['newObject'](pathid_3)
							pgate_3 = path_3['values'][G['PATH_GATE']]
							preq_3 = path_3['values'][G['PATH_REQUIREMENT']]
						if (((unit_3['values'][G['COMPLETED']] == 1) and ((pgate_3 == 0) or (preq_3 <= 0))) and (unit_3['flags'][G['LEVEL_JUSTCONVERTED']] is False)):
							unit_3['values'][G['COMPLETED']] = 2
							found_3 = True
				if (found_3 is not None and found_3 is not False):
					G['particles']('hot', (x + ox), (y + oy), 10, L_T([0, 3]))
					G['MF_playsound'](opensound)
				else:
					timer = (timer + 15)
			if (timer == (upoint + 45)):
				ox = 1
				oy = 0
				unlockables_4 = G['findallhere']((x + ox), (y + oy))
				found_4 = False
				if (L_len(unlockables_4) > 0):
					for i_10, unitid_4 in L_ipairs(unlockables_4):
						unit_4 = G['mmf']['newObject'](unitid_4)
						pgate_4, preq_4 = 0, 0
						pathid_4 = G['MF_findpath_id'](unitid_4)
						if (pathid_4 is not None):
							path_4 = G['mmf']['newObject'](pathid_4)
							pgate_4 = path_4['values'][G['PATH_GATE']]
							preq_4 = path_4['values'][G['PATH_REQUIREMENT']]
						if (((unit_4['values'][G['COMPLETED']] == 1) and ((pgate_4 == 0) or (preq_4 <= 0))) and (unit_4['flags'][G['LEVEL_JUSTCONVERTED']] is False)):
							unit_4['values'][G['COMPLETED']] = 2
							found_4 = True
				if (found_4 is not None and found_4 is not False):
					G['particles']('hot', (x + ox), (y + oy), 10, L_T([0, 3]))
					G['MF_playsound'](opensound)
			if (timer == (upoint + 50)):
				if (G['matches'] is None):
					if (data['values'][G['MAPCLEAR']] == 0):
						data['values'][G['UNLOCK']] = 0
						data['values'][G['UNLOCKTIMER']] = 0
						G['generaldata']['values'][G['IGNORE']] = 0
						G['hiddenmap'] = None
					else:
						data['values'][G['MAPCLEAR']] = 0
						data['values'][G['UNLOCK']] = 4
						data['values'][G['UNLOCKTIMER']] = (-30)
				else:
					data['values'][G['UNLOCK']] = 5
					data['values'][G['UNLOCKTIMER']] = 0
		elif (unlock == 3):
			docheck = (timer % 10)
			if ((docheck == 0) and (timer > 0)):
				newstuff = L_T()
				unlocks = L_T()
				currtype = 0
				if (L_len(G['hiddenmap']) > 0):
					for i_11, v_7 in L_ipairs(G['hiddenmap']):
						unit_5 = G['mmf']['newObject'](v_7)
						unit_5['values'][G['COMPLETED']] = L_max(unit_5['values'][G['COMPLETED']], 1)
						ux, uy = unit_5['values'][G['XPOS']], unit_5['values'][G['YPOS']]
						if (unit_5['strings'][G['UNITNAME']] != 'path'):
							currtype = 0
						else:
							L_insert(unlocks, L_T([ux, uy]))
							currtype = 1
						G['MF_playsound'](L_concat('whoosh_quiet', L_tostring(G['math']['random'](1, 5))))
						G['particles']('glow', ux, uy, 5, L_T([1, 2]))
						th, things = L_adjust((*G['checkhidden'](ux, uy),), 2)
						if (th is not None and th is not False):
							for c, d in L_ipairs(things):
								dunit = G['mmf']['newObject'](d)
								addthis = False
								if (((dunit['strings'][G['UNITNAME']] != 'path') and (currtype == 0)) or ((ux == x) and (uy == y))):
									addthis = True
								elif ((dunit['strings'][G['UNITNAME']] == 'path') and (currtype == 1)):
									addthis = True
									if ((unit_5['strings'][G['UNITNAME']] == 'path') and (unit_5['values'][G['PATH_GATE']] > 0)):
										addthis = False
								if (addthis is not None and addthis is not False):
									L_insert(newstuff, d)
				if (L_len(G['hiddenmap']['unlocks']) > 0):
					for i_12, v_8 in L_ipairs(G['hiddenmap']['unlocks']):
						ux_2, uy_2 = v_8[1], v_8[2]
						G['unlocklevels'](ux_2, uy_2, True)
				G['hiddenmap'] = L_T()
				G['hiddenmap']['unlocks'] = L_T()
				G['hiddenmap']['start'] = L_T([x, y])
				if (L_len(newstuff) > 0):
					for i_13, v_9 in L_ipairs(newstuff):
						L_insert(G['hiddenmap'], v_9)
				if (L_len(unlocks) > 0):
					for i_14, v_10 in L_ipairs(unlocks):
						L_insert(G['hiddenmap']['unlocks'], v_10)
				if ((L_len(newstuff) == 0) and (L_len(unlocks) == 0)):
					G['hiddenmap'] = L_T()
					G['hiddenmap']['unlocks'] = L_T()
					G['hiddenmap']['start'] = L_T([x, y])
					data['values'][G['UNLOCK']] = 2
					data['values'][G['UNLOCKTIMER']] = 110
	G['unlockeffect'] = f_unlockeffect
	def f_unlocklevels(x_2=None, y_2=None, visuals_=None, reveal_=None, *_):  # L699
		ox_2, oy_2 = 0, 0
		visuals = False
		reveal = False
		if (visuals_ is not None):
			visuals = visuals_
		if (reveal_ is not None):
			reveal = reveal_
		for a in L_range(1, 4):
			ndrs = G['ndirs'][a]
			ox_2 = ndrs[1]
			oy_2 = ndrs[2]
			levels = G['findallhere']((x_2 + ox_2), (y_2 + oy_2))
			if (L_len(levels) > 0):
				for i_15, v_11 in L_ipairs(levels):
					unit_6 = G['mmf']['newObject'](v_11)
					if ((unit_6['values'][G['COMPLETED']] < 2) and (L_strlen(unit_6['strings'][G['LEVELFILE']]) > 0)):
						if (visuals is False):
							if (unit_6['strings'][G['UNITNAME']] != 'path'):
								G['MF_savelevel'](v_11, 2)
							else:
								if (unit_6['values'][G['PATH_GATE']] == 0):
									G['MF_savepath'](v_11, 3)
								else:
									G['MF_savepath'](v_11, 1)
						if ((visuals is not None and visuals is not False) or (reveal is not None and reveal is not False)):
							unit_6['values'][G['COMPLETED']] = 2
							if ((unit_6['strings'][G['UNITNAME']] == 'path') and (unit_6['values'][G['PATH_GATE']] > 0)):
								unit_6['values'][G['COMPLETED']] = 1
						if (visuals is not None and visuals is not False):
							G['particles']('hot', (x_2 + ox_2), (y_2 + oy_2), 10, L_T([0, 3]))
							if (G['matches'] is None):
								G['MF_playsound'](L_concat('whoosh_alt', L_tostring(G['math']['random'](1, 5))))
							else:
								G['MF_playsound'](L_concat('intro_flower_', L_tostring(G['math']['random'](1, 7))))
	G['unlocklevels'] = f_unlocklevels
	def f_checkhidden(x_3=None, y_3=None, *_):  # L762
		ox_3, oy_3 = 0, 0
		result_3 = L_T()
		current_2 = L_T()
		hidden_2 = False
		for a_2 in L_range(1, 4):
			ndrs_2 = G['ndirs'][a_2]
			ox_3 = ndrs_2[1]
			oy_3 = ndrs_2[2]
			levels_2 = G['findallhere']((x_3 + ox_3), (y_3 + oy_3), None, True)
			if (L_len(levels_2) > 0):
				for i_16, v_12 in L_ipairs(levels_2):
					unit_7 = G['mmf']['newObject'](v_12)
					if ((unit_7['values'][G['COMPLETED']] == 0) and (L_strlen(unit_7['strings'][G['LEVELFILE']]) > 0)):
						L_insert(result_3, v_12)
						hidden_2 = True
		return (hidden_2, result_3,)
		return ()
	G['checkhidden'] = f_checkhidden
	def f_prizeget(id__7=None, *_):  # L790
		unit_8 = G['mmf']['newObject'](id__7)
		x_4 = L_floor(L_div((unit_8['x'] - G['Xoffset']), G['tilesize']))
		y_4 = L_floor(L_div((unit_8['y'] - G['Yoffset']), G['tilesize']))
		G['particles']('glow', x_4, y_4, 20, L_T([0, 3]), 1, 0)
		G['MF_playsound']('rule')
	G['prizeget'] = f_prizeget
	def f_hiddendata(x_5=None, y_5=None, reveal__2=None, *_):  # L799
		more = True
		reveal_2 = False
		if (reveal__2 is not None):
			reveal_2 = reveal__2
		hiddens = L_T()
		alreadydone = L_T()
		cx_2, cy_2 = x_5, y_5
		currtype_2 = 0
		while (more is not None and more is not False):
			id__8 = (cx_2 + (cy_2 * G['roomsizex']))
			if (alreadydone[id__8] is None):
				current_3 = G['findallhere'](cx_2, cy_2, None, True)
				current_gate = False
				if (L_len(current_3) > 0):
					for i_17, v_13 in L_ipairs(current_3):
						unit_9 = G['mmf']['newObject'](v_13)
						if (unit_9['strings'][G['UNITNAME']] == 'path'):
							currtype_2 = 1
							if (unit_9['values'][G['PATH_GATE']] > 0):
								current_gate = True
							if ((cx_2 == x_5) and (cy_2 == y_5)):
								current_gate = False
						else:
							currtype_2 = 0
				if ((cx_2 == x_5) and (cy_2 == y_5)):
					currtype_2 = (-1)
				hidden_3, result_4 = L_adjust((*G['checkhidden'](cx_2, cy_2),), 2)
				if (L_len(result_4) > 0):
					if (current_gate is False):
						for i_18, v_14 in L_ipairs(result_4):
							unit_10 = G['mmf']['newObject'](v_14)
							L_insert(hiddens, L_T([v_14, currtype_2]))
			alreadydone[id__8] = 1
			if (L_len(hiddens) > 0):
				unitid_5 = hiddens[1][1]
				unit_11 = G['mmf']['newObject'](unitid_5)
				currtype_2 = hiddens[1][2]
				L_remove(hiddens, 1)
				if (unit_11['strings'][G['UNITNAME']] != 'path'):
					if ((currtype_2 == 0) or (currtype_2 == (-1))):
						G['MF_savelevel'](unitid_5, 1)
						cx_2, cy_2 = unit_11['values'][G['XPOS']], unit_11['values'][G['YPOS']]
						if (reveal_2 is not None and reveal_2 is not False):
							unit_11['values'][G['COMPLETED']] = 1
				else:
					if ((currtype_2 == 1) or (currtype_2 == (-1))):
						if (unit_11['values'][G['PATH_GATE']] == 0):
							G['MF_savepath'](unitid_5, 3)
						else:
							G['MF_savepath'](unitid_5, 1)
						cx_2, cy_2 = unit_11['values'][G['XPOS']], unit_11['values'][G['YPOS']]
						G['unlocklevels'](cx_2, cy_2, None, reveal_2)
						if (reveal_2 is not None and reveal_2 is not False):
							unit_11['values'][G['COMPLETED']] = 1
			else:
				more = False
	G['hiddendata'] = f_hiddendata
	def f_getleveltree(*_):  # L899
		result_5 = ''
		if (L_len(G['leveltree']) > 0):
			for i_19, v_15 in L_ipairs(G['leveltree']):
				if (i_19 < L_len(G['leveltree'])):
					result_5 = L_concat(result_5, v_15, ',')
				else:
					result_5 = L_concat(result_5, v_15)
		else:
			L_noop('Leveltree is empty?')
		return result_5
	G['getleveltree'] = f_getleveltree
	def f_getleveltree_id(*_):  # L917
		result_6 = ''
		if (L_len(G['leveltree_id']) > 0):
			for i_20, v_16 in L_ipairs(G['leveltree_id']):
				if (i_20 < L_len(G['leveltree_id'])):
					result_6 = L_concat(result_6, v_16, ',')
				else:
					result_6 = L_concat(result_6, v_16)
		else:
			L_noop('Leveltree_id is empty?')
		return result_6
	G['getleveltree_id'] = f_getleveltree_id
	def f_openlevels(*_):  # L935
		levels_3 = L_T()
		for i_21, unit_12 in L_ipairs(G['units']):
			if (L_strlen(unit_12['strings'][G['U_LEVELFILE']]) > 1):
				L_insert(levels_3, unit_12['fixed'])
		gates = G['MF_findgates']()
		for i_22, unitid_6 in L_ipairs(gates):
			L_insert(levels_3, unitid_6)
		if (L_len(levels_3) > 0):
			for i_23, unitid_7 in L_ipairs(levels_3):
				unit_13 = G['mmf']['newObject'](unitid_7)
				if (unit_13['values'][G['COMPLETED']] == 3):
					x_6, y_6 = unit_13['values'][G['XPOS']], unit_13['values'][G['YPOS']]
					G['unlocklevels'](x_6, y_6, None, True)
					G['hiddendata'](x_6, y_6, True)
	G['openlevels'] = f_openlevels
	def f_addpath(id__9=None, *_):  # L964
		unitid_8 = G['MF_create']('path')
		unit_14 = G['mmf']['newObject'](unitid_8)
		i_24 = L_tostring(id__9)
		unit_14['values'][G['ONLINE']] = 1
		unit_14['values'][G['XPOS']] = (_t1 if L_t(_t1 := L_tonumber(G['MF_read']('level', 'paths', L_concat(i_24, 'X')))) else 0)
		unit_14['values'][G['YPOS']] = (_t2 if L_t(_t2 := L_tonumber(G['MF_read']('level', 'paths', L_concat(i_24, 'Y')))) else 0)
		unit_14['values'][G['DIR']] = (_t3 if L_t(_t3 := L_tonumber(G['MF_read']('level', 'paths', L_concat(i_24, 'dir')))) else 4)
		unit_14['values'][G['PATH_STYLE']] = (_t4 if L_t(_t4 := L_tonumber(G['MF_read']('level', 'paths', L_concat(i_24, 'style')))) else 0)
		unit_14['values'][G['PATH_GATE']] = (_t5 if L_t(_t5 := L_tonumber(G['MF_read']('level', 'paths', L_concat(i_24, 'gate')))) else 0)
		unit_14['values'][G['PATH_REQUIREMENT']] = (_t6 if L_t(_t6 := L_tonumber(G['MF_read']('level', 'paths', L_concat(i_24, 'requirement')))) else 0)
		world_2 = G['generaldata']['strings'][G['WORLD']]
		pathid_5 = L_concat(G['generaldata']['strings'][G['CURRLEVEL']], ',', L_tostring(unit_14['values'][G['XPOS']]), ',', L_tostring(unit_14['values'][G['YPOS']]))
		completed_save = (_t7 if L_t(_t7 := L_tonumber(G['MF_read']('save', world_2, pathid_5))) else 0)
		unit_14['values'][G['COMPLETED']] = L_max(unit_14['values'][G['COMPLETED']], completed_save)
		if (unit_14['values'][G['PATH_STYLE']] > 0):
			unit_14['values'][G['COMPLETED']] = L_max(2, unit_14['values'][G['COMPLETED']])
		unit_14['strings'][G['PATH_OBJECT']] = G['MF_read']('level', 'paths', L_concat(i_24, 'object'))
		unit_14['strings'][G['PATH_GATEOBJECT']] = G['MF_read']('level', 'paths', L_concat(i_24, 'unlock'))
		unit_14['x'] = ((G['Xoffset'] + (unit_14['values'][G['XPOS']] * G['tilesize'])) + (G['tilesize'] * 0.5))
		unit_14['y'] = ((G['Yoffset'] + (unit_14['values'][G['YPOS']] * G['tilesize'])) + (G['tilesize'] * 0.5))
		L_insert(G['paths'], unitid_8)
	G['addpath'] = f_addpath
	def f_addspecial(id__10=None, *_):  # L998
		unitid_9 = G['MF_create']('specialobject')
		unit_15 = G['mmf']['newObject'](unitid_9)
		i_25 = L_tostring(id__10)
		unit_15['values'][G['ONLINE']] = 1
		unit_15['values'][G['XPOS']] = G['MF_read']('level', 'specials', L_concat(i_25, 'X'))
		unit_15['values'][G['YPOS']] = G['MF_read']('level', 'specials', L_concat(i_25, 'Y'))
		unit_15['strings'][G['PATH_OBJECT']] = G['MF_read']('level', 'specials', L_concat(i_25, 'data'))
		unit_15['x'] = ((G['Xoffset'] + ((unit_15['values'][G['XPOS']] * G['tilesize']) * G['spritedata']['values'][G['TILEMULT']])) + ((G['tilesize'] * 0.5) * G['spritedata']['values'][G['TILEMULT']]))
		unit_15['y'] = ((G['Yoffset'] + ((unit_15['values'][G['YPOS']] * G['tilesize']) * G['spritedata']['values'][G['TILEMULT']])) + ((G['tilesize'] * 0.5) * G['spritedata']['values'][G['TILEMULT']]))
	G['addspecial'] = f_addspecial
	def f_loadlevelcompletion(*_):  # L1013
		world_3 = G['generaldata']['strings'][G['WORLD']]
		for i_26, unit_16 in L_ipairs(G['units']):
			level_2 = unit_16['strings'][G['LEVELFILE']]
			if (L_strlen(level_2) > 0):
				completion = (_t1 if L_t(_t1 := L_tonumber(G['MF_read']('save', world_3, level_2))) else 0)
				if (completion > 0):
					unit_16['values'][G['COMPLETED']] = completion
		for i_27, unitid_10 in L_ipairs(G['paths']):
			unit_17 = G['mmf']['newObject'](unitid_10)
			level_3 = unit_17['strings'][G['LEVELFILE']]
			x_7, y_7 = unit_17['values'][G['XPOS']], unit_17['values'][G['YPOS']]
			if (L_strlen(level_3) > 0):
				completion_2 = (_t2 if L_t(_t2 := L_tonumber(G['MF_read']('save', world_3, L_concat(level_3, ',', L_tostring(x_7), ',', L_tostring(y_7))))) else 0)
				if (completion_2 > 0):
					unit_17['values'][G['COMPLETED']] = completion_2
	G['loadlevelcompletion'] = f_loadlevelcompletion
	def f_revealpaths(dataid_2=None, *_):  # L1042
		gdata = G['mmf']['newObject'](dataid_2)
		world_4 = G['generaldata']['strings'][G['WORLD']]
		level_4 = G['generaldata']['strings'][G['CURRLEVEL']]
		removethesepaths = L_T()
		removetheseunits = L_T()
		for i_28, unitid_11 in L_ipairs(G['paths']):
			unit_18 = G['mmf']['newObject'](unitid_11)
			x_8, y_8 = unit_18['values'][G['XPOS']], unit_18['values'][G['YPOS']]
			status = unit_18['values'][G['COMPLETED']]
			if ((status > 0) and (unit_18['values'][G['PATH_TARGET']] == 0)):
				newid = G['MF_create'](unit_18['strings'][G['PATH_OBJECT']])
				new = G['mmf']['newObject'](newid)
				new['values'][G['ONLINE']] = 1
				new['values'][G['XPOS']] = unit_18['values'][G['XPOS']]
				new['values'][G['YPOS']] = unit_18['values'][G['YPOS']]
				new['x'] = ((G['Xoffset'] + ((new['values'][G['XPOS']] * G['tilesize']) * G['spritedata']['values'][G['TILEMULT']])) + ((G['tilesize'] * 0.5) * G['spritedata']['values'][G['TILEMULT']]))
				new['y'] = ((G['Yoffset'] + ((new['values'][G['YPOS']] * G['tilesize']) * G['spritedata']['values'][G['TILEMULT']])) + ((G['tilesize'] * 0.5) * G['spritedata']['values'][G['TILEMULT']]))
				new['values'][G['DIR']] = unit_18['values'][G['DIR']]
				new['values'][G['COMPLETED']] = (3 - (L_min(unit_18['values'][G['PATH_GATE']], 1) * 2))
				new['strings'][G['LEVELFILE']] = ''
				G['addunit'](newid)
				unit_18['values'][G['PATH_TARGET']] = newid
				prizes = (_t1 if L_t(_t1 := L_tonumber(G['MF_read']('save', L_concat(world_4, '_prize'), 'total'))) else 0)
				clears = (_t2 if L_t(_t2 := L_tonumber(G['MF_read']('save', L_concat(world_4, '_clears'), 'total'))) else 0)
				bonus = (_t3 if L_t(_t3 := L_tonumber(G['MF_read']('save', L_concat(world_4, '_bonus'), 'total'))) else 0)
				localprizes = (_t4 if L_t(_t4 := L_tonumber(G['MF_read']('save', L_concat(world_4, '_prize'), level_4))) else 0)
				if (new['strings'][G['UNITTYPE']] == 'text'):
					G['updatecode'] = 1
				if ((unit_18['values'][G['PATH_GATE']] == 1) and (prizes >= unit_18['values'][G['PATH_REQUIREMENT']])):
					if (status < 3):
						new['values'][G['COMPLETED']] = (-2)
						new['values'][G['A']] = unit_18['values'][G['PATH_REQUIREMENT']]
						unit_18['values'][G['COMPLETED']] = 3
					else:
						new['values'][G['COMPLETED']] = 3
						G['opengate'](newid)
				elif ((unit_18['values'][G['PATH_GATE']] == 2) and (clears >= unit_18['values'][G['PATH_REQUIREMENT']])):
					if (status < 3):
						new['values'][G['COMPLETED']] = (-3)
						new['values'][G['A']] = unit_18['values'][G['PATH_REQUIREMENT']]
						unit_18['values'][G['COMPLETED']] = 3
					else:
						new['values'][G['COMPLETED']] = 3
						G['opengate'](newid)
				elif ((unit_18['values'][G['PATH_GATE']] == 3) and (bonus >= unit_18['values'][G['PATH_REQUIREMENT']])):
					if (status < 3):
						new['values'][G['COMPLETED']] = (-4)
						new['values'][G['A']] = unit_18['values'][G['PATH_REQUIREMENT']]
						unit_18['values'][G['COMPLETED']] = 3
					else:
						new['values'][G['COMPLETED']] = 3
						G['opengate'](newid)
				elif ((unit_18['values'][G['PATH_GATE']] == 4) and (localprizes >= unit_18['values'][G['PATH_REQUIREMENT']])):
					if (status < 3):
						new['values'][G['COMPLETED']] = (-5)
						new['values'][G['A']] = unit_18['values'][G['PATH_REQUIREMENT']]
						unit_18['values'][G['COMPLETED']] = 3
					else:
						new['values'][G['COMPLETED']] = 3
						G['opengate'](newid)
				if (unit_18['values'][G['PATH_GATE']] == 0):
					unit_18['flags'][G['DEAD']] = True
					L_insert(removetheseunits, unitid_11)
				newtest = G['mmf']['newObject'](newid)
				if (newtest is not None):
					if (G['generaldata']['strings'][G['WORLD']] != G['generaldata']['strings'][G['BASEWORLD']]):
						newname = G['getname'](new)
						hidethis = G['hasfeature'](newname, 'is', 'hide', newid, x_8, y_8)
						if (hidethis is not None):
							new['visible'] = False
					if (new['values'][G['TILING']] == 1):
						G['dynamic'](newid)
				L_insert(removethesepaths, i_28)
		roffset = 0
		for a_3, b in L_ipairs(removethesepaths):
			L_remove(G['paths'], (b - roffset))
			roffset = (roffset + 1)
		for a_4, b_2 in L_ipairs(removetheseunits):
			G['MF_cleanremove'](b_2)
	G['revealpaths'] = f_revealpaths
	def f_opengate(unitid_12=None, *_):  # L1160
		unit_19 = G['mmf']['newObject'](unitid_12)
		pathobject = G['editor']['strings'][G['PATH_OBJECT']]
		cpo, cpgo = G['MF_checkcustompathobject'](unitid_12), None
		if (L_len(cpgo) > 0):
			pathobject = cpgo
		newid_2 = G['MF_create'](pathobject)
		new_2 = G['mmf']['newObject'](newid_2)
		new_2['values'][G['ONLINE']] = 1
		new_2['values'][G['XPOS']] = unit_19['values'][G['XPOS']]
		new_2['values'][G['YPOS']] = unit_19['values'][G['YPOS']]
		new_2['x'] = ((G['Xoffset'] + ((new_2['values'][G['XPOS']] * G['tilesize']) * G['spritedata']['values'][G['TILEMULT']])) + ((G['tilesize'] * 0.5) * G['spritedata']['values'][G['TILEMULT']]))
		new_2['y'] = ((G['Yoffset'] + ((new_2['values'][G['YPOS']] * G['tilesize']) * G['spritedata']['values'][G['TILEMULT']])) + ((G['tilesize'] * 0.5) * G['spritedata']['values'][G['TILEMULT']]))
		new_2['values'][G['DIR']] = unit_19['values'][G['DIR']]
		new_2['values'][G['COMPLETED']] = 3
		new_2['strings'][G['LEVELFILE']] = ''
		G['addunit'](newid_2)
		if (new_2['values'][G['TILING']] == 1):
			G['dynamic'](newid_2)
		G['delunit'](unitid_12)
		G['MF_cleanremove'](unitid_12)
	G['opengate'] = f_opengate
	def f_mapunlock(dataid_3=None, *_):  # L1192
		data_2 = G['mmf']['newObject'](dataid_3)
		world_5 = G['generaldata']['strings'][G['WORLD']]
		level_5 = G['generaldata']['strings'][G['CURRLEVEL']]
		data_2['values'][G['UNLOCKTIMER']] = (data_2['values'][G['UNLOCKTIMER']] + 1)
		timer_2 = data_2['values'][G['UNLOCKTIMER']]
		unlock_2 = data_2['values'][G['UNLOCK']]
		if (unlock_2 == 4):
			if (timer_2 == 5):
				unlocklevels = (_t1 if L_t(_t1 := G['MF_read']('level', 'general', 'unlocklevels')) else '')
				levels_4 = G['MF_parsestring'](unlocklevels)
				G['matches'] = L_T()
				G['matches']['origin'] = level_5
				G['matches']['previous'] = data_2['strings'][1]
				for i_29, v_17 in L_ipairs(levels_4):
					if (L_strlen(v_17) > 0):
						L_insert(G['matches'], v_17)
			if ((timer_2 == 10) and (L_len(G['matches']) == 0)):
				G['generaldata']['values'][G['IGNORE']] = 0
				data_2['values'][G['MAPCLEAR']] = 0
				data_2['values'][G['UNLOCK']] = 0
				data_2['values'][G['UNLOCKTIMER']] = 0
				G['hiddemap'] = None
				G['matches'] = None
		if ((unlock_2 == 4) or (unlock_2 == 5)):
			if (G['matches'] is not None):
				if ((timer_2 == 10) and (L_len(G['matches']) > 0)):
					data_2['values'][G['UNLOCK']] = 5
					unlock_2 = data_2['values'][G['UNLOCK']]
		if (unlock_2 == 5):
			if (((timer_2 == (-80)) and (G['generaldata']['values'][G['MODE']] == 0)) and ((G['editor']['values'][G['INEDITOR']] == 0) or (G['editor']['values'][G['INEDITOR']] == 3))):
				G['MF_playsound']('roll')
			if (((((timer_2 > (-80)) and (timer_2 < (-20))) and ((timer_2 % 2) == 0)) and (G['generaldata']['values'][G['MODE']] == 0)) and ((G['editor']['values'][G['INEDITOR']] == 0) or (G['editor']['values'][G['INEDITOR']] == 3))):
				for i_30, unit_20 in L_ipairs(G['units']):
					if (unit_20['strings'][G['LEVELFILE']] == G['matches']['origin']):
						x_9, y_9 = unit_20['values'][G['XPOS']], unit_20['values'][G['YPOS']]
						G['particles']('unlock', x_9, y_9, 2, L_T([2, 4]))
			if (((timer_2 == (-20)) and (G['generaldata']['values'][G['MODE']] == 0)) and ((G['editor']['values'][G['INEDITOR']] == 0) or (G['editor']['values'][G['INEDITOR']] == 3))):
				for i_31, unit_21 in L_ipairs(G['units']):
					if (unit_21['strings'][G['LEVELFILE']] == G['matches']['origin']):
						if (G['hiddenmap'] is None):
							G['hiddenmap'] = L_T()
							G['hiddenmap']['unlocks'] = L_T()
						G['hiddenmap']['start'] = L_T([unit_21['values'][G['XPOS']], unit_21['values'][G['YPOS']]])
						G['generaldata']['values'][G['SHAKE']] = 15
						data_2['values'][G['UNLOCK']] = 2
						data_2['values'][G['UNLOCKTIMER']] = 71
						unit_21['direction'] = 16
						unit_21['values'][G['COMPLETED']] = 3
						prizeid_2 = G['MF_specialcreate']('Prize')
						prize_2 = G['mmf']['newObject'](prizeid_2)
						G['MF_playsound_freq']('winnery_fast', 38000)
						G['MF_playsound']('pop3')
						G['MF_stopsound']('roll')
						x_10, y_10 = unit_21['values'][G['XPOS']], unit_21['values'][G['YPOS']]
						prize_2['layer'] = 2
						prize_2['values'][G['ONLINE']] = 1
						prize_2['values'][G['XPOS']] = ((G['Xoffset'] + (x_10 * G['tilesize'])) + (G['tilesize'] * 0.5))
						prize_2['values'][G['YPOS']] = ((G['Yoffset'] + (y_10 * G['tilesize'])) + (G['tilesize'] * 0.5))
						prize_2['values'][G['YVEL']] = (-20)
						prize_2['scaleX'] = 0.1
						prize_2['scaleY'] = 0.1
						prize_2['direction'] = 1
						G['particles']('smoke', unit_21['values'][G['XPOS']], unit_21['values'][G['YPOS']], 20, L_T([0, 3]))
			if ((timer_2 == 10) and (L_len(G['matches']) == 0)):
				data_2['values'][G['UNLOCK']] = 6
				unlock_2 = data_2['values'][G['UNLOCK']]
			if (timer_2 == 60):
				G['generaldata']['values'][G['TRANSITIONREASON']] = 10
				G['generaldata']['values'][G['TRANSITIONED']] = 0
				G['MF_loop']('transition', 1)
		if (unlock_2 == 6):
			if (timer_2 == 80):
				G['generaldata']['values'][G['TRANSITIONREASON']] = 10
				G['generaldata']['values'][G['TRANSITIONED']] = 0
				G['MF_loop']('transition', 1)
		if ((unlock_2 == 5) or (unlock_2 == 6)):
			if ((((G['generaldata']['values'][G['TRANSITIONED']] == 1) and (G['generaldata']['values'][G['TRANSITIONREASON']] == 10)) and (G['generaldata']['values'][G['MODE']] == 0)) and ((G['editor']['values'][G['INEDITOR']] == 0) or (G['editor']['values'][G['INEDITOR']] == 3))):
				cursors_2 = G['getunitswitheffect']('select')
				for i_32, cursorunit_2 in L_ipairs(cursors_2):
					cursorunit_2['visible'] = False
				G['mapunlock_transition'](dataid_3, cursors_2)
	G['mapunlock'] = f_mapunlock
	def f_mapunlock_transition(dataid_4=None, cursors_3=None, *_):  # L1323
		data_3 = G['mmf']['newObject'](dataid_4)
		cursor = G['mmf']['newObject'](G['cursorid'])
		world_6 = G['generaldata']['strings'][G['WORLD']]
		PREVIOUS = 1
		TRANSITION = 18
		TRANSITIONREASON = 20
		unlock_3 = data_3['values'][G['UNLOCK']]
		if (unlock_3 == 5):
			for i_33, cursorunit_3 in L_ipairs(cursors_3):
				cursorunit_3['visible'] = False
			G['generaldata']['values'][TRANSITION] = 0
			G['generaldata']['values'][TRANSITIONREASON] = 0
			G['generaldata']['strings'][G['CURRLEVEL']] = G['matches'][1]
			L_remove(G['matches'], 1)
			data_3['values'][G['UNLOCKTIMER']] = (-90)
			G['clearunits']()
			G['MF_loop']('clear', 1)
			G['MF_loop']('new', 1)
			for i_34, unit_22 in L_ipairs(G['units']):
				if (unit_22['strings'][G['LEVELFILE']] == G['matches']['origin']):
					unit_22['direction'] = 0
					unit_22['values'][G['COMPLETED']] = 2
		elif (unlock_3 == 6):
			G['generaldata']['values'][TRANSITION] = 0
			G['generaldata']['values'][TRANSITIONREASON] = 0
			G['generaldata']['values'][G['IGNORE']] = 0
			G['generaldata']['strings'][G['CURRLEVEL']] = G['matches']['origin']
			for i_35, cursorunit_4 in L_ipairs(cursors_3):
				cursorunit_4['visible'] = True
			data_3['strings'][G['PREVIOUSLEVEL']] = G['matches']['previous']
			G['clearunits']()
			G['MF_loop']('clear', 1)
			G['MF_loop']('new', 1)
			data_3['values'][G['UNLOCK']] = 0
			data_3['values'][G['UNLOCKTIMER']] = 0
			data_3['values'][G['MAPCLEAR']] = 0
			G['matches'] = None
	G['mapunlock_transition'] = f_mapunlock_transition
	def f_getgates(*_):  # L1383
		G['gatelist'] = L_T()
		world_7 = G['generaldata']['strings'][G['WORLD']]
		level_6 = G['generaldata']['strings'][G['CURRLEVEL']]
		G['generaldata']['values'][G['IGNORE']] = 1
		for i_36, unit_23 in L_ipairs(G['units']):
			if (unit_23['values'][G['COMPLETED']] < (-1)):
				L_insert(G['gatelist'], unit_23['fixed'])
				x_11, y_11 = unit_23['values'][G['XPOS']], unit_23['values'][G['YPOS']]
				G['MF_store']('save', world_7, L_concat(level_6, ',', L_tostring(x_11), ',', L_tostring(y_11)), '3')
				G['hiddendata'](x_11, y_11, False)
	G['getgates'] = f_getgates
	def f_gateunlock(dataid_5=None, *_):  # L1401
		data_4 = G['mmf']['newObject'](dataid_5)
		world_8 = G['generaldata']['strings'][G['WORLD']]
		level_7 = G['generaldata']['strings'][G['CURRLEVEL']]
		data_4['values'][G['UNLOCKTIMER']] = (data_4['values'][G['UNLOCKTIMER']] + 1)
		timer_3 = data_4['values'][G['UNLOCKTIMER']]
		unlock_4 = data_4['values'][G['UNLOCK']]
		if (unlock_4 == 7):
			for i_37, unitid_13 in L_ipairs(G['gatelist']):
				unit_24 = G['mmf']['newObject'](unitid_13)
				x_12, y_12 = unit_24['values'][G['XPOS']], unit_24['values'][G['YPOS']]
				if (timer_3 == 10):
					gateobjs = G['MF_findgates']()
					gatetype = (-1)
					gatereq = 0
					for i_38, v_18 in L_ipairs(gateobjs):
						vunit = G['mmf']['newObject'](v_18)
						if (unitid_13 == vunit['values'][G['PATH_TARGET']]):
							gatetype = vunit['values'][G['PATH_GATE']]
							gatereq = vunit['values'][G['PATH_REQUIREMENT']]
					G['MF_gateeffect'](unitid_13, gatereq, gatetype)
					G['MF_playsound']('roll')
				if ((timer_3 > 10) and (timer_3 < 130)):
					if ((timer_3 % 20) == 0):
						if (unit_24['values'][G['COMPLETED']] == (-2)):
							G['particles']('bonus', x_12, y_12, 2, L_T([2, 4]))
						elif (unit_24['values'][G['COMPLETED']] == (-3)):
							G['particles']('bonus', x_12, y_12, 2, L_T([4, 2]))
						elif (unit_24['values'][G['COMPLETED']] == (-4)):
							G['particles']('bonus', x_12, y_12, 2, L_T([0, 3]))
						elif (unit_24['values'][G['COMPLETED']] == (-5)):
							G['particles']('bonus', x_12, y_12, 2, L_T([2, 4]))
				elif (timer_3 == 130):
					G['generaldata']['values'][G['SHAKE']] = 20
					G['generaldata']['values'][G['IGNORE']] = 0
					if (unit_24['values'][G['COMPLETED']] == (-2)):
						G['particles']('bonus', x_12, y_12, 40, L_T([2, 4]))
					elif (unit_24['values'][G['COMPLETED']] == (-3)):
						G['particles']('bonus', x_12, y_12, 40, L_T([4, 2]))
					elif (unit_24['values'][G['COMPLETED']] == (-4)):
						G['particles']('bonus', x_12, y_12, 40, L_T([0, 3]))
					elif (unit_24['values'][G['COMPLETED']] == (-5)):
						G['particles']('bonus', x_12, y_12, 40, L_T([2, 4]))
					data_4['values'][G['UNLOCK']] = 0
					data_4['values'][G['UNLOCKTIMER']] = 0
					unit_24['strings'][G['U_LEVELFILE']] = ''
					G['particles']('unlock', x_12, y_12, 20, L_T([0, 3]))
					G['MF_playsound']('gate')
					G['MF_stopsound']('roll')
					hidden_4 = L_first(G['checkhidden'](x_12, y_12))
					if (hidden_4 is not None and hidden_4 is not False):
						data_4['values'][G['UNLOCKTIMER']] = 109
						data_4['values'][G['UNLOCK']] = 2
						G['hiddenmap'] = L_T()
						G['hiddenmap']['unlocks'] = L_T()
						G['hiddenmap']['start'] = L_T([x_12, y_12])
					G['opengate'](unitid_13)
	G['gateunlock'] = f_gateunlock
	def f_handlespecial(unitid_14=None, type_=None, data_5=None, *_):  # L1484
		unit_25 = G['mmf']['newObject'](unitid_14)
		if (type_ == 'controls'):
			subtype = data_5[1]
			gamepad = G['MF_profilefound']()
			gamepad_ = False
			if (gamepad is not None):
				gamepad_ = True
			if (G['generaldata2']['values'][G['BUTTONPROMPTTYPE']] == 0):
				gamepad_ = False
				gamepad = None
			if ((gamepad is None) or (((((((gamepad is not None) and (subtype != 'right')) and (subtype != 'left')) and (subtype != 'up')) and (subtype != 'right2')) and (subtype != 'left2')) and (subtype != 'up2'))):
				x_13 = ((G['Xoffset'] + ((unit_25['values'][G['XPOS']] * G['tilesize']) * G['spritedata']['values'][G['TILEMULT']])) + ((G['tilesize'] * G['spritedata']['values'][G['TILEMULT']]) * 0.5))
				y_13 = ((G['Yoffset'] + ((unit_25['values'][G['YPOS']] * G['tilesize']) * G['spritedata']['values'][G['TILEMULT']])) + ((G['tilesize'] * G['spritedata']['values'][G['TILEMULT']]) * 0.5))
				xtile = unit_25['values'][G['XPOS']]
				ytile = unit_25['values'][G['YPOS']]
				finaltype = subtype
				if ((gamepad is None) or (((gamepad is not None) and (subtype != 'down')) and (subtype != 'down2'))):
					G['createcontrolicon'](finaltype, gamepad_, x_13, y_13, 'InGame', None, 1, L_T([xtile, ytile]))
				elif ((gamepad is not None) and ((subtype == 'down') or (subtype == 'down2'))):
					if (subtype == 'down2'):
						finaltype = 'move2'
					else:
						finaltype = 'move'
					G['createcontrolicon'](finaltype, gamepad_, x_13, y_13, 'InGame', None, 1, L_T([xtile, ytile]))
				if ((((((subtype != 'right') and (subtype != 'left')) and (subtype != 'up')) and (subtype != 'right2')) and (subtype != 'left2')) and (subtype != 'up2')):
					if ((subtype == 'down') and (gamepad is None)):
						finaltype = 'move'
					if ((subtype == 'down2') and (gamepad is None)):
						finaltype = 'move2'
					G['writetext'](G['langtext'](finaltype), 0, x_13, ((y_13 + (G['tilesize'] * G['spritedata']['values'][G['TILEMULT']])) + 2), 'InGame', True, 1, True)
		elif (type_ == 'level'):
			x_14, y_14 = unit_25['values'][G['XPOS']], unit_25['values'][G['YPOS']]
			things_2 = G['findallhere'](x_14, y_14)
			levelfile = data_5[1]
			G['MF_setfile']('level', L_concat('Data/Worlds/', G['generaldata']['strings'][G['WORLD']], '/', levelfile, '.ld'))
			levelname = G['MF_read']('level', 'general', 'name')
			leveltype = L_tonumber(G['MF_read']('level', 'general', 'leveltype'))
			G['MF_setfile']('level', L_concat('Data/Worlds/', G['generaldata']['strings'][G['WORLD']], '/', G['generaldata']['strings'][G['CURRLEVEL']], '.ld'))
			leveltype_bool = False
			if (leveltype == 1):
				for i_39, v_19 in L_ipairs(G['leveltree']):
					if ((v_19 != G['generaldata']['strings'][G['LEVELFILE']]) and (v_19 == levelfile)):
						leveltype_bool = True
			unit_25['flags'][G['MAPLEVEL']] = leveltype_bool
			for i_40, v_20 in L_ipairs(things_2):
				level_8 = G['mmf']['newObject'](v_20)
				if (level_8['className'] != 'level'):
					level_8['strings'][G['U_LEVELFILE']] = levelfile
					level_8['strings'][G['U_LEVELNAME']] = levelname
					level_8['values'][G['VISUALLEVEL']] = L_tonumber(data_5[3])
					level_8['values'][G['VISUALSTYLE']] = L_tonumber(data_5[2])
					level_8['flags'][G['MAPLEVEL']] = leveltype_bool
					if (L_strlen(data_5[4]) > 0):
						level_8['values'][G['COMPLETED']] = L_tonumber(data_5[4])
					if ((L_strlen(data_5[5]) > 0) and (L_strlen(data_5[6]) > 0)):
						level_8['strings'][G['COLOUR']] = L_concat(data_5[5], ',', data_5[6])
					if ((L_strlen(data_5[7]) > 0) and (L_strlen(data_5[8]) > 0)):
						level_8['strings'][G['CLEARCOLOUR']] = L_concat(data_5[7], ',', data_5[8])
		elif (type_ == 'flower'):
			flowerid = G['MF_specialcreate']('Flower_center')
			flower = G['mmf']['newObject'](flowerid)
			flower['strings'][2] = 'flower'
			flower['values'][10] = 2
			flower['values'][6] = 1
			flower['values'][8] = L_tonumber(data_5[3])
			flower['x'] = unit_25['x']
			flower['y'] = unit_25['y']
			flower['strings'][1] = L_concat(data_5[1], ', ', data_5[2])
		elif (type_ == 'art'):
			artid = G['MF_specialcreate']('Secret_art')
			art = G['mmf']['newObject'](artid)
			art['x'] = (unit_25['x'] + (G['tilesize'] * 0.5))
			art['y'] = (unit_25['y'] - (G['tilesize'] * 0.5))
		elif (type_ == 'sign'):
			x_15, y_15 = unit_25['values'][G['XPOS']], unit_25['values'][G['YPOS']]
			things_3 = G['findallhere'](x_15, y_15)
			fulltext = L_concat(data_5[1], '=', data_5[2], '=', data_5[3])
			for i_41, v_21 in L_ipairs(things_3):
				vunit_2 = G['mmf']['newObject'](v_21)
				vunit_2['strings'][G['UNITSIGNTEXT']] = fulltext
		elif (type_ == 'sign_lang'):
			x_16, y_16 = unit_25['values'][G['XPOS']], unit_25['values'][G['YPOS']]
			things_4 = G['findallhere'](x_16, y_16)
			fulltext_2 = L_concat(G['langtext'](data_5[1], True, True), '=', G['langtext'](data_5[2], True, True), '=', G['langtext'](data_5[3], True, True))
			for i_42, v_22 in L_ipairs(things_4):
				vunit_3 = G['mmf']['newObject'](v_22)
				vunit_3['strings'][G['UNITSIGNTEXT']] = fulltext_2
	G['handlespecial'] = f_handlespecial
	def f_checkmaplevel(unitid_15=None, *_):  # L1621
		unit_26 = G['mmf']['newObject'](unitid_15)
		for i_43, v_23 in L_ipairs(G['leveltree']):
			if ((v_23 != G['generaldata']['strings'][G['LEVELFILE']]) and (v_23 == unit_26['strings'][G['U_LEVELFILE']])):
				unit_26['flags'][G['MAPLEVEL']] = True
	G['checkmaplevel'] = f_checkmaplevel
	def f_gateindicatorcheck(x_17=None, y_17=None, *_):  # L1631
		cursors_4 = G['getunitswitheffect']('select', None, None, None, True)
		for i_44, unit_27 in L_ipairs(cursors_4):
			x_ = unit_27['values'][G['XPOS']]
			y_ = unit_27['values'][G['YPOS']]
			dx = abs((x_ - x_17))
			dy = abs((y_ - y_17))
			if ((dx + dy) <= 1):
				return True
		return False
	G['gateindicatorcheck'] = f_gateindicatorcheck
	def f_rewritecontrolicontext(unitid_16=None, *_):  # L1649
		unit_28 = G['mmf']['newObject'](unitid_16)
		x_18 = ((G['Xoffset'] + ((unit_28['values'][G['MISC_A']] * G['tilesize']) * G['spritedata']['values'][G['TILEMULT']])) + ((G['tilesize'] * G['spritedata']['values'][G['TILEMULT']]) * 0.5))
		y_18 = ((G['Yoffset'] + ((unit_28['values'][G['MISC_B']] * G['tilesize']) * G['spritedata']['values'][G['TILEMULT']])) + ((G['tilesize'] * G['spritedata']['values'][G['TILEMULT']]) * 0.5))
		finaltype_2 = unit_28['strings'][G['BUTTONNAME']]
		if (finaltype_2 == 'down'):
			finaltype_2 = 'move'
		G['writetext'](G['langtext'](finaltype_2), 0, x_18, ((y_18 + (G['tilesize'] * G['spritedata']['values'][G['TILEMULT']])) + 2), 'InGame', True, 1, False)
	G['rewritecontrolicontext'] = f_rewritecontrolicontext
	def f_customending_win(*_):  # L1664
		G['MF_end_single']()
		G['MF_credits'](1)
	G['customending_win'] = f_customending_win
	def f_displaysigntext(x_19=None, y_19=None, ignore=None, *_):  # L1669
		if ((ignore is not None) and (ignore is not None and ignore is not False)):
			return False
		for i_45 in L_range((-1), 1):
			for j in L_range((-1), 1):
				if ((i_45 == 0) or (j == 0)):
					tileid = ((x_19 + i_45) + ((y_19 + j) * G['roomsizex']))
					if (G['unitmap'][tileid] is not None):
						stuff = G['findfeatureat'](None, 'is', 'you', (x_19 + i_45), (y_19 + j))
						if (stuff is not None):
							return True
						elif (G['featureindex']['3d'] is not None):
							stuff = G['findfeatureat'](None, 'is', '3d', (x_19 + i_45), (y_19 + j))
							if (stuff is not None):
								return True
						elif (G['featureindex']['you2'] is not None):
							stuff = G['findfeatureat'](None, 'is', 'you2', (x_19 + i_45), (y_19 + j))
							if (stuff is not None):
								return True
		return False
	G['displaysigntext'] = f_displaysigntext
	def f_specialroomscale(*_):  # L1705
		s = G['getspecialroomscale']()
		if (s > 0):
			G['spritedata']['values'][G['TILEMULT']] = s
	G['specialroomscale'] = f_specialroomscale
	def f_getspecialroomscale(*_):  # L1713
		x_20 = G['generaldata']['values'][G['ROOMSIZEX']]
		y_20 = G['generaldata']['values'][G['ROOMSIZEY']]
		if ((x_20 <= 5) and (y_20 == 7)):
			return 2.244
		if ((x_20 <= 16) and (y_20 == 9)):
			return 2.244
		if ((x_20 <= 22) and (y_20 == 13)):
			return 1.544
		if ((x_20 <= 24) and (y_20 == 14)):
			return 1.46
		if ((x_20 <= 29) and (y_20 == 17)):
			return 1.3
		if ((x_20 <= 31) and (y_20 == 18)):
			return 1.14
		if (y_20 <= 6):
			if (x_20 == 8):
				return 4.38
		if (y_20 <= 7):
			if (x_20 == 19):
				return 1.875
			elif (x_20 == 16):
				return 2.24
			elif (x_20 == 13):
				return 2.74
			elif (x_20 == 11):
				return 3.24
			if (y_20 == 7):
				if (x_20 == 12):
					return 2.88
				elif ((x_20 >= 5) and (x_20 <= 10)):
					return 2.88
		if (y_20 <= 8):
			if (x_20 == 24):
				return 1.544
			elif (x_20 == 19):
				return 1.875
			elif (x_20 == 16):
				return 2.24
		if (y_20 <= 9):
			if (x_20 == 24):
				return 1.544
			elif (x_20 == 19):
				return 1.875
		if (y_20 <= 10):
			if (x_20 == 24):
				return 1.544
			elif (x_20 == 19):
				return 1.875
			elif (x_20 == 18):
				return 2.0
		if ((y_20 <= 11) and (x_20 == 24)):
			return 1.544
		if (y_20 <= 12):
			if (x_20 == 24):
				return 1.544
			elif (x_20 == 22):
				return 1.64
		if (y_20 <= 13):
			if (x_20 == 24):
				return 1.544
			elif (x_20 == 23):
				return 1.544
		if ((y_20 <= 14) and (x_20 == 26)):
			return 1.46
		elif ((y_20 <= 16) and (x_20 == 29)):
			return 1.3
		elif ((y_20 <= 17) and (x_20 == 30)):
			return 1.244
		elif ((y_20 <= 18) and (x_20 == 32)):
			return 1.144
		elif ((y_20 <= 19) and (x_20 == 34)):
			return 1.044
		return 0
	G['getspecialroomscale'] = f_getspecialroomscale
