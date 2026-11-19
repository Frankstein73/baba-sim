"""Generated from dynamictiling.lua by tools/lua2py.py. Do not edit."""
from babasim.luart import *  # noqa: F403


def load(G):
	def f_dynamictile(unitid=None, x=None, y=None, name=None, extra_=None, *_):  # L1
		ox, oy = 0, 0
		result = 0
		exclude = 0
		layer = G['map'][0]
		extra = L_T([name, 'edge', 'level'])
		if (extra_ is not None):
			for a, b in L_ipairs(extra_):
				L_insert(extra, b)
		i_ = 4
		sdirs = L_T()
		sresult = False
		sresult2 = False
		if (((G['unitreference'][name] is not None) and (G['specialtiling'][G['unitreference'][name]] is not None)) and L_t(G['specialtiling'][G['unitreference'][name]])):
			i_ = 8
		for i in L_range(1, i_):
			v = G['dirs_diagonals_'][i]
			ox = v[1]
			oy = v[2]
			sdirs[i] = 0
			tileid = ((x + ox) + ((y + oy) * G['roomsizex']))
			uth = G['unittypeshere'][tileid]
			maptile = 255
			found = False
			if ((uth is not None) and L_t(G['inbounds']((x + ox), (y + oy)))):
				for c, d in L_ipairs(extra):
					if (uth[d] is not None):
						if ((d != 'level') or (G['generaldata']['strings'][G['WORLD']] == G['generaldata']['strings'][G['BASEWORLD']])):
							found = True
							break
						else:
							if ((unitid < 0) or (unitid > 2)):
								unit = G['mmf']['newObject'](unitid)
								if (unit['values'][G['COMPLETED']] > 0):
									found = True
									break
							if (G['unitmap'][tileid] is not None):
								umh = G['unitmap'][tileid]
								for e, f in L_ipairs(umh):
									funit = G['mmf']['newObject'](f)
									if ((funit['strings'][G['UNITNAME']] == 'level') and (L_t(funit['visible']) and (funit['values'][G['COMPLETED']] > 0))):
										found = True
										break
			if (((((x + ox) == 0) or ((y + oy) == 0)) or ((x + ox) == (G['roomsizex'] - 1))) or ((y + oy) == (G['roomsizey'] - 1))):
				maptile = 1
			if ((found is not None and found is not False) or (maptile != 255)):
				sdirs[i] = 1
				if (i < 5):
					result = (result + L_pow(2, (i - 1)))
				else:
					sresult = True
		if (sresult is not None and sresult is not False):
			result = G['handlespecialtiling'](sdirs, result)
			if (result > 31):
				sresult2 = True
				result = (result % 32)
		return (result, sresult2,)
		return ()
	G['dynamictile'] = f_dynamictile
	def f_dynamictiling(*_):  # L97
		for i_2, unitid_2 in L_ipairs(G['tiledunits']):
			unit_2 = G['mmf']['newObject'](unitid_2)
			if (unit_2['values'][G['TILING']] == 1):
				unit_2['direction'], unit_2['flags'][G['SPECIALTILING']] = L_adjust((*G['dynamictile'](unitid_2, unit_2['values'][G['XPOS']], unit_2['values'][G['YPOS']], unit_2['strings'][G['UNITNAME']]),), 2)
				unit_2['values'][G['VISUALDIR']] = unit_2['direction']
	G['dynamictiling'] = f_dynamictiling
	def f_dynamic(id_=None, extra__2=None, *_):  # L108
		unit_3 = G['mmf']['newObject'](id_)
		if (unit_3['values'][G['TILING']] == 1):
			x_2, y_2 = unit_3['values'][G['XPOS']], unit_3['values'][G['YPOS']]
			ox_2, oy_2 = 0, 0
			name_2 = unit_3['strings'][G['UNITNAME']]
			extra_2 = L_T([name_2, 'edge', 'level'])
			if (extra__2 is not None):
				for a_2, b_2 in L_ipairs(extra__2):
					L_insert(extra_2, b_2)
			unit_3['direction'], unit_3['flags'][G['SPECIALTILING']] = L_adjust((*G['dynamictile'](unit_3['fixed'], x_2, y_2, name_2, extra_2),), 2)
			unit_3['values'][G['VISUALDIR']] = unit_3['direction']
			i__2 = 4
			if (G['specialtiling']['exists'] is not None):
				i__2 = 8
			for i_3 in L_range(1, i__2):
				v_2 = G['dirs_diagonals_'][i_3]
				ox_2 = v_2[1]
				oy_2 = v_2[2]
				tileid_2 = ((x_2 + ox_2) + ((y_2 + oy_2) * G['roomsizex']))
				tiledata = G['unitmap'][tileid_2]
				if ((tiledata is not None) and L_t(G['inbounds']((x_2 + ox_2), (y_2 + oy_2)))):
					for a_3, b_3 in L_ipairs(tiledata):
						tile = G['mmf']['newObject'](b_3)
						if ((tile['strings'][G['UNITNAME']] == name_2) and (tile['values'][G['TILING']] == 1)):
							tile['direction'], tile['flags'][G['SPECIALTILING']] = L_adjust((*G['dynamictile'](b_3, (x_2 + ox_2), (y_2 + oy_2), name_2, extra__2),), 2)
							tile['values'][G['VISUALDIR']] = tile['direction']
	G['dynamic'] = f_dynamic
	def f_dynamicat(x_3=None, y_3=None, *_):  # L154
		ox_3, oy_3 = 0, 0
		i__3 = 4
		if (G['specialtiling']['exists'] is not None):
			i__3 = 8
		for i_4 in L_range(1, i__3):
			v_3 = G['dirs_diagonals_'][i_4]
			ox_3 = v_3[1]
			oy_3 = v_3[2]
			if L_t(G['inbounds']((x_3 + ox_3), (y_3 + oy_3))):
				tiles = G['findallhere']((x_3 + ox_3), (y_3 + oy_3))
				if (L_len(tiles) > 0):
					for a_4, b_4 in L_ipairs(tiles):
						tile_2 = G['mmf']['newObject'](b_4)
						if (tile_2['values'][G['TILING']] == 1):
							tile_2['direction'], tile_2['flags'][G['SPECIALTILING']] = L_adjust((*G['dynamictile'](b_4, (x_3 + ox_3), (y_3 + oy_3), tile_2['strings'][G['UNITNAME']]),), 2)
							tile_2['values'][G['VISUALDIR']] = tile_2['direction']
	G['dynamicat'] = f_dynamicat
	def f_setspecialtiling(name_3=None, status=None, *_):  # L185
		G['specialtiling'][name_3] = status
		G['specialtiling']['exists'] = True
	G['setspecialtiling'] = f_setspecialtiling
	def f_handlespecialtiling(sdirs_2=None, result_=None, *_):  # L190
		dat = L_concat(L_tostring(sdirs_2[1]), L_tostring(sdirs_2[2]), L_tostring(sdirs_2[3]), L_tostring(sdirs_2[4]))
		dat2 = L_concat(L_tostring(sdirs_2[5]), L_tostring(sdirs_2[6]), L_tostring(sdirs_2[7]), L_tostring(sdirs_2[8]))
		result_2 = result_
		opts = L_T([], {'1100': L_T([], {'1xxx': 1}), '0110': L_T([], {'x1xx': 5}), '0011': L_T([], {'xx1x': 11}), '1001': L_T([], {'xxx1': 19}), '1110': L_T([], {'10xx': 2, '01xx': 6, '11xx': 9}), '0111': L_T([], {'x10x': 7, 'x01x': 13, 'x11x': 16}), '1011': L_T([], {'xx10': 12, 'xx01': 21, 'xx11': 27}), '1101': L_T([], {'1xx0': 3, '0xx1': 20, '1xx1': 23}), '1111': L_T([], {'1000': 4, '0100': 8, '0010': 14, '0001': 22, '1100': 10, '0110': 17, '0011': 28, '1001': 24, '1010': 15, '0101': 25, '1110': 18, '0111': 30, '1011': 29, '1101': 26, '1111': 31})})
		if (opts[dat] is not None):
			for i_5, v_4 in L_pairs(opts[dat]):
				found_2 = True
				if (((found_2 is not None and found_2 is not False) and (L_sub(i_5, 1, 1) != 'x')) and (L_sub(i_5, 1, 1) != L_sub(dat2, 1, 1))):
					found_2 = False
				if (((found_2 is not None and found_2 is not False) and (L_sub(i_5, 2, 2) != 'x')) and (L_sub(i_5, 2, 2) != L_sub(dat2, 2, 2))):
					found_2 = False
				if (((found_2 is not None and found_2 is not False) and (L_sub(i_5, 3, 3) != 'x')) and (L_sub(i_5, 3, 3) != L_sub(dat2, 3, 3))):
					found_2 = False
				if (((found_2 is not None and found_2 is not False) and (L_sub(i_5, 4, 4) != 'x')) and (L_sub(i_5, 4, 4) != L_sub(dat2, 4, 4))):
					found_2 = False
				if (found_2 is not None and found_2 is not False):
					result_2 = (15 + v_4)
					break
		return result_2
	G['handlespecialtiling'] = f_handlespecialtiling
