# api-hashing-db-ida

Plugin for IDA Pro (compatible with IDA Pro 9.2) is created to resolve API Hashing automaticaly. Plugin includes binary database that contains all exports of dlls used in malware and hashes for 3 algorithms.

# Usage

Add all files from lates Release to plugin directory of IDA Pro. Dump file is added to check the perfomance.

You can use Python scripts to create your own binary database.

```get_all_exports_in_list.py``` adding all export functions from specific dll to ```all_exports.txt```

```hash_module_name.py``` calculating DLLName hash using 1 of 3 algorithm. You may add result to the beginning of the ```all_exports.txt```

```calculate_all_hashes_in_DB_exports.py``` calculating hashes of exports, recieved from ```get_all_exports_in_list.py```

```pack_hashes_to_raw_bin.py``` packing .txt database to binary

```compress_script.py``` zlib compression of binary database

# pack_hashes_to_raw_bin_v2.py

Script includes functionality of ```pack_hashes_to_raw_bin.py``` and ```compress_script.py```. Combined script for working with binary hash database

# Usage

1. Create/update database:
```python script.py [--update] input.txt output.bin [--compress]```
2. Compress file only:
```python script.py --compress input.bin output.bin```

**Options:**

```--update```     Update existing database (only for database creation)

```--compress```   Compress output file after database creation
