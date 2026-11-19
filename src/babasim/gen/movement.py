"""Generated from movement.lua by tools/lua2py.py. Do not edit."""
from babasim.luart import *  # noqa: F403


def load(G):
	def f_movecommand(ox=None, oy=None, dir_=None, playerid_=None, dir_2=None, no3d_=None, *_):  # L1
		G['statusblock'](None, None, True)
		G['movelist'] = L_T()
		debug_moves = 0
		take = 1
		takecount = 8
		finaltake = False
		no3d = (_t1 if L_t(_t1 := no3d_) else False)
		playerid = (_t2 if L_t(_t2 := playerid_) else 1)
		still_moving = L_T()
		levelpush = (-1)
		levelpull = (-1)
		levelmovedir = dir_
		levelmove = L_T()
		levelmove2 = L_T()
		if (playerid == 1):
			levelmove = G['findfeature']('level', 'is', 'you')
		elif (playerid == 2):
			levelmove = G['findfeature']('level', 'is', 'you2')
			if (levelmove is None):
				levelmove = G['findfeature']('level', 'is', 'you')
		elif (playerid == 3):
			levelmove = (_t3 if L_t(_t3 := G['findfeature']('level', 'is', 'you')) else L_T())
			levelmove2 = G['findfeature']('level', 'is', 'you2')
			if ((L_len(levelmove) > 0) and (dir_ is not None)):
				levelmovedir = dir_
			elif ((levelmove2 is not None) and (dir_ is not None)):
				levelmovedir = dir_
			elif (dir_2 is not None):
				levelmovedir = dir_2
			if (levelmove2 is not None):
				for i, v in L_ipairs(levelmove2):
					L_insert(levelmove, v)
			if (L_len(levelmove) == 0):
				levelmove = None
		if (levelmove is not None):
			valid = False
			for i_2, v_2 in L_ipairs(levelmove):
				if ((valid is False) and L_t(G['testcond'](v_2[2], 1))):
					valid = True
			if (G['featureindex']['reverse'] is not None):
				levelmovedir = L_first(G['reversecheck'](1, levelmovedir))
			if L_t(G['cantmove']('level', 1, levelmovedir)):
				valid = False
			if (valid is not None and valid is not False):
				ndrs = G['ndirs'][(levelmovedir + 1)]
				ox_2, oy_2 = ndrs[1], ndrs[2]
				if (G['isstill'](1, None, None, levelmovedir) is False):
					G['addundo'](L_T(['levelupdate', G['Xoffset'], G['Yoffset'], (G['Xoffset'] + (ox_2 * G['tilesize'])), (G['Yoffset'] + (oy_2 * G['tilesize'])), G['mapdir'], levelmovedir]))
					G['MF_scrollroom']((ox_2 * G['tilesize']), (oy_2 * G['tilesize']))
				else:
					G['addundo'](L_T(['levelupdate', G['Xoffset'], G['Yoffset'], G['Xoffset'], G['Yoffset'], G['mapdir'], levelmovedir]))
				if (levelmovedir != 4):
					G['mapdir'] = levelmovedir
				G['updateundo'] = True
		while ((take <= takecount) or (finaltake is not None and finaltake is not False)):
			moving_units = L_T()
			been_seen = L_T()
			skiptake = False
			if (finaltake is False):
				if (take == 1):
					players = L_T()
					players2 = L_T()
					players3 = L_T()
					empty = L_T()
					empty2 = L_T()
					empty3 = L_T()
					if (playerid == 1):
						players, empty = L_adjust((*G['findallfeature'](None, 'is', 'you'),), 2)
					elif (playerid == 2):
						players, empty = L_adjust((*G['findallfeature'](None, 'is', 'you2'),), 2)
						if (L_len(players) == 0):
							players, empty = L_adjust((*G['findallfeature'](None, 'is', 'you'),), 2)
					elif (playerid == 3):
						players, empty = L_adjust((*G['findallfeature'](None, 'is', 'you'),), 2)
						players2, empty2 = L_adjust((*G['findallfeature'](None, 'is', 'you2'),), 2)
						for i_3, v_3 in L_ipairs(players2):
							L_insert(players, v_3)
						for i_4, v_4 in L_ipairs(empty2):
							L_insert(empty, v_4)
					fdir = 4
					for i_5, v_5 in L_ipairs(players):
						sleeping = False
						fdir = dir_
						if (playerid == 3):
							if (i_5 > (L_len(players) - L_len(players2))):
								fdir = dir_2
						if (v_5 != 2):
							unit = G['mmf']['newObject'](v_5)
							unitname = G['getname'](unit)
							sleep = G['hasfeature'](unitname, 'is', 'sleep', v_5)
							still = G['cantmove'](unitname, v_5, fdir)
							if (sleep is not None):
								sleeping = True
							elif (still is not None and still is not False):
								sleeping = True
								if (fdir != 4):
									G['updatedir'](v_5, fdir)
							else:
								if (fdir != 4):
									G['updatedir'](v_5, fdir)
						else:
							thisempty = empty[i_5]
							for a, b in L_pairs(thisempty):
								x = (a % G['roomsizex'])
								y = L_floor(L_div(a, G['roomsizex']))
								sleep_2 = G['hasfeature']('empty', 'is', 'sleep', 2, x, y)
								still_2 = G['cantmove']('empty', 2, fdir, x, y)
								if ((sleep_2 is not None) or (still_2 is not None and still_2 is not False)):
									thisempty[a] = None
						if ((sleeping is False) and (fdir != 4)):
							if (been_seen[v_5] is None):
								x_2, y_2 = (-1), (-1)
								if (v_5 != 2):
									unit_2 = G['mmf']['newObject'](v_5)
									x_2, y_2 = unit_2['values'][G['XPOS']], unit_2['values'][G['YPOS']]
									L_insert(moving_units, L_T([], {'unitid': v_5, 'reason': 'you', 'state': 0, 'moves': 1, 'dir': fdir, 'xpos': x_2, 'ypos': y_2}))
									been_seen[v_5] = L_len(moving_units)
								else:
									thisempty_2 = empty[i_5]
									for a_2, b_2 in L_pairs(thisempty_2):
										x_2 = (a_2 % G['roomsizex'])
										y_2 = L_floor(L_div(a_2, G['roomsizex']))
										L_insert(moving_units, L_T([], {'unitid': 2, 'reason': 'you', 'state': 0, 'moves': 1, 'dir': fdir, 'xpos': x_2, 'ypos': y_2}))
										been_seen[v_5] = L_len(moving_units)
							else:
								id_ = been_seen[v_5]
								this = moving_units[id_]
					fdir = 4
					if ((((G['featureindex']['3d'] is not None) and (G['spritedata']['values'][G['CAMTARGET']] != 0)) and (G['spritedata']['values'][G['CAMTARGET']] != 0.5)) and (no3d is False)):
						sleeping_2 = False
						domove = False
						turndir = 0
						ox_3, oy_3 = 0, 0
						v_6 = (_t4 if L_t(_t4 := G['MF_getfixed'](G['spritedata']['values'][G['CAMTARGET']])) else 0)
						if ((v_6 != 2) and (v_6 != 0)):
							unit_3 = G['mmf']['newObject'](v_6)
							udir = unit_3['values'][G['DIR']]
							ndrs_2 = G['ndirs'][(udir + 1)]
							ox_3, oy_3 = ndrs_2[1], ndrs_2[2]
							if (dir_ == 1):
								domove = True
							elif (dir_ == 0):
								turndir = (-1)
							elif (dir_ == 2):
								turndir = 1
							fdir = (((udir + turndir) + 4) % 4)
							unitname_2 = G['getname'](unit_3)
							sleep_3 = G['hasfeature'](unitname_2, 'is', 'sleep', v_6)
							still_3 = G['cantmove'](unitname_2, v_6, fdir)
							if (sleep_3 is not None):
								sleeping_2 = True
							elif (still_3 is not None and still_3 is not False):
								sleeping_2 = True
								if (fdir != 4):
									G['updatedir'](v_6, fdir)
							else:
								if (fdir != 4):
									G['updatedir'](v_6, fdir)
							if (((sleeping_2 is False) and (fdir != 4)) and (domove is not None and domove is not False)):
								if (been_seen[v_6] is None):
									x_3, y_3 = (-1), (-1)
									if (v_6 != 2):
										unit_4 = G['mmf']['newObject'](v_6)
										x_3, y_3 = unit_4['values'][G['XPOS']], unit_4['values'][G['YPOS']]
										L_insert(moving_units, L_T([], {'unitid': v_6, 'reason': 'you', 'state': 0, 'moves': 1, 'dir': fdir, 'xpos': x_3, 'ypos': y_3}))
										been_seen[v_6] = L_len(moving_units)
								else:
									id__2 = been_seen[v_6]
									this_2 = moving_units[id__2]
				if (take == 2):
					movers, mempty = L_adjust((*G['findallfeature'](None, 'is', 'move'),), 2)
					moving_units, been_seen = L_adjust((*G['add_moving_units']('move', movers, moving_units, been_seen, mempty),), 2)
					amovers, aempty = L_adjust((*G['findallfeature'](None, 'is', 'auto'),), 2)
					moving_units, been_seen = L_adjust((*G['add_moving_units']('auto', amovers, moving_units, been_seen, aempty),), 2)
					chillers, cempty = L_adjust((*G['findallfeature'](None, 'is', 'chill'),), 2)
					moving_units, been_seen = L_adjust((*G['add_moving_units']('chill', chillers, moving_units, been_seen, cempty),), 2)
				elif (take == 3):
					nudges1, nempty1 = L_adjust((*G['findallfeature'](None, 'is', 'nudgeright'),), 2)
					moving_units, been_seen = L_adjust((*G['add_moving_units']('nudgeright', nudges1, moving_units, been_seen, nempty1),), 2)
					if (L_len(moving_units) == 0):
						skiptake = True
				elif (take == 4):
					nudges2, nempty2 = L_adjust((*G['findallfeature'](None, 'is', 'nudgeup'),), 2)
					moving_units, been_seen = L_adjust((*G['add_moving_units']('nudgeup', nudges2, moving_units, been_seen, nempty2),), 2)
					if (L_len(moving_units) == 0):
						skiptake = True
				elif (take == 5):
					nudges3, nempty3 = L_adjust((*G['findallfeature'](None, 'is', 'nudgeleft'),), 2)
					moving_units, been_seen = L_adjust((*G['add_moving_units']('nudgeleft', nudges3, moving_units, been_seen, nempty3),), 2)
					if (L_len(moving_units) == 0):
						skiptake = True
				elif (take == 6):
					nudges4, nempty4 = L_adjust((*G['findallfeature'](None, 'is', 'nudgedown'),), 2)
					moving_units, been_seen = L_adjust((*G['add_moving_units']('nudgedown', nudges4, moving_units, been_seen, nempty4),), 2)
					if (L_len(moving_units) == 0):
						skiptake = True
				elif (take == 7):
					fears = G['getunitverbtargets']('fear')
					for i_6, v_7 in L_ipairs(fears):
						fearname = v_7[1]
						fearlist = v_7[2]
						for a_3, b_3 in L_ipairs(fearlist):
							sleeping_3 = False
							uid = b_3[1]
							feartargets = b_3[2]
							valid_2, feardir = False, 4
							amount = L_len(feartargets)
							if (fearname != 'empty'):
								valid_2, feardir, amount = L_adjust((*G['findfears'](uid, feartargets),), 3)
							else:
								x_4 = L_floor((uid % G['roomsizex']))
								y_4 = L_floor(L_div(uid, G['roomsizex']))
								valid_2, feardir = L_adjust((*G['findfears'](2, feartargets, x_4, y_4),), 2)
							if ((valid_2 is not None and valid_2 is not False) and (amount > 0)):
								if (fearname != 'empty'):
									unit_5 = G['mmf']['newObject'](uid)
									unitname_3 = G['getname'](unit_5)
									sleep_4 = G['hasfeature'](unitname_3, 'is', 'sleep', uid)
									still_4 = G['cantmove'](unitname_3, uid, feardir)
									if (sleep_4 is not None):
										sleeping_3 = True
									elif (still_4 is not None and still_4 is not False):
										sleeping_3 = True
										G['updatedir'](uid, feardir)
									else:
										G['updatedir'](uid, feardir)
								else:
									x_5 = (uid % G['roomsizex'])
									y_5 = L_floor(L_div(uid, G['roomsizex']))
									sleep_5 = G['hasfeature']('empty', 'is', 'sleep', 2, x_5, y_5)
									still_5 = G['cantmove']('empty', 2, feardir, x_5, y_5)
									if ((sleep_5 is not None) or (still_5 is not None and still_5 is not False)):
										sleeping_3 = True
								bsid = uid
								if (fearname == 'empty'):
									bsid = (uid + 200)
								if (sleeping_3 is False):
									if (been_seen[bsid] is None):
										x_6, y_6 = (-1), (-1)
										if (fearname != 'empty'):
											unit_6 = G['mmf']['newObject'](uid)
											x_6, y_6 = unit_6['values'][G['XPOS']], unit_6['values'][G['YPOS']]
											L_insert(moving_units, L_T([], {'unitid': uid, 'reason': 'fear', 'state': 0, 'moves': amount, 'dir': feardir, 'xpos': x_6, 'ypos': y_6}))
											been_seen[bsid] = L_len(moving_units)
										else:
											x_6 = (uid % G['roomsizex'])
											y_6 = L_floor(L_div(uid, G['roomsizex']))
											L_insert(moving_units, L_T([], {'unitid': 2, 'reason': 'fear', 'state': 0, 'moves': amount, 'dir': feardir, 'xpos': x_6, 'ypos': y_6}))
											been_seen[bsid] = L_len(moving_units)
									else:
										id__3 = been_seen[bsid]
										this_3 = moving_units[id__3]
										this_3['moves'] = (this_3['moves'] + 1)
				elif (take == 8):
					shifts = L_first(G['findallfeature'](None, 'is', 'shift', True))
					for i_7, v_8 in L_ipairs(shifts):
						if (v_8 != 2):
							affected = L_T()
							unit_7 = G['mmf']['newObject'](v_8)
							x_7, y_7 = unit_7['values'][G['XPOS']], unit_7['values'][G['YPOS']]
							tileid = (x_7 + (y_7 * G['roomsizex']))
							if (G['unitmap'][tileid] is not None):
								if (L_len(G['unitmap'][tileid]) > 1):
									for a_4, b_4 in L_ipairs(G['unitmap'][tileid]):
										if ((b_4 != v_8) and L_t(G['floating'](b_4, v_8, x_7, y_7))):
											if (G['isstill_or_locked'](b_4, x_7, y_7, unit_7['values'][G['DIR']]) is False):
												if (been_seen[b_4] is None):
													L_insert(moving_units, L_T([], {'unitid': b_4, 'reason': 'shift', 'state': 0, 'moves': 1, 'dir': unit_7['values'][G['DIR']], 'xpos': x_7, 'ypos': y_7}))
													been_seen[b_4] = L_len(moving_units)
												else:
													id__4 = been_seen[b_4]
													this_4 = moving_units[id__4]
													this_4['moves'] = (this_4['moves'] + 1)
					levelshift = G['findfeature']('level', 'is', 'shift')
					if (levelshift is not None):
						leveldir = G['mapdir']
						valid_3 = False
						for a_5, b_5 in L_ipairs(levelshift):
							if ((valid_3 is False) and L_t(G['testcond'](b_5[2], 1))):
								valid_3 = True
						if (valid_3 is not None and valid_3 is not False):
							for a_6, unit_8 in L_ipairs(G['units']):
								x_8, y_8 = unit_8['values'][G['XPOS']], unit_8['values'][G['YPOS']]
								if L_t(G['floating_level'](unit_8['fixed'])):
									G['updatedir'](unit_8['fixed'], leveldir)
									if ((G['isstill_or_locked'](unit_8['fixed'], x_8, y_8, leveldir) is False) and (G['issleep'](unit_8['fixed'], x_8, y_8) is False)):
										L_insert(moving_units, L_T([], {'unitid': unit_8['fixed'], 'reason': 'shift', 'state': 0, 'moves': 1, 'dir': unit_8['values'][G['DIR']], 'xpos': x_8, 'ypos': y_8}))
			else:
				for i_8, data in L_ipairs(still_moving):
					if (data['unitid'] != 2):
						unit_9 = G['mmf']['newObject'](data['unitid'])
						L_insert(moving_units, L_T([], {'unitid': data['unitid'], 'reason': data['reason'], 'state': data['state'], 'moves': data['moves'], 'dir': unit_9['values'][G['DIR']], 'xpos': unit_9['values'][G['XPOS']], 'ypos': unit_9['values'][G['YPOS']]}))
					else:
						L_insert(moving_units, L_T([], {'unitid': data['unitid'], 'reason': data['reason'], 'state': data['state'], 'moves': data['moves'], 'dir': data['dir'], 'xpos': data['xpos'], 'ypos': data['ypos']}))
				still_moving = L_T()
			unitcount = L_len(moving_units)
			done = False
			state = 0
			if (skiptake is not None and skiptake is not False):
				done = True
			G['do_mod_hook']('movement_take', L_T([moving_units, take]))
			while (((done is False) and (skiptake is False)) and (debug_moves < G['movelimit'])):
				smallest_state = 99
				delete_moving_units = L_T()
				for i_9, data_2 in L_ipairs(moving_units):
					solved = False
					skipthis = False
					smallest_state = L_min(smallest_state, data_2['state'])
					if (data_2['unitid'] == 0):
						solved = True
					if (((data_2['state'] == state) and (data_2['moves'] > 0)) and (data_2['unitid'] != 0)):
						unit_10 = L_T()
						dir__2, name = 4, ''
						x_9, y_9 = data_2['xpos'], data_2['ypos']
						holder = 0
						if (data_2['unitid'] != 2):
							unit_10 = G['mmf']['newObject'](data_2['unitid'])
							dir__2 = unit_10['values'][G['DIR']]
							name = G['getname'](unit_10)
							x_9, y_9 = unit_10['values'][G['XPOS']], unit_10['values'][G['YPOS']]
							holder = (_t5 if L_t(_t5 := unit_10['holder']) else 0)
						else:
							dir__2 = data_2['dir']
							name = 'empty'
						debug_moves = (debug_moves + 1)
						if (((x_9 != (-1)) and (y_9 != (-1))) and (holder == 0)):
							result = (-1)
							solved = False
							if (state == 0):
								if ((data_2['unitid'] == 2) and (((data_2['reason'] == 'move') and (dir__2 == 4)) or (data_2['reason'] == 'chill'))):
									data_2['dir'] = G['fixedrandom'](0, 3)
									dir__2 = data_2['dir']
									if L_t(G['cantmove'](name, data_2['unitid'], dir__2, x_9, y_9)):
										skipthis = True
							elif (state == 3):
								if ((data_2['reason'] == 'move') or (data_2['reason'] == 'chill')):
									newdir_ = G['rotate'](dir__2)
									if (G['cantmove'](name, data_2['unitid'], newdir_, x_9, y_9) is False):
										dir__2 = newdir_
									if ((data_2['unitid'] != 2) and (unit_10['flags'][G['DEAD']] is False)):
										G['updatedir'](data_2['unitid'], newdir_)
										if L_t(G['cantmove'](name, data_2['unitid'], newdir_, x_9, y_9)):
											skipthis = True
							if (((state == 0) and (data_2['reason'] == 'shift')) and (data_2['unitid'] != 2)):
								G['updatedir'](data_2['unitid'], data_2['dir'])
								dir__2 = data_2['dir']
							if (dir__2 == 4):
								dir__2 = G['fixedrandom'](0, 3)
							olddir = dir__2
							returnolddir = False
							if (data_2['reason'] == 'nudgeright'):
								dir__2 = 0
								returnolddir = True
							elif (data_2['reason'] == 'nudgeup'):
								dir__2 = 1
								returnolddir = True
							elif (data_2['reason'] == 'nudgeleft'):
								dir__2 = 2
								returnolddir = True
							elif (data_2['reason'] == 'nudgedown'):
								dir__2 = 3
								returnolddir = True
							if (G['featureindex']['reverse'] is not None):
								revdir = L_first(G['reversecheck'](data_2['unitid'], dir__2, x_9, y_9))
								if (revdir != dir__2):
									dir__2 = revdir
									returnolddir = True
							newdir = dir__2
							ndrs_3 = G['ndirs'][(dir__2 + 1)]
							if (ndrs_3 is None):
								G['MF_alert'](L_concat('dir is invalid: ', L_tostring(dir__2), ', ', L_tostring(name)))
							ox_4, oy_4 = ndrs_3[1], ndrs_3[2]
							pushobslist = L_T()
							obslist, allobs, specials = L_adjust((*G['check'](data_2['unitid'], x_9, y_9, dir__2, False, data_2['reason']),), 3)
							pullobs, pullallobs, pullspecials = L_adjust((*G['check'](data_2['unitid'], x_9, y_9, dir__2, True, data_2['reason']),), 3)
							if (returnolddir is not None and returnolddir is not False):
								dir__2 = olddir
							swap = G['hasfeature'](name, 'is', 'swap', data_2['unitid'], x_9, y_9)
							still_6 = G['cantmove'](name, data_2['unitid'], newdir, x_9, y_9)
							if (returnolddir is not None and returnolddir is not False):
								dir__2 = newdir
							for c, obs in L_pairs(obslist):
								if (solved is False):
									if (obs == 0):
										if (state == 0):
											result = L_max(result, 0)
										else:
											result = L_max(result, 0)
									elif (obs == (-1)):
										result = L_max(result, 2)
										levelpush_ = G['findfeature']('level', 'is', 'push')
										if (levelpush_ is not None):
											for e, f in L_ipairs(levelpush_):
												if L_t(G['testcond'](f[2], 1)):
													levelpush = dir__2
									else:
										if ((swap is None) or (still_6 is not None and still_6 is not False)):
											if (L_len(allobs) == 0):
												obs = 0
											if (obs == 1):
												thisobs = allobs[c]
												solid = True
												for f_2, g in L_pairs(specials):
													if ((g[1] == thisobs) and (g[2] == 'weak')):
														solid = False
														obs = 0
														result = L_max(result, 0)
												if (solid is not None and solid is not False):
													if (state < 2):
														data_2['state'] = L_max(data_2['state'], 2)
														result = L_max(result, 2)
													else:
														result = L_max(result, 2)
											else:
												if (state < 1):
													data_2['state'] = L_max(data_2['state'], 1)
													result = L_max(result, 1)
												else:
													L_insert(pushobslist, obs)
													result = L_max(result, 1)
										else:
											result = L_max(result, 0)
							if (skipthis is False):
								result_check = False
								while ((result_check is False) and (solved is False)):
									if (result == 0):
										if (state > 0):
											for j, jdata in L_pairs(moving_units):
												if ((jdata['state'] >= 2) and (jdata['state'] != 10)):
													jdata['state'] = 0
										L_insert(G['movelist'], L_T([data_2['unitid'], ox_4, oy_4, olddir, specials, x_9, y_9]))
										if ((data_2['unitid'] == 2) and (data_2['moves'] > 1)):
											data_2['xpos'] = (x_9 + ox_4)
											data_2['ypos'] = (y_9 + oy_4)
											data_2['dir'] = dir__2
										swapped = L_T()
										if ((swap is not None) and (still_6 is False)):
											for a_7, b_6 in L_ipairs(allobs):
												if (((b_6 != (-1)) and (b_6 != 2)) and (b_6 != 0)):
													swapunit = G['mmf']['newObject'](b_6)
													swapname = G['getname'](swapunit)
													obsstill = G['hasfeature'](swapname, 'is', 'still', b_6, (x_9 + ox_4), (y_9 + oy_4))
													if (obsstill is None):
														G['addaction'](b_6, L_T(['update', x_9, y_9, None]))
														swapped[b_6] = 1
										swaps = G['findfeatureat'](None, 'is', 'swap', (x_9 + ox_4), (y_9 + oy_4), L_T(['still']))
										if (swaps is not None):
											for a_8, b_7 in L_ipairs(swaps):
												if ((swapped[b_7] is None) and (b_7 != 2)):
													G['addaction'](b_7, L_T(['update', x_9, y_9, None]))
										finalpullobs = L_T()
										for c_2, pobs in L_ipairs(pullobs):
											if ((pobs < (-1)) or (pobs > 1)):
												paobs = pullallobs[c_2]
												hm = 0
												if (paobs != 2):
													hm = G['trypush'](paobs, ox_4, oy_4, dir__2, True, x_9, y_9, data_2['reason'], data_2['unitid'])
												else:
													hm = G['trypush'](paobs, ox_4, oy_4, dir__2, True, (x_9 - ox_4), (y_9 - oy_4), data_2['reason'], data_2['unitid'])
												if (hm == 0):
													L_insert(finalpullobs, paobs)
											elif (pobs == (-1)):
												levelpull_ = G['findfeature']('level', 'is', 'pull')
												if (levelpull_ is not None):
													for e_2, f_3 in L_ipairs(levelpull_):
														if L_t(G['testcond'](f_3[2], 1)):
															levelpull = dir__2
										for c_3, pobs_2 in L_ipairs(finalpullobs):
											G['pushedunits'] = L_T()
											if (pobs_2 != 2):
												G['dopush'](pobs_2, ox_4, oy_4, dir__2, True, x_9, y_9, data_2['reason'], data_2['unitid'])
											else:
												G['dopush'](pobs_2, ox_4, oy_4, dir__2, True, (x_9 - ox_4), (y_9 - oy_4), data_2['reason'], data_2['unitid'])
										solved = True
									elif (result == 1):
										if (state < 1):
											data_2['state'] = L_max(data_2['state'], 1)
											result_check = True
										else:
											finalpushobs = L_T()
											for c_4, pushobs in L_ipairs(pushobslist):
												hm_2 = 0
												if (pushobs != 2):
													hm_2 = G['trypush'](pushobs, ox_4, oy_4, dir__2, False, x_9, y_9, data_2['reason'])
												else:
													hm_2 = G['trypush'](pushobs, ox_4, oy_4, dir__2, False, (x_9 + ox_4), (y_9 + oy_4), data_2['reason'])
												if (hm_2 == 0):
													L_insert(finalpushobs, pushobs)
												elif ((hm_2 == 1) or (hm_2 == (-1))):
													result = L_max(result, 2)
												else:
													G['MF_alert']('HOO HAH')
													return None
											if (result == 1):
												for c_5, pushobs_2 in L_ipairs(finalpushobs):
													G['pushedunits'] = L_T()
													if (pushobs_2 != 2):
														G['dopush'](pushobs_2, ox_4, oy_4, dir__2, False, x_9, y_9, data_2['reason'])
													else:
														G['dopush'](pushobs_2, ox_4, oy_4, dir__2, False, (x_9 + ox_4), (y_9 + oy_4), data_2['reason'])
												result = 0
									elif (result == 2):
										if (state < 2):
											data_2['state'] = L_max(data_2['state'], 2)
											result_check = True
										else:
											if (state < 3):
												data_2['state'] = L_max(data_2['state'], 3)
												result_check = True
											else:
												if (((data_2['reason'] == 'move') or (data_2['reason'] == 'chill')) and (state < 4)):
													data_2['state'] = L_max(data_2['state'], 4)
													result_check = True
												else:
													weak = G['hasfeature'](name, 'is', 'weak', data_2['unitid'], x_9, y_9)
													if ((weak is not None) and (G['issafe'](data_2['unitid'], x_9, y_9) is False)):
														G['delete'](data_2['unitid'], x_9, y_9)
														G['generaldata']['values'][G['SHAKE']] = 3
														pmult, sound = L_adjust((*G['checkeffecthistory']('weak'),), 2)
														G['MF_particles']('destroy', x_9, y_9, (5 * pmult), 0, 3, 1, 1)
														G['setsoundname']('removal', 1, sound)
														data_2['moves'] = 1
													solved = True
									else:
										result_check = True
							else:
								solved = True
						else:
							solved = True
					if (solved is not None and solved is not False):
						data_2['moves'] = (data_2['moves'] - 1)
						if (state > 0):
							data_2['state'] = 10
						if (data_2['moves'] == 0):
							L_insert(delete_moving_units, i_9)
						else:
							L_insert(still_moving, L_T([], {'unitid': data_2['unitid'], 'reason': data_2['reason'], 'state': data_2['state'], 'moves': data_2['moves'], 'dir': data_2['dir'], 'xpos': data_2['xpos'], 'ypos': data_2['ypos']}))
							L_insert(delete_moving_units, i_9)
				deloffset = 0
				for i_10, v_9 in L_ipairs(delete_moving_units):
					todel = (v_9 - deloffset)
					L_remove(moving_units, todel)
					deloffset = (deloffset + 1)
				if (L_len(G['movelist']) > 0):
					for i_11, data_3 in L_ipairs(G['movelist']):
						G['move'](data_3[1], data_3[2], data_3[3], data_3[4], data_3[5], None, None, data_3[6], data_3[7])
				G['movelist'] = L_T()
				if (smallest_state > state):
					state = (state + 1)
				else:
					state = smallest_state
				if (L_len(moving_units) == 0):
					G['doupdate']()
					done = True
				else:
					G['movemap'] = L_T()
			if (debug_moves >= G['movelimit']):
				G['HACK_INFINITY'] = 200
				G['destroylevel']('toocomplex')
				return None
			if (L_len(still_moving) > 0):
				finaltake = True
				moving_units = L_T()
			else:
				finaltake = False
			if (finaltake is False):
				take = (take + 1)
		if (levelpush >= 0):
			ndrs_4 = G['ndirs'][(levelpush + 1)]
			ox_5, oy_5 = ndrs_4[1], ndrs_4[2]
			G['addundo'](L_T(['levelupdate', G['Xoffset'], G['Yoffset'], (G['Xoffset'] + (ox_5 * G['tilesize'])), (G['Yoffset'] + (oy_5 * G['tilesize'])), G['mapdir'], levelpush]))
			G['mapdir'] = levelpush
			G['MF_scrollroom']((ox_5 * G['tilesize']), (oy_5 * G['tilesize']))
			G['updateundo'] = True
		if (levelpull >= 0):
			ndrs_5 = G['ndirs'][(levelpull + 1)]
			ox_6, oy_6 = ndrs_5[1], ndrs_5[2]
			G['addundo'](L_T(['levelupdate', G['Xoffset'], G['Yoffset'], (G['Xoffset'] + (ox_6 * G['tilesize'])), (G['Yoffset'] + (oy_6 * G['tilesize'])), G['mapdir'], levelpull]))
			G['mapdir'] = levelpull
			G['MF_scrollroom']((ox_6 * G['tilesize']), (oy_6 * G['tilesize']))
			G['updateundo'] = True
		if (G['HACK_MOVES'] >= 10000):
			G['HACK_MOVES'] = 0
			G['HACK_INFINITY'] = 200
			G['destroylevel']('infinity')
			return None
		G['do_mod_hook']('movement_end')
		G['doupdate']()
		G['code']()
		G['conversion']()
		G['doupdate']()
		G['code']()
		G['moveblock']()
		if (dir_ is not None):
			G['mapcursor_move'](ox, oy, dir_)
		if ((L_len(G['units']) > 0) and (no3d is False)):
			vistest, vt2 = L_adjust((*G['findallfeature'](None, 'is', '3d', True),), 2)
			if ((L_len(vistest) > 0) or (L_len(vt2) > 0)):
				target = (_t6 if L_t(_t6 := vistest[1]) else G['vt'][1])
				G['visionmode'](1)
			elif (G['spritedata']['values'][G['VISION']] == 1):
				vistest2 = G['findfeature'](None, 'is', '3d')
				if (vistest2 is None):
					G['visionmode'](0)
	G['movecommand'] = f_movecommand
	def f_check(unitid=None, x_10=None, y_10=None, dir__3=None, pulling_=None, reason=None, *_):  # L950
		pulling = False
		if (pulling_ is not None):
			pulling = pulling_
		dir__4 = dir__3
		if (pulling is not None and pulling is not False):
			dir__4 = G['rotate'](dir__3)
		ndrs_6 = G['ndirs'][(dir__4 + 1)]
		ox_7, oy_7 = ndrs_6[1], ndrs_6[2]
		result_2 = L_T()
		results = L_T()
		specials_2 = L_T()
		unit_11 = L_T()
		name_2 = ''
		if (unitid != 2):
			unit_11 = G['mmf']['newObject'](unitid)
			name_2 = G['getname'](unit_11)
		else:
			name_2 = 'empty'
		lockpartner = ''
		open = G['hasfeature'](name_2, 'is', 'open', unitid, x_10, y_10)
		shut = G['hasfeature'](name_2, 'is', 'shut', unitid, x_10, y_10)
		eat = G['hasfeature'](name_2, 'eat', None, unitid, x_10, y_10)
		phantom = G['hasfeature'](name_2, 'is', 'phantom', unitid, x_10, y_10)
		if (pulling is not None and pulling is not False):
			phantom = None
		if (open is not None):
			lockpartner = 'shut'
		elif (shut is not None):
			lockpartner = 'open'
		obs_2 = G['findobstacle']((x_10 + ox_7), (y_10 + oy_7))
		if ((L_len(obs_2) > 0) and (phantom is None)):
			for i_12, id__5 in L_ipairs(obs_2):
				if (id__5 == (-1)):
					L_insert(result_2, (-1))
					L_insert(results, (-1))
				else:
					obsunit = G['mmf']['newObject'](id__5)
					obsname = G['getname'](obsunit)
					alreadymoving = G['findupdate'](id__5, 'update')
					valid_4 = True
					localresult = 0
					if (L_len(alreadymoving) > 0):
						for a_9, b_8 in L_ipairs(alreadymoving):
							nx, ny = b_8[3], b_8[4]
							if (((nx != x_10) and (ny != y_10)) and ((reason == 'shift') and (pulling is False))):
								valid_4 = False
							if (((nx == x_10) and (ny == (y_10 + (oy_7 * 2)))) or ((ny == y_10) and (nx == (x_10 + (ox_7 * 2))))):
								valid_4 = False
					if ((lockpartner != '') and (pulling is False)):
						partner = G['hasfeature'](obsname, 'is', lockpartner, id__5, (x_10 + ox_7), (y_10 + oy_7))
						if (((partner is not None) and ((G['issafe'](id__5, (x_10 + ox_7), (y_10 + oy_7)) is False) or (G['issafe'](unitid, x_10, y_10) is False))) and L_t(G['floating'](id__5, unitid, (x_10 + ox_7), (y_10 + oy_7)))):
							valid_4 = False
							L_insert(specials_2, L_T([id__5, 'lock']))
					if ((eat is not None) and (pulling is False)):
						eats = G['hasfeature'](name_2, 'eat', obsname, unitid, (x_10 + ox_7), (y_10 + oy_7))
						if (((eats is not None) and (G['issafe'](id__5, (x_10 + ox_7), (y_10 + oy_7)) is False)) and L_t(G['floating'](id__5, unitid, (x_10 + ox_7), (y_10 + oy_7)))):
							valid_4 = False
							L_insert(specials_2, L_T([id__5, 'eat']))
					weak_2 = G['hasfeature'](obsname, 'is', 'weak', id__5, (x_10 + ox_7), (y_10 + oy_7))
					if ((weak_2 is not None) and (pulling is False)):
						if ((G['issafe'](id__5, (x_10 + ox_7), (y_10 + oy_7)) is False) and L_t(G['floating'](id__5, unitid, (x_10 + ox_7), (y_10 + oy_7)))):
							L_insert(specials_2, L_T([id__5, 'weak']))
					added = False
					if (valid_4 is not None and valid_4 is not False):
						isstop = G['hasfeature'](obsname, 'is', 'stop', id__5, (x_10 + ox_7), (y_10 + oy_7))
						ispush = G['hasfeature'](obsname, 'is', 'push', id__5, (x_10 + ox_7), (y_10 + oy_7))
						ispull = G['hasfeature'](obsname, 'is', 'pull', id__5, (x_10 + ox_7), (y_10 + oy_7))
						isswap = G['hasfeature'](obsname, 'is', 'swap', id__5, (x_10 + ox_7), (y_10 + oy_7))
						isstill = G['cantmove'](obsname, id__5, dir__3, (x_10 + ox_7), (y_10 + oy_7))
						if ((ispush is not None) and (isstill is not None and isstill is not False)):
							ispush = None
							isstop = True
						if ((ispull is not None) and (isstill is not None and isstill is not False)):
							ispull = None
							isstop = True
						if ((isswap is not None) and (isstill is not None and isstill is not False)):
							isswap = None
						if (((isstop is not None) and (obsname == 'level')) and (obsunit['visible'] is False)):
							isstop = None
						if (((((isstop is not None) and (ispush is None)) and ((ispull is None) or ((ispull is not None) and (pulling is False)))) or (((ispull is not None) and (pulling is False)) and (ispush is None))) and (isswap is None)):
							if ((weak_2 is None) or ((weak_2 is not None) and (G['floating'](id__5, unitid, (x_10 + ox_7), (y_10 + oy_7)) is False))):
								L_insert(result_2, 1)
								L_insert(results, id__5)
								localresult = 1
								added = True
						if ((localresult != 1) and (localresult != (-1))):
							if (((ispush is not None) and (pulling is False)) and (isswap is None)):
								L_insert(result_2, id__5)
								L_insert(results, id__5)
								added = True
							if ((ispull is not None) and (pulling is not None and pulling is not False)):
								L_insert(result_2, id__5)
								L_insert(results, id__5)
								added = True
					if (added is False):
						L_insert(result_2, 0)
						L_insert(results, id__5)
		elif (phantom is None):
			emptystop = G['hasfeature']('empty', 'is', 'stop', 2, (x_10 + ox_7), (y_10 + oy_7))
			emptypush = G['hasfeature']('empty', 'is', 'push', 2, (x_10 + ox_7), (y_10 + oy_7))
			emptypull = G['hasfeature']('empty', 'is', 'pull', 2, (x_10 + ox_7), (y_10 + oy_7))
			emptyswap = G['hasfeature']('empty', 'is', 'swap', 2, (x_10 + ox_7), (y_10 + oy_7))
			emptystill = G['cantmove']('empty', 2, dir__4, (x_10 + ox_7), (y_10 + oy_7))
			localresult_2 = 0
			valid_5 = True
			bname = 'empty'
			if ((eat is not None) and (pulling is False)):
				eats_2 = G['hasfeature'](name_2, 'eat', 'empty', unitid, (x_10 + ox_7), (y_10 + oy_7))
				if (((eats_2 is not None) and (G['issafe'](2, (x_10 + ox_7), (y_10 + oy_7)) is False)) and L_t(G['floating'](unitid, 2, (x_10 + ox_7), (y_10 + oy_7)))):
					valid_5 = False
					L_insert(specials_2, L_T([2, 'eat']))
			if ((lockpartner != '') and (pulling is False)):
				partner_2 = G['hasfeature']('empty', 'is', lockpartner, 2, (x_10 + ox_7), (y_10 + oy_7))
				if (((partner_2 is not None) and ((G['issafe'](2, (x_10 + ox_7), (y_10 + oy_7)) is False) or (G['issafe'](unitid, x_10, y_10) is False))) and L_t(G['floating'](unitid, 2, (x_10 + ox_7), (y_10 + oy_7)))):
					valid_5 = False
					L_insert(specials_2, L_T([2, 'lock']))
			weak_3 = G['hasfeature']('empty', 'is', 'weak', 2, (x_10 + ox_7), (y_10 + oy_7))
			if ((weak_3 is not None) and (pulling is False)):
				if ((G['issafe'](2, (x_10 + ox_7), (y_10 + oy_7)) is False) and L_t(G['floating'](unitid, 2, (x_10 + ox_7), (y_10 + oy_7)))):
					valid_5 = False
					L_insert(specials_2, L_T([2, 'weak']))
			added_2 = False
			if (valid_5 is not None and valid_5 is not False):
				estop = 0
				if ((emptyswap is not None) and (emptystill is not None and emptystill is not False)):
					emptyswap = None
				if ((emptypush is None) and (emptyswap is None)):
					if ((emptypull is not None) and (pulling is False)):
						estop = 1
					elif (((emptypull is not None) and (pulling is not None and pulling is not False)) and (emptystill is not None and emptystill is not False)):
						estop = 1
					elif ((emptypull is None) and (emptystop is not None)):
						estop = 1
				elif (emptystill is not None and emptystill is not False):
					estop = 1
				if (estop == 1):
					localresult_2 = 1
					L_insert(result_2, 1)
					L_insert(results, 2)
					added_2 = True
				if (localresult_2 != 1):
					if (((emptypush is not None) and (pulling is False)) and (emptyswap is None)):
						L_insert(result_2, 2)
						L_insert(results, 2)
						added_2 = True
					if ((emptypull is not None) and (pulling is not None and pulling is not False)):
						L_insert(result_2, 2)
						L_insert(results, 2)
						added_2 = True
			if (added_2 is False):
				L_insert(result_2, 0)
				L_insert(results, 2)
		if (L_len(results) == 0):
			result_2 = L_T([0])
			results = L_T([0])
		return (result_2, results, specials_2,)
		return ()
	G['check'] = f_check
	def f_trypush(unitid_2=None, ox_8=None, oy_8=None, dir__5=None, pulling__2=None, x_=None, y_=None, reason_2=None, pusherid=None, *_):  # L1205
		x_11, y_11 = 0, 0
		unit_12 = L_T()
		name_3 = ''
		if (unitid_2 != 2):
			unit_12 = G['mmf']['newObject'](unitid_2)
			x_11, y_11 = unit_12['values'][G['XPOS']], unit_12['values'][G['YPOS']]
			name_3 = G['getname'](unit_12)
		else:
			x_11 = x_
			y_11 = y_
			name_3 = 'empty'
		tileid_2 = (x_11 + (y_11 * G['roomsizex']))
		moveid = L_concat(L_tostring(tileid_2), name_3, L_tostring(dir__5))
		if (G['movemap'][moveid] is None):
			G['movemap'][moveid] = L_T()
		if (G['movemap'][moveid]['tryresult'] is None):
			G['movemap'][moveid]['tryresult'] = 0
		movedata = G['movemap'][moveid]
		pulling_2 = (_t1 if L_t(_t1 := pulling__2) else False)
		weak_4 = G['hasfeature'](name_3, 'is', 'weak', unitid_2, x_, y_)
		if (((weak_4 is None) or (pulling_2 is not None and pulling_2 is not False)) or ((weak_4 is not None) and L_t(G['issafe'](unitid_2, x_, y_)))):
			result_3 = 0
			if (movedata['tryresult'] == 0):
				hmlist, hms, specials_3 = L_adjust((*G['check'](unitid_2, x_11, y_11, dir__5, False, reason_2),), 3)
				for i_13, hm_3 in L_pairs(hmlist):
					done_2 = False
					while (done_2 is False):
						if (hm_3 == 0):
							result_3 = L_max(0, result_3)
							done_2 = True
						elif ((hm_3 == 1) or (hm_3 == (-1))):
							if ((pulling_2 is False) or ((pulling_2 is not None and pulling_2 is not False) and (hms[i_13] != pusherid))):
								result_3 = L_max(1, result_3)
								done_2 = True
							else:
								result_3 = L_max(0, result_3)
								done_2 = True
						else:
							if (pulling_2 is False):
								hm_3 = G['trypush'](hm_3, ox_8, oy_8, dir__5, pulling_2, (x_11 + ox_8), (y_11 + oy_8), reason_2, unitid_2)
							else:
								result_3 = L_max(0, result_3)
								done_2 = True
				movedata['tryresult'] = (result_3 + 1)
			else:
				result_3 = (movedata['tryresult'] - 1)
			return result_3
		else:
			return 0
	G['trypush'] = f_trypush
	def f_dopush(unitid_3=None, ox_9=None, oy_9=None, dir__6=None, pulling__3=None, x__2=None, y__2=None, reason_3=None, pusherid_2=None, *_):  # L1280
		pid2 = L_concat(L_tostring((ox_9 + (oy_9 * G['roomsizex']))), L_tostring(unitid_3))
		G['pushedunits'][pid2] = 1
		x_12, y_12 = 0, 0
		unit_13 = L_T()
		name_4 = ''
		pushsound = False
		if (unitid_3 != 2):
			unit_13 = G['mmf']['newObject'](unitid_3)
			x_12, y_12 = unit_13['values'][G['XPOS']], unit_13['values'][G['YPOS']]
			name_4 = G['getname'](unit_13)
		else:
			x_12 = x__2
			y_12 = y__2
			name_4 = 'empty'
		pulling_3 = False
		if (pulling__3 is not None):
			pulling_3 = pulling__3
		swaps_2 = G['findfeatureat'](None, 'is', 'swap', (x_12 + ox_9), (y_12 + oy_9), L_T(['still']))
		if ((swaps_2 is not None) and ((unitid_3 != 2) or ((unitid_3 == 2) and (pulling_3 is False)))):
			for a_10, b_9 in L_ipairs(swaps_2):
				if ((pulling_3 is False) or ((pulling_3 is not None and pulling_3 is not False) and (b_9 != pusherid_2))):
					alreadymoving_2 = G['findupdate'](b_9, 'update')
					valid_6 = True
					if (L_len(alreadymoving_2) > 0):
						valid_6 = False
					if (valid_6 is not None and valid_6 is not False):
						G['addaction'](b_9, L_T(['update', x_12, y_12, None]))
		if (pulling_3 is not None and pulling_3 is not False):
			swap_2 = G['hasfeature'](name_4, 'is', 'swap', unitid_3, x_12, y_12, L_T(['still']))
			if (swap_2 is not None and swap_2 is not False):
				swapthese = G['findallhere']((x_12 + ox_9), (y_12 + oy_9))
				for a_11, b_10 in L_ipairs(swapthese):
					if (b_10 != pusherid_2):
						alreadymoving_3 = G['findupdate'](b_10, 'update')
						valid_7 = True
						if (L_len(alreadymoving_3) > 0):
							valid_7 = False
						if ((valid_7 is not None and valid_7 is not False) and (b_10 != 2)):
							G['addaction'](b_10, L_T(['update', x_12, y_12, None]))
							pushsound = True
		hm_4 = 0
		tileid_3 = (x_12 + (y_12 * G['roomsizex']))
		moveid_2 = L_concat(L_tostring(tileid_3), name_4, L_tostring(dir__6))
		if (G['movemap'][moveid_2] is None):
			G['movemap'][moveid_2] = L_T()
		if (G['movemap'][moveid_2]['push'] is None):
			G['movemap'][moveid_2]['push'] = 0
			G['movemap'][moveid_2]['pull'] = 0
			G['movemap'][moveid_2]['result'] = 0
		movedata_2 = G['movemap'][moveid_2]
		if (G['HACK_MOVES'] < 10000):
			hmlist_2, hms_2, specials_4 = L_adjust((*G['check'](unitid_3, x_12, y_12, dir__6, False, reason_3),), 3)
			pullhmlist, pullhms, pullspecials_2 = L_adjust((*G['check'](unitid_3, x_12, y_12, dir__6, True, reason_3),), 3)
			result_4 = 0
			weak_5 = G['hasfeature'](name_4, 'is', 'weak', unitid_3, x__2, y__2)
			if (movedata_2['result'] == 0):
				for i_14, obs_3 in L_pairs(hmlist_2):
					done_3 = False
					while (done_3 is False):
						if (obs_3 == 0):
							result_4 = L_max(0, result_4)
							done_3 = True
						elif ((obs_3 == 1) or (obs_3 == (-1))):
							if ((pulling_3 is False) or ((pulling_3 is not None and pulling_3 is not False) and (hms_2[i_14] != pusherid_2))):
								result_4 = L_max(2, result_4)
								done_3 = True
							else:
								result_4 = L_max(0, result_4)
								done_3 = True
						else:
							if ((pulling_3 is False) or ((pulling_3 is not None and pulling_3 is not False) and (hms_2[i_14] != pusherid_2))):
								result_4 = L_max(1, result_4)
								done_3 = True
							else:
								result_4 = L_max(0, result_4)
								done_3 = True
				movedata_2['result'] = (result_4 + 1)
			else:
				result_4 = (movedata_2['result'] - 1)
				G['done'] = True
			finaldone = False
			while ((finaldone is False) and (G['HACK_MOVES'] < 10000)):
				if (result_4 == 0):
					L_insert(G['movelist'], L_T([unitid_3, ox_9, oy_9, dir__6, specials_4, x_12, y_12]))
					pushsound = True
					finaldone = True
					hm_4 = 0
					if ((pulling_3 is False) and (movedata_2['pull'] == 0)):
						for i_15, obs_4 in L_ipairs(pullhmlist):
							if ((obs_4 < (-1)) or ((obs_4 > 1) and (obs_4 != pusherid_2))):
								if (obs_4 != 2):
									L_insert(G['movelist'], L_T([obs_4, ox_9, oy_9, dir__6, pullspecials_2, x_12, y_12]))
									pushsound = True
								pid = L_concat(L_tostring(((x_12 - ox_9) + ((y_12 - oy_9) * G['roomsizex']))), L_tostring(obs_4))
								if (G['pushedunits'][pid] is None):
									G['pushedunits'][pid] = 1
									hm_4 = G['dopush'](obs_4, ox_9, oy_9, dir__6, True, (x_12 - ox_9), (y_12 - oy_9), reason_3, unitid_3)
								movedata_2['pull'] = 1
				elif (result_4 == 1):
					if (movedata_2['push'] == 0):
						for i_16, v_10 in L_ipairs(hmlist_2):
							if (((v_10 != (-1)) and (v_10 != 0)) and (v_10 != 1)):
								pid_2 = L_concat(L_tostring(((x_12 + ox_9) + ((y_12 + oy_9) * G['roomsizex']))), L_tostring(v_10))
								if ((pulling_3 is False) or (((pulling_3 is not None and pulling_3 is not False) and (hms_2[i_16] != pusherid_2)) and (G['pushedunits'][pid_2] is None))):
									G['pushedunits'][pid_2] = 1
									hm_4 = G['dopush'](v_10, ox_9, oy_9, dir__6, False, (x_12 + ox_9), (y_12 + oy_9), reason_3, unitid_3)
					else:
						hm_4 = (movedata_2['push'] - 1)
					movedata_2['push'] = (hm_4 + 1)
					if (hm_4 == 0):
						result_4 = 0
					else:
						result_4 = 2
				elif (result_4 == 2):
					hm_4 = 1
					if (weak_5 is not None):
						G['delete'](unitid_3, x_12, y_12)
						pmult_2, sound_2 = L_adjust((*G['checkeffecthistory']('weak'),), 2)
						G['setsoundname']('removal', 1, sound_2)
						G['generaldata']['values'][G['SHAKE']] = 3
						G['MF_particles']('destroy', x_12, y_12, (5 * pmult_2), 0, 3, 1, 1)
						result_4 = 0
						hm_4 = 0
					finaldone = True
			if ((pulling_3 is not None and pulling_3 is not False) and (G['HACK_MOVES'] < 10000)):
				hmlist_2, hms_2, specials_4 = L_adjust((*G['check'](unitid_3, x_12, y_12, dir__6, pulling_3, reason_3),), 3)
				hm_4 = 0
				for i_17, obs_5 in L_pairs(hmlist_2):
					if ((obs_5 < (-1)) or (obs_5 > 1)):
						pid_3 = L_concat(L_tostring(((x_12 - ox_9) + ((y_12 - oy_9) * G['roomsizex']))), L_tostring(obs_5))
						if ((obs_5 != 2) and (G['pushedunits'][pid_3] is None)):
							L_insert(G['movelist'], L_T([obs_5, ox_9, oy_9, dir__6, specials_4, x_12, y_12]))
							pushsound = True
						if (G['pushedunits'][pid_3] is None):
							G['pushedunits'][pid_3] = 1
							hm_4 = G['dopush'](obs_5, ox_9, oy_9, dir__6, pulling_3, (x_12 - ox_9), (y_12 - oy_9), reason_3, unitid_3)
				if (movedata_2['pull'] == 0):
					movedata_2['pull'] = (hm_4 + 1)
				else:
					hm_4 = (movedata_2['pull'] - 1)
			if ((pushsound is not None and pushsound is not False) and (G['generaldata2']['strings'][G['TURNSOUND']] == '')):
				G['setsoundname']('turn', 5)
		G['HACK_MOVES'] = (G['HACK_MOVES'] + 1)
		return hm_4
	G['dopush'] = f_dopush
	def f_move(unitid_4=None, ox_10=None, oy_10=None, dir__7=None, specials_=None, instant_=None, simulate_=None, x__3=None, y__3=None, *_):  # L1512
		instant = (_t1 if L_t(_t1 := instant_) else False)
		simulate = (_t2 if L_t(_t2 := simulate_) else False)
		x_13, y_13 = 0, 0
		unit_14 = L_T()
		if (unitid_4 != 2):
			unit_14 = G['mmf']['newObject'](unitid_4)
			x_13, y_13 = unit_14['values'][G['XPOS']], unit_14['values'][G['YPOS']]
		else:
			x_13 = x__3
			y_13 = y__3
		specials_5 = L_T()
		if (specials_ is not None):
			specials_5 = specials_
		gone = False
		for i_18, v_11 in L_pairs(specials_5):
			if (gone is False):
				b_11 = v_11[1]
				reason_4 = v_11[2]
				dodge = False
				bx, by = 0, 0
				if ((b_11 != 2) and (G['deleted'][b_11] is not None)):
					G['MF_alert']('Already gone')
					dodge = True
				elif ((b_11 != 2) and (reason_4 != 'weak')):
					bunit = G['mmf']['newObject'](b_11)
					bx, by = bunit['values'][G['XPOS']], bunit['values'][G['YPOS']]
					if ((bx != (x_13 + ox_10)) or (by != (y_13 + oy_10))):
						dodge = True
					else:
						for c_6, d in L_ipairs(G['movelist']):
							if (d[1] == b_11):
								nx_2, ny_2 = d[2], d[3]
								if ((nx_2 != (x_13 + ox_10)) or (ny_2 != (y_13 + oy_10))):
									dodge = True
				else:
					bx, by = (x_13 + ox_10), (y_13 + oy_10)
				if (dodge is False):
					if (reason_4 == 'lock'):
						unlocked = False
						valid_8 = True
						soundshort = ''
						if (b_11 != 2):
							bunit_2 = G['mmf']['newObject'](b_11)
							if L_t(bunit_2['flags'][G['DEAD']]):
								valid_8 = False
						if ((unitid_4 != 2) and L_t(unit_14['flags'][G['DEAD']])):
							valid_8 = False
						if (valid_8 is not None and valid_8 is not False):
							pmult_3 = 1.0
							effect1 = False
							effect2 = False
							if (G['issafe'](b_11, bx, by) is False):
								G['delete'](b_11, bx, by)
								unlocked = True
								effect1 = True
							if (G['issafe'](unitid_4, x_13, y_13) is False):
								G['delete'](unitid_4, x_13, y_13)
								unlocked = True
								gone = True
								effect2 = True
							if ((effect1 is not None and effect1 is not False) or (effect2 is not None and effect2 is not False)):
								pmult_4, sound_3 = L_adjust((*G['checkeffecthistory']('unlock'),), 2)
								soundshort = sound_3
							if (effect1 is not None and effect1 is not False):
								G['MF_particles']('unlock', bx, by, (15 * pmult_3), 2, 4, 1, 1)
								G['generaldata']['values'][G['SHAKE']] = 8
							if (effect2 is not None and effect2 is not False):
								G['MF_particles']('unlock', x_13, y_13, (15 * pmult_3), 2, 4, 1, 1)
								G['generaldata']['values'][G['SHAKE']] = 8
						if (unlocked is not None and unlocked is not False):
							G['setsoundname']('turn', 7, soundshort)
					elif (reason_4 == 'eat'):
						pmult_5, sound_4 = L_adjust((*G['checkeffecthistory']('eat'),), 2)
						G['MF_particles']('eat', bx, by, (10 * pmult_5), 0, 3, 1, 1)
						G['generaldata']['values'][G['SHAKE']] = 3
						G['delete'](b_11, bx, by)
						G['setsoundname']('removal', 1, sound_4)
					elif (reason_4 == 'weak'):
						if ((b_11 == 2) and (unitid_4 != 2)):
							pmult_6, sound_5 = L_adjust((*G['checkeffecthistory']('weak'),), 2)
							G['MF_particles']('destroy', bx, by, (5 * pmult_6), 0, 3, 1, 1)
							G['generaldata']['values'][G['SHAKE']] = 3
							G['delete'](b_11, bx, by)
							G['setsoundname']('removal', 1, sound_5)
		if (((gone is False) and (simulate is False)) and (unitid_4 != 2)):
			if (instant is not None and instant is not False):
				G['update'](unitid_4, (x_13 + ox_10), (y_13 + oy_10), dir__7)
				G['MF_alert'](L_concat('Instant movement on ', L_tostring(unitid_4)))
			else:
				G['addaction'](unitid_4, L_T(['update', (x_13 + ox_10), (y_13 + oy_10), dir__7]))
			if ((L_t(unit_14['visible']) and (L_len(G['movelist']) < 700)) and (G['spritedata']['values'][G['VISION']] == 0)):
				if ((G['generaldata']['values'][G['DISABLEPARTICLES']] == 0) and (G['generaldata5']['values'][G['LEVEL_DISABLEPARTICLES']] == 0)):
					effectid = G['MF_effectcreate']('effect_bling')
					effect = G['mmf']['newObject'](effectid)
					midxdelta = (G['spritedata']['values'][G['XMIDTILE']] - (G['roomsizex'] * 0.5))
					midydelta = (G['spritedata']['values'][G['YMIDTILE']] - (G['roomsizey'] * 0.5))
					midx = ((G['roomsizex'] * 0.5) + (midxdelta * G['generaldata2']['values'][G['ZOOM']]))
					midy = ((G['roomsizey'] * 0.5) + (midydelta * G['generaldata2']['values'][G['ZOOM']]))
					mx = (x_13 - midx)
					my = (y_13 - midy)
					c1, c2 = 0, 0
					if (((unit_14['colour'] is not None) and (unit_14['colour'][1] is not None)) and (unit_14['colour'][2] is not None)):
						c1 = unit_14['colour'][1]
						c2 = unit_14['colour'][2]
					else:
						if (unit_14['active'] is False):
							c1, c2 = L_adjust((*G['getcolour'](unitid_4),), 2)
						else:
							c1, c2 = L_adjust((*G['getcolour'](unitid_4, 'active'),), 2)
					G['MF_setcolour'](effectid, c1, c2)
					xvel, yvel = 0, 0
					if (ox_10 != 0):
						xvel = (0 - L_div(ox_10, abs(ox_10)))
					if (oy_10 != 0):
						yvel = (0 - L_div(oy_10, abs(oy_10)))
					dx = (mx + 0.5)
					dy = (my + 0.75)
					dxvel = xvel
					dyvel = yvel
					if (G['generaldata2']['values'][G['ROOMROTATION']] == 90):
						dx = (my + 0.75)
						dy = ((0 - mx) - 0.5)
						dxvel = yvel
						dyvel = (0 - xvel)
					elif (G['generaldata2']['values'][G['ROOMROTATION']] == 180):
						dx = ((0 - mx) - 0.5)
						dy = ((0 - my) - 0.75)
						dxvel = (0 - xvel)
						dyvel = (0 - yvel)
					elif (G['generaldata2']['values'][G['ROOMROTATION']] == 270):
						dx = ((0 - my) - 0.75)
						dy = (mx + 0.5)
						dxvel = (0 - yvel)
						dyvel = xvel
					effect['values'][G['ONLINE']] = 3
					effect['values'][G['XPOS']] = (G['Xoffset'] + (((midx + (dx * G['generaldata2']['values'][G['ZOOM']])) * G['tilesize']) * G['spritedata']['values'][G['TILEMULT']]))
					effect['values'][G['YPOS']] = (G['Yoffset'] + (((midy + (dy * G['generaldata2']['values'][G['ZOOM']])) * G['tilesize']) * G['spritedata']['values'][G['TILEMULT']]))
					effect['scaleX'] = (G['generaldata2']['values'][G['ZOOM']] * G['spritedata']['values'][G['TILEMULT']])
					effect['scaleY'] = (G['generaldata2']['values'][G['ZOOM']] * G['spritedata']['values'][G['TILEMULT']])
					effect['values'][G['XVEL']] = ((((dxvel * G['math']['random'](10, 30)) * 0.1) * G['spritedata']['values'][G['TILEMULT']]) * G['generaldata2']['values'][G['ZOOM']])
					effect['values'][G['YVEL']] = ((((dyvel * G['math']['random'](10, 30)) * 0.1) * G['spritedata']['values'][G['TILEMULT']]) * G['generaldata2']['values'][G['ZOOM']])
				if (unit_14['values'][G['TILING']] == 2):
					unit_14['values'][G['VISUALDIR']] = (((unit_14['values'][G['VISUALDIR']] + 1) + 4) % 4)
		return gone
	G['move'] = f_move
	def f_add_moving_units(rule=None, newdata=None, data_4=None, been_seen_2=None, empty_=None, *_):  # L1727
		result_5 = data_4
		seen = been_seen_2
		emptyseen = L_T()
		empty_2 = (_t1 if L_t(_t1 := empty_) else L_T())
		for i_19, v_12 in L_ipairs(newdata):
			sleeping_4 = False
			if (v_12 != 2):
				unit_15 = G['mmf']['newObject'](v_12)
				unitname_4 = G['getname'](unit_15)
				sleep_6 = G['hasfeature'](unitname_4, 'is', 'sleep', v_12)
				if ((rule == 'chill') and (sleep_6 is None)):
					dir__8 = G['fixedrandom'](0, 3)
					if (data_4['unitid'] != 2):
						G['updatedir'](v_12, dir__8)
				dir__9 = unit_15['values'][G['DIR']]
				if (rule == 'nudgeright'):
					dir__9 = 0
				elif (rule == 'nudgeup'):
					dir__9 = 1
				elif (rule == 'nudgeleft'):
					dir__9 = 2
				elif (rule == 'nudgedown'):
					dir__9 = 3
				still_7 = G['cantmove'](unitname_4, v_12, dir__9)
				if ((sleep_6 is not None) or (still_7 is not None and still_7 is not False)):
					sleeping_4 = True
			else:
				thisempty_3 = empty_2[i_19]
				for a_12, b_12 in L_pairs(thisempty_3):
					x_14 = (a_12 % G['roomsizex'])
					y_14 = L_floor(L_div(a_12, G['roomsizex']))
					dir__10 = data_4['dir']
					if (rule == 'nudgeright'):
						dir__10 = 0
					elif (rule == 'nudgeup'):
						dir__10 = 1
					elif (rule == 'nudgeleft'):
						dir__10 = 2
					elif (rule == 'nudgedown'):
						dir__10 = 3
					sleep_7 = G['hasfeature']('empty', 'is', 'sleep', 2, x_14, y_14)
					still_8 = G['cantmove']('empty', 2, dir__10, x_14, y_14)
					if ((sleep_7 is not None) or (still_8 is not None and still_8 is not False)):
						thisempty_3[a_12] = None
			if (sleeping_4 is False):
				seencode = v_12
				if (v_12 == 2):
					seencode = ((i_19 * 1000) + v_12)
				if (seen[seencode] is None):
					dir__11 = 4
					x_15, y_15 = (-1), (-1)
					if (v_12 != 2):
						unit_16 = G['mmf']['newObject'](v_12)
						x_15, y_15 = unit_16['values'][G['XPOS']], unit_16['values'][G['YPOS']]
						L_insert(result_5, L_T([], {'unitid': v_12, 'reason': rule, 'state': 0, 'moves': 1, 'dir': dir__11, 'xpos': x_15, 'ypos': y_15}))
						seen[seencode] = L_len(result_5)
					else:
						thisempty_4 = empty_2[i_19]
						for a_13, b_13 in L_pairs(thisempty_4):
							x_15 = (a_13 % G['roomsizex'])
							y_15 = L_floor(L_div(a_13, G['roomsizex']))
							dir__11 = G['emptydir'](x_15, y_15)
							L_insert(result_5, L_T([], {'unitid': 2, 'reason': rule, 'state': 0, 'moves': 1, 'dir': dir__11, 'xpos': x_15, 'ypos': y_15}))
							seen[seencode] = L_len(result_5)
							if (emptyseen[seencode] is None):
								emptyseen[seencode] = L_T()
							L_insert(emptyseen[seencode], L_len(result_5))
				else:
					if (v_12 != 2):
						id__6 = seen[seencode]
						this_5 = result_5[id__6]
						this_5['moves'] = (this_5['moves'] + 1)
					elif (emptyseen[seencode] is not None):
						for a_14, b_14 in L_ipairs(emptyseen[seencode]):
							this_6 = result_5[b_14]
							this_6['moves'] = (this_6['moves'] + 1)
		return (result_5, seen,)
		return ()
	G['add_moving_units'] = f_add_moving_units
