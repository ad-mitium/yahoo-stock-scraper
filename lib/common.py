#!/usr/bin/env python3
# 
import os
from pathlib import Path

def test_path(output_folder_path):
    if os.path.exists(output_folder_path):
        # print(os.path.dirname(output_folder_path))
        pass
    else:
#        print('Failed to find path to data '+ os.path(data_output_path))
        Path(output_folder_path).mkdir( parents=True, exist_ok=True)
        # raise SystemExit('Path to '+output_folder_path+' not found')

def joinpath(rootdir, targetdir):
    return os.path.join(os.sep, rootdir + os.sep, targetdir)


