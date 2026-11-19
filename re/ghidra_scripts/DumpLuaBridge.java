// Headless: for every defined string that names a Lua global (function names from the game's
// Lua + MF_* natives), find code xrefs, and decompile each referencing function once.
// Output: <outdir>/xrefs.tsv (string, ref addr, func addr, func name) and <outdir>/funcs/<addr>.c
//@category BabaRE
import ghidra.app.script.GhidraScript;
import ghidra.app.decompiler.*;
import ghidra.program.model.data.StringDataInstance;
import ghidra.program.model.listing.*;
import ghidra.program.model.symbol.*;
import ghidra.program.model.address.*;
import ghidra.program.model.mem.*;
import java.io.*;
import java.nio.file.*;
import java.util.*;

public class DumpLuaBridge extends GhidraScript {
    @Override
    public void run() throws Exception {
        String[] args = getScriptArgs();
        Path names = Paths.get(args[0]);
        Path out = Paths.get(args[1]);
        Files.createDirectories(out.resolve("funcs"));
        Set<String> wanted = new HashSet<>(Files.readAllLines(names));

        DecompInterface dec = new DecompInterface();
        dec.openProgram(currentProgram);
        Listing listing = currentProgram.getListing();
        ReferenceManager rm = currentProgram.getReferenceManager();
        FunctionManager fm = currentProgram.getFunctionManager();
        Set<Address> done = new HashSet<>();

        Memory mem = currentProgram.getMemory();
        try (PrintWriter tsv = new PrintWriter(Files.newBufferedWriter(out.resolve("xrefs.tsv")))) {
            // Every referenced address: read a C string there (handles tail-merged literals,
            // where "block" is the last 6 bytes of "startblock\0").
            AddressIterator dests = rm.getReferenceDestinationIterator(currentProgram.getMinAddress(), true);
            while (dests.hasNext() && !monitor.isCancelled()) {
                Address a = dests.next();
                MemoryBlock blk = mem.getBlock(a);
                if (blk == null || blk.isExecute() || !blk.isInitialized()) continue;
                StringBuilder sb = new StringBuilder();
                boolean ok = true;
                for (int i = 0; i < 64; i++) {
                    byte b;
                    try { b = mem.getByte(a.add(i)); } catch (Exception e) { ok = false; break; }
                    if (b == 0) break;
                    if (b < 0x20 || b > 0x7e) { ok = false; break; }
                    sb.append((char) b);
                }
                String s = sb.toString();
                if (!ok || !wanted.contains(s)) continue;
                for (Reference r : rm.getReferencesTo(a)) {
                    Function f = fm.getFunctionContaining(r.getFromAddress());
                    String fa = f == null ? "-" : f.getEntryPoint().toString();
                    tsv.printf("%s\t%s\t%s\t%s\t%s%n", s, r.getFromAddress(), fa, f == null ? "-" : f.getName(), r.getReferenceType());
                    if (f != null && done.add(f.getEntryPoint())) {
                        DecompileResults res = dec.decompileFunction(f, 300, monitor);
                        String c = res.decompileCompleted() ? res.getDecompiledFunction().getC() : "// FAILED: " + res.getErrorMessage();
                        Files.writeString(out.resolve("funcs/" + fa + ".c"), c);
                    }
                }
            }
        }
        println("decompiled " + done.size() + " functions");
    }
}
