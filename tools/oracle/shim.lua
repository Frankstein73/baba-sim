-- Dev-only oracle: stand-ins for the native side so the original Lua can run headless.
-- Call order of the Lua entry points follows re/NATIVE_TURN_LOOP.md.
-- Requires the game's Lua directory in ORACLE_GAME (never shipped with the engine).

local GAME = ORACLE_GAME

local function norm(v)
	if (type(v) == "number") then
		return math.tointeger(v) or v
	end
	return v
end

-- natives hand integral doubles back to Lua as integers; mirror that on write
local function deftable(default)
	local raw = {}
	return setmetatable({}, {
		__index = function(_, k) local v = raw[k]; if (v == nil) then return default end; return v end,
		__newindex = function(_, k, v) raw[k] = norm(v) end,
		__raw = raw,
	})
end

print = function() end
ORACLE = {objs = {}, order = {}, nextfixed = 0, won = false, alerts = {}, missing = {}, ld = {}, world = {}, tiles = {}}
local O = ORACLE

local function newobj(class)
	O.nextfixed = O.nextfixed + 1
	local fixed = O.nextfixed
	local obj = {
		values = deftable(0), strings = deftable(""), flags = deftable(false),
		fixed = fixed, className = class, x = 0, y = 0, visible = true, layer = 1,
		scaleX = 1, scaleY = 1, angle = 0, direction = 0, colour = {},
	}
	O.objs[fixed] = obj
	return obj
end

mmf = {newObject = function(fixed) return O.objs[fixed] end}

-- TileMap: only layer 0 keeps tiles after load (the level edge, tile 0,0); 255 = empty
local tilemap = {}
local function newlayer(l)
	return {
		get_x = function(_, x, y) local t = O.tiles[l .. ":" .. x .. "," .. y]; return t and t[1] or 255 end,
		get_y = function(_, x, y) local t = O.tiles[l .. ":" .. x .. "," .. y]; return t and t[2] or 255 end,
		set_x = function() end, set_tile = function() end, unset_tile = function() end,
	}
end
for l = 0, 2 do tilemap[l] = newlayer(l) end
TileMap = {new = function() return tilemap end}

function MF_create(class)
	local obj = newobj(class)
	obj.values[ID] = -1
	return obj.fixed
end

function MF_emptycreate(class, x, y)
	local fixed = MF_create(class)
	setundo(1)
	return fixed
end

function MF_specialcreate(class) return MF_create(class) end
function MF_effectcreate(class) return MF_create(class) end

local function destroy(fixed) O.objs[fixed] = nil end
function MF_remove(fixed) destroy(fixed); setundo(1) end
function MF_specialremove(fixed, kind) destroy(fixed); setundo(1) end
function MF_cleanremove(fixed)
	local obj = O.objs[fixed]
	if (obj ~= nil) then obj.flags[DEAD] = true end
	destroy(fixed)
end

function MF_getfixed(id)
	for _, unit in ipairs(units) do
		if (unit.values[ID] == id) and (unit.flags[DEAD] == false) then return unit.fixed end
	end
	return nil
