"""Generated from rules.lua by tools/lua2py.py. Do not edit."""
from babasim.luart import *  # noqa: F403


def load(G):
	def f_code(alreadyrun_=None, *_):  # L1
		playrulesound = False
		alreadyrun = (_t1 if L_t(_t1 := alreadyrun_) else False)
		G['poweredstatus'] = L_T()
		if (G['updatecode'] == 1):
			G['HACK_INFINITY'] = (G['HACK_INFINITY'] + 1)
			if L_t(G['generaldata']['flags'][G['LOGGING']]):
				G['logrulelist']['new'] = L_T()
			G['MF_removeblockeffect'](0)
			G['wordrelatedunits'] = L_T()
			G['do_mod_hook']('rule_update', L_T([alreadyrun]))
			if (G['HACK_INFINITY'] < 200):
				checkthese = L_T()
				wordidentifier = ''
				G['wordunits'], wordidentifier, G['wordrelatedunits'] = L_adjust((*G['findwordunits'](),), 3)
				wordunitresult = L_T()
				if (L_len(G['wordunits']) > 0):
					for i, v in L_ipairs(G['wordunits']):
						if L_t(G['testcond'](v[2], v[1])):
							wordunitresult[v[1]] = 1
							L_insert(checkthese, v[1])
						else:
							wordunitresult[v[1]] = 0
				G['features'] = L_T()
				G['featureindex'] = L_T()
				G['condfeatureindex'] = L_T()
				G['visualfeatures'] = L_T()
				G['notfeatures'] = L_T()
				G['groupfeatures'] = L_T()
				firstwords = L_T()
				alreadyused = L_T()
				G['do_mod_hook']('rule_baserules')
				for i_2, v_2 in L_ipairs(G['baserulelist']):
					G['addbaserule'](v_2[1], v_2[2], v_2[3], v_2[4])
				G['formlettermap']()
				if (L_len(G['codeunits']) > 0):
					for i_3, v_3 in L_ipairs(G['codeunits']):
						L_insert(checkthese, v_3)
				if ((L_len(checkthese) > 0) or (L_len(G['letterunits']) > 0)):
					for iid, unitid in L_ipairs(checkthese):
						unit = G['mmf']['newObject'](unitid)
						x, y = unit['values'][G['XPOS']], unit['values'][G['YPOS']]
						ox, oy, nox, noy = 0, 0, None, None
						tileid = (x + (y * G['roomsizex']))
						G['setcolour'](unit['fixed'])
						if (((alreadyused[tileid] is None) and (unit['values'][G['TYPE']] != 5)) and (unit['flags'][G['DEAD']] is False)):
							for i_4 in L_range(1, 2):
								drs = G['dirs'][(i_4 + 2)]
								ndrs = G['dirs'][i_4]
								ox = drs[1]
								oy = drs[2]
								nox = ndrs[1]
								noy = ndrs[2]
								hm = L_first(G['codecheck'](unitid, ox, oy, i_4, None, wordunitresult))
								hm2 = L_first(G['codecheck'](unitid, nox, noy, i_4, None, wordunitresult))
								if ((L_len(hm) == 0) and (L_len(hm2) > 0)):
									L_insert(firstwords, L_T([L_T([unitid]), i_4, 1, unit['strings'][G['UNITNAME']], unit['values'][G['TYPE']], L_T()]))
									if (alreadyused[tileid] is None):
										alreadyused[tileid] = L_T()
									alreadyused[tileid][i_4] = 1
					for a, b in L_pairs(G['letterunits_map']):
						for iid_2, data in L_ipairs(b):
							x_2, y_2, i_5 = data[3], data[4], data[5]
							unitids = data[7]
							width = data[6]
							word, wtype = data[1], data[2]
							unitid_2 = unitids[1]
							tileid_2 = (x_2 + (y_2 * G['roomsizex']))
							if ((alreadyused[tileid_2] is None) or ((alreadyused[tileid_2] is not None) and (alreadyused[tileid_2][i_5] is None))):
								drs_2 = G['dirs'][(i_5 + 2)]
								ndrs_2 = G['dirs'][i_5]
								G['ox'] = drs_2[1]
								G['oy'] = drs_2[2]
								G['nox'] = (ndrs_2[1] * width)
								G['noy'] = (ndrs_2[2] * width)
								hm_2 = L_first(G['codecheck'](unitid_2, G['ox'], G['oy'], i_5))
								hm2_2 = L_first(G['codecheck'](unitid_2, G['nox'], G['noy'], i_5))
								if ((L_len(hm_2) == 0) and (L_len(hm2_2) > 0)):
									L_insert(firstwords, L_T([unitids, i_5, width, word, wtype, L_T()]))
									if (alreadyused[tileid_2] is None):
										alreadyused[tileid_2] = L_T()
									alreadyused[tileid_2][i_5] = 1
					G['docode'](firstwords, G['wordunits'])
					G['subrules']()
					G['grouprules']()
					playrulesound = G['postrules'](alreadyrun)
					G['updatecode'] = 0
					newwordunits, newwordidentifier, wordrelatedunits = L_adjust((*G['findwordunits'](),), 3)
					if (newwordidentifier != wordidentifier):
						G['updatecode'] = 1
						G['code'](True)
					else:
						pass
			else:
				G['MF_alert']('Level destroyed - code() run too many times')
				G['destroylevel']('infinity')
				return None
			if (alreadyrun is False):
				G['effects_decors']()
				if (G['featureindex']['broken'] is not None):
					G['brokenblock'](G['checkthese'])
				if (G['featureindex']['3d'] is not None):
					G['updatevisiontargets']()
				if L_t(G['generaldata']['flags'][G['LOGGING']]):
					G['updatelogrules']()
			G['do_mod_hook']('rule_update_after', L_T([alreadyrun]))
		if (alreadyrun is False):
			rulesoundshort = ''
			alreadyrun = True
			if ((playrulesound is not None and playrulesound is not False) and (G['generaldata5']['values'][G['LEVEL_DISABLERULEEFFECT']] == 0)):
				pmult, sound = L_adjust((*G['checkeffecthistory']('rule'),), 2)
				rulesoundshort = sound
				rulename = L_concat('rule', L_tostring(G['math']['random'](1, 5)), rulesoundshort)
				G['MF_playsound'](rulename)
	G['code'] = f_code
	def f_docode(firstwords_2=None, *_):  # L191
		donefirstwords = L_T()
		existingfinals = L_T()
		limiter = 0
		if (L_len(firstwords_2) > 0):
			for k, unitdata in L_ipairs(firstwords_2):
				if (L_type(unitdata[1]) == 'number'):
					G['timedmessage']('Old rule format detected. Please replace modified .lua files to ensure functionality.')
				unitids_2 = unitdata[1]
				unitid_3 = unitids_2[1]
				dir_ = unitdata[2]
				width_2 = unitdata[3]
				word_2 = unitdata[4]
				wtype_2 = unitdata[5]
				existing = (_t1 if L_t(_t1 := unitdata[6]) else L_T())
				existing_wordid = (_t2 if L_t(_t2 := unitdata[7]) else 1)
				existing_id = (_t3 if L_t(_t3 := unitdata[8]) else '')
				if (L_sub(word_2, 1, 5) == 'text_'):
					word_2 = L_sub(word_2, 6)
				unit_2 = G['mmf']['newObject'](unitid_3)
				x_3, y_3 = unit_2['values'][G['XPOS']], unit_2['values'][G['YPOS']]
				tileid_id = (x_3 + (y_3 * G['roomsizex']))
				unique_id = L_concat(L_tostring(tileid_id), '_', existing_id)
				limiter = (limiter + 1)
				if (limiter > 5000):
					G['MF_alert']('Level destroyed - firstwords run too many times')
					G['destroylevel']('toocomplex')
					return None
				if ((donefirstwords[unique_id] is None) or (((donefirstwords[unique_id] is not None) and (donefirstwords[unique_id][dir_] is None)) and (limiter < 5000))):
					ox_2, oy_2 = 0, 0
					name = word_2
					drs_3 = G['dirs'][dir_]
					ox_2 = drs_3[1]
					oy_2 = drs_3[2]
					if (donefirstwords[unique_id] is None):
						donefirstwords[unique_id] = L_T()
					donefirstwords[unique_id][dir_] = 1
					sentences = L_T()
					finals = L_T()
					maxlen = 0
					variations = 1
					sent_ids = L_T()
					newfirstwords = L_T()
					if (L_len(existing) == 0):
						sentences, finals, maxlen, variations, sent_ids, newfirstwords = L_adjust((*G['calculatesentences'](unitid_3, x_3, y_3, dir_),), 6)
					else:
						sentences[1] = existing
						maxlen = 3
						finals[1] = L_T()
						sent_ids = L_T([existing_id])
					if (sentences is None):
						return None
					if (L_len(newfirstwords) > 0):
						for i_6, v_4 in L_ipairs(newfirstwords):
							L_insert(firstwords_2, v_4)
					if (maxlen > 2):
						for i_7 in L_range(1, variations):
							current = finals[i_7]
							letterword = ''
							stage = 0
							prevstage = 0
							tileids = L_T()
							notids = L_T()
							notwidth = 0
							notslot = 0
							stage3reached = False
							stage2reached = False
							doingcond = False
							nocondsafterthis = False
							condsafeand = False
							firstrealword = False
							letterword_prevstage = 0
							letterword_firstid = 0
							currtiletype = 0
							prevtiletype = 0
							prevsafewordid = 0
							prevsafewordtype = 0
							stop = False
							sent = sentences[i_7]
							sent_id = sent_ids[i_7]
							thissent = ''
							j = 0
							for wordid in L_range(existing_wordid, L_len(sent)):
								j = (j + 1)
								s = sent[wordid]
								nexts = (_t4 if L_t(_t4 := sent[(wordid + 1)]) else L_T([(-1), (-1), L_T([(-1)]), 1]))
								prevtiletype = currtiletype
								tilename = s[1]
								tiletype = s[2]
								tileid_3 = s[3][1]
								tilewidth = s[4]
								if (L_sub(tilename, 1, 10) == 'text_text_'):
									tilename = L_sub(tilename, 6)
								wordtile = False
								currtiletype = tiletype
								thissent = L_concat(thissent, tilename, ',', L_tostring(wordid), '  ')
								for a_2, b_2 in L_ipairs(s[3]):
									L_insert(tileids, b_2)
								if (tiletype != 5):
									if (stage == 0):
										if (tiletype == 0):
											prevstage = stage
											stage = 2
										elif (tiletype == 3):
											prevstage = stage
											stage = 1
										elif (tiletype != 4):
											prevstage = stage
											stage = (-1)
											stop = True
									elif (stage == 1):
										if (tiletype == 0):
											prevstage = stage
											stage = 2
										elif (tiletype == 6):
											prevstage = stage
											stage = 6
										elif (tiletype != 4):
											prevstage = stage
											stage = (-1)
											stop = True
									elif (stage == 2):
										if (wordid != L_len(sent)):
											if (((tiletype == 1) and (prevtiletype != 4)) and (((prevstage != 4) or (doingcond is not None and doingcond is not False)) or (stage3reached is False))):
												stage2reached = True
												doingcond = False
												prevstage = stage
												nocondsafterthis = True
												stage = 3
											elif ((((tiletype == 7) and (stage2reached is False)) and (nocondsafterthis is False)) and ((doingcond is False) or (prevstage != 4))):
												doingcond = True
												prevstage = stage
												stage = 3
											elif ((tiletype == 6) and (prevtiletype != 4)):
												prevstage = stage
												stage = 4
											elif (tiletype != 4):
												prevstage = stage
												stage = (-1)
												stop = True
										else:
											stage = (-1)
											stop = True
									elif (stage == 3):
										stage3reached = True
										if (((tiletype == 0) or (tiletype == 2)) or (tiletype == 8)):
											prevstage = stage
											stage = 5
										elif (tiletype != 4):
											stage = (-1)
											stop = True
									elif (stage == 4):
										if (wordid <= L_len(sent)):
											if (((tiletype == 0) or ((tiletype == 2) and (stage3reached is not None and stage3reached is not False))) or ((tiletype == 8) and (stage3reached is not None and stage3reached is not False))):
												prevstage = stage
												stage = 2
											elif ((((tiletype == 1) and (stage3reached is not None and stage3reached is not False)) and (doingcond is False)) and (prevtiletype != 4)):
												stage2reached = True
												nocondsafterthis = True
												prevstage = stage
												stage = 3
											elif (((tiletype == 7) and (nocondsafterthis is False)) and ((prevtiletype != 6) or ((prevtiletype == 6) and (doingcond is not None and doingcond is not False)))):
												doingcond = True
												stage2reached = True
												prevstage = stage
												stage = 3
											elif (tiletype != 4):
												prevstage = stage
												stage = (-1)
												stop = True
										else:
											stage = (-1)
											stop = True
									elif (stage == 5):
										if (wordid != L_len(sent)):
											if (((tiletype == 1) and (doingcond is not None and doingcond is not False)) and (prevtiletype != 4)):
												stage2reached = True
												doingcond = False
												prevstage = stage
												nocondsafterthis = True
												stage = 3
											elif ((tiletype == 6) and (prevtiletype != 4)):
												prevstage = stage
												stage = 4
											elif (tiletype != 4):
												prevstage = stage
												stage = (-1)
												stop = True
										else:
											stage = (-1)
											stop = True
									elif (stage == 6):
										if (tiletype == 3):
											prevstage = stage
											stage = 1
										elif (tiletype != 4):
											prevstage = stage
											stage = (-1)
											stop = True
								if (stage > 0):
									firstrealword = True
								if (tiletype == 4):
									if ((L_len(notids) == 0) or (prevtiletype == 0)):
										notids = s[3]
										notwidth = tilewidth
										notslot = wordid
								else:
									if ((stop is False) and (tiletype != 0)):
										notids = L_T()
										notwidth = 0
										notslot = 0
								if ((prevtiletype != 4) and (wordid > existing_wordid)):
									prevsafewordid = (wordid - 1)
									prevsafewordtype = prevtiletype
								if ((prevtiletype == 4) and (tiletype == 6)):
									stop = True
									stage = (-1)
								if (stop is False):
									subsent_id = L_sub(sent_id, ((wordid - existing_wordid) + 1))
									current['sent'] = sent
									L_insert(current, L_T([tilename, tiletype, tileids, tilewidth, wordid, subsent_id]))
									tileids = L_T()
									if (((wordid == L_len(sent)) and (L_len(current) >= 3)) and (j > 1)):
										subsent_id = L_concat(L_tostring(tileid_id), '_', L_sub(sent_id, 1, j), '_', L_tostring(dir_))
										if (existingfinals[subsent_id] is None):
											existingfinals[subsent_id] = 1
										else:
											finals[i_7] = L_T()
								else:
									for a_3 in L_range(1, L_len(s[3])):
										if (L_len(tileids) > 0):
											L_remove(tileids, L_len(tileids))
									if (((tiletype == 0) and (prevtiletype == 0)) and (L_len(notids) > 0)):
										notids = L_T()
										notwidth = 0
									if ((L_len(current) >= 3) and (j > 1)):
										subsent_id_2 = L_concat(L_tostring(tileid_id), '_', L_sub(sent_id, 1, (j - 1)), '_', L_tostring(dir_))
										if (existingfinals[subsent_id_2] is None):
											existingfinals[subsent_id_2] = 1
										else:
											finals[i_7] = L_T()
									if (wordid < L_len(sent)):
										if (wordid > existing_wordid):
											if (((((L_len(notids) > 0) and (firstrealword is not None and firstrealword is not False)) and (notslot > 1)) and ((tiletype != 7) or ((tiletype == 7) and (prevtiletype == 0)))) and ((tiletype != 1) or ((tiletype == 1) and (prevtiletype == 0)))):
												subsent_id_3 = L_sub(sent_id, ((notslot - existing_wordid) + 1))
												L_insert(firstwords_2, L_T([notids, dir_, notwidth, 'not', 4, sent, notslot, subsent_id_3]))
												if (((nexts[2] is not None) and (((nexts[2] == 0) or (nexts[2] == 3)) or (nexts[2] == 4))) and (tiletype != 3)):
													subsent_id_3 = L_sub(sent_id, j)
													L_insert(firstwords_2, L_T([s[3], dir_, tilewidth, tilename, tiletype, sent, wordid, subsent_id_3]))
											else:
												if ((prevtiletype == 0) and ((tiletype == 1) or (tiletype == 7))):
													subsent_id_4 = L_sub(sent_id, (wordid - existing_wordid))
													L_insert(firstwords_2, L_T([sent[(wordid - 1)][3], dir_, tilewidth, tilename, tiletype, sent, (wordid - 1), subsent_id_4]))
												elif (((((prevsafewordtype == 0) and (prevsafewordid > 0)) and (prevtiletype == 4)) and (tiletype != 1)) and (tiletype != 2)):
													subsent_id_5 = L_sub(sent_id, ((prevsafewordid - existing_wordid) + 1))
													L_insert(firstwords_2, L_T([sent[prevsafewordid][3], dir_, tilewidth, tilename, tiletype, sent, prevsafewordid, subsent_id_5]))
												else:
													subsent_id_6 = L_sub(sent_id, j)
													L_insert(firstwords_2, L_T([s[3], dir_, tilewidth, tilename, tiletype, sent, wordid, subsent_id_6]))
											break
										elif (wordid == existing_wordid):
											if (nexts[3][1] != (-1)):
												subsent_id_7 = L_sub(sent_id, (j + 1))
												L_insert(firstwords_2, L_T([nexts[3], dir_, nexts[4], nexts[1], nexts[2], sent, (wordid + 1), subsent_id_7]))
											break
					if (L_len(finals) > 0):
						for i_8, sentence in L_ipairs(finals):
							group_objects = L_T()
							group_targets = L_T()
							group_conds = L_T()
							group = group_objects
							stage_2 = 0
							prefix = ''
							allowedwords = L_T([0])
							allowedwords_extra = L_T()
							testing = ''
							extraids = L_T()
							extraids_current = ''
							extraids_ifvalid = L_T()
							valid = True
							if (L_len(sentence) >= 3):
								if (L_len(finals) > 1):
									for a_4, b_3 in L_ipairs(finals):
										if ((L_len(b_3) == L_len(sentence)) and (a_4 > i_8)):
											identical = True
											for c, d in L_ipairs(b_3):
												currids = d[3]
												equivids = (_t5 if L_t(_t5 := sentence[c][3]) else L_T())
												for e, f in L_ipairs(currids):
													if (f != equivids[e]):
														identical = False
											if (identical is not None and identical is not False):
												valid = False
							else:
								valid = False
							if (valid is not None and valid is not False):
								for index, wdata in L_ipairs(sentence):
									wname = wdata[1]
									wtype_3 = wdata[2]
									wid = wdata[3]
									testing = L_concat(testing, wname, ' ')
									wcategory = (-1)
									if (((wtype_3 == 1) or (wtype_3 == 3)) or (wtype_3 == 7)):
										wcategory = 1
									elif ((wtype_3 != 4) and (wtype_3 != 6)):
										wcategory = 0
									else:
										L_insert(extraids_ifvalid, L_T([L_concat(prefix, wname), wtype_3, wid]))
										extraids_current = wname
									if (wcategory == 0):
										allowed = False
										for a_5, b_4 in L_ipairs(allowedwords):
											if (b_4 == wtype_3):
												allowed = True
												break
										if (allowed is False):
											for a_6, b_5 in L_ipairs(allowedwords_extra):
												if (wname == b_5):
													allowed = True
													break
										if (allowed is not None and allowed is not False):
											L_insert(group, L_T([L_concat(prefix, wname), wtype_3, wid]))
										else:
											sent_2 = sentence['sent']
											wordid_2 = wdata[5]
											subsent_id_8 = wdata[6]
											L_insert(firstwords_2, L_T([L_T([wid[1]]), dir_, 1, wname, wtype_3, sent_2, wordid_2, subsent_id_8]))
											break
									elif (wcategory == 1):
										if (index < L_len(sentence)):
											allowedwords = L_T([0])
											allowedwords_extra = L_T()
											realname = G['unitreference'][L_concat('text_', wname)]
											cargtype = False
											cargextra = False
											argtype = L_T([0])
											argextra = L_T()
											if (G['changes'][realname] is not None):
												wchanges = G['changes'][realname]
												if (wchanges['argtype'] is not None):
													argtype = wchanges['argtype']
													cargtype = True
												if (wchanges['argextra'] is not None):
													argextra = wchanges['argextra']
													cargextra = True
											if ((cargtype is False) or (cargextra is False)):
												wvalues = (_t6 if L_t(_t6 := G['tileslist'][realname]) else L_T())
												if (cargtype is False):
													argtype = (_t7 if L_t(_t7 := wvalues['argtype']) else L_T([0]))
												if (cargextra is False):
													argextra = (_t8 if L_t(_t8 := wvalues['argextra']) else L_T())
											if (realname is None):
												G['MF_alert'](L_concat('No object found for ', wname, '!'))
												valid = False
												break
											else:
												if (wtype_3 == 1):
													allowedwords = argtype
													stage_2 = 1
													target = L_T([L_concat(prefix, wname), wtype_3, wid])
													L_insert(group_targets, L_T([target, L_T()]))
													sid = L_len(group_targets)
													group = group_targets[sid][2]
													G['newcondgroup'] = 1
												elif (wtype_3 == 3):
													allowedwords = L_T([0])
													cond = L_T([L_concat(prefix, wname), wtype_3, wid])
													L_insert(group_conds, L_T([cond, L_T()]))
												elif (wtype_3 == 7):
													allowedwords = argtype
													allowedwords_extra = argextra
													stage_2 = 2
													cond_2 = L_T([L_concat(prefix, wname), wtype_3, wid])
													L_insert(group_conds, L_T([cond_2, L_T()]))
													sid_2 = L_len(group_conds)
													group = group_conds[sid_2][2]
									if (wtype_3 == 4):
										if (prefix == 'not '):
											prefix = ''
										else:
											prefix = 'not '
									else:
										prefix = ''
									if (((wname != extraids_current) and (L_strlen(extraids_current) > 0)) and (wtype_3 != 4)):
										for a_7, extraids_valid in L_ipairs(extraids_ifvalid):
											L_insert(extraids, L_T([L_concat(prefix, extraids_valid[1]), extraids_valid[2], extraids_valid[3]]))
										extraids_ifvalid = L_T()
										extraids_current = ''
								if L_t(G['generaldata']['flags'][G['LOGGING']]):
									G['rulelog'](sentence, testing)
								conds = L_T()
								condids = L_T()
								for c_2, group_cond in L_ipairs(group_conds):
									rule_cond = group_cond[1][1]
									condids = G['copytable'](condids, group_cond[1][3])
									L_insert(conds, L_T([rule_cond, L_T()]))
									condgroup = conds[L_len(conds)][2]
									for e_2, condword in L_ipairs(group_cond[2]):
										rule_condword = condword[1]
										condids = G['copytable'](condids, condword[3])
										L_insert(condgroup, rule_condword)
								for c_3, group_object in L_ipairs(group_objects):
									rule_object = group_object[1]
									for d_2, group_target in L_ipairs(group_targets):
										rule_verb = group_target[1][1]
										for e_3, target_2 in L_ipairs(group_target[2]):
											rule_target = target_2[1]
											finalconds = L_T()
											for g, finalcond in L_ipairs(conds):
												L_insert(finalconds, L_T([finalcond[1], finalcond[2]]))
											rule = L_T([rule_object, rule_verb, rule_target])
											ids = L_T()
											ids = G['copytable'](ids, group_object[3])
											ids = G['copytable'](ids, group_target[1][3])
											ids = G['copytable'](ids, target_2[3])
											for g_2, h in L_ipairs(extraids):
												ids = G['copytable'](ids, h[3])
											for g_3, h_2 in L_ipairs(condids):
												ids = G['copytable'](ids, h_2)
											G['addoption'](rule, finalconds, ids)
	G['docode'] = f_docode
	def f_codecheck(unitid_4=None, ox_3=None, oy_3=None, cdir_=None, ignore_end_=None, wordunitresult_=None, *_):  # L858
		unit_3 = G['mmf']['newObject'](unitid_4)
		ux, uy = unit_3['values'][G['XPOS']], unit_3['values'][G['YPOS']]
		x_4 = (unit_3['values'][G['XPOS']] + ox_3)
		y_4 = (unit_3['values'][G['YPOS']] + oy_3)
		result = L_T()
		letters = False
		justletters = False
		cdir = (_t1 if L_t(_t1 := cdir_) else 0)
		wordunitresult_2 = (_t2 if L_t(_t2 := wordunitresult_) else L_T())
		ignore_end = False
		if (ignore_end_ is not None):
			ignore_end = ignore_end_
		if (cdir == 0):
			G['MF_alert']('CODECHECK - CDIR == 0 - why??')
		tileid_4 = (x_4 + (y_4 * G['roomsizex']))
		if (G['unitmap'][tileid_4] is not None):
			for i_9, b_6 in L_ipairs(G['unitmap'][tileid_4]):
				v_5 = G['mmf']['newObject'](b_6)
				w = 1
				if ((v_5['values'][G['TYPE']] != 5) and (v_5['flags'][G['DEAD']] is False)):
					if (v_5['strings'][G['UNITTYPE']] == 'text'):
						L_insert(result, L_T([L_T([b_6]), w, v_5['strings'][G['NAME']], v_5['values'][G['TYPE']], cdir]))
					else:
						if (L_len(G['wordunits']) > 0):
							valid_2 = False
							if ((wordunitresult_2[b_6] is not None) and (wordunitresult_2[b_6] == 1)):
								valid_2 = True
							elif (wordunitresult_2[b_6] is None):
								for c_4, d_3 in L_ipairs(G['wordunits']):
									if ((b_6 == d_3[1]) and L_t(G['testcond'](d_3[2], d_3[1]))):
										valid_2 = True
										break
							if (valid_2 is not None and valid_2 is not False):
								L_insert(result, L_T([L_T([b_6]), w, v_5['strings'][G['UNITNAME']], v_5['values'][G['TYPE']], cdir]))
				else:
					justletters = True
		if (G['letterunits_map'][tileid_4] is not None):
			for i_10, v_6 in L_ipairs(G['letterunits_map'][tileid_4]):
				unitids_3 = v_6[7]
				width_3 = v_6[6]
				word_3 = v_6[1]
				wtype_4 = v_6[2]
				dir__2 = v_6[5]
				if ((L_strlen(word_3) > 5) and (L_sub(word_3, 1, 5) == 'text_')):
					word_3 = L_sub(v_6[1], 6)
				valid_3 = True
				if (((ignore_end is not None and ignore_end is not False) and ((x_4 != v_6[3]) or (y_4 != v_6[4]))) and (width_3 > 1)):
					valid_3 = False
				if ((cdir != 0) and (width_3 > 1)):
					if ((((cdir == 1) and (ux > v_6[3])) and (ux < (v_6[3] + width_3))) or (((cdir == 2) and (uy > v_6[4])) and (uy < (v_6[4] + width_3)))):
						valid_3 = False
				if ((dir__2 == cdir) and (valid_3 is not None and valid_3 is not False)):
					L_insert(result, L_T([unitids_3, width_3, word_3, wtype_4, dir__2]))
					letters = True
		return (result, letters, justletters,)
		return ()
	G['codecheck'] = f_codecheck
	def f_addoption(option=None, conds_=None, ids_2=None, visible=None, notrule=None, tags_=None, *_):  # L949
		visual = True
		if (visible is not None):
			visual = visible
		conds_2 = L_T()
		if (conds_ is not None):
			conds_2 = conds_
		else:
			G['MF_alert'](L_concat('nil conditions in rule: ', option[1], ', ', option[2], ', ', option[3]))
		tags = (_t1 if L_t(_t1 := tags_) else L_T())
		if (L_len(option) == 3):
			rule_2 = L_T([option, conds_2, ids_2, tags])
			L_insert(G['features'], rule_2)
			target_3 = option[1]
			verb = option[2]
			effect = option[3]
			if (G['featureindex'][effect] is None):
				G['featureindex'][effect] = L_T()
			if (G['featureindex'][target_3] is None):
				G['featureindex'][target_3] = L_T()
			if (G['featureindex'][verb] is None):
				G['featureindex'][verb] = L_T()
			L_insert(G['featureindex'][effect], rule_2)
			L_insert(G['featureindex'][verb], rule_2)
			if (target_3 != effect):
				L_insert(G['featureindex'][target_3], rule_2)
			if (visual is not None and visual is not False):
				visualrule = G['copyrule'](rule_2)
				L_insert(G['visualfeatures'], visualrule)
			groupcond = False
			if ((((L_sub(target_3, 1, 5) == 'group') or (L_sub(effect, 1, 5) == 'group')) or (L_sub(target_3, 1, 9) == 'not group')) or (L_sub(effect, 1, 9) == 'not group')):
				groupcond = True
			if (notrule is not None):
				notrule_effect = notrule[1]
				notrule_id = notrule[2]
				if (G['notfeatures'][notrule_effect] is None):
					G['notfeatures'][notrule_effect] = L_T()
				nr_e = G['notfeatures'][notrule_effect]
				if (nr_e[notrule_id] is None):
					nr_e[notrule_id] = L_T()
				nr_i = nr_e[notrule_id]
				L_insert(nr_i, rule_2)
			if (L_len(conds_2) > 0):
				addedto = L_T()
				for i_11, cond_3 in L_ipairs(conds_2):
					condname = cond_3[1]
					if (L_sub(condname, 1, 4) == 'not '):
						condname = L_sub(condname, 5)
					if (G['condfeatureindex'][condname] is None):
						G['condfeatureindex'][condname] = L_T()
					if (addedto[condname] is None):
						L_insert(G['condfeatureindex'][condname], rule_2)
						addedto[condname] = 1
					if (cond_3[2] is not None):
						if (L_len(cond_3[2]) > 0):
							newconds = L_T()
							for a_8, b_7 in L_ipairs(cond_3[2]):
								alreadyused_2 = L_T()
								if ((b_7 != 'all') and (b_7 != 'not all')):
									alreadyused_2[b_7] = 1
									L_insert(newconds, b_7)
								elif (b_7 == 'all'):
									for a_9, mat in L_pairs(G['objectlist']):
										if ((alreadyused_2[a_9] is None) and (G['findnoun'](a_9, G['nlist']['short']) is False)):
											L_insert(newconds, a_9)
											alreadyused_2[a_9] = 1
								elif (b_7 == 'not all'):
									L_insert(newconds, 'empty')
									L_insert(newconds, 'text')
								if ((L_sub(b_7, 1, 5) == 'group') or (L_sub(b_7, 1, 9) == 'not group')):
									groupcond = True
							cond_3[2] = newconds
			if (groupcond is not None and groupcond is not False):
				L_insert(G['groupfeatures'], rule_2)
			targetnot = L_sub(target_3, 1, 4)
			targetnot_ = L_sub(target_3, 5)
			if ((((((targetnot == 'not ') and (G['objectlist'][targetnot_] is not None)) and (L_sub(targetnot_, 1, 5) != 'group')) and (L_sub(effect, 1, 5) != 'group')) and (L_sub(effect, 1, 9) != 'not group')) or (((L_sub(effect, 1, 5) == 'group') or (L_sub(effect, 1, 9) == 'not group')) and (targetnot_ == 'all'))):
				if (targetnot_ != 'all'):
					for i_12, mat_2 in L_pairs(G['objectlist']):
						if ((i_12 != targetnot_) and (G['findnoun'](i_12) is False)):
							rule_3 = L_T([i_12, verb, effect])
							newconds_2 = L_T()
							for a_10, b_8 in L_ipairs(conds_2):
								L_insert(newconds_2, b_8)
							G['addoption'](rule_3, newconds_2, ids_2, False, L_T([effect, L_len(G['featureindex'][effect])]), tags)
				else:
					mats = L_T(['empty', 'text'])
					for m, i_13 in L_pairs(mats):
						rule_4 = L_T([i_13, verb, effect])
						newconds_3 = L_T()
						for a_11, b_9 in L_ipairs(conds_2):
							L_insert(newconds_3, b_9)
						G['addoption'](rule_4, newconds_3, ids_2, False, L_T([effect, L_len(G['featureindex'][effect])]), tags)
	G['addoption'] = f_addoption
	def f_subrules(*_):  # L1112
		mimicprotects = L_T()
		if (G['featureindex']['all'] is not None):
			for k_2, rules in L_ipairs(G['featureindex']['all']):
				rule_5 = rules[1]
				conds_3 = rules[2]
				ids_3 = rules[3]
				tags_2 = rules[4]
				if (rule_5[3] == 'all'):
					if (rule_5[2] != 'is'):
						nconds = L_T()
						if (G['featureindex']['not all'] is not None):
							for a_12, prules in L_ipairs(G['featureindex']['not all']):
								prule = prules[1]
								pconds = prules[2]
								if (((prule[1] == rule_5[1]) and (prule[2] == rule_5[2])) and (prule[3] == 'not all')):
									ipconds = L_first(G['invertconds'](pconds))
									for c_5, d_4 in L_ipairs(ipconds):
										L_insert(nconds, d_4)
						for i_14, mat_3 in L_pairs(G['objectlist']):
							if (G['findnoun'](i_14) is False):
								newrule = L_T([rule_5[1], rule_5[2], i_14])
								newconds_4 = L_T()
								for a_13, b_10 in L_ipairs(conds_3):
									L_insert(newconds_4, b_10)
								for a_14, b_11 in L_ipairs(nconds):
									L_insert(newconds_4, b_11)
								G['addoption'](newrule, newconds_4, ids_3, False, None, tags_2)
				if ((rule_5[1] == 'all') and (L_sub(rule_5[3], 1, 4) != 'not ')):
					nconds_2 = L_T()
					if (G['featureindex']['not all'] is not None):
						for a_15, prules_2 in L_ipairs(G['featureindex']['not all']):
							prule_2 = prules_2[1]
							pconds_2 = prules_2[2]
							if (((prule_2[1] == rule_5[1]) and (prule_2[2] == rule_5[2])) and (prule_2[3] == L_concat('not ', rule_5[3]))):
								ipconds_2 = L_first(G['invertconds'](pconds_2))
								if L_t(G['crashy_']):
									G['crashy'] = True
								for c_6, d_5 in L_ipairs(ipconds_2):
									L_insert(nconds_2, d_5)
					for i_15, mat_4 in L_pairs(G['objectlist']):
						if (G['findnoun'](i_15) is False):
							newrule_2 = L_T([i_15, rule_5[2], rule_5[3]])
							newconds_5 = L_T()
							for a_16, b_12 in L_ipairs(conds_3):
								L_insert(newconds_5, b_12)
							for a_17, b_13 in L_ipairs(nconds_2):
								L_insert(newconds_5, b_13)
							G['addoption'](newrule_2, newconds_5, ids_3, False, None, tags_2)
				if ((rule_5[1] == 'all') and (L_sub(rule_5[3], 1, 4) == 'not ')):
					for i_16, mat_5 in L_pairs(G['objectlist']):
						if (G['findnoun'](i_16) is False):
							newrule_3 = L_T([i_16, rule_5[2], rule_5[3]])
							newconds_6 = L_T()
							for a_18, b_14 in L_ipairs(conds_3):
								L_insert(newconds_6, b_14)
							G['addoption'](newrule_3, newconds_6, ids_3, False, None, tags_2)
		if (G['featureindex']['mimic'] is not None):
			for i_17, rules_2 in L_ipairs(G['featureindex']['mimic']):
				rule_6 = rules_2[1]
				conds_4 = rules_2[2]
				tags_3 = rules_2[4]
				if (rule_6[2] == 'mimic'):
					object = rule_6[1]
					target_4 = rule_6[3]
					isnot = False
					if (L_sub(target_4, 1, 4) == 'not '):
						target_4 = L_sub(target_4, 5)
						isnot = True
					if (isnot is not None and isnot is not False):
						if (mimicprotects[object] is None):
							mimicprotects[object] = L_T()
						L_insert(mimicprotects[object], L_T([target_4, conds_4, rule_6[3]]))
		limiter_2 = 0
		limit = 250
		if (G['featureindex']['mimic'] is not None):
			for i_18, rules_3 in L_ipairs(G['featureindex']['mimic']):
				rule_7 = rules_3[1]
				conds_5 = rules_3[2]
				tags_4 = rules_3[4]
				if (rule_7[2] == 'mimic'):
					object_2 = rule_7[1]
					target_5 = rule_7[3]
					mprotects = (_t1 if L_t(_t1 := mimicprotects[object_2]) else L_T())
					extraconds = L_T()
					valid_4 = True
					if (L_sub(target_5, 1, 4) == 'not '):
						valid_4 = False
					for a_19, b_15 in L_ipairs(mprotects):
						if (b_15[1] == target_5):
							pconds_3 = b_15[2]
							if (L_len(pconds_3) == 0):
								valid_4 = False
							else:
								newconds_7 = L_first(G['invertconds'](pconds_3))
								for c_7, d_6 in L_ipairs(newconds_7):
									L_insert(extraconds, d_6)
					copythese = L_T()
					if (valid_4 is not None and valid_4 is not False):
						if ((G['getmat'](object_2) is not None) and (G['getmat'](target_5) is not None)):
							if (G['featureindex'][target_5] is not None):
								copythese = G['featureindex'][target_5]
						for a_20, b_16 in L_ipairs(copythese):
							trule = b_16[1]
							tconds = b_16[2]
							ids_4 = b_16[3]
							ttags = b_16[4]
							valid_5 = True
							for c_8, d_7 in L_ipairs(ttags):
								if (d_7 == 'mimic'):
									valid_5 = False
							if (((trule[1] == target_5) and (trule[2] != 'mimic')) and (valid_5 is not None and valid_5 is not False)):
								newconds_8 = L_T()
								newtags = L_T()
								for c_9, d_8 in L_ipairs(tconds):
									L_insert(newconds_8, d_8)
								for c_10, d_9 in L_ipairs(conds_5):
									L_insert(newconds_8, d_9)
								for c_11, d_10 in L_ipairs(extraconds):
									L_insert(newconds_8, d_10)
								for c_12, d_11 in L_ipairs(ttags):
									L_insert(newtags, d_11)
								for c_13, d_12 in L_ipairs(tags_4):
									L_insert(newtags, d_12)
								L_insert(newtags, L_concat('mimicparent_', L_tostring(i_18)))
								L_insert(newtags, 'mimic')
								newword1 = object_2
								newword2 = trule[2]
								newword3 = trule[3]
								newrule_4 = L_T([newword1, newword2, newword3])
								limiter_2 = (limiter_2 + 1)
								G['addoption'](newrule_4, newconds_8, ids_4, True, None, newtags)
								if (limiter_2 > limit):
									G['MF_alert']('Level destroyed - mimic happened too many times!')
									G['destroylevel']('toocomplex')
									return None
	G['subrules'] = f_subrules
	def f_postrules(alreadyrun__2=None, *_):  # L1345
		protects = L_T()
		newruleids = L_T()
		ruleeffectlimiter = L_T()
		playrulesound_2 = False
		alreadyrun_2 = (_t1 if L_t(_t1 := alreadyrun__2) else False)
		for i_19, unit_4 in L_ipairs(G['units']):
			unit_4['active'] = False
		limit_2 = L_len(G['features'])
		for i_20, rules_4 in L_ipairs(G['features']):
			if (i_20 <= limit_2):
				rule_8 = rules_4[1]
				conds_6 = rules_4[2]
				ids_5 = rules_4[3]
				if ((rule_8[1] == rule_8[3]) and (rule_8[2] == 'is')):
					L_insert(protects, i_20)
				if (ids_5 is not None):
					works = True
					idlist = L_T()
					effectsok = False
					if (L_len(ids_5) > 0):
						for a_21, b_17 in L_ipairs(ids_5):
							L_insert(idlist, b_17)
					if ((L_len(idlist) > 0) and (works is not None and works is not False)):
						for a_22, d_13 in L_ipairs(idlist):
							for c_14, b_18 in L_ipairs(d_13):
								if (b_18 != 0):
									bunit = G['mmf']['newObject'](b_18)
									if (bunit['strings'][G['UNITTYPE']] == 'text'):
										bunit['active'] = True
										G['setcolour'](b_18, 'active')
									newruleids[b_18] = 1
									if ((((G['ruleids'][b_18] is None) and (L_len(G['undobuffer']) > 1)) and (alreadyrun_2 is False)) and (G['generaldata5']['values'][G['LEVEL_DISABLERULEEFFECT']] == 0)):
										if (ruleeffectlimiter[b_18] is None):
											x_5, y_5 = bunit['values'][G['XPOS']], bunit['values'][G['YPOS']]
											c1, c2 = L_adjust((*G['getcolour'](b_18, 'active'),), 2)
											G['MF_particles_for_unit']('bling', x_5, y_5, 5, c1, c2, 1, 1, b_18)
											ruleeffectlimiter[b_18] = 1
										if (rule_8[2] != 'play'):
											playrulesound_2 = True
					elif ((L_len(idlist) > 0) and (works is False)):
						for a_23, visualrules in L_pairs(G['visualfeatures']):
							vrule = visualrules[1]
							same = G['comparerules'](rule_8, vrule)
							if (same is not None and same is not False):
								L_remove(G['visualfeatures'], a_23)
				rulenot = 0
				neweffect = ''
				nothere = L_sub(rule_8[3], 1, 4)
				if (nothere == 'not '):
					rulenot = 1
					neweffect = L_sub(rule_8[3], 5)
				if (rulenot == 1):
					newconds_9, crashy = L_adjust((*G['invertconds'](conds_6, None, rule_8[3]),), 2)
					newbaserule = L_T([rule_8[1], rule_8[2], neweffect])
					target_6 = rule_8[1]
					verb_2 = rule_8[2]
					targetlists = L_T()
					L_insert(targetlists, target_6)
					if (((verb_2 == 'is') and (neweffect == 'text')) and (G['featureindex']['write'] is not None)):
						L_insert(targetlists, 'write')
					for e_4, g_4 in L_ipairs(targetlists):
						for a_24, b_19 in L_ipairs(G['featureindex'][g_4]):
							same_2 = G['comparerules'](newbaserule, b_19[1])
							if ((same_2 is not None and same_2 is not False) or (((g_4 == 'write') and (target_6 == b_19[1][1])) and (b_19[1][2] == 'write'))):
								theseconds = b_19[2]
								if (L_len(newconds_9) > 0):
									if (newconds_9[1] != 'never'):
										for c_15, d_14 in L_ipairs(newconds_9):
											L_insert(theseconds, d_14)
									else:
										theseconds = L_T(['never', L_T()])
								if (crashy is not None and crashy is not False):
									G['addoption'](L_T([rule_8[1], 'is', 'crash']), theseconds, ids_5, False, None, rules_4[4])
								b_19[2] = theseconds
		if (L_len(protects) > 0):
			for i_21, v_7 in L_ipairs(protects):
				rule_9 = G['features'][v_7]
				baserule = rule_9[1]
				conds_7 = rule_9[2]
				target_7 = baserule[1]
				newconds_10 = L_T([L_T(['never', L_T()])])
				if (conds_7[1] != 'never'):
					if (L_len(conds_7) > 0):
						newconds_10 = L_T()
						for a_25, b_20 in L_ipairs(conds_7):
							condword_2 = b_20[1]
							condgroup_2 = L_T()
							if (L_sub(condword_2, 1, 1) == '('):
								condword_2 = L_sub(condword_2, 2)
							if (L_sub(condword_2, (-1)) == ')'):
								condword_2 = L_sub(condword_2, 1, (L_len(condword_2) - 1))
							newcondword = L_concat('not ', condword_2)
							if (L_sub(condword_2, 1, 3) == 'not'):
								newcondword = L_sub(condword_2, 5)
							if (a_25 == 1):
								newcondword = L_concat('(', newcondword)
							if (a_25 == L_len(conds_7)):
								newcondword = L_concat(newcondword, ')')
							if (b_20[2] is not None):
								for c_16, d_15 in L_ipairs(b_20[2]):
									L_insert(condgroup_2, d_15)
							L_insert(newconds_10, L_T([newcondword, condgroup_2]))
					if (G['featureindex'][target_7] is not None):
						for a_26, rules_5 in L_ipairs(G['featureindex'][target_7]):
							targetrule = rules_5[1]
							targetconds = rules_5[2]
							object_3 = targetrule[3]
							if ((((targetrule[1] == target_7) and (((targetrule[2] == 'is') and (target_7 != object_3)) or ((targetrule[2] == 'write') and (L_sub(object_3, 1, 4) != 'not ')))) and (((G['getmat'](object_3) is not None) or (object_3 == 'revert')) or ((targetrule[2] == 'write') and (L_sub(object_3, 1, 4) != 'not ')))) and (L_sub(object_3, 1, 5) != 'group')):
								if (L_len(newconds_10) > 0):
									if (newconds_10[1] == 'never'):
										targetconds = L_T()
									for c_17, d_16 in L_ipairs(newconds_10):
										L_insert(targetconds, d_16)
								rules_5[2] = targetconds
		G['ruleids'] = newruleids
		if (G['spritedata']['values'][G['VISION']] == 0):
			G['ruleblockeffect']()
		return playrulesound_2
	G['postrules'] = f_postrules
	def f_grouprules(*_):  # L1559
		G['groupmembers'] = L_T()
		groupmembers_quick = L_T()
		isgroup = L_T()
		isnotgroup = L_T()
		xgroup = L_T()
		xnotgroup = L_T()
		groupx = L_T()
		notgroupx = L_T()
		groupxgroup = L_T()
		groupxgroup_diffname = L_T()
		groupisnotgroup = L_T()
		notgroupisgroup = L_T()
		evilrecursion = False
		notgroupisgroup_diffname = L_T()
		memberships = L_T()
		combined = L_T()
		for i_22, v_8 in L_ipairs(G['groupfeatures']):
			rule_10 = v_8[1]
			conds_8 = v_8[2]
			type_isgroup = False
			type_isnotgroup = False
			type_xgroup = False
			type_xnotgroup = False
			type_groupx = False
			type_notgroupx = False
			type_recursive = False
			groupname1 = ''
			groupname2 = ''
			if (L_sub(rule_10[1], 1, 5) == 'group'):
				type_groupx = True
				groupname1 = rule_10[1]
			elif (L_sub(rule_10[1], 1, 9) == 'not group'):
				type_notgroupx = True
				groupname1 = L_sub(rule_10[1], 5)
			if (L_sub(rule_10[3], 1, 5) == 'group'):
				type_xgroup = True
				groupname2 = rule_10[3]
				if (rule_10[2] == 'is'):
					type_isgroup = True
			elif (L_sub(rule_10[3], 1, 9) == 'not group'):
				type_xnotgroup = True
				groupname2 = L_sub(rule_10[3], 5)
				if (rule_10[2] == 'is'):
					type_isnotgroup = True
			if ((conds_8 is not None) and (L_len(conds_8) > 0)):
				for a_27, cond_4 in L_ipairs(conds_8):
					params = (_t1 if L_t(_t1 := cond_4[2]) else L_T())
					for c_18, param in L_ipairs(params):
						if ((L_sub(param, 1, 5) == 'group') or (L_sub(param, 1, 9) == 'not group')):
							type_recursive = True
							break
			if (type_isgroup is not None and type_isgroup is not False):
				if ((type_groupx is False) and (type_notgroupx is False)):
					L_insert(isgroup, L_T([v_8, type_recursive]))
					if (memberships[rule_10[3]] is None):
						memberships[rule_10[3]] = L_T()
					if (memberships[rule_10[3]][rule_10[1]] is None):
						memberships[rule_10[3]][rule_10[1]] = L_T()
					L_insert(memberships[rule_10[3]][rule_10[1]], L_T([v_8, type_recursive]))
				elif (type_notgroupx is False):
					if (groupname1 == groupname2):
						L_insert(groupxgroup, L_T([v_8, type_recursive]))
					else:
						L_insert(groupxgroup_diffname, L_T([v_8, type_recursive]))
				else:
					if (groupname1 == groupname2):
						L_insert(notgroupisgroup, L_T([v_8, type_recursive]))
					else:
						evilrecursion = True
						L_insert(notgroupisgroup_diffname, L_T([v_8, type_recursive]))
			elif (type_xgroup is not None and type_xgroup is not False):
				if ((type_groupx is False) and (type_notgroupx is False)):
					L_insert(xgroup, L_T([v_8, type_recursive]))
				else:
					L_insert(groupxgroup, L_T([v_8, type_recursive]))
			elif (type_isnotgroup is not None and type_isnotgroup is not False):
				if ((type_groupx is False) and (type_notgroupx is False)):
					if (isnotgroup[rule_10[1]] is None):
						isnotgroup[rule_10[1]] = L_T()
					L_insert(isnotgroup[rule_10[1]], L_T([v_8, type_recursive]))
					if (xnotgroup[rule_10[1]] is None):
						xnotgroup[rule_10[1]] = L_T()
					L_insert(xnotgroup[rule_10[1]], L_T([v_8, type_recursive]))
				elif (type_notgroupx is False):
					if (groupname1 == groupname2):
						L_insert(groupisnotgroup, L_T([v_8, type_recursive]))
					else:
						L_insert(groupxgroup_diffname, L_T([v_8, type_recursive]))
				else:
					if (groupname1 == groupname2):
						L_insert(groupxgroup, L_T([v_8, type_recursive]))
					else:
						evilrecursion = True
						L_insert(notgroupisgroup_diffname, L_T([v_8, type_recursive]))
			elif (type_xnotgroup is not None and type_xnotgroup is not False):
				if (xnotgroup[rule_10[1]] is None):
					xnotgroup[rule_10[1]] = L_T()
				L_insert(xnotgroup[rule_10[1]], L_T([v_8, type_recursive]))
			elif (type_groupx is not None and type_groupx is not False):
				L_insert(groupx, L_T([v_8, type_recursive]))
			elif (type_notgroupx is not None and type_notgroupx is not False):
				L_insert(notgroupx, L_T([v_8, type_recursive]))
		diffname_done = False
		diffname_used = L_T()
		while (diffname_done is False):
			diffname_done = True
			for i_23, v_ in L_ipairs(groupxgroup_diffname):
				if (diffname_used[i_23] is None):
					v_9 = v_[1]
					recursion = (_t2 if L_t(_t2 := v_[2]) else False)
					rule_11 = v_9[1]
					conds_9 = v_9[2]
					ids_6 = v_9[3]
					tags_5 = v_9[4]
					gn1 = rule_11[1]
					gn2 = rule_11[3]
					notrule_2 = False
					if (L_sub(gn2, 1, 4) == 'not '):
						notrule_2 = True
					newconds_11 = L_T()
					newconds_11 = G['copyconds'](newconds_11, conds_9)
					for a_28, b_ in L_ipairs(isgroup):
						b_21 = b_[1]
						brec = (_t3 if L_t(_t3 := (_t4 if L_t(_t4 := b_[2]) else recursion)) else False)
						grule = b_21[1]
						gconds = b_21[2]
						if (grule[3] == gn1):
							diffname_used[i_23] = 1
							diffname_done = False
							newconds_11 = G['copyconds'](newconds_11, gconds)
							newrule_5 = L_T([grule[1], 'is', gn2])
							if (notrule_2 is False):
								L_insert(isgroup, L_T([L_T([newrule_5, newconds_11, ids_6, tags_5]), brec]))
							else:
								if (isnotgroup[grule[1]] is None):
									isnotgroup[grule[1]] = L_T()
								L_insert(isnotgroup[grule[1]], L_T([L_T([newrule_5, newconds_11, ids_6, tags_5]), brec]))
		if (evilrecursion is not None and evilrecursion is not False):
			diffname_done = False
			evilrec_id = ''
			evilrec_id_base = ''
			evilrec_memberships_base = L_T()
			evilrec_memberships_quick = L_T()
			evilrec_limit = 0
			for i_24, v_10 in L_pairs(memberships):
				evilrec_id_base = L_concat(evilrec_id_base, i_24)
				for a_29, b_22 in L_pairs(v_10):
					evilrec_id_base = L_concat(evilrec_id_base, a_29)
					if (evilrec_memberships_quick[i_24] is None):
						evilrec_memberships_quick[i_24] = L_T()
					evilrec_memberships_quick[i_24][a_29] = b_22
					if (evilrec_memberships_base[i_24] is None):
						evilrec_memberships_base[i_24] = L_T()
					evilrec_memberships_base[i_24][a_29] = b_22
			evilrec_id = evilrec_id_base
			while ((diffname_done is False) and (evilrec_limit < 10)):
				foundmembers = L_T()
				foundid = evilrec_id_base
				for i_25, v_11 in L_pairs(evilrec_memberships_base):
					foundid = L_concat(foundid, i_25)
					for a_30, b_23 in L_pairs(v_11):
						foundid = L_concat(foundid, a_30)
				for i_26, v__2 in L_ipairs(notgroupisgroup_diffname):
					v_12 = v__2[1]
					recursion_2 = (_t5 if L_t(_t5 := v__2[2]) else False)
					rule_12 = v_12[1]
					conds_10 = v_12[2]
					ids_7 = v_12[3]
					tags_6 = v_12[4]
					notrule_3 = False
					gn1_2 = L_sub(rule_12[1], 5)
					gn2_2 = rule_12[3]
					if (L_sub(gn2_2, 1, 4) == 'not '):
						notrule_3 = True
						gn2_2 = L_sub(gn2_2, 5)
					if (foundmembers[gn2_2] is None):
						foundmembers[gn2_2] = L_T()
					for a_31, b_24 in L_pairs(G['objectlist']):
						if ((G['findnoun'](a_31) is False) and ((evilrec_memberships_quick[gn1_2] is None) or ((evilrec_memberships_quick[gn1_2] is not None) and (evilrec_memberships_quick[gn1_2][a_31] is None)))):
							if (foundmembers[gn2_2][a_31] is None):
								foundmembers[gn2_2][a_31] = L_T()
							L_insert(foundmembers[gn2_2][a_31], L_T([v_12, recursion_2]))
				for i_27, v_13 in L_pairs(foundmembers):
					foundid = L_concat(foundid, i_27)
					for a_32, b_25 in L_pairs(v_13):
						foundid = L_concat(foundid, a_32)
				if (foundid == evilrec_id):
					diffname_done = True
					for i_28, v_14 in L_pairs(foundmembers):
						for a_33, d_17 in L_pairs(v_14):
							for c_19, b__2 in L_ipairs(d_17):
								b_26 = b__2[1]
								brule = b_26[1]
								rec = (_t6 if L_t(_t6 := b__2[2]) else False)
								newrule_6 = L_T([a_33, 'is', brule[3]])
								newconds_12 = L_T()
								newconds_12 = G['copyconds'](newconds_12, b_26[2])
								newids = G['concatenate'](b_26[3])
								newtags_2 = G['concatenate'](b_26[4])
								if (L_sub(brule[3], 1, 4) != 'not '):
									L_insert(isgroup, L_T([L_T([newrule_6, newconds_12, newids, newtags_2]), rec]))
								else:
									if (isnotgroup[a_33] is None):
										isnotgroup[a_33] = L_T()
									L_insert(isnotgroup[a_33], L_T([L_T([newrule_6, newconds_12, newids, newtags_2]), rec]))
				else:
					evilrec_memberships_quick = L_T()
					evilrec_id = foundid
					for i_29, v_15 in L_pairs(evilrec_memberships_base):
						evilrec_memberships_quick[i_29] = L_T()
						for a_34, b_27 in L_pairs(v_15):
							evilrec_memberships_quick[i_29][a_34] = b_27
					for i_30, v_16 in L_pairs(foundmembers):
						evilrec_memberships_quick[i_30] = L_T()
						for a_35, b_28 in L_pairs(v_16):
							evilrec_memberships_quick[i_30][a_35] = b_28
					evilrec_limit = (evilrec_limit + 1)
			if (evilrec_limit >= 10):
				G['HACK_INFINITY'] = 200
				G['destroylevel']('infinity')
				return None
		memberships = L_T()
		for i_31, v__3 in L_ipairs(isgroup):
			v_17 = v__3[1]
			recursion_3 = (_t7 if L_t(_t7 := v__3[2]) else False)
			rule_13 = v_17[1]
			conds_11 = v_17[2]
			ids_8 = v_17[3]
			tags_7 = v_17[4]
			name_ = rule_13[1]
			namelist = L_T()
			if (L_sub(name_, 1, 4) != 'not '):
				namelist = L_T([name_])
			elif (name_ != 'not all'):
				for a_36, b_29 in L_pairs(G['objectlist']):
					if ((G['findnoun'](a_36) is False) and (a_36 != L_sub(name_, 5))):
						L_insert(namelist, a_36)
			for index_2, name_2 in L_ipairs(namelist):
				never = False
				prevents = L_T()
				if (isnotgroup[name_2] is not None):
					for a_37, b__3 in L_ipairs(isnotgroup[name_2]):
						b_30 = b__3[1]
						brule_2 = b_30[1]
						grouptype = L_sub(brule_2[3], 5)
						if (grouptype == rule_13[3]):
							recursion_3 = (_t8 if L_t(_t8 := b__3[2]) else recursion_3)
							pconds_4, crashy_2, neverfound = L_adjust((*G['invertconds'](b_30[2]),), 3)
							if (neverfound is False):
								for a_38, cond_5 in L_ipairs(pconds_4):
									L_insert(prevents, cond_5)
							else:
								never = True
								break
				if (never is False):
					fconds = L_T()
					fconds = G['copyconds'](fconds, conds_11)
					fconds = G['copyconds'](fconds, prevents)
					L_insert(G['groupmembers'], L_T([name_2, fconds, rule_13[3], recursion_3]))
					if (groupmembers_quick[L_concat(name_2, '_', rule_13[3])] is None):
						groupmembers_quick[L_concat(name_2, '_', rule_13[3])] = L_T()
					L_insert(groupmembers_quick[L_concat(name_2, '_', rule_13[3])], L_T([name_2, fconds, rule_13[3], recursion_3]))
					if (memberships[rule_13[3]] is None):
						memberships[rule_13[3]] = L_T()
					L_insert(memberships[rule_13[3]], L_T([name_2, fconds]))
					for a_39, b__4 in L_ipairs(groupx):
						b_31 = b__4[1]
						recursion_3 = (_t9 if L_t(_t9 := b__4[2]) else recursion_3)
						grule_2 = b_31[1]
						gconds_2 = b_31[2]
						gids = b_31[3]
						gtags = b_31[4]
						if (grule_2[1] == rule_13[3]):
							newrule_7 = L_T([name_2, grule_2[2], grule_2[3]])
							newconds_13 = L_T()
							newids_2 = G['concatenate'](ids_8, gids)
							newtags_3 = G['concatenate'](tags_7, gtags)
							newconds_13 = G['copyconds'](newconds_13, conds_11)
							newconds_13 = G['copyconds'](newconds_13, gconds_2)
							if (L_len(prevents) == 0):
								L_insert(combined, L_T([newrule_7, newconds_13, newids_2, newtags_3]))
							else:
								newconds_13 = G['copyconds'](newconds_13, prevents)
								L_insert(combined, L_T([newrule_7, newconds_13, newids_2, newtags_3]))
		for i_32, v__4 in L_ipairs(groupxgroup):
			v_18 = v__4[1]
			recursion_4 = (_t10 if L_t(_t10 := v__4[2]) else False)
			rule_14 = v_18[1]
			conds_12 = v_18[2]
			ids_9 = v_18[3]
			tags_8 = v_18[4]
			gn1_3 = rule_14[1]
			gn2_3 = rule_14[3]
			never_2 = False
			notrule_4 = False
			if (L_sub(gn1_3, 1, 4) == 'not '):
				notrule_4 = True
				gn1_3 = L_sub(gn1_3, 5)
			prevents_2 = L_T()
			if (xnotgroup[gn1_3] is not None):
				for a_40, b__5 in L_ipairs(xnotgroup[gn1_3]):
					b_32 = b__5[1]
					brule_3 = b_32[1]
					if (((brule_3[1] == rule_14[1]) and (brule_3[2] == rule_14[2])) and (brule_3[3] == L_concat('not ', rule_14[3]))):
						recursion_4 = (_t11 if L_t(_t11 := b__5[2]) else recursion_4)
						pconds_5, crashy_3, neverfound_2 = L_adjust((*G['invertconds'](b_32[2]),), 3)
						if (neverfound_2 is False):
							for a_41, cond_6 in L_ipairs(pconds_5):
								L_insert(prevents_2, cond_6)
						else:
							never_2 = True
							break
			if (never_2 is False):
				team1 = L_T()
				team2 = L_T()
				if (notrule_4 is False):
					if (memberships[gn1_3] is not None):
						for a_42, b_33 in L_ipairs(memberships[gn1_3]):
							L_insert(team1, b_33)
				else:
					ignorethese = L_T()
					if (memberships[gn1_3] is not None):
						for a_43, b_34 in L_ipairs(memberships[gn1_3]):
							ignorethese[b_34[1]] = 1
							iconds, icrash, inever = L_adjust((*G['invertconds'](b_34[2]),), 3)
							if (inever is False):
								L_insert(team1, L_T([b_34[1], iconds]))
					for a_44, b_35 in L_pairs(G['objectlist']):
						if ((G['findnoun'](a_44) is False) and (ignorethese[a_44] is None)):
							L_insert(team1, L_T([a_44]))
				if (memberships[gn2_3] is not None):
					for a_45, b_36 in L_ipairs(memberships[gn2_3]):
						L_insert(team2, b_36)
				for a_46, b_37 in L_ipairs(team1):
					for c_20, d_18 in L_ipairs(team2):
						newrule_8 = L_T([b_37[1], rule_14[2], d_18[1]])
						newconds_14 = L_T()
						newconds_14 = G['copyconds'](newconds_14, conds_12)
						if (b_37[2] is not None):
							newconds_14 = G['copyconds'](newconds_14, b_37[2])
						if (d_18[2] is not None):
							newconds_14 = G['copyconds'](newconds_14, d_18[2])
						if (L_len(prevents_2) > 0):
							newconds_14 = G['copyconds'](newconds_14, prevents_2)
						newids_3 = G['concatenate'](ids_9)
						newtags_4 = G['concatenate'](tags_8)
						L_insert(combined, L_T([newrule_8, newconds_14, newids_3, newtags_4]))
		if (L_len(notgroupx) > 0):
			for name_3, v_19 in L_pairs(G['objectlist']):
				if (G['findnoun'](name_3) is False):
					for a_47, b__6 in L_ipairs(notgroupx):
						b_38 = b__6[1]
						recursion_5 = (_t12 if L_t(_t12 := b__6[2]) else False)
						rule_15 = b_38[1]
						conds_13 = b_38[2]
						ids_10 = b_38[3]
						tags_9 = b_38[4]
						newconds_15 = L_T()
						newconds_15 = G['copyconds'](newconds_15, conds_13)
						groupname = L_sub(rule_15[1], 5)
						valid_6 = True
						if (groupmembers_quick[L_concat(name_3, '_', groupname)] is not None):
							for c_21, d_19 in L_ipairs(groupmembers_quick[L_concat(name_3, '_', groupname)]):
								recursion_5 = (_t13 if L_t(_t13 := d_19[4]) else recursion_5)
								iconds_2, icrash_2, inever_2 = L_adjust((*G['invertconds'](d_19[2]),), 3)
								newconds_15 = G['copyconds'](newconds_15, iconds_2)
								if (inever_2 is not None and inever_2 is not False):
									valid_6 = False
									break
						if (valid_6 is not None and valid_6 is not False):
							newrule_9 = L_T([name_3, rule_15[2], rule_15[3]])
							newids_4 = L_T()
							newtags_5 = L_T()
							newids_4 = G['concatenate'](newids_4, ids_10)
							newtags_5 = G['concatenate'](newtags_5, tags_9)
							L_insert(combined, L_T([newrule_9, newconds_15, newids_4, newtags_5]))
		for i_33, v__5 in L_ipairs(xgroup):
			v_20 = v__5[1]
			recursion_6 = (_t14 if L_t(_t14 := v__5[2]) else False)
			rule_16 = v_20[1]
			conds_14 = v_20[2]
			ids_11 = v_20[3]
			tags_10 = v_20[4]
			if (((L_sub(rule_16[1], 1, 5) != 'group') and (L_sub(rule_16[1], 1, 9) != 'not group')) and (rule_16[2] != 'is')):
				team2_2 = L_T()
				if (memberships[rule_16[3]] is not None):
					for a_48, b_39 in L_ipairs(memberships[rule_16[3]]):
						L_insert(team2_2, b_39)
				for a_49, b_40 in L_ipairs(team2_2):
					newrule_10 = L_T([rule_16[1], rule_16[2], b_40[1]])
					newconds_16 = L_T()
					newconds_16 = G['copyconds'](newconds_16, conds_14)
					if (b_40[2] is not None):
						newconds_16 = G['copyconds'](newconds_16, b_40[2])
					newids_5 = G['concatenate'](ids_11)
					newtags_6 = G['concatenate'](tags_10)
					L_insert(combined, L_T([newrule_10, newconds_16, newids_5, newtags_6]))
		for i_34, k_3 in L_pairs(xnotgroup):
			for c_22, v__6 in L_ipairs(k_3):
				v_21 = v__6[1]
				recursion_7 = (_t15 if L_t(_t15 := v__6[2]) else False)
				rule_17 = v_21[1]
				conds_15 = v_21[2]
				ids_12 = v_21[3]
				tags_11 = v_21[4]
				if (((L_sub(rule_17[1], 1, 5) != 'group') and (L_sub(rule_17[1], 1, 9) != 'not group')) and (rule_17[2] != 'is')):
					team2_3 = L_T()
					gn2_4 = L_sub(rule_17[3], 5)
					if (memberships[gn2_4] is not None):
						for a_50, b_41 in L_ipairs(memberships[gn2_4]):
							L_insert(team2_3, b_41)
					for a_51, b_42 in L_ipairs(team2_3):
						newrule_11 = L_T([rule_17[1], rule_17[2], L_concat('not ', b_42[1])])
						newconds_17 = L_T()
						newconds_17 = G['copyconds'](newconds_17, conds_15)
						if (b_42[2] is not None):
							newconds_17 = G['copyconds'](newconds_17, b_42[2])
						newids_6 = G['concatenate'](ids_12)
						newtags_7 = G['concatenate'](tags_11)
						L_insert(combined, L_T([newrule_11, newconds_17, newids_6, newtags_7]))
		for i_35, v__7 in L_ipairs(groupisnotgroup):
			v_22 = v__7[1]
			recursion_8 = (_t16 if L_t(_t16 := v__7[2]) else False)
			rule_18 = v_22[1]
			conds_16 = v_22[2]
			ids_13 = v_22[3]
			tags_12 = v_22[4]
			team1_2 = L_T()
			if (memberships[rule_18[1]] is not None):
				for a_52, b_43 in L_ipairs(memberships[rule_18[1]]):
					L_insert(team1_2, b_43)
			for a_53, b_44 in L_ipairs(team1_2):
				newrule_12 = L_T([b_44[1], 'is', 'crash'])
				newconds_18 = L_T()
				newconds_18 = G['copyconds'](newconds_18, conds_16)
				if (b_44[2] is not None):
					newconds_18 = G['copyconds'](newconds_18, b_44[2])
				newids_7 = G['concatenate'](ids_13)
				newtags_8 = G['concatenate'](tags_12)
				L_insert(combined, L_T([newrule_12, newconds_18, newids_7, newtags_8]))
		for i_36, v__8 in L_ipairs(notgroupisgroup):
			v_23 = v__8[1]
			recursion_9 = (_t17 if L_t(_t17 := v__8[2]) else False)
			rule_19 = v_23[1]
			conds_17 = v_23[2]
			ids_14 = v_23[3]
			tags_13 = v_23[4]
			team1_3 = L_T()
			gn1_4 = L_sub(rule_19[1], 5)
			ignorethese_2 = L_T()
			if (memberships[gn1_4] is not None):
				for a_54, b_45 in L_ipairs(memberships[gn1_4]):
					ignorethese_2[b_45[1]] = 1
					iconds_3, icrash_3, inever_3 = L_adjust((*G['invertconds'](b_45[2]),), 3)
					if (inever_3 is False):
						L_insert(team1_3, L_T([b_45[1], iconds_3]))
			for a_55, b_46 in L_pairs(G['objectlist']):
				if ((G['findnoun'](a_55) is False) and (ignorethese_2[a_55] is None)):
					L_insert(team1_3, L_T([a_55]))
			for a_56, b_47 in L_ipairs(team1_3):
				newrule_13 = L_T([b_47[1], 'is', 'crash'])
				newconds_19 = L_T()
				newconds_19 = G['copyconds'](newconds_19, conds_17)
				if (b_47[2] is not None):
					newconds_19 = G['copyconds'](newconds_19, b_47[2])
				newids_8 = G['concatenate'](ids_14)
				newtags_9 = G['concatenate'](tags_13)
				L_insert(combined, L_T([newrule_13, newconds_19, newids_8, newtags_9]))
		for i_37, v_24 in L_ipairs(combined):
			G['addoption'](v_24[1], v_24[2], v_24[3], False, None, v_24[4])
	G['grouprules'] = f_grouprules
	def f_copyrule(rule_20=None, *_):  # L2319
		baserule_2 = rule_20[1]
		conds_18 = rule_20[2]
		ids_15 = rule_20[3]
		tags_14 = rule_20[4]
		newbaserule_2 = L_T()
		newconds_20 = L_T()
		newids_9 = L_T()
		newtags_10 = L_T()
		newbaserule_2 = L_T([baserule_2[1], baserule_2[2], baserule_2[3]])
		if (L_len(conds_18) > 0):
			for i_38, cond_7 in L_ipairs(conds_18):
				newcond = L_T([cond_7[1]])
				if (cond_7[2] is not None):
					condnames = cond_7[2]
					newcond[2] = L_T()
					for a_57, b_48 in L_ipairs(condnames):
						L_insert(newcond[2], b_48)
				L_insert(newconds_20, newcond)
		if (L_len(ids_15) > 0):
			for i_39, id_ in L_ipairs(ids_15):
				iid_3 = L_T()
				for a_58, b_49 in L_ipairs(id_):
					L_insert(iid_3, b_49)
				L_insert(newids_9, iid_3)
		if (L_len(tags_14) > 0):
			for i_40, tag in L_ipairs(tags_14):
				L_insert(newtags_10, tag)
		newrule_14 = L_T([newbaserule_2, newconds_20, newids_9, newtags_10])
		return newrule_14
	G['copyrule'] = f_copyrule
	def f_comparerules(baserule1=None, baserule2=None, *_):  # L2372
		same_3 = True
		for i_41, v_25 in L_ipairs(baserule1):
			if (v_25 != baserule2[i_41]):
				same_3 = False
		return same_3
	G['comparerules'] = f_comparerules
	def f_findwordunits(*_):  # L2384
		result_2 = L_T()
		alreadydone = L_T()
		checkrecursion = L_T()
		related = L_T()
		identifier = ''
		fullid = L_T()
		if (G['featureindex']['word'] is not None):
			for i_42, v_26 in L_ipairs(G['featureindex']['word']):
				rule_21 = v_26[1]
				conds_19 = v_26[2]
				ids_16 = v_26[3]
				name_4 = rule_21[1]
				subid = ''
				if (rule_21[2] == 'is'):
					if (((G['objectlist'][name_4] is not None) and (name_4 != 'text')) and (alreadydone[name_4] is None)):
						these = G['findall'](L_T([name_4, L_T()]))
						alreadydone[name_4] = 1
						if (L_len(these) > 0):
							for a_59, b_50 in L_ipairs(these):
								bunit_2 = G['mmf']['newObject'](b_50)
								valid_7 = True
								if (G['featureindex']['broken'] is not None):
									if (G['hasfeature'](G['getname'](bunit_2), 'is', 'broken', b_50, bunit_2['values'][G['XPOS']], bunit_2['values'][G['YPOS']]) is not None):
										valid_7 = False
								if (valid_7 is not None and valid_7 is not False):
									L_insert(result_2, L_T([b_50, conds_19]))
									subid = L_concat(subid, name_4)
					if (L_len(subid) > 0):
						for a_60, b_51 in L_ipairs(conds_19):
							condtype = b_51[1]
							params_2 = (_t1 if L_t(_t1 := b_51[2]) else L_T())
							subid = L_concat(subid, condtype)
							if (L_len(params_2) > 0):
								for c_23, d_20 in L_ipairs(params_2):
									subid = L_concat(subid, L_tostring(d_20))
									related = G['findunits'](d_20, related, conds_19)
					L_insert(fullid, subid)
					if (L_len(ids_16) > 0):
						if (L_len(ids_16[1]) == 1):
							firstunit = G['mmf']['newObject'](ids_16[1][1])
							notname = name_4
							if (L_sub(name_4, 1, 4) == 'not '):
								notname = L_sub(name_4, 5)
							if ((firstunit['strings'][G['UNITNAME']] != L_concat('text_', name_4)) and (firstunit['strings'][G['UNITNAME']] != L_concat('text_', notname))):
								L_insert(checkrecursion, L_T([name_4, i_42]))
					else:
						G['MF_alert']('No ids listed in Word-related rule! rules.lua line 1302 - this needs fixing asap (related to grouprules line 1118)')
			L_sort(fullid)
			for i_43, v_27 in L_ipairs(fullid):
				identifier = L_concat(identifier, v_27)
			for a_61, checkname_ in L_ipairs(checkrecursion):
				found = False
				checkname = checkname_[1]
				b_52 = checkname
				if (L_sub(b_52, 1, 4) == 'not '):
					b_52 = L_sub(checkname, 5)
				for i_44, v_28 in L_ipairs(G['featureindex']['word']):
					rule_22 = v_28[1]
					ids_17 = v_28[3]
					tags_15 = v_28[4]
					if (((rule_22[1] == b_52) or (rule_22[1] == 'all')) or ((rule_22[1] != b_52) and (L_sub(rule_22[1], 1, 3) == 'not'))):
						for c_24, g_5 in L_ipairs(ids_17):
							for a_62, d_21 in L_ipairs(g_5):
								idunit = G['mmf']['newObject'](d_21)
								if ((idunit['strings'][G['UNITNAME']] == L_concat('text_', rule_22[1])) or (rule_22[1] == 'all')):
									found = True
								elif (L_sub(rule_22[1], 1, 5) == 'group'):
									found = True
								elif ((rule_22[1] != checkname) and (L_sub(rule_22[1], 1, 3) == 'not')):
									found = True
						for c_25, g_6 in L_ipairs(tags_15):
							if (g_6 == 'mimic'):
								found = True
				if (found is False):
					identifier = 'null'
					G['wordunits'] = L_T()
					for i_45, v_29 in L_pairs(G['featureindex']['word']):
						rule_23 = v_29[1]
						ids_18 = v_29[3]
						if ((rule_23[1] == b_52) or (rule_23[1] == L_concat('not ', b_52))):
							v_29[2] = L_T([L_T(['never', L_T()])])
					if (L_sub(checkname, 1, 4) == 'not '):
						notrules_word = G['notfeatures']['word']
						notrules_id = checkname_[2]
						disablethese = notrules_word[notrules_id]
						for i_46, v_30 in L_ipairs(disablethese):
							v_30[2] = L_T([L_T(['never', L_T()])])
		return (result_2, identifier, related,)
		return ()
	G['findwordunits'] = f_findwordunits
	def f_ruleblockeffect(*_):  # L2552
		handled = L_T()
		for i_47, rules_6 in L_pairs(G['features']):
			rule_24 = rules_6[1]
			conds_20 = rules_6[2]
			ids_19 = rules_6[3]
			blocked = False
			for a_63, b_53 in L_ipairs(conds_20):
				if (b_53[1] == 'never'):
					blocked = True
					break
			if (blocked is not None and blocked is not False):
				for a_64, d_22 in L_ipairs(ids_19):
					for c_26, b_54 in L_ipairs(d_22):
						if (handled[b_54] is None):
							runit = G['mmf']['newObject'](b_54)
							blockid = G['MF_create']('Ingame_blocked')
							bunit_3 = G['mmf']['newObject'](blockid)
							bunit_3['x'] = runit['x']
							bunit_3['y'] = runit['y']
							bunit_3['values'][G['XPOS']] = runit['values'][G['XPOS']]
							bunit_3['values'][G['YPOS']] = runit['values'][G['YPOS']]
							bunit_3['layer'] = 1
							bunit_3['values'][G['ZLAYER']] = 20
							bunit_3['values'][G['TYPE']] = b_54
							bunit_3['scaleX'] = (G['spritedata']['values'][G['TILEMULT']] * G['generaldata2']['values'][G['ZOOM']])
							bunit_3['scaleY'] = (G['spritedata']['values'][G['TILEMULT']] * G['generaldata2']['values'][G['ZOOM']])
							bunit_3['visible'] = runit['visible']
							c1_2, c2_2 = L_adjust((*G['getuicolour']('blocked'),), 2)
							G['MF_setcolour'](blockid, c1_2, c2_2)
							handled[b_54] = 2
			else:
				for a_65, d_23 in L_ipairs(ids_19):
					for c_27, b_55 in L_ipairs(d_23):
						if (handled[b_55] is None):
							handled[b_55] = 1
						elif (handled[b_55] == 2):
							G['MF_removeblockeffect'](b_55)
	G['ruleblockeffect'] = f_ruleblockeffect
	def f_getsentencevariant(sentences_2=None, combo=None, *_):  # L2614
		result_3 = L_T()
		for i_48, words in L_ipairs(sentences_2):
			currcombo = combo[i_48]
			current_2 = words[currcombo]
			L_insert(result_3, current_2)
		return result_3
	G['getsentencevariant'] = f_getsentencevariant
	def f_addbaserule(rule1=None, rule2=None, rule3=None, conds__2=None, *_):  # L2628
		if (G['featureindex'][rule1] is None):
			G['featureindex'][rule1] = L_T()
		if (G['featureindex'][rule2] is None):
			G['featureindex'][rule2] = L_T()
		if (G['featureindex'][rule3] is None):
			G['featureindex'][rule3] = L_T()
		conds_21 = (_t1 if L_t(_t1 := conds__2) else L_T())
		rule_25 = L_T([rule1, rule2, rule3])
		fullrule = L_T([rule_25, conds_21, L_T(), L_T(['base'])])
		L_insert(G['features'], fullrule)
		L_insert(G['featureindex'][rule1], fullrule)
		L_insert(G['featureindex'][rule2], fullrule)
		L_insert(G['featureindex'][rule3], fullrule)
	G['addbaserule'] = f_addbaserule
	def f_calculatesentences(unitid_5=None, x_6=None, y_6=None, dir__3=None, *_):  # L2652
		drs_4 = G['dirs'][dir__3]
		ox_4, oy_4 = drs_4[1], drs_4[2]
		finals_2 = L_T()
		sentences_3 = L_T()
		sentence_ids = L_T()
		firstwords_3 = L_T()
		sents = L_T()
		done = False
		verbfound = False
		objfound = False
		starting = True
		step = 0
		rstep = 0
		combo_2 = L_T()
		variantshere = L_T()
		totalvariants = 1
		maxpos = 0
		prevsharedtype = (-1)
		prevmaxw = 1
		currw = 0
		limiter_3 = 5000
		combospots = L_T()
		unit_5 = G['mmf']['newObject'](unitid_5)
		done_2 = False
		while ((done_2 is False) and (totalvariants < limiter_3)):
			words_2, letters_2, jletters = L_adjust((*G['codecheck'](unitid_5, (ox_4 * rstep), (oy_4 * rstep), dir__3, True),), 3)
			step = (step + 1)
			rstep = (rstep + 1)
			if (totalvariants >= limiter_3):
				G['MF_alert']('Level destroyed - too many variants A')
				G['destroylevel']('toocomplex')
				return (None,)
			if (totalvariants < limiter_3):
				sharedtype = (-1)
				maxw = 1
				if (L_len(words_2) > 0):
					sents[step] = L_T()
					for i_49, v_31 in L_ipairs(words_2):
						if (sharedtype == (-1)):
							sharedtype = v_31[4]
						elif (v_31[4] != sharedtype):
							sharedtype = (-2)
						if (v_31[4] == 1):
							verbfound = True
						if (v_31[4] == 0):
							objfound = True
						if ((starting is not None and starting is not False) and (((v_31[4] == 0) or (v_31[4] == 3)) or (v_31[4] == 4))):
							starting = False
						maxw = L_max(maxw, v_31[2])
						L_insert(sents[step], v_31)
						if (v_31[2] > 1):
							currw = L_max(currw, (v_31[2] + 1))
					if ((((((sharedtype >= 0) and (prevsharedtype >= 0)) and (L_len(words_2) > 0)) and (maxw == 1)) and (prevmaxw == 1)) and (currw == 0)):
						if (((((sharedtype == 0) and (prevsharedtype == 0)) or ((sharedtype == 1) and (prevsharedtype == 1))) or ((sharedtype == 2) and (prevsharedtype == 2))) or ((sharedtype == 0) and (prevsharedtype == 2))):
							done_2 = True
							sents[step] = None
							L_insert(firstwords_3, L_T([words_2[1][1], dir__3, words_2[1][2], words_2[1][3], words_2[1][4], L_T()]))
					currw = L_max((currw - 1), 0)
					prevsharedtype = sharedtype
					prevmaxw = maxw
					if (done_2 is False):
						if (starting is not None and starting is not False):
							sents[step] = None
							step = (step - 1)
						else:
							totalvariants = (totalvariants * L_len(words_2))
							variantshere[step] = L_len(words_2)
							combo_2[step] = 1
							if (totalvariants >= limiter_3):
								G['MF_alert']('Level destroyed - too many variants B')
								G['destroylevel']('toocomplex')
								return (None,)
							if (L_len(words_2) > 1):
								combospots[(L_len(combospots) + 1)] = step
							if (totalvariants > L_len(finals_2)):
								limitdiff = (totalvariants - L_len(finals_2))
								for i_50 in L_range(1, limitdiff):
									L_insert(finals_2, L_T())
				else:
					if (jletters is not None and jletters is not False):
						variantshere[step] = 0
						sents[step] = L_T()
						combo_2[step] = 0
						if (starting is not None and starting is not False):
							sents[step] = None
							step = (step - 1)
					else:
						done_2 = True
		if (totalvariants >= limiter_3):
			G['MF_alert']('Level destroyed - too many variants C')
			G['destroylevel']('toocomplex')
			return (None,)
		if (((verbfound is False) or (step < 3)) or (objfound is False)):
			return (L_T(), L_T(), 0, 0, L_T(), firstwords_3,)
		maxpos = step
		combostep = 0
		for i_51 in L_range(1, totalvariants):
			step = 1
			sentences_3[i_51] = L_T()
			sentence_ids[i_51] = ''
			while (step < maxpos):
				c_28 = combo_2[step]
				if (c_28 is not None):
					if (c_28 > 0):
						s_2 = sents[step]
						word_4 = s_2[c_28]
						w_2 = word_4[2]
						L_insert(sentences_3[i_51], L_T([word_4[3], word_4[4], word_4[1], word_4[2]]))
						sentence_ids[i_51] = L_concat(sentence_ids[i_51], L_tostring((c_28 - 1)))
						step = (step + w_2)
					else:
						break
				else:
					G['MF_alert'](L_concat('c is nil, ', L_tostring(step)))
					break
			if (L_len(combospots) > 0):
				combostep = 0
				targetstep = combospots[(combostep + 1)]
				combo_2[targetstep] = (combo_2[targetstep] + 1)
				while (combo_2[targetstep] > variantshere[targetstep]):
					combo_2[targetstep] = 1
					combostep = ((combostep + 1) % L_len(combospots))
					targetstep = combospots[(combostep + 1)]
					combo_2[targetstep] = (combo_2[targetstep] + 1)
		return (sentences_3, finals_2, maxpos, totalvariants, sentence_ids, firstwords_3,)
		return ()
	G['calculatesentences'] = f_calculatesentences
	def f_invertconds(conds_22=None, db=None, target_=None, *_):  # L2877
		newconds_21 = (_t1 if L_t(_t1 := db) else L_T())
		crash = False
		doparentheses = True
		neverfound_3 = False
		if (L_len(conds_22) > 0):
			for a_66, cond_8 in L_ipairs(conds_22):
				newcond_2 = L_T()
				condname_2 = cond_8[1]
				condname_s = ''
				params_3 = cond_8[2]
				prefix_2 = L_sub(condname_2, 1, 4)
				if (prefix_2 == '(not'):
					condname_s = L_sub(condname_2, 6)
					condname_2 = L_sub(condname_2, 6)
				elif (prefix_2 == 'not '):
					condname_s = L_sub(condname_2, 5)
					condname_2 = L_sub(condname_2, 5)
				else:
					condname_s = condname_2
					condname_2 = L_concat('not ', condname_2)
				newcond_2[1] = condname_2
				newcond_2[2] = L_T()
				valid_8 = True
				if (L_len(params_3) > 0):
					for m_2, n in L_ipairs(params_3):
						if (condname_s != 'feeling'):
							L_insert(newcond_2[2], n)
						else:
							if ((target_ is None) or (target_ != L_concat('not ', n))):
								L_insert(newcond_2[2], n)
							elif (cond_8[1] == 'feeling'):
								crash = True
				if ((L_len(params_3) > 0) and (L_len(newcond_2[2]) == 0)):
					valid_8 = False
				if (valid_8 is not None and valid_8 is not False):
					L_insert(newconds_21, newcond_2)
		else:
			L_insert(newconds_21, L_T(['never', L_T()]))
			doparentheses = False
			neverfound_3 = True
		if (doparentheses is not None and doparentheses is not False):
			for i_52, cond_9 in L_ipairs(newconds_21):
				if (i_52 == 1):
					cond_9[1] = L_concat('(', cond_9[1])
				if (i_52 == L_len(newconds_21)):
					cond_9[1] = L_concat(cond_9[1], ')')
		return (newconds_21, crash, neverfound_3,)
		return ()
	G['invertconds'] = f_invertconds
	def f_rulelog(sent_3=None, text=None, *_):  # L2951
		wdata_2 = sent_3[1]
		wids = wdata_2[3]
		unitid_6 = wids[1]
		x_7, y_7 = 0, 0
		if (unitid_6 is not None):
			unit_6 = G['mmf']['newObject'](unitid_6)
			x_7 = unit_6['values'][G['XPOS']]
			y_7 = unit_6['values'][G['YPOS']]
		bundle = L_T([x_7, y_7, text])
		L_insert(G['logrulelist']['new'], bundle)
	G['rulelog'] = f_rulelog
	def f_updatelogrules(*_):  # L2967
		checklist1 = L_T()
		checklist2 = L_T()
		newrules = L_T()
		gonerules = L_T()
		if (((G['logrulelist'] is not None) and (G['logrulelist']['new'] is not None)) and (G['logrulelist']['old'] is not None)):
			if (G['generaldata']['values'][G['UPDATE']] < 2):
				for i_53, v_32 in L_ipairs(G['logrulelist']['old']):
					id__2 = v_32[3]
					checklist1[id__2] = 1
				for i_54, v_33 in L_ipairs(G['logrulelist']['new']):
					id__3 = v_33[3]
					checklist2[id__3] = 1
					if (checklist1[id__3] is None):
						L_insert(newrules, L_T([v_33[1], v_33[2], v_33[3]]))
				for i_55, v_34 in L_ipairs(G['logrulelist']['old']):
					id__4 = v_34[3]
					if (checklist2[id__4] is None):
						L_insert(gonerules, L_T([v_34[1], v_34[2], v_34[3]]))
				for i_56, v_35 in L_ipairs(gonerules):
					G['id'] = L_concat(L_tostring(v_35[1]), ':', L_tostring(v_35[2]), ':', L_tostring(v_35[3]))
					G['dolog']('rule_remove', 'event', G['id'])
				for i_57, v_36 in L_ipairs(newrules):
					G['id'] = L_concat(L_tostring(v_36[1]), ':', L_tostring(v_36[2]), ':', L_tostring(v_36[3]))
					G['dolog']('rule_add', 'event', G['id'])
			G['logrulelist']['old'] = L_T()
			for i_58, v_37 in L_ipairs(G['logrulelist']['new']):
				L_insert(G['logrulelist']['old'], L_T([v_37[1], v_37[2], v_37[3]]))
			G['logrulelist']['new'] = L_T()
	G['updatelogrules'] = f_updatelogrules
