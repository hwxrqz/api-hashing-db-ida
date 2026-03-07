import struct
import sys

def create_binary_database(input_file, output_file):
    entries = []
    with open(input_file, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            func_name, hash_str = line.split(':')
            entries.append((func_name, int(hash_str, 16)))

    entries.sort(key=lambda x: x[1])

    offset = len(entries) * 16  # offset to Name section
    hash_table = []
    string_table = bytearray()

    for func_name, hash_val in entries:
        hash_table.append((hash_val, offset)) # Adding values to Hash table
        
        string_table.extend(func_name.encode('ascii')) # Adding value to Name Section
        string_table.append(0x00)  # End of value
        
        offset += len(func_name) + 1 # Update offset

    with open(output_file, 'wb') as f:
        # Write Hash table
        for hash_val, offset_val in hash_table:
            # Hash 4 bytes little-endian + 4 bytes Reserved
            f.write(struct.pack('<I', hash_val))
            f.write(b'\x00' * 4)
            # Offset 8 bytes little-endian)
            f.write(struct.pack('<Q', offset_val))
        
        f.write(string_table)   # Write Name section

if __name__ == '__main__':
    # Usage: script.py input.txt output.bin  
    create_binary_database(sys.argv[1], sys.argv[2])
    print(f"Binary DataBase has created: {sys.argv[2]}")