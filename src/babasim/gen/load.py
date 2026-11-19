"""Generated from load.lua by tools/lua2py.py. Do not edit."""
from babasim.luart import *  # noqa: F403


def load(G):
	def f_init(tilemapid=None, roomsizex_=None, roomsizey_=None, tilesize_=None, Xoffset_=None, Yoffset_=None, generaldataid=None, generaldataid2=None, generaldataid3=None, generaldataid4=None, generaldataid5=None, spritedataid=None, vardataid=None, screenw_=None, screenh_=None, *_):  # L1
		G['map'] = G['TileMap']['new'](tilemapid)
		G['generaldata'] = G['mmf']['newObject'](generaldataid)
		G['generaldata2'] = G['mmf']['newObject'](generaldataid2)
		G['generaldata3'] = G['mmf']['newObject'](generaldataid3)
		G['generaldata4'] = G['mmf']['newObject'](generaldataid4)
		G['generaldata5'] = G['mmf']['newObject'](generaldataid5)
		G['spritedata'] = G['mmf']['newObject'](spritedataid)
		G['vardata'] = G['mmf']['newObject'](vardataid)
		G['roomsizex'] = roomsizex_
		G['roomsizey'] = roomsizey_
		G['tilesize'] = tilesize_
		G['f_tilesize'] = G['spritedata']['values'][G['FIXEDTILESIZE']]
		G['Xoffset'] = Xoffset_
		G['Yoffset'] = Yoffset_
		G['screenw'] = screenw_
		G['screenh'] = screenh_
		G['features'] = L_T()
		G['visualfeatures'] = L_T()
		G['featureindex'] = L_T()
		G['condfeatureindex'] = L_T()
		G['objectdata'] = L_T()
		G['units'] = L_T()
		G['tiledunits'] = L_T()
		G['codeunits'] = L_T()
		G['unitlists'] = L_T()
		G['objectlist'] = L_T()
		G['objectpalette'] = L_T()
		G['undobuffer'] = L_T()
		G['animunits'] = L_T()
		G['unitmap'] = L_T()
		G['unittypeshere'] = L_T()
		G['unitreference'] = L_T()
		G['deleted'] = L_T()
		G['ruleids'] = L_T()
		G['updatelist'] = L_T()
		G['objectcolours'] = L_T()
		G['wordunits'] = L_T()
		G['wordrelatedunits'] = L_T()
		G['letterunits'] = L_T()
		G['letterunits_map'] = L_T()
		G['paths'] = L_T()
		G['paradox'] = L_T()
		G['movelist'] = L_T()
		G['effecthistory'] = L_T()
		G['notfeatures'] = L_T()
		G['groupfeatures'] = L_T()
		G['groupmembers'] = L_T()
		G['pushedunits'] = L_T()
		G['customobjects'] = L_T()
		G['cobjects'] = L_T()
		G['condstatus'] = L_T()
		G['emptydata'] = L_T()
		G['leveldata'] = L_T()
		G['leveldata']['colours'] = L_T()
		G['leveldata']['currcolour'] = 0
		G['undobuffer_editor'] = L_T([L_T()])
		G['latestleveldetails'] = L_T([], {'lnum': (-1), 'ltype': (-1)})
		G['edgetiles'] = L_T()
		G['funnywalls'] = L_T()
		G['visiontargets'] = L_T()
		G['vision_rendered'] = L_T()
		G['deletereference'] = L_T()
		G['poweredstatus'] = L_T()
		G['specialtiling'] = L_T()
		G['backparticles'] = L_T()
		G['generaldata']['values'][G['CURRID']] = 1
		G['updatecode'] = 1
		G['doundo'] = True
		G['updateundo'] = True
		G['ruledebug'] = False
		G['modsinuse'] = False
		G['logevents'] = True
		G['maprotation'] = 0
		G['mapdir'] = 3
		G['last_key'] = 0
		G['levelconversions'] = L_T()
		G['auto_dir'] = L_T()
		G['destroylevel_check'] = False
		G['destroylevel_style'] = ''
		G['HACK_MOVES'] = 0
		G['HACK_INFINITY'] = 0
		G['movemap'] = L_T()
		G['Seed'] = 0
		G['Fixedseed'] = 100
		G['Seedingtype'] = 0
		G['base_octave'] = 4
		G['unitlimit'] = 2000
		G['movelimit'] = 15000
		G['selection_vwidth'] = 50
		G['levellimit'] = 120
		G['logrulelist'] = L_T()
		G['logrulelist']['old'] = L_T()
		G['logrulelist']['new'] = L_T()
		G['nlist'] = L_T()
		G['setupnounlists']()
		G['generatetiles']()
		G['formatobjlist']()
		G['generatefreqs']()
		G['baserulelist'] = L_T()
		G['setupbaserules']()
	G['init'] = f_init
	def f_resetlogrules(*_):  # L116
		G['logrulelist'] = L_T()
		G['logrulelist']['old'] = L_T()
		G['logrulelist']['new'] = L_T()
	G['resetlogrules'] = f_resetlogrules
	def f_setupbaserules(*_):  # L122
		L_insert(G['baserulelist'], L_T(['text', 'is', 'push']))
		L_insert(G['baserulelist'], L_T(['level', 'is', 'stop']))
		L_insert(G['baserulelist'], L_T(['cursor', 'is', 'select']))
	G['setupbaserules'] = f_setupbaserules
	def f_setupmenu(editorid=None, editor2id=None, editor3id=None, editor4id=None, selectorid=None, placerid=None, no_menu_change_=None, *_):  # L128
		G['editor'] = G['mmf']['newObject'](editorid)
		G['editor2'] = G['mmf']['newObject'](editor2id)
		G['editor3'] = G['mmf']['newObject'](editor3id)
		G['editor4'] = G['mmf']['newObject'](editor4id)
		G['editor_selector'] = G['mmf']['newObject'](selectorid)
		G['editor_placer'] = G['mmf']['newObject'](placerid)
		G['changes'] = L_T()
		G['selectionrect'] = L_T()
		G['selectionrect']['x'] = 0
		G['selectionrect']['y'] = 0
		G['selectionrect']['w'] = 0
		G['selectionrect']['h'] = 0
		G['objlistdata'] = L_T()
		G['objlistdata']['alltags'] = L_T()
		G['objlistdata']['tags'] = L_T()
		G['objlistdata']['objectreference'] = L_T()
		G['objlistdata']['tilereference'] = L_T()
		G['objlistdata']['gridreference_overlap'] = L_T()
		G['objlistdata']['gridreference_full'] = L_T()
		G['objlistdata']['search'] = ''
		no_menu_change = (_t1 if L_t(_t1 := no_menu_change_) else False)
		if (no_menu_change is False):
			G['menu'] = L_T(['intro'])
		seentags = L_T()
		L_insert(G['objlistdata']['alltags'], 'text_verb')
		L_insert(G['objlistdata']['alltags'], 'text_quality')
		L_insert(G['objlistdata']['alltags'], 'text_condition')
		L_insert(G['objlistdata']['alltags'], 'text_prefix')
		L_insert(G['objlistdata']['alltags'], 'common')
		L_insert(G['objlistdata']['alltags'], 'movement')
		L_insert(G['objlistdata']['alltags'], 'animal')
		L_insert(G['objlistdata']['alltags'], 'obstacle')
		L_insert(G['objlistdata']['alltags'], 'floor')
		L_insert(G['objlistdata']['alltags'], 'danger')
		L_insert(G['objlistdata']['alltags'], 'plant')
		L_insert(G['objlistdata']['alltags'], 'item')
		for i, v in L_ipairs(G['objlistdata']['alltags']):
			seentags[v] = 1
		for i_2, v_2 in L_ipairs(G['editor_objlist']):
			if (v_2['tags'] is not None):
				for a, b in L_ipairs(v_2['tags']):
					if (seentags[b] is None):
						seentags[b] = 1
						L_insert(G['objlistdata']['alltags'], b)
	G['setupmenu'] = f_setupmenu
	def f_generatetiles(*_):  # L188
		G['tilereference'] = L_T()
		G['tilereference']['0,0'] = ''
		for i_3, tile in L_pairs(G['tileslist']):
			tiledata = tile['tile']
			x = tiledata[1]
			y = tiledata[2]
			id_ = L_concat(L_tostring(x), ',', L_tostring(y))
			G['tilereference'][id_] = i_3
			if ((tile['type'] == 3) or (tile['type'] == 7)):
				G['conditions'][i_3] = L_T()
				conddata = G['conditions'][i_3]
				conddata['arguments'] = False
				if (tile['type'] == 7):
					conddata['arguments'] = True
					conddata['argtype'] = L_T()
					argtype = (_t1 if L_t(_t1 := tile['argtype']) else L_T([0]))
					for a_2, b_2 in L_ipairs(argtype):
						L_insert(conddata['argtype'], b_2)
					if (tile['argextra'] is not None):
						conddata['argextra'] = L_T()
						for a_3, b_3 in L_ipairs(tile['argextra']):
							L_insert(conddata['argextra'], b_3)
	G['generatetiles'] = f_generatetiles
	def f_worldinit(*_):  # L229
		G['unitreference'] = L_T()
		for i_4, tile_2 in L_pairs(G['tileslist']):
			if ((tile_2['does_not_exist'] is None) or (tile_2['does_not_exist'] is False)):
				thisid = G['MF_create'](i_4)
				name = (_t1 if L_t(_t1 := tile_2['name']) else 'error')
				sprite = (_t2 if L_t(_t2 := tile_2['sprite']) else name)
				root = (_t3 if L_t(_t3 := tile_2['sprite_in_root']) else False)
				G['MF_changesprite'](thisid, sprite, root)
				G['MF_cleanremove'](thisid)
				if (name != 'error'):
					G['unitreference'][name] = i_4
		G['unitreference']['level'] = 'level'
		if (G['generaldata']['values'][G['MODE']] == 0):
			world = G['generaldata']['strings'][G['WORLD']]
			slot = G['generaldata2']['values'][G['SAVESLOT']]
			G['MF_store']('settings', 'savegame', 'world', world)
			G['MF_store']('settings', 'savegame', 'slot', L_tostring(slot))
		if L_t(G['modsinuse']):
			G['refreshfiles']()
			G['unitreference']['level'] = 'level'
	G['worldinit'] = f_worldinit
	def f_createobjectpalette(*_):  # L263
		G['objectpalette'] = L_T()
		objectids = G['MF_read']('level', 'tiles', 'changed_short')
		objids = G['MF_parsestring'](objectids)
		for i_5, v_3 in L_ipairs(objids):
			objid = L_concat('object', v_3)
			name_2 = L_first(G['getactualdata_objlist'](objid, 'name'))
			if (name_2 is not None):
				G['objectpalette'][name_2] = objid
		G['objectpalette']['level'] = 'level'
	G['createobjectpalette'] = f_createobjectpalette
	def f_loadpathgate(*_):  # L281
		if (G['generaldata']['strings'][G['WORLD']] != G['generaldata']['strings'][G['BASEWORLD']]):
			pathgate = ''
			filegate = G['MF_read']('level', 'general', 'gatepath')
			if (L_strlen(filegate) > 0):
				filegate_ = (_t1 if L_t(_t1 := G['unitreference'][filegate]) else '')
				pathgate = filegate_
			if (L_strlen(pathgate) == 0):
				linegate = (_t2 if L_t(_t2 := G['unitreference']['line']) else '')
				pathgate = linegate
			if (L_strlen(pathgate) == 0):
				for i_6, v_4 in L_pairs(G['unitreference']):
					pathgate = v_4
					break
			G['editor']['strings'][G['PATHOBJECT']] = pathgate
		else:
			G['editor']['strings'][G['PATHOBJECT']] = 'object117'
	G['loadpathgate'] = f_loadpathgate
	def f_loadtile(x_2=None, y_2=None, *_):  # L313
		id__2 = L_concat(L_tostring(x_2), ',', L_tostring(y_2))
		if (G['tilereference'][id__2] is not None):
			return G['tilereference'][id__2]
		else:
			L_noop(L_concat("Couldn't find object with tile id: ", L_tostring(x_2), ', ', L_tostring(y_2)))
			return 'error'
	G['loadtile'] = f_loadtile
	def f_loadtile_oldlevel(x_3=None, y_3=None, *_):  # L324
		id__3 = L_concat(L_tostring(x_3), ',', L_tostring(y_3))
		G['oldtiles'] = L_T([], {'0,0': 'wall', '1,0': 'wall', '2,0': 'baba', '3,0': 'keke', '4,0': 'rock', '5,0': 'text_grass', '6,0': 'tile', '7,0': 'text_and', '8,0': 'text_hide', '9,0': 'text_follow', '10,0': 'text_float', '0,1': 'wall', '1,1': 'wall', '2,1': 'lava', '3,1': 'water', '4,1': 'wall', '5,1': 'text_empty', '6,1': 'text_tile', '7,1': 'text_weak', '8,1': 'text_back', '9,1': 'cloud', '10,1': 'pillar', '0,2': 'text_baba', '1,2': 'text_keke', '2,2': 'text_flag', '3,2': 'flag', '4,2': 'ice', '5,2': 'text_shift', '6,2': 'statue', '7,2': 'text_all', '8,2': 'text_right', '9,2': 'text_cloud', '10,2': 'text_pillar', '0,3': 'text_rock', '1,3': 'text_lava', '2,3': 'text_wall', '3,3': 'text_ice', '4,3': 'text_is', '5,3': 'text_statue', '6,3': 'text_more', '7,3': 'text_safe', '8,3': 'text_up', '9,3': 'star', '10,3': 'text_rose', '0,4': 'text_water', '1,4': 'text_win', '2,4': 'text_push', '3,4': 'text_stop', '4,4': 'text_move', '5,4': 'text_best', '6,4': 'text_tele', '7,4': 'hand', '8,4': 'text_left', '9,4': 'text_star', '10,4': 'text_red', '0,5': 'text_melt', '1,5': 'text_hot', '2,5': 'text_you', '3,5': 'text_not', '4,5': 'text_sink', '5,5': 'love', '6,5': 'door', '7,5': 'text_hand', '8,5': 'text_down', '9,5': 'dust', '10,5': 'text_violet', '0,6': 'text_stick', '1,6': 'text_defeat', '2,6': 'skull', '3,6': 'grass', '4,6': 'text_skull', '5,6': 'text_love', '6,6': 'text_door', '7,6': 'text_text', '8,6': 'text_restart', '9,6': 'text_dust', '10,6': 'text_blue', '0,7': 'key', '1,7': 'text_key', '2,7': 'text_open', '3,7': 'text_shut', '4,7': 'text_has', '5,7': 'box', '6,7': 'text_box', '7,7': 'belt', '8,7': 'text_make', '9,7': 'text_fall', '10,7': 'violet', '0,8': 'text_belt', '1,8': 'me', '2,8': 'text_me', '3,8': 'orb', '4,8': 'text_orb', '5,8': 'text_swap', '6,8': 'text_pull', '7,8': 'text_on', '8,8': 'text_star', '9,8': 'moon', '10,8': 'rose', '0,9': 'text_moon', '1,9': 'star', '2,9': 'moon', '3,9': 'hedge', '4,9': 'text_hedge', '5,9': 'text_level', '6,9': 'text_orb', '7,9': 'orb', '8,9': 'text_bonus', '9,9': 'text_moon', '10,9': 'text_group', '0,10': 'brick', '1,10': 'text_brick', '2,10': 'text_wonder', '3,10': 'text_eat', '4,10': 'text_statue', '5,10': 'statue'})
		if (G['oldtiles'][id__3] is not None):
			corresponding = G['oldtiles'][id__3]
			for a_4, b_4 in L_pairs(G['tileslist']):
				if (b_4['name'] == corresponding):
					return a_4
		else:
			G['MF_alert']('Trying to load mystery object')
		if (G['tilereference'][id__3] is not None):
			return G['tilereference'][id__3]
		else:
			L_noop(L_concat("Couldn't find object with tile id: ", L_tostring(x_3), ', ', L_tostring(y_3)))
			return 'error'
	G['loadtile_oldlevel'] = f_loadtile_oldlevel
	def f_firstlevel(*_):  # L466
		world_2 = G['generaldata']['strings'][G['WORLD']]
		level = G['generaldata']['strings'][G['CURRLEVEL']]
		G['generaldata']['strings'][G['CURRLEVEL']] = ''
		if (L_strlen(level) == 0):
			flevel = G['MF_read']('world', 'general', 'firstlevel')
			slevel = G['MF_read']('world', 'general', 'start')
			fstatus = (_t1 if L_t(_t1 := L_tonumber(G['MF_read']('save', world_2, flevel))) else 0)
			intro = (_t2 if L_t(_t2 := L_tonumber(G['MF_read']('save', world_2, 'intro'))) else 0)
			if (L_strlen(flevel) > 0):
				if ((fstatus != 3) or (L_strlen(slevel) == 0)):
					G['sublevel'](slevel, 0, 0)
					G['sublevel'](flevel, 0, 0)
					G['generaldata']['strings'][G['CURRLEVEL']] = flevel
					G['generaldata']['strings'][G['PARENT']] = slevel
					if ((world_2 == G['generaldata']['strings'][G['BASEWORLD']]) and (intro == 0)):
						G['MF_intro']()
				else:
					G['generaldata']['strings'][G['CURRLEVEL']] = slevel
			elif (L_strlen(slevel) > 0):
				G['generaldata']['strings'][G['CURRLEVEL']] = slevel
				G['sublevel'](slevel, 0, 0)
	G['firstlevel'] = f_firstlevel
	def f_loadcustomobjects(data=None, *_):  # L500
		cobjects = G['MF_parsestring'](data)
		G['customobjects'] = L_T()
		target = ''
		if (L_len(cobjects) > 0):
			for i_7, v_5 in L_ipairs(cobjects):
				if (L_sub(v_5, 1, 4) == 'OBJ-'):
					target = L_sub(v_5, 5)
					G['customobjects'][target] = L_T()
				else:
					if (L_strlen(target) > 0):
						L_insert(G['customobjects'][target], v_5)
					else:
						G['MF_alert']("customobject's target was an empty string!")
	G['loadcustomobjects'] = f_loadcustomobjects
	def f_createcobjectlist(*_):  # L522
		G['cobjects'] = L_T()
		for a_5, b_5 in L_pairs(G['customobjects']):
			for c, d in L_ipairs(b_5):
				G['cobjects'][d] = 1
		G['cobjects'][1] = 'SET'
	G['createcobjectlist'] = f_createcobjectlist
