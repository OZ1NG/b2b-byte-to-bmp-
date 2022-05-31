#!/usr/bin/python3
import sys
import os
import struct

def padding(index, length): # for test
    index = hex(index)[2:]
    return '0'*(length-len(index)) + index

def print_hex(data): # for test
    tmp = ''
    idx = 0
    print(" " * 9, "00 01 02 03 04 05 06 07 08 09 0A 0B 0C 0D 0E 0F\n")
    for i,v in enumerate(data):
        if (i % 0x10) == 0:
            if (len(tmp) != 0):
                print(padding(idx, 8)+' ', tmp)
                tmp = ''
                idx += 0x10
        char_tmp = hex(v)[2:]
        if (len(char_tmp) < 2):
            tmp += '0'+hex(v)[2:]+' '
        else:
            tmp += hex(v)[2:]+' '
    print(padding(idx, 8)+' ', tmp+"\n")

# 디렉토리의 파일 이름 전부 가져오기
def getFileNames(PATH, ASM_FILES):
    # 현재 디렉토리에 존재하는 asm 파일 이름 확인
    files = os.listdir(PATH)
    # print(files) # TEST
    for f in files:
        if(".asm" in f[-4:]):
            ASM_FILES.append(PATH+f)

    if(len(ASM_FILES)):
        print("[+] asm files list : ", ASM_FILES)
    else:
        # 파싱할 asm 파일이 없으므로 종료
        print("[!] asm file doesn't exist!")
        exit(0)

'''
    struct.pack(">B", int) unsigned char  1byte
    struct.pack(">H", int) unsigned short 2byte
    struct.pack(">I", int) unsigned int   4byte
'''
class Bmp24:
    def __init__(self, PATH='./'):
        self.ASM_FILES = None
        self.PATH = PATH
        self.BMP_DATA = []
        self.ASM_DATA = None 
        
        # 모든 값은 little endian

        # BITMAPFILEHEADER
        self.bf = b''
        self.bfType = b'BM'                                 # 2byte # 매직 넘버(BM) 
        self.bfSize = b''                                   # 4byte # 파일 크기 # CNN을 위해서니 정사각형 크기로 고정할 것 # 헤더크기 포함
        self.bfReserved1 = struct.pack(">H", 0x00)        # 2byte # 예약된 공간
        self.bfReserved2 = struct.pack(">H", 0x00)        # 2byte # 예약된 공간
        self.bfOffBits = struct.pack(">I", 0x36)            # 4byte # 비트맵 데이터의 시작 위치 # 헤더 다음의 실제 비트맵 바이트 들의 위치

        # BITMAPINFOHEADER(Windows Version 3)
        self.bi = b''
        self.biSize = struct.pack(">I", 0x28)               # 4byte # bi 헤더 크기
        self.biWidth = b''                                  # 4byte # 비트맵 이미지의 가로 크기
        self.biHeight = b''                                 # 4byte # 비트맵 이미지의 세로 크기 # 양수면 상하가 뒤집혀져 있는 상태(보통 양수) # 픽셀 개수
        self.biPlanes = struct.pack(">H", 0x01)           # 2byte # 사용하는 색상판의 수. 항상 1로 고정
        self.biBitCount = struct.pack(">H", 0x18)           # 2byte # 픽셀 하나를 표현하는 비트 수
        self.biCompression = struct.pack(">I", 0x00)        # 4byte # 압축 방식 # 0으로 고정(압축 X)
        self.biSizeImage = b''                              # 4byte # 비트맵 이미지의 픽셀 데이터 크기(압축되지 않은 크기) # 헤더를 제외한 픽셀 데이터에 대한 크기
        self.biXPelsPerMeter = struct.pack(">I", 0x00)      # 4byte # 그림의 가로 해상도(미터당 픽셀) # 그냥 0으로 고정(상관 없음)
        self.biYPelsPerMeter = struct.pack(">I", 0x00)      # 4byte # 그림의 세로 해상도(미터당 픽셀) # 그냥 0으로 고정(상관 없음)
        self.biClrUsed = struct.pack(">I", 0x00)            # 4byte # 색상 테이블에서 실제 사용되는 색상 수 # 그냥 0으로 고정(상관 없음)
        self.biClrImportant = struct.pack(">I", 0x00)       # 4byte # 비트맵을 표현하기 위해 필요한 색상 인덱스 수 # 그냥 0으로 고정(상관 없음)
        
        # BITAMPCOREHEADER(OS/2)
        ## 미래의 누군가에게 맡긴다...

        # BITMAP PIXELS
        self.pi = b''

    def create_24bmp(self, data):
        


        # bitmap header (14bit)        
        self.create_bitmapfileheader_header(file_size)

        pass

    # 14byte의 기본 비트맵 헤더 생성
    def create_bitmapfileheader_header(self, file_size):
        self.bfSize = struct.pack(">I", file_size)          # 4byte # 파일 크기 # CNN을 위해서니 정사각형 크기로 고정할 것
        
    def create_bitmapinfoheader_header(self, biWidth=0, biHeight=0, biSizeImage=0):
        self.biWidth = struct.pack(">I", biWidth)         # 4byte # 비트맵 이미지의 가로 크기
        self.biHeight = struct.pack(">I", biHeight)        # 4byte # 비트맵 이미지의 세로 크기 # 양수면 상하가 뒤집혀져 있는 상태(보통 양수) # 픽셀 개수
        self.biSizeImage = struct.pack(">I", biSizeImage)     # 4byte # 비트맵 이미지의 픽셀 데이터 크기(압축되지 않은 크기) # 헤더를 제외한 픽셀 데이터에 대한 크기

    def create_pi(self, file_data):
        
        pass

    def save_bmp(self):
        pass

class asm2bmp:
    def __init__(self):
        self.bmp24 = Bmp24()
    
    # opcode의 크기를 15byte로 패딩->3의 배수로 패딩을 통해 가공시킨 뒤 읽어옴
    # 3의 배수인 이유는 비트맵에서 한 픽셀을 3바이트로 표현 가능하기 떄문임
    def read_asm(self, file_data):
        for line in file_data:
            # 주석 제거
            remark_idx = line.find(";")
            if(remark_idx != -1):
                line = line[:remark_idx]
            line = line.strip()

            # opcode
            opcode = line.split(' ', 1)[0]
            ## opcode padding : 패딩 값은 0xff # 변경 가능
            opcode += "\xff" * (3 - (len(opcode) % 3))
            
            # operands
            operands = line.split(' ', 1)[1]
            ## operands padding : 패딩 값은 0xa0 # 변경 가능
            operands += "\xa0" * (3 - (len(operands) % 3))
            
            
        pass
