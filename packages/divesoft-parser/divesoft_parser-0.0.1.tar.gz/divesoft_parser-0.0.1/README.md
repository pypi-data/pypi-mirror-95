Divesoft Log Parser
===================

Python parser for Divesoft Freedom (DLF) log files.

## Example usage

```python3
from divesoft_parser import DLFDecoder

dive = DLFDecoder.from_file('00000001.DLF')
print(dive.serial)
```

## Support Notes

The majority of testing has been done against open circuit dive logs from a 3.0 computer,
little support exists for CCR specific data e.g. setpoints, cell calibration etc.

## Implementation references

- https://github.com/subsurface/libdc
- https://wetnotes.com/
- Wetnotes Desktop
