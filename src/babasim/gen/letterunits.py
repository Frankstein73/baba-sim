"""Generated from letterunits.lua by tools/lua2py.py. Do not edit."""
from babasim.luart import *  # noqa: F403


def load(G):
	def f_formlettermap(*_):  # L1
		G['letterunits_map'] = L_T()
		lettermap = L_T()
		letterunitlist = L_T()
		if (L_len(G['letterunits']) > 0):
			for i, unitid in L_ipairs(G['letterunits']):
				unit = G['mmf']['newObject'](unitid)
				if ((unit['values'][G['TYPE']] == 5) and (unit['flags'][G['DEAD']] is False)):
					x, y = unit['values'][G['XPOS']], unit['values'][G['YPOS']]
					tileid = (x + (y * G['roomsizex']))
					name = L_sub(unit['strings'][G['UNITNAME']], 6)
					if (lettermap[tileid] is None):
						lettermap[tileid] = L_T()
					L_insert(lettermap[tileid], L_T([name, unitid]))
			for tileid_2, v in L_pairs(lettermap):
				x_2 = L_floor((tileid_2 % G['roomsizex']))
				y_2 = L_floor(L_div(tileid_2, G['roomsizex']))
				ux, uy = x_2, (y_2 - 1)
				lx, ly = (x_2 - 1), y_2
				dx, dy = x_2, (y_2 + 1)
				rx, ry = (x_2 + 1), y_2
				tidr = (rx + (ry * G['roomsizex']))
				tidu = (ux + (uy * G['roomsizex']))
				tidl = (lx + (ly * G['roomsizex']))
				tidd = (dx + (dy * G['roomsizex']))
				continuer = False
				continued = False
				if (lettermap[tidr] is not None):
					continuer = True
				if (lettermap[tidd] is not None):
					continued = True
				if (L_len(G['cobjects']) > 0):
					for a, b in L_ipairs(v):
						n = b[1]
						if (G['cobjects'][n] is not None):
							continuer = True
							continued = True
							break
				if ((lettermap[tidl] is None) and (continuer is not None and continuer is not False)):
					letterunitlist = G['formletterunits'](x_2, y_2, lettermap, 1, letterunitlist)
				if ((lettermap[tidu] is None) and (continued is not None and continued is not False)):
					letterunitlist = G['formletterunits'](x_2, y_2, lettermap, 2, letterunitlist)
			if (G['unitreference']['text_play'] is not None):
				letterunitlist = G['cullnotes'](letterunitlist)
			for i_2, v_2 in L_ipairs(letterunitlist):
				x_3 = v_2[3]
				y_3 = v_2[4]
				w = v_2[6]
				dir_ = v_2[5]
				dr = G['dirs'][dir_]
				ox, oy = dr[1], dr[2]
				tileid_3 = (x_3 + (y_3 * G['roomsizex']))
				if (G['letterunits_map'][tileid_3] is None):
					G['letterunits_map'][tileid_3] = L_T()
				L_insert(G['letterunits_map'][tileid_3], L_T([v_2[1], v_2[2], v_2[3], v_2[4], v_2[5], v_2[6], v_2[7]]))
				if (w > 1):
					endtileid = ((x_3 + (ox * (w - 1))) + ((y_3 + (oy * (w - 1))) * G['roomsizex']))
					if (G['letterunits_map'][endtileid] is None):
						G['letterunits_map'][endtileid] = L_T()
					L_insert(G['letterunits_map'][endtileid], L_T([v_2[1], v_2[2], v_2[3], v_2[4], v_2[5], v_2[6], v_2[7]]))
	G['formlettermap'] = f_formlettermap
	def f_cullnotes(database_=None, *_):  # L109
		database = database_
		freqs = G['play_data']['freqs']
		comparison = L_T()
		delthese = L_T()
		specialcases = L_T([], {'bsharp': 1, 'esharp': 1, 'cflat_': 1, 'fflat_': 1})
		for i_3, v_3 in L_ipairs(database):
			w_2 = v_3[1]
			sw = L_sub(L_concat(w_2, '_'), 1, 6)
			if ((freqs[w_2] is not None) or (specialcases[sw] is not None)):
				tileid_4 = ((v_3[3] + (v_3[4] * G['roomsizex'])) + (((v_3[5] - 1) * G['roomsizex']) * G['roomsizey']))
				if (comparison[tileid_4] is None):
					comparison[tileid_4] = L_T()
					comparison[tileid_4]['longest'] = L_len(w_2)
				comparison[tileid_4]['longest'] = L_max(L_len(w_2), comparison[tileid_4]['longest'])
				L_insert(comparison[tileid_4], L_T([L_len(w_2), i_3]))
		for i_4, v_4 in L_pairs(comparison):
			for a_2, b_2 in L_ipairs(v_4):
				if (b_2[1] < v_4['longest']):
					L_insert(delthese, b_2[2])
		L_sort(delthese)
		i_5 = L_len(delthese)
		for j in L_range(1, L_len(delthese)):
			c = delthese[i_5]
			L_remove(database, c)
			i_5 = (i_5 - 1)
		return database
	G['cullnotes'] = f_cullnotes
	def f_formletterunits(x_4=None, y_4=None, lettermap_2=None, dir__2=None, database__2=None, *_):  # L169
		dr_2 = G['dirs'][dir__2]
		ox_2, oy_2 = dr_2[1], dr_2[2]
		cx, cy = x_4, y_4
		jumble = L_T()
		jumblecombo = L_T()
		totalcombos = 1
		done = False
		database_2 = database__2
		while (done is False):
			tileid_5 = (cx + (cy * G['roomsizex']))
			if (lettermap_2[tileid_5] is not None):
				L_insert(jumble, L_T())
				cjumble = jumble[L_len(jumble)]
				for i_6, v_5 in L_ipairs(lettermap_2[tileid_5]):
					L_insert(cjumble, L_T([v_5[1], v_5[2]]))
				L_insert(jumblecombo, 0)
				totalcombos = (totalcombos * L_len(cjumble))
				cx = (cx + ox_2)
				cy = (cy + oy_2)
			else:
				done = True
		been_seen = L_T()
		if (L_len(jumble) > 0):
			for j_2 in L_range(1, totalcombos):
				word = ''
				subword = ''
				prevword = ''
				prevwordid = 0
				wordids = L_T()
				branches = L_T()
				offset = 0
				updatecombo = True
				for i_7, cjumble_2 in L_ipairs(jumble):
					ccombo = (jumblecombo[i_7] + 1)
					cword = cjumble_2[ccombo]
					word = L_concat(word, cword[1])
					L_insert(wordids, cword[2])
					if (i_7 > 1):
						subword = L_concat(prevword, cword[1])
					if (updatecombo is not None and updatecombo is not False):
						jumblecombo[i_7] = (jumblecombo[i_7] + 1)
						if (jumblecombo[i_7] >= L_len(cjumble_2)):
							jumblecombo[i_7] = 0
							updatecombo = True
						else:
							updatecombo = False
					found, fullwords, partwords = L_adjust((*G['findletterwords'](word, (i_7 - 1), subword),), 3)
					for a_3, b_3 in L_ipairs(partwords):
						L_insert(branches, L_T([prevword, (i_7 - 2), False, L_T([prevwordid])]))
					prevword = cword[1]
					prevwordid = cword[2]
					for a_4, b_4 in L_ipairs(branches):
						w_3 = b_4[1]
						pos = b_4[2]
						dead = b_4[3]
						wids = b_4[4]
						w_3 = L_concat(w_3, cword[1])
						b_4[1] = w_3
						L_insert(b_4[4], cword[2])
						if (dead is False):
							sfound, sfullwords = L_adjust((*G['findletterwords'](w_3, (i_7 - 1), None, False),), 2)
							if (sfound is False):
								b_4[3] = True
								if (L_len(b_4[4]) > 0):
									L_remove(b_4[4], L_len(b_4[4]))
							else:
								if (L_len(sfullwords) > 0):
									for c_2, d in L_ipairs(sfullwords):
										w_4 = d[1]
										t = d[2]
										wordcode = L_concat(w_4, L_tostring(pos))
										fwids = L_T()
										for c_3, d_2 in L_ipairs(b_4[4]):
											L_insert(fwids, d_2)
										if (been_seen[wordcode] is None):
											been_seen[wordcode] = 1
											L_insert(database_2, L_T([w_4, t, (x_4 + (ox_2 * pos)), (y_4 + (oy_2 * pos)), dir__2, L_len(fwids), fwids]))
					if (found is False):
						if ((L_strlen(word) > 0) and (L_len(wordids) > 0)):
							word = L_sub(word, (-1))
							wid = wordids[L_len(wordids)]
							wordids = L_T([wid])
							offset = (i_7 - 1)
					else:
						if (L_len(fullwords) > 0):
							for a_5, b_5 in L_ipairs(fullwords):
								w_5 = b_5[1]
								t_2 = b_5[2]
								pos_2 = b_5[3]
								fulloffset = (offset + pos_2)
								wordcode_2 = L_concat(w_5, L_tostring(fulloffset))
								fwids_2 = L_T()
								for c_4, d_3 in L_ipairs(wordids):
									L_insert(fwids_2, d_3)
								if (been_seen[wordcode_2] is None):
									been_seen[wordcode_2] = 1
									L_insert(database_2, L_T([w_5, t_2, (x_4 + (ox_2 * fulloffset)), (y_4 + (oy_2 * fulloffset)), dir__2, L_len(fwids_2), fwids_2]))
		return database_2
	G['formletterunits'] = f_formletterunits
	def f_findletterwords(word_=None, wordpos_=None, subword_=None, mainbranch_=None, *_):  # L330
		word_2 = word_
		subword_2 = subword_
		wordpos = (_t1 if L_t(_t1 := wordpos_) else 0)
		mainbranch = True
		found_2 = False
		foundsub = False
		fullwords_2 = L_T()
		fullwords_c = L_T()
		newbranches = L_T()
		if (mainbranch_ is not None):
			mainbranch = mainbranch_
		result = L_T()
		if (L_strlen(word_2) > 1):
			for i_8, v_6 in L_pairs(G['unitreference']):
				name_2 = i_8
				if ((L_strlen(name_2) > 5) and (L_sub(name_2, 1, 5) == 'text_')):
					name_2 = L_sub(name_2, 6)
				if ((L_strlen(word_2) <= L_strlen(name_2)) and (L_sub(name_2, 1, L_strlen(word_2)) == word_2)):
					if (L_strlen(word_2) == L_strlen(name_2)):
						L_insert(fullwords_2, L_T([name_2, 0]))
						found_2 = True
					else:
						found_2 = True
				if (((wordpos > 0) and (L_strlen(word_2) >= 2)) and (mainbranch is not None and mainbranch is not False)):
					if ((L_strlen(name_2) >= L_strlen(subword_2)) and (L_sub(name_2, 1, L_strlen(subword_2)) == subword_2)):
						L_insert(newbranches, L_T([subword_2, wordpos]))
						foundsub = True
		if (L_strlen(word_2) > 0):
			for c_5, d_4 in L_pairs(G['cobjects']):
				if ((c_5 != 1) and (L_strlen(L_tostring(c_5)) > 0)):
					name_3 = c_5
					if ((L_strlen(name_3) > 5) and (L_sub(name_3, 1, 5) == 'text_')):
						name_3 = L_sub(name_3, 6)
					if ((L_strlen(word_2) <= L_strlen(name_3)) and (L_sub(name_3, 1, L_strlen(word_2)) == word_2)):
						if (L_strlen(word_2) == L_strlen(name_3)):
							L_insert(fullwords_c, L_T([name_3, 0]))
							found_2 = True
						else:
							found_2 = True
					if (((wordpos > 0) and (L_strlen(word_2) >= 2)) and (mainbranch is not None and mainbranch is not False)):
						if ((L_strlen(name_3) >= L_strlen(subword_2)) and (L_sub(name_3, 1, L_strlen(subword_2)) == subword_2)):
							L_insert(newbranches, L_T([subword_2, wordpos]))
							foundsub = True
		if (L_strlen(word_2) <= 1):
			found_2 = True
		if (L_len(fullwords_2) > 0):
			for i_9, v_7 in L_ipairs(fullwords_2):
				text = v_7[1]
				textpos = v_7[2]
				alttext = L_concat('text_', text)
				name_base = G['unitreference'][text]
				name_general = G['objectpalette'][text]
				altname_base = G['unitreference'][alttext]
				altname_general = G['objectpalette'][alttext]
				realname = altname_general
				realname_general = name_general
				if (G['generaldata']['strings'][G['WORLD']] == G['generaldata']['strings'][G['BASEWORLD']]):
					realname = altname_base
					realname_general = name_base
				if (realname is not None):
					name_4 = L_first(G['getactualdata_objlist'](realname, 'name'))
					wtype = L_first(G['getactualdata_objlist'](realname, 'type'))
					if ((name_4 == text) or (name_4 == alttext)):
						if (wtype != 5):
							if (realname_general is not None):
								G['objectlist'][text] = 1
							elif (((text == 'all') or (text == 'empty')) and (realname is not None)):
								G['objectlist'][text] = 1
							L_insert(result, L_T([name_4, wtype, textpos]))
		if (L_len(fullwords_c) > 0):
			for i_10, v_8 in L_ipairs(fullwords_c):
				if (word_2 == v_8[1]):
					L_insert(result, L_T([v_8[1], 8, v_8[2]]))
		return (found_2, result, newbranches,)
		return ()
	G['findletterwords'] = f_findletterwords
