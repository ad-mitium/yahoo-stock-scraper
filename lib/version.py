
def ver_info():
    version_info = (0, 2, 0)
    version_number = '.'.join(str(c) for c in version_info)
    version = 'ver. '+version_number
    return version



if (__name__ == '__main__'):
    print(ver_info())