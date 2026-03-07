import zlib
import sys

def compress_binary_file(input_file, output_file):
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

if __name__ == '__main__':
    #Usage: python compress_script.py input.bin output.bin    
    compress_binary_file(sys.argv[1], sys.argv[2])