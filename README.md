# Sysdig AuditTrail: Unveiling Linux System Behavior with an Advanced Auditing Tool
## CSE 545 Software Security
An auditing tool that helps in backtracking Linux system behavior using logs obtained from Sysdig logger tool.
## Run commands:
### Parse log:
```bash
python LogParser.py
```
### Create Initial Graph:
```bash
python GraphGenerator.py
dot -Tsvg initialGraph.dot > initialOutput.svg
```
### Create Backtrack Graph:
```bash
python Backtrack.py
dot -Tsvg backtrackGraph.dot > backtrackOutput.svg
```


