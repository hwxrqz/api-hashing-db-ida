import zlib
import struct
import sys
import os

def compress_binary_file(input_file, output_file):
    """Compresses a binary file using zlib"""
    try:
        with open(input_file, 'rb') as f:
            original_data = f.read()
            
        compressed_data = zlib.compress(original_data)

        with open(output_file, 'wb') as f:
            f.write(compressed_data)

        print(f"Original size: {len(original_data)} bytes")
        print(f"Packed size: {len(compressed_data)} bytes")
        print(f"Compression ratio: {len(compressed_data)/len(original_data)*100:.1f}%")
        
    except Exception as e:
        print(f"Compression error: {e}")
        sys.exit(1)

def read_binary_database(bin_file):
    """Reads an existing binary database and returns a list of (hash_val, func_name)"""
    entries = []
    with open(bin_file, 'rb') as f:
        data = f.read()
        
    pos = 0
    # Read hash table entries
    while pos + 16 <= len(data):
        hash_val = struct.unpack('<I', data[pos:pos+4])[0]
        # Skip 4 bytes reserved
        offset = struct.unpack('<Q', data[pos+8:pos+16])[0]
        
        # Find the start of the string by offset
        str_start = offset
        str_end = str_start
        while str_end < len(data) and data[str_end] != 0:
            str_end += 1
        
        if str_end < len(data):
            func_name = data[str_start:str_end].decode('ascii')
            entries.append((hash_val, func_name))
        
        pos += 16
    
    return entries

def read_text_database(txt_file):
    """Reads a text database and returns a list of (func_name, hash_val)"""
    entries = []
    with open(txt_file, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            # Supports format "function_name:hash" or just hash (each line is a hash)
            if ':' in line:
                func_name, hash_str = line.split(':')
                entries.append((func_name.strip(), int(hash_str.strip(), 16)))
            else:
                # If no function name, use empty string
                entries.append(('', int(line.strip(), 16)))
    return entries

def create_binary_database(input_file, output_file, update=False):
    """Creates or updates a binary database"""
    
    # Read new text database
    new_entries = read_text_database(input_file)
    
    # If update mode and file exists, read old database
    if update and os.path.exists(output_file):
        old_entries = read_binary_database(output_file)
        
        # Create dictionaries for quick lookup
        # Key - hash_val, value - func_name
        old_hash_to_name = {}
        # Key - func_name, value - set(hash_values)
        old_name_to_hashes = {}
        
        for hash_val, func_name in old_entries:
            old_hash_to_name[hash_val] = func_name
            if func_name not in old_name_to_hashes:
                old_name_to_hashes[func_name] = set()
            old_name_to_hashes[func_name].add(hash_val)
        
        # Process new entries
        combined_entries = []
        name_to_hashes = old_name_to_hashes.copy()
        
        for func_name, hash_val in new_entries:
            # If hash already exists, skip
            if hash_val in old_hash_to_name:
                continue
            
            # If function name already exists in database, add only hash
            if func_name in name_to_hashes:
                # Check if this hash already exists for this name
                if hash_val not in name_to_hashes[func_name]:
                    combined_entries.append((hash_val, func_name))
                    name_to_hashes[func_name].add(hash_val)
            else:
                # Add new name-hash pair
                combined_entries.append((hash_val, func_name))
                name_to_hashes[func_name] = {hash_val}
        
        # Merge old and new entries
        all_entries = old_entries + combined_entries
        
    else:
        # Create new database from scratch (remove duplicates)
        unique_entries = {}
        for func_name, hash_val in new_entries:
            # Use hash as key to remove duplicates
            unique_entries[hash_val] = func_name
        
        all_entries = [(hash_val, func_name) for hash_val, func_name in unique_entries.items()]
    
    # Sort by hash
    all_entries.sort(key=lambda x: x[0])
    
    # Build mapping of function names to offsets
    name_to_offset = {}
    string_table = bytearray()
    current_offset = len(all_entries) * 16  # Start of string table
    
    # Iterate through sorted entries and create string table
    for hash_val, func_name in all_entries:
        if func_name not in name_to_offset:
            name_to_offset[func_name] = current_offset
            if func_name:  # If name is not empty
                string_table.extend(func_name.encode('ascii'))
            string_table.append(0x00)  # Null terminator
            current_offset += len(func_name) + 1
    
    # Write binary database
    with open(output_file, 'wb') as f:
        # Write hash table
        for hash_val, func_name in all_entries:
            f.write(struct.pack('<I', hash_val))  # Hash (4 bytes)
            f.write(b'\x00' * 4)  # Reserved (4 bytes)
            f.write(struct.pack('<Q', name_to_offset[func_name]))  # Offset (8 bytes)
        
        # Write string table
        f.write(string_table)
    
    return len(all_entries)

def main():
    if len(sys.argv) < 2:
        print("Combined script for working with binary hash database")
        print("\nUsage:")
        print("  1. Create/update database:")
        print("     python script.py [--update] input.txt output.bin [--compress]")
        print("  2. Compress file only:")
        print("     python script.py --compress input.bin output.bin")
        print("\nOptions:")
        print("  --update     Update existing database (only for database creation)")
        print("  --compress   Compress output file after database creation")
        sys.exit(1)
    
    # Check compression mode
    if sys.argv[1] == '--compress' and len(sys.argv) == 4:
        # Compression only mode
        input_file = sys.argv[2]
        output_file = sys.argv[3]
        
        if not os.path.exists(input_file):
            print(f"Error: Input file '{input_file}' not found")
            sys.exit(1)
            
        print(f"Compressing file {input_file} to {output_file}...")
        compress_binary_file(input_file, output_file)
        
    else:
        # Database creation/update mode
        update_mode = False
        compress_mode = False
        input_file = None
        output_file = None
        
        # Parse arguments
        i = 1
        while i < len(sys.argv):
            arg = sys.argv[i]
            if arg == '--update':
                update_mode = True
            elif arg == '--compress':
                compress_mode = True
            elif not input_file:
                input_file = arg
            elif not output_file:
                output_file = arg
            i += 1
        
        if not input_file or not output_file:
            print("Error: Input and/or output files not specified")
            print("Usage: python script.py [--update] input.txt output.bin [--compress]")
            sys.exit(1)
        
        if not os.path.exists(input_file):
            print(f"Error: Input file '{input_file}' not found")
            sys.exit(1)
        
        try:
            # Create/update database
            print(f"{'Updating' if update_mode else 'Creating'} database...")
            entry_count = create_binary_database(input_file, output_file, update_mode)
            print(f"Database successfully {'updated' if update_mode else 'created'}: {output_file}")
            print(f"Number of entries: {entry_count}")
            
            # If compression is requested
            if compress_mode:
                # Create temporary name for compressed file
                compressed_file = output_file + ".compressed"
                print(f"\nCompressing database...")
                compress_binary_file(output_file, compressed_file)
                
                # Replace original with compressed
                os.remove(output_file)
                os.rename(compressed_file, output_file)
                print(f"Compressed database saved to: {output_file}")
                
        except Exception as e:
            print(f"Error: {e}")
            sys.exit(1)

if __name__ == '__main__':
    main()