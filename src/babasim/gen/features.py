"""Generated from features.lua by tools/lua2py.py. Do not edit."""
from babasim.luart import *  # noqa: F403


def load(G):
	def f_findfeature(rule1=None, rule2=None, rule3=None, *_):  # L1
		options = L_T()
		result = L_T()
		rule = ''
		if (rule1 is not None):
			rule = L_concat(rule1, ' ')
		if (rule2 is not None):
			rule = L_concat(rule, rule2, ' ')
		if (rule3 is not None):
			rule = L_concat(rule, rule3)
		if (G['featureindex'][rule1] is not None):
			for i, rules in L_ipairs(G['featureindex'][rule1]):
				rule_2 = rules[1]
				conds = rules[2]
				if (conds[1] != 'never'):
					if ((rule_2[1] == rule1) and (rule_2[2] == rule2)):
						baserule = L_T([rule_2[1], rule_2[2], rule_2[3]])
						L_insert(options, L_T([baserule, conds]))
		if ((G['featureindex'][rule3] is not None) and (G['featureindex'][rule1] is None)):
			for i_2, rules_2 in L_ipairs(G['featureindex'][rule3]):
				rule_3 = rules_2[1]
				conds_2 = rules_2[2]
				if (conds_2[1] != 'never'):
					if ((rule_3[3] == rule3) and (rule_3[2] == rule2)):
						baserule_2 = L_T([rule_3[1], rule_3[2], rule_3[3]])
						L_insert(options, L_T([baserule_2, conds_2]))
		if (((rule1 is None) and (rule3 is None)) and (rule2 is not None)):
			if (G['featureindex'][rule2] is not None):
				for i_3, rules_3 in L_ipairs(G['featureindex'][rule2]):
					usable = False
					rule_4 = rules_3[1]
					conds_3 = rules_3[2]
					if (conds_3[1] != 'never'):
						for a, mat in L_pairs(G['objectlist']):
							if (a == rule_4[3]):
								usable = True
						for a_2, mat_2 in L_ipairs(G['customobjects']):
							if (mat_2 == rule_4[3]):
								usable = True
						if ((rule_4[2] == rule2) and (usable is not None and usable is not False)):
							baserule_3 = L_T([rule_4[1], rule_4[2], rule_4[3]])
							L_insert(options, L_T([baserule_3, conds_3]))
		for i_4, rules_4 in L_ipairs(options):
			words = L_T()
			baserule_4 = rules_4[1]
			for a_3, b in L_ipairs(baserule_4):
				L_insert(words, b)
			if (L_len(words) >= 3):
				one = words[3]
				two = L_concat(words[2], ' ', words[3])
				three = L_concat(words[1], ' ', words[2], ' ', words[3])
				if ((((one == rule) or (two == rule)) or (three == rule)) or (((rule2 == words[2]) and (rule1 is None)) and (rule3 is None))):
					L_insert(result, L_T([baserule_4[1], rules_4[2]]))
		if (L_len(result) > 0):
			return result
		else:
			return None
	G['findfeature'] = f_findfeature
	def f_findfeatureat(rule1_2=None, rule2_2=None, rule3_2=None, x=None, y=None, blockers_=None, checkedconds=None, *_):  # L101
		result_2 = L_T()
		blockers = (_t1 if L_t(_t1 := blockers_) else L_T())
		targets = G['findfeature'](rule1_2, rule2_2, rule3_2)
		if (targets is not None):
			tileid = (x + (y * G['roomsizex']))
			if ((G['unitmap'][tileid] is not None) and (L_len(G['unitmap'][tileid]) > 0)):
				for a_4, unitid in L_ipairs(G['unitmap'][tileid]):
					unit = G['mmf']['newObject'](unitid)
					name = G['getname'](unit)
					for i_5, v in L_ipairs(targets):
						if (name == v[1]):
							valid = True
							for c, d in L_ipairs(blockers):
								testing = G['hasfeature'](name, 'is', d, unitid, x, y, checkedconds)
								if (testing is not None):
									valid = False
									break
							if (valid is not None and valid is not False):
								conds_4 = v[2]
								if L_t(G['testcond'](conds_4, unit['fixed'], None, None, None, None, checkedconds)):
									L_insert(result_2, unit['fixed'])
		if (L_len(result_2) > 0):
			return result_2
		else:
			return None
	G['findfeatureat'] = f_findfeatureat
	def f_hasfeature(rule1_3=None, rule2_3=None, rule3_3=None, unitid_2=None, x_2=None, y_2=None, checkedconds_2=None, ignorebroken_=None, *_):  # L146
		ignorebroken = False
		if (ignorebroken_ is not None):
			ignorebroken = ignorebroken_
		if (((rule1_3 is not None) and (rule2_3 is not None)) and (rule3_3 is not None)):
			if (G['featureindex'][rule1_3] is not None):
				for i_6, rules_5 in L_ipairs(G['featureindex'][rule1_3]):
					rule_5 = rules_5[1]
					conds_5 = rules_5[2]
					if (conds_5[1] != 'never'):
						if (((rule_5[1] == rule1_3) and (rule_5[2] == rule2_3)) and (rule_5[3] == rule3_3)):
							if L_t(G['testcond'](conds_5, unitid_2, x_2, y_2, None, None, checkedconds_2, ignorebroken)):
								return True
			if ((L_sub(rule1_3, 1, 5) == 'text_') and (G['featureindex']['text'] is not None)):
				for i_7, rules_6 in L_ipairs(G['featureindex']['text']):
					rule_6 = rules_6[1]
					conds_6 = rules_6[2]
					if (conds_6[1] != 'never'):
						if (((rule_6[1] == 'text') and (rule_6[2] == rule2_3)) and (rule_6[3] == rule3_3)):
							if L_t(G['testcond'](conds_6, unitid_2, x_2, y_2, None, None, checkedconds_2, ignorebroken)):
								return True
		if (((rule3_3 is not None) and (rule2_3 is not None)) and (rule1_3 is not None)):
			if (G['featureindex'][rule3_3] is not None):
				for i_8, rules_7 in L_ipairs(G['featureindex'][rule3_3]):
					rule_7 = rules_7[1]
					conds_7 = rules_7[2]
					if (conds_7[1] != 'never'):
						if (((rule_7[1] == rule1_3) and (rule_7[2] == rule2_3)) and (rule_7[3] == rule3_3)):
							if L_t(G['testcond'](conds_7, unitid_2, x_2, y_2, None, None, checkedconds_2, ignorebroken)):
								return True
			if ((L_sub(rule3_3, 1, 5) == 'text_') and (G['featureindex']['text'] is not None)):
				for i_9, rules_8 in L_ipairs(G['featureindex']['text']):
					rule_8 = rules_8[1]
					conds_8 = rules_8[2]
					if (conds_8[1] != 'never'):
						if (((rule_8[1] == rule1_3) and (rule_8[2] == rule2_3)) and (rule_8[3] == 'text')):
							if L_t(G['testcond'](conds_8, unitid_2, x_2, y_2, None, None, checkedconds_2, ignorebroken)):
								return True
		if (((G['featureindex'][rule2_3] is not None) and (rule1_3 is not None)) and (rule3_3 is None)):
			usable_2 = False
			if (G['featureindex'][rule1_3] is not None):
				for i_10, rules_9 in L_ipairs(G['featureindex'][rule1_3]):
					rule_9 = rules_9[1]
					conds_9 = rules_9[2]
					if (conds_9[1] != 'never'):
						for a_5, mat_3 in L_pairs(G['objectlist']):
							if (a_5 == rule_9[1]):
								usable_2 = True
								break
						if (((rule_9[1] == rule1_3) and (rule_9[2] == rule2_3)) and (usable_2 is not None and usable_2 is not False)):
							if L_t(G['testcond'](conds_9, unitid_2, x_2, y_2, None, None, checkedconds_2, ignorebroken)):
								return True
		return None
	G['hasfeature'] = f_hasfeature
	def f_findallfeature(rule1_4=None, rule2_4=None, rule3_4=None, ignore_empty_=None, checkedconds_3=None, *_):  # L245
		group = G['findfeature'](rule1_4, rule2_4, rule3_4)
		ignore_empty = (_t1 if L_t(_t1 := ignore_empty_) else False)
		result_3 = L_T()
		empty = L_T()
		if (group is not None):
			for i_11, v_2 in L_ipairs(group):
				if (v_2[1] != 'empty'):
					fgroupmembers = G['findall'](v_2)
					for a_6, b_2 in L_ipairs(fgroupmembers):
						L_insert(result_3, b_2)
						L_insert(empty, L_T())
				else:
					if (ignore_empty is False):
						conds_10 = v_2[2]
						needstest = False
						testbroken = False
						valid_2 = True
						if ((L_len(conds_10) > 0) and ((conds_10[1] is not None) and (conds_10[1][1] != 'never'))):
							needstest = True
						elif ((L_len(conds_10) > 0) and ((conds_10[1] is not None) and (conds_10[1][1] == 'never'))):
							valid_2 = False
						if (G['featureindex']['broken'] is not None):
							testbroken = True
						if (valid_2 is not None and valid_2 is not False):
							L_insert(result_3, 2)
							L_insert(empty, L_T())
							thisempty = empty[L_len(empty)]
							for a_7 in L_range(1, (G['roomsizex'] - 2)):
								for b_3 in L_range(1, (G['roomsizey'] - 2)):
									tileid_2 = (a_7 + (b_3 * G['roomsizex']))
									if ((G['unitmap'][tileid_2] is None) or (L_len(G['unitmap'][tileid_2]) == 0)):
										valid_2 = True
										if (testbroken is not None and testbroken is not False):
											brok = G['isitbroken']('empty', 2, a_7, b_3)
											if (brok == 1):
												valid_2 = False
										if (valid_2 is not None and valid_2 is not False):
											if (needstest is False):
												thisempty[tileid_2] = 0
											else:
												if L_t(G['testcond'](conds_10, 2, a_7, b_3, None, None, checkedconds_3)):
													thisempty[tileid_2] = 0
		return (result_3, empty,)
		return ()
	G['findallfeature'] = f_findallfeature
	def f_getunitswitheffect(rule3_5=None, nolevels_=None, ignorethese_=None, checkedconds_4=None, ignorebroken__2=None, *_):  # L319
		group_2 = L_T()
		result_4 = L_T()
		ignorethese = (_t1 if L_t(_t1 := ignorethese_) else L_T())
		ignorebroken_2 = (_t2 if L_t(_t2 := ignorebroken__2) else False)
		nolevels = (_t3 if L_t(_t3 := nolevels_) else False)
		if (G['featureindex'][rule3_5] is not None):
			for i_12, v_3 in L_ipairs(G['featureindex'][rule3_5]):
				rule_10 = v_3[1]
				conds_11 = v_3[2]
				if (((rule_10[2] == 'is') and (conds_11[1] != 'never')) and (G['findnoun'](rule_10[1], G['nlist']['brief']) is False)):
					L_insert(group_2, L_T([rule_10[1], conds_11]))
			for i_13, v_4 in L_ipairs(group_2):
				if (v_4[1] != 'empty'):
					name_2 = v_4[1]
					fgroupmembers_2 = G['unitlists'][name_2]
					valid_3 = True
					if ((name_2 == 'level') and (nolevels is not None and nolevels is not False)):
						valid_3 = False
					if ((fgroupmembers_2 is not None) and (valid_3 is not None and valid_3 is not False)):
						for a_8, b_4 in L_ipairs(fgroupmembers_2):
							if L_t(G['testcond'](v_4[2], b_4, None, None, None, None, checkedconds_4, ignorebroken_2)):
								unit_2 = G['mmf']['newObject'](b_4)
								if (unit_2['flags'][G['DEAD']] is False):
									valid_3 = True
									for c_2, d_2 in L_ipairs(ignorethese):
										if (d_2 == b_4):
											valid_3 = False
											break
									if (valid_3 is not None and valid_3 is not False):
										L_insert(result_4, unit_2)
				else:
					pass
		return result_4
	G['getunitswitheffect'] = f_getunitswitheffect
	def f_getunitswithverb(rule2_5=None, ignorethese__2=None, checkedconds_5=None, *_):  # L379
		group_3 = L_T()
		result_5 = L_T()
		ignorethese_2 = (_t1 if L_t(_t1 := ignorethese__2) else L_T())
		if (G['featureindex'][rule2_5] is not None):
			for i_14, v_5 in L_ipairs(G['featureindex'][rule2_5]):
				rule_11 = v_5[1]
				conds_12 = v_5[2]
				name_3 = rule_11[1]
				if ((((rule_11[2] == rule2_5) and (conds_12[1] != 'never')) and (G['findnoun'](rule_11[1], G['nlist']['brief']) is False)) and (L_sub(rule_11[3], 1, 4) != 'not ')):
					if (group_3[name_3] is None):
						group_3[name_3] = L_T()
					L_insert(group_3[name_3], L_T([rule_11[3], conds_12]))
			for i_15, v_6 in L_pairs(group_3):
				if (L_sub(i_15, 1, 4) != 'not '):
					if (i_15 != 'empty'):
						name_4 = i_15
						fgroupmembers_3 = G['unitlists'][name_4]
						if ((fgroupmembers_3 is not None) and (L_len(fgroupmembers_3) > 0)):
							for c_3, d_3 in L_ipairs(v_6):
								L_insert(result_5, L_T([d_3[1], L_T(), name_4]))
								thisthisresult = result_5[L_len(result_5)][2]
								for a_9, b_5 in L_ipairs(fgroupmembers_3):
									if L_t(G['testcond'](d_3[2], b_5, None, None, None, None, checkedconds_5)):
										unit_3 = G['mmf']['newObject'](b_5)
										if (unit_3['flags'][G['DEAD']] is False):
											valid_4 = True
											for e, f in L_ipairs(ignorethese_2):
												if (f == b_5):
													valid_4 = False
													break
											if (valid_4 is not None and valid_4 is not False):
												L_insert(result_5[L_len(result_5)][2], unit_3)
					else:
						name_5 = i_15
						empties = G['findempty']()
						if (L_len(empties) > 0):
							for c_4, d_4 in L_ipairs(v_6):
								L_insert(result_5, L_T([d_4[1], L_T(), name_5]))
								for e_2, f_2 in L_ipairs(empties):
									x_3 = L_floor((f_2 % G['roomsizex']))
									y_3 = L_floor(L_div(f_2, G['roomsizex']))
									if L_t(G['testcond'](d_4[2], 2, x_3, y_3, None, None, checkedconds_5)):
										valid_5 = True
										for g, h in L_ipairs(ignorethese_2):
											if (f_2 == h):
												valid_5 = False
												break
										if (valid_5 is not None and valid_5 is not False):
											L_insert(result_5[L_len(result_5)][2], f_2)
		return result_5
	G['getunitswithverb'] = f_getunitswithverb
	def f_getunitverbtargets(rule2_6=None, checkedconds_6=None, *_):  # L468
		group_4 = L_T()
		result_6 = L_T()
		if (G['featureindex'][rule2_6] is not None):
			for i_16, v_7 in L_ipairs(G['featureindex'][rule2_6]):
				rule_12 = v_7[1]
				conds_13 = v_7[2]
				name_6 = rule_12[1]
				isnot = L_sub(rule_12[3], 1, 4)
				if ((((rule_12[2] == rule2_6) and (conds_13[1] != 'never')) and (G['findnoun'](rule_12[1], G['nlist']['brief']) is False)) and (isnot != 'not ')):
					if (group_4[name_6] is None):
						group_4[name_6] = L_T()
					L_insert(group_4[name_6], L_T([rule_12[3], conds_13]))
			for name_7, v_8 in L_pairs(group_4):
				if (L_sub(name_7, 1, 4) != 'not '):
					if (name_7 != 'empty'):
						fgroupmembers_4 = (_t1 if L_t(_t1 := G['unitlists'][name_7]) else L_T())
						finalgroup = L_T()
						for a_10, b_6 in L_ipairs(fgroupmembers_4):
							myverbs = L_T()
							for c_5, d_5 in L_ipairs(v_8):
								if L_t(G['testcond'](d_5[2], b_6, None, None, None, None, checkedconds_6)):
									unit_4 = G['mmf']['newObject'](b_6)
									if (unit_4['flags'][G['DEAD']] is False):
										L_insert(myverbs, d_5[1])
							L_insert(finalgroup, L_T([b_6, myverbs]))
						L_insert(result_6, L_T([name_7, finalgroup]))
					else:
						empties_2 = G['findempty']()
						finalgroup_2 = L_T()
						if (L_len(empties_2) > 0):
							for a_11, b_7 in L_ipairs(empties_2):
								x_4 = L_floor((b_7 % G['roomsizex']))
								y_4 = L_floor(L_div(b_7, G['roomsizex']))
								myverbs_2 = L_T()
								for c_6, d_6 in L_ipairs(v_8):
									if L_t(G['testcond'](d_6[2], 2, x_4, y_4, None, None, checkedconds_6)):
										L_insert(myverbs_2, d_6[1])
								L_insert(finalgroup_2, L_T([b_7, myverbs_2]))
							L_insert(result_6, L_T([name_7, finalgroup_2]))
		return result_6
	G['getunitverbtargets'] = f_getunitverbtargets
	def f_hasfeature_count(rule1_5=None, rule2_7=None, rule3_6=None, unitid_3=None, x_5=None, y_5=None, checkedconds_7=None, *_):  # L542
		result_7 = 0
		if (((G['featureindex'][rule1_5] is not None) and (G['featureindex'][rule3_6] is not None)) and (rule2_7 is not None)):
			if (L_len(G['featureindex'][rule1_5]) < L_len(G['featureindex'][rule3_6])):
				for i_17, v_9 in L_ipairs(G['featureindex'][rule1_5]):
					rule_13 = v_9[1]
					conds_14 = v_9[2]
					if (((rule_13[1] == rule1_5) and (rule_13[2] == rule2_7)) and (rule_13[3] == rule3_6)):
						if L_t(G['testcond'](conds_14, unitid_3, x_5, y_5, None, None, checkedconds_7)):
							result_7 = (result_7 + 1)
			else:
				for i_18, v_10 in L_ipairs(G['featureindex'][rule3_6]):
					rule_14 = v_10[1]
					conds_15 = v_10[2]
					if (((rule_14[1] == rule1_5) and (rule_14[2] == rule2_7)) and (rule_14[3] == rule3_6)):
						if L_t(G['testcond'](conds_15, unitid_3, x_5, y_5, None, None, checkedconds_7)):
							result_7 = (result_7 + 1)
		return result_7
	G['hasfeature_count'] = f_hasfeature_count
