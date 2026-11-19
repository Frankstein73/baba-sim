"""Generated from blocks.lua by tools/lua2py.py. Do not edit."""
from babasim.luart import *  # noqa: F403


def load(G):
	def f_effectblock(*_):  # L1
		levelhide = None
		if (G['featureindex']['level'] is not None):
			levelhide = G['hasfeature']('level', 'is', 'hide', 1)
			isred = G['hasfeature']('level', 'is', 'red', 1)
			isblue = G['hasfeature']('level', 'is', 'blue', 1)
			isgreen = G['hasfeature']('level', 'is', 'green', 1)
			islime = G['hasfeature']('level', 'is', 'lime', 1)
			isyellow = G['hasfeature']('level', 'is', 'yellow', 1)
			ispurple = G['hasfeature']('level', 'is', 'purple', 1)
			ispink = G['hasfeature']('level', 'is', 'pink', 1)
			isrosy = G['hasfeature']('level', 'is', 'rosy', 1)
			isblack = G['hasfeature']('level', 'is', 'black', 1)
			isgrey = G['hasfeature']('level', 'is', 'grey', 1)
			issilver = G['hasfeature']('level', 'is', 'silver', 1)
			iswhite = G['hasfeature']('level', 'is', 'white', 1)
			isbrown = G['hasfeature']('level', 'is', 'brown', 1)
			isorange = G['hasfeature']('level', 'is', 'orange', 1)
			iscyan = G['hasfeature']('level', 'is', 'cyan', 1)
			colours = L_T([isred, isorange, isyellow, islime, isgreen, iscyan, isblue, ispurple, ispink, isrosy, isblack, isgrey, issilver, iswhite, isbrown])
			ccolours = L_T([L_T([2, 2]), L_T([2, 3]), L_T([2, 4]), L_T([5, 3]), L_T([5, 2]), L_T([1, 4]), L_T([3, 2]), L_T([3, 1]), L_T([4, 1]), L_T([4, 2]), L_T([0, 4]), L_T([0, 1]), L_T([0, 2]), L_T([0, 3]), L_T([6, 1])])
			G['leveldata']['colours'] = L_T()
			c1, c2 = (-1), (-1)
			for a in L_range(1, L_len(ccolours)):
				if (colours[a] is not None):
					c = ccolours[a]
					if (L_len(G['leveldata']['colours']) == 0):
						c1 = c[1]
						c2 = c[2]
					L_insert(G['leveldata']['colours'], L_T([c[1], c[2]]))
			if (L_len(G['leveldata']['colours']) == 1):
				if ((c1 > (-1)) and (c2 > (-1))):
					if ((c1 == 0) and (c2 == 4)):
						G['MF_backcolour'](c1, c2)
					else:
						G['MF_backcolour_dim'](c1, c2)
			elif (L_len(G['leveldata']['colours']) == 0):
				G['MF_backcolour'](0, 4)
		else:
			G['MF_backcolour'](0, 4)
		resetcolour = L_T()
		updatecolour = L_T()
		for i, unit in L_ipairs(G['units']):
			unit['new'] = False
			unit['flags'][G['LEVELVISOVERRIDE']] = False
			if (levelhide is None):
				unit['visible'] = True
			else:
				unit['visible'] = False
				unit['flags'][G['LEVELVISOVERRIDE']] = True
			if (unit['className'] != 'level'):
				name = unit['strings'][G['UNITNAME']]
				isred_2 = G['hasfeature'](name, 'is', 'red', unit['fixed'])
				isblue_2 = G['hasfeature'](name, 'is', 'blue', unit['fixed'])
				islime_2 = G['hasfeature'](name, 'is', 'lime', unit['fixed'])
				isgreen_2 = G['hasfeature'](name, 'is', 'green', unit['fixed'])
				isyellow_2 = G['hasfeature'](name, 'is', 'yellow', unit['fixed'])
				ispurple_2 = G['hasfeature'](name, 'is', 'purple', unit['fixed'])
				ispink_2 = G['hasfeature'](name, 'is', 'pink', unit['fixed'])
				isrosy_2 = G['hasfeature'](name, 'is', 'rosy', unit['fixed'])
				isblack_2 = G['hasfeature'](name, 'is', 'black', unit['fixed'])
				isgrey_2 = G['hasfeature'](name, 'is', 'grey', unit['fixed'])
				issilver_2 = G['hasfeature'](name, 'is', 'silver', unit['fixed'])
				iswhite_2 = G['hasfeature'](name, 'is', 'white', unit['fixed'])
				isbrown_2 = G['hasfeature'](name, 'is', 'brown', unit['fixed'])
				isorange_2 = G['hasfeature'](name, 'is', 'orange', unit['fixed'])
				iscyan_2 = G['hasfeature'](name, 'is', 'cyan', unit['fixed'])
				unit['colours'] = L_T()
				colours_2 = L_T([isred_2, isorange_2, isyellow_2, islime_2, isgreen_2, iscyan_2, isblue_2, ispurple_2, ispink_2, isrosy_2, isblack_2, isgrey_2, issilver_2, iswhite_2, isbrown_2])
				ccolours_2 = L_T([L_T([2, 2]), L_T([2, 3]), L_T([2, 4]), L_T([5, 3]), L_T([5, 2]), L_T([1, 4]), L_T([3, 2]), L_T([3, 1]), L_T([4, 1]), L_T([4, 2]), L_T([0, 4]), L_T([0, 1]), L_T([0, 2]), L_T([0, 3]), L_T([6, 1])])
				c1_2, c2_2, ca = (-1), (-1), (-1)
				unit['flags'][G['PHANTOM']] = False
				isphantom = G['hasfeature'](name, 'is', 'phantom', unit['fixed'])
				if (isphantom is not None):
					unit['flags'][G['PHANTOM']] = True
				for a_2 in L_range(1, L_len(ccolours_2)):
					if (colours_2[a_2] is not None):
						c_2 = ccolours_2[a_2]
						if (L_len(unit['colours']) == 0):
							c1_2 = c_2[1]
							c2_2 = c_2[2]
							ca = a_2
						L_insert(unit['colours'], c_2)
				if (L_len(unit['colours']) == 1):
					if (((c1_2 > (-1)) and (c2_2 > (-1))) and (ca > 0)):
						G['MF_setcolour'](unit['fixed'], c1_2, c2_2)
						unit['colour'] = L_T([c1_2, c2_2])
						unit['values'][G['A']] = ca
				elif (L_len(unit['colours']) == 0):
					if ((unit['values'][G['A']] > 0) and (L_floor(unit['values'][G['A']]) == unit['values'][G['A']])):
						if ((unit['strings'][G['UNITTYPE']] != 'text') or (unit['active'] is False)):
							G['setcolour'](unit['fixed'])
						else:
							G['setcolour'](unit['fixed'], 'active')
						unit['values'][G['A']] = 0
				else:
					unit['values'][G['A']] = ca
					if (unit['strings'][G['UNITTYPE']] == 'text'):
						curr = ((unit['currcolour'] % L_len(unit['colours'])) + 1)
						c_3 = unit['colours'][curr]
						unit['colour'] = L_T([c_3[1], c_3[2]])
						G['MF_setcolour'](unit['fixed'], c_3[1], c_3[2])
		if (levelhide is None):
			ishide = L_first(G['findallfeature'](None, 'is', 'hide', True))
			for i_2, unitid in L_ipairs(ishide):
				unit_2 = G['mmf']['newObject'](unitid)
				unit_2['visible'] = False
				unit_2['flags'][G['LEVELVISOVERRIDE']] = True
	G['effectblock'] = f_effectblock
	def f_brokenblock(ids=None, *_):  # L157
		checkthese = L_T()
		if (ids is None):
			checkthese = G['units']
		else:
			checkthese = ids
		for i_3, unit_3 in L_ipairs(checkthese):
			name_2 = unit_3['strings'][G['UNITNAME']]
			realbroken = unit_3['broken']
			unit_3['broken'] = 0
			broken = G['hasfeature'](name_2, 'is', 'broken', unit_3['fixed'])
			unit_3['broken'] = realbroken
			if ((broken is not None) and (unit_3['broken'] == 0)):
				unit_3['broken'] = 1
				G['addundo'](L_T(['broken', 1, unit_3['values'][G['ID']], unit_3['strings'][G['UNITNAME']]]))
			elif ((broken is None) and (unit_3['broken'] == 1)):
				unit_3['broken'] = 0
				G['addundo'](L_T(['broken', 0, unit_3['values'][G['ID']], unit_3['strings'][G['UNITNAME']]]))
	G['brokenblock'] = f_brokenblock
	def f_statusblock(ids_2=None, undoing_=None, noturn_=None, *_):  # L183
		checkthese_2 = L_T()
		undoing = (_t1 if L_t(_t1 := undoing_) else False)
		noturn = (_t2 if L_t(_t2 := noturn_) else False)
		G['generaldata5']['values'][G['AUTO_ON']] = 0
		if (G['featureindex']['level'] is not None):
			auto_on = G['hasfeature_count']('level', 'is', 'auto', 1)
			if (auto_on is not None):
				G['generaldata5']['values'][G['AUTO_ON']] = auto_on
		if (ids_2 is None):
			checkthese_2 = G['units']
		else:
			for i_4, v in L_ipairs(ids_2):
				vunit = G['mmf']['newObject'](v)
				L_insert(checkthese_2, vunit)
		if (undoing is False):
			G['brokenblock'](checkthese_2)
		for i_5, unit_4 in L_pairs(checkthese_2):
			name_3 = G['getname'](unit_4)
			if (undoing is False):
				ur = G['hasfeature_count'](name_3, 'is', 'right', unit_4['fixed'])
				uu = G['hasfeature_count'](name_3, 'is', 'up', unit_4['fixed'])
				ul = G['hasfeature_count'](name_3, 'is', 'left', unit_4['fixed'])
				ud = G['hasfeature_count'](name_3, 'is', 'down', unit_4['fixed'])
				turn = L_T()
				deturn = L_T()
				if (G['featureindex']['turn'] is not None):
					for a_3, b in L_ipairs(G['featureindex']['turn']):
						rule = b[1]
						conds = b[2]
						if (((rule[1] == name_3) and (rule[2] == 'is')) and (rule[3] == 'turn')):
							L_insert(turn, L_T([rule[2], conds]))
				if (G['featureindex']['deturn'] is not None):
					for a_4, b_2 in L_ipairs(G['featureindex']['deturn']):
						rule_2 = b_2[1]
						conds_2 = b_2[2]
						if (((rule_2[1] == name_3) and (rule_2[2] == 'is')) and (rule_2[3] == 'deturn')):
							L_insert(deturn, L_T([rule_2[2], conds_2]))
				if (G['issleep'](unit_4['fixed']) is False):
					currdir = unit_4['values'][G['DIR']]
					fdir = currdir
					if ((noturn is False) and ((((ur > 0) or (uu > 0)) or (ul > 0)) or (ud > 0))):
						if (((ur > uu) and (ur > ul)) and (ur > ud)):
							fdir = 0
						elif (((uu > ur) and (uu > ul)) and (uu > ud)):
							fdir = 1
						elif (((ul > ur) and (ul > uu)) and (ul > ud)):
							fdir = 2
						elif (((ud > ur) and (ud > ul)) and (ud > uu)):
							fdir = 3
						elif (currdir == 3):
							if (((ul > 0) and (ul >= uu)) and (ul >= ur)):
								fdir = 2
							elif (((uu > 0) and (uu > ul)) and (uu >= ur)):
								fdir = 1
							elif (((ur > 0) and (ur > ul)) and (ur > uu)):
								fdir = 0
						elif (currdir == 2):
							if (((uu > 0) and (uu >= ur)) and (uu >= ul)):
								fdir = 1
							elif (((ur > 0) and (ur > uu)) and (ur >= ud)):
								fdir = 0
							elif (((ud > 0) and (ud > ur)) and (ud > uu)):
								fdir = 3
						elif (currdir == 1):
							if (((ur > 0) and (ur >= ul)) and (ur >= ud)):
								fdir = 0
							elif (((ud > 0) and (ud > ur)) and (ud >= ul)):
								fdir = 3
							elif (((ul > 0) and (ul > ur)) and (ul > ud)):
								fdir = 2
						elif (currdir == 0):
							if (((ud > 0) and (ud >= ul)) and (ud >= uu)):
								fdir = 3
							elif (((ul > 0) and (ul > ud)) and (ul >= uu)):
								fdir = 2
							elif (((uu > 0) and (uu > ud)) and (uu > ul)):
								fdir = 1
						if (fdir != currdir):
							G['updatedir'](unit_4['fixed'], fdir)
							currdir = fdir
					if ((((turn is not None) or (deturn is not None)) and (undoing is False)) and (noturn is False)):
						x, y = unit_4['values'][G['XPOS']], unit_4['values'][G['YPOS']]
						turns = 0
						deturns = 0
						if (turn is not None):
							for a_5, b_3 in L_ipairs(turn):
								if L_t(G['testcond'](b_3[2], unit_4['fixed'], x, y)):
									turns = (turns + 1)
						if (deturn is not None):
							for a_6, b_4 in L_ipairs(deturn):
								if L_t(G['testcond'](b_4[2], unit_4['fixed'], x, y)):
									deturns = (deturns + 1)
						if (turns >= deturns):
							turns = (turns - deturns)
							deturns = 0
						if (deturns >= turns):
							deturns = (deturns - turns)
							turns = 0
						if (turns > 0):
							for d in L_range(1, turns):
								currdir = (((currdir + 4) - 1) % 4)
							G['updatedir'](unit_4['fixed'], currdir)
						if (deturns > 0):
							for d_2 in L_range(1, deturns):
								currdir = (((currdir + 4) + 1) % 4)
							G['updatedir'](unit_4['fixed'], currdir)
				if (G['generaldata']['values'][G['MODE']] == 0):
					if (G['featureindex']['back'] is not None):
						isback = G['hasfeature'](name_3, 'is', 'back', unit_4['fixed'])
						if ((isback is None) and (unit_4['back_init'] != 0)):
							G['addundo'](L_T(['backset', name_3, unit_4['values'][G['ID']], unit_4['back_init']]))
							unit_4['back_init'] = 0
						if ((isback is not None) and (unit_4['back_init'] == 0)):
							G['addundo'](L_T(['backset', name_3, unit_4['values'][G['ID']], 0]))
							unit_4['back_init'] = (L_len(G['undobuffer']) + 1)
					elif (unit_4['back_init'] != 0):
						G['addundo'](L_T(['backset', name_3, unit_4['values'][G['ID']], unit_4['back_init']]))
						unit_4['back_init'] = 0
			oldfloat = unit_4['values'][G['FLOAT']]
			newfloat = 0
			if ((unit_4['values'][G['FLOAT']] < 2) and (G['generaldata']['values'][G['MODE']] == 0)):
				unit_4['values'][G['FLOAT']] = 0
			isfloat = G['hasfeature'](name_3, 'is', 'float', unit_4['fixed'])
			if ((isfloat is not None) and (G['generaldata']['values'][G['MODE']] == 0)):
				unit_4['values'][G['FLOAT']] = 1
				newfloat = 1
			if (undoing is False):
				if (((oldfloat != newfloat) and (G['generaldata']['values'][G['MODE']] == 0)) and (G['generaldata2']['values'][G['ENDINGGOING']] == 0)):
					G['addaction'](unit_4['fixed'], L_T(['dofloat', oldfloat, newfloat, unit_4['values'][G['ID']], unit_4['fixed'], name_3]))
	G['statusblock'] = f_statusblock
	def f_moveblock(onlystartblock_=None, *_):  # L394
		onlystartblock = (_t1 if L_t(_t1 := onlystartblock_) else False)
		isshift, istele = L_T(), L_T()
		isfollow = G['findfeature'](None, 'follow', None, True)
		if (onlystartblock is False):
			isshift = L_first(G['findallfeature'](None, 'is', 'shift', True))
			istele = L_first(G['findallfeature'](None, 'is', 'tele', True))
		doned = L_T()
		if (isfollow is not None):
			for h, j in L_ipairs(isfollow):
				allfollows = G['findall'](j)
				if (L_len(allfollows) > 0):
					for k, l in L_ipairs(allfollows):
						if (G['issleep'](l) is False):
							unit_5 = G['mmf']['newObject'](l)
							x_2, y_2, name_4, dir_ = unit_5['values'][G['XPOS']], unit_5['values'][G['YPOS']], unit_5['strings'][G['UNITNAME']], unit_5['values'][G['DIR']]
							unitrules = L_T()
							followedfound = False
							if (unit_5['strings'][G['UNITTYPE']] == 'text'):
								name_4 = 'text'
							if (G['featureindex'][name_4] is not None):
								for a_7, b_5 in L_ipairs(G['featureindex'][name_4]):
									baserule = b_5[1]
									conds_3 = b_5[2]
									verb = baserule[2]
									if (verb == 'follow'):
										if L_t(G['testcond'](conds_3, l)):
											L_insert(unitrules, b_5)
							follow = G['xthis'](unitrules, name_4, 'follow')
							if ((L_len(follow) > 0) and (unit_5['flags'][G['DEAD']] is False)):
								distance = 9999
								targetdir = (-1)
								stophere = False
								highesttarget = False
								counterclockwise = False
								priorityfollow = (-1)
								priorityfollowdir = (-1)
								highpriorityfollow = (-1)
								highpriorityfollowdir = (-1)
								for i_6, v_2 in L_ipairs(follow):
									these = G['findall'](L_T([v_2]))
									if ((L_len(these) > 0) and (stophere is False)):
										for a_8, b_6 in L_ipairs(these):
											if ((b_6 != unit_5['fixed']) and (stophere is False)):
												funit = G['mmf']['newObject'](b_6)
												fx, fy = funit['values'][G['XPOS']], funit['values'][G['YPOS']]
												xdir = (fx - x_2)
												ydir = (fy - y_2)
												dist = (abs(xdir) + abs(ydir))
												fdir_2 = (-1)
												if (abs(xdir) <= abs(ydir)):
													if (ydir >= 0):
														fdir_2 = 3
													else:
														fdir_2 = 1
												else:
													if (xdir > 0):
														fdir_2 = 0
													else:
														fdir_2 = 2
												if ((dist <= distance) and (dist > 0)):
													distance = dist
													targetdir = fdir_2
													if (dist == 1):
														if (unit_5['followed'] != funit['values'][G['ID']]):
															ndrs = G['ndirs'][(dir_ + 1)]
															ox, oy = ndrs[1], ndrs[2]
															priorityfollow = funit['values'][G['ID']]
															priorityfollowdir = targetdir
															if (((x_2 + ox) == fx) and ((y_2 + oy) == fy)):
																highpriorityfollow = funit['values'][G['ID']]
																highpriorityfollowdir = targetdir
																highesttarget = True
															elif (highesttarget is False):
																turnl = (((dir_ + 1) + 4) % 4)
																ndrsl = G['ndirs'][(turnl + 1)]
																oxl, oyl = ndrsl[1], ndrsl[2]
																if (((x_2 + oxl) == fx) and ((y_2 + oyl) == fy)):
																	highpriorityfollow = funit['values'][G['ID']]
																	highpriorityfollowdir = targetdir
																	counterclockwise = True
																elif (counterclockwise is False):
																	turnr = (((dir_ - 1) + 4) % 4)
																	ndrsr = G['ndirs'][(turnr + 1)]
																	oxr, oyr = ndrsr[1], ndrsr[2]
																	if (((x_2 + oxr) == fx) and ((y_2 + oyr) == fy)):
																		highpriorityfollow = funit['values'][G['ID']]
																		highpriorityfollowdir = targetdir
														else:
															followedfound = True
															stophere = True
															break
										if (stophere is not None and stophere is not False):
											break
									if (stophere is not None and stophere is not False):
										break
								if (followedfound is False):
									if (highpriorityfollow > (-1)):
										if (onlystartblock is False):
											G['addundo'](L_T(['followed', unit_5['values'][G['ID']], unit_5['followed'], highpriorityfollow, unit_5['strings'][G['UNITNAME']]]), unit_5['fixed'])
										unit_5['followed'] = highpriorityfollow
										targetdir = highpriorityfollowdir
										stophere = True
										followedfound = True
									elif (priorityfollow > (-1)):
										if (onlystartblock is False):
											G['addundo'](L_T(['followed', unit_5['values'][G['ID']], unit_5['followed'], priorityfollow, unit_5['strings'][G['UNITNAME']]]), unit_5['fixed'])
										unit_5['followed'] = priorityfollow
										targetdir = priorityfollowdir
										stophere = True
										followedfound = True
									elif (unit_5['followed'] > (-1)):
										if (onlystartblock is False):
											G['addundo'](L_T(['followed', unit_5['values'][G['ID']], unit_5['followed'], 0, unit_5['strings'][G['UNITNAME']]]), unit_5['fixed'])
										unit_5['followed'] = (-1)
								if (targetdir >= 0):
									G['updatedir'](unit_5['fixed'], targetdir, onlystartblock)
		if (onlystartblock is False):
			isback_2 = L_first(G['findallfeature'](None, 'is', 'back', True))
			for i_7, unitid_2 in L_ipairs(isback_2):
				unit_6 = G['mmf']['newObject'](unitid_2)
				undooffset = (L_len(G['undobuffer']) - unit_6['back_init'])
				undotargetid = ((undooffset * 2) + 1)
				if (((undotargetid <= L_len(G['undobuffer'])) and (unit_6['back_init'] > 0)) and (unit_6['flags'][G['DEAD']] is False)):
					currentundo = G['undobuffer'][undotargetid]
					G['particles']('wonder', unit_6['values'][G['XPOS']], unit_6['values'][G['YPOS']], 1, L_T([3, 0]))
					G['updateundo'] = True
					if (currentundo is not None):
						for a_9, line in L_ipairs(currentundo):
							style = line[1]
							if ((style == 'update') and (line[9] == unit_6['values'][G['ID']])):
								uid = line[9]
								if (G['paradox'][uid] is None):
									ux, uy = unit_6['values'][G['XPOS']], unit_6['values'][G['YPOS']]
									oldx, oldy = line[6], line[7]
									x_3, y_3, dir__2 = line[3], line[4], line[5]
									ox_2 = (x_3 - oldx)
									oy_2 = (y_3 - oldy)
									if ((ox_2 != 0) or (oy_2 != 0)):
										G['addaction'](unitid_2, L_T(['update', x_3, y_3, dir__2]))
									else:
										G['addaction'](unitid_2, L_T(['updatedir', dir__2]))
									G['updateundo'] = True
									if (G['objectdata'][unitid_2] is None):
										G['objectdata'][unitid_2] = L_T()
									odata = G['objectdata'][unitid_2]
									odata['tele'] = 1
								else:
									G['particles']('hot', line[3], line[4], 1, L_T([1, 1]))
									G['updateundo'] = True
							elif ((style == 'create') and (line[3] == unit_6['values'][G['ID']])):
								uid_2 = line[4]
								if (G['paradox'][uid_2] is None):
									name_5 = unit_6['strings'][G['UNITNAME']]
									delname = L_T()
									for b_7, bline in L_ipairs(currentundo):
										if ((bline[1] == 'remove') and (bline[6] == uid_2)):
											x_4, y_4, dir__3, levelfile, levelname, vislevel, complete, visstyle, maplevel, colour, clearcolour, followed, back_init = bline[3], bline[4], bline[5], bline[8], bline[9], bline[10], bline[11], bline[12], bline[13], bline[14], bline[15], bline[16], bline[17]
											newname = bline[2]
											newunitname = ''
											newunitid = 0
											ux_2, uy_2 = unit_6['values'][G['XPOS']], unit_6['values'][G['YPOS']]
											newunitname = G['unitreference'][newname]
											newunitid = G['MF_emptycreate'](newunitname, ux_2, uy_2)
											newunit = G['mmf']['newObject'](newunitid)
											newunit['values'][G['ONLINE']] = 1
											newunit['values'][G['XPOS']] = ux_2
											newunit['values'][G['YPOS']] = uy_2
											newunit['values'][G['DIR']] = dir__3
											newunit['values'][G['ID']] = bline[6]
											newunit['flags'][9] = True
											newunit['strings'][G['U_LEVELFILE']] = levelfile
											newunit['strings'][G['U_LEVELNAME']] = levelname
											newunit['flags'][G['MAPLEVEL']] = maplevel
											newunit['values'][G['VISUALLEVEL']] = vislevel
											newunit['values'][G['VISUALSTYLE']] = visstyle
											newunit['values'][G['COMPLETED']] = complete
											newunit['strings'][G['COLOUR']] = colour
											newunit['strings'][G['CLEARCOLOUR']] = clearcolour
											if (newunit['className'] == 'level'):
												G['MF_setcolourfromstring'](newunitid, colour)
											G['addunit'](newunitid, True)
											G['addunitmap'](newunitid, x_4, y_4, newunit['strings'][G['UNITNAME']])
											G['dynamic'](unitid_2)
											newunit['followed'] = followed
											newunit['back_init'] = back_init
											if (newunit['strings'][G['UNITTYPE']] == 'text'):
												G['updatecode'] = 1
											undowordunits = currentundo['wordunits']
											undowordrelatedunits = currentundo['wordrelatedunits']
											if (L_len(undowordunits) > 0):
												for a_10, b_8 in L_ipairs(undowordunits):
													if (b_8 == bline[6]):
														G['updatecode'] = 1
											if (L_len(undowordrelatedunits) > 0):
												for a_11, b_9 in L_ipairs(undowordrelatedunits):
													if (b_9 == bline[6]):
														G['updatecode'] = 1
											L_insert(delname, L_T([newunit['strings'][G['UNITNAME']], bline[6], newunit['values'][G['XPOS']], newunit['values'][G['YPOS']], newunit['values'][G['DIR']]]))
									G['addundo'](L_T(['remove', unit_6['strings'][G['UNITNAME']], unit_6['values'][G['XPOS']], unit_6['values'][G['YPOS']], unit_6['values'][G['DIR']], unit_6['values'][G['ID']], unit_6['values'][G['ID']], unit_6['strings'][G['U_LEVELFILE']], unit_6['strings'][G['U_LEVELNAME']], unit_6['values'][G['VISUALLEVEL']], unit_6['values'][G['COMPLETED']], unit_6['values'][G['VISUALSTYLE']], unit_6['flags'][G['MAPLEVEL']], unit_6['strings'][G['COLOUR']], unit_6['strings'][G['CLEARCOLOUR']], unit_6['followed'], unit_6['back_init'], unit_6['originalname'], unit_6['strings'][G['UNITSIGNTEXT']], unit_6['holder']]))
									for a_12, b_10 in L_ipairs(delname):
										G['MF_alert'](L_concat('added undo for ', b_10[1], ' with ID ', L_tostring(b_10[2])))
										G['addundo'](L_T(['create', b_10[1], b_10[2], b_10[2], 'back', b_10[3], b_10[4], b_10[5]]))
									G['delunit'](unitid_2)
									G['dynamic'](unitid_2)
									G['MF_specialremove'](unitid_2, 2)
			G['doupdate']()
			for i_8, unitid_3 in L_ipairs(istele):
				if (G['isgone'](unitid_3) is False):
					unit_7 = G['mmf']['newObject'](unitid_3)
					name_6 = G['getname'](unit_7)
					x_5, y_5 = unit_7['values'][G['XPOS']], unit_7['values'][G['YPOS']]
					targets = G['findallhere'](x_5, y_5)
					telethis = False
					telethisx, telethisy = 0, 0
					if (L_len(targets) > 0):
						for i_9, v_3 in L_ipairs(targets):
							vunit_2 = G['mmf']['newObject'](v_3)
							thistype = vunit_2['strings'][G['UNITTYPE']]
							vname = vunit_2['strings'][G['UNITNAME']]
							targetvalid = G['isgone'](v_3)
							targetstill = G['hasfeature'](vname, 'is', 'still', v_3, x_5, y_5)
							if (((targetstill is None) and L_t(G['floating'](v_3, unitid_3, x_5, y_5))) and (vunit_2['flags'][G['DEAD']] is False)):
								targetname = G['getname'](vunit_2)
								if (G['objectdata'][v_3] is None):
									G['objectdata'][v_3] = L_T()
								odata_2 = G['objectdata'][v_3]
								if (odata_2['tele'] is None):
									if ((targetname != name_6) and (v_3 != unitid_3)):
										teles = istele
										if (L_len(teles) > 1):
											teletargets = L_T()
											targettele = 0
											for a_13, b_11 in L_ipairs(teles):
												tele = G['mmf']['newObject'](b_11)
												telename = G['getname'](tele)
												if (((b_11 != unitid_3) and (telename == name_6)) and (tele['flags'][G['DEAD']] is False)):
													L_insert(teletargets, b_11)
											if (L_len(teletargets) > 0):
												randomtarget = G['fixedrandom'](1, L_len(teletargets))
												targettele = teletargets[randomtarget]
												limit = 0
												while ((targettele == unitid_3) and (limit < 10)):
													randomtarget = G['fixedrandom'](1, L_len(teletargets))
													targettele = teletargets[randomtarget]
													limit = (limit + 1)
												odata_2['tele'] = 1
												tele_2 = G['mmf']['newObject'](targettele)
												tx, ty = tele_2['values'][G['XPOS']], tele_2['values'][G['YPOS']]
												vx, vy = vunit_2['values'][G['XPOS']], vunit_2['values'][G['YPOS']]
												G['update'](v_3, tx, ty)
												pmult, sound = L_adjust((*G['checkeffecthistory']('tele'),), 2)
												G['MF_particles']('glow', vx, vy, (5 * pmult), 1, 4, 1, 1)
												G['MF_particles']('glow', tx, ty, (5 * pmult), 1, 4, 1, 1)
												G['setsoundname']('turn', 6, sound)
			for a_14, unitid_4 in L_ipairs(isshift):
				if ((unitid_4 != 2) and (unitid_4 != 1)):
					unit_8 = G['mmf']['newObject'](unitid_4)
					x_6, y_6, dir__4 = unit_8['values'][G['XPOS']], unit_8['values'][G['YPOS']], unit_8['values'][G['DIR']]
					things = G['findallhere'](x_6, y_6, unitid_4)
					if ((L_len(things) > 0) and (G['isgone'](unitid_4) is False)):
						for e, f in L_ipairs(things):
							if (L_t(G['floating'](unitid_4, f, x_6, y_6)) and (G['issleep'](unitid_4, x_6, y_6) is False)):
								newunit_2 = G['mmf']['newObject'](f)
								name_7 = newunit_2['strings'][G['UNITNAME']]
								if (G['featureindex']['reverse'] is not None):
									turndir = unit_8['values'][G['DIR']]
									turndir = L_first(G['reversecheck'](newunit_2['fixed'], unit_8['values'][G['DIR']], x_6, y_6))
								if (newunit_2['flags'][G['DEAD']] is False):
									G['addundo'](L_T(['update', name_7, x_6, y_6, newunit_2['values'][G['DIR']], x_6, y_6, unit_8['values'][G['DIR']], newunit_2['values'][G['ID']]]))
									newunit_2['values'][G['DIR']] = unit_8['values'][G['DIR']]
			G['doupdate']()
	G['moveblock'] = f_moveblock
	def f_fallblock(*_):  # L850
		checks = L_T()
		isfall = L_first(G['findallfeature'](None, 'is', 'fall', True))
		isfall_r = L_first(G['findallfeature'](None, 'is', 'fallright', True))
		isfall_u = L_first(G['findallfeature'](None, 'is', 'fallup', True))
		isfall_l = L_first(G['findallfeature'](None, 'is', 'fallleft', True))
		flist = L_T()
		flist['down'] = L_T()
		flist['right'] = L_T()
		flist['up'] = L_T()
		flist['left'] = L_T()
		fd, fr, fu, fl = flist['down'], flist['right'], flist['up'], flist['left']
		fdl = L_len(isfall)
		frl = L_len(isfall_r)
		ful = L_len(isfall_u)
		fll = L_len(isfall_l)
		if (G['featureindex']['reverse'] is not None):
			for a_15, unitid_5 in L_ipairs(isfall):
				if ((a_15 <= fdl) and (L_first(G['reversecheck'](unitid_5, 0)) > 0)):
					L_insert(isfall_u, unitid_5)
					isfall[a_15] = (-1)
			for a_16, unitid_6 in L_ipairs(isfall_r):
				if ((a_16 <= frl) and (L_first(G['reversecheck'](unitid_6, 0)) > 0)):
					L_insert(isfall_l, unitid_6)
					isfall_r[a_16] = (-1)
			for a_17, unitid_7 in L_ipairs(isfall_u):
				if ((a_17 <= ful) and (L_first(G['reversecheck'](unitid_7, 0)) > 0)):
					L_insert(isfall, unitid_7)
					isfall_u[a_17] = (-1)
			for a_18, unitid_8 in L_ipairs(isfall_l):
				if ((a_18 <= fll) and (L_first(G['reversecheck'](unitid_8, 0)) > 0)):
					L_insert(isfall_r, unitid_8)
					isfall_l[a_18] = (-1)
		for a_19, unitid_9 in L_ipairs(isfall):
			if (unitid_9 != (-1)):
				L_insert(checks, L_T([unitid_9, 3]))
				if (fd[unitid_9] is None):
					fd[unitid_9] = 1
				else:
					fd[unitid_9] = (fd[unitid_9] + 1)
		for a_20, unitid_10 in L_ipairs(isfall_r):
			if (unitid_10 != (-1)):
				L_insert(checks, L_T([unitid_10, 0]))
				if (fr[unitid_10] is None):
					fr[unitid_10] = 1
				else:
					fr[unitid_10] = (fr[unitid_10] + 1)
		for a_21, unitid_11 in L_ipairs(isfall_u):
			if (unitid_11 != (-1)):
				L_insert(checks, L_T([unitid_11, 1]))
				if (fu[unitid_11] is None):
					fu[unitid_11] = 1
				else:
					fu[unitid_11] = (fu[unitid_11] + 1)
				if (((fd[unitid_11] is not None) and (fd[unitid_11] > 0)) and (fu[unitid_11] > 0)):
					fd[unitid_11] = (fd[unitid_11] - 1)
					fu[unitid_11] = (fu[unitid_11] - 1)
		for a_22, unitid_12 in L_ipairs(isfall_l):
			if (unitid_12 != (-1)):
				L_insert(checks, L_T([unitid_12, 2]))
				if (fl[unitid_12] is None):
					fl[unitid_12] = 1
				else:
					fl[unitid_12] = (fl[unitid_12] + 1)
				if (((fr[unitid_12] is not None) and (fr[unitid_12] > 0)) and (fl[unitid_12] > 0)):
					fr[unitid_12] = (fr[unitid_12] - 1)
					fl[unitid_12] = (fl[unitid_12] - 1)
		done = False
		objdatalist = L_T()
		limiter = 0
		limit_2 = 6000
		while ((done is False) and (limiter < limit_2)):
			settled = True
			if (L_len(checks) > 0):
				for a_23, data in L_pairs(checks):
					unitid_13 = data[1]
					falldir = data[2]
					if (G['objectdata'][unitid_13] is None):
						G['objectdata'][unitid_13] = L_T()
					unit_9 = G['mmf']['newObject'](unitid_13)
					x_7, y_7, dir__5 = unit_9['values'][G['XPOS']], unit_9['values'][G['YPOS']], unit_9['values'][G['DIR']]
					name_8 = unit_9['strings'][G['UNITNAME']]
					drs = G['ndirs'][(falldir + 1)]
					ox_3, oy_3 = drs[1], drs[2]
					onground = False
					valid = False
					flistnames = L_T(['right', 'up', 'left', 'down'])
					flist_ = flist[flistnames[(falldir + 1)]]
					if ((flist_[unitid_13] is not None) and (flist_[unitid_13] > 0)):
						valid = True
					odata_3 = G['objectdata'][unitid_13]
					if ((odata_3['fallen'] is not None) and (odata_3['fallen'] != falldir)):
						valid = False
						onground = True
					if (odata_3['fallen'] is None):
						L_insert(objdatalist, L_T([unitid_13, falldir]))
					if (L_t(unit_9['flags'][G['DEAD']]) or L_t(G['cantmove'](name_8, unitid_13, falldir, x_7, y_7))):
						valid = False
					if (valid is not None and valid is not False):
						while (((onground is False) and (limiter < limit_2)) and L_t(G['inbounds']((x_7 + ox_3), (y_7 + oy_3)))):
							below, below_, specials = L_adjust((*G['check'](unitid_13, x_7, y_7, falldir, False, 'fall'),), 3)
							deletethese = L_T()
							result = 0
							for c_4, d_3 in L_pairs(below):
								if (d_3 != 0):
									result = 1
								else:
									if ((below_[c_4] != 0) and (result != 1)):
										if (result != 0):
											result = 2
										else:
											for e_2, f_2 in L_ipairs(specials):
												if (f_2[1] == below_[c_4]):
													result = 2
												if (f_2[2] == 'weak'):
													L_insert(deletethese, f_2[1])
							if (G['inbounds']((x_7 + ox_3), (y_7 + oy_3)) is False):
								result = 1
							if (result != 1):
								gone = False
								if (result == 0):
									G['update'](unitid_13, (x_7 + ox_3), (y_7 + oy_3))
								elif (result == 2):
									gone = G['move'](unitid_13, ox_3, oy_3, dir__5, specials, True, True, x_7, y_7)
								if (gone is False):
									x_7 = (x_7 + ox_3)
									y_7 = (y_7 + oy_3)
									settled = False
									for a_24, b_12 in L_ipairs(deletethese):
										G['delete'](b_12, x_7, y_7)
										pmult_2, sound_2 = L_adjust((*G['checkeffecthistory']('weak'),), 2)
										G['setsoundname']('removal', 1, sound_2)
										G['generaldata']['values'][G['SHAKE']] = 3
										G['MF_particles']('destroy', x_7, y_7, (5 * pmult_2), 0, 3, 1, 1)
									if L_t(unit_9['flags'][G['DEAD']]):
										onground = True
										settled = True
										L_remove(checks, a_23)
									else:
										G['update'](unitid_13, x_7, y_7)
								else:
									onground = True
							else:
								onground = True
							limiter = (limiter + 1)
					else:
						onground = True
				if (settled is not None and settled is not False):
					done = True
			else:
				done = True
		if (limiter >= limit_2):
			G['HACK_INFINITY'] = 200
			G['destroylevel']('infinity')
			return None
		for i_10, v_4 in L_ipairs(objdatalist):
			unitid_14 = v_4[1]
			falldir_2 = v_4[2]
			if (G['objectdata'][unitid_14] is None):
				G['objectdata'][unitid_14] = L_T()
			odata_4 = G['objectdata'][unitid_14]
			if (odata_4['fallen'] is None):
				odata_4['fallen'] = falldir_2
	G['fallblock'] = f_fallblock
	def f_block(small_=None, *_):  # L1125
		delthese = L_T()
		doned_2 = L_T()
		unitsnow = L_len(G['units'])
		removalsound = 1
		removalshort = ''
		small = (_t1 if L_t(_t1 := small_) else False)
		doremovalsound = False
		if (small is False):
			if (G['generaldata2']['values'][G['ENDINGGOING']] == 0):
				isdone = G['getunitswitheffect']('done', False, delthese)
				for id_, unit_10 in L_ipairs(isdone):
					L_insert(doned_2, unit_10)
				if (L_len(doned_2) > 0):
					G['setsoundname']('turn', 10)
				for i_11, unit_11 in L_ipairs(doned_2):
					G['updateundo'] = True
					ufloat = unit_11['values'][G['FLOAT']]
					ded = unit_11['flags'][G['DEAD']]
					unit_11['values'][G['FLOAT']] = 2
					unit_11['values'][G['EFFECTCOUNT']] = G['math']['random']((-10), 10)
					unit_11['values'][G['POSITIONING']] = 7
					unit_11['flags'][G['DEAD']] = True
					x_8, y_8 = unit_11['values'][G['XPOS']], unit_11['values'][G['YPOS']]
					if ((G['spritedata']['values'][G['VISION']] == 1) and (unit_11['values'][G['ID']] == G['spritedata']['values'][G['CAMTARGET']])):
						G['updatevisiontargets']()
					if ((ufloat != 2) and (ded is False)):
						G['addundo'](L_T(['done', unit_11['strings'][G['UNITNAME']], unit_11['values'][G['XPOS']], unit_11['values'][G['YPOS']], unit_11['values'][G['DIR']], unit_11['values'][G['ID']], unit_11['fixed'], ufloat, unit_11['originalname']]))
					G['delunit'](unit_11['fixed'])
					G['dynamicat'](x_8, y_8)
			ismore = G['getunitswitheffect']('more', False, delthese)
			for id__2, unit_12 in L_ipairs(ismore):
				x_9, y_9 = unit_12['values'][G['XPOS']], unit_12['values'][G['YPOS']]
				name_9 = unit_12['strings'][G['UNITNAME']]
				doblocks = L_T()
				for i_12 in L_range(1, 4):
					drs_2 = G['ndirs'][i_12]
					G['ox'] = drs_2[1]
					G['oy'] = drs_2[2]
					valid_2 = True
					obs = G['findobstacle']((x_9 + G['ox']), (y_9 + G['oy']))
					tileid = ((x_9 + G['ox']) + ((y_9 + G['oy']) * G['roomsizex']))
					if (L_len(obs) > 0):
						for a_25, b_13 in L_ipairs(obs):
							if (b_13 == (-1)):
								valid_2 = False
							elif ((b_13 != 0) and (b_13 != (-1))):
								bunit = G['mmf']['newObject'](b_13)
								obsname = bunit['strings'][G['UNITNAME']]
								obsstop = G['hasfeature'](obsname, 'is', 'stop', b_13, (x_9 + G['ox']), (y_9 + G['oy']))
								obspush = G['hasfeature'](obsname, 'is', 'push', b_13, (x_9 + G['ox']), (y_9 + G['oy']))
								obspull = G['hasfeature'](obsname, 'is', 'pull', b_13, (x_9 + G['ox']), (y_9 + G['oy']))
								if ((((obsstop is not None) or (obspush is not None)) or (obspull is not None)) or (obsname == name_9)):
									valid_2 = False
									break
					else:
						obsstop_2 = G['hasfeature']('empty', 'is', 'stop', 2, (x_9 + G['ox']), (y_9 + G['oy']))
						obspush_2 = G['hasfeature']('empty', 'is', 'push', 2, (x_9 + G['ox']), (y_9 + G['oy']))
						obspull_2 = G['hasfeature']('empty', 'is', 'pull', 2, (x_9 + G['ox']), (y_9 + G['oy']))
						if (((obsstop_2 is not None) or (obspush_2 is not None)) or (obspull_2 is not None)):
							valid_2 = False
					if (valid_2 is not None and valid_2 is not False):
						newunit_3 = G['copy'](unit_12['fixed'], (x_9 + G['ox']), (y_9 + G['oy']))
		isplay = G['getunitswithverb']('play', delthese)
		for id__3, ugroup in L_ipairs(isplay):
			sound_freq = ugroup[1]
			sound_units = ugroup[2]
			sound_name = ugroup[3]
			if (L_len(sound_units) > 0):
				ptunes = G['play_data']['tunes']
				pfreqs = G['play_data']['freqs']
				tune = 'beep'
				freq = (_t2 if L_t(_t2 := pfreqs[sound_freq]) else 24000)
				if (ptunes[sound_name] is not None):
					tune = ptunes[sound_name]
				G['MF_playsound_freq'](tune, freq)
				G['setsoundname']('turn', 11, None)
				if (sound_name != 'empty'):
					for a_26, unit_13 in L_ipairs(sound_units):
						x_10, y_10 = unit_13['values'][G['XPOS']], unit_13['values'][G['YPOS']]
						G['MF_particles']('music', unit_13['values'][G['XPOS']], unit_13['values'][G['YPOS']], 1, 0, 3, 3, 1)
		ishold = G['getunitswitheffect']('hold', False, delthese)
		holders = L_T()
		for id__4, unit_14 in L_ipairs(ishold):
			x_11, y_11 = unit_14['values'][G['XPOS']], unit_14['values'][G['YPOS']]
			tileid_2 = (x_11 + (y_11 * G['roomsizex']))
			holders[unit_14['values'][G['ID']]] = unit_14['fixed']
			if (G['unitmap'][tileid_2] is not None):
				water = G['findallhere'](x_11, y_11)
				if (L_len(water) > 0):
					for a_27, b_14 in L_ipairs(water):
						if L_t(G['floating'](b_14, unit_14['fixed'], x_11, y_11)):
							if (b_14 != unit_14['fixed']):
								bunit_2 = G['mmf']['newObject'](b_14)
								if (bunit_2['holder'] != unit_14['values'][G['ID']]):
									G['addundo'](L_T(['holder', bunit_2['values'][G['ID']], bunit_2['holder'], unit_14['values'][G['ID']]]), G['unitid'])
									bunit_2['holder'] = unit_14['values'][G['ID']]
		for i_13, unit_15 in L_ipairs(G['units']):
			if ((unit_15['holder'] is not None) and (unit_15['holder'] != 0)):
				if (holders[unit_15['holder']] is not None):
					unitid_15 = G['getunitid'](unit_15['holder'])
					bunit_3 = G['mmf']['newObject'](unitid_15)
					x_12, y_12 = bunit_3['values'][G['XPOS']], bunit_3['values'][G['YPOS']]
					name_10 = G['getname'](unit_15)
					hdir = 4
					ox_4 = (x_12 - unit_15['values'][G['XPOS']])
					oy_4 = (y_12 - unit_15['values'][G['YPOS']])
					if ((ox_4 > 0) and (oy_4 == 0)):
						hdir = 0
					elif ((ox_4 == 0) and (oy_4 < 0)):
						hdir = 1
					elif ((ox_4 < 0) and (oy_4 == 0)):
						hdir = 2
					elif ((ox_4 == 0) and (oy_4 > 0)):
						hdir = 3
					if (G['cantmove'](name_10, unit_15['fixed'], hdir, unit_15['values'][G['XPOS']], unit_15['values'][G['YPOS']]) is False):
						G['update'](unit_15['fixed'], x_12, y_12, unit_15['values'][G['DIR']])
						if (G['floating'](unit_15['fixed'], unitid_15, x_12, y_12) is False):
							G['addundo'](L_T(['holder', unit_15['values'][G['ID']], unit_15['holder'], 0]), unitid_15)
							unit_15['holder'] = 0
					else:
						G['addundo'](L_T(['holder', unit_15['values'][G['ID']], unit_15['holder'], 0]), unitid_15)
						unit_15['holder'] = 0
				else:
					G['addundo'](L_T(['holder', unit_15['values'][G['ID']], unit_15['holder'], 0]), G['unitid'])
					unit_15['holder'] = 0
			else:
				unit_15['holder'] = 0
		issink = G['getunitswitheffect']('sink', False, delthese)
		for id__5, unit_16 in L_ipairs(issink):
			x_13, y_13 = unit_16['values'][G['XPOS']], unit_16['values'][G['YPOS']]
			tileid_3 = (x_13 + (y_13 * G['roomsizex']))
			if (G['unitmap'][tileid_3] is not None):
				water_2 = G['findallhere'](x_13, y_13)
				sunk = False
				if (L_len(water_2) > 0):
					for a_28, b_15 in L_ipairs(water_2):
						if L_t(G['floating'](b_15, unit_16['fixed'], x_13, y_13)):
							if (b_15 != unit_16['fixed']):
								dosink = True
								for c_5, d_4 in L_ipairs(delthese):
									if ((d_4 == unit_16['fixed']) or (d_4 == b_15)):
										dosink = False
								safe1 = G['issafe'](b_15)
								safe2 = G['issafe'](unit_16['fixed'])
								if ((safe1 is not None and safe1 is not False) and (safe2 is not None and safe2 is not False)):
									dosink = False
								if (dosink is not None and dosink is not False):
									G['generaldata']['values'][G['SHAKE']] = 3
									if (safe1 is False):
										L_insert(delthese, b_15)
									pmult_3, sound_3 = L_adjust((*G['checkeffecthistory']('sink'),), 2)
									removalshort = sound_3
									removalsound = 3
									c1_3, c2_3 = L_adjust((*G['getcolour'](unit_16['fixed']),), 2)
									G['MF_particles']('destroy', x_13, y_13, (15 * pmult_3), c1_3, c2_3, 1, 1)
									if ((b_15 != unit_16['fixed']) and (safe2 is False)):
										sunk = True
				if (sunk is not None and sunk is not False):
					L_insert(delthese, unit_16['fixed'])
		delthese, doremovalsound = L_adjust((*G['handledels'](delthese, doremovalsound),), 2)
		isboom = G['getunitswitheffect']('boom', False, delthese)
		for id__6, unit_17 in L_ipairs(isboom):
			ux_3, uy_3 = unit_17['values'][G['XPOS']], unit_17['values'][G['YPOS']]
			sunk_2 = False
			doeffect = True
			if (G['issafe'](unit_17['fixed']) is False):
				sunk_2 = True
			else:
				doremovalsound = True
			name_11 = unit_17['strings'][G['UNITNAME']]
			if (unit_17['strings'][G['UNITTYPE']] == 'text'):
				name_11 = 'text'
			count = G['hasfeature_count'](name_11, 'is', 'boom', unit_17['fixed'], ux_3, uy_3)
			dim = L_min((count - 1), L_max(G['roomsizex'], G['roomsizey']))
			locs = L_T()
			if (dim <= 0):
				L_insert(locs, L_T([0, 0]))
			else:
				for g in L_range((-dim), dim):
					for h_2 in L_range((-dim), dim):
						L_insert(locs, L_T([g, h_2]))
			for a_29, b_16 in L_ipairs(locs):
				g_2 = b_16[1]
				h_3 = b_16[2]
				x_14 = (ux_3 + g_2)
				y_14 = (uy_3 + h_3)
				tileid_4 = (x_14 + (y_14 * G['roomsizex']))
				if ((G['unitmap'][tileid_4] is not None) and L_t(G['inbounds'](x_14, y_14, 1))):
					water_3 = G['findallhere'](x_14, y_14)
					if (L_len(water_3) > 0):
						for e_3, f_3 in L_ipairs(water_3):
							if L_t(G['floating'](f_3, unit_17['fixed'], x_14, y_14)):
								if (f_3 != unit_17['fixed']):
									doboom = True
									for c_6, d_5 in L_ipairs(delthese):
										if (d_5 == f_3):
											doboom = False
										elif (d_5 == unit_17['fixed']):
											sunk_2 = False
									if ((doboom is not None and doboom is not False) and (G['issafe'](f_3) is False)):
										L_insert(delthese, f_3)
										G['MF_particles']('smoke', x_14, y_14, 4, 0, 2, 1, 1)
			if (doeffect is not None and doeffect is not False):
				G['generaldata']['values'][G['SHAKE']] = 6
				pmult_4, sound_4 = L_adjust((*G['checkeffecthistory']('boom'),), 2)
				removalshort = sound_4
				removalsound = 1
				c1_4, c2_4 = L_adjust((*G['getcolour'](unit_17['fixed']),), 2)
				G['MF_particles']('smoke', ux_3, uy_3, (15 * pmult_4), c1_4, c2_4, 1, 1)
			if (sunk_2 is not None and sunk_2 is not False):
				L_insert(delthese, unit_17['fixed'])
		delthese, doremovalsound = L_adjust((*G['handledels'](delthese, doremovalsound),), 2)
		isweak = G['getunitswitheffect']('weak', False, delthese)
		for id__7, unit_18 in L_ipairs(isweak):
			if ((G['issafe'](unit_18['fixed']) is False) and (unit_18['new'] is False)):
				x_15, y_15 = unit_18['values'][G['XPOS']], unit_18['values'][G['YPOS']]
				stuff = G['findallhere'](x_15, y_15)
				if (L_len(stuff) > 0):
					for i_14, v_5 in L_ipairs(stuff):
						if L_t(G['floating'](v_5, unit_18['fixed'], x_15, y_15)):
							vunit_3 = G['mmf']['newObject'](v_5)
							thistype_2 = vunit_3['strings'][G['UNITTYPE']]
							if (v_5 != unit_18['fixed']):
								pmult_5, sound_5 = L_adjust((*G['checkeffecthistory']('weak'),), 2)
								G['MF_particles']('destroy', x_15, y_15, (5 * pmult_5), 0, 3, 1, 1)
								removalshort = sound_5
								removalsound = 1
								G['generaldata']['values'][G['SHAKE']] = 4
								L_insert(delthese, unit_18['fixed'])
								break
		delthese, doremovalsound = L_adjust((*G['handledels'](delthese, doremovalsound, True),), 2)
		ismelt = G['getunitswitheffect']('melt', False, delthese)
		for id__8, unit_19 in L_ipairs(ismelt):
			hot = G['findfeature'](None, 'is', 'hot')
			x_16, y_16 = unit_19['values'][G['XPOS']], unit_19['values'][G['YPOS']]
			if (hot is not None):
				for a_30, b_17 in L_ipairs(hot):
					lava = G['findtype'](b_17, x_16, y_16, 0)
					if ((L_len(lava) > 0) and (G['issafe'](unit_19['fixed']) is False)):
						for c_7, d_6 in L_ipairs(lava):
							if L_t(G['floating'](d_6, unit_19['fixed'], x_16, y_16)):
								pmult_6, sound_6 = L_adjust((*G['checkeffecthistory']('hot'),), 2)
								G['MF_particles']('smoke', x_16, y_16, (5 * pmult_6), 0, 1, 1, 1)
								G['generaldata']['values'][G['SHAKE']] = 5
								removalshort = sound_6
								removalsound = 9
								L_insert(delthese, unit_19['fixed'])
								break
		delthese, doremovalsound = L_adjust((*G['handledels'](delthese, doremovalsound, True),), 2)
		isyou = G['getunitswitheffect']('you', False, delthese)
		isyou2 = G['getunitswitheffect']('you2', False, delthese)
		isyou3 = G['getunitswitheffect']('3d', False, delthese)
		for i_15, v_6 in L_ipairs(isyou2):
			L_insert(isyou, v_6)
		for i_16, v_7 in L_ipairs(isyou3):
			L_insert(isyou, v_7)
		for id__9, unit_20 in L_ipairs(isyou):
			x_17, y_17 = unit_20['values'][G['XPOS']], unit_20['values'][G['YPOS']]
			defeat = G['findfeature'](None, 'is', 'defeat')
			if (defeat is not None):
				for a_31, b_18 in L_ipairs(defeat):
					if (b_18[1] != 'empty'):
						skull = G['findtype'](b_18, x_17, y_17, 0)
						if ((L_len(skull) > 0) and (G['issafe'](unit_20['fixed']) is False)):
							for c_8, d_7 in L_ipairs(skull):
								doit = False
								if (d_7 != unit_20['fixed']):
									if L_t(G['floating'](d_7, unit_20['fixed'], x_17, y_17)):
										kunit = G['mmf']['newObject'](d_7)
										kname = kunit['strings'][G['UNITNAME']]
										weakskull = G['hasfeature'](kname, 'is', 'weak', d_7)
										if ((weakskull is None) or ((weakskull is not None) and L_t(G['issafe'](d_7)))):
											doit = True
								else:
									doit = True
								if (doit is not None and doit is not False):
									pmult_7, sound_7 = L_adjust((*G['checkeffecthistory']('defeat'),), 2)
									G['MF_particles']('destroy', x_17, y_17, (5 * pmult_7), 0, 3, 1, 1)
									G['generaldata']['values'][G['SHAKE']] = 5
									removalshort = sound_7
									removalsound = 1
									L_insert(delthese, unit_20['fixed'])
		delthese, doremovalsound = L_adjust((*G['handledels'](delthese, doremovalsound),), 2)
		isshut = G['getunitswitheffect']('shut', False, delthese)
		for id__10, unit_21 in L_ipairs(isshut):
			open = G['findfeature'](None, 'is', 'open')
			x_18, y_18 = unit_21['values'][G['XPOS']], unit_21['values'][G['YPOS']]
			if (open is not None):
				for i_17, v_8 in L_ipairs(open):
					key = G['findtype'](v_8, x_18, y_18, 0)
					if (L_len(key) > 0):
						doparts = False
						for a_32, b_19 in L_ipairs(key):
							if ((b_19 != 0) and L_t(G['floating'](b_19, unit_21['fixed'], x_18, y_18))):
								if (G['issafe'](unit_21['fixed']) is False):
									G['generaldata']['values'][G['SHAKE']] = 8
									L_insert(delthese, unit_21['fixed'])
									doparts = True
									G['online'] = False
								if ((b_19 != unit_21['fixed']) and (G['issafe'](b_19) is False)):
									L_insert(delthese, b_19)
									doparts = True
								if (doparts is not None and doparts is not False):
									pmult_8, sound_8 = L_adjust((*G['checkeffecthistory']('unlock'),), 2)
									G['setsoundname']('turn', 7, sound_8)
									G['MF_particles']('unlock', x_18, y_18, (15 * pmult_8), 2, 4, 1, 1)
								break
		delthese, doremovalsound = L_adjust((*G['handledels'](delthese, doremovalsound),), 2)
		iseat = G['getunitswithverb']('eat', delthese)
		iseaten = L_T()
		for id__11, ugroup_2 in L_ipairs(iseat):
			v_9 = ugroup_2[1]
			if (ugroup_2[3] != 'empty'):
				for a_33, unit_22 in L_ipairs(ugroup_2[2]):
					x_19, y_19 = unit_22['values'][G['XPOS']], unit_22['values'][G['YPOS']]
					things_2 = G['findtype'](L_T([v_9, None]), x_19, y_19, unit_22['fixed'])
					if (L_len(things_2) > 0):
						for a_34, b_20 in L_ipairs(things_2):
							if ((((G['issafe'](b_20) is False) and L_t(G['floating'](b_20, unit_22['fixed'], x_19, y_19))) and (b_20 != unit_22['fixed'])) and (iseaten[b_20] is None)):
								G['generaldata']['values'][G['SHAKE']] = 4
								L_insert(delthese, b_20)
								iseaten[b_20] = 1
								pmult_9, sound_9 = L_adjust((*G['checkeffecthistory']('eat'),), 2)
								G['MF_particles']('eat', x_19, y_19, (5 * pmult_9), 0, 3, 1, 1)
								removalshort = sound_9
								removalsound = 1
		delthese, doremovalsound = L_adjust((*G['handledels'](delthese, doremovalsound, True),), 2)
		if (small is False):
			ismake = G['getunitswithverb']('make', delthese)
			for id__12, ugroup_3 in L_ipairs(ismake):
				v_10 = ugroup_3[1]
				for a_35, unit_23 in L_ipairs(ugroup_3[2]):
					x_20, y_20, dir__6, name_12 = 0, 0, 4, ''
					leveldata = L_T()
					if (ugroup_3[3] != 'empty'):
						x_20, y_20, dir__6 = unit_23['values'][G['XPOS']], unit_23['values'][G['YPOS']], unit_23['values'][G['DIR']]
						name_12 = G['getname'](unit_23)
						leveldata = L_T([unit_23['strings'][G['U_LEVELFILE']], unit_23['strings'][G['U_LEVELNAME']], unit_23['flags'][G['MAPLEVEL']], unit_23['values'][G['VISUALLEVEL']], unit_23['values'][G['VISUALSTYLE']], unit_23['values'][G['COMPLETED']], unit_23['strings'][G['COLOUR']], unit_23['strings'][G['CLEARCOLOUR']]])
					else:
						x_20 = L_floor((unit_23 % G['roomsizex']))
						y_20 = L_floor(L_div(unit_23, G['roomsizex']))
						name_12 = 'empty'
						dir__6 = G['emptydir'](x_20, y_20)
					if (dir__6 == 4):
						dir__6 = G['fixedrandom'](0, 3)
					exists = False
					if ((v_10 != 'text') and (v_10 != 'all')):
						for b_21, mat in L_pairs(G['objectlist']):
							if (b_21 == v_10):
								exists = True
					else:
						exists = True
					if (exists is not None and exists is not False):
						domake = True
						if (name_12 != 'empty'):
							thingshere = G['findallhere'](x_20, y_20)
							if (L_len(thingshere) > 0):
								for a_36, b_22 in L_ipairs(thingshere):
									thing = G['mmf']['newObject'](b_22)
									thingname = thing['strings'][G['UNITNAME']]
									if ((thing['flags'][G['CONVERTED']] is False) and ((thingname == v_10) or ((thing['strings'][G['UNITTYPE']] == 'text') and (v_10 == 'text')))):
										domake = False
						if (domake is not None and domake is not False):
							if (G['findnoun'](v_10, G['nlist']['short']) is False):
								G['create'](v_10, x_20, y_20, dir__6, x_20, y_20, None, None, leveldata)
							elif (v_10 == 'text'):
								if ((name_12 != 'text') and (name_12 != 'all')):
									G['create'](L_concat('text_', name_12), x_20, y_20, dir__6, x_20, y_20, None, None, leveldata)
									G['updatecode'] = 1
							elif (L_sub(v_10, 1, 5) == 'group'):
								pass
		delthese, doremovalsound = L_adjust((*G['handledels'](delthese, doremovalsound),), 2)
		if (G['featureindex']['hold'] is not None):
			ishold_2 = G['getunitswitheffect']('hold', False, delthese)
			holders_2 = L_T()
			for id__13, unit_24 in L_ipairs(ishold_2):
				x_21, y_21 = unit_24['values'][G['XPOS']], unit_24['values'][G['YPOS']]
				tileid_5 = (x_21 + (y_21 * G['roomsizex']))
				holders_2[unit_24['values'][G['ID']]] = 1
				if (G['unitmap'][tileid_5] is not None):
					water_4 = G['findallhere'](x_21, y_21)
					if (L_len(water_4) > 0):
						for a_37, b_23 in L_ipairs(water_4):
							if L_t(G['floating'](b_23, unit_24['fixed'], x_21, y_21)):
								if (b_23 != unit_24['fixed']):
									bunit_4 = G['mmf']['newObject'](b_23)
									G['addundo'](L_T(['holder', bunit_4['values'][G['ID']], bunit_4['holder'], unit_24['values'][G['ID']]]), G['unitid'])
									bunit_4['holder'] = unit_24['values'][G['ID']]
			for i_18, unit_25 in L_ipairs(G['units']):
				if ((unit_25['holder'] is not None) and (unit_25['holder'] != 0)):
					if (holders_2[unit_25['holder']] is not None):
						unitid_16 = G['getunitid'](unit_25['holder'])
						bunit_5 = G['mmf']['newObject'](unitid_16)
						x_22, y_22 = bunit_5['values'][G['XPOS']], bunit_5['values'][G['YPOS']]
						G['update'](unit_25['fixed'], x_22, y_22, unit_25['values'][G['DIR']])
					else:
						G['addundo'](L_T(['holder', unit_25['values'][G['ID']], unit_25['holder'], 0]), G['unitid'])
						unit_25['holder'] = 0
				else:
					unit_25['holder'] = 0
		isyou = G['getunitswitheffect']('you', False, delthese)
		isyou2 = G['getunitswitheffect']('you2', False, delthese)
		isyou3 = G['getunitswitheffect']('3d', False, delthese)
		for i_19, v_11 in L_ipairs(isyou2):
			L_insert(isyou, v_11)
		for i_20, v_12 in L_ipairs(isyou3):
			L_insert(isyou, v_12)
		for id__14, unit_26 in L_ipairs(isyou):
			if ((unit_26['flags'][G['DEAD']] is False) and (delthese[unit_26['fixed']] is None)):
				x_23, y_23 = unit_26['values'][G['XPOS']], unit_26['values'][G['YPOS']]
				if (small is False):
					bonus = G['findfeature'](None, 'is', 'bonus')
					if (bonus is not None):
						for a_38, b_24 in L_ipairs(bonus):
							if (b_24[1] != 'empty'):
								flag = G['findtype'](b_24, x_23, y_23, 0)
								if (L_len(flag) > 0):
									for c_9, d_8 in L_ipairs(flag):
										if L_t(G['floating'](d_8, unit_26['fixed'], x_23, y_23)):
											pmult_10, sound_10 = L_adjust((*G['checkeffecthistory']('bonus'),), 2)
											G['MF_particles']('bonus', x_23, y_23, (10 * pmult_10), 4, 1, 1, 1)
											removalshort = sound_10
											removalsound = 2
											G['MF_playsound']('bonus')
											G['MF_bonus'](1)
											G['addundo'](L_T(['bonus', 1]))
											if (G['issafe'](d_8, x_23, y_23) is False):
												G['generaldata']['values'][G['SHAKE']] = 5
												L_insert(delthese, d_8)
					ending = G['findfeature'](None, 'is', 'end')
					if (ending is not None):
						for a_39, b_25 in L_ipairs(ending):
							if (b_25[1] != 'empty'):
								flag_2 = G['findtype'](b_25, x_23, y_23, 0)
								if (L_len(flag_2) > 0):
									for c_10, d_9 in L_ipairs(flag_2):
										if (L_t(G['floating'](d_9, unit_26['fixed'], x_23, y_23)) and (G['generaldata']['values'][G['MODE']] == 0)):
											if (G['generaldata']['strings'][G['WORLD']] == G['generaldata']['strings'][G['BASEWORLD']]):
												G['MF_particles']('unlock', x_23, y_23, 10, 1, 4, 1, 1)
												G['MF_end'](unit_26['fixed'], d_9)
												break
											elif (G['editor']['values'][G['INEDITOR']] != 0):
												pmult_11 = L_first(G['checkeffecthistory']('win'))
												G['MF_particles']('win', x_23, y_23, (10 * pmult_11), 2, 4, 1, 1)
												G['MF_end_single']()
												G['MF_win']()
												break
											else:
												pmult_12 = L_first(G['checkeffecthistory']('win'))
												mods_run = G['do_mod_hook']('levelpack_end', L_T())
												if (mods_run is False):
													G['MF_particles']('win', x_23, y_23, (10 * pmult_12), 2, 4, 1, 1)
													G['MF_end_single']()
													G['MF_win']()
													G['MF_credits'](1)
												break
				win = G['findfeature'](None, 'is', 'win')
				if (win is not None):
					for a_40, b_26 in L_ipairs(win):
						if (b_26[1] != 'empty'):
							flag_3 = G['findtype'](b_26, x_23, y_23, 0)
							if (L_len(flag_3) > 0):
								for c_11, d_10 in L_ipairs(flag_3):
									if ((L_t(G['floating'](d_10, unit_26['fixed'], x_23, y_23)) and (G['hasfeature'](b_26[1], 'is', 'done', d_10, x_23, y_23) is None)) and (G['hasfeature'](b_26[1], 'is', 'end', d_10, x_23, y_23) is None)):
										pmult_13 = L_first(G['checkeffecthistory']('win'))
										G['MF_particles']('win', x_23, y_23, (10 * pmult_13), 2, 4, 1, 1)
										G['MF_win']()
										break
		delthese, doremovalsound = L_adjust((*G['handledels'](delthese, doremovalsound),), 2)
		G['do_mod_hook']('block')
		for i_21, unit_27 in L_ipairs(G['units']):
			if (G['inbounds'](unit_27['values'][G['XPOS']], unit_27['values'][G['YPOS']], 1) is False):
				L_insert(delthese, unit_27['fixed'])
		delthese, doremovalsound = L_adjust((*G['handledels'](delthese, doremovalsound),), 2)
		if (small is False):
			iscrash = G['getunitswitheffect']('crash', False, delthese)
			if (L_len(iscrash) > 0):
				G['HACK_INFINITY'] = 200
				G['destroylevel']('infinity')
				return None
		if (doremovalsound is not None and doremovalsound is not False):
			G['setsoundname']('removal', removalsound, removalshort)
	G['block'] = f_block
	def f_handledels(delthese_2=None, doremovalsound_2=None, simultaneous=None, *_):  # L1927
		result_2 = (_t1 if L_t(_t1 := doremovalsound_2) else False)
		simult = (_t2 if L_t(_t2 := simultaneous) else False)
		if (simult is not None and simult is not False):
			for i_22, uid_3 in L_pairs(delthese_2):
				if (G['deleted'][uid_3] is None):
					G['handleinside'](uid_3)
		for i_23, uid_4 in L_pairs(delthese_2):
			result_2 = True
			if (G['deleted'][uid_4] is None):
				G['delete'](uid_4, None, None, None, simult)
				G['deleted'][uid_4] = 1
		return (L_T(), result_2,)
		return ()
	G['handledels'] = f_handledels
	def f_startblock(light_=None, *_):  # L1951
		light = (_t1 if L_t(_t1 := light_) else False)
		G['diceblock']()
		if (light is False):
			G['generaldata5']['values'][G['AUTO_ON']] = 0
			G['destroylevel_check'] = False
			G['destroylevel_style'] = ''
			if (G['featureindex']['level'] is not None):
				auto_on_2 = G['hasfeature_count']('level', 'is', 'auto', 1)
				if (auto_on_2 is not None):
					G['generaldata5']['values'][G['AUTO_ON']] = auto_on_2
		if ((light is False) and (G['featureindex']['level'] is not None)):
			G['MF_levelrotation'](0)
			G['maprotation'] = 0
			for i_24, v_13 in L_ipairs(G['featureindex']['level']):
				rule_3 = v_13[1]
				conds_4 = v_13[2]
				if L_t(G['testcond'](conds_4, 1)):
					if ((rule_3[1] == 'level') and (rule_3[2] == 'is')):
						if (rule_3[3] == 'right'):
							G['maprotation'] = 90
							G['mapdir'] = 0
							G['MF_levelrotation'](90)
						elif (rule_3[3] == 'up'):
							G['maprotation'] = 180
							G['mapdir'] = 1
							G['MF_levelrotation'](180)
						elif (rule_3[3] == 'left'):
							G['maprotation'] = 270
							G['mapdir'] = 2
							G['MF_levelrotation'](270)
						elif (rule_3[3] == 'down'):
							G['maprotation'] = 0
							G['mapdir'] = 3
							G['MF_levelrotation'](0)
		for i_25, unit_28 in L_ipairs(G['units']):
			name_13 = unit_28['strings'][G['UNITNAME']]
			unitid_17 = unit_28['fixed']
			unitrules_2 = L_T()
			if (unit_28['strings'][G['UNITTYPE']] == 'text'):
				name_13 = 'text'
			if (G['featureindex'][name_13] is not None):
				for a_41, b_27 in L_ipairs(G['featureindex'][name_13]):
					conds_5 = b_27[2]
					if L_t(G['testcond'](conds_5, unitid_17)):
						L_insert(unitrules_2, b_27)
				isfloat_2 = G['isthis'](unitrules_2, 'float')
				sleep = G['isthis'](unitrules_2, 'sleep')
				if (isfloat_2 is not None and isfloat_2 is not False):
					unit_28['values'][G['FLOAT']] = 1
				if (sleep is not None and sleep is not False):
					if (unit_28['values'][G['TILING']] == 2):
						unit_28['values'][G['VISUALDIR']] = (-1)
						unit_28['direction'] = ((((unit_28['values'][G['DIR']] * 8) + unit_28['values'][G['VISUALDIR']]) + 32) % 32)
		G['moveblock'](True)
		G['effectblock']()
		G['newundo']()
	G['startblock'] = f_startblock
	def f_visionblock(*_):  # L2066
		vistest, vt2 = L_adjust((*G['findallfeature'](None, 'is', '3d', True),), 2)
		if ((L_len(vistest) > 0) or (L_len(vt2) > 0)):
			G['visionmode'](1, None, True)
		else:
			G['visionmode'](0, None, True)
	G['visionblock'] = f_visionblock
	def f_levelblock(*_):  # L2075
		unlocked = False
		things_3 = L_T()
		donethings = L_T()
		delthese_3 = L_T()
		edelthese = L_T()
		emptythings = L_T()
		if (G['destroylevel_check'] is False):
			if (G['featureindex']['level'] is not None):
				for i_26, v_14 in L_ipairs(G['featureindex']['level']):
					L_insert(things_3, v_14)
			if (G['featureindex']['empty'] is not None):
				for i_27, v_15 in L_ipairs(G['featureindex']['empty']):
					rule_4 = v_15[1]
					if ((rule_4[1] == 'empty') and ((rule_4[2] == 'is') or (rule_4[2] == 'eat'))):
						L_insert(emptythings, v_15)
			lstill = G['isstill_or_locked'](1, None, None, G['mapdir'])
			lsleep = G['issleep'](1)
			lsafe = G['issafe'](1)
			emptybonus = False
			emptydone = False
			ewintiles = L_T()
			eendtiles = L_T()
			levelteledone = 0
			if (L_len(emptythings) > 0):
				for i_28 in L_range(1, (G['roomsizex'] - 2)):
					for j_2 in L_range(1, (G['roomsizey'] - 2)):
						tileid_6 = (i_28 + (j_2 * G['roomsizex']))
						if ((G['unitmap'][tileid_6] is None) or (L_len(G['unitmap'][tileid_6]) == 0)):
							esafe = G['issafe'](2, i_28, j_2)
							keypair = ''
							winpair = ''
							hotpair = ''
							defeatpair = ''
							bonuspair = ''
							endpair = ''
							canmelt = False
							candefeat = False
							canwin = False
							canbonus = False
							canend = False
							unlock = False
							victory = False
							melt = False
							defeat_2 = False
							bonus_2 = False
							ending_2 = False
							emptyboom = False
							for a_42, rules in L_ipairs(emptythings):
								rule_5 = rules[1]
								conds_6 = rules[2]
								if (rule_5[2] == 'is'):
									if ((rule_5[3] == 'open') and L_t(G['testcond'](conds_6, 2, i_28, j_2))):
										if (L_strlen(keypair) == 0):
											keypair = 'shut'
										elif (keypair == 'open'):
											unlock = True
									elif ((rule_5[3] == 'shut') and L_t(G['testcond'](conds_6, 2, i_28, j_2))):
										if (L_strlen(keypair) == 0):
											keypair = 'open'
										elif (keypair == 'shut'):
											unlock = True
									if ((rule_5[3] == 'melt') and L_t(G['testcond'](conds_6, 2, i_28, j_2))):
										canmelt = True
										if (L_strlen(hotpair) == 0):
											hotpair = 'hot'
										elif (hotpair == 'melt'):
											melt = True
									elif ((rule_5[3] == 'hot') and L_t(G['testcond'](conds_6, 2, i_28, j_2))):
										if (L_strlen(hotpair) == 0):
											hotpair = 'melt'
										elif (hotpair == 'hot'):
											melt = True
									if ((rule_5[3] == 'defeat') and L_t(G['testcond'](conds_6, 2, i_28, j_2))):
										if (L_strlen(defeatpair) == 0):
											defeatpair = 'you'
										elif (defeatpair == 'defeat'):
											defeat_2 = True
									elif ((((rule_5[3] == 'you') or (rule_5[3] == 'you2')) or (rule_5[3] == '3d')) and L_t(G['testcond'](conds_6, 2, i_28, j_2))):
										candefeat = True
										canwin = True
										if (L_strlen(defeatpair) == 0):
											defeatpair = 'defeat'
										elif (defeatpair == 'you'):
											defeat_2 = True
									if ((rule_5[3] == 'win') and L_t(G['testcond'](conds_6, 2, i_28, j_2))):
										if (L_strlen(winpair) == 0):
											winpair = 'you'
										elif (winpair == 'win'):
											victory = True
									elif ((((rule_5[3] == 'you') or (rule_5[3] == 'you2')) or (rule_5[3] == '3d')) and L_t(G['testcond'](conds_6, 2, i_28, j_2))):
										candefeat = True
										canwin = True
										if (L_strlen(winpair) == 0):
											winpair = 'win'
										elif (winpair == 'you'):
											victory = True
									if ((rule_5[3] == 'bonus') and L_t(G['testcond'](conds_6, 2, i_28, j_2))):
										if (L_strlen(bonuspair) == 0):
											bonuspair = 'you'
										elif (bonuspair == 'bonus'):
											bonus_2 = True
										canbonus = True
									elif ((((rule_5[3] == 'you') or (rule_5[3] == 'you2')) or (rule_5[3] == '3d')) and L_t(G['testcond'](conds_6, 2, i_28, j_2))):
										if (L_strlen(bonuspair) == 0):
											bonuspair = 'bonus'
										elif (bonuspair == 'you'):
											bonus_2 = True
									if ((rule_5[3] == 'end') and L_t(G['testcond'](conds_6, 2, i_28, j_2))):
										if (L_strlen(endpair) == 0):
											endpair = 'you'
										elif (bonuspair == 'end'):
											ending_2 = True
										canend = True
									elif ((((rule_5[3] == 'you') or (rule_5[3] == 'you2')) or (rule_5[3] == '3d')) and L_t(G['testcond'](conds_6, 2, i_28, j_2))):
										if (L_strlen(endpair) == 0):
											endpair = 'end'
										elif (endpair == 'you'):
											ending_2 = True
									if ((rule_5[3] == 'done') and L_t(G['testcond'](conds_6, 2, i_28, j_2))):
										emptydone = True
									if ((rule_5[3] == 'boom') and L_t(G['testcond'](conds_6, 2, i_28, j_2))):
										emptyboom = True
									if (((keypair == 'shut') and (G['hasfeature']('level', 'is', 'shut', 1, i_28, j_2) is not None)) and L_t(G['floating_level'](2, i_28, j_2))):
										unlock = True
									elif (((keypair == 'open') and (G['hasfeature']('level', 'is', 'open', 1, i_28, j_2) is not None)) and L_t(G['floating_level'](2, i_28, j_2))):
										unlock = True
									if (((canmelt is not None and canmelt is not False) and (G['hasfeature']('level', 'is', 'hot', 1, i_28, j_2) is not None)) and L_t(G['floating_level'](2, i_28, j_2))):
										melt = True
									if (((candefeat is not None and candefeat is not False) and (G['hasfeature']('level', 'is', 'defeat', 1, i_28, j_2) is not None)) and L_t(G['floating_level'](2, i_28, j_2))):
										defeat_2 = True
									if (((canwin is not None and canwin is not False) and (G['hasfeature']('level', 'is', 'win', 1, i_28, j_2) is not None)) and L_t(G['floating_level'](2, i_28, j_2))):
										victory = True
									if (((canbonus is not None and canbonus is not False) and (((G['hasfeature']('level', 'is', 'you', 1, i_28, j_2) is not None) or (G['hasfeature']('level', 'is', 'you2', 1, i_28, j_2) is not None)) or (G['hasfeature']('level', 'is', '3d', 1, i_28, j_2) is not None))) and L_t(G['floating_level'](2, i_28, j_2))):
										bonus_2 = True
									if (((canend is not None and canend is not False) and (((G['hasfeature']('level', 'is', 'you', 1, i_28, j_2) is not None) or (G['hasfeature']('level', 'is', 'you2', 1, i_28, j_2) is not None)) or (G['hasfeature']('level', 'is', '3d', 1, i_28, j_2) is not None))) and L_t(G['floating_level'](2, i_28, j_2))):
										ending_2 = True
									if (victory is not None and victory is not False):
										L_insert(ewintiles, L_T([i_28, j_2]))
									if (ending_2 is not None and ending_2 is not False):
										L_insert(eendtiles, L_T([i_28, j_2]))
								elif (((rule_5[2] == 'eat') and (rule_5[3] == 'level')) and (lsafe is False)):
									if (L_t(G['testcond'](conds_6, 2, i_28, j_2)) and L_t(G['floating_level'](2, i_28, j_2))):
										pmult_14, sound_11 = L_adjust((*G['checkeffecthistory']('eat'),), 2)
										G['setsoundname']('removal', 1, sound_11)
										G['destroylevel']()
										return None
							if (emptyboom is not None and emptyboom is not False):
								count_2 = G['hasfeature_count']('empty', 'is', 'boom', 2, i_28, j_2)
								dim_2 = L_min((count_2 - 1), L_max(G['roomsizex'], G['roomsizey']))
								locs_2 = L_T()
								if (dim_2 <= 0):
									L_insert(locs_2, L_T([0, 0]))
								else:
									for g_3 in L_range((-dim_2), dim_2):
										for h_4 in L_range((-dim_2), dim_2):
											L_insert(locs_2, L_T([g_3, h_4]))
								for a_43, b_28 in L_ipairs(locs_2):
									g_4 = b_28[1]
									h_5 = b_28[2]
									x_24 = (i_28 + g_4)
									y_24 = (j_2 + h_5)
									tileid_7 = (x_24 + (y_24 * G['roomsizex']))
									if ((G['unitmap'][tileid_7] is not None) and L_t(G['inbounds'](x_24, y_24, 1))):
										water_5 = G['findallhere'](x_24, y_24)
										if (L_len(water_5) > 0):
											for e_4, f_4 in L_ipairs(water_5):
												if L_t(G['floating'](f_4, 2, x_24, y_24)):
													doboom_2 = True
													for c_12, d_11 in L_ipairs(delthese_3):
														if (d_11 == f_4):
															doboom_2 = False
													if ((doboom_2 is not None and doboom_2 is not False) and (G['issafe'](f_4) is False)):
														L_insert(delthese_3, f_4)
														G['MF_particles']('smoke', x_24, y_24, 4, 0, 2, 1, 1)
								pmult_15, sound_12 = L_adjust((*G['checkeffecthistory']('boom'),), 2)
								G['MF_particles']('smoke', i_28, j_2, (2 * pmult_15), 0, 3, 1, 1)
								G['setsoundname']('removal', 1)
								if (esafe is False):
									L_insert(edelthese, L_T([i_28, j_2]))
							alive = True
							if (((unlock is not None and unlock is not False) and (esafe is False)) and (alive is not None and alive is not False)):
								G['setsoundname']('turn', 7)
								if (G['math']['random'](1, 4) == 1):
									G['MF_particles']('unlock', i_28, j_2, 1, 2, 4, 1, 1)
								alive = False
								L_insert(edelthese, L_T([i_28, j_2]))
							if (((melt is not None and melt is not False) and (esafe is False)) and (alive is not None and alive is not False)):
								G['setsoundname']('turn', 9)
								if (G['math']['random'](1, 4) == 1):
									G['MF_particles']('smoke', i_28, j_2, 1, 0, 1, 1, 1)
								alive = False
								L_insert(edelthese, L_T([i_28, j_2]))
							if (((defeat_2 is not None and defeat_2 is not False) and (esafe is False)) and (alive is not None and alive is not False)):
								G['setsoundname']('turn', 1)
								if (G['math']['random'](1, 4) == 1):
									G['MF_particles']('destroy', i_28, j_2, 1, 0, 3, 1, 1)
								alive = False
								L_insert(edelthese, L_T([i_28, j_2]))
							if ((bonus_2 is not None and bonus_2 is not False) and (esafe is False)):
								if (alive is not None and alive is not False):
									G['setsoundname']('turn', 2)
									if (G['math']['random'](1, 4) == 1):
										G['MF_particles']('win', i_28, j_2, 1, 4, 2, 1, 1)
									alive = False
									L_insert(edelthese, L_T([i_28, j_2]))
								if (emptybonus is False):
									G['MF_playsound']('bonus')
									G['MF_bonus'](1)
									G['addundo'](L_T(['bonus', 1]))
									emptybonus = True
							if ((victory is not None and victory is not False) and (alive is not None and alive is not False)):
								G['MF_win']()
								return None
							if (((ending_2 is not None and ending_2 is not False) and (alive is not None and alive is not False)) and (G['generaldata']['strings'][G['WORLD']] != G['generaldata']['strings'][G['BASEWORLD']])):
								if (G['editor']['values'][G['INEDITOR']] != 0):
									G['MF_end_single']()
									G['MF_win']()
									return None
								else:
									G['MF_end_single']()
									G['MF_win']()
									G['MF_credits'](1)
									return None
			if (emptydone is not None and emptydone is not False):
				donenum = G['math']['random'](1, 4)
				G['MF_playsound'](L_concat('done', L_tostring(donenum)))
			for a_44, b_29 in L_ipairs(delthese_3):
				bunit_6 = G['mmf']['newObject'](b_29)
				G['delete'](b_29, bunit_6['values'][G['XPOS']], bunit_6['values'][G['YPOS']])
			for a_45, b_30 in L_ipairs(edelthese):
				G['delete'](2, b_30[1], b_30[2])
			if (L_len(ewintiles) > 0):
				for a_46, b_31 in L_ipairs(ewintiles):
					i_29, j_3 = b_31[1], b_31[2]
					tileid_8 = (i_29 + (j_3 * G['roomsizex']))
					if ((G['unitmap'][tileid_8] is None) or (L_len(G['unitmap'][tileid_8]) == 0)):
						G['MF_win']()
						return None
			if ((L_len(eendtiles) > 0) and (G['generaldata']['strings'][G['WORLD']] != G['generaldata']['strings'][G['BASEWORLD']])):
				for a_47, b_32 in L_ipairs(eendtiles):
					i_30, j_4 = b_32[1], b_32[2]
					tileid_9 = (i_30 + (j_4 * G['roomsizex']))
					if ((G['unitmap'][tileid_9] is None) or (L_len(G['unitmap'][tileid_9]) == 0)):
						if (G['editor']['values'][G['INEDITOR']] != 0):
							G['MF_end_single']()
							G['MF_win']()
							return None
						else:
							G['MF_end_single']()
							G['MF_win']()
							G['MF_credits'](1)
							return None
			if (L_len(things_3) > 0):
				for i_31, rules_2 in L_ipairs(things_3):
					rule_6 = rules_2[1]
					conds_7 = rules_2[2]
					if (rule_6[2] == 'eat'):
						eaten = L_T()
						if ((rule_6[1] == 'level') and L_t(G['testcond'](conds_7, 1))):
							target = rule_6[3]
							if ((target != 'all') and (target != 'empty')):
								dothese = L_T()
								if (L_sub(target, 1, 5) != 'group'):
									dothese = L_T([target])
								else:
									dothese = G['findgroup'](target)
								for c_13, d_12 in L_ipairs(dothese):
									if (G['unitlists'][d_12] is not None):
										if (((d_12 == 'level') and (L_len(G['unitlists']['level']) > 0)) and (lsafe is False)):
											pmult_16, sound_13 = L_adjust((*G['checkeffecthistory']('eat'),), 2)
											G['setsoundname']('removal', 1, sound_13)
											G['destroylevel']()
											return None
										for a_48, unitid_18 in L_ipairs(G['unitlists'][d_12]):
											if (G['issafe'](unitid_18) is False):
												L_insert(eaten, unitid_18)
							elif (target == 'empty'):
								empties = G['findempty']()
								for a_49, b_33 in L_ipairs(empties):
									x_25 = (b_33 % G['roomsizex'])
									y_25 = L_floor(L_div(b_33, G['roomsizex']))
									G['generaldata']['values'][G['SHAKE']] = 4
									pmult_17, sound_14 = L_adjust((*G['checkeffecthistory']('eat'),), 2)
									G['MF_particles']('eat', x_25, y_25, (5 * pmult_17), 0, 3, 1, 1)
									G['setsoundname']('removal', 1, sound_14)
									G['delete'](2, x_25, y_25)
						elif ((rule_6[1] != 'level') and (rule_6[3] == 'level')):
							dothese_2 = L_T()
							if ((G['findnoun'](rule_6[1]) is False) or (rule_6[1] == 'text')):
								dothese_2 = G['findall'](L_T([rule_6[1], conds_7]), None, True)
							elif (rule_6[1] == 'empty'):
								dothese_2 = G['findempty'](conds_7, True)
							if ((L_len(dothese_2) > 0) and (lsafe is False)):
								pmult_18, sound_15 = L_adjust((*G['checkeffecthistory']('eat'),), 2)
								G['setsoundname']('removal', 1, sound_15)
								G['destroylevel']()
								return None
						for a_50, b_34 in L_ipairs(eaten):
							bunit_7 = G['mmf']['newObject'](b_34)
							x_26, y_26 = bunit_7['values'][G['XPOS']], bunit_7['values'][G['YPOS']]
							G['generaldata']['values'][G['SHAKE']] = 4
							pmult_19, sound_16 = L_adjust((*G['checkeffecthistory']('eat'),), 2)
							G['MF_particles']('eat', x_26, y_26, (5 * pmult_19), 0, 3, 1, 1)
							G['setsoundname']('removal', 1, sound_16)
							G['delete'](b_34, x_26, y_26)
					if (((rule_6[1] == 'level') and (rule_6[2] == 'is')) and L_t(G['testcond'](conds_7, 1))):
						action = rule_6[3]
						if (((action == 'you') or (action == 'you2')) or (action == '3d')):
							defeats = G['findfeature'](None, 'is', 'defeat')
							wins = G['findfeature'](None, 'is', 'win')
							ends = G['findfeature'](None, 'is', 'end')
							bonus_3 = G['findfeature'](None, 'is', 'bonus')
							if (defeats is not None):
								for a_51, b_35 in L_ipairs(defeats):
									if (b_35[1] != 'level'):
										allyous = G['findall'](b_35)
										if (L_len(allyous) > 0):
											for c_14, d_13 in L_ipairs(allyous):
												if ((G['issafe'](1) is False) and L_t(G['floating_level'](d_13))):
													G['destroylevel']()
													return None
									elif (L_t(G['testcond'](b_35[2], 1)) and (lsafe is False)):
										G['destroylevel']()
										return None
							if (((L_len(L_first(G['findallfeature']('empty', 'is', 'defeat'))) > 0) and L_t(G['floating_level'](2))) and (lsafe is False)):
								G['destroylevel']()
								return None
							canwin_2 = False
							canend_2 = False
							canbonus_2 = False
							if (wins is not None):
								for a_52, b_36 in L_ipairs(wins):
									if (b_36[1] != 'level'):
										allyous_2 = G['findall'](b_36)
										if (L_len(allyous_2) > 0):
											for c_15, d_14 in L_ipairs(allyous_2):
												if L_t(G['floating_level'](d_14)):
													canwin_2 = True
									elif L_t(G['testcond'](b_36[2], 1)):
										canwin_2 = True
							if (ends is not None):
								for a_53, b_37 in L_ipairs(ends):
									if (b_37[1] != 'level'):
										allyous_3 = G['findall'](b_37)
										if (L_len(allyous_3) > 0):
											for c_16, d_15 in L_ipairs(allyous_3):
												if L_t(G['floating_level'](d_15)):
													canend_2 = True
									elif L_t(G['testcond'](b_37[2], 1)):
										canend_2 = True
							if (bonus_3 is not None):
								for a_54, b_38 in L_ipairs(bonus_3):
									allbonus = G['findall'](b_38)
									if (L_len(allbonus) > 0):
										for c_17, d_16 in L_ipairs(allbonus):
											if ((G['issafe'](d_16) is False) and L_t(G['floating_level'](d_16))):
												unit_29 = G['mmf']['newObject'](d_16)
												pmult_20, sound_17 = L_adjust((*G['checkeffecthistory']('bonus'),), 2)
												G['MF_particles']('bonus', unit_29['values'][G['XPOS']], unit_29['values'][G['YPOS']], (10 * pmult_20), 4, 1, 1, 1)
												G['MF_playsound']('bonus')
												canbonus_2 = True
												G['generaldata']['values'][G['SHAKE']] = 2
												G['setsoundname']('removal', 2, sound_17)
												G['delete'](d_16)
							if ((L_len(L_first(G['findallfeature']('empty', 'is', 'win'))) > 0) and L_t(G['floating_level'](2))):
								canwin_2 = True
							if ((L_len(L_first(G['findallfeature']('empty', 'is', 'end'))) > 0) and L_t(G['floating_level'](2))):
								canend_2 = True
							if (canbonus_2 is not None and canbonus_2 is not False):
								G['MF_bonus'](1)
								G['addundo'](L_T(['bonus', 1]))
							if (canwin_2 is not None and canwin_2 is not False):
								G['MF_win']()
								return None
							if ((canend_2 is not None and canend_2 is not False) and (G['generaldata']['strings'][G['WORLD']] != G['generaldata']['strings'][G['BASEWORLD']])):
								if (G['editor']['values'][G['INEDITOR']] != 0):
									G['MF_end_single']()
									G['MF_win']()
									return None
								else:
									G['MF_end_single']()
									G['MF_win']()
									G['MF_credits'](1)
									return None
						elif (action == 'defeat'):
							yous = G['findfeature'](None, 'is', 'you')
							yous2 = G['findfeature'](None, 'is', 'you2')
							yous3 = G['findfeature'](None, 'is', '3d')
							if (yous is None):
								yous = L_T()
							if (yous2 is not None):
								for i_32, v_16 in L_ipairs(yous2):
									L_insert(yous, v_16)
							if (yous3 is not None):
								for i_33, v_17 in L_ipairs(yous3):
									L_insert(yous, v_17)
							if (yous is not None):
								for a_55, b_39 in L_ipairs(yous):
									if (b_39[1] != 'level'):
										allyous_4 = G['findall'](b_39)
										if (L_len(allyous_4) > 0):
											for c_18, d_17 in L_ipairs(allyous_4):
												if ((G['issafe'](d_17) is False) and L_t(G['floating_level'](d_17))):
													unit_30 = G['mmf']['newObject'](d_17)
													pmult_21, sound_18 = L_adjust((*G['checkeffecthistory']('defeat'),), 2)
													G['MF_particles']('destroy', unit_30['values'][G['XPOS']], unit_30['values'][G['YPOS']], (5 * pmult_21), 0, 3, 1, 1)
													G['setsoundname']('removal', 1, sound_18)
													G['generaldata']['values'][G['SHAKE']] = 2
													G['delete'](d_17)
									elif (L_t(G['testcond'](b_39[2], 1)) and (lsafe is False)):
										G['destroylevel']()
										return None
						elif (action == 'weak'):
							for i_34, unit_31 in L_ipairs(G['units']):
								name_14 = unit_31['strings'][G['UNITNAME']]
								if (unit_31['strings'][G['UNITTYPE']] == 'text'):
									name_14 = 'text'
								if (L_t(G['floating_level'](unit_31['fixed'])) and (lsafe is False)):
									G['destroylevel']()
						elif (action == 'hot'):
							melts = G['findfeature'](None, 'is', 'melt')
							if (melts is not None):
								for a_56, b_40 in L_ipairs(melts):
									allmelts = G['findall'](b_40)
									if (L_len(allmelts) > 0):
										for c_19, d_18 in L_ipairs(allmelts):
											if ((G['issafe'](d_18) is False) and L_t(G['floating_level'](d_18))):
												unit_32 = G['mmf']['newObject'](d_18)
												pmult_22, sound_19 = L_adjust((*G['checkeffecthistory']('hot'),), 2)
												G['MF_particles']('smoke', unit_32['values'][G['XPOS']], unit_32['values'][G['YPOS']], (5 * pmult_22), 0, 1, 1, 1)
												G['generaldata']['values'][G['SHAKE']] = 2
												G['setsoundname']('removal', 9, sound_19)
												G['delete'](d_18)
						elif (action == 'melt'):
							hots = G['findfeature'](None, 'is', 'hot')
							if ((hots is not None) and (lsafe is False)):
								for a_57, b_41 in L_ipairs(hots):
									doit_2 = False
									if (b_41[1] != 'level'):
										allhots = G['findall'](b_41)
										for c_20, d_19 in L_ipairs(allhots):
											if L_t(G['floating_level'](d_19)):
												doit_2 = True
									elif L_t(G['testcond'](b_41[2], 1)):
										doit_2 = True
									if (doit_2 is not None and doit_2 is not False):
										G['destroylevel']()
							if (((L_len(L_first(G['findallfeature']('empty', 'is', 'hot'))) > 0) and L_t(G['floating_level'](2))) and (lsafe is False)):
								G['destroylevel']()
								return None
						elif (action == 'open'):
							shuts = G['findfeature'](None, 'is', 'shut')
							openthese = L_T()
							if (shuts is not None):
								for a_58, b_42 in L_ipairs(shuts):
									doit_3 = False
									if (b_42[1] != 'level'):
										allshuts = G['findall'](b_42)
										for c_21, d_20 in L_ipairs(allshuts):
											if L_t(G['floating_level'](d_20)):
												doit_3 = True
												if (G['issafe'](d_20) is False):
													L_insert(openthese, d_20)
									elif L_t(G['testcond'](b_42[2], 1)):
										doit_3 = True
									if (doit_3 is not None and doit_3 is not False):
										if (lsafe is False):
											G['destroylevel']()
											return None
							if (L_len(openthese) > 0):
								G['generaldata']['values'][G['SHAKE']] = 8
								for a_59, b_43 in L_ipairs(openthese):
									bunit_8 = G['mmf']['newObject'](b_43)
									bx, by = bunit_8['values'][G['XPOS']], bunit_8['values'][G['YPOS']]
									pmult_23, sound_20 = L_adjust((*G['checkeffecthistory']('unlock'),), 2)
									G['setsoundname']('turn', 7, sound_20)
									G['MF_particles']('unlock', bx, by, (15 * pmult_23), 2, 4, 1, 1)
									G['delete'](b_43)
									G['deleted'][b_43] = 1
							if (((L_len(L_first(G['findallfeature']('empty', 'is', 'shut'))) > 0) and L_t(G['floating_level'](2))) and (lsafe is False)):
								G['destroylevel']()
								return None
						elif (action == 'shut'):
							opens = G['findfeature'](None, 'is', 'open')
							openthese_2 = L_T()
							if (opens is not None):
								for a_60, b_44 in L_ipairs(opens):
									doit_4 = False
									if (b_44[1] != 'level'):
										allopens = G['findall'](b_44)
										for c_22, d_21 in L_ipairs(allopens):
											if L_t(G['floating_level'](d_21)):
												doit_4 = True
												if (G['issafe'](d_21) is False):
													L_insert(openthese_2, d_21)
									elif L_t(G['testcond'](b_44[2], 1)):
										doit_4 = True
									if (doit_4 is not None and doit_4 is not False):
										if (lsafe is False):
											G['destroylevel']()
											return None
							if (L_len(openthese_2) > 0):
								G['generaldata']['values'][G['SHAKE']] = 8
								for a_61, b_45 in L_ipairs(openthese_2):
									bunit_9 = G['mmf']['newObject'](b_45)
									bx_2, by_2 = bunit_9['values'][G['XPOS']], bunit_9['values'][G['YPOS']]
									pmult_24, sound_21 = L_adjust((*G['checkeffecthistory']('unlock'),), 2)
									G['setsoundname']('turn', 7, sound_21)
									G['MF_particles']('unlock', bx_2, by_2, (15 * pmult_24), 2, 4, 1, 1)
									G['delete'](b_45)
									G['deleted'][b_45] = 1
							if (((L_len(L_first(G['findallfeature']('empty', 'is', 'open'))) > 0) and L_t(G['floating_level'](2))) and (lsafe is False)):
								G['destroylevel']()
								return None
						elif (action == 'sink'):
							openthese_3 = L_T()
							for a_62, unit_33 in L_ipairs(G['units']):
								name_15 = unit_33['strings'][G['UNITNAME']]
								if (unit_33['strings'][G['UNITTYPE']] == 'text'):
									name_15 = 'text'
								if L_t(G['floating_level'](unit_33['fixed'])):
									if (lsafe is False):
										G['destroylevel']()
										return None
									if (G['issafe'](unit_33['fixed']) is False):
										L_insert(openthese_3, unit_33['fixed'])
							if (L_len(openthese_3) > 0):
								G['generaldata']['values'][G['SHAKE']] = 3
								for a_63, b_46 in L_ipairs(openthese_3):
									bunit_10 = G['mmf']['newObject'](b_46)
									bx_3, by_3 = bunit_10['values'][G['XPOS']], bunit_10['values'][G['YPOS']]
									pmult_25, sound_22 = L_adjust((*G['checkeffecthistory']('sink'),), 2)
									G['setsoundname']('removal', 3, sound_22)
									c1_5, c2_5 = L_adjust((*G['getcolour'](b_46),), 2)
									G['MF_particles']('destroy', bx_3, by_3, (15 * pmult_25), c1_5, c2_5, 1, 1)
									G['delete'](b_46)
									G['deleted'][b_46] = 1
						elif (action == 'boom'):
							openthese_4 = L_T()
							for a_64, unit_34 in L_ipairs(G['units']):
								name_16 = unit_34['strings'][G['UNITNAME']]
								if (unit_34['strings'][G['UNITTYPE']] == 'text'):
									name_16 = 'text'
								if L_t(G['floating_level'](unit_34['fixed'])):
									if (lsafe is False):
										G['destroylevel']()
										return None
									if (G['issafe'](unit_34['fixed']) is False):
										L_insert(openthese_4, unit_34['fixed'])
							if (L_len(openthese_4) > 0):
								G['generaldata']['values'][G['SHAKE']] = 3
								for a_65, b_47 in L_ipairs(openthese_4):
									bunit_11 = G['mmf']['newObject'](b_47)
									bx_4, by_4 = bunit_11['values'][G['XPOS']], bunit_11['values'][G['YPOS']]
									pmult_26, sound_23 = L_adjust((*G['checkeffecthistory']('boom'),), 2)
									G['setsoundname']('removal', 1, sound_23)
									G['MF_particles']('smoke', bx_4, by_4, (15 * pmult_26), 0, 2, 1, 1)
									G['delete'](b_47)
									G['deleted'][b_47] = 1
						elif (action == 'done'):
							doned_3 = L_T()
							for a_66, unit_35 in L_ipairs(G['units']):
								L_insert(doned_3, unit_35)
							G['updateundo'] = True
							for a_67, unit_36 in L_ipairs(doned_3):
								G['addundo'](L_T(['done', unit_36['strings'][G['UNITNAME']], unit_36['values'][G['XPOS']], unit_36['values'][G['YPOS']], unit_36['values'][G['DIR']], unit_36['values'][G['ID']], unit_36['fixed'], unit_36['values'][G['FLOAT']]]))
								unit_36['values'][G['FLOAT']] = 2
								unit_36['values'][G['EFFECTCOUNT']] = G['math']['random']((-10), 10)
								unit_36['values'][G['POSITIONING']] = 7
								unit_36['flags'][G['DEAD']] = True
								G['delunit'](unit_36['fixed'])
							G['MF_playsound']('doneall_c')
						elif (action == 'bonus'):
							yous_2 = G['findfeature'](None, 'is', 'you')
							yous2_2 = G['findfeature'](None, 'is', 'you2')
							yous3_2 = G['findfeature'](None, 'is', '3d')
							bonusget = False
							if (yous_2 is None):
								yous_2 = L_T()
							if (yous2_2 is not None):
								for i_35, v_18 in L_ipairs(yous2_2):
									L_insert(yous_2, v_18)
							if (yous3_2 is not None):
								for i_36, v_19 in L_ipairs(yous3_2):
									L_insert(yous_2, v_19)
							if (yous_2 is not None):
								for a_68, b_48 in L_ipairs(yous_2):
									if (b_48[1] != 'level'):
										allyous_5 = G['findall'](b_48)
										if (L_len(allyous_5) > 0):
											for c_23, d_22 in L_ipairs(allyous_5):
												if L_t(G['floating_level'](d_22)):
													bonusget = True
													if (lsafe is False):
														G['destroylevel']('bonus')
														return None
									elif L_t(G['testcond'](b_48[2], 1)):
										bonusget = True
										if (lsafe is False):
											G['destroylevel']('bonus')
											return None
							if ((((L_len(L_first(G['findallfeature']('empty', 'is', 'you'))) > 0) or (L_len(L_first(G['findallfeature']('empty', 'is', 'you2'))) > 0)) or (L_len(L_first(G['findallfeature']('empty', 'is', '3d'))) > 0)) and L_t(G['floating_level'](2))):
								bonusget = True
								if (lsafe is False):
									G['destroylevel']('bonus')
									return None
							if (bonusget is not None and bonusget is not False):
								G['MF_playsound']('bonus')
								G['MF_bonus'](1)
								G['addundo'](L_T(['bonus', 1]))
						elif (action == 'win'):
							yous_3 = G['findfeature'](None, 'is', 'you')
							yous2_3 = G['findfeature'](None, 'is', 'you2')
							yous3_3 = G['findfeature'](None, 'is', '3d')
							if (yous_3 is None):
								yous_3 = L_T()
							if (yous2_3 is not None):
								for i_37, v_20 in L_ipairs(yous2_3):
									L_insert(yous_3, v_20)
							if (yous3_3 is not None):
								for i_38, v_21 in L_ipairs(yous3_3):
									L_insert(yous_3, v_21)
							canwin_3 = False
							if (yous_3 is not None):
								for a_69, b_49 in L_ipairs(yous_3):
									allyous_6 = G['findall'](b_49)
									doit_5 = False
									for c_24, d_23 in L_ipairs(allyous_6):
										if L_t(G['floating_level'](d_23)):
											doit_5 = True
									if (doit_5 is not None and doit_5 is not False):
										canwin_3 = True
										for c_25, d_24 in L_ipairs(allyous_6):
											unit_37 = G['mmf']['newObject'](d_24)
											pmult_27, sound_24 = L_adjust((*G['checkeffecthistory']('win'),), 2)
											G['MF_particles']('win', unit_37['values'][G['XPOS']], unit_37['values'][G['YPOS']], (10 * pmult_27), 2, 4, 1, 1)
							emptyyou = False
							if ((((L_len(L_first(G['findallfeature']('empty', 'is', 'you'))) > 0) or (L_len(L_first(G['findallfeature']('empty', 'is', 'you2'))) > 0)) or (L_len(L_first(G['findallfeature']('empty', 'is', '3d'))) > 0)) and L_t(G['floating_level'](2))):
								emptyyou = True
							if ((((G['hasfeature']('level', 'is', 'you', 1) is not None) or (G['hasfeature']('level', 'is', 'you2', 1) is not None)) or (G['hasfeature']('level', 'is', '3d', 1) is not None)) or (emptyyou is not None and emptyyou is not False)):
								canwin_3 = True
							if (canwin_3 is not None and canwin_3 is not False):
								G['MF_win']()
								return None
						elif (action == 'end'):
							yous_4 = G['findfeature'](None, 'is', 'you')
							yous2_4 = G['findfeature'](None, 'is', 'you2')
							yous3_4 = G['findfeature'](None, 'is', '3d')
							if (yous_4 is None):
								yous_4 = L_T()
							if (yous2_4 is not None):
								for i_39, v_22 in L_ipairs(yous2_4):
									L_insert(yous_4, v_22)
							if (yous3_4 is not None):
								for i_40, v_23 in L_ipairs(yous3_4):
									L_insert(yous_4, v_23)
							canend_3 = False
							if (yous_4 is not None):
								for a_70, b_50 in L_ipairs(yous_4):
									allyous_7 = G['findall'](b_50)
									doit_6 = False
									for c_26, d_25 in L_ipairs(allyous_7):
										if L_t(G['floating_level'](d_25)):
											doit_6 = True
									if (doit_6 is not None and doit_6 is not False):
										canend_3 = True
										for c_27, d_26 in L_ipairs(allyous_7):
											unit_38 = G['mmf']['newObject'](d_26)
											pmult_28, sound_25 = L_adjust((*G['checkeffecthistory']('win'),), 2)
											G['MF_particles']('win', unit_38['values'][G['XPOS']], unit_38['values'][G['YPOS']], (10 * pmult_28), 2, 4, 1, 1)
							emptyyou_2 = False
							if ((((L_len(L_first(G['findallfeature']('empty', 'is', 'you'))) > 0) or (L_len(L_first(G['findallfeature']('empty', 'is', 'you2'))) > 0)) or (L_len(L_first(G['findallfeature']('empty', 'is', '3d'))) > 0)) and L_t(G['floating_level'](2))):
								emptyyou_2 = True
							if ((((G['hasfeature']('level', 'is', 'you', 1) is not None) or (G['hasfeature']('level', 'is', 'you2', 1) is not None)) or (G['hasfeature']('level', 'is', '3d', 1) is not None)) or (emptyyou_2 is not None and emptyyou_2 is not False)):
								canend_3 = True
							if ((canend_3 is not None and canend_3 is not False) and (G['generaldata']['strings'][G['WORLD']] != G['generaldata']['strings'][G['BASEWORLD']])):
								if (G['editor']['values'][G['INEDITOR']] != 0):
									G['MF_end_single']()
									G['MF_win']()
									break
								else:
									G['MF_end_single']()
									G['MF_win']()
									G['MF_credits'](1)
									break
						elif (((action == 'tele') and (levelteledone < 3)) and (lstill is False)):
							levelteledone = (levelteledone + 1)
							for a_71, unit_39 in L_ipairs(G['units']):
								x_27, y_27 = unit_39['values'][G['XPOS']], unit_39['values'][G['YPOS']]
								tx_2, ty_2 = G['fixedrandom'](1, (G['roomsizex'] - 2)), G['fixedrandom'](1, (G['roomsizey'] - 2))
								if L_t(G['floating_level'](unit_39['fixed'])):
									G['update'](unit_39['fixed'], tx_2, ty_2)
									pmult_29, sound_26 = L_adjust((*G['checkeffecthistory']('tele'),), 2)
									G['MF_particles']('glow', x_27, y_27, (5 * pmult_29), 1, 4, 1, 1)
									G['MF_particles']('glow', tx_2, ty_2, (5 * pmult_29), 1, 4, 1, 1)
									G['setsoundname']('turn', 6, sound_26)
						elif (action == 'move'):
							dir__7 = G['mapdir']
							if (G['featureindex']['reverse'] is not None):
								dir__7 = L_first(G['reversecheck'](1, dir__7))
							drs_3 = G['ndirs'][(dir__7 + 1)]
							ox_5, oy_5 = drs_3[1], drs_3[2]
							if ((lstill is False) and (lsleep is False)):
								G['addundo'](L_T(['levelupdate', G['Xoffset'], G['Yoffset'], (G['Xoffset'] + (ox_5 * G['tilesize'])), (G['Yoffset'] + (oy_5 * G['tilesize'])), dir__7, dir__7]))
								G['MF_scrollroom']((ox_5 * G['tilesize']), (oy_5 * G['tilesize']))
								G['updateundo'] = True
						elif (action == 'chill'):
							dir__8 = G['fixedrandom'](0, 3)
							G['addundo'](L_T(['mapdir', G['mapdir'], dir__8]))
							G['mapdir'] = dir__8
							drs_4 = G['ndirs'][(dir__8 + 1)]
							ox_6, oy_6 = drs_4[1], drs_4[2]
							if ((lstill is False) and (lsleep is False)):
								G['addundo'](L_T(['levelupdate', G['Xoffset'], G['Yoffset'], (G['Xoffset'] + (ox_6 * G['tilesize'])), (G['Yoffset'] + (oy_6 * G['tilesize'])), dir__8, dir__8]))
								G['MF_scrollroom']((ox_6 * G['tilesize']), (oy_6 * G['tilesize']))
								G['updateundo'] = True
						elif (action == 'nudgeright'):
							dir__9 = 0
							if (G['featureindex']['reverse'] is not None):
								dir__9 = L_first(G['reversecheck'](1, dir__9))
							drs_5 = G['ndirs'][(dir__9 + 1)]
							ox_7, oy_7 = drs_5[1], drs_5[2]
							if ((lstill is False) and (lsleep is False)):
								G['addundo'](L_T(['levelupdate', G['Xoffset'], G['Yoffset'], (G['Xoffset'] + (ox_7 * G['tilesize'])), (G['Yoffset'] + (oy_7 * G['tilesize'])), G['mapdir'], G['mapdir']]))
								G['MF_scrollroom']((ox_7 * G['tilesize']), (oy_7 * G['tilesize']))
								G['updateundo'] = True
						elif (action == 'nudgeup'):
							dir__10 = 1
							if (G['featureindex']['reverse'] is not None):
								dir__10 = L_first(G['reversecheck'](1, dir__10))
							drs_6 = G['ndirs'][(dir__10 + 1)]
							ox_8, oy_8 = drs_6[1], drs_6[2]
							if ((lstill is False) and (lsleep is False)):
								G['addundo'](L_T(['levelupdate', G['Xoffset'], G['Yoffset'], (G['Xoffset'] + (ox_8 * G['tilesize'])), (G['Yoffset'] + (oy_8 * G['tilesize'])), G['mapdir'], G['mapdir']]))
								G['MF_scrollroom']((ox_8 * G['tilesize']), (oy_8 * G['tilesize']))
								G['updateundo'] = True
						elif (action == 'nudgeleft'):
							dir__11 = 2
							if (G['featureindex']['reverse'] is not None):
								dir__11 = L_first(G['reversecheck'](1, dir__11))
							drs_7 = G['ndirs'][(dir__11 + 1)]
							ox_9, oy_9 = drs_7[1], drs_7[2]
							if ((lstill is False) and (lsleep is False)):
								G['addundo'](L_T(['levelupdate', G['Xoffset'], G['Yoffset'], (G['Xoffset'] + (ox_9 * G['tilesize'])), (G['Yoffset'] + (oy_9 * G['tilesize'])), G['mapdir'], G['mapdir']]))
								G['MF_scrollroom']((ox_9 * G['tilesize']), (oy_9 * G['tilesize']))
								G['updateundo'] = True
						elif (action == 'nudgedown'):
							dir__12 = 3
							if (G['featureindex']['reverse'] is not None):
								dir__12 = L_first(G['reversecheck'](1, dir__12))
							drs_8 = G['ndirs'][(dir__12 + 1)]
							ox_10, oy_10 = drs_8[1], drs_8[2]
							if ((lstill is False) and (lsleep is False)):
								G['addundo'](L_T(['levelupdate', G['Xoffset'], G['Yoffset'], (G['Xoffset'] + (ox_10 * G['tilesize'])), (G['Yoffset'] + (oy_10 * G['tilesize'])), G['mapdir'], G['mapdir']]))
								G['MF_scrollroom']((ox_10 * G['tilesize']), (oy_10 * G['tilesize']))
								G['updateundo'] = True
						elif (action == 'fall'):
							drop = 20
							dir__13 = G['mapdir']
							ox_11 = 0
							oy_11 = 1
							if (G['featureindex']['reverse'] is not None):
								dir__13, ox_11, oy_11 = L_adjust((*G['reversecheck'](1, dir__13, None, None, ox_11, oy_11),), 3)
							if (lstill is False):
								G['addundo'](L_T(['levelupdate', G['Xoffset'], G['Yoffset'], (G['Xoffset'] + ((G['tilesize'] * drop) * ox_11)), (G['Yoffset'] + ((G['tilesize'] * drop) * oy_11)), dir__13, dir__13]))
								G['MF_scrollroom'](((G['tilesize'] * drop) * ox_11), ((G['tilesize'] * drop) * oy_11))
								G['updateundo'] = True
						elif (action == 'fallright'):
							drop_2 = 35
							dir__14 = G['mapdir']
							ox_12 = 1
							oy_12 = 0
							if (G['featureindex']['reverse'] is not None):
								dir__14, ox_12, oy_12 = L_adjust((*G['reversecheck'](1, dir__14, None, None, ox_12, oy_12),), 3)
							if (lstill is False):
								G['addundo'](L_T(['levelupdate', G['Xoffset'], G['Yoffset'], (G['Xoffset'] + ((G['tilesize'] * drop_2) * ox_12)), (G['Yoffset'] + ((G['tilesize'] * drop_2) * oy_12)), dir__14, dir__14]))
								G['MF_scrollroom'](((G['tilesize'] * drop_2) * ox_12), ((G['tilesize'] * drop_2) * oy_12))
								G['updateundo'] = True
						elif (action == 'fallup'):
							drop_3 = 20
							dir__15 = G['mapdir']
							ox_13 = 0
							oy_13 = (-1)
							if (G['featureindex']['reverse'] is not None):
								dir__15, ox_13, oy_13 = L_adjust((*G['reversecheck'](1, dir__15, None, None, ox_13, oy_13),), 3)
							if (lstill is False):
								G['addundo'](L_T(['levelupdate', G['Xoffset'], G['Yoffset'], (G['Xoffset'] + ((G['tilesize'] * drop_3) * ox_13)), (G['Yoffset'] + ((G['tilesize'] * drop_3) * oy_13)), dir__15, dir__15]))
								G['MF_scrollroom'](((G['tilesize'] * drop_3) * ox_13), ((G['tilesize'] * drop_3) * oy_13))
								G['updateundo'] = True
						elif (action == 'fallleft'):
							drop_4 = 35
							dir__16 = G['mapdir']
							ox_14 = (-1)
							oy_14 = 0
							if (G['featureindex']['reverse'] is not None):
								dir__16, ox_14, oy_14 = L_adjust((*G['reversecheck'](1, dir__16, None, None, ox_14, oy_14),), 3)
							if (lstill is False):
								G['addundo'](L_T(['levelupdate', G['Xoffset'], G['Yoffset'], (G['Xoffset'] + ((G['tilesize'] * drop_4) * ox_14)), (G['Yoffset'] + ((G['tilesize'] * drop_4) * oy_14)), dir__16, dir__16]))
								G['MF_scrollroom'](((G['tilesize'] * drop_4) * ox_14), ((G['tilesize'] * drop_4) * oy_14))
								G['updateundo'] = True
						elif (rule_6[3] == 'turn'):
							newmapdir = (((G['mapdir'] - 1) + 4) % 4)
							newmaprotation = ((((G['mapdir'] + 1) + 4) % 4) * 90)
							G['updateundo'] = True
							G['addundo'](L_T(['maprotation', G['maprotation'], newmaprotation, newmapdir]))
							G['addundo'](L_T(['mapdir', G['mapdir'], newmapdir]))
							G['maprotation'] = newmaprotation
							G['mapdir'] = newmapdir
							G['MF_levelrotation'](G['maprotation'])
						elif (rule_6[3] == 'deturn'):
							newmapdir_2 = (((G['mapdir'] + 1) + 4) % 4)
							newmaprotation_2 = ((((G['mapdir'] + 1) + 4) % 4) * 90)
							G['updateundo'] = True
							G['addundo'](L_T(['maprotation', G['maprotation'], newmaprotation_2, newmapdir_2]))
							G['addundo'](L_T(['mapdir', G['mapdir'], newmapdir_2]))
							G['maprotation'] = newmaprotation_2
							G['mapdir'] = newmapdir_2
							G['MF_levelrotation'](G['maprotation'])
						elif (action == 'empty'):
							G['destroylevel']('empty')
			if (G['featureindex']['done'] is not None):
				for i_41, v_24 in L_ipairs(G['featureindex']['done']):
					L_insert(donethings, v_24)
			if ((L_len(donethings) > 0) and (G['generaldata']['values'][G['WINTIMER']] == 0)):
				for i_42, rules_3 in L_ipairs(donethings):
					rule_7 = rules_3[1]
					conds_8 = rules_3[2]
					if (((rule_7[1] == 'all') and (rule_7[2] == 'is')) and (rule_7[3] == 'done')):
						targets_2 = L_first(G['findallfeature'](None, 'is', 'done', True))
						found = False
						levelunits_ = L_T()
						for a_72, v_25 in L_ipairs(targets_2):
							unit_40 = G['mmf']['newObject'](v_25)
							if (unit_40['className'] != 'level'):
								found = True
								break
						if (G['objectlist']['level'] is not None):
							for a_73, unit_41 in L_ipairs(G['units']):
								if (unit_41['className'] == 'level'):
									L_insert(levelunits_, unit_41['fixed'])
						if (found is not None and found is not False):
							if ((G['generaldata']['strings'][G['WORLD']] == G['generaldata']['strings'][G['BASEWORLD']]) and (G['editor']['values'][G['INEDITOR']] == 0)):
								G['MF_playsound']('doneall_c')
								G['MF_allisdone']()
							elif ((G['editor']['values'][G['INEDITOR']] != 0) and (L_len(targets_2) >= ((L_len(G['units']) - L_len(G['codeunits'])) - L_len(levelunits_)))):
								pmult_30 = L_first(G['checkeffecthistory']('win'))
								G['MF_playsound']('doneall_c')
								G['MF_done_single']()
								G['MF_win']()
								break
							elif (L_len(targets_2) >= ((L_len(G['units']) - L_len(G['codeunits'])) - L_len(levelunits_))):
								pmult_31 = L_first(G['checkeffecthistory']('win'))
								mods_run_2 = G['do_mod_hook']('levelpack_done', L_T())
								if (mods_run_2 is False):
									G['MF_playsound']('doneall_c')
									G['MF_done_single']()
									G['MF_win']()
									G['MF_credits'](2)
								break
			if ((G['generaldata']['strings'][G['WORLD']] == G['generaldata']['strings'][G['BASEWORLD']]) and (G['generaldata']['strings'][G['CURRLEVEL']] == '305level')):
				numfound = False
				if (G['featureindex']['image'] is not None):
					for i_43, v_26 in L_ipairs(G['featureindex']['image']):
						rule_8 = v_26[1]
						conds_9 = v_26[2]
						if (((rule_8[1] == 'image') and (rule_8[2] == 'is')) and (L_len(conds_9) == 0)):
							num = rule_8[3]
							nums = L_T([], {'one': L_T([1, 'image_desc_1']), 'two': L_T([2, 'image_desc_2']), 'three': L_T([3, 'image_desc_3']), 'four': L_T([4, 'image_desc_4']), 'five': L_T([5, 'image_desc_5']), 'six': L_T([6, 'image_desc_6']), 'seven': L_T([7, 'image_desc_7']), 'eight': L_T([8, 'image_desc_8']), 'nine': L_T([9, 'image_desc_9']), 'ten': L_T([10, 'image_desc_10']), 'fourteen': L_T([11, 'image_desc_11']), 'sixteen': L_T([12, 'image_desc_12']), 'minusone': L_T([13, 'image_desc_13']), 'minustwo': L_T([14, 'image_desc_14']), 'minusthree': L_T([15, 'image_desc_15']), 'minusten': L_T([16, 'image_desc_16']), 'win': L_T([0, 'win'])})
							if (nums[num] is not None):
								data_2 = nums[num]
								if (data_2[2] != 'win'):
									G['MF_setart'](data_2[1], G['langtext'](data_2[2], True))
									numfound = True
								else:
									yous_5 = L_first(G['findallfeature'](None, 'is', 'you', True))
									yous2_5 = L_first(G['findallfeature'](None, 'is', 'you2', True))
									yous3_5 = L_first(G['findallfeature'](None, 'is', '3d', True))
									if (L_len(yous2_5) > 0):
										for a_74, b_51 in L_ipairs(yous2_5):
											L_insert(yous_5, b_51)
									if (L_len(yous3_5) > 0):
										for a_75, b_52 in L_ipairs(yous3_5):
											L_insert(yous_5, b_52)
									for a_76, b_53 in L_ipairs(yous_5):
										unit_42 = G['mmf']['newObject'](b_53)
										x_28, y_28 = unit_42['values'][G['XPOS']], unit_42['values'][G['YPOS']]
										if (x_28 > (G['roomsizex'] - 16)):
											pmult_32 = L_first(G['checkeffecthistory']('win'))
											G['MF_particles']('win', x_28, y_28, (10 * pmult_32), 2, 4, 1, 1)
											G['MF_win']()
											break
				if (numfound is False):
					G['MF_setart'](0, '')
			if (unlocked is not None and unlocked is not False):
				G['setsoundname']('turn', 7)
			G['do_mod_hook']('block_level')
		totalunitcount = G['MF_totalunitcount']()
		if ((L_len(G['units']) >= G['unitlimit']) or (totalunitcount >= (G['unitlimit'] + 1000))):
			G['HACK_INFINITY'] = 200
			G['destroylevel']('toocomplex')
			return None
	G['levelblock'] = f_levelblock
	def f_findplayer(undoing_2=None, *_):  # L3532
		playerfound = False
		playerfound_3d = False
		noundo = False
		if ((undoing_2 is not None) and (undoing_2 == 2)):
			noundo = True
		players1 = G['findfeature'](None, 'is', 'you')
		players2 = G['findfeature'](None, 'is', 'you2')
		players3 = G['findfeature'](None, 'is', '3d')
		players = L_T()
		if (players1 is not None):
			for i_44, v_27 in L_ipairs(players1):
				L_insert(players, v_27)
		if (players2 is not None):
			for i_45, v_28 in L_ipairs(players2):
				L_insert(players, v_28)
		limit_3 = L_len(players)
		if (players3 is not None):
			for i_46, v_29 in L_ipairs(players3):
				if (v_29[1] != 'empty'):
					L_insert(players, v_29)
		if (L_len(players) > 0):
			for i_47, v_30 in L_ipairs(players):
				if ((v_30[1] != 'level') and (v_30[1] != 'empty')):
					allplayers = G['findall'](v_30)
					if (L_len(allplayers) > 0):
						playerfound = True
						if (i_47 > limit_3):
							unitid_19 = allplayers[1]
							unit_43 = G['mmf']['newObject'](unitid_19)
							playerfound_3d = True
							if ((G['spritedata']['values'][G['CAMTARGET']] == 0) or (G['spritedata']['values'][G['CAMTARGET']] == 0.5)):
								G['spritedata']['values'][G['CAMTARGET']] = unit_43['values'][G['ID']]
				elif (v_30[1] == 'level'):
					if L_t(G['testcond'](v_30[2], 1)):
						playerfound = True
				elif (v_30[1] == 'empty'):
					empties_2 = G['findempty'](v_30[2], True)
					if (L_len(empties_2) > 0):
						playerfound = True
		if ((playerfound_3d is False) and (playerfound is not None and playerfound is not False)):
			G['visionmode'](0, None, noundo)
		if (playerfound is not None and playerfound is not False):
			G['MF_musicstate'](0)
			G['generaldata2']['values'][G['NOPLAYER']] = 0
		else:
			if (G['generaldata2']['values'][G['NOPLAYER']] == 0):
				G['dolog']('no_you', 'event')
			G['MF_musicstate'](1)
			G['generaldata2']['values'][G['NOPLAYER']] = 1
	G['findplayer'] = f_findplayer
	def f_diceblock(*_):  # L3618
		G['condstatus'] = L_T()
		if (G['condfeatureindex']['often'] is not None):
			for i_48, v_31 in L_ipairs(G['condfeatureindex']['often']):
				conds_10 = v_31[2]
				identifier = L_tostring(conds_10)
				if (G['condstatus'][identifier] is None):
					G['condstatus'][identifier] = L_T()
				data_3 = G['condstatus'][identifier]
		if (G['condfeatureindex']['seldom'] is not None):
			for i_49, v_32 in L_ipairs(G['condfeatureindex']['seldom']):
				conds_11 = v_32[2]
				identifier_2 = L_tostring(conds_11)
				if (G['condstatus'][identifier_2] is None):
					G['condstatus'][identifier_2] = L_T()
				data_4 = G['condstatus'][identifier_2]
	G['diceblock'] = f_diceblock
