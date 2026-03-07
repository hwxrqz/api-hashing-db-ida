def ApiHash(name):
    hash_value = 0
    position = 0
    
    for char in name:
        # Преобразование символа в нижний регистр (как в C++ коде)
        char_code = ord(char)
        if char_code < ord('a'):
            char_code += 32
        
        # Вычисление temp в зависимости от четности position
        if position & 1:
            temp = ~(char_code ^ (hash_value >> 3) ^ (hash_value << 9)) & 0xFFFFFFFF
        else:
            temp = char_code ^ (hash_value >> 1) ^ (32 * hash_value)
        
        # Обновление hash_value
        hash_value = (hash_value ^ temp) & 0xFFFFFFFF
        position += 1
    
    return hash_value & 0x7FFFFFFF
    
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

INTERESTING_DLLS = [
    'kernel32.dll', 'comctl32.dll', 'advapi32.dll', 'comdlg32.dll', 
    'gdi32.dll', 'msvcrt.dll', 'netapi32.dll', 'ntdll.dll', 
    'ntoskrnl.exe', 'oleaut32.dll', 'psapi.dll', 'shell32.dll', 
    'shlwapi.dll', 'urlmon.dll', 'user32.dll', 'winhttp.dll', 
    'wininet.dll', 'ws2_32.dll', 'wship6.dll', 'advpack.dll', 
    'crypt32.dll', 'crypt.dll', 'wsock32.dll'
]

for dll in INTERESTING_DLLS:
    print(dll + ':' + hex(ApiHash(dll))[2:].upper())