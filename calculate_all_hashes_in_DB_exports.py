def ApiHash(name):
    hash_value = 0
    position = 0
    
    for char in name:
        char_code = ord(char)
        if char_code < ord('a'):
            char_code += 32
        
        if position & 1:
            temp = ~(char_code ^ (hash_value >> 3) ^ (hash_value << 9)) & 0xFFFFFFFF
        else:
            temp = char_code ^ (hash_value >> 1) ^ (32 * hash_value)
        
        hash_value = (hash_value ^ temp) & 0xFFFFFFFF
        position += 1
    
    return hash_value & 0x7FFFFFFF
    
def ApiHash_func(name):
    v5 = 0  # hash accumulator
    v1 = 0  # counter
    
    for char in name:
        v6 = ord(char)
        
        if v1 & 1:
            v8 = (~(v6 ^ (v5 >> 3) ^ (v5 << 9))) & 0xFFFFFFFF
        else:
            v8 = (v6 ^ (v5 >> 1) ^ (32 * v5)) & 0xFFFFFFFF
        
        v5 = (v5 ^ v8) & 0xFFFFFFFF
        v1 += 1
    
    return v5 & 0x7FFFFFFF
    
def compute_api_hash2(api_name: str) -> int:
    hash_val = 0x4230
    for c in api_name:
        hash_val = (ord(c) + 0x7313 * hash_val) & 0xFFFFFFFF
    return (hash_val ^ 0xAB98) & 0xFFFFFFFF    
    
def djb2_custom_hash(input_string, max_length=0):
    result = 0x1505
    
    if isinstance(input_string, str):
        input_bytes = input_string.encode('latin-1')
    else:
        input_bytes = input_string
    
    for i, char_byte in enumerate(input_bytes):
        if max_length > 0 and i >= max_length:
            break
            
        byte = char_byte
        
        if byte == 0:
            break
            
        if byte >= 0x61 and byte <= 0x7A:  # 'a' to 'z'
            byte -= 0x20
        
        result = (32 * (result & 0xFFFFFFFF) + byte + (result & 0xFFFFFFFF)) & 0xFFFFFFFF
    
    return result


with open('all_exports.txt', 'r') as f:
    functions = [line.strip() for line in f.readlines()]

with open('all_exports_api_hashes.txt', 'w') as out_file:
    for func in functions:
        h = hex(ApiHash1(func))[2:].upper()
        out_file.write(f"{func}:{h}\n")