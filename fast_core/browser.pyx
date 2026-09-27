# distutils: language = c++
from libcpp.string cimport string

# Імпортуємо C++ клас
cdef extern from "browser_engine.h":
    cdef cppclass BrowserEngine:
        BrowserEngine() except +
        string fetch_url(string url)
        string search_github_repo(string query)
        string search_pypi_package(string query)

# Створюємо Python-клас обгортку
cdef class FastBrowser:
    cdef BrowserEngine* _engine

    def __cinit__(self):
        self._engine = new BrowserEngine()

    def __dealloc__(self):
        if self._engine != NULL:
            del self._engine

    def fetch(self, str url):
        cdef string c_url = url.encode('utf-8')
        return self._engine.fetch_url(c_url).decode('utf-8')

    def search_github(self, str query):
        cdef string c_query = query.encode('utf-8')
        return self._engine.search_github_repo(c_query).decode('utf-8')
        
    def search_pypi(self, str query):
        cdef string c_query = query.encode('utf-8')
        return self._engine.search_pypi_package(c_query).decode('utf-8')