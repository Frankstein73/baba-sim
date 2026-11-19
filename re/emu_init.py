"""Run the binary's static initializers in Unicorn and recover every global string object.

Short std::string globals are built from immediates (no __cstring reference), so the only way
to learn which global holds "block" is to execute the initializers and read memory afterwards.
Output: re/out/globals_str.tsv  (address, length, value)
"""

import struct
import subprocess
import sys
from pathlib import Path

from unicorn import UC_ARCH_X86, UC_HOOK_CODE, UC_MODE_64, Uc, UcError
from unicorn.x86_const import (UC_X86_REG_RAX, UC_X86_REG_RDI, UC_X86_REG_RDX, UC_X86_REG_RIP,
                               UC_X86_REG_RSI, UC_X86_REG_RSP)

BIN = Path(__file__).parent / "bin/Chowdren"
OUT = Path(__file__).parent / "out"
data = BIN.read_bytes()

SEGS = [  # vmaddr, vmsize, fileoff, filesize  (from otool -l)
    (0x100000000, 0x690000, 0, 6881280),
    (0x100690000, 0x1C000, 6881280, 114688),
    (0x1006AC000, 0x366000, 6995968, 491520),
]
INIT_ARRAY = (0x100690348, 0xB8)
STACK, STACK_SZ = 0x7F0000000000, 0x100000
HEAP, HEAP_SZ = 0x200000000, 0x4000000
RET_SENTINEL = 0x300000000

stubs = {}
for line in subprocess.run(["otool", "-Iv", str(BIN)], capture_output=True, text=True).stdout.splitlines():
    parts = line.split()
    if len(parts) == 3 and parts[0].startswith("0x"):
        stubs[int(parts[0], 16)] = parts[2]
STUB_LO, STUB_HI = min(stubs), max(stubs) + 6

mu = Uc(UC_ARCH_X86, UC_MODE_64)
for va, vs, fo, fs in SEGS:
    mu.mem_map(va, vs)
    mu.mem_write(va, data[fo:fo + fs])
mu.mem_map(0, 0x200000)  # unbound GOT entries are 0; let reads through them land on zeros
mu.mem_map(STACK, STACK_SZ)
mu.mem_map(HEAP, HEAP_SZ)
mu.mem_map(RET_SENTINEL, 0x1000)
heap_top = HEAP
atexit = []  # (dtor, obj)
unknown = {}


def malloc(n):
    global heap_top
    p = heap_top
    heap_top += (n + 15) & ~15
    return p


def ret(uc, value=None):
    if value is not None:
        uc.reg_write(UC_X86_REG_RAX, value)
    rsp = uc.reg_read(UC_X86_REG_RSP)
    uc.reg_write(UC_X86_REG_RIP, struct.unpack("<Q", uc.mem_read(rsp, 8))[0])
    uc.reg_write(UC_X86_REG_RSP, rsp + 8)


def hook(uc, addr, size, _):
    if addr == RET_SENTINEL:
        uc.emu_stop()
        return
    if not (STUB_LO <= addr < STUB_HI):
        return
    name = stubs.get(addr, f"?{addr:x}")
    rdi, rsi, rdx = (uc.reg_read(r) for r in (UC_X86_REG_RDI, UC_X86_REG_RSI, UC_X86_REG_RDX))
    if name == "___cxa_atexit":
        atexit.append((rdi, rsi))
        ret(uc, 0)
    elif name in ("__Znwm", "__Znam", "_malloc"):
        ret(uc, malloc(rdi))
    elif name in ("_memcpy", "_memmove", "___memcpy_chk", "___memmove_chk"):
        uc.mem_write(rdi, bytes(uc.mem_read(rsi, rdx)))
        ret(uc, rdi)
    elif name in ("_memset", "___memset_chk"):
        uc.mem_write(rdi, bytes([rsi & 0xFF]) * rdx)
        ret(uc, rdi)
    elif name in ("___bzero", "_bzero"):
        uc.mem_write(rdi, bytes(rsi))
        ret(uc)
    elif name == "_strlen":
        n = 0
        while uc.mem_read(rdi + n, 1)[0]:
            n += 1
        ret(uc, n)
    else:
        unknown[name] = unknown.get(name, 0) + 1
        ret(uc, 0)


mu.hook_add(UC_HOOK_CODE, hook)
mu.mem_write(RET_SENTINEL, b"\x90")
inits = struct.unpack_from(f"<{INIT_ARRAY[1] // 8}Q", data, INIT_ARRAY[0] - 0x100690000 + 6881280)
for fn in inits:
    rsp = STACK + STACK_SZ - 0x1000
    mu.mem_write(rsp, struct.pack("<Q", RET_SENTINEL))
    mu.reg_write(UC_X86_REG_RSP, rsp)
    try:
        mu.emu_start(fn, RET_SENTINEL + 1)
    except UcError as e:
        print(f"init {fn:#x}: {e} at {mu.reg_read(UC_X86_REG_RIP):#x}", file=sys.stderr)

# dtor most used by atexit = the string destructor
from collections import Counter
dtors = Counter(d for d, _ in atexit)
print("atexit calls:", len(atexit), "top dtors:", [(hex(d), n) for d, n in dtors.most_common(4)])
print("unknown stubs:", unknown)
STRING_DTOR = dtors.most_common(1)[0][0]


def read_string(obj):
    raw = bytes(mu.mem_read(obj, 24))
    if raw[0] & 1 == 0:  # libc++ short: size<<1 in byte 0, chars from byte 1
        n = raw[0] >> 1
        return raw[1:1 + n] if n <= 22 else None
    cap, n, ptr = struct.unpack("<QQQ", raw)
    if n > 1 << 20:
        return None
    try:
        return bytes(mu.mem_read(ptr, n))
    except UcError:
        return None


OUT.mkdir(exist_ok=True)
rows = 0
with open(OUT / "globals_str.tsv", "w") as f:
    for dtor, obj in atexit:
        if dtor != STRING_DTOR:
            continue
        s = read_string(obj)
        if s is None:
            continue
        f.write(f"{obj:#x}\t{dtor:#x}\t{len(s)}\t{s.decode('latin1')!r}\n")
        rows += 1
print("strings:", rows)
