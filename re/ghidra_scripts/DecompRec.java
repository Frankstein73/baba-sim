// Decompile functions at the given addresses and their callees up to a depth, skipping ones already on disk.
// Args: <outdir> <depth> addr...
//@category BabaRE
import ghidra.app.script.GhidraScript;
import ghidra.app.decompiler.*;
import ghidra.program.model.listing.*;
import java.nio.file.*;
import java.util.*;

public class DecompRec extends GhidraScript {
    @Override
    public void run() throws Exception {
        String[] a = getScriptArgs();
        Path out = Paths.get(a[0]);
        int depth = Integer.parseInt(a[1]);
        Files.createDirectories(out);
        DecompInterface dec = new DecompInterface();
        dec.openProgram(currentProgram);
        Deque<Object[]> q = new ArrayDeque<>();
        Set<Function> seen = new HashSet<>();
        for (int i = 2; i < a.length; i++) {
            Function f = currentProgram.getFunctionManager().getFunctionContaining(toAddr(Long.decode(a[i])));
            if (f == null) { println("no function at " + a[i]); continue; }
            if (seen.add(f)) q.add(new Object[]{f, 0});
        }
        int n = 0;
        while (!q.isEmpty()) {
            Object[] e = q.poll();
            Function f = (Function) e[0];
            int d = (Integer) e[1];
            Path p = out.resolve(f.getEntryPoint() + ".c");
            if (!Files.exists(p) && f.getBody().getNumAddresses() < 60000) {
                DecompileResults r = dec.decompileFunction(f, 300, monitor);
                Files.writeString(p, r.decompileCompleted() ? r.getDecompiledFunction().getC() : "// FAILED " + r.getErrorMessage());
                n++;
            }
            if (d < depth) {
                for (Function c : f.getCalledFunctions(monitor)) {
                    if (c.isThunk() || c.isExternal()) continue;
                    if (seen.add(c)) q.add(new Object[]{c, d + 1});
                }
            }
        }
        println("decompiled " + n + ", visited " + seen.size());
    }
}
