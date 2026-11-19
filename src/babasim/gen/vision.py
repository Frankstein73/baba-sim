"""Generated from vision.lua by tools/lua2py.py. Do not edit."""
from babasim.luart import *  # noqa: F403


def load(G):
	def f_visionmode(state=None, target_=None, noundo_=None, extradata_=None, *_):  # L1
		noundo = (_t1 if L_t(_t1 := noundo_) else False)
		target = (_t2 if L_t(_t2 := target_) else 0)
		extra = (_t3 if L_t(_t3 := extradata_) else L_T())
		if ((G['spritedata']['values'][G['VISION']] == 0) and (state == 1)):
			G['visiontargets'] = L_T()
			if (target == 0):
				vistest, vt2 = L_adjust((*G['findallfeature'](None, 'is', '3d', True),), 2)
				for i, v in L_ipairs(vistest):
					L_insert(G['visiontargets'], v)
				target = (_t4 if L_t(_t4 := G['visiontargets'][1]) else 0)
			if (target != 0):
				G['funnywalls'] = L_T()
				if (target != 0.5):
					unit = G['mmf']['newObject'](target)
					if (unit['values'][G['ONLINE']] != 4):
						G['spritedata']['values'][G['CAMTARGET']] = unit['values'][G['ID']]
						G['spritedata']['values'][G['XCAMERA']] = unit['values'][G['XPOS']]
						G['spritedata']['values'][G['YCAMERA']] = unit['values'][G['YPOS']]
						G['spritedata']['values'][G['CAMDIR']] = unit['values'][G['DIR']]
					G['MF_setupvision'](target)
				elif (L_len(extra) == 3):
					G['spritedata']['values'][G['CAMTARGET']] = 0.5
					G['spritedata']['values'][G['XCAMERA']] = extra[1]
					G['spritedata']['values'][G['YCAMERA']] = extra[2]
					G['spritedata']['values'][G['CAMDIR']] = extra[3]
					G['MF_setupvision'](target)
				G['MF_removeblockeffect'](0)
				G['updateanimations'](None, True)
				if (noundo is False):
					if (target != 0.5):
						unit_2 = G['mmf']['newObject'](target)
						G['addundo'](L_T(['startvision', unit_2['values'][G['ID']]]))
						G['updateundo'] = True
					else:
						G['addundo'](L_T(['startvision', 0.5]))
						G['updateundo'] = True
		elif ((G['spritedata']['values'][G['VISION']] == 1) and (state == 0)):
			G['MF_loop']('clearedges', 1)
			G['HACK_ROOMSIZEUNDO'] = True
			G['MF_loop']('roomsize', 1)
			G['HACK_ROOMSIZEUNDO'] = False
			G['MF_resetobjectpos']()
			G['visiontargets'] = L_T()
			if (noundo is False):
				G['addundo'](L_T(['stopvision', G['spritedata']['values'][G['CAMTARGET']], G['spritedata']['values'][G['XCAMERA']], G['spritedata']['values'][G['YCAMERA']], G['spritedata']['values'][G['CAMDIR']]]))
				G['updateundo'] = True
			for i_2, unitid in L_ipairs(G['HACK_ROOMSIZEUNDO_DELTHESE']):
				G['delete'](unitid, None, None, True, True)
			G['HACK_ROOMSIZEUNDO_DELTHESE'] = L_T()
			G['funnywalls'] = L_T()
			G['MF_closevision']()
			G['dynamictiling']()
			G['ruleblockeffect']()
			G['spritedata']['values'][G['CAMTARGET']] = 0
			for i_3, unit_3 in L_ipairs(G['units']):
				cc = (_t5 if L_t(_t5 := unit_3['colour']) else L_T())
				cc1 = (_t6 if L_t(_t6 := cc[1]) else 0)
				cc2 = (_t7 if L_t(_t7 := cc[2]) else 3)
				G['MF_setcolour'](unit_3['fixed'], cc1, cc2)
		G['spritedata']['values'][G['VISION']] = state
	G['visionmode'] = f_visionmode
	def f_changevisiontarget(not_this_=None, *_):  # L96
		current = G['spritedata']['values'][G['CAMTARGET']]
		newtarget = 0
		not_this = (_t1 if L_t(_t1 := not_this_) else (-1))
		if (L_len(G['visiontargets']) > 0):
			fixed = (_t2 if L_t(_t2 := G['MF_getfixed'](current)) else 0)
			if (fixed == 0):
				newtarget = G['visiontargets'][1]
			else:
				targetid = 0
				for i_4, v_2 in L_ipairs(G['visiontargets']):
					if (v_2 == fixed):
						targetid = (i_4 + 1)
						break
				if (targetid > L_len(G['visiontargets'])):
					targetid = 1
				newtarget = G['visiontargets'][targetid]
		if (newtarget != not_this):
			if (newtarget is None):
				G['visionmode'](0, 0, None, L_T([G['spritedata']['values'][G['XCAMERA']], G['spritedata']['values'][G['YCAMERA']], G['spritedata']['values'][G['CAMDIR']]]))
				G['spritedata']['values'][G['CAMTARGET']] = 0
			elif ((newtarget != 0) and (newtarget != 2)):
				test = G['MF_findfixed'](newtarget)
				if (test is not None):
					unit_4 = G['mmf']['newObject'](newtarget)
					newtarget = unit_4['values'][G['ID']]
					G['MF_updatevision'](unit_4['values'][G['DIR']])
					G['MF_updatevisionpos'](unit_4['values'][G['XPOS']], unit_4['values'][G['YPOS']])
				else:
					newtarget = 0
				G['spritedata']['values'][G['CAMTARGET']] = newtarget
			else:
				G['spritedata']['values'][G['CAMTARGET']] = newtarget
		else:
			G['spritedata']['values'][G['CAMTARGET']] = 0.5
			newtarget = 0.5
		if (newtarget != current):
			fixed_2 = G['getunitid'](current)
			if (fixed_2 != 0):
				unit_5 = G['mmf']['newObject'](fixed_2)
				unit_5['x'] = (-24)
				unit_5['y'] = (-24)
				unit_5['scaleX'] = 1
				unit_5['scaleY'] = 1
		G['addundo'](L_T(['visiontarget', current, newtarget]))
		G['updateundo'] = True
	G['changevisiontarget'] = f_changevisiontarget
	def f_updatevisiontargets(*_):  # L165
		G['visiontargets'] = L_T()
		current_2 = G['spritedata']['values'][G['CAMTARGET']]
		vistest_2, vt2_2 = L_adjust((*G['findallfeature'](None, 'is', '3d', True),), 2)
		for i_5, v_3 in L_ipairs(vistest_2):
			L_insert(G['visiontargets'], v_3)
		targetid_2 = 1
		if (current_2 != 0):
			for i_6, v_4 in L_ipairs(G['visiontargets']):
				unit_6 = G['mmf']['newObject'](v_4)
				if ((unit_6['values'][G['ID']] == current_2) and (unit_6['flags'][G['DEAD']] is False)):
					targetid_2 = i_6
					break
		target_2 = (_t1 if L_t(_t1 := G['visiontargets'][targetid_2]) else 0)
		stopvision = False
		if (target_2 != 0):
			unit_7 = G['mmf']['newObject'](target_2)
			if (unit_7['flags'][G['DEAD']] is False):
				G['spritedata']['values'][G['CAMTARGET']] = unit_7['values'][G['ID']]
				G['MF_updatevision'](unit_7['values'][G['DIR']])
				G['MF_updatevisionpos'](unit_7['values'][G['XPOS']], unit_7['values'][G['YPOS']])
			else:
				stopvision = True
		else:
			stopvision = True
		if (((stopvision is not None and stopvision is not False) and (G['spritedata']['values'][G['VISION']] == 1)) and (G['spritedata']['values'][G['CAMTARGET']] != 0.5)):
			G['visionmode'](0, 0, None, L_T([G['spritedata']['values'][G['XCAMERA']], G['spritedata']['values'][G['YCAMERA']], G['spritedata']['values'][G['CAMDIR']]]))
		if (((target_2 != current_2) and (current_2 != 0)) and (G['MF_getfixed'](current_2) is not None)):
			fixed_3 = G['getunitid'](current_2)
			if (fixed_3 != 0):
				unit_8 = G['mmf']['newObject'](fixed_3)
				unit_8['x'] = (-24)
				unit_8['y'] = (-24)
				unit_8['scaleX'] = 1
				unit_8['scaleY'] = 1
	G['updatevisiontargets'] = f_updatevisiontargets
	def f_extrarender(*_):  # L220
		cx, cy, cdir = G['spritedata']['values'][G['XCAMERA']], G['spritedata']['values'][G['YCAMERA']], G['spritedata']['values'][G['CAMDIR']]
		mx, my = (G['screenw'] * 0.5), (G['screenh'] * 0.5)
		mtx, mty = (G['roomsizex'] * 0.5), (G['roomsizey'] * 0.5)
		maxscale = 13
		cx = (cx - mtx)
		cy = (cy - mty)
		exists = L_T()
		renderthese = L_T()
		for i_7, unit_9 in L_ipairs(G['units']):
			if (unit_9['values'][G['ZLAYER']] < 21):
				if L_t(unit_9['visible']):
					if (unit_9['xpos'] is None):
						unit_9['xpos'] = unit_9['values'][G['XPOS']]
					if (unit_9['ypos'] is None):
						unit_9['ypos'] = unit_9['values'][G['YPOS']]
					if (unit_9['xpos'] != unit_9['values'][G['XPOS']]):
						if (abs((unit_9['xpos'] - unit_9['values'][G['XPOS']])) > 2):
							unit_9['xpos'] = unit_9['values'][G['XPOS']]
						else:
							unit_9['xpos'] = (unit_9['xpos'] + ((unit_9['values'][G['XPOS']] - unit_9['xpos']) * 0.4))
					if (unit_9['ypos'] != unit_9['values'][G['YPOS']]):
						if (abs((unit_9['ypos'] - unit_9['values'][G['YPOS']])) > 2):
							unit_9['ypos'] = unit_9['values'][G['YPOS']]
						else:
							unit_9['ypos'] = (unit_9['ypos'] + ((unit_9['values'][G['YPOS']] - unit_9['ypos']) * 0.4))
					dothis = G['cullvision']((unit_9['xpos'] - G['spritedata']['values'][G['XCAMERA']]), (unit_9['ypos'] - G['spritedata']['values'][G['YCAMERA']]), cdir)
					if (dothis is not None and dothis is not False):
						L_insert(renderthese, unit_9)
					else:
						unit_9['x'] = (-24)
						unit_9['y'] = (-24)
						unit_9['scaleX'] = 1
						unit_9['scaleY'] = 1
				exists[unit_9['fixed']] = 1
		for i_8, unitid_2 in L_ipairs(G['edgetiles']):
			unit_10 = G['mmf']['newObject'](unitid_2)
			if (unit_10 is not None):
				if L_t(unit_10['visible']):
					if (unit_10['xpos'] is None):
						unit_10['xpos'] = unit_10['values'][G['XPOS']]
					if (unit_10['ypos'] is None):
						unit_10['ypos'] = unit_10['values'][G['YPOS']]
					if (unit_10['xpos'] != unit_10['values'][G['XPOS']]):
						if (abs((unit_10['xpos'] - unit_10['values'][G['XPOS']])) > 2):
							unit_10['xpos'] = unit_10['values'][G['XPOS']]
						else:
							unit_10['xpos'] = (unit_10['xpos'] + ((unit_10['values'][G['XPOS']] - unit_10['xpos']) * 0.4))
					if (unit_10['ypos'] != unit_10['values'][G['YPOS']]):
						if (abs((unit_10['ypos'] - unit_10['values'][G['YPOS']])) > 2):
							unit_10['ypos'] = unit_10['values'][G['YPOS']]
						else:
							unit_10['ypos'] = (unit_10['ypos'] + ((unit_10['values'][G['YPOS']] - unit_10['ypos']) * 0.4))
					dothis_2 = G['cullvision']((unit_10['xpos'] - G['spritedata']['values'][G['XCAMERA']]), (unit_10['ypos'] - G['spritedata']['values'][G['YCAMERA']]), cdir)
					if (dothis_2 is not None and dothis_2 is not False):
						L_insert(renderthese, unit_10)
					else:
						unit_10['x'] = (-24)
						unit_10['y'] = (-24)
						unit_10['scaleX'] = 1
						unit_10['scaleY'] = 1
				exists[unit_10['fixed']] = 1
		renders = 0
		for i_9, unit_11 in L_ipairs(renderthese):
			rendered = G['extrarender_do'](unit_11, True, cx, cy, cdir, mx, my, mtx, mty, L_T([maxscale]))
			renders = (renders + 1)
			if (rendered is not None and rendered is not False):
				exists[unit_11['fixed']] = 2
		removethese = L_T()
		for i_10, unit_12 in L_ipairs(G['funnywalls']):
			ownerid = unit_12['values'][G['VISUALSTYLE']]
			if ((exists[ownerid] is not None) and (exists[ownerid] == 2)):
				owner = G['mmf']['newObject'](ownerid)
				unit_12['visible'] = owner['visible']
				if (L_t(owner['visible']) and (owner['values'][G['ID']] != G['spritedata']['values'][G['CAMTARGET']])):
					unit_12['xpos'] = owner['xpos']
					unit_12['ypos'] = owner['ypos']
					unit_12['values'][G['XPOS']] = owner['values'][G['XPOS']]
					unit_12['values'][G['YPOS']] = owner['values'][G['YPOS']]
					unit_12['values'][G['ZPOS']] = owner['values'][G['ZPOS']]
					unit_12['values'][G['ZLAYER']] = (owner['values'][G['ZLAYER']] + 0.5)
					unit_12['values'][G['FLOAT']] = owner['values'][G['FLOAT']]
					unit_12['strings'][G['COLOUR']] = owner['strings'][G['COLOUR']]
					unit_12['strings'][G['CLEARCOLOUR']] = owner['strings'][G['CLEARCOLOUR']]
					unit_12['flags'][G['PHANTOM']] = owner['flags'][G['PHANTOM']]
					G['extrarender_do'](unit_12, True, cx, cy, cdir, mx, my, mtx, mty, L_T([maxscale]))
					renders = (renders + 1)
				elif (owner['values'][G['ID']] != G['spritedata']['values'][G['CAMTARGET']]):
					unit_12['visible'] = False
			elif ((exists[ownerid] is not None) and (exists[ownerid] == 1)):
				unit_12['visible'] = False
			elif (exists[ownerid] is None):
				unit_12['flags'][G['DEAD']] = True
				L_insert(removethese, L_T([i_10, unit_12['fixed']]))
		offset = 0
		for i_11, v_5 in L_ipairs(removethese):
			L_remove(G['funnywalls'], (v_5[1] - offset))
			offset = (offset + 1)
			G['MF_cleanremove'](v_5[2])
	G['extrarender'] = f_extrarender
	def f_cullvision(dx=None, dy=None, cd=None, *_):  # L379
		ox, oy = 0, 0
		if ((dx == 0) and (dy == 0)):
			return True
		elif ((abs(dx) > 8) or (abs(dy) > 8)):
			return False
		if ((cd < 1) or (cd > 3)):
			ox = 1
		elif ((cd > 1) and (cd < 3)):
			ox = (-1)
		if ((cd < 2) and (cd > 0)):
			oy = (-1)
		elif ((cd > 2) and (cd < 4)):
			oy = 1
		if ((ox > 0) and (dx >= 0)):
			return True
		elif ((ox < 0) and (dx <= 0)):
			return True
		if ((oy > 0) and (dy >= 0)):
			return True
		elif ((oy < 0) and (dy <= 0)):
			return True
		return False
	G['cullvision'] = f_cullvision
	def f_extrarender_do(unit_13=None, setcolour_=None, cx_2=None, cy_2=None, cdir_2=None, mx_2=None, my_2=None, mtx_2=None, mty_2=None, data=None, *_):  # L415
		setcolour = True
		if (setcolour_ is not None):
			setcolour = setcolour_
		cangle = G['math']['rad']((cdir_2 * 90))
		maxs = data[1]
		ux = unit_13['xpos']
		uy = unit_13['ypos']
		x, y = (ux - mtx_2), (uy - mty_2)
		diffx = ((x - cx_2) * G['f_tilesize'])
		diffy = ((y - cy_2) * G['f_tilesize'])
		xdist, ydist = None, None
		if (L_floor(cdir_2) == cdir_2):
			if (cdir_2 == 0):
				xdist = ((cy_2 - y) * G['f_tilesize'])
				ydist = ((cx_2 - x) * G['f_tilesize'])
			elif (cdir_2 == 1):
				xdist = ((cx_2 - x) * G['f_tilesize'])
				ydist = ((y - cy_2) * G['f_tilesize'])
			elif (cdir_2 == 2):
				xdist = ((y - cy_2) * G['f_tilesize'])
				ydist = ((x - cx_2) * G['f_tilesize'])
			elif (cdir_2 == 3):
				xdist = ((x - cx_2) * G['f_tilesize'])
				ydist = ((cy_2 - y) * G['f_tilesize'])
		else:
			dist = G['math']['sqrt']((L_pow(diffy, 2) + L_pow(diffx, 2)))
			dir_ = (0 - G['math']['atan2'](diffy, diffx))
			ydist = (0 - (G['math']['cos']((dir_ - cangle)) * dist))
			xdist = (G['math']['sin']((dir_ - cangle)) * dist)
		z = (0 - L_div(ydist, G['f_tilesize']))
		hor = L_div(xdist, G['f_tilesize'])
		if (xdist < 0):
			hor = (0 - abs(L_div(xdist, G['f_tilesize'])))
		if (((unit_13['values'][G['ZLAYER']] > 15) and (unit_13['values'][G['ZLAYER']] <= 20)) and (unit_13['className'] != 'edge')):
			z = (z + 0.1)
		negz = (8 - z)
		partmult = L_div((negz * (0.5 * (negz + 1))), 2)
		sizedelta = L_div((8 - z), 4)
		sizemult = ((10 - partmult) - 1)
		scale = (maxs - sizemult)
		n_negz = (8 - (z + 1))
		n_partmult = L_div((n_negz * (0.5 * (n_negz + 1))), 2)
		n_sizemult = ((10 - n_partmult) - 1)
		n_scale = (maxs - n_sizemult)
		difference = L_div(n_scale, scale)
		nx = (mx_2 - ((hor * scale) * G['f_tilesize']))
		ny = my_2
		result = False
		if (((((scale > 0) and (z >= 0)) and (z < 9)) and (nx > (0 - ((scale * G['tilesize']) * 0.5)))) and (nx < (G['screenw'] + ((scale * G['tilesize']) * 0.5)))):
			result = True
			unit_13['x'] = nx
			unit_13['y'] = ny
			if (L_floor(z) == z):
				unit_13['scaleX'] = scale
				unit_13['scaleY'] = scale
			else:
				unit_13['scaleX'] = (scale + 0.05)
				unit_13['scaleY'] = (scale + 0.05)
			unit_13['values'][G['ZPOS']] = L_floor((z + 0.5))
			if (unit_13['values'][G['ONLINE']] == 4):
				unit_13['values'][G['ZPOS']] = (L_floor((z + 0.5)) + 0.5)
			elif (((unit_13['values'][G['ZLAYER']] > 15) and (unit_13['values'][G['ZLAYER']] <= 20)) and (unit_13['className'] != 'edge')):
				unit_13['values'][G['ZPOS']] = (unit_13['values'][G['ZPOS']] + 0.25)
			unit_13['flags'][G['VISION_OPTIMIZE']] = True
			if ((hor == 0) and (unit_13['values'][G['ZLAYER']] > 10)):
				unit_13['flags'][G['VISION_CENTERED']] = True
			else:
				unit_13['flags'][G['VISION_CENTERED']] = False
			if (((unit_13['values'][G['ONLINE']] != 4) and L_t(unit_13['visible'])) and (unit_13['values'][G['ID']] != G['spritedata']['values'][G['CAMTARGET']])):
				if ((unit_13['values'][G['ZLAYER']] <= 10) and (unit_13['className'] != 'edge')):
					unit_13['scaleY'] = sizedelta
					unit_13['y'] = ((ny + ((G['tilesize'] * scale) * 0.5)) - ((G['tilesize'] * sizedelta) * 0.5))
					topw = difference
					botw = 1.0
					topc = 0.5
					botc = 0.5
					if (hor != 0):
						awidth = (abs(hor) + L_max((abs(hor) - 1), 0))
						fullwidth = (scale + ((sizedelta * awidth) * 2))
						unit_13['scaleX'] = fullwidth
						topwidth = L_div(n_scale, fullwidth)
						botwidth = L_div(scale, fullwidth)
						topcenter = (1 - (topwidth * 0.5))
						botcenter = (0 + (botwidth * 0.5))
						if (hor < 0):
							topcenter = (0 + (topwidth * 0.5))
							botcenter = (1 - (botwidth * 0.5))
						topw = topwidth
						botw = botwidth
						topc = topcenter
					unit_13['strings'][G['SHADEREFFECTS']] = L_concat(L_tostring(topw), ',', L_tostring(botw), ',1.0,1.0,', L_tostring(topc), ',', L_tostring(botc), ',0.5,0.5')
					if (unit_13['values'][G['TILING']] == 1):
						G['visiontiling'](unit_13, L_floor(cdir_2))
				elif ((unit_13['values'][G['ZLAYER']] > 10) and (unit_13['values'][G['ZLAYER']] <= 15)):
					if (hor != 0):
						awidth_2 = (abs(hor) + L_max((abs(hor) - 1), 0))
						unit_13['scaleX'] = (sizedelta * awidth_2)
						righth = difference
						lefth = 1.0
						if (hor > 0):
							unit_13['x'] = ((nx + ((G['tilesize'] * scale) * 0.5)) + (((G['tilesize'] * sizedelta) * 0.5) * awidth_2))
						elif (hor < 0):
							unit_13['x'] = ((nx - ((G['tilesize'] * scale) * 0.5)) - (((G['tilesize'] * sizedelta) * 0.5) * awidth_2))
							lefth = difference
							righth = 1.0
						unit_13['strings'][G['SHADEREFFECTS']] = L_concat('1.0,1.0,', L_tostring(lefth), ',', L_tostring(righth), ',', '0.5,0.5,0.5,0.5')
					else:
						unit_13['x'] = (-24)
						unit_13['y'] = (-24)
						unit_13['scaleX'] = 1
						unit_13['scaleY'] = 1
						unit_13['flags'][G['VISION_OPTIMIZE']] = False
						unit_13['strings'][G['SHADEREFFECTS']] = '1.0,1.0,1.0,1.0,0.5,0.5,0.5,0.5'
				if (setcolour is not None and setcolour is not False):
					coloffset = L_min(L_max(((z - 1) * 7), 0), 255)
					colour = (_t1 if L_t(_t1 := unit_13['colour']) else L_T())
					c1 = (_t2 if L_t(_t2 := colour[1]) else 0)
					c2 = (_t3 if L_t(_t3 := colour[2]) else 3)
					if (unit_13['className'] == 'edge'):
						c1 = 1
						c2 = 1
					unit_13['strings'][G['CLEARCOLOUR']] = L_concat(L_tostring(c1), ',', L_tostring(c2), ',', L_tostring(coloffset))
		else:
			unit_13['flags'][G['VISION_OPTIMIZE']] = False
			unit_13['x'] = (-24)
			unit_13['y'] = (-24)
			unit_13['scaleX'] = 1
			unit_13['scaleY'] = 1
			unit_13['values'][G['ZPOS']] = (-1)
			unit_13['strings'][G['SHADEREFFECTS']] = '1.0,1.0,1.0,1.0,0.5,0.5,0.5,0.5'
		return result
	G['extrarender_do'] = f_extrarender_do
	def f_grid_3d(*_):  # L605
		vertlines = 3
		for i_12 in L_range((0 - vertlines), vertlines):
			unitid_3 = G['MF_specialcreate']('Grid_vertical')
			unit_14 = G['mmf']['newObject'](unitid_3)
			hor_2 = (i_12 - 0.5)
			z_2 = 8
			z2 = 1
			maxs_2 = 13
			negz_2 = (8 - z_2)
			partmult_2 = L_div((negz_2 * (0.5 * (negz_2 + 1))), 2)
			sizedelta_2 = L_div((8 - z_2), 4)
			sizemult_2 = ((10 - partmult_2) - 1)
			scale_2 = (maxs_2 - sizemult_2)
			negz2 = (8 - z2)
			partmult2 = L_div((negz2 * (0.5 * (negz2 + 1))), 2)
			sizedelta2 = L_div((8 - z2), 4)
			sizemult2 = ((10 - partmult2) - 1)
			scale2 = (maxs_2 - sizemult2)
			nx_2 = ((G['screenw'] * 0.5) - ((hor_2 * scale_2) * G['f_tilesize']))
			ny_2 = (G['screenh'] * 0.5)
			unit_14['x'] = nx_2
			unit_14['y'] = (ny_2 + 48)
			tx = ((G['screenw'] * 0.5) - ((hor_2 * scale2) * G['f_tilesize']))
			ty = (G['screenh'] - 24)
			dir__2 = (0 - G['math']['atan2']((ty - (ny_2 + 48)), (tx - nx_2)))
			unit_14['angle'] = (G['math']['deg'](dir__2) + 90)
			unit_14['scaleY'] = 12.0
			G['MF_setcolour'](unitid_3, 1, 2)
		for i_13 in L_range(0, 8):
			unitid_4 = G['MF_specialcreate']('Grid_horizontal')
			unit_15 = G['mmf']['newObject'](unitid_4)
			z_3 = i_13
			maxs_3 = 13
			negz_3 = (8 - z_3)
			partmult_3 = L_div((negz_3 * (0.5 * (negz_3 + 1))), 2)
			sizedelta_3 = L_div((8 - z_3), 4)
			sizemult_3 = ((10 - partmult_3) - 1)
			scale_3 = (maxs_3 - sizemult_3)
			nx_3 = 0
			ny_3 = (G['screenh'] * 0.5)
			unit_15['x'] = nx_3
			unit_15['y'] = (ny_3 + ((G['tilesize'] * scale_3) * 0.5))
			unit_15['scaleX'] = 32.0
			G['MF_setcolour'](unitid_4, 1, 2)
	G['grid_3d'] = f_grid_3d
	def f_setupvision_wall(unitid_5=None, *_):  # L670
		unit_16 = G['mmf']['newObject'](unitid_5)
		if (unit_16['flags'][G['DEAD']] is False):
			wallid = G['MF_create'](unit_16['className'])
			wall = G['mmf']['newObject'](wallid)
			wall['values'][G['VISUALSTYLE']] = unitid_5
			wall['values'][G['ONLINE']] = 4
			wall['scaleX'] = unit_16['scaleX']
			wall['scaleY'] = unit_16['scaleY']
			wall['values'][G['XPOS']] = unit_16['values'][G['XPOS']]
			wall['values'][G['YPOS']] = unit_16['values'][G['YPOS']]
			wall['values'][G['TILING']] = unit_16['values'][G['TILING']]
			wall['strings'][G['COLOUR']] = unit_16['strings'][G['COLOUR']]
			wall['strings'][G['CLEARCOLOUR']] = unit_16['strings'][G['CLEARCOLOUR']]
			wall['strings'][1] = unit_16['strings'][1]
			wall['strings'][2] = unit_16['strings'][2]
			wall['strings'][3] = unit_16['strings'][3]
			L_insert(G['funnywalls'], wall)
	G['setupvision_wall'] = f_setupvision_wall
	def f_visiontiling(unit_17=None, cdir_3=None, *_):  # L696
		if (unit_17['values'][G['TILING']] == 1):
			if (cdir_3 == 1):
				unit_17['direction'] = unit_17['values'][G['VISUALDIR']]
			else:
				dir__3 = unit_17['values'][G['VISUALDIR']]
				r, u, l, d = 0, 0, 0, 0
				if (dir__3 >= 8):
					dir__3 = (dir__3 - 8)
					d = 1
				if (dir__3 >= 4):
					dir__3 = (dir__3 - 4)
					l = 1
				if (dir__3 >= 2):
					dir__3 = (dir__3 - 2)
					u = 1
				if (dir__3 >= 1):
					dir__3 = (dir__3 - 1)
					r = 1
				nr, nu, nl, nd = 0, 0, 0, 0
				if (cdir_3 == 2):
					nr = u
					nu = l
					nl = d
					nd = r
				elif (cdir_3 == 3):
					nr = l
					nu = d
					nl = r
					nd = u
				else:
					nr = d
					nu = r
					nl = u
					nd = l
				final = (((nr + (nu * 2)) + (nl * 4)) + (nd * 8))
				unit_17['direction'] = final
	G['visiontiling'] = f_visiontiling
