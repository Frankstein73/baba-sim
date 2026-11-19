// Decompile the functions at the given addresses into <outdir>/<addr>.c. Args: <outdir> addr...
//@category BabaRE
import ghidra.app.script.GhidraScript;
import ghidra.app.decompiler.*;
import ghidra.program.model.listing.*;
import java.nio.file.*;

public class Decomp extends GhidraScript {
    @Override
    public void run() throws Exception {
        String[] a = getScriptArgs();
        Path out = Paths.get(a[0]);
        Files.createDirectories(out);
        DecompInterface dec = new DecompInterface();
        dec.openProgram(currentProgram);
        for (int i = 1; i < a.length; i++) {
            Function f = currentProgram.getFunctionManager().getFunctionContaining(toAddr(Long.decode(a[i])));
            if (f == null) { println("no function at " + a[i]); continue; }
            DecompileResults r = dec.decompileFunction(f, 600, monitor);
            Files.writeString(out.resolve(f.getEntryPoint() + ".c"),
                r.decompileCompleted() ? r.getDecompiledFunction().getC() : "// FAILED " + r.getErrorMessage());
        }
    }
}