end
function MF_findfixed(fixed) if (O.objs[fixed] ~= nil) then return fixed end return nil end
function MF_totalunitcount() return #units end
function MF_getunits() local r = {}; for _, u in ipairs(units) do r[#r + 1] = u.fixed end; return r end

function MF_alert(s) O.alerts[#O.alerts + 1] = tostring(s) end
function MF_win() O.won = true end
function MF_restart() O.restart = true end
function MF_random(a, b) return math.random(a, b) end
function MF_parsestring(s)
	local r = {}
	for part in string.gmatch(s or "", "[^,]+") do r[#r + 1] = part end
	return r
end
function MF_read(file, section, key)
	local src = (file == "level") and O.ld or ((file == "world") and O.world or nil)
	if (src == nil) or (src[section] == nil) then return "" end
	return src[section][key] or ""
end
function MF_update() ORACLE_turngroup(1) end
function MF_findpaths() return {} end
function MF_findgates() return {} end
function MF_findlevelunit() return {} end

-- the shipped Lua 5.3 is built with the 5.1/5.2 compatibility library
math.atan2 = math.atan2 or math.atan
math.pow = math.pow or function(a, b) return a ^ b end
unpack = unpack or table.unpack
loadstring = loadstring or load
function fixed_to_str(x) return tostring(x) end

-- every other MF_* native is audio/visual/menu: no-op, but remember which ones were hit
setmetatable(_G, {__index = function(_, k)
	if (type(k) == "string") and (string.sub(k, 1, 3) == "MF_") then
		O.missing[k] = (O.missing[k] or 0) + 1
		return function() return nil end
	end
	return nil
end})

for _, f in ipairs(ORACLE_FILES) do
	local chunk, err = loadfile(GAME .. "/" .. f)
	if (chunk == nil) then error(err) end
	chunk()
end

local function dataobj() return newobj("data").fixed end

function ORACLE_boot(world)
	local ids = {}
	for i = 1, 14 do ids[i] = dataobj() end
	init(0, 35, 20, 24, 0, 0, ids[1], ids[2], ids[3], ids[4], ids[5], ids[6], ids[7], 854, 480)
	setupmenu(ids[8], ids[9], ids[10], ids[11], ids[12], ids[13], true)
	generaldata.strings[WORLD] = world
	generaldata.strings[BASEWORLD] = "baba"
	generaldata.values[MODE] = 0
	spritedata.values[TILEMULT] = 1
	generaldata2.values[ZOOM] = 1
	editor.strings[MENU] = "ingame"
	worldinit()
end

-- level = {name=, width=, height=, cells = {{x,y,layer,tx,ty,dir}, ...} in file order}
function ORACLE_loadlevel(level)
	O.won = false
	O.restart = false
	O.tiles = {}
	clearunits()
	clear()
	local seeding = tonumber(MF_read("level", "general", "seeding"))
	if (seeding ~= nil) then setseedingtype(seeding) else setseedingtype(0) end
	generaldata.strings[CURRLEVEL] = level.name
	generaldata.values[ROOMSIZEX] = level.width
	generaldata.values[ROOMSIZEY] = level.height
	roomsizex, roomsizey = level.width, level.height
	local custom = MF_read("level", "general", "customobjects")
	if (#custom > 0) then loadcustomobjects(custom) end
	-- FUN_1001ab590: each redefined object is created once so addchange() reads its [tiles] entries
	restoredefaults()
	if (#MF_read("level", "tiles", "changed") > 0) then
		local lists = math.max(tonumber(MF_read("level", "tiles", "changed_count")) or 1, 1)
		for i = 1, lists do
			local id = "changed"
			if (i > 1) then id = id .. tostring(i) end
			for target in string.gmatch(MF_read("level", "tiles", id), "%w+") do
				if (tileslist[target] ~= nil) then
					local fixed = MF_create(target)
					addchange(fixed)
					MF_cleanremove(fixed)
				end
			end
		end
		handleobjectchanges()
	end

	local bycell = {}
	for _, c in ipairs(level.cells) do
		bycell[c[1] .. "," .. c[2] .. "," .. c[3]] = c
	end
	for x = 0, level.width - 1 do
		for y = 0, level.height - 1 do
			for l = 0, 2 do
				local c = bycell[x .. "," .. y .. "," .. l]
				if (c ~= nil) then
					if (c[4] > 0) or (c[5] > 0) then
						local class = loadtile(c[4], c[5])
						local obj = newobj(class)
						obj.values[ID] = -1
						obj.values[XPOS] = x
						obj.values[YPOS] = y
						obj.values[DIR] = c[6]
						obj.values[ONLINE] = 1
						obj.flags[9] = true
						addunit(obj.fixed, nil, true)
					else
						O.tiles[l .. ":" .. x .. "," .. y] = {c[4], c[5]}
					end
				end
			end
		end
	end

	-- FUN_1001b1dc0: seed text is CURRLEVEL .. LEVELNAME
	generaldata.strings[LEVELNAME] = MF_read("level", "general", "name")
	setfixedrandom(level.name .. generaldata.strings[LEVELNAME])
	pcall(overrideundoseeding)

	code()
	undostate(false)
	startblock()
	animate()
	clear()
	undostate(true)
	code()
	do_mod_hook("level_start")
end

function ORACLE_turngroup(v)
	generaldata.values[UPDATE] = v
	doupdate(); smallclear(); setunitmap()
	code()
	if (v == 1) then
		updateeffecthistory(); fallblock(); doupdate(); code(); statusblock(); domaprotation()
	else
		reseteffecthistory(); statusblock(nil, true)
	end
	if (v == 1) then
		conversion(true); fallblock()
	end
	doupdate(); code()
	if (v == 1) then
		levelblock(); block(); dolevelconversions()
	end
	for _, unit in ipairs(units) do unit.flags[CONVERTED] = false end
	doupdate(); smallclear(); setunitmap()
	code(); findplayer(v); checkturnsound()
	effectblock(); diceblock()
	if (v == 1) then
		shorteffectblock(); groupcheck(); destroylevel_do()
	end
	update_cleanup()
	if (v == 1) then
		for _, unit in ipairs(units) do
			unit.values[MOVED] = math.max(0, unit.values[MOVED] - 1)
			unit.values[PUSHED] = 4
		end
		generaldata.values[UPDATE] = 0
		newundo(); animate(); cleanup(); do_mod_hook("turn_end")
	else
		generaldata.values[UPDATE] = 0
		animate(); cleanup()
	end
end

function ORACLE_seed(n) math.randomseed(n) end

function ORACLE_command(key) command(key, 1) end

function ORACLE_undo()
	dolog("undo")
	undo()
	ORACLE_turngroup(2)
end

-- flat snapshot in units order: {name, x, y, dir, id, float, ...}
function ORACLE_state()
	local out = {}
	for i, unit in ipairs(units) do
		out[i] = {unit.strings[UNITNAME], unit.values[XPOS], unit.values[YPOS], unit.values[DIR],
			unit.values[ID], unit.values[FLOAT], unit.strings[UNITTYPE], unit.className, unit.values[ZLAYER]}
	end
	return out
end

function ORACLE_rules()
	local out = {}
	for _, f in ipairs(features) do
		local r = f[1]
		local conds = {}
		for _, c in ipairs(f[2] or {}) do conds[#conds + 1] = tostring(c[1]) end
		out[#out + 1] = {r[1], r[2], r[3], table.concat(conds, ",")}
	end
	return out
end
