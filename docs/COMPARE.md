# REA tools vs ikitaku strategy nodes

REA (morluto/rea) is a reverse-engineering MCP. It gives an agent probes
into binaries, apps, and runtime. Ikitaku is a reasoner. Its strategy
nodes are mental tools for the same question — why does this work —
applied to concepts and data, not to a binary.

| REA probe | what it returns | ikitaku node | what it returns |
|---|---|---|---|
| native decompile (Hopper/Ghidra/IDA) | pseudocode, calls, refs | rank ladder R0–R5 | surface ops → purpose |
| call graph / references | who calls whom | origin trace A→B→C | directed causal pair |
| strings / symbols | named evidence | English costume map | word → layer 5 verb |
| JS/Electron module graph | imports, IPC, routes | composition graph | outer/inner verb edges |
| browser observation | page, scripts, network | black-box trials | input/output residual |
| HAR / capture | requests and payloads | series fit | pattern, residual, conf |
| .NET / APK metadata | types, methods, manifest | object analysis | fields as attrs of a form |
| evidence bundle | claim + supporting artifact | hypothesis session | form, conf, english |

Shared shape: a probe returns evidence, not a verdict. The agent (or the
reasoner) decides. REA's evidence is bytes and calls. Ikitaku's evidence
is a scored form and a span.

What REA has that ikitaku does not:

- a real target (a file, a process, a page)
- a tool catalog with stable schemas
- evidence attached to each claim

What ikitaku has that REA does not:

- non-commutative composition (cycle-add ≠ add-cycle)
- a rank ladder from surface to purpose
- a compare of several hypotheses under a budget

The harness should treat ikitaku as one organ, the way REA treats Ghidra
as one provider. Call it when the task is a compare or a pattern read.
Do not call it to open a binary.
