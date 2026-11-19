"""Generated from modsupport.lua by tools/lua2py.py. Do not edit."""
from babasim.luart import *  # noqa: F403


def load(G):
	G['mod_hook_functions'] = L_T([], {'level_start': L_T(), 'level_end': L_T(), 'level_win': L_T(), 'level_win_after': L_T(), 'level_restart': L_T(), 'rule_update': L_T(), 'rule_baserules': L_T(), 'rule_update_after': L_T(), 'command_given': L_T(), 'movement_take': L_T(), 'movement_end': L_T(), 'block': L_T(), 'block_level': L_T(), 'turn_auto': L_T(), 'turn_end': L_T(), 'always': L_T(), 'effect_once': L_T(), 'effect_always': L_T(), 'undoed': L_T(), 'undoed_after': L_T(), 'levelpack_end': L_T(), 'levelpack_done': L_T(), 'text_input_ok': L_T(), 'mouse_click': L_T(), 'keyboard_input': L_T(), 'keyboard_hold': L_T()})
	def f_do_mod_hook(name=None, extra_=None, *_):  # L117
		extra = (_t1 if L_t(_t1 := extra_) else L_T())
		mods_run = False
		if (G['mod_hook_functions'][name] is not None):
			for i, v in L_pairs(G['mod_hook_functions'][name]):
				if (L_type(v) == 'function'):
					v(extra)
					mods_run = True
		return mods_run
	G['do_mod_hook'] = f_do_mod_hook
	G['buttonclick_list'] = L_T()
	def f_buttonclicked(name_2=None, unitid=None, *_):  # L135
		if ((L_strlen(name_2) > 0) and (G['buttonclick_list'][name_2] is not None)):
			G['buttonclick_list'][name_2](unitid)
	G['buttonclicked'] = f_buttonclicked
	G['slider_list'] = L_T()
	def f_slidermoved(name_3=None, unitid_2=None, value=None, change=None, *_):  # L143
		if ((L_strlen(name_3) > 0) and (G['slider_list'][name_3] is not None)):
			G['slider_list'][name_3](unitid_2, value, change)
	G['slidermoved'] = f_slidermoved
	G['undo_list'] = L_T()
	def f_undocall(id_=None, data=None, *_):  # L151
		if ((L_len(id_) > 0) and (G['undo_list'][id_] is not None)):
			G['undo_list'][id_](id_, data)
	G['undocall'] = f_undocall
	G['special_customtypes'] = L_T()
	def f_handlespecial_custom(unitid_3=None, text=None, id_comma=None, id_equals=None, x=None, y=None, *_):  # L159
		data_2 = (_t1 if L_t(_t1 := G['special_customtypes'][id_comma]) else G['special_customtypes'][id_equals])
		if (data_2 is not None):
			data_2(unitid_3, text)
	G['handlespecial_custom'] = f_handlespecial_custom
	def f_leveltransition_change(levelid=None, levelnumber=None, leveltype=None, resetleveltree=None, *_):  # L168
		G['generaldata']['values'][G['TRANSITIONREASON']] = 9
		G['generaldata']['values'][G['IGNORE']] = 1
		G['generaldata']['values'][G['WINTIMER']] = 0
		G['generaldata3']['values'][G['STOPTRANSITION']] = 1
		G['MF_store']('save', G['generaldata']['strings'][G['WORLD']], 'Previous', G['generaldata']['strings'][G['CURRLEVEL']])
		G['changelevel'](levelid, levelnumber, leveltype, resetleveltree)
		G['MF_loop']('transition', 1)
	G['leveltransition_change'] = f_leveltransition_change
	def f_leveltransition_sublevel(levelid_2=None, levelnumber_2=None, leveltype_2=None, *_):  # L178
		G['generaldata']['values'][G['TRANSITIONREASON']] = 9
		G['generaldata']['values'][G['IGNORE']] = 1
		G['generaldata']['values'][G['WINTIMER']] = 0
		G['generaldata3']['values'][G['STOPTRANSITION']] = 1
		G['MF_store']('save', G['generaldata']['strings'][G['WORLD']], 'Previous', G['generaldata']['strings'][G['CURRLEVEL']])
		G['sublevel'](levelid_2, levelnumber_2, leveltype_2)
		G['MF_loop']('transition', 1)
	G['leveltransition_sublevel'] = f_leveltransition_sublevel
	def f_leveltransition_leave(*_):  # L188
		G['generaldata']['values'][G['TRANSITIONREASON']] = 1
		G['generaldata']['values'][G['IGNORE']] = 1
		G['generaldata']['values'][G['WINTIMER']] = 0
		G['generaldata3']['values'][G['STOPTRANSITION']] = 0
		G['uplevel'](G['levelid'], G['levelnumber'], G['leveltype'])
		G['MF_loop']('transition', 1)
	G['leveltransition_leave'] = f_leveltransition_leave
	def f_setupmods_global(*_):  # L199
		files = G['MF_filelist']('Data/Lua/', '*.lua')
		L_sort(files)
		for i_2, file in L_ipairs(files):
			L_noop(L_concat('Added custom lua file ', file))
			G['dofile'](L_concat('Data/Lua/', file))
	G['setupmods_global'] = f_setupmods_global
	def f_setupmods_levelpack(*_):  # L210
		world = G['generaldata']['strings'][G['WORLD']]
		files_2 = G['MF_filelist'](L_concat('Data/Worlds/', world, '/Lua/'), '*.lua')
		L_sort(files_2)
		for i_3, file_2 in L_ipairs(files_2):
			L_noop(L_concat('Added custom levelpack (', world, ') lua file ', file_2))
			G['dofile'](L_concat('Data/Worlds/', world, '/Lua/', file_2))
		G['modsinuse'] = True
	G['setupmods_levelpack'] = f_setupmods_levelpack
