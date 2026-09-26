# cython: language_level=3
# distutils: language = c++

from libcpp.string cimport string

cdef extern from *:
    """
    #include <string>
    #include <cctype>

    struct FastStats {
        long lines;
        long words;
        long chars;
    };

    inline FastStats process_text_cpp(const std::string& text) {
        FastStats stats = {0, 0, (long)text.length()};
        bool in_word = false;
        
        for (char c : text) {
            if (c == '\n') stats.lines++;
            if (std::isspace(static_cast<unsigned char>(c))) {
                in_word = false;
            } else if (!in_word) {
                in_word = true;
                stats.words++;
            }
        }
        if (text.length() > 0 && text.back() != '\n') {
            stats.lines++;
        }
        return stats;
    }
    """
    struct FastStats:
        long lines
        long words
        long chars
    FastStats process_text_cpp(string text)

def analyze_code_fast(str text_data):
    """Швидка обробка тексту через C++"""
    cdef string c_text = text_data.encode('utf-8')
    cdef FastStats stats = process_text_cpp(c_text)
    return {
        "lines": stats.lines,
        "words": stats.words,
        "chars": stats.chars
    }