"""Generated from convert.lua by tools/lua2py.py. Do not edit."""
from babasim.luart import *  # noqa: F403


def load(G):
	def f_conversion(dolevels_=None, *_):  # L1
		alreadydone = L_T()
		dolevels = (_t1 if L_t(_t1 := dolevels_) else False)
		for i, v in L_pairs(G['features']):
			words = v[1]
			operator = words[2]
			if (((operator == 'is') or (operator == 'write')) or (operator == 'become')):
				output = L_T()
				name = words[1]
				thing = words[3]
				if (((((((G['getmat'](thing) is not None) or (thing == L_concat('not ', name))) or (thing == 'all')) or (G['unitreference'][thing] is not None)) or ((thing == 'text') and (G['unitreference']['text_text'] is not None))) or (thing == 'revert')) or ((operator == 'write') and L_t(G['getmat_text'](L_concat('text_', name))))):
					if ((G['featureindex'][name] is not None) and (alreadydone[name] is None)):
						alreadydone[name] = 1
						for a, b in L_ipairs(G['featureindex'][name]):
							rule = b[1]
							conds = b[2]
							target, verb, object = rule[1], rule[2], rule[3]
							if ((verb == 'is') or (verb == 'become')):
								if (((target == name) and (object != 'word')) and ((object != name) or (verb == 'become'))):
									if ((object != 'text') and (object != 'revert')):
										if (object == L_concat('not ', name)):
											L_insert(output, L_T(['error', conds, verb]))
										else:
											for d, mat in L_pairs(G['objectlist']):
												if ((L_sub(d, 1, 5) != 'group') and (d == object)):
													L_insert(output, L_T([object, conds, verb]))
									elif ((name != object) or (verb == 'become')):
										if (object != 'revert'):
											L_insert(output, L_T([object, conds, verb]))
										else:
											L_insert(output, 1, L_T([object, conds, verb]))
							elif (verb == 'write'):
								if ((L_sub(object, 1, 4) != 'not ') and (target == name)):
									L_insert(output, L_T([object, conds, 'write']))
					if (L_len(output) > 0):
						conversions = L_T()
						for k, v3 in L_pairs(output):
							object_2 = v3[1]
							conds_2 = v3[2]
							op = v3[3]
							if ((op == 'is') or (op == 'become')):
								if (((G['findnoun'](object_2, G['nlist']['brief']) is False) and (object_2 != 'word')) and (object_2 != 'text')):
									L_insert(conversions, v3)
								elif (object_2 == 'all'):
									L_insert(conversions, L_T(['createall', conds_2]))
								elif (object_2 == 'text'):
									L_insert(conversions, L_T([L_concat('text_', name), conds_2]))
							elif (op == 'write'):
								L_insert(conversions, v3)
						if (L_len(conversions) > 0):
							G['convert'](name, conversions, dolevels)
	G['conversion'] = f_conversion
	def f_convert(stuff=None, mats=None, dolevels__2=None, *_):  # L86
		layer = G['map'][0]
		delthese = L_T()
		mat1 = stuff
		dolevels_2 = (_t1 if L_t(_t1 := dolevels__2) else False)
		donewid = False
		if (dolevels_2 is False):
			if (mat1 != 'empty'):
				targets = L_T()
				if (G['unitlists'][mat1] is not None):
					targets = G['unitlists'][mat1]
				if (G['editor2']['values'][G['CURSORSEXIST']] == 1):
					if (G['featureindex'][mat1] is not None):
						for i_2, v_2 in L_ipairs(G['featureindex'][mat1]):
							rule_2 = v_2[1]
							if ((rule_2[2] == 'is') and (rule_2[3] == 'select')):
								G['editor']['values'][G['NAMEFLAG']] = 0
								break
				if (L_len(targets) > 0):
					for i_3, mat_2 in L_pairs(mats):
						if (mat_2[1] == 'createall'):
							donewid = True
							break
					for i_4, unitid in L_pairs(targets):
						unit = G['mmf']['newObject'](unitid)
						x, y, dir_, id_ = unit['values'][G['XPOS']], unit['values'][G['YPOS']], unit['values'][G['DIR']], unit['values'][G['ID']]
						name_2 = G['getname'](unit)
						reverting = False
						mats2 = L_T()
						if (unit['flags'][G['CONVERTED']] is False):
							for a_2, matdata in L_pairs(mats):
								mat2 = matdata[1]
								conds_3 = matdata[2]
								op_2 = matdata[3]
								if (op_2 == 'write'):
									mat2 = L_concat('text_', matdata[1])
								if (reverting is False):
									objectfound = False
									if ((G['unitreference'][mat2] is not None) and (mat2 != 'level')):
										object_3 = G['unitreference'][mat2]
										if ((G['tileslist'][object_3]['name'] == mat2) and ((G['changes'][object_3] is None) or (G['changes'][object_3]['name'] is None))):
											objectfound = True
										elif (G['changes'][object_3] is not None):
											if ((G['changes'][object_3]['name'] is not None) and (G['changes'][object_3]['name'] == mat2)):
												objectfound = True
									else:
										objectfound = True
									if (L_t(G['testcond'](conds_3, unit['fixed'])) and (objectfound is not None and objectfound is not False)):
										ingameid = 0
										if ((a_2 == 1) and (donewid is False)):
											ingameid = id_
										elif ((a_2 > 1) or (donewid is not None and donewid is not False)):
											ingameid = G['newid']()
										if (mat2 == 'revert'):
											if (unit['strings'][G['UNITNAME']] != unit['originalname']):
												reverting = True
										if ((mat2 != 'revert') or ((mat2 == 'revert') and (reverting is not None and reverting is not False))):
											L_insert(mats2, L_T([mat2, ingameid, id_]))
											unit['flags'][G['CONVERTED']] = True
								else:
									break
						if (L_len(mats2) > 0):
							G['addaction'](unit['fixed'], L_T(['convert', mats2]))
			elif (mat1 == 'empty'):
				convunitmap = L_T()
				for a_3, unit_2 in L_pairs(G['units']):
					tileid = (unit_2['values'][G['XPOS']] + (unit_2['values'][G['YPOS']] * G['roomsizex']))
					convunitmap[tileid] = 1
				for i_5 in L_range(0, (G['roomsizex'] - 1)):
					for j in L_range(0, (G['roomsizey'] - 1)):
						empty = True
						mats2_2 = L_T()
						tileid_2 = (i_5 + (j * G['roomsizex']))
						if (convunitmap[tileid_2] is not None):
							empty = False
						if (G['emptydata'][tileid_2] is not None):
							if ((G['emptydata'][tileid_2]['conv'] is not None) and L_t(G['emptydata'][tileid_2]['conv'])):
								empty = False
						if (L_invoke(layer, 'get_x', i_5, j) != 255):
							empty = False
						if (empty is not None and empty is not False):
							for a_4, matdata_2 in L_pairs(mats):
								mat2_2 = matdata_2[1]
								conds_4 = matdata_2[2]
								op_3 = matdata_2[3]
								if (op_3 == 'write'):
									mat2_2 = L_concat('text_', matdata_2[1])
								objectfound_2 = False
								if ((G['unitreference'][mat2_2] is not None) and (mat2_2 != 'level')):
									object_4 = G['unitreference'][mat2_2]
									if ((G['tileslist'][object_4]['name'] == mat2_2) and ((G['changes'][object_4] is None) or (G['changes'][object_4]['name'] is None))):
										objectfound_2 = True
									elif (G['changes'][object_4] is not None):
										if ((G['changes'][object_4]['name'] is not None) and (G['changes'][object_4]['name'] == mat2_2)):
											objectfound_2 = True
								elif (mat2_2 != 'revert'):
									objectfound_2 = True
								if ((mat2_2 != 'empty') and (objectfound_2 is not None and objectfound_2 is not False)):
									if L_t(G['testcond'](conds_4, 2, i_5, j)):
										L_insert(mats2_2, L_T([mat2_2, i_5, j]))
						if (L_len(mats2_2) > 0):
							G['addaction'](2, L_T(['emptyconvert', mats2_2]))
		if ((mat1 == 'level') and (dolevels_2 is not None and dolevels_2 is not False)):
			for i_6, v_3 in L_ipairs(mats):
				L_insert(G['levelconversions'], v_3)
	G['convert'] = f_convert
	def f_doconvert(data=None, extrarule_=None, *_):  # L264
		style = data[2]
		mats2_3 = data[3]
		unitid_2 = data[1]
		unit_3 = L_T()
		x_2, y_2, dir__2, name_3, id__2, completed, float_, ogname = 0, 0, 0, '', 0, 0, 0, ''
		delthis = False
		delthis_createall = False
		delthis_createall_ = False
		if (unitid_2 != 2):
			unit_3 = G['mmf']['newObject'](unitid_2)
			x_2, y_2, dir__2, name_3, id__2, completed, ogname = unit_3['values'][G['XPOS']], unit_3['values'][G['YPOS']], unit_3['values'][G['DIR']], unit_3['strings'][G['UNITNAME']], unit_3['values'][G['ID']], unit_3['values'][G['COMPLETED']], unit_3['originalname']
		cdata = L_T()
		cdata[1] = name_3
		if (style == 'convert'):
			for a_5, mats2data in L_ipairs(mats2_3):
				mat2_3 = mats2data[1]
				ingameid_2 = mats2data[2]
				baseingameid = mats2data[3]
				unitname = ''
				if (((mat2_3 == 'revert') and (unitid_2 != 2)) and (ogname is not None)):
					originalname = ogname
					if (L_strlen(originalname) > 0):
						unitname = G['unitreference'][originalname]
						mat2_3 = originalname
					else:
						unitname = None
					if (G['source'] == 'emptyconvert'):
						unitname = ''
						mat2_3 = 'empty'
					if (unitname == unit_3['className']):
						G['MF_alert'](L_concat('Trying to revert object to the same thing: ', L_tostring(originalname)))
						return None
				elif ((mat2_3 == 'revert') and (unitid_2 == 2)):
					G['MF_alert']('Trying to revert empty')
					return None
				if ((((mat2_3 != 'empty') and (mat2_3 != 'error')) and (mat2_3 != 'revert')) and (mat2_3 != 'createall')):
					if (mats2data[1] != 'revert'):
						unitname = G['unitreference'][mat2_3]
					if (mat2_3 == 'level'):
						unitname = 'level'
					if (unitname is None):
						G['MF_alert'](L_concat('no className found for ', mat2_3, '!'))
						return None
					newunitid = G['MF_emptycreate'](unitname, x_2, y_2)
					newunit = G['mmf']['newObject'](newunitid)
					newunit['values'][G['ONLINE']] = 1
					newunit['values'][G['XPOS']] = x_2
					newunit['values'][G['YPOS']] = y_2
					newunit['values'][G['DIR']] = dir__2
					newunit['values'][G['POSITIONING']] = 20
					newunit['values'][G['VISUALLEVEL']] = unit_3['values'][G['VISUALLEVEL']]
					newunit['values'][G['VISUALSTYLE']] = unit_3['values'][G['VISUALSTYLE']]
					newunit['values'][G['COMPLETED']] = completed
					newunit['strings'][G['COLOUR']] = unit_3['strings'][G['COLOUR']]
					newunit['strings'][G['CLEARCOLOUR']] = unit_3['strings'][G['CLEARCOLOUR']]
					if (unitname == 'level'):
						newunit['values'][G['COMPLETED']] = L_max(completed, 1)
						newunit['flags'][G['LEVEL_JUSTCONVERTED']] = True
						if (L_strlen(unit_3['strings'][G['LEVELFILE']]) > 0):
							newunit['values'][G['COMPLETED']] = L_max(completed, 2)
						if ((L_strlen(unit_3['strings'][G['COLOUR']]) == 0) or (L_strlen(unit_3['strings'][G['CLEARCOLOUR']]) == 0)):
							newunit['strings'][G['COLOUR']] = '1,2'
							newunit['strings'][G['CLEARCOLOUR']] = '1,3'
							G['MF_setcolour'](newunitid, 1, 2)
						else:
							c = G['MF_parsestring'](unit_3['strings'][G['COLOUR']])
							G['MF_setcolour'](newunitid, c[1], c[2])
						newunit['visible'] = True
					newunit['values'][G['ID']] = ingameid_2
					newunit['strings'][G['U_LEVELFILE']] = unit_3['strings'][G['U_LEVELFILE']]
					newunit['strings'][G['U_LEVELNAME']] = unit_3['strings'][G['U_LEVELNAME']]
					newunit['flags'][G['MAPLEVEL']] = unit_3['flags'][G['MAPLEVEL']]
					newunit['values'][G['EFFECT']] = 1
					newunit['flags'][9] = True
					newunit['flags'][G['CONVERTED']] = True
					cdata[2] = mat2_3
					G['addundo'](L_T(['convert', cdata[1], cdata[2], ingameid_2, baseingameid, x_2, y_2, dir__2]))
					G['addundo'](L_T(['create', mat2_3, ingameid_2, baseingameid, 'convert', x_2, y_2, dir__2]))
					G['addunit'](newunitid)
					G['addunitmap'](newunitid, x_2, y_2, newunit['strings'][G['UNITNAME']])
					G['poscorrect'](newunitid, G['generaldata2']['values'][G['ROOMROTATION']], G['generaldata2']['values'][G['ZOOM']], 0)
					if ((G['spritedata']['values'][G['VISION']] == 0) or (((newunit['values'][G['TILING']] == 1) and (newunit['values'][G['ZLAYER']] <= 10)) and (newunit['values'][G['ZLAYER']] >= 0))):
						G['dynamic'](newunitid)
					newunit['new'] = False
					newunit['originalname'] = unit_3['originalname']
					if (newunit['strings'][G['UNITTYPE']] == 'text'):
						G['updatecode'] = 1
					else:
						newname = newunit['strings'][G['UNITNAME']]
						notnewname = L_concat('not ', newunit['strings'][G['UNITNAME']])
						if (G['featureindex']['word'] is not None):
							for i_7, v_4 in L_ipairs(G['featureindex']['word']):
								rule_3 = v_4[1]
								conds_5 = v_4[2]
								if ((rule_3[2] == 'is') and (rule_3[3] == 'word')):
									if (rule_3[1] == newname):
										G['updatecode'] = 1
										break
									elif (unitid_2 != 2):
										if (rule_3[1] == unitname):
											G['updatecode'] = 1
											break
									if (L_len(conds_5) > 0):
										for a_6, b_2 in L_ipairs(conds_5):
											if ((b_2[2] is not None) and (L_len(b_2[2]) > 0)):
												for c_2, d_2 in L_ipairs(b_2[2]):
													if ((d_2 == newname) or ((L_sub(d_2, 1, 4) == 'not ') and (L_sub(d_2, 5) != newname))):
														G['updatecode'] = 1
														break
													elif (unitid_2 != 2):
														if ((d_2 == unitname) or ((L_sub(d_2, 1, 4) == 'not ') and (L_sub(d_2, 5) != unitname))):
															G['updatecode'] = 1
															break
					delthis = True
				elif (mat2_3 == 'error'):
					if (unitid_2 != 2):
						unit_4 = G['mmf']['newObject'](unitid_2)
						x_3, y_3 = unit_4['values'][G['XPOS']], unit_4['values'][G['YPOS']]
						pmult, sound = L_adjust((*G['checkeffecthistory']('paradox'),), 2)
						c1, c2 = L_adjust((*G['getcolour'](unitid_2),), 2)
						G['MF_particles']('unlock', x_3, y_3, (20 * pmult), c1, c2, 1, 1)
					delthis = True
				elif (mat2_3 == 'empty'):
					G['addundo'](L_T(['convert', cdata[1], 'empty', ingameid_2, baseingameid, x_2, y_2, dir__2]))
					G['updateunitmap'](unitid_2, x_2, y_2, x_2, y_2, unit_3['strings'][G['UNITNAME']])
					delthis = True
					tileid_3 = (x_2 + (y_2 * G['roomsizex']))
					if (G['emptydata'][tileid_3] is None):
						G['emptydata'][tileid_3] = L_T()
					G['emptydata'][tileid_3]['conv'] = True
				elif (mat2_3 == 'createall'):
					delthis_createall = G['createall_single'](unitid_2)
					delthis = delthis_createall
					delthis_createall_ = True
			if (((delthis_createall_ is not None and delthis_createall_ is not False) and (delthis_createall is False)) and (delthis is not None and delthis is not False)):
				delthis = False
			if ((delthis is not None and delthis is not False) and (unit_3['flags'][G['DEAD']] is False)):
				G['addundo'](L_T(['remove', unit_3['strings'][G['UNITNAME']], unit_3['values'][G['XPOS']], unit_3['values'][G['YPOS']], unit_3['values'][G['DIR']], unit_3['values'][G['ID']], unit_3['values'][G['ID']], unit_3['strings'][G['U_LEVELFILE']], unit_3['strings'][G['U_LEVELNAME']], unit_3['values'][G['VISUALLEVEL']], unit_3['values'][G['COMPLETED']], unit_3['values'][G['VISUALSTYLE']], unit_3['flags'][G['MAPLEVEL']], unit_3['strings'][G['COLOUR']], unit_3['strings'][G['CLEARCOLOUR']], unit_3['followed'], unit_3['back_init'], unit_3['originalname'], unit_3['strings'][G['UNITSIGNTEXT']], unit_3['holder']]))
				if (unit_3['strings'][G['UNITTYPE']] == 'text'):
					G['updatecode'] = 1
				G['delunit'](unitid_2)
				G['dynamic'](unitid_2)
				G['MF_specialremove'](unitid_2, 2)
		elif (style == 'emptyconvert'):
			for a_7, mats2data_2 in L_ipairs(mats2_3):
				mat2_4 = mats2data_2[1]
				i_8 = mats2data_2[2]
				j_2 = mats2data_2[3]
				if ((mat2_4 != 'createall') and (mat2_4 != 'error')):
					unitname_2 = G['unitreference'][mat2_4]
					newunitid_2 = G['MF_emptycreate'](unitname_2, i_8, j_2)
					newunit_2 = G['mmf']['newObject'](newunitid_2)
					cdata[1] = 'empty'
					id__3 = G['newid']()
					dir__3 = G['emptydir'](i_8, j_2)
					if (dir__3 == 4):
						dir__3 = G['fixedrandom'](0, 3)
					newunit_2['values'][G['ONLINE']] = 1
					newunit_2['values'][G['XPOS']] = i_8
					newunit_2['values'][G['YPOS']] = j_2
					newunit_2['values'][G['DIR']] = dir__3
					newunit_2['values'][G['ID']] = id__3
					newunit_2['values'][G['EFFECT']] = 1
					newunit_2['flags'][9] = True
					newunit_2['flags'][G['CONVERTED']] = True
					cdata[2] = mat2_4
					G['addundo'](L_T(['convert', cdata[1], cdata[2], id__3, id__3, i_8, j_2, dir__3]))
					G['addundo'](L_T(['create', mat2_4, id__3, (-1), 'emptyconvert', i_8, j_2, dir__3]))
					G['addunit'](newunitid_2)
					G['addunitmap'](newunitid_2, i_8, j_2, newunit_2['strings'][G['UNITNAME']])
					G['dynamic'](newunitid_2)
					newunit_2['originalname'] = 'empty'
					tileid_4 = (i_8 + (j_2 * G['roomsizex']))
					if (G['emptydata'][tileid_4] is None):
						G['emptydata'][tileid_4] = L_T()
					G['emptydata'][tileid_4]['conv'] = True
					if (newunit_2['strings'][G['UNITTYPE']] == 'text'):
						G['updatecode'] = 1
					else:
						if (G['featureindex']['word'] is not None):
							for i_9, v_5 in L_ipairs(G['featureindex']['word']):
								rule_4 = v_5[1]
								if (rule_4[1] == newunit_2['strings'][G['UNITNAME']]):
									G['updatecode'] = 1
								elif (unitid_2 != 2):
									if (rule_4[1] == unit_3['strings'][G['UNITNAME']]):
										G['updatecode'] = 1
				elif (mat2_4 == 'createall'):
					G['createall_single'](2, None, i_8, j_2)
	G['doconvert'] = f_doconvert
	def f_dolevelconversions(*_):  # L549
		if (((L_len(G['features']) > 0) and (G['generaldata']['values'][G['WINTIMER']] == 0)) and (G['destroylevel_check'] is False)):
			mats_2 = G['levelconversions']
			mat1_2 = 'level'
			levelmats = L_T()
			revert = False
			for i_10, matdata_3 in L_pairs(mats_2):
				conds_6 = matdata_3[2]
				mat2_5 = matdata_3[1]
				op_4 = matdata_3[3]
				if (op_4 == 'write'):
					mat2_5 = L_concat('text_', matdata_3[1])
				objectfound_3 = False
				if ((op_4 == 'become') and (mat2_5 == 'level')):
					op_4 = 'is'
					mat2_5 = 'revert'
				if (G['unitreference'][mat2_5] is not None):
					object_5 = G['unitreference'][mat2_5]
					if ((G['tileslist'][object_5]['name'] == mat2_5) and ((G['changes'][object_5] is None) or (G['changes'][object_5]['name'] is None))):
						objectfound_3 = True
					elif (G['changes'][object_5] is not None):
						if ((G['changes'][object_5]['name'] is not None) and (G['changes'][object_5]['name'] == mat2_5)):
							objectfound_3 = True
				elif ((mat2_5 == 'error') and L_t(G['testcond'](conds_6, 1))):
					G['destroylevel']()
				elif (mat2_5 == 'revert'):
					objectfound_3 = True
				if (L_t(G['testcond'](conds_6, 1)) and (objectfound_3 is not None and objectfound_3 is not False)):
					if (mat2_5 != 'revert'):
						L_insert(levelmats, mat2_5)
						G['MF_alert'](L_concat('Converting level into ', mat2_5))
					else:
						revert = True
						levelmats = L_T(['revert'])
						break
			if ((L_len(levelmats) > 0) and (L_len(levelmats) < 50)):
				if (G['editor']['values'][G['INEDITOR']] == 0):
					if (revert is False):
						G['level_to_convert'] = L_T([G['generaldata']['strings'][G['CURRLEVEL']], levelmats])
						savestring = ''
						for a_8, b_3 in L_pairs(levelmats):
							savestring = L_concat(savestring, b_3, ',')
						upperlevel = (_t1 if L_t(_t1 := G['leveltree'][(L_len(G['leveltree']) - 1)]) else G['generaldata']['strings'][G['CURRLEVEL']])
						convertdata = G['MF_read']('save', L_concat(G['generaldata']['strings'][G['WORLD']], '_', upperlevel, '_convert'), 'converts')
						levelconverts = (_t2 if L_t(_t2 := L_tonumber(convertdata)) else 0)
						idtostore = levelconverts
						if (levelconverts == 0):
							totalconverts = (_t3 if L_t(_t3 := L_tonumber(G['MF_read']('save', L_concat(G['generaldata']['strings'][G['WORLD']], '_converts'), 'total'))) else 0)
							G['MF_store']('save', L_concat(G['generaldata']['strings'][G['WORLD']], '_converts'), L_tostring(totalconverts), L_concat(G['generaldata']['strings'][G['WORLD']], '_', upperlevel, '_convert'))
							totalconverts = (totalconverts + 1)
							G['MF_store']('save', L_concat(G['generaldata']['strings'][G['WORLD']], '_converts'), 'total', L_tostring(totalconverts))
						if (levelconverts > 0):
							for a_9 in L_range(1, levelconverts):
								result = L_first(L_find(L_concat('___', G['MF_read']('save', L_concat(G['generaldata']['strings'][G['WORLD']], '_', upperlevel, '_convert'), L_tostring((a_9 - 1)))), L_concat('___', G['generaldata']['strings'][G['CURRLEVEL']])))
								if (result is not None):
									idtostore = (a_9 - 1)
						G['MF_store']('save', L_concat(G['generaldata']['strings'][G['WORLD']], '_', upperlevel, '_convert'), L_tostring(idtostore), L_concat(G['generaldata']['strings'][G['CURRLEVEL']], ',', savestring))
						if (idtostore == levelconverts):
							levelconverts = (levelconverts + 1)
							G['MF_store']('save', L_concat(G['generaldata']['strings'][G['WORLD']], '_', upperlevel, '_convert'), 'converts', L_tostring(levelconverts))
					else:
						G['level_to_convert'] = L_T([G['generaldata']['strings'][G['CURRLEVEL']], levelmats])
						upperlevel_2 = (_t4 if L_t(_t4 := G['leveltree'][(L_len(G['leveltree']) - 1)]) else G['generaldata']['strings'][G['CURRLEVEL']])
						convertdata_2 = G['MF_read']('save', L_concat(G['generaldata']['strings'][G['WORLD']], '_', upperlevel_2, '_convert'), 'converts')
						levelconverts_2 = (_t5 if L_t(_t5 := L_tonumber(convertdata_2)) else 0)
						found = (-1)
						if (levelconverts_2 > 0):
							for a_10 in L_range(1, levelconverts_2):
								result_2 = L_first(L_find(L_concat('___', G['MF_read']('save', L_concat(G['generaldata']['strings'][G['WORLD']], '_', upperlevel_2, '_convert'), L_tostring((a_10 - 1)))), L_concat('___', G['generaldata']['strings'][G['CURRLEVEL']])))
								if (result_2 is not None):
									found = a_10
								if ((found > 0) and (a_10 > found)):
									newa = (a_10 - 1)
									datatostore = G['MF_read']('save', L_concat(G['generaldata']['strings'][G['WORLD']], '_', upperlevel_2, '_convert'), L_tostring((a_10 - 1)))
									G['MF_store']('save', L_concat(G['generaldata']['strings'][G['WORLD']], '_', upperlevel_2, '_convert'), L_tostring((newa - 1)), datatostore)
						if (found > 0):
							levelconverts_2 = (levelconverts_2 - 1)
							if (levelconverts_2 > 0):
								G['MF_store']('save', L_concat(G['generaldata']['strings'][G['WORLD']], '_', upperlevel_2, '_convert'), 'converts', L_tostring(levelconverts_2))
							else:
								G['MF_deletesave_group'](L_concat(G['generaldata']['strings'][G['WORLD']], '_', upperlevel_2, '_convert'), 'converts')
								totalconverts_2 = L_tonumber(G['MF_read']('save', L_concat(G['generaldata']['strings'][G['WORLD']], '_converts'), 'total'))
								found2 = (-1)
								if (totalconverts_2 is not None):
									for a_11 in L_range(1, totalconverts_2):
										result_3 = L_first(L_find(L_concat('___', G['MF_read']('save', L_concat(G['generaldata']['strings'][G['WORLD']], '_converts'), L_tostring((a_11 - 1)))), L_concat('___', G['generaldata']['strings'][G['WORLD']], '_', upperlevel_2, '_convert')))
										if (result_3 is not None):
											found2 = a_11
										if ((found2 > 0) and (a_11 > found2)):
											newa_2 = (a_11 - 1)
											datatostore_2 = G['MF_read']('save', L_concat(G['generaldata']['strings'][G['WORLD']], '_converts'), L_tostring((a_11 - 1)))
											G['MF_store']('save', L_concat(G['generaldata']['strings'][G['WORLD']], '_converts'), L_tostring((newa_2 - 1)), datatostore_2)
								if (found2 > 0):
									totalconverts_2 = (totalconverts_2 - 1)
									if (totalconverts_2 > 0):
										G['MF_store']('save', L_concat(G['generaldata']['strings'][G['WORLD']], '_converts'), 'total', L_tostring(totalconverts_2))
									else:
										G['MF_deletesave_group'](L_concat(G['generaldata']['strings'][G['WORLD']], '_converts'))
					G['uplevel']()
				else:
					G['level_to_convert'] = L_T()
				G['MF_levelconversion']()
			elif (L_len(levelmats) >= 50):
				G['HACK_INFINITY'] = 200
				G['destroylevel']('toocomplex')
			G['levelconversions'] = L_T()
	G['dolevelconversions'] = f_dolevelconversions
	def f_handleconvertedlevels(level=None, mats_3=None, *_):  # L720
		if (L_len(mats_3) > 0):
			G['level_to_convert'] = L_T([level, mats_3])
			G['convertlevel']()
	G['handleconvertedlevels'] = f_handleconvertedlevels
	def f_convertlevel(*_):  # L728
		doundostate = G['doundo']
		G['doundo'] = False
		for i_11, unit_5 in L_pairs(G['units']):
			if ((unit_5['strings'][G['LEVELFILE']] == G['level_to_convert'][1]) and (unit_5['flags'][G['CONVERTED']] is False)):
				mats_4 = G['level_to_convert'][2]
				mats2_4 = L_T()
				for a_12, b_4 in L_ipairs(mats_4):
					ingameid_3 = unit_5['values'][G['ID']]
					if (a_12 > 1):
						ingameid_3 = G['newid']()
					L_insert(mats2_4, L_T([b_4, ingameid_3, None]))
				G['doconvert'](L_T([unit_5['fixed'], 'convert', mats2_4]))
		G['doundo'] = doundostate
	G['convertlevel'] = f_convertlevel
