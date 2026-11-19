// Label recovered global std::string objects (re/out/globals_str.tsv) as s_<value>, then
// decompile every function that references a global whose value is a Lua/MF_ name.
// Args: <globals_str.tsv> <lua_names.txt> <outdir>
//@category BabaRE
import ghidra.app.script.GhidraScript;
import ghidra.app.decompiler.*;
import ghidra.program.model.listing.*;
import ghidra.program.model.symbol.*;
import ghidra.program.model.address.*;
import java.io.*;
import java.nio.file.*;
import java.util.*;

public class LabelStringsAndDump extends GhidraScript {
    @Override
    public void run() throws Exception {
        String[] a = getScriptArgs();
        List<String> rows = Files.readAllLines(Paths.get(a[0]));
        Set<String> wanted = new HashSet<>(Files.readAllLines(Paths.get(a[1])));
        Path out = Paths.get(a[2]);
        Files.createDirectories(out.resolve("funcs2"));
        SymbolTable st = currentProgram.getSymbolTable();
        ReferenceManager rm = currentProgram.getReferenceManager();
        FunctionManager fm = currentProgram.getFunctionManager();
        Map<Address, String> wantedAddrs = new LinkedHashMap<>();
        int labeled = 0;
        for (String row : rows) {
            String[] f = row.split("\t");
            Address addr = toAddr(Long.decode(f[0]));
            String v = f[3];
            v = v.substring(1, v.length() - 1);  // strip python repr quotes
            String label = "s_" + v.replaceAll("[^A-Za-z0-9_]", "_");
            if (label.length() > 60) label = label.substring(0, 60);
            st.createLabel(addr, label, SourceType.USER_DEFINED);
            labeled++;
            if (wanted.contains(v)) wantedAddrs.put(addr, v);
        }
        DecompInterface dec = new DecompInterface();
        dec.openProgram(currentProgram);
        Set<Address> done = new HashSet<>();
        try (PrintWriter tsv = new PrintWriter(Files.newBufferedWriter(out.resolve("xrefs2.tsv")))) {
            for (Map.Entry<Address, String> e : wantedAddrs.entrySet()) {
                for (Reference r : rm.getReferencesTo(e.getKey())) {
                    Function fn = fm.getFunctionContaining(r.getFromAddress());
                    String fa = fn == null ? "-" : fn.getEntryPoint().toString();
                    tsv.printf("%s\t%s\t%s\t%s%n", e.getValue(), r.getFromAddress(), fa, r.getReferenceType());
                    if (fn != null && done.add(fn.getEntryPoint())) {
                        DecompileResults res = dec.decompileFunction(fn, 600, monitor);
                        String c = res.decompileCompleted() ? res.getDecompiledFunction().getC() : "// FAILED: " + res.getErrorMessage();
                        Files.writeString(out.resolve("funcs2/" + fa + ".c"), c);
                    }
                }
            }
        }
        println("labeled " + labeled + ", wanted " + wantedAddrs.size() + ", decompiled " + done.size());
    }
}
