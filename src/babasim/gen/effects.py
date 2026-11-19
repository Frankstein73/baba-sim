"""Generated from effects.lua by tools/lua2py.py. Do not edit."""
from babasim.luart import *  # noqa: F403


def load(G):
	def f_effects(timer=None, *_):  # L1
		G['doeffect'](timer, None, 'win', 'unlock', 1, 2, 20, L_T([2, 4]))
		G['doeffect'](timer, None, 'best', 'unlock', 6, 30, 2, L_T([2, 4]))
		G['doeffect'](timer, None, 'tele', 'glow', 1, 5, 20, L_T([1, 4]))
		G['doeffect'](timer, None, 'hot', 'hot', 1, 80, 10, L_T([0, 1]))
		G['doeffect'](timer, None, 'bonus', 'bonus', 1, 2, 20, L_T([4, 1]))
		G['doeffect'](timer, None, 'wonder', 'wonder', 1, 10, 5, L_T([0, 3]))
		G['doeffect'](timer, None, 'sad', 'tear', 1, 2, 20, L_T([3, 2]))
		G['doeffect'](timer, None, 'sleep', 'sleep', 1, 2, 60, L_T([3, 2]))
		G['doeffect'](timer, None, 'broken', 'error', 3, 10, 8, L_T([2, 2]))
		G['doeffect'](timer, None, 'pet', 'pet', 1, 0, 50, L_T([3, 1]), 'nojitter', None, True)
		G['doeffect'](timer, None, 'angry', 'angry', 1, 10, 5, L_T([2, 2]))
		G['doeffect'](timer, None, 'happy', 'happy', 1, 10, 5, L_T([5, 4]))
		G['doeffect'](timer, None, 'power', 'electricity', 2, 5, 8, L_T([2, 4]))
		G['doeffect'](timer, None, 'power2', 'electricity', 2, 5, 8, L_T([5, 4]))
		G['doeffect'](timer, None, 'power3', 'electricity', 2, 5, 8, L_T([4, 4]))
		rnd = G['math']['random'](2, 4)
		G['doeffect'](timer, None, 'end', 'unlock', 1, 1, 10, L_T([1, rnd]), 'inwards')
		G['do_mod_hook']('effect_always')
	G['effects'] = f_effects
	def f_effects_decors(*_):  # L28
		G['MF_cleandecors']()
	G['effects_decors'] = f_effects_decors
	def f_shorteffectblock(*_):  # L33
		G['doshorteffect'](None, 'party', 'confetti', 6, L_T([(-20), 20]), L_T([(-25), (-10)]), L_T([L_T([1, 4]), L_T([2, 2]), L_T([2, 4]), L_T([4, 1]), L_T([5, 3])]))
		G['do_mod_hook']('effect_once')
	G['shorteffectblock'] = f_shorteffectblock
	def f_doeffect(timer_2=None, word2_=None, word3=None, particle=None, count=None, chance=None, timing=None, colour=None, specialrule_=None, layer_=None, follow_=None, *_):  # L39
		zoom = G['generaldata2']['values'][G['ZOOM']]
		specialrule = (_t1 if L_t(_t1 := specialrule_) else '')
		layer = (_t2 if L_t(_t2 := layer_) else 1)
		word2 = (_t3 if L_t(_t3 := word2_) else 'is')
		follow = (_t4 if L_t(_t4 := follow_) else False)
		if ((timer_2 % timing) == 0):
			this = G['findfeature'](None, word2, word3)
			c1 = colour[1]
			c2 = colour[2]
			if (this is not None):
				for k, v in L_ipairs(this):
					if ((v[1] != 'empty') and (v[1] != 'all')):
						these = G['findall'](v, True)
						if (L_len(these) > 0):
							for a, b in L_ipairs(these):
								unit = G['mmf']['newObject'](b)
								x, y = unit['values'][G['XPOS']], unit['values'][G['YPOS']]
								if (word3 == 'broken'):
									if (unit['strings'][G['UNITTYPE']] == 'text'):
										c1, c2 = L_adjust((*G['getcolour'](b, 'active'),), 2)
									else:
										c1, c2 = L_adjust((*G['getcolour'](b),), 2)
								if L_t(unit['visible']):
									for i in L_range(1, count):
										partid = 0
										if (chance > 1):
											if (G['math']['random'](chance) == 1):
												if (specialrule != 'nojitter'):
													partid = G['MF_particle'](particle, x, y, c1, c2, layer)
												else:
													partid = G['MF_staticparticle'](particle, x, y, c1, c2, layer)
										else:
											if (specialrule != 'nojitter'):
												partid = G['MF_particle'](particle, x, y, c1, c2, layer)
											else:
												partid = G['MF_staticparticle'](particle, x, y, c1, c2, layer)
										if (((partid is not None) and (partid != 0)) and (follow is not None and follow is not False)):
											part = G['mmf']['newObject'](partid)
											part['values'][G['FOLLOW']] = unit['fixed']
										if (((partid is not None) and (specialrule == 'inwards')) and (partid != 0)):
											part_2 = G['mmf']['newObject'](partid)
											part_2['values'][G['ONLINE']] = 2
											midx = L_floor((G['roomsizex'] * 0.5))
											midy = L_floor((G['roomsizey'] * 0.5))
											mx = ((x + 0.5) - midx)
											my = ((y + 0.5) - midy)
											dir_ = (0 - G['math']['atan2'](my, mx))
											dist = G['math']['sqrt']((L_pow(my, 2) + L_pow(mx, 2)))
											roomrad = G['math']['rad'](G['generaldata2']['values'][G['ROOMROTATION']])
											mx = (G['Xoffset'] + (((midx + ((G['math']['cos']((dir_ + roomrad)) * dist) * zoom)) * G['tilesize']) * G['spritedata']['values'][G['TILEMULT']]))
											my = (G['Yoffset'] + (((midy - ((G['math']['sin']((dir_ + roomrad)) * dist) * zoom)) * G['tilesize']) * G['spritedata']['values'][G['TILEMULT']]))
											part_2['x'] = (mx + G['math']['random']((0 - ((G['tilesize'] * 1.5) * zoom)), ((G['tilesize'] * 1.5) * zoom)))
											part_2['y'] = (my + G['math']['random']((0 - ((G['tilesize'] * 1.5) * zoom)), ((G['tilesize'] * 1.5) * zoom)))
											part_2['values'][G['XPOS']] = part_2['x']
											part_2['values'][G['YPOS']] = part_2['y']
											dir_ = (G['math']['pi'] - G['math']['atan2']((part_2['y'] - my), (part_2['x'] - mx)))
											dist = G['math']['sqrt']((L_pow((part_2['y'] - my), 2) + L_pow((part_2['x'] - mx), 2)))
											part_2['values'][G['XVEL']] = (G['math']['cos'](dir_) * (dist * 0.2))
											part_2['values'][G['YVEL']] = (0 - (G['math']['sin'](dir_) * (dist * 0.2)))
					if ((v[1] == 'empty') or (v[1] == 'level')):
						ignorebroken = False
						if (word3 == 'broken'):
							ignorebroken = True
						if ((v[1] != 'level') or ((v[1] == 'level') and L_t(G['testcond'](v[2], 1)))):
							for i_2 in L_range(1, (G['roomsizex'] - 2)):
								for j in L_range(1, (G['roomsizey'] - 2)):
									tileid = (i_2 + (j * G['roomsizex']))
									if ((G['unitmap'][tileid] is None) or ((G['unitmap'][tileid] is not None) and (L_len(G['unitmap'][tileid]) == 0))):
										if ((v[1] != 'empty') or ((v[1] == 'empty') and L_t(G['testcond'](v[2], 2, i_2, j, None, None, None, ignorebroken)))):
											partid_2 = 0
											if (chance > 1):
												if (G['math']['random'](chance) == 1):
													if (specialrule != 'nojitter'):
														partid_2 = G['MF_particle'](particle, i_2, j, c1, c2, layer)
													else:
														partid_2 = G['MF_staticparticle'](particle, i_2, j, c1, c2, layer)
											else:
												if (specialrule != 'nojitter'):
													partid_2 = G['MF_particle'](particle, i_2, j, c1, c2, layer)
												else:
													partid_2 = G['MF_staticparticle'](particle, i_2, j, c1, c2, layer)
	G['doeffect'] = f_doeffect
	def f_domaprotation(*_):  # L169
		if (G['featureindex']['level'] is not None):
			for i_3, v_2 in L_ipairs(G['featureindex']['level']):
				rule = v_2[1]
				conds = v_2[2]
				if L_t(G['testcond'](conds, 1)):
					if ((rule[1] == 'level') and (rule[2] == 'is')):
						if ((rule[3] == 'right') and (G['mapdir'] != 0)):
							G['updateundo'] = True
							G['addundo'](L_T(['maprotation', G['maprotation'], 90, 0]))
							G['addundo'](L_T(['mapdir', G['mapdir'], 0]))
							G['maprotation'] = 90
							G['mapdir'] = 0
							G['MF_levelrotation'](G['maprotation'])
						elif ((rule[3] == 'up') and (G['mapdir'] != 1)):
							G['updateundo'] = True
							G['addundo'](L_T(['maprotation', G['maprotation'], 180, 1]))
							G['addundo'](L_T(['mapdir', G['mapdir'], 1]))
							G['maprotation'] = 180
							G['mapdir'] = 1
							G['MF_levelrotation'](G['maprotation'])
						elif ((rule[3] == 'left') and (G['mapdir'] != 2)):
							G['updateundo'] = True
							G['addundo'](L_T(['maprotation', G['maprotation'], 270, 2]))
							G['addundo'](L_T(['mapdir', G['mapdir'], 2]))
							G['maprotation'] = 270
							G['mapdir'] = 2
							G['MF_levelrotation'](G['maprotation'])
						elif ((rule[3] == 'down') and (G['mapdir'] != 3)):
							G['updateundo'] = True
							G['addundo'](L_T(['maprotation', G['maprotation'], 0, 3]))
							G['addundo'](L_T(['mapdir', G['mapdir'], 3]))
							G['maprotation'] = 0
							G['mapdir'] = 3
							G['MF_levelrotation'](G['maprotation'])
	G['domaprotation'] = f_domaprotation
	def f_levelparticles(name=None, *_):  # L212
		G['backparticles'] = L_T()
		if (G['particletypes'][name] is not None):
			data = G['particletypes'][name]
			partname = (_t1 if L_t(_t1 := data['object']) else 'Level_particle')
			G['backparticles']['name'] = name
			G['backparticles']['update'] = data['update']
			if (data['customfunc'] is None):
				amount = data['amount']
				for i_4 in L_range(1, amount):
					unitid = G['MF_specialcreate'](partname)
					unit_2 = G['mmf']['newObject'](unitid)
					unit_2['values'][G['ONLINE']] = 1
					unit_2['x'] = (G['Xoffset'] + G['math']['random'](0, (G['screenw'] - 1)))
					unit_2['y'] = (G['Yoffset'] + G['math']['random'](0, (G['screenh'] - 1)))
					unit_2['layer'] = 1
					unit_2['values'][G['XPOS']] = unit_2['x']
					unit_2['values'][G['YPOS']] = unit_2['y']
					if (data['animation'] is not None):
						if (L_type(data['animation']) == 'number'):
							unit_2['direction'] = data['animation']
						elif (L_type(data['animation']) == 'table'):
							chunk = L_div(amount, L_len(data['animation']))
							which = (L_floor(L_div((i_4 - 1), chunk)) + 1)
							unit_2['direction'] = data['animation'][which]
					if (data['x_velocity'] is not None):
						unit_2['values'][G['XVEL']] = data['x_velocity']
					if (data['y_velocity'] is not None):
						unit_2['values'][G['YVEL']] = data['y_velocity']
					if (data['colour'] is not None):
						c = data['colour']
						G['MF_setcolour'](unitid, c[1], c[2])
						unit_2['strings'][G['COLOUR']] = L_concat(L_tostring(c[1]), ',', L_tostring(c[2]))
					unit_2['values'][G['DIR']] = G['math']['random'](0, 259)
					unit_2['strings'][1] = name
					if (data['extra'] is not None):
						data['extra'](unitid)
					if (((partname != 'Level_particle') and (data['add_to_list'] is not None)) and L_t(data['add_to_list'])):
						L_insert(G['backparticles'], unit_2)
			else:
				data['customfunc']()
			if (data['init_extra'] is not None):
				data['init_extra']()
		else:
			L_noop(L_concat('No particles with name ', name))
	G['levelparticles'] = f_levelparticles
	def f_backparticles_update(timer_3=None, *_):  # L284
		if (G['backparticles']['update'] is not None):
			G['backparticles']['update'](timer_3)
	G['backparticles_update'] = f_backparticles_update
	def f_dotransition(*_):  # L290
		sw = (G['screenw'] * 0.5)
		sh = (G['screenh'] * 0.5)
		mult = 1.5
		initialdistx = (sw * mult)
		initialdisty = (sh * mult)
		xpos = sw
		ypos = sh
		count_2 = 36
		increment = L_div(360, count_2)
		for i_5 in L_range(0, (count_2 - 1)):
			blobid = G['MF_specialcreate']('Transition_blob')
			blob = G['mmf']['newObject'](blobid)
			blob['values'][G['ONLINE']] = 1
			blob['values'][G['XPOS']] = (xpos + (G['math']['cos']((G['math']['rad'](increment) * i_5)) * initialdistx))
			blob['values'][G['YPOS']] = (ypos - (G['math']['sin']((G['math']['rad'](increment) * i_5)) * initialdisty))
			blob['flags'][10] = True
			G['MF_setcolour'](blobid, 1, 0)
			x_2, y_2 = blob['values'][G['XPOS']], blob['values'][G['YPOS']]
			steps = 50
			if (G['generaldata']['values'][G['FASTTRANSITION']] == 1):
				steps = 22.5
			spd = ((L_div(G['math']['sqrt']((L_pow((y_2 - sh), 2) + L_pow((x_2 - sw), 2))), steps) * 5) + G['math']['random']((-9), 7))
			dir__2 = (0 - G['math']['atan2']((ypos - y_2), (xpos - x_2)))
			blob['values'][G['XVEL']] = (G['math']['cos'](dir__2) * spd)
			blob['values'][G['YVEL']] = (0 - (G['math']['sin'](dir__2) * spd))
			blob['layer'] = 2
			blob['x'] = (-256)
			blob['y'] = (-256)
		count_2 = 12
		increment = L_div(360, count_2)
		mult = 1.8
		initialdistx = (sw * mult)
		initialdisty = (sh * mult)
		for i_6 in L_range(1, count_2):
			blobid_2 = G['MF_specialcreate']('Transition_bigblob')
			blob_2 = G['mmf']['newObject'](blobid_2)
			blob_2['values'][G['ONLINE']] = 1
			blob_2['values'][G['XPOS']] = (xpos + (G['math']['cos']((G['math']['rad'](increment) * i_6)) * initialdistx))
			blob_2['values'][G['YPOS']] = (ypos - (G['math']['sin']((G['math']['rad'](increment) * i_6)) * initialdisty))
			blob_2['flags'][10] = True
			G['MF_setcolour'](blobid_2, 1, 0)
			x_3, y_3 = blob_2['values'][G['XPOS']], blob_2['values'][G['YPOS']]
			steps_2 = 72
			if (G['generaldata']['values'][G['FASTTRANSITION']] == 1):
				steps_2 = 36
			spd_2 = (L_div(G['math']['sqrt']((L_pow((y_3 - sh), 2) + L_pow((x_3 - sw), 2))), steps_2) * 5)
			dir__3 = (0 - G['math']['atan2']((ypos - y_3), (xpos - x_3)))
			blob_2['values'][G['XVEL']] = ((G['math']['cos'](dir__3) * spd_2) * 1.01)
			blob_2['values'][G['YVEL']] = (0 - (G['math']['sin'](dir__3) * spd_2))
			blob_2['layer'] = 2
			blob_2['x'] = (-256)
			blob_2['y'] = (-256)
			blob_2['scale'] = 1.15
		count_2 = 4
		locations = L_T([L_T([(-1), (-1)]), L_T([1, (-1)]), L_T([1, 1]), L_T([(-1), 1])])
		mult = 1.8
		for i_7 in L_range(1, count_2):
			blobid_3 = G['MF_specialcreate']('Transition_bigblob')
			blob_3 = G['mmf']['newObject'](blobid_3)
			l = locations[i_7]
			lx, ly = l[1], l[2]
			blob_3['values'][G['ONLINE']] = 1
			blob_3['values'][G['XPOS']] = (sw + ((lx * sw) * mult))
			blob_3['values'][G['YPOS']] = (sh + ((ly * sh) * mult))
			blob_3['flags'][10] = True
			G['MF_setcolour'](blobid_3, 1, 0)
			x_4, y_4 = blob_3['values'][G['XPOS']], blob_3['values'][G['YPOS']]
			steps_3 = 72
			if (G['generaldata']['values'][G['FASTTRANSITION']] == 1):
				steps_3 = 36
			spd_3 = (L_div(G['math']['sqrt']((L_pow((y_4 - sh), 2) + L_pow((x_4 - sw), 2))), steps_3) * 5)
			dir__4 = (0 - G['math']['atan2']((ypos - y_4), (xpos - x_4)))
			blob_3['values'][G['XVEL']] = ((G['math']['cos'](dir__4) * spd_3) * 1.01)
			blob_3['values'][G['YVEL']] = (0 - (G['math']['sin'](dir__4) * spd_3))
			blob_3['layer'] = 2
			blob_3['x'] = (-256)
			blob_3['y'] = (-256)
			blob_3['scale'] = 1.15
	G['dotransition'] = f_dotransition
	def f_particles(name_2=None, x_5=None, y_5=None, count_3=None, colour_2=None, layer__2=None, zoom_=None, *_):  # L403
		layer_2 = (_t1 if L_t(_t1 := layer__2) else 1)
		zoom_2 = (_t2 if L_t(_t2 := zoom_) else 1)
		G['MF_particles'](name_2, x_5, y_5, count_3, colour_2[1], colour_2[2], layer_2, zoom_2)
	G['particles'] = f_particles
	def f_doparticles(name_3=None, x_6=None, y_6=None, count_4=None, c1_2=None, c2_2=None, layer__3=None, zoom__2=None, *_):  # L410
		layer_3 = (_t1 if L_t(_t1 := layer__3) else 1)
		zoom_3 = (_t2 if L_t(_t2 := zoom__2) else 1)
		ax, ay = 0, 0
		rx, ry = 0, 0
		mult_2 = 0
		if (zoom_3 == 1):
			mtx = (G['roomsizex'] * 0.5)
			mty = (G['roomsizey'] * 0.5)
			mx_2 = ((mtx * G['tilesize']) * G['spritedata']['values'][G['TILEMULT']])
			my_2 = ((mty * G['tilesize']) * G['spritedata']['values'][G['TILEMULT']])
			dx = (x_6 - (mtx - 0.5))
			dy = (y_6 - (mty - 0.5))
			dir__5 = (0 - G['math']['atan2'](dy, dx))
			dist_2 = G['math']['sqrt']((L_pow(dy, 2) + L_pow(dx, 2)))
			roomrotrad = G['math']['rad'](G['generaldata2']['values'][G['ROOMROTATION']])
			mult_2 = ((G['tilesize'] * G['spritedata']['values'][G['TILEMULT']]) * G['generaldata2']['values'][G['ZOOM']])
			ax = ((G['Xoffset'] + mx_2) + ((G['math']['cos']((dir__5 + roomrotrad)) * dist_2) * mult_2))
			ay = ((G['Yoffset'] + my_2) - ((G['math']['sin']((dir__5 + roomrotrad)) * dist_2) * mult_2))
		elif (zoom_3 == 0):
			ax = ((G['Xoffset'] + (x_6 * G['tilesize'])) + (G['tilesize'] * 0.5))
			ay = ((G['Yoffset'] + (y_6 * G['tilesize'])) + (G['tilesize'] * 0.5))
			mult_2 = G['tilesize']
		for i_8 in L_range(1, count_4):
			unitid_2 = G['MF_effectcreate'](L_concat('effect_', name_3))
			unit_3 = G['mmf']['newObject'](unitid_2)
			rx = G['math']['random']((0 - (mult_2 * 0.5)), (mult_2 * 0.5))
			ry = G['math']['random']((0 - (mult_2 * 0.5)), (mult_2 * 0.5))
			unit_3['x'] = (ax + rx)
			unit_3['y'] = (ay + ry)
			G['MF_setcolour'](unitid_2, c1_2, c2_2)
			unit_3['values'][G['XPOS']] = (-20)
			unit_3['values'][G['YPOS']] = (-20)
			unit_3['values'][24] = ax
			unit_3['values'][25] = ay
			unit_3['layer'] = layer_3
			if (zoom_3 == 1):
				unit_3['scaleX'] = (G['spritedata']['values'][G['TILEMULT']] * G['generaldata2']['values'][G['ZOOM']])
				unit_3['scaleY'] = (G['spritedata']['values'][G['TILEMULT']] * G['generaldata2']['values'][G['ZOOM']])
	G['doparticles'] = f_doparticles
	def f_adddecor(rule3=None, decor=None, *_):  # L469
		targets = L_first(G['findallfeature'](None, 'is', rule3, True))
		for i_9, unitid_3 in L_ipairs(targets):
			unit_4 = G['mmf']['newObject'](unitid_3)
			if (unit_4['strings'][G['DECOR']] != decor):
				dunitid = 0
				if (unit_4['strings'][G['DECOR']] == ''):
					dunitid = G['MF_specialcreate']('Level_decor')
				else:
					dunitid = G['MF_finddecor'](unitid_3)
				dunit = G['mmf']['newObject'](dunitid)
				dunit['values'][G['DECOR_OWNER']] = unitid_3
				dunit['values'][G['DECOR_DIR']] = unit_4['values'][G['DIR']]
				dunit['values'][G['DECOR_SET']] = 1
				unitname = unit_4['strings'][G['UNITNAME']]
				unit_4['strings'][G['DECOR']] = decor
				if (G['decor_offsets'][unitname] is not None):
					data_2 = G['decor_offsets'][unitname]
					G['MF_alert'](L_len(data_2))
					r = L_T()
					if (L_len(data_2) == 4):
						r = data_2[1]
						dunit['values'][G['DECOR_OXR']] = r[1]
						dunit['values'][G['DECOR_OYR']] = r[2]
					else:
						r = G['decor_offsets'][unitname]
						dunit['values'][G['DECOR_OXR']] = r[1]
						dunit['values'][G['DECOR_OYR']] = r[2]
					if (L_len(data_2) == 4):
						r = data_2[2]
						dunit['values'][G['DECOR_OXU']] = r[1]
						dunit['values'][G['DECOR_OYU']] = r[2]
					else:
						r = G['decor_offsets'][unitname]
						dunit['values'][G['DECOR_OXU']] = 0
						dunit['values'][G['DECOR_OYU']] = r[2]
					if (L_len(data_2) == 4):
						r = data_2[3]
						dunit['values'][G['DECOR_OXL']] = r[1]
						dunit['values'][G['DECOR_OYL']] = r[2]
					else:
						r = G['decor_offsets'][unitname]
						dunit['values'][G['DECOR_OXL']] = (0 - r[1])
						dunit['values'][G['DECOR_OYL']] = r[2]
					if (L_len(data_2) == 4):
						r = data_2[4]
						dunit['values'][G['DECOR_OXD']] = r[1]
						dunit['values'][G['DECOR_OYD']] = r[2]
					else:
						r = G['decor_offsets'][unitname]
						dunit['values'][G['DECOR_OXD']] = 0
						dunit['values'][G['DECOR_OYD']] = r[2]
	G['adddecor'] = f_adddecor
	def f_unitcoloureffect(*_):  # L544
		if (G['generaldata5']['values'][G['DISABLEBLINKING']] == 0):
			if ((G['generaldata5']['values'][G['AUTO_ON']] == 0) or (G['generaldata5']['values'][G['AUTO_DELAY']] > 10)):
				for i_10, unit_5 in L_pairs(G['units']):
					if ((unit_5['colours'] is not None) and (L_len(unit_5['colours']) > 1)):
						curr = ((unit_5['currcolour'] % L_len(unit_5['colours'])) + 1)
						c_2 = unit_5['colours'][curr]
						unit_5['currcolour'] = ((unit_5['currcolour'] + 1) % L_len(unit_5['colours']))
						unit_5['colour'] = L_T([c_2[1], c_2[2]])
						G['MF_setcolour'](unit_5['fixed'], c_2[1], c_2[2])
			if (G['generaldata5']['values'][G['AUTO_ON']] == 0):
				if ((G['leveldata']['colours'] is not None) and (L_len(G['leveldata']['colours']) > 1)):
					curr_2 = ((G['leveldata']['currcolour'] % L_len(G['leveldata']['colours'])) + 1)
					c_3 = G['leveldata']['colours'][curr_2]
					G['leveldata']['currcolour'] = ((G['leveldata']['currcolour'] + 1) % L_len(G['leveldata']['colours']))
					if ((c_3[1] == 0) and (c_3[2] == 4)):
						G['MF_backcolour'](c_3[1], c_3[2])
					else:
						G['MF_backcolour_dim'](c_3[1], c_3[2])
	G['unitcoloureffect'] = f_unitcoloureffect
	def f_doshorteffect(word2__2=None, word3_2=None, particle_2=None, count_5=None, xvel_=None, yvel_=None, colours=None, layer__4=None, *_):  # L575
		xvel = 0
		yvel = 0
		c1_3, c2_3 = 0, 3
		layer_4 = (_t1 if L_t(_t1 := layer__4) else 1)
		xmin, xmax = 0, 0
		ymin, ymax = 0, 0
		if (xvel_ is not None):
			if (L_type(xvel_) == 'table'):
				xmin = xvel_[1]
				xmax = xvel_[2]
			else:
				xvel = (_t2 if L_t(_t2 := L_tonumber(xvel_)) else 0)
		if (yvel_ is not None):
			if (L_type(yvel_) == 'table'):
				ymin = yvel_[1]
				ymax = yvel_[2]
			else:
				yvel = (_t3 if L_t(_t3 := L_tonumber(yvel_)) else 0)
		cnum = 0
		if (colours is not None):
			c_4 = colours[1]
			if (L_type(c_4) == 'table'):
				cnum = L_len(colours)
			else:
				c1_3 = (_t4 if L_t(_t4 := L_tonumber(colours[1])) else 0)
				c2_3 = (_t5 if L_t(_t5 := L_tonumber(colours[2])) else 3)
		word2_2 = (_t6 if L_t(_t6 := word2__2) else 'is')
		this_2 = G['findfeature'](None, word2_2, word3_2)
		if (this_2 is not None):
			for k_2, v_3 in L_ipairs(this_2):
				if (((v_3[1] != 'empty') and (v_3[1] != 'all')) and (v_3[1] != 'level')):
					these_2 = G['findall'](v_3, True)
					for a_2, b_2 in L_ipairs(these_2):
						unit_6 = G['mmf']['newObject'](b_2)
						x_7, y_7 = unit_6['values'][G['XPOS']], unit_6['values'][G['YPOS']]
						if L_t(unit_6['visible']):
							for i_11 in L_range(1, count_5):
								if (cnum > 0):
									rnd_2 = G['math']['random'](1, cnum)
									col = colours[rnd_2]
									c1_3 = col[1]
									c2_3 = col[2]
								partid_3 = G['MF_particle'](particle_2, x_7, y_7, c1_3, c2_3, layer_4)
								if ((partid_3 is not None) and (partid_3 != 0)):
									part_3 = G['mmf']['newObject'](partid_3)
									part_3['values'][G['ONLINE']] = 1
									part_3['x'] = unit_6['x']
									part_3['y'] = unit_6['y']
									part_3['values'][G['XPOS']] = unit_6['x']
									part_3['values'][G['YPOS']] = unit_6['y']
									if ((xmin != 0) or (xmax != 0)):
										xvel = G['math']['random'](xmin, xmax)
									if ((ymin != 0) or (ymax != 0)):
										yvel = G['math']['random'](ymin, ymax)
									part_3['values'][G['XVEL']] = xvel
									part_3['values'][G['YVEL']] = yvel
				elif ((v_3[1] == 'empty') or (v_3[1] == 'level')):
					if ((v_3[1] != 'level') or ((v_3[1] == 'level') and L_t(G['testcond'](v_3[2], 1)))):
						for i_12 in L_range(1, (G['roomsizex'] - 2)):
							for j_2 in L_range(1, (G['roomsizey'] - 2)):
								tileid_2 = (i_12 + (j_2 * G['roomsizex']))
								if (cnum > 0):
									rnd_3 = G['math']['random'](1, cnum)
									col_2 = colours[rnd_3]
									c1_3 = col_2[1]
									c2_3 = col_2[2]
								if ((G['unitmap'][tileid_2] is None) or ((G['unitmap'][tileid_2] is not None) and (L_len(G['unitmap'][tileid_2]) == 0))):
									if ((v_3[1] != 'empty') or ((v_3[1] == 'empty') and L_t(G['testcond'](v_3[2], 2, i_12, j_2, None, None, None, G['ignorebroken'])))):
										partid_4 = G['MF_particle'](particle_2, i_12, j_2, c1_3, c2_3, layer_4)
										if ((partid_4 is not None) and (partid_4 != 0)):
											part_4 = G['mmf']['newObject'](partid_4)
											part_4['values'][G['ONLINE']] = 1
											part_4['x'] = ((G['Xoffset'] + (((i_12 - 1) * G['tilesize']) * G['spritedata']['values'][G['TILEMULT']])) + ((G['tilesize'] * 1.5) * G['spritedata']['values'][G['TILEMULT']]))
											part_4['y'] = ((G['Yoffset'] + (((j_2 - 1) * G['tilesize']) * G['spritedata']['values'][G['TILEMULT']])) + ((G['tilesize'] * 1.5) * G['spritedata']['values'][G['TILEMULT']]))
											part_4['values'][G['XPOS']] = part_4['x']
											part_4['values'][G['YPOS']] = part_4['y']
											if ((xmin != 0) or (xmax != 0)):
												xvel = G['math']['random'](xmin, xmax)
											if ((ymin != 0) or (ymax != 0)):
												yvel = G['math']['random'](ymin, ymax)
											part_4['values'][G['XVEL']] = xvel
											part_4['values'][G['YVEL']] = yvel
	G['doshorteffect'] = f_doshorteffect
