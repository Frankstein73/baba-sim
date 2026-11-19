"""Generated from clears.lua by tools/lua2py.py. Do not edit."""
from babasim.luart import *  # noqa: F403


def load(G):
	def f_clearunits(restore_=None, *_):  # L1
		G['units'] = L_T()
		G['tiledunits'] = L_T()
		G['codeunits'] = L_T()
		G['animunits'] = L_T()
		G['unitlists'] = L_T()
		G['undobuffer'] = L_T()
		G['unitmap'] = L_T()
		G['unittypeshere'] = L_T()
		G['prevunitmap'] = L_T()
		G['ruleids'] = L_T()
		G['objectlist'] = L_T()
		G['objectpalette'] = L_T()
		G['updatelist'] = L_T()
		G['objectcolours'] = L_T()
		G['wordunits'] = L_T()
		G['wordrelatedunits'] = L_T()
		G['letterunits'] = L_T()
		G['letterunits_map'] = L_T()
		G['paths'] = L_T()
		G['paradox'] = L_T()
		G['movelist'] = L_T()
		G['deleted'] = L_T()
		G['effecthistory'] = L_T()
		G['notfeatures'] = L_T()
		G['groupfeatures'] = L_T()
		G['groupmembers'] = L_T()
		G['pushedunits'] = L_T()
		G['customobjects'] = L_T()
		G['cobjects'] = L_T()
		G['condstatus'] = L_T()
		G['emptydata'] = L_T()
		G['leveldata'] = L_T()
		G['leveldata']['colours'] = L_T()
		G['leveldata']['currcolour'] = 0
		G['poweredstatus'] = L_T()
		G['specialtiling'] = L_T()
		G['backparticles'] = L_T()
		G['visiontargets'] = L_T()
		G['vision_rendered'] = L_T()
		G['generaldata']['values'][G['CURRID']] = 1
		G['updateundo'] = True
		G['hiddenmap'] = None
		G['levelconversions'] = L_T()
		G['last_key'] = 0
		G['auto_dir'] = L_T()
		G['destroylevel_check'] = False
		G['destroylevel_style'] = ''
		G['HACK_MOVES'] = 0
		G['HACK_INFINITY'] = 0
		G['movemap'] = L_T()
		restore = True
		if (restore_ is not None):
			restore = G['norestore_']
		if (restore is not None and restore is not False):
			G['newundo']()
			L_noop('clearunits')
			G['restoredefaults']()
	G['clearunits'] = f_clearunits
	def f_smallclear(*_):  # L70
		G['objectdata'] = L_T()
		G['deleted'] = L_T()
		G['updatelist'] = L_T()
		G['movelist'] = L_T()
		G['pushedunits'] = L_T()
		G['levelconversions'] = L_T()
		G['vision_rendered'] = L_T()
		G['poweredstatus'] = L_T()
		G['HACK_MOVES'] = 0
		G['movemap'] = L_T()
		if (L_len(G['units']) > 2000):
			G['destroylevel']('toocomplex')
			G['updateundo'] = True
	G['smallclear'] = f_smallclear
	def f_clear(*_):  # L89
		G['features'] = L_T()
		G['featureindex'] = L_T()
		G['condfeatureindex'] = L_T()
		G['visualfeatures'] = L_T()
		G['objectdata'] = L_T()
		G['deleted'] = L_T()
		G['ruleids'] = L_T()
		G['updatelist'] = L_T()
		G['wordunits'] = L_T()
		G['wordrelatedunits'] = L_T()
		G['letterunits_map'] = L_T()
		G['paradox'] = L_T()
		G['movelist'] = L_T()
		G['effecthistory'] = L_T()
		G['notfeatures'] = L_T()
		G['groupfeatures'] = L_T()
		G['groupmembers'] = L_T()
		G['pushedunits'] = L_T()
		G['condstatus'] = L_T()
		G['emptydata'] = L_T()
		G['leveldata'] = L_T()
		G['leveldata']['colours'] = L_T()
		G['leveldata']['currcolour'] = 0
		G['poweredstatus'] = L_T()
		G['visiontargets'] = L_T()
		G['vision_rendered'] = L_T()
		G['updatecode'] = 1
		G['updateundo'] = False
		G['hiddenmap'] = None
		G['levelconversions'] = L_T()
		G['maprotation'] = 0
		G['mapdir'] = 3
		G['last_key'] = 0
		G['auto_dir'] = L_T()
		G['destroylevel_check'] = False
		G['destroylevel_style'] = ''
		G['HACK_MOVES'] = 0
		G['HACK_INFINITY'] = 0
		G['movemap'] = L_T()
		L_noop()
	G['clear'] = f_clear
