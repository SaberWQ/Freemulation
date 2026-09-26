# cython: language_level=3
from libc.stdio cimport FILE, fopen, fread, fclose

def fast_hex_dump(str filepath, int max_bytes=4096):
    cdef bytes py_bytes = filepath.encode('utf-8')
    cdef char* filename = py_bytes
    cdef FILE* file = fopen(filename, "rb")
    if file == NULL:
        return "Помилка відкриття файлу"

    cdef unsigned char buffer[4096]
    cdef size_t bytes_read = fread(buffer, 1, max_bytes, file)
    fclose(file)

    cdef list result = []
    cdef size_t i, j
    cdef str line, hex_part, ascii_part

    for i from 0 <= i < bytes_read by 16:
        hex_part = " ".join([f"{buffer[i+j]:02X}" for j in range(min(16, bytes_read - i))])
        ascii_part = "".join([chr(buffer[i+j]) if 32 <= buffer[i+j] <= 126 else "." for j in range(min(16, bytes_read - i))])
        result.append(f"{i:08X}  {hex_part:<48}  |{ascii_part}|")

    return "\n".join(result)