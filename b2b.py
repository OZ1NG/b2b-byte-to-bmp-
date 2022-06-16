#!/usr/bin/python3
# byte to bmp (b2b)
from bmp24 import Bmp24
from bmpGrayScale import BmpGrayScale
import sys
import os
import argparse

__VERSION__ = 1.0

TYPE = None
PATH = None
RESIZE_OUTPUT_PATH = None
RESULT_OUTPUT_PATH = None
BLOCK_SIDE = 5
RESIZE_ROW = 256
RESIZE_COL = 256

class Bmp:
    def __init__(self, PATH="./"):
        self.EXE_FILES = []
        self.PATH = PATH
        self.bmp24 = Bmp24(PATH=PATH)
        self.bmpGS = BmpGrayScale(PATH=PATH)
        
    # 디렉토리의 file_type에 해당하는 파일 이름 전부 가져오기
    def get_files_path(self, PATH="./", file_type=".exe"):
        # 현재 디렉토리에 존재하는 asm 파일 이름 확인
        files = os.listdir(PATH)
        for f in files:
            if(file_type in f[-len(file_type):]):
                self.EXE_FILES.append(f)

        if(len(self.EXE_FILES)):
            print(f"[+] {file_type} files count : ", len(self.EXE_FILES))
        else:
            # 파싱할 파일이 없으므로 종료
            print(f"[!] {file_type} file doesn't exist!")
            exit(0)

def argparse_init(): # ver4 new code
    parser = argparse.ArgumentParser(description='Domino Monitor')
    parser.add_argument('--method', '-m', help='METHOD : normal : Template Based Domato Fuzzing, iframe : Template Based Domato iframe Fuzzing', default='normal')
    
    return 

def version():
    global __VERSION__
    print("b2b(byte to bmp) ver.%1f" %__VERSION__)
    print("Made by OZ1NG.")

def argparse_init():
    parser = argparse.ArgumentParser(description='3Min Speech')
    parser.add_argument('--type', '-t', help='Create bmp type : bmp24, grayscale', default=None)
    parser.add_argument('--path', '-p', help='Target byte files directory path.',  default=None)
    parser.add_argument('--resize_output_path', '-r', help='Set resize bmp output directory path.', default='./resize')
    parser.add_argument('--result_output_path', '-R', help='Set resize bmp output directory path.', default='./result')
    parser.add_argument('--block_side', '-b', help='Set Block Side', default=5) 
    parser.add_argument('--resize_row', '-o', help="Set Resize bmp's row size.", default=256) 
    parser.add_argument('--resize_col', '-c', help="Set Resize bmp's column size.", default=256) 
    parser.add_argument('--version', '-v', help='Show Version', action='store_true')

    return parser

def set_type(parser):
    global TYPE, PATH, RESIZE_OUTPUT_PATH, RESULT_OUTPUT_PATH, BLOCK_SIDE, RESIZE_ROW, RESIZE_COL
    args = parser.parse_args()

    if(args.version):
        version()
        os._exit(0)

    TYPE = args.type
    PATH = args.path
    if(
        (TYPE == None)
        or
        (PATH == None)
    ):
        parser.print_help()
        os._exit(0)

    RESIZE_OUTPUT_PATH = args.resize_output_path
    RESULT_OUTPUT_PATH = args.result_output_path

    BLOCK_SIDE = args.block_side
    RESIZE_ROW = args.resize_row
    RESIZE_COL = args.resize_col

if __name__ == "__main__":
    set_type(argparse_init())

    bmp = Bmp(PATH=PATH)
    bmp.get_files_path(PATH=PATH)
    count = 0
    for f in bmp.EXE_FILES:
        count += 1
        print(" [%d/%d] Running... %s" %(count ,len(bmp.EXE_FILES), f), end='\r')
        file_data = open(PATH+'/'+f, 'rb').read()
        if(TYPE == "bmp24"):
            bmp.bmp24.make(file_data, bmp_file_name=f, resize_output_path=RESIZE_OUTPUT_PATH, result_output_path=RESULT_OUTPUT_PATH, block_side=BLOCK_SIDE, resize_row=RESIZE_ROW, resize_column=RESIZE_COL)
        elif(TYPE == "grayscale"):
            bmp.bmpGS.make(file_data, bmp_file_name=f, resize_output_path=RESIZE_OUTPUT_PATH, result_output_path=RESULT_OUTPUT_PATH, block_side=BLOCK_SIDE, resize_row=RESIZE_ROW, resize_column=RESIZE_COL)
        else:
            raise TypeError("Plz Set Type. (Type value : bmp24, grayscale)")

    print("\n[+] Done")