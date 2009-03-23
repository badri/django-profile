'''
TODO:
# create and load custom fixtures
# how to add files in fixtures?
'''
from utils.fileFilter import tests as fileFilterTests
__test__ = {
    'fileFilterTests': fileFilterTests,
}

if __name__ == "__main__":
    import doctest
    doctest.testmod()

