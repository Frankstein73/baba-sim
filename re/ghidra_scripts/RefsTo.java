// Print every reference to the given addresses (args), with source function and type.
//@category BabaRE
import ghidra.app.script.GhidraScript;
import ghidra.program.model.listing.*;
import ghidra.program.model.symbol.*;
import ghidra.program.model.address.*;

public class RefsTo extends GhidraScript {
    @Override
    public void run() throws Exception {
        FunctionManager fm = currentProgram.getFunctionManager();
        for (String s : getScriptArgs()) {
            Address a = toAddr(Long.decode(s));
            println("== " + a + " " + fm.getFunctionAt(a));
            for (Reference r : currentProgram.getReferenceManager().getReferencesTo(a)) {
                Function f = fm.getFunctionContaining(r.getFromAddress());
                println("   from " + r.getFromAddress() + " in " + (f == null ? "-" : f.getName() + "@" + f.getEntryPoint()) + " " + r.getReferenceType());
            }
        }
    }
}
