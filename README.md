# F-I-M-S

Simple file integrity management system.

## Usage

Initialize a baseline hash database:

```bash
python /home/runner/work/F-I-M-S/F-I-M-S/fims.py init /path/to/monitor --baseline baseline.json
```

Scan files against the baseline:

```bash
python /home/runner/work/F-I-M-S/F-I-M-S/fims.py scan /path/to/monitor --baseline baseline.json
```