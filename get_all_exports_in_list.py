import os
import sys
import pefile

def get_exports(dll_name):
    system32 = os.path.join(os.environ['WINDIR'], 'System32')
    dll_path = os.path.join(system32, dll_name)
    
    if not os.path.exists(dll_path):
        print(f"File {dll_path} does not exist")
        sys.exit(1)

    pe = pefile.PE(dll_path)

    exports = []
    for export in pe.DIRECTORY_ENTRY_EXPORT.symbols:
        if export.name:
            exports.append(export.name.decode('utf-8'))
    
    print(f"Exports recieved for {dll_name}")
    return exports

def save_to_file(exports, filename='all_exports.txt'):
    with open(filename, 'w', encoding='utf-8') as f:
        for func in exports:
            f.write(func + '\n')
    print(f"Saved {len(exports)} functions into {filename}")
    
INTERESTING_DLLS = [
    'kernel32.dll', 'comctl32.dll', 'advapi32.dll', 'comdlg32.dll', 'gdi32.dll', 
    'msvcrt.dll', 'netapi32.dll', 'ntdll.dll', 'ntoskrnl.exe', 'oleaut32.dll', 
    'psapi.dll', 'shell32.dll', 'shlwapi.dll', 'urlmon.dll', 'user32.dll', 
    'winhttp.dll', 'wininet.dll', 'ws2_32.dll', 'wship6.dll', 'advpack.dll', 
    'crypt32.dll', 'wsock32.dll'
]

if __name__ == '__main__':
    all_exports = []
    for dll in INTERESTING_DLLS:
        all_exports.extend(get_exports(dll))
    
    all_exports.sort()
    save_to_file(all_exports)