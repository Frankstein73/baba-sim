"""Generated from conditions.lua by tools/lua2py.py. Do not edit."""
from babasim.luart import *  # noqa: F403


def load(G):
	def f_testcond(conds=None, unitid=None, x_=None, y_=None, autofail_=None, limit_=None, checkedconds_=None, ignorebroken_=None, subgroup_=None, *_):  # L1
		result = True
		orhandling = False
		orresult = False
		x, y, name, dir_, broken = 0, 0, '', 4, 0
		surrounds = L_T()
		autofail = (_t1 if L_t(_t1 := autofail_) else L_T())
		limit = (_t2 if L_t(_t2 := limit_) else 0)
		limit = (limit + 1)
		if (limit > 80):
			G['HACK_INFINITY'] = 200
			G['destroylevel']('infinity')
			return None
		checkedconds = L_T()
		ignorebroken = (_t3 if L_t(_t3 := ignorebroken_) else False)
		subgroup = (_t4 if L_t(_t4 := subgroup_) else L_T())
		if (checkedconds_ is not None):
			for i, v in L_pairs(checkedconds_):
				checkedconds[i] = v
		if (L_len(G['features']) == 0):
			return False
		if ((((unitid != 0) and (unitid != 1)) and (unitid != 2)) and (unitid is not None)):
			unit = G['mmf']['newObject'](unitid)
			x = unit['values'][G['XPOS']]
			y = unit['values'][G['YPOS']]
			name = unit['strings'][G['UNITNAME']]
			dir_ = unit['values'][G['DIR']]
			broken = (_t5 if L_t(_t5 := unit['broken']) else 0)
			if (unit['strings'][G['UNITTYPE']] == 'text'):
				name = 'text'
		elif (unitid == 2):
			x = x_
			y = y_
			name = 'empty'
			broken = 0
			if (((G['featureindex']['broken'] is not None) and (ignorebroken is False)) and (checkedconds[L_tostring(conds)] is None)):
				checkedconds[L_tostring(conds)] = 1
				broken = G['isitbroken']('empty', 2, x, y, checkedconds)
		elif (unitid == 1):
			name = 'level'
			surrounds = G['parsesurrounds']()
			dir_ = (_t6 if L_t(_t6 := L_tonumber(surrounds['dir'])) else 4)
			broken = 0
			if (((G['featureindex']['broken'] is not None) and (ignorebroken is False)) and (checkedconds[L_tostring(conds)] is None)):
				checkedconds[L_tostring(conds)] = 1
				broken = G['isitbroken']('level', 1, x, y, checkedconds)
		checkedconds[L_tostring(conds)] = 1
		checkedconds[L_concat(L_tostring(conds), '_s_')] = 1
		if ((unitid == 0) or (unitid is None)):
			L_noop(L_concat('WARNING!! Unitid is ', L_tostring(unitid)))
		if (ignorebroken is not None and ignorebroken is not False):
			broken = 0
		if (broken == 1):
			result = False
		if ((conds is not None) and ((broken is None) or (broken == 0))):
			if (L_len(conds) > 0):
				valid = False
				for i_2, cond in L_ipairs(conds):
					condtype = cond[1]
					params_ = cond[2]
					params = L_T()
					extras = L_T()
					if (L_sub(condtype, 1, 1) == '('):
						condtype = L_sub(condtype, 2)
						orhandling = True
						orresult = False
					if (L_sub(condtype, (-1)) == ')'):
						condtype = L_sub(condtype, 1, (L_strlen(condtype) - 1))
					basecondtype = L_sub(condtype, 1, 4)
					notcond = False
					if (basecondtype == 'not '):
						basecondtype = L_sub(condtype, 5)
						notcond = True
					else:
						basecondtype = condtype
					if (condtype != 'never'):
						condname = G['unitreference'][L_concat('text_', basecondtype)]
						conddata = (_t7 if L_t(_t7 := G['conditions'][condname]) else L_T())
						if (conddata['argextra'] is not None):
							extras = conddata['argextra']
					for a, b in L_ipairs(autofail):
						if (condtype == b):
							result = False
							valid = True
					if ((result is False) and (valid is not None and valid is not False)):
						break
					if (params_ is not None):
						handlegroup = False
						for a_2, b_2 in L_ipairs(params_):
							if (L_sub(b_2, 1, 4) == 'not '):
								L_insert(params, b_2)
							else:
								L_insert(params, 1, b_2)
							if ((L_sub(b_2, 1, 5) == 'group') or (L_sub(b_2, 1, 9) == 'not group')):
								handlegroup = True
						removegroup = L_T()
						removegroupoffset = 0
						if (handlegroup is not None and handlegroup is not False):
							plimit = L_len(params)
							for a_3 in L_range(1, plimit):
								b_3 = params[a_3]
								mem = subgroup_
								notnoun = False
								if (L_sub(b_3, 1, 5) == 'group'):
									if (mem is None):
										mem = G['findgroup'](b_3, False, limit, checkedconds)
									L_insert(removegroup, a_3)
								elif (L_sub(b_3, 1, 9) == 'not group'):
									notnoun = True
									if (mem is None):
										mem = G['findgroup'](L_sub(b_3, 5), True, limit, checkedconds)
									else:
										memfound = L_T()
										for c, d in L_ipairs(mem):
											memfound[d] = 1
										mem = L_T()
										for c_2, mat in L_pairs(G['objectlist']):
											if ((memfound[c_2] is None) and (G['findnoun'](c_2, G['nlist']['short']) is False)):
												L_insert(mem, c_2)
									L_insert(removegroup, a_3)
								if (mem is not None):
									for c_3, d_2 in L_ipairs(mem):
										if (notnoun is not None and notnoun is not False):
											L_insert(params, d_2)
										else:
											L_insert(params, 1, d_2)
											removegroupoffset = (removegroupoffset - 1)
								if ((mem is None) or (L_len(mem) == 0)):
									L_insert(params, '_NONE_')
									break
							for a_4, b_4 in L_ipairs(removegroup):
								L_remove(params, (b_4 - removegroupoffset))
								removegroupoffset = (removegroupoffset + 1)
					condsubtype = ''
					if (L_sub(basecondtype, 1, 7) == 'powered'):
						for a_5, b_5 in L_pairs(G['condlist']):
							if ((L_len(basecondtype) > L_len(a_5)) and (L_sub(basecondtype, 1, L_len(a_5)) == a_5)):
								condsubtype = L_sub(basecondtype, (L_len(a_5) + 1))
								basecondtype = L_sub(basecondtype, 1, L_len(a_5))
								break
					if (G['condlist'][basecondtype] is not None):
						valid = True
						cfunc = G['condlist'][basecondtype]
						subresult = True
						ccc = False
						cdata = L_T([], {'name': name, 'x': x, 'y': y, 'unitid': unitid, 'dir': dir_, 'extras': extras, 'limit': limit, 'conds': conds, 'subtype': condsubtype, 'i': i_2, 'surrounds': surrounds, 'notcond': notcond, 'debugname': cond[1]})
						subresult, checkedconds, ccc = cfunc(params, checkedconds, checkedconds_, cdata), None, None
						clearcconds = (_t8 if L_t(_t8 := ccc) else False)
						if (notcond is not None and notcond is not False):
							subresult = (not (subresult is not None and subresult is not False))
						if ((subresult is not None and subresult is not False) and (clearcconds is not None and clearcconds is not False)):
							checkedconds = L_T()
							if (checkedconds_ is not None):
								for i_3, v_2 in L_pairs(checkedconds_):
									checkedconds[i_3] = v_2
							checkedconds[L_tostring(conds)] = 1
							checkedconds[L_concat(L_tostring(conds), '_s_')] = 1
						if (subresult is False):
							if (orhandling is False):
								result = False
								break
						elif (orhandling is not None and orhandling is not False):
							orresult = True
					else:
						G['MF_alert'](L_concat('condtype ', L_tostring(condtype), " doesn't exist?"))
						result = False
						break
					if (L_sub(cond[1], (-1)) == ')'):
						orhandling = False
						if (orresult is False):
							result = False
							break
						else:
							result = True
				if (valid is False):
					G['MF_alert']('invalid condition!')
					result = True
					for a_6, b_6 in L_ipairs(conds):
						G['MF_alert'](L_tostring(b_6[1]))
		return result
	G['testcond'] = f_testcond
	def _anon1(params_2=None, checkedconds_2=None, *_):  # L293
		return False
	def _anon2(params_3=None, checkedconds_3=None, checkedconds__2=None, cdata_2=None, *_):  # L296
		allfound = 0
		alreadyfound = L_T()
		unitid_2, x_2, y_2, surrounds_2 = cdata_2['unitid'], cdata_2['x'], cdata_2['y'], cdata_2['surrounds']
		tileid = (x_2 + (y_2 * G['roomsizex']))
		if (unitid_2 != 2):
			if (L_len(params_3) > 0):
				for a_7, b_7 in L_ipairs(params_3):
					pname = b_7
					pnot = False
					if (L_sub(b_7, 1, 4) == 'not '):
						pnot = True
						pname = L_sub(b_7, 5)
					bcode = L_concat(b_7, '_', L_tostring(a_7))
					if (L_sub(pname, 1, 5) == 'group'):
						return False
					if (unitid_2 != 1):
						if (((pname != 'empty') and (b_7 != 'level')) or ((b_7 == 'level') and (alreadyfound[1] is not None))):
							if (G['unitmap'][tileid] is not None):
								for c_4, d_3 in L_ipairs(G['unitmap'][tileid]):
									if ((d_3 != unitid_2) and (alreadyfound[d_3] is None)):
										unit_2 = G['mmf']['newObject'](d_3)
										name_ = G['getname'](unit_2)
										if (pnot is False):
											if ((name_ == pname) and (alreadyfound[bcode] is None)):
												alreadyfound[bcode] = 1
												alreadyfound[d_3] = 1
												allfound = (allfound + 1)
										else:
											if (((name_ != pname) and (alreadyfound[bcode] is None)) and (name_ != 'text')):
												alreadyfound[bcode] = 1
												alreadyfound[d_3] = 1
												allfound = (allfound + 1)
							else:
								L_noop(L_concat('unitmap is nil at ', L_tostring(x_2), ', ', L_tostring(y_2), ' for object ', L_tostring(G['name']), ' (', L_tostring(unitid_2), ')!'))
						elif (pname == 'empty'):
							if (pnot is False):
								return False
							else:
								if (G['unitmap'][tileid] is not None):
									for c_5, d_4 in L_ipairs(G['unitmap'][tileid]):
										if ((d_4 != unitid_2) and (alreadyfound[d_4] is None)):
											alreadyfound[bcode] = 1
											alreadyfound[d_4] = 1
											allfound = (allfound + 1)
						elif (((b_7 == 'level') and (alreadyfound[bcode] is None)) and (alreadyfound[1] is None)):
							alreadyfound[bcode] = 1
							alreadyfound[1] = 1
							allfound = (allfound + 1)
					else:
						ulist = False
						if ((b_7 != 'empty') and (b_7 != 'level')):
							if (pnot is False):
								if (((G['unitlists'][b_7] is not None) and (L_len(G['unitlists'][b_7]) > 0)) and (alreadyfound[bcode] is None)):
									for c_6, d_5 in L_ipairs(G['unitlists'][b_7]):
										if (alreadyfound[d_5] is None):
											alreadyfound[bcode] = 1
											alreadyfound[d_5] = 1
											ulist = True
											break
							else:
								for c_7, d_6 in L_pairs(G['unitlists']):
									tested = False
									if ((c_7 != pname) and (L_len(d_6) > 0)):
										for e, f in L_ipairs(d_6):
											if ((alreadyfound[f] is None) and (alreadyfound[bcode] is None)):
												alreadyfound[bcode] = 1
												alreadyfound[f] = 1
												ulist = True
												tested = True
												break
									if (tested is not None and tested is not False):
										break
						elif (b_7 == 'empty'):
							empties = G['findempty']()
							if (L_len(empties) > 0):
								for c_8, d_7 in L_ipairs(empties):
									if ((alreadyfound[d_7] is None) and (alreadyfound[bcode] is None)):
										alreadyfound[bcode] = 1
										alreadyfound[d_7] = 1
										ulist = True
										break
						elif (b_7 == 'level'):
							for c_9, unit_3 in L_ipairs(G['units']):
								if (((unit_3['className'] == 'level') and (alreadyfound[unit_3['fixed']] is None)) and (alreadyfound[bcode] is None)):
									alreadyfound[bcode] = 1
									alreadyfound[unit_3['fixed']] = 1
									ulist = True
									break
						if ((b_7 != 'text') and (ulist is False)):
							if (surrounds_2['o'] is not None):
								for c_10, d_8 in L_ipairs(surrounds_2['o']):
									if (pnot is False):
										if ((d_8 == pname) and (alreadyfound[bcode] is None)):
											alreadyfound[bcode] = 1
											ulist = True
									else:
										if ((d_8 != pname) and (alreadyfound[bcode] is None)):
											alreadyfound[bcode] = 1
											ulist = True
						if ((ulist is not None and ulist is not False) or (b_7 == 'text')):
							alreadyfound[bcode] = 1
							allfound = (allfound + 1)
			else:
				L_noop('no parameters given!')
				return False
		else:
			for a_8, b_8 in L_ipairs(params_3):
				bcode_2 = L_concat(b_8, '_', L_tostring(a_8))
				if ((b_8 == 'level') and (alreadyfound[bcode_2] is None)):
					alreadyfound[bcode_2] = 1
					allfound = (allfound + 1)
				else:
					return False
		return (allfound == L_len(params_3))
	def _anon3(params_4=None, checkedconds_4=None, checkedconds__3=None, cdata_3=None, *_):  # L468
		allfound_2 = 0
		alreadyfound_2 = L_T()
		unitid_3, x_3, y_3, surrounds_3 = cdata_3['unitid'], cdata_3['x'], cdata_3['y'], cdata_3['surrounds']
		if (L_len(params_4) > 0):
			for a_9, b_9 in L_ipairs(params_4):
				pname_2 = b_9
				pnot_2 = False
				if (L_sub(b_9, 1, 4) == 'not '):
					pnot_2 = True
					pname_2 = L_sub(b_9, 5)
				bcode_3 = L_concat(b_9, '_', L_tostring(a_9))
				if (L_sub(pname_2, 1, 5) == 'group'):
					return False
				if (unitid_3 != 1):
					if ((b_9 != 'level') or ((b_9 == 'level') and (alreadyfound_2[1] is not None))):
						for g in L_range((-1), 1):
							for h in L_range((-1), 1):
								if (pname_2 != 'empty'):
									tileid_2 = ((x_3 + g) + ((y_3 + h) * G['roomsizex']))
									if (G['unitmap'][tileid_2] is not None):
										for c_11, d_9 in L_ipairs(G['unitmap'][tileid_2]):
											if ((d_9 != unitid_3) and (alreadyfound_2[d_9] is None)):
												unit_4 = G['mmf']['newObject'](d_9)
												name__2 = G['getname'](unit_4)
												if (pnot_2 is False):
													if ((name__2 == pname_2) and (alreadyfound_2[bcode_3] is None)):
														alreadyfound_2[bcode_3] = 1
														alreadyfound_2[d_9] = 1
														allfound_2 = (allfound_2 + 1)
												else:
													if (((name__2 != pname_2) and (alreadyfound_2[bcode_3] is None)) and (name__2 != 'text')):
														alreadyfound_2[bcode_3] = 1
														alreadyfound_2[d_9] = 1
														allfound_2 = (allfound_2 + 1)
								else:
									nearempty = False
									tileid_3 = ((x_3 + g) + ((y_3 + h) * G['roomsizex']))
									l = G['map'][0]
									tile = L_invoke(l, 'get_x', (x_3 + g), (y_3 + h))
									tcode = L_concat(L_tostring(tileid_3), 'e')
									if ((((G['unitmap'][tileid_3] is None) or (L_len(G['unitmap'][tileid_3]) == 0)) and (tile == 255)) and (alreadyfound_2[tcode] is None)):
										nearempty = True
									if ((g == 0) and (h == 0)):
										if (unitid_3 == 2):
											if (pnot_2 is False):
												nearempty = False
										elif ((unitid_3 != 1) and (pnot_2 is not None and pnot_2 is not False)):
											if ((G['unitmap'][tileid_3] is None) or (L_len(G['unitmap'][tileid_3]) <= 1)):
												nearempty = True
									if (pnot_2 is False):
										if ((nearempty is not None and nearempty is not False) and (alreadyfound_2[bcode_3] is None)):
											alreadyfound_2[bcode_3] = 1
											alreadyfound_2[tcode] = 1
											allfound_2 = (allfound_2 + 1)
									else:
										if ((nearempty is False) and (alreadyfound_2[bcode_3] is None)):
											alreadyfound_2[bcode_3] = 1
											alreadyfound_2[tcode] = 1
											allfound_2 = (allfound_2 + 1)
					elif (((b_9 == 'level') and (alreadyfound_2[bcode_3] is None)) and (alreadyfound_2[1] is None)):
						alreadyfound_2[bcode_3] = 1
						alreadyfound_2[1] = 1
						allfound_2 = (allfound_2 + 1)
				else:
					ulist_2 = False
					if ((b_9 != 'empty') and (b_9 != 'level')):
						if (pnot_2 is False):
							if ((G['unitlists'][pname_2] is not None) and (L_len(G['unitlists'][pname_2]) > 0)):
								for c_12, d_10 in L_ipairs(G['unitlists'][pname_2]):
									if ((alreadyfound_2[d_10] is None) and (alreadyfound_2[bcode_3] is None)):
										alreadyfound_2[bcode_3] = 1
										alreadyfound_2[d_10] = 1
										ulist_2 = True
										break
						else:
							for c_13, d_11 in L_pairs(G['unitlists']):
								tested_2 = False
								if ((c_13 != pname_2) and (L_len(d_11) > 0)):
									for e_2, f_2 in L_ipairs(d_11):
										if ((alreadyfound_2[f_2] is None) and (alreadyfound_2[bcode_3] is None)):
											alreadyfound_2[bcode_3] = 1
											alreadyfound_2[f_2] = 1
											ulist_2 = True
											tested_2 = True
											break
								if (tested_2 is not None and tested_2 is not False):
									break
					elif (b_9 == 'empty'):
						empties_2 = G['findempty']()
						if (L_len(empties_2) > 0):
							for c_14, d_12 in L_ipairs(empties_2):
								if ((alreadyfound_2[d_12] is None) and (alreadyfound_2[bcode_3] is None)):
									alreadyfound_2[bcode_3] = 1
									alreadyfound_2[d_12] = 1
									ulist_2 = True
									break
					if ((b_9 != 'text') and (ulist_2 is False)):
						for e_3, f_3 in L_pairs(surrounds_3):
							if (e_3 != 'dir'):
								for c_15, d_13 in L_ipairs(f_3):
									if (pnot_2 is False):
										if (((ulist_2 is False) and (d_13 == pname_2)) and (alreadyfound_2[bcode_3] is None)):
											alreadyfound_2[bcode_3] = 1
											ulist_2 = True
									else:
										if (((ulist_2 is False) and (d_13 != pname_2)) and (alreadyfound_2[bcode_3] is None)):
											alreadyfound_2[bcode_3] = 1
											ulist_2 = True
					if ((ulist_2 is not None and ulist_2 is not False) or (b_9 == 'text')):
						alreadyfound_2[bcode_3] = 1
						allfound_2 = (allfound_2 + 1)
		else:
			L_noop('no parameters given!')
			return False
		return (allfound_2 == L_len(params_4))
	def _anon4(params_5=None, checkedconds_5=None, checkedconds__4=None, cdata_4=None, *_):  # L647
		allfound_3 = 0
		alreadyfound_3 = L_T()
		unitid_4, x_4, y_4, surrounds_4 = cdata_4['unitid'], cdata_4['x'], cdata_4['y'], cdata_4['surrounds']
		if (L_len(params_5) > 0):
			for a_10, b_10 in L_ipairs(params_5):
				pname_3 = b_10
				pnot_3 = False
				if (L_sub(b_10, 1, 4) == 'not '):
					pnot_3 = True
					pname_3 = L_sub(b_10, 5)
				bcode_4 = L_concat(b_10, '_', L_tostring(a_10))
				if (L_sub(pname_3, 1, 5) == 'group'):
					return False
				if (unitid_4 != 1):
					if ((b_10 != 'level') or ((b_10 == 'level') and (alreadyfound_3[1] is not None))):
						for g_2 in L_range((-1), 1):
							for h_2 in L_range((-1), 1):
								if (((h_2 != 0) and (g_2 == 0)) or ((h_2 == 0) and (g_2 != 0))):
									if (pname_3 != 'empty'):
										tileid_4 = ((x_4 + g_2) + ((y_4 + h_2) * G['roomsizex']))
										if (G['unitmap'][tileid_4] is not None):
											for c_16, d_14 in L_ipairs(G['unitmap'][tileid_4]):
												if ((d_14 != unitid_4) and (alreadyfound_3[d_14] is None)):
													unit_5 = G['mmf']['newObject'](d_14)
													name__3 = G['getname'](unit_5)
													if (pnot_3 is False):
														if ((name__3 == pname_3) and (alreadyfound_3[bcode_4] is None)):
															alreadyfound_3[bcode_4] = 1
															alreadyfound_3[d_14] = 1
															allfound_3 = (allfound_3 + 1)
													else:
														if (((name__3 != pname_3) and (alreadyfound_3[bcode_4] is None)) and (name__3 != 'text')):
															alreadyfound_3[bcode_4] = 1
															alreadyfound_3[d_14] = 1
															allfound_3 = (allfound_3 + 1)
									else:
										nearempty_2 = False
										tileid_5 = ((x_4 + g_2) + ((y_4 + h_2) * G['roomsizex']))
										l_2 = G['map'][0]
										tile_2 = L_invoke(l_2, 'get_x', (x_4 + g_2), (y_4 + h_2))
										tcode_2 = L_concat(L_tostring(tileid_5), 'e')
										if ((((G['unitmap'][tileid_5] is None) or (L_len(G['unitmap'][tileid_5]) == 0)) and (tile_2 == 255)) and (alreadyfound_3[tcode_2] is None)):
											nearempty_2 = True
										if ((g_2 == 0) and (h_2 == 0)):
											if (unitid_4 == 2):
												if (pnot_3 is False):
													nearempty_2 = False
											elif ((unitid_4 != 1) and (pnot_3 is not None and pnot_3 is not False)):
												if ((G['unitmap'][tileid_5] is None) or (L_len(G['unitmap'][tileid_5]) <= 1)):
													nearempty_2 = True
										if (pnot_3 is False):
											if ((nearempty_2 is not None and nearempty_2 is not False) and (alreadyfound_3[bcode_4] is None)):
												alreadyfound_3[bcode_4] = 1
												alreadyfound_3[tcode_2] = 1
												allfound_3 = (allfound_3 + 1)
										else:
											if ((nearempty_2 is False) and (alreadyfound_3[bcode_4] is None)):
												alreadyfound_3[bcode_4] = 1
												alreadyfound_3[tcode_2] = 1
												allfound_3 = (allfound_3 + 1)
					elif (((b_10 == 'level') and (alreadyfound_3[bcode_4] is None)) and (alreadyfound_3[1] is None)):
						alreadyfound_3[bcode_4] = 1
						alreadyfound_3[1] = 1
						allfound_3 = (allfound_3 + 1)
				else:
					ulist_3 = False
					if ((b_10 != 'empty') and (b_10 != 'level')):
						if (pnot_3 is False):
							if ((G['unitlists'][pname_3] is not None) and (L_len(G['unitlists'][pname_3]) > 0)):
								for c_17, d_15 in L_ipairs(G['unitlists'][pname_3]):
									if ((alreadyfound_3[d_15] is None) and (alreadyfound_3[bcode_4] is None)):
										alreadyfound_3[bcode_4] = 1
										alreadyfound_3[d_15] = 1
										ulist_3 = True
										break
						else:
							for c_18, d_16 in L_pairs(G['unitlists']):
								tested_3 = False
								if ((c_18 != pname_3) and (L_len(d_16) > 0)):
									for e_4, f_4 in L_ipairs(d_16):
										if ((alreadyfound_3[f_4] is None) and (alreadyfound_3[bcode_4] is None)):
											alreadyfound_3[bcode_4] = 1
											alreadyfound_3[f_4] = 1
											ulist_3 = True
											tested_3 = True
											break
								if (tested_3 is not None and tested_3 is not False):
									break
					elif (b_10 == 'empty'):
						empties_3 = G['findempty']()
						if (L_len(empties_3) > 0):
							for c_19, d_17 in L_ipairs(empties_3):
								if ((alreadyfound_3[d_17] is None) and (alreadyfound_3[bcode_4] is None)):
									alreadyfound_3[bcode_4] = 1
									alreadyfound_3[d_17] = 1
									ulist_3 = True
									break
					if ((b_10 != 'text') and (ulist_3 is False)):
						for e_5, f_5 in L_pairs(surrounds_4):
							if ((e_5 != 'dir') and (e_5 != 'o')):
								for c_20, d_18 in L_ipairs(f_5):
									if (pnot_3 is False):
										if (((ulist_3 is False) and (d_18 == pname_3)) and (alreadyfound_3[bcode_4] is None)):
											alreadyfound_3[bcode_4] = 1
											ulist_3 = True
									else:
										if (((ulist_3 is False) and (d_18 != pname_3)) and (alreadyfound_3[bcode_4] is None)):
											alreadyfound_3[bcode_4] = 1
											ulist_3 = True
					if ((ulist_3 is not None and ulist_3 is not False) or (b_10 == 'text')):
						alreadyfound_3[bcode_4] = 1
						allfound_3 = (allfound_3 + 1)
		else:
			L_noop('no parameters given!')
			return False
		return (allfound_3 == L_len(params_5))
	def _anon5(params_6=None, checkedconds_6=None, checkedconds__5=None, cdata_5=None, *_):  # L828
		allfound_4 = 0
		alreadyfound_4 = L_T()
		unitid_5, x_5, y_5, dir__2, extras_2, surrounds_5, conds_2 = cdata_5['unitid'], cdata_5['x'], cdata_5['y'], cdata_5['dir'], cdata_5['extras'], cdata_5['surrounds'], L_tostring(cdata_5['conds'])
		if ((unitid_5 == 2) and ((checkedconds__5 is None) or (checkedconds__5[conds_2] is None))):
			dir__2 = G['emptydir'](x_5, y_5, checkedconds_6)
		ndrs = G['ndirs'][(dir__2 + 1)]
		ox = ndrs[1]
		oy = ndrs[2]
		tileid_6 = ((x_5 + ox) + ((y_5 + oy) * G['roomsizex']))
		if ((L_len(params_6) > 0) and (dir__2 != 4)):
			for a_11, b_11 in L_ipairs(params_6):
				pname_4 = b_11
				pnot_4 = False
				if (L_sub(b_11, 1, 4) == 'not '):
					pnot_4 = True
					pname_4 = L_sub(b_11, 5)
				bcode_5 = L_concat(b_11, '_', L_tostring(a_11))
				if (L_sub(pname_4, 1, 5) == 'group'):
					return False
				if (unitid_5 != 1):
					if (((pname_4 != 'empty') and (b_11 != 'level')) or ((b_11 == 'level') and (alreadyfound_4[1] is not None))):
						if (G['stringintable'](pname_4, extras_2) is False):
							if (G['unitmap'][tileid_6] is not None):
								for c_21, d_19 in L_ipairs(G['unitmap'][tileid_6]):
									if ((d_19 != unitid_5) and (alreadyfound_4[d_19] is None)):
										unit_6 = G['mmf']['newObject'](d_19)
										name__4 = G['getname'](unit_6)
										if (pnot_4 is False):
											if ((name__4 == pname_4) and (alreadyfound_4[bcode_5] is None)):
												alreadyfound_4[bcode_5] = 1
												alreadyfound_4[d_19] = 1
												allfound_4 = (allfound_4 + 1)
										else:
											if (((name__4 != pname_4) and (alreadyfound_4[bcode_5] is None)) and (name__4 != 'text')):
												alreadyfound_4[bcode_5] = 1
												alreadyfound_4[d_19] = 1
												allfound_4 = (allfound_4 + 1)
						else:
							if (pnot_4 is False):
								if (((((pname_4 == 'right') and (dir__2 == 0)) or ((pname_4 == 'up') and (dir__2 == 1))) or ((pname_4 == 'left') and (dir__2 == 2))) or ((pname_4 == 'down') and (dir__2 == 3))):
									if (alreadyfound_4[bcode_5] is None):
										alreadyfound_4[bcode_5] = 1
										allfound_4 = (allfound_4 + 1)
							else:
								if (((((pname_4 == 'right') and (dir__2 != 0)) or ((pname_4 == 'up') and (dir__2 != 1))) or ((pname_4 == 'left') and (dir__2 != 2))) or ((pname_4 == 'down') and (dir__2 != 3))):
									if (alreadyfound_4[bcode_5] is None):
										alreadyfound_4[bcode_5] = 1
										allfound_4 = (allfound_4 + 1)
					elif (pname_4 == 'empty'):
						l_3 = G['map'][0]
						tile_3 = L_invoke(l_3, 'get_x', (x_5 + ox), (y_5 + oy))
						if (pnot_4 is False):
							if (((G['unitmap'][tileid_6] is None) or (L_len(G['unitmap'][tileid_6]) == 0)) and (tile_3 == 255)):
								if (alreadyfound_4[bcode_5] is None):
									alreadyfound_4[bcode_5] = 1
									allfound_4 = (allfound_4 + 1)
						else:
							if (((G['unitmap'][tileid_6] is not None) and (L_len(G['unitmap'][tileid_6]) > 0)) or (tile_3 != 255)):
								if (alreadyfound_4[bcode_5] is None):
									alreadyfound_4[bcode_5] = 1
									allfound_4 = (allfound_4 + 1)
					elif (((b_11 == 'level') and (alreadyfound_4[bcode_5] is None)) and (alreadyfound_4[1] is None)):
						alreadyfound_4[bcode_5] = 1
						alreadyfound_4[1] = 1
						allfound_4 = (allfound_4 + 1)
				else:
					dirids = L_T(['r', 'u', 'l', 'd'])
					dirid = dirids[(dir__2 + 1)]
					if (surrounds_5[dirid] is not None):
						for c_22, d_20 in L_ipairs(surrounds_5[dirid]):
							if (pnot_4 is False):
								if ((d_20 == pname_4) and (alreadyfound_4[bcode_5] is None)):
									alreadyfound_4[bcode_5] = 1
									allfound_4 = (allfound_4 + 1)
							else:
								if ((d_20 != pname_4) and (alreadyfound_4[bcode_5] is None)):
									alreadyfound_4[bcode_5] = 1
									allfound_4 = (allfound_4 + 1)
		else:
			return False
		return (allfound_4 == L_len(params_6))
	def _anon6(params_7=None, checkedconds_7=None, checkedconds__6=None, cdata_6=None, *_):  # L953
		allfound_5 = 0
		alreadyfound_5 = L_T()
		unitid_6, x_6, y_6, dir__3, extras_3, surrounds_6, conds_3 = cdata_6['unitid'], cdata_6['x'], cdata_6['y'], cdata_6['dir'], cdata_6['extras'], cdata_6['surrounds'], L_tostring(cdata_6['conds'])
		if ((unitid_6 == 2) and ((checkedconds__6 is None) or (checkedconds__6[conds_3] is None))):
			dir__3 = G['emptydir'](x_6, y_6, checkedconds_7)
		for i_4 in L_range(1, 4):
			ndrs_2 = G['ndirs'][i_4]
			ox_2 = ndrs_2[1]
			oy_2 = ndrs_2[2]
			tileid_7 = ((x_6 + ox_2) + ((y_6 + oy_2) * G['roomsizex']))
			if (L_len(params_7) > 0):
				for a_12, b_12 in L_ipairs(params_7):
					pname_5 = b_12
					pnot_5 = False
					if (L_sub(b_12, 1, 4) == 'not '):
						pnot_5 = True
						pname_5 = L_sub(b_12, 5)
					bcode_6 = L_concat(b_12, '_', L_tostring(a_12))
					if (L_sub(pname_5, 1, 5) == 'group'):
						return False
					if (((pname_5 != 'empty') and (b_12 != 'level')) or ((b_12 == 'level') and (alreadyfound_5[1] is not None))):
						if (G['unitmap'][tileid_7] is not None):
							for c_23, d_21 in L_ipairs(G['unitmap'][tileid_7]):
								if ((d_21 != unitid_6) and (alreadyfound_5[d_21] is None)):
									unit_7 = G['mmf']['newObject'](d_21)
									name__5 = G['getname'](unit_7)
									ndrs_ = G['ndirs'][(unit_7['values'][G['DIR']] + 1)]
									ox_ = ndrs_[1]
									oy_ = ndrs_[2]
									x__2 = (unit_7['values'][G['XPOS']] + ox_)
									y__2 = (unit_7['values'][G['YPOS']] + oy_)
									if (pnot_5 is False):
										if ((((name__5 == pname_5) and (x__2 == x_6)) and (y__2 == y_6)) and (alreadyfound_5[bcode_6] is None)):
											alreadyfound_5[bcode_6] = 1
											alreadyfound_5[d_21] = 1
											allfound_5 = (allfound_5 + 1)
									else:
										if (((((name__5 != pname_5) or (x__2 != x_6)) or (y__2 != y_6)) and (alreadyfound_5[bcode_6] is None)) and (name__5 != 'text')):
											alreadyfound_5[bcode_6] = 1
											alreadyfound_5[d_21] = 1
											allfound_5 = (allfound_5 + 1)
					elif (pname_5 == 'empty'):
						l_4 = G['map'][0]
						tile_4 = L_invoke(l_4, 'get_x', (x_6 + ox_2), (y_6 + oy_2))
						watching = False
						if (tile_4 == 255):
							dir__4 = G['emptydir']((x_6 + ox_2), (y_6 + oy_2), checkedconds_7)
							if (dir__4 != 4):
								ndrs__2 = (_t1 if L_t(_t1 := G['ndirs'][(dir__4 + 1)]) else L_T())
								ox__2 = (_t2 if L_t(_t2 := ndrs__2[1]) else 0)
								oy__2 = (_t3 if L_t(_t3 := ndrs__2[2]) else 0)
								x__3 = ((x_6 + ox_2) + ox__2)
								y__3 = ((y_6 + oy_2) + oy__2)
								if ((x__3 == x_6) and (y__3 == y_6)):
									watching = True
						if (pnot_5 is False):
							if (((G['unitmap'][tileid_7] is None) or (L_len(G['unitmap'][tileid_7]) == 0)) and (watching is not None and watching is not False)):
								if (alreadyfound_5[bcode_6] is None):
									alreadyfound_5[bcode_6] = 1
									allfound_5 = (allfound_5 + 1)
						else:
							if (((G['unitmap'][tileid_7] is not None) and (L_len(G['unitmap'][tileid_7]) > 0)) or (watching is False)):
								if (alreadyfound_5[bcode_6] is None):
									alreadyfound_5[bcode_6] = 1
									allfound_5 = (allfound_5 + 1)
					elif (((b_12 == 'level') and (alreadyfound_5[bcode_6] is None)) and (alreadyfound_5[1] is None)):
						alreadyfound_5[bcode_6] = 1
						alreadyfound_5[1] = 1
						allfound_5 = (allfound_5 + 1)
			else:
				return False
		return (allfound_5 == L_len(params_7))
	def _anon7(params_8=None, checkedconds_8=None, checkedconds__7=None, cdata_7=None, *_):  # L1063
		allfound_6 = 0
		alreadyfound_6 = L_T()
		targets = L_T()
		unitid_7, x_7, y_7, dir__5, conds_4, surrounds_7 = cdata_7['unitid'], cdata_7['x'], cdata_7['y'], cdata_7['dir'], L_tostring(cdata_7['conds']), cdata_7['surrounds']
		if (unitid_7 == 2):
			dir__5 = G['emptydir'](x_7, y_7)
		ndrs_3 = G['ndirs'][(dir__5 + 1)]
		ox_3 = ndrs_3[1]
		oy_3 = ndrs_3[2]
		nx, ny = x_7, y_7
		tileid_8 = ((x_7 + ox_3) + ((y_7 + oy_3) * G['roomsizex']))
		solid = 0
		if ((checkedconds__7 is not None) and (checkedconds__7[L_concat(L_tostring(conds_4), '_s_')] is not None)):
			return False
		if ((L_len(params_8) > 0) and (dir__5 != 4)):
			while ((solid == 0) and L_t(G['inbounds'](nx, ny, 1))):
				nx = (nx + ox_3)
				ny = (ny + oy_3)
				tileid_8 = (nx + (ny * G['roomsizex']))
				if L_t(G['inbounds'](nx, ny, 1)):
					if (G['unitmap'][tileid_8] is not None):
						if (L_len(G['unitmap'][tileid_8]) > 0):
							detected = False
							for a_13, b_13 in L_ipairs(G['unitmap'][tileid_8]):
								unit_8 = G['mmf']['newObject'](b_13)
								name__6 = G['getname'](unit_8)
								if (G['hasfeature'](name__6, 'is', 'hide', b_13, nx, ny, checkedconds_8) is None):
									L_insert(targets, L_T([b_13, name__6]))
									detected = True
							if (detected is False):
								L_insert(targets, L_T([2, 'empty']))
						else:
							L_insert(targets, L_T([2, 'empty']))
					else:
						L_insert(targets, L_T([2, 'empty']))
					solid = G['simplecheck'](nx, ny, True, checkedconds_8)
				else:
					solid = 1
			for a_14, b_14 in L_ipairs(params_8):
				pname_6 = b_14
				pnot_6 = False
				if (L_sub(b_14, 1, 4) == 'not '):
					pnot_6 = True
					pname_6 = L_sub(b_14, 5)
				bcode_7 = L_concat(b_14, '_', L_tostring(a_14))
				if (L_sub(pname_6, 1, 5) == 'group'):
					return False
				if (unitid_7 != 1):
					if (((pname_6 != 'empty') and (b_14 != 'level')) or ((b_14 == 'level') and (alreadyfound_6[1] is not None))):
						for c_24, d_ in L_ipairs(targets):
							d_22 = d_[1]
							if (((d_22 != unitid_7) and (alreadyfound_6[d_22] is None)) and (d_22 != 2)):
								name__7 = d_[2]
								if (pnot_6 is False):
									if ((name__7 == pname_6) and (alreadyfound_6[bcode_7] is None)):
										alreadyfound_6[bcode_7] = 1
										alreadyfound_6[d_22] = 1
										allfound_6 = (allfound_6 + 1)
								else:
									if (((name__7 != pname_6) and (alreadyfound_6[bcode_7] is None)) and (name__7 != 'text')):
										alreadyfound_6[bcode_7] = 1
										alreadyfound_6[d_22] = 1
										allfound_6 = (allfound_6 + 1)
					elif (pname_6 == 'empty'):
						for c_25, d__2 in L_ipairs(targets):
							d_23 = d__2[1]
							if (d_23 == 2):
								if (pnot_6 is False):
									if (alreadyfound_6[bcode_7] is None):
										alreadyfound_6[bcode_7] = 1
										alreadyfound_6[d_23] = 1
										allfound_6 = (allfound_6 + 1)
								else:
									if (alreadyfound_6[bcode_7] is None):
										alreadyfound_6[bcode_7] = 1
										alreadyfound_6[d_23] = 1
										allfound_6 = (allfound_6 + 1)
					elif (((b_14 == 'level') and (alreadyfound_6[bcode_7] is None)) and (alreadyfound_6[1] is None)):
						alreadyfound_6[bcode_7] = 1
						alreadyfound_6[1] = 1
						allfound_6 = (allfound_6 + 1)
				else:
					dirids_2 = L_T(['r', 'u', 'l', 'd'])
					dirid_2 = dirids_2[(dir__5 + 1)]
					if (surrounds_7[dirid_2] is not None):
						for c_26, d_24 in L_ipairs(surrounds_7[dirid_2]):
							if (pnot_6 is False):
								if ((d_24 == pname_6) and (alreadyfound_6[bcode_7] is None)):
									alreadyfound_6[bcode_7] = 1
									allfound_6 = (allfound_6 + 1)
							else:
								if ((d_24 != pname_6) and (alreadyfound_6[bcode_7] is None)):
									alreadyfound_6[bcode_7] = 1
									allfound_6 = (allfound_6 + 1)
		elif (L_len(params_8) == 0):
			L_noop('no parameters given!')
			return False
		else:
			return False
		return (allfound_6 == L_len(params_8))
	def _anon8(params_9=None, checkedconds_9=None, checkedconds__8=None, cdata_8=None, *_):  # L1216
		allfound_7 = 0
		alreadyfound_7 = L_T()
		unitcount = L_T()
		name_2, unitid_8, notcond_2 = cdata_8['name'], cdata_8['unitid'], cdata_8['notcond']
		if (L_len(params_9) > 0):
			for a_15, b_15 in L_ipairs(params_9):
				if (unitcount[b_15] is None):
					unitcount[b_15] = 0
				unitcount[b_15] = (unitcount[b_15] + 1)
			if ((unitcount['level'] is not None) and (unitcount['level'] > 0)):
				unitcount['level'] = (unitcount['level'] - 1)
			for a_16, b_16 in L_ipairs(params_9):
				pname_7 = b_16
				pnot_7 = False
				if (L_sub(b_16, 1, 4) == 'not '):
					pnot_7 = True
					pname_7 = L_sub(b_16, 5)
				bcode_8 = L_concat(b_16, '_', L_tostring(a_16))
				if (L_sub(pname_7, 1, 5) == 'group'):
					return False
				if (((b_16 != 'level') and (b_16 != 'empty')) or ((b_16 == 'level') and (unitcount['level'] > 0))):
					if (pnot_7 is False):
						if (alreadyfound_7[bcode_8] is None):
							if ((G['unitlists'][b_16] is None) or ((L_len(G['unitlists'][b_16]) == 0) and (alreadyfound_7[bcode_8] is None))):
								alreadyfound_7[bcode_8] = 1
								allfound_7 = (allfound_7 + 1)
							elif ((G['unitlists'][b_16] is not None) and (L_len(G['unitlists'][b_16]) > 0)):
								found = False
								if (b_16 != name_2):
									if (L_len(G['unitlists'][b_16]) < unitcount[b_16]):
										found = True
								else:
									if (L_len(G['unitlists'][b_16]) < (unitcount[b_16] + 1)):
										found = True
								if (found is not None and found is not False):
									alreadyfound_7[bcode_8] = 1
									allfound_7 = (allfound_7 + 1)
					else:
						foundunits = 0
						targetcount = unitcount[b_16]
						for c_27, d_25 in L_pairs(G['unitlists']):
							if ((((c_27 != pname_7) and (L_len(G['unitlists'][c_27]) > 0)) and (c_27 != 'text')) and (L_sub(c_27, 1, 5) != 'text_')):
								for e_6, f_6 in L_ipairs(d_25):
									if ((f_6 != unitid_8) and (alreadyfound_7[f_6] is None)):
										alreadyfound_7[f_6] = 1
										foundunits = (foundunits + 1)
										if (foundunits >= targetcount):
											break
							if (foundunits >= targetcount):
								break
						if ((foundunits < targetcount) and (alreadyfound_7[bcode_8] is None)):
							alreadyfound_7[bcode_8] = 1
							allfound_7 = (allfound_7 + 1)
				elif (b_16 == 'empty'):
					empties_4 = G['findempty']()
					if (name_2 != 'empty'):
						if ((L_len(empties_4) < unitcount[b_16]) and (alreadyfound_7[bcode_8] is None)):
							alreadyfound_7[bcode_8] = 1
							allfound_7 = (allfound_7 + 1)
					else:
						if ((L_len(empties_4) < (unitcount[b_16] + 1)) and (alreadyfound_7[bcode_8] is None)):
							alreadyfound_7[bcode_8] = 1
							allfound_7 = (allfound_7 + 1)
				elif (b_16 == 'level'):
					allfound_7 = (-99)
					break
		else:
			L_noop('no parameters given!')
			return False
		if (notcond_2 is not None and notcond_2 is not False):
			return (allfound_7 > 0)
		return (allfound_7 == L_len(params_9))
	def _anon9(params_10=None, checkedconds_10=None, checkedconds__9=None, cdata_9=None, *_):  # L1333
		allfound_8 = 0
		alreadyfound_8 = L_T()
		unitid_9, x_8, y_8, surrounds_8 = cdata_9['unitid'], cdata_9['x'], cdata_9['y'], cdata_9['surrounds']
		if (L_len(params_10) > 0):
			for a_17, b_17 in L_ipairs(params_10):
				pname_8 = b_17
				pnot_8 = False
				if (L_sub(b_17, 1, 4) == 'not '):
					pnot_8 = True
					pname_8 = L_sub(b_17, 5)
				bcode_9 = L_concat(b_17, '_', L_tostring(a_17))
				if (L_sub(pname_8, 1, 5) == 'group'):
					return False
				dist = ((G['roomsizey'] - y_8) - 2)
				if (unitid_9 != 1):
					if ((b_17 != 'level') or ((b_17 == 'level') and (alreadyfound_8[1] is not None))):
						if (dist >= 1):
							for g_3 in L_range(1, dist):
								if (pname_8 != 'empty'):
									tileid_9 = (x_8 + ((y_8 + g_3) * G['roomsizex']))
									if (G['unitmap'][tileid_9] is not None):
										for c_28, d_26 in L_ipairs(G['unitmap'][tileid_9]):
											if ((d_26 != unitid_9) and (alreadyfound_8[d_26] is None)):
												unit_9 = G['mmf']['newObject'](d_26)
												name__8 = G['getname'](unit_9)
												if (pnot_8 is False):
													if ((name__8 == pname_8) and (alreadyfound_8[bcode_9] is None)):
														alreadyfound_8[bcode_9] = 1
														alreadyfound_8[d_26] = 1
														allfound_8 = (allfound_8 + 1)
												else:
													if (((name__8 != pname_8) and (alreadyfound_8[bcode_9] is None)) and (name__8 != 'text')):
														alreadyfound_8[bcode_9] = 1
														alreadyfound_8[d_26] = 1
														allfound_8 = (allfound_8 + 1)
								else:
									nearempty_3 = False
									tileid_10 = (x_8 + ((y_8 + g_3) * G['roomsizex']))
									l_5 = G['map'][0]
									tile_5 = L_invoke(l_5, 'get_x', x_8, (y_8 + g_3))
									tcode_3 = L_concat(L_tostring(tileid_10), 'e')
									if ((((G['unitmap'][tileid_10] is None) or (L_len(G['unitmap'][tileid_10]) == 0)) and (tile_5 == 255)) and (alreadyfound_8[tcode_3] is None)):
										nearempty_3 = True
									if (pnot_8 is False):
										if ((nearempty_3 is not None and nearempty_3 is not False) and (alreadyfound_8[bcode_9] is None)):
											alreadyfound_8[bcode_9] = 1
											alreadyfound_8[tcode_3] = 1
											allfound_8 = (allfound_8 + 1)
									else:
										if ((nearempty_3 is False) and (alreadyfound_8[bcode_9] is None)):
											alreadyfound_8[bcode_9] = 1
											alreadyfound_8[tcode_3] = 1
											allfound_8 = (allfound_8 + 1)
					elif (((b_17 == 'level') and (alreadyfound_8[bcode_9] is None)) and (alreadyfound_8[1] is None)):
						alreadyfound_8[bcode_9] = 1
						alreadyfound_8[1] = 1
						allfound_8 = (allfound_8 + 1)
				else:
					ulist_4 = False
					if ((b_17 != 'empty') and (b_17 != 'level')):
						if (pnot_8 is False):
							if (((G['unitlists'][pname_8] is not None) and (L_len(G['unitlists'][pname_8]) > 0)) and (alreadyfound_8[bcode_9] is None)):
								for c_29, d_27 in L_ipairs(G['unitlists'][pname_8]):
									if (alreadyfound_8[d_27] is None):
										alreadyfound_8[bcode_9] = 1
										alreadyfound_8[d_27] = 1
										ulist_4 = True
										break
						else:
							for c_30, d_28 in L_pairs(G['unitlists']):
								tested_4 = False
								if (((c_30 != pname_8) and (L_len(d_28) > 0)) and (alreadyfound_8[bcode_9] is None)):
									for e_7, f_7 in L_ipairs(d_28):
										if (alreadyfound_8[f_7] is None):
											alreadyfound_8[bcode_9] = 1
											alreadyfound_8[f_7] = 1
											ulist_4 = True
											tested_4 = True
											break
								if (tested_4 is not None and tested_4 is not False):
									break
					elif (b_17 == 'empty'):
						empties_5 = G['findempty']()
						if ((L_len(empties_5) > 0) and (alreadyfound_8[bcode_9] is None)):
							for c_31, d_29 in L_ipairs(G['unitlists'][pname_8]):
								if (alreadyfound_8[d_29] is None):
									alreadyfound_8[bcode_9] = 1
									alreadyfound_8[d_29] = 1
									ulist_4 = True
									break
					if ((b_17 != 'text') and (ulist_4 is False)):
						if (surrounds_8['d'] is not None):
							for c_32, d_30 in L_ipairs(surrounds_8['d']):
								if (pnot_8 is False):
									if (((ulist_4 is False) and (d_30 == pname_8)) and (alreadyfound_8[bcode_9] is None)):
										alreadyfound_8[bcode_9] = 1
										ulist_4 = True
								else:
									if (((ulist_4 is False) and (d_30 != pname_8)) and (alreadyfound_8[bcode_9] is None)):
										alreadyfound_8[bcode_9] = 1
										ulist_4 = True
					if ((ulist_4 is not None and ulist_4 is not False) or (b_17 == 'text')):
						alreadyfound_8[bcode_9] = 1
						allfound_8 = (allfound_8 + 1)
		else:
			L_noop('no parameters given!')
			return False
		return (allfound_8 == L_len(params_10))
	def _anon10(params_11=None, checkedconds_11=None, checkedconds__10=None, cdata_10=None, *_):  # L1499
		allfound_9 = 0
		alreadyfound_9 = L_T()
		unitid_10, x_9, y_9, surrounds_9 = cdata_10['unitid'], cdata_10['x'], cdata_10['y'], cdata_10['surrounds']
		if (L_len(params_11) > 0):
			for a_18, b_18 in L_ipairs(params_11):
				pname_9 = b_18
				pnot_9 = False
				if (L_sub(b_18, 1, 4) == 'not '):
					pnot_9 = True
					pname_9 = L_sub(b_18, 5)
				bcode_10 = L_concat(b_18, '_', L_tostring(a_18))
				if (L_sub(pname_9, 1, 5) == 'group'):
					return False
				dist_2 = (y_9 - 1)
				if (unitid_10 != 1):
					if ((b_18 != 'level') or ((b_18 == 'level') and (alreadyfound_9[1] is not None))):
						if (y_9 > 1):
							for g_4 in L_range(1, dist_2):
								if (pname_9 != 'empty'):
									tileid_11 = (x_9 + ((y_9 - g_4) * G['roomsizex']))
									if (G['unitmap'][tileid_11] is not None):
										for c_33, d_31 in L_ipairs(G['unitmap'][tileid_11]):
											if ((d_31 != unitid_10) and (alreadyfound_9[d_31] is None)):
												unit_10 = G['mmf']['newObject'](d_31)
												name__9 = G['getname'](unit_10)
												if (pnot_9 is False):
													if ((name__9 == pname_9) and (alreadyfound_9[bcode_10] is None)):
														alreadyfound_9[bcode_10] = 1
														alreadyfound_9[d_31] = 1
														allfound_9 = (allfound_9 + 1)
												else:
													if (((name__9 != pname_9) and (alreadyfound_9[bcode_10] is None)) and (name__9 != 'text')):
														alreadyfound_9[bcode_10] = 1
														alreadyfound_9[d_31] = 1
														allfound_9 = (allfound_9 + 1)
								else:
									nearempty_4 = False
									tileid_12 = (x_9 + ((y_9 - g_4) * G['roomsizex']))
									l_6 = G['map'][0]
									tile_6 = L_invoke(l_6, 'get_x', x_9, (y_9 - g_4))
									tcode_4 = L_concat(L_tostring(tileid_12), 'e')
									if ((((G['unitmap'][tileid_12] is None) or (L_len(G['unitmap'][tileid_12]) == 0)) and (tile_6 == 255)) and (alreadyfound_9[tcode_4] is None)):
										nearempty_4 = True
									if (pnot_9 is False):
										if ((nearempty_4 is not None and nearempty_4 is not False) and (alreadyfound_9[bcode_10] is None)):
											alreadyfound_9[bcode_10] = 1
											alreadyfound_9[tcode_4] = 1
											allfound_9 = (allfound_9 + 1)
									else:
										if ((nearempty_4 is False) and (alreadyfound_9[bcode_10] is None)):
											alreadyfound_9[bcode_10] = 1
											alreadyfound_9[tcode_4] = 1
											allfound_9 = (allfound_9 + 1)
					elif (((b_18 == 'level') and (alreadyfound_9[bcode_10] is None)) and (alreadyfound_9[1] is None)):
						alreadyfound_9[bcode_10] = 1
						alreadyfound_9[1] = 1
						allfound_9 = (allfound_9 + 1)
				else:
					ulist_5 = False
					if ((b_18 != 'empty') and (b_18 != 'level')):
						if (pnot_9 is False):
							if (((G['unitlists'][pname_9] is not None) and (L_len(G['unitlists'][pname_9]) > 0)) and (alreadyfound_9[bcode_10] is None)):
								for c_34, d_32 in L_ipairs(G['unitlists'][pname_9]):
									if (alreadyfound_9[d_32] is None):
										alreadyfound_9[bcode_10] = 1
										alreadyfound_9[d_32] = 1
										ulist_5 = True
										break
						else:
							for c_35, d_33 in L_pairs(G['unitlists']):
								tested_5 = False
								if (((c_35 != pname_9) and (L_len(d_33) > 0)) and (alreadyfound_9[bcode_10] is None)):
									for e_8, f_8 in L_ipairs(d_33):
										if (alreadyfound_9[f_8] is None):
											alreadyfound_9[bcode_10] = 1
											alreadyfound_9[f_8] = 1
											ulist_5 = True
											tested_5 = True
											break
								if (tested_5 is not None and tested_5 is not False):
									break
					elif (b_18 == 'empty'):
						empties_6 = G['findempty']()
						if (L_len(empties_6) > 0):
							for c_36, d_34 in L_ipairs(empties_6):
								if ((alreadyfound_9[d_34] is None) and (alreadyfound_9[bcode_10] is None)):
									alreadyfound_9[bcode_10] = 1
									alreadyfound_9[d_34] = 1
									ulist_5 = True
									break
					if ((b_18 != 'text') and (ulist_5 is False)):
						if (surrounds_9['u'] is not None):
							for c_37, d_35 in L_ipairs(surrounds_9['u']):
								if (pnot_9 is False):
									if (((ulist_5 is False) and (d_35 == pname_9)) and (alreadyfound_9[bcode_10] is None)):
										alreadyfound_9[bcode_10] = 1
										ulist_5 = True
								else:
									if (((ulist_5 is False) and (d_35 != pname_9)) and (alreadyfound_9[bcode_10] is None)):
										alreadyfound_9[bcode_10] = 1
										ulist_5 = True
					if ((ulist_5 is not None and ulist_5 is not False) or (b_18 == 'text')):
						alreadyfound_9[bcode_10] = 1
						allfound_9 = (allfound_9 + 1)
		else:
			L_noop('no parameters given!')
			return False
		return (allfound_9 == L_len(params_11))
	def _anon11(params_12=None, checkedconds_12=None, checkedconds__11=None, cdata_11=None, *_):  # L1665
		allfound_10 = 0
		alreadyfound_10 = L_T()
		unitid_11, x_10, y_10, surrounds_10 = cdata_11['unitid'], cdata_11['x'], cdata_11['y'], cdata_11['surrounds']
		if (L_len(params_12) > 0):
			for a_19, b_19 in L_ipairs(params_12):
				pname_10 = b_19
				pnot_10 = False
				if (L_sub(b_19, 1, 4) == 'not '):
					pnot_10 = True
					pname_10 = L_sub(b_19, 5)
				bcode_11 = L_concat(b_19, '_', L_tostring(a_19))
				if (L_sub(pname_10, 1, 5) == 'group'):
					return False
				dist_3 = (x_10 - 1)
				if (unitid_11 != 1):
					if ((b_19 != 'level') or ((b_19 == 'level') and (alreadyfound_10[1] is not None))):
						if (x_10 > 1):
							for g_5 in L_range(1, dist_3):
								if (pname_10 != 'empty'):
									tileid_13 = ((x_10 - g_5) + (y_10 * G['roomsizex']))
									if (G['unitmap'][tileid_13] is not None):
										for c_38, d_36 in L_ipairs(G['unitmap'][tileid_13]):
											if ((d_36 != unitid_11) and (alreadyfound_10[d_36] is None)):
												unit_11 = G['mmf']['newObject'](d_36)
												name__10 = G['getname'](unit_11)
												if (pnot_10 is False):
													if ((name__10 == pname_10) and (alreadyfound_10[bcode_11] is None)):
														alreadyfound_10[bcode_11] = 1
														alreadyfound_10[d_36] = 1
														allfound_10 = (allfound_10 + 1)
												else:
													if (((name__10 != pname_10) and (alreadyfound_10[bcode_11] is None)) and (name__10 != 'text')):
														alreadyfound_10[bcode_11] = 1
														alreadyfound_10[d_36] = 1
														allfound_10 = (allfound_10 + 1)
								else:
									nearempty_5 = False
									tileid_14 = ((x_10 - g_5) + (y_10 * G['roomsizex']))
									l_7 = G['map'][0]
									tile_7 = L_invoke(l_7, 'get_x', (x_10 - g_5), y_10)
									tcode_5 = L_concat(L_tostring(tileid_14), 'e')
									if ((((G['unitmap'][tileid_14] is None) or (L_len(G['unitmap'][tileid_14]) == 0)) and (tile_7 == 255)) and (alreadyfound_10[tcode_5] is None)):
										nearempty_5 = True
									if (pnot_10 is False):
										if ((nearempty_5 is not None and nearempty_5 is not False) and (alreadyfound_10[bcode_11] is None)):
											alreadyfound_10[bcode_11] = 1
											alreadyfound_10[tcode_5] = 1
											allfound_10 = (allfound_10 + 1)
									else:
										if ((nearempty_5 is False) and (alreadyfound_10[bcode_11] is None)):
											alreadyfound_10[bcode_11] = 1
											alreadyfound_10[tcode_5] = 1
											allfound_10 = (allfound_10 + 1)
					elif (((b_19 == 'level') and (alreadyfound_10[bcode_11] is None)) and (alreadyfound_10[1] is None)):
						alreadyfound_10[bcode_11] = 1
						alreadyfound_10[1] = 1
						allfound_10 = (allfound_10 + 1)
				else:
					ulist_6 = False
					if ((b_19 != 'empty') and (b_19 != 'level')):
						if (pnot_10 is False):
							if (((G['unitlists'][pname_10] is not None) and (L_len(G['unitlists'][pname_10]) > 0)) and (alreadyfound_10[bcode_11] is None)):
								for c_39, d_37 in L_ipairs(G['unitlists'][pname_10]):
									if (alreadyfound_10[d_37] is None):
										alreadyfound_10[bcode_11] = 1
										alreadyfound_10[d_37] = 1
										ulist_6 = True
										break
						else:
							for c_40, d_38 in L_pairs(G['unitlists']):
								tested_6 = False
								if (((c_40 != pname_10) and (L_len(d_38) > 0)) and (alreadyfound_10[bcode_11] is None)):
									for e_9, f_9 in L_ipairs(d_38):
										if (alreadyfound_10[f_9] is None):
											alreadyfound_10[bcode_11] = 1
											alreadyfound_10[f_9] = 1
											ulist_6 = True
											tested_6 = True
											break
								if (tested_6 is not None and tested_6 is not False):
									break
					elif (b_19 == 'empty'):
						empties_7 = G['findempty']()
						if (L_len(empties_7) > 0):
							for c_41, d_39 in L_ipairs(empties_7):
								if ((alreadyfound_10[d_39] is None) and (alreadyfound_10[bcode_11] is None)):
									alreadyfound_10[bcode_11] = 1
									alreadyfound_10[d_39] = 1
									ulist_6 = True
									break
					if ((b_19 != 'text') and (ulist_6 is False)):
						if (surrounds_10['l'] is not None):
							for c_42, d_40 in L_ipairs(surrounds_10['l']):
								if (pnot_10 is False):
									if (((ulist_6 is False) and (d_40 == pname_10)) and (alreadyfound_10[bcode_11] is None)):
										alreadyfound_10[bcode_11] = 1
										ulist_6 = True
								else:
									if (((ulist_6 is False) and (d_40 != pname_10)) and (alreadyfound_10[bcode_11] is None)):
										alreadyfound_10[bcode_11] = 1
										ulist_6 = True
					if ((ulist_6 is not None and ulist_6 is not False) or (b_19 == 'text')):
						alreadyfound_10[bcode_11] = 1
						allfound_10 = (allfound_10 + 1)
		else:
			L_noop('no parameters given!')
			return False
		return (allfound_10 == L_len(params_12))
	def _anon12(params_13=None, checkedconds_13=None, checkedconds__12=None, cdata_12=None, *_):  # L1831
		allfound_11 = 0
		alreadyfound_11 = L_T()
		unitid_12, x_11, y_11, surrounds_11 = cdata_12['unitid'], cdata_12['x'], cdata_12['y'], cdata_12['surrounds']
		if (L_len(params_13) > 0):
			for a_20, b_20 in L_ipairs(params_13):
				pname_11 = b_20
				pnot_11 = False
				if (L_sub(b_20, 1, 4) == 'not '):
					pnot_11 = True
					pname_11 = L_sub(b_20, 5)
				bcode_12 = L_concat(b_20, '_', L_tostring(a_20))
				if (L_sub(pname_11, 1, 5) == 'group'):
					return False
				dist_4 = ((G['roomsizex'] - x_11) - 2)
				if (unitid_12 != 1):
					if ((b_20 != 'level') or ((b_20 == 'level') and (alreadyfound_11[1] is not None))):
						if (dist_4 >= 1):
							for g_6 in L_range(1, dist_4):
								if (pname_11 != 'empty'):
									tileid_15 = ((x_11 + g_6) + (y_11 * G['roomsizex']))
									if (G['unitmap'][tileid_15] is not None):
										for c_43, d_41 in L_ipairs(G['unitmap'][tileid_15]):
											if ((d_41 != unitid_12) and (alreadyfound_11[d_41] is None)):
												unit_12 = G['mmf']['newObject'](d_41)
												name__11 = G['getname'](unit_12)
												if (pnot_11 is False):
													if ((name__11 == pname_11) and (alreadyfound_11[bcode_12] is None)):
														alreadyfound_11[bcode_12] = 1
														alreadyfound_11[d_41] = 1
														allfound_11 = (allfound_11 + 1)
												else:
													if (((name__11 != pname_11) and (alreadyfound_11[bcode_12] is None)) and (name__11 != 'text')):
														alreadyfound_11[bcode_12] = 1
														alreadyfound_11[d_41] = 1
														allfound_11 = (allfound_11 + 1)
								else:
									nearempty_6 = False
									tileid_16 = ((x_11 + g_6) + (y_11 * G['roomsizex']))
									l_8 = G['map'][0]
									tile_8 = L_invoke(l_8, 'get_x', (x_11 + g_6), y_11)
									tcode_6 = L_concat(L_tostring(tileid_16), 'e')
									if (((G['unitmap'][tileid_16] is None) or (L_len(G['unitmap'][tileid_16]) == 0)) and (alreadyfound_11[tcode_6] is None)):
										nearempty_6 = True
									if (pnot_11 is False):
										if ((nearempty_6 is not None and nearempty_6 is not False) and (alreadyfound_11[bcode_12] is None)):
											alreadyfound_11[bcode_12] = 1
											alreadyfound_11[tcode_6] = 1
											allfound_11 = (allfound_11 + 1)
									else:
										if ((nearempty_6 is False) and (alreadyfound_11[bcode_12] is None)):
											alreadyfound_11[bcode_12] = 1
											alreadyfound_11[tcode_6] = 1
											allfound_11 = (allfound_11 + 1)
					elif (((b_20 == 'level') and (alreadyfound_11[bcode_12] is None)) and (alreadyfound_11[1] is None)):
						alreadyfound_11[bcode_12] = 1
						alreadyfound_11[1] = 1
						allfound_11 = (allfound_11 + 1)
				else:
					ulist_7 = False
					if ((b_20 != 'empty') and (b_20 != 'level')):
						if (pnot_11 is False):
							if (((G['unitlists'][pname_11] is not None) and (L_len(G['unitlists'][pname_11]) > 0)) and (alreadyfound_11[bcode_12] is None)):
								for c_44, d_42 in L_ipairs(G['unitlists'][pname_11]):
									if (alreadyfound_11[d_42] is None):
										alreadyfound_11[bcode_12] = 1
										alreadyfound_11[d_42] = 1
										ulist_7 = True
										break
						else:
							for c_45, d_43 in L_pairs(G['unitlists']):
								tested_7 = False
								if (((c_45 != pname_11) and (L_len(d_43) > 0)) and (alreadyfound_11[bcode_12] is None)):
									for e_10, f_10 in L_ipairs(d_43):
										if (alreadyfound_11[f_10] is None):
											alreadyfound_11[bcode_12] = 1
											alreadyfound_11[f_10] = 1
											ulist_7 = True
											tested_7 = True
											break
								if (tested_7 is not None and tested_7 is not False):
									break
					elif (b_20 == 'empty'):
						empties_8 = G['findempty']()
						if ((L_len(empties_8) > 0) and (alreadyfound_11[bcode_12] is None)):
							for c_46, d_44 in L_ipairs(G['unitlists'][pname_11]):
								if (alreadyfound_11[d_44] is None):
									alreadyfound_11[bcode_12] = 1
									alreadyfound_11[d_44] = 1
									ulist_7 = True
									break
					if ((b_20 != 'text') and (ulist_7 is False)):
						if (surrounds_11['r'] is not None):
							for c_47, d_45 in L_ipairs(surrounds_11['r']):
								if (pnot_11 is False):
									if (((ulist_7 is False) and (d_45 == pname_11)) and (alreadyfound_11[bcode_12] is None)):
										alreadyfound_11[bcode_12] = 1
										ulist_7 = True
								else:
									if (((ulist_7 is False) and (d_45 != pname_11)) and (alreadyfound_11[bcode_12] is None)):
										alreadyfound_11[bcode_12] = 1
										ulist_7 = True
					if ((ulist_7 is not None and ulist_7 is not False) or (b_20 == 'text')):
						alreadyfound_11[bcode_12] = 1
						allfound_11 = (allfound_11 + 1)
		else:
			L_noop('no parameters given!')
			return False
		return (allfound_11 == L_len(params_13))
	def _anon13(params_14=None, checkedconds_14=None, checkedconds__13=None, cdata_13=None, *_):  # L1997
		allfound_12 = 0
		alreadyfound_12 = L_T()
		name_3, unitid_13, x_12, y_12, limit_2 = cdata_13['name'], cdata_13['unitid'], cdata_13['x'], cdata_13['y'], cdata_13['limit']
		if (L_len(params_14) > 0):
			for a_21, b_21 in L_ipairs(params_14):
				pname_12 = b_21
				pnot_12 = False
				if (L_sub(b_21, 1, 4) == 'not '):
					pnot_12 = True
					pname_12 = L_sub(b_21, 5)
				bcode_13 = L_concat(b_21, '_', L_tostring(a_21))
				if (G['featureindex'][name_3] is not None):
					for c_48, d_46 in L_ipairs(G['featureindex'][name_3]):
						drule = d_46[1]
						dconds = d_46[2]
						if (checkedconds_14[L_tostring(dconds)] is None):
							if (pnot_12 is False):
								if (((drule[1] == name_3) and (drule[2] == 'is')) and (drule[3] == b_21)):
									checkedconds_14[L_tostring(dconds)] = 1
									if ((alreadyfound_12[bcode_13] is None) and L_t(G['testcond'](dconds, unitid_13, x_12, y_12, None, limit_2, checkedconds_14))):
										alreadyfound_12[bcode_13] = 1
										allfound_12 = (allfound_12 + 1)
										break
							else:
								if (L_sub(drule[3], 1, 4) != 'not '):
									obj = G['unitreference'][L_concat('text_', drule[3])]
									if (obj is not None):
										objtype = L_first(G['getactualdata_objlist'](obj, 'type'))
										if (objtype == 2):
											if (((drule[1] == name_3) and (drule[2] == 'is')) and (drule[3] != pname_12)):
												checkedconds_14[L_tostring(dconds)] = 1
												if ((alreadyfound_12[bcode_13] is None) and L_t(G['testcond'](dconds, unitid_13, x_12, y_12, None, limit_2, checkedconds_14))):
													alreadyfound_12[bcode_13] = 1
													allfound_12 = (allfound_12 + 1)
													break
		else:
			return False
		return (allfound_12 == L_len(params_14))
	def _anon14(params_15=None, checkedconds_15=None, checkedconds__14=None, cdata_14=None, *_):  # L2062
		failure = False
		unitid_14, x_13, y_13 = cdata_14['unitid'], cdata_14['x'], cdata_14['y']
		if (unitid_14 != 1):
			tileid_17 = (x_13 + (y_13 * G['roomsizex']))
			if (G['unitmap'][tileid_17] is not None):
				for c_49, d_47 in L_ipairs(G['unitmap'][tileid_17]):
					if (d_47 != unitid_14):
						failure = True
						break
		else:
			failure = True
		return (failure is False)
	def _anon15(params_16=None, checkedconds_16=None, checkedconds__15=None, cdata_15=None, *_):  # L2082
		found_2 = False
		x_14, y_14, limit_3, subtype, conds_5 = cdata_15['x'], cdata_15['y'], cdata_15['limit'], cdata_15['subtype'], L_tostring(cdata_15['conds'])
		fullname = L_concat('power', subtype)
		if (G['poweredstatus'][fullname] is not None):
			found_2 = G['poweredstatus'][fullname]
		elif (G['featureindex'][fullname] is not None):
			for c_50, d_48 in L_ipairs(G['featureindex'][fullname]):
				drule_2 = d_48[1]
				dconds_2 = d_48[2]
				if (checkedconds_16[L_tostring(dconds_2)] is None):
					if (((L_sub(drule_2[1], 1, 4) != 'not ') and (drule_2[2] == 'is')) and (drule_2[3] == fullname)):
						if ((drule_2[1] != 'empty') and (drule_2[1] != 'level')):
							if (G['unitlists'][drule_2[1]] is not None):
								checkedconds_16[L_tostring(dconds_2)] = 1
								for e_11, f_11 in L_ipairs(G['unitlists'][drule_2[1]]):
									if L_t(G['testcond'](dconds_2, f_11, x_14, y_14, None, limit_3, checkedconds_16)):
										found_2 = True
										break
						elif (drule_2[1] == 'empty'):
							empties_9 = G['findempty'](dconds_2, True)
							if (L_len(empties_9) > 0):
								found_2 = True
						elif ((drule_2[1] == 'level') and L_t(G['testcond'](dconds_2, 1, x_14, y_14, None, limit_3, checkedconds_16))):
							found_2 = True
				if (found_2 is not None and found_2 is not False):
					break
		checkedconds_16 = (_t1 if L_t(_t1 := checkedconds__15) else L_T([], {L_tostring(conds_5): 1}))
		if ((checkedconds__15 is None) and (G['poweredstatus'][fullname] is None)):
			G['poweredstatus'][fullname] = found_2
		return found_2
	def _anon16(params_17=None, checkedconds_17=None, *_):  # L2137
		return (G['last_key'] == 4)
	def _anon17(params_18=None, checkedconds_18=None, checkedconds__16=None, cdata_16=None, *_):  # L2140
		unitid_15, x_15, y_15, conds_6, i_5 = cdata_16['unitid'], cdata_16['x'], cdata_16['y'], L_tostring(cdata_16['conds']), cdata_16['i']
		if (G['condstatus'][L_tostring(conds_6)] is None):
			G['condstatus'][L_tostring(conds_6)] = L_T()
		rnd = G['fixedrandom'](1, 4)
		d_49 = G['condstatus'][L_tostring(conds_6)]
		id_ = L_concat('often', '_', L_tostring(i_5))
		if (unitid_15 != 2):
			id_ = L_concat(id_, '_', L_tostring(unitid_15))
		else:
			id_ = L_concat(id_, '_', L_tostring(unitid_15), L_tostring(x_15), L_tostring(y_15))
		if (d_49[id_] is not None):
			rnd = d_49[id_]
		else:
			d_49[id_] = rnd
		return (rnd > 1)
	def _anon18(params_19=None, checkedconds_19=None, checkedconds__17=None, cdata_17=None, *_):  # L2166
		unitid_16, x_16, y_16, conds_7, i_6 = cdata_17['unitid'], cdata_17['x'], cdata_17['y'], L_tostring(cdata_17['conds']), cdata_17['i']
		if (G['condstatus'][L_tostring(conds_7)] is None):
			G['condstatus'][L_tostring(conds_7)] = L_T()
		rnd_2 = G['fixedrandom'](1, 6)
		d_50 = G['condstatus'][L_tostring(conds_7)]
		id__2 = L_concat('seldom', '_', L_tostring(i_6))
		if (unitid_16 != 2):
			id__2 = L_concat(id__2, '_', L_tostring(unitid_16))
		else:
			id__2 = L_concat(id__2, '_', L_tostring(unitid_16), L_tostring(x_16), L_tostring(y_16))
		if (d_50[id__2] is not None):
			rnd_2 = d_50[id__2]
		else:
			d_50[id__2] = rnd_2
		return (rnd_2 == 1)
	G['condlist'] = L_T([], {'never': _anon1, 'on': _anon2, 'near': _anon3, 'nextto': _anon4, 'facing': _anon5, 'facedby': _anon6, 'seeing': _anon7, 'without': _anon8, 'above': _anon9, 'below': _anon10, 'besideright': _anon11, 'besideleft': _anon12, 'feeling': _anon13, 'lonely': _anon14, 'powered': _anon15, 'idle': _anon16, 'often': _anon17, 'seldom': _anon18})
