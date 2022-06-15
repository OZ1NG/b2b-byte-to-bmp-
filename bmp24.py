#!/usr/bin/python3
import os
import struct
import numpy as np
from PIL import Image

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

DEBUG = False
def debug_print(*msg):
    if(DEBUG):
        print("[DEBUG]", " ".join(msg))

'''
    struct.pack("<B", int) unsigned char  1byte
    struct.pack("<H", int) unsigned short 2byte
    struct.pack("<I", int) unsigned int   4byte
'''
class Bmp24:
    def __init__(self, PATH='./', BMP_FILE_NAME="result.bmp"):
        self.ASM_FILES = None
        self.PATH = PATH
        self.BMP_DATA = []
        self.ASM_DATA = None 
        self.BMP_FILE_NAME = BMP_FILE_NAME
        
        # 모든 값은 little endian
        self.bmp = b''

        # BITMAPFILEHEADER
        self.bf = b''
        self.bfType = b'BM'                                 # 2byte # 매직 넘버(BM) 
        self.bfSize = b''                                   # 4byte # 파일 크기 # CNN을 위해서니 정사각형 크기로 고정할 것 # 헤더크기 포함
        self.bfReserved1 = struct.pack("<H", 0x00)          # 2byte # 예약된 공간
        self.bfReserved2 = struct.pack("<H", 0x00)          # 2byte # 예약된 공간
        self.bfOffBits = struct.pack("<I", 0x36)            # 4byte # 비트맵 데이터의 시작 위치 # 헤더 다음의 실제 비트맵 바이트 들의 위치

        # BITMAPINFOHEADER(Windows Version 3) # default
        self.bi = b''
        self.biSize = struct.pack("<I", 0x28)               # 4byte # bi 헤더 크기
        self.biWidth = b''                                  # 4byte # 비트맵 이미지의 가로 크기
        self.biHeight = b''                                 # 4byte # 비트맵 이미지의 세로 크기 # 양수면 상하가 뒤집혀져 있는 상태(보통 양수) # 픽셀 개수
        self.biPlanes = struct.pack("<H", 0x01)             # 2byte # 사용하는 색상판의 수. 항상 1로 고정
        self.biBitCount = struct.pack("<H", 0x18)           # 2byte # 픽셀 하나를 표현하는 비트 수
        self.biCompression = struct.pack("<I", 0x00)        # 4byte # 압축 방식 # 0으로 고정(압축 X)
        self.biSizeImage = b''                              # 4byte # 비트맵 이미지의 픽셀 데이터 크기(압축되지 않은 크기) # 헤더를 제외한 픽셀 데이터에 대한 크기
        self.biXPelsPerMeter = struct.pack("<I", 0x00)      # 4byte # 그림의 가로 해상도(미터당 픽셀) # 그냥 0으로 고정(상관 없음)
        self.biYPelsPerMeter = struct.pack("<I", 0x00)      # 4byte # 그림의 세로 해상도(미터당 픽셀) # 그냥 0으로 고정(상관 없음)
        self.biClrUsed = struct.pack("<I", 0x00)            # 4byte # 색상 테이블에서 실제 사용되는 색상 수 # 그냥 0으로 고정(상관 없음)
        self.biClrImportant = struct.pack("<I", 0x00)       # 4byte # 비트맵을 표현하기 위해 필요한 색상 인덱스 수 # 그냥 0으로 고정(상관 없음)
        
        # BITAMPCOREHEADER(OS/2)
        ## 미래의 누군가에게 맡긴다...

        # BITMAP PIXELS
        self.pi = b''

    def set_bmp_file_name(self, BMP_FILE_NAME="result.bmp"):
        self.BMP_FILE_NAME = BMP_FILE_NAME

    def set_path(self, PATH="./"):
        self.PATH = PATH

    # map_line : 완성된 비트맵 이미지의 한줄의 픽셀 개수(정사각형으로 고정), 만약 가로 세로 길이를 따로 구하고 싶다면 map_line 부분을 수정하면된다.
    def create_24bmp(self, data, map_row=128, map_column=128, block_row=5, block_column=5): # TODO : mapline -> map column map row로 바꿀것
        # bitmap pixel data (??byte)
        pixel_size = self.create_pi(data, map_row=map_row, map_column=map_column, block_row=block_row, block_column=block_column) # default : 5*5

        # bitmap info header (0x28byte)
        self.create_bitmapinfoheader_header(biWidth=map_column, biHeight=map_row)

        # bitmap header (14bit)        
        file_size = 0x35 + pixel_size # 0x35 : bfOffBits-1 == header size
        self.create_bitmapfileheader_header(file_size)

    # TODO : 값이 없는 필드의 경우 예외 처리 과정 추가 필요
    def combine_data(self):
        self.bf += self.bfType + self.bfSize + self.bfReserved1 + self.bfReserved2 + self.bfOffBits
        self.bi += self.biSize + self.biWidth + self.biHeight + self.biPlanes + self.biBitCount + self.biCompression + self.biSizeImage + self.biXPelsPerMeter + self.biYPelsPerMeter + self.biClrUsed + self.biClrImportant

        self.bmp += self.bf + self.bi + self.pi
        return True

    # 14byte의 기본 비트맵 헤더 생성
    def create_bitmapfileheader_header(self, file_size):
        self.bfSize = struct.pack("<I", file_size)          # 4byte # 파일 크기 # CNN을 위해서니 정사각형 크기로 고정할 것
        
    def create_bitmapinfoheader_header(self, biWidth=0, biHeight=0):
        self.biWidth = struct.pack("<I", biWidth)               # 4byte # 비트맵 이미지의 가로 크기(픽셀 개수)
        self.biHeight = struct.pack("<I", biHeight)             # 4byte # 비트맵 이미지의 세로 크기 # 양수면 상하가 뒤집혀져 있는 상태(보통 양수) # 픽셀 개수
        self.biSizeImage = struct.pack("<I", biWidth*biHeight)  # 4byte # 비트맵 이미지의 픽셀 데이터 크기(압축되지 않은 크기) # 헤더를 제외한 픽셀 데이터에 대한 크기

    # pixel data : self.pi 에 픽셀 데이터 저장, return : 전체 픽셀 바이트 개수
    # map_line : map의 한줄 픽셀 개수
    def create_pi(self, file_data, map_line=25, map_row=5, map_column=5, block_row=5, block_column=5):
        # 만약 한 줄(열)의 픽셀 개수가 block_row보다 작은 경우 raise
        if(
            (map_row < block_row)
            or
            (map_column < block_column)
        ):
            raise ValueError("map_row and map_column each great than block_row and block_column")
        map_column *= 3
        # 블록들 생성
        blocks = self.block_create(file_data, map_row=map_row, map_column=map_column ,block_row=block_row, block_column=block_column)        
        #if(self.padding_flag):
        if(map_column % (block_column*3) != 0):
            map_column += (block_column*3 - (map_column % (block_column*3))) # map_line + ?하는 이유는 패딩이 된 경우 한 줄의 크기가 패딩에 의해 늘어나기 때문이다.
        if(map_row % block_row != 0):
            map_row += (block_row - (map_row % block_row)) # map_line + ?하는 이유는 패딩이 된 경우 한 줄의 크기가 패딩에 의해 늘어나기 때문이다.            
        debug_print("map_column : ", map_column)
        debug_print("map_row : ", map_row )
            
        pixel_block = self.block_combine(blocks, map_row=map_row, map_column=map_column)
        self.pi = pixel_block.tobytes() # 바이트 타입으로 한번에 리턴
        return len(self.pi)

    # map_col
    # map_row
    # block_col
    # block_row
    # pad_block_size
    # pad_col
    # pad_row
    # 사진 
    def get_padsize(self, map_col=1, map_row=1, block_col=1, block_row=1):
        pad_col = 0
        pad_row = 0
        if((map_col % block_col) != 0):
            pad_col = (block_col - (map_col % block_col)) # pad block의 행의 픽셀 개수
        if(map_row % block_row != 0):
            pad_row = (block_row - (map_row % block_row)) # pad block의 열의 픽셀 개수
        
        padding_col_size = pad_row * map_col
        padding_row_size = pad_col * map_row
        pad_block_size = pad_col * pad_row
        total_padding_size = padding_col_size + padding_row_size + pad_block_size

        return total_padding_size
        
    # 하나의 블럭 생성 (1map = row*column 크기)
    # column : 한 블럭의 가로 크기
    # row : 한 블록의 세로 크기
    def block_create(self, file_data, map_row=1, map_column=1, block_row=1, block_column=1):
        # block_column은 무조건 3의 배수(1픽셀은 3바이트로 표현되기 때문)
        block_column *= 3

        debug_print("map_col :",map_column) 
        debug_print("map_row :",map_row)
        debug_print("block_col :",block_column)
        debug_print("block_row :",block_row)

        file_data += b'\x90'*self.get_padsize(map_row=map_row, map_col=map_column, block_col=block_column, block_row=block_row)  # nop padding
        debug_print("file_data :", len(file_data))
        debug_print("len(file_data)/(block_row*block_column) :", len(file_data)/(block_row*block_column))
        
        blocks = np.frombuffer(file_data, dtype=np.uint8).reshape((int(len(file_data)/(block_row*block_column)),block_row,block_column)) # 8비트(1바이트) 단위로 배열로 변경
        return blocks

    # padBytes : 패딩해줘야 하는 값 : bmp24는 한 행(column)당 4바이트의 단위를 맞춰줘야 함(실제로 있는 멤버 변수)
    def block_padBytes(self, column_data):
        # 한 행의 길이가 4의 배수인지 체크
        if((len(column_data[0]) % 4) != 0):
            # padding # overhead... sry...
            padding_ = list(np.zeros((1, 4 - (len(column_data[0]) % 4)))[0])
            tmp_list = []
            for r in column_data:
                #print("r:",list(r))
                tmp_list.append(list(r) + padding_)
            return np.array(tmp_list)
        return column_data

    # blocks type : np.array
    def block_combine(self, blocks:np.array, map_row=5, map_column=5):
        result = None
        # 한 줄당 블록의 개수 == map_row / block row 개수
        block_row_count = int(map_row/len(blocks[0]))
        block_column_count = int(map_column/len(blocks[0][0]))
        debug_print("blocks : ", len(blocks))
        debug_print("block_row_count : ", block_row_count)
        debug_print("block_column_count : ", block_column_count)
        
        for bcc in range(0, len(blocks), block_column_count):
            #print("bcc:", bcc)
            tmp1 = tuple(blocks[bcc:bcc+block_column_count])
            #print("tmp1:", tmp1)
            tmp2 = np.concatenate(tmp1, axis=1) # axis=1 : y축으로 병합
            if(result is None):
                result = self.block_padBytes(tmp2)
                #print("RESULT : ",result)
                continue
            
            tmp2 = self.block_padBytes(tmp2)
            #print("tmp2 : ",tmp2[0])
            #print("tmp2 len : ",len(tmp2[0]))
            
            #print("result : ",result[-1])
            
            result = np.concatenate((result, tmp2), axis=0) # x축으로 병합 # result 아래에 tmp2를 추가함

        return result
        
    # bmp 이미지를 resize
    def image_resize(self, width=256, height=256, bmp_file_name='result.bmp', output_path=None):
        img = Image.open(self.PATH+'/bmp_result/'+bmp_file_name)
        img_resize = img.resize((width, height))
        if(bmp_file_name.find(".bmp") == -1): # .bmp가 없으면
            bmp_file_name = bmp_file_name+".bmp"
        bmp_file_name = bmp_file_name[:bmp_file_name.find(".bmp")] + "_reize.bmp"
        if(output_path != None):
            #img_resize.save(self.PATH+'/'+bmp_file_name)
            save_path = output_path
            if(os.path.isdir(save_path) == False):
                os.mkdir(save_path)
            save_path = output_path+'/'+bmp_file_name
        else:
            save_path = self.PATH+'/resize_result'
            if(os.path.isdir(save_path) == False):
                os.mkdir(save_path)
                #raise FileNotFoundError("Dir not Found. Path : " + save_path)
            save_path =save_path+'/'+bmp_file_name
        img_resize.save(save_path)
        debug_print("[+] Resize Done")

    def save_bmp(self, bmp_file_name="result.bmp"):
        save_path = self.PATH + '/bmp_result'
        if(os.path.isdir(save_path) == False):
            os.mkdir(save_path)
            #raise FileNotFoundError("Dir not Found. Path : " + save_path)
        save_path = save_path + '/' + bmp_file_name
        # combine data
        self.combine_data()
        with open(save_path, 'wb') as fp:
            fp.write(self.bmp)
        debug_print("[+] Save Done")

    # 약수를 통해 최대한 가장 가까운 width와 height 값을 구함        
    def getHeightWidth(self, file_size):
        divisorsList = []
        for i in range(1, int(file_size**(1/2)) + 1):
            if (file_size % i == 0):
                divisorsList.append(i) 
                if ( (i**2) != file_size) : 
                    divisorsList.append(file_size // i)
        divisorsList.sort()
        # 더 큰 값이 width가 된다.
        height = 0
        width = 0
        idx = int(len(divisorsList)/2)
        if((len(divisorsList) % 2) == 0): # 짝수
            height = divisorsList[idx-1]
            width = divisorsList[idx]
        else: # 홀수
            height = divisorsList[idx]
            width = height
        #print("divisorsList :",divisorsList)
        debug_print("init_height : ",height)
        debug_print("init_width : ",width)
        return height, width

    def make(self, file_data, bmp_file_name="result.bmp", path="./", output_path="./"):
        file_size = len(file_data) 
        debug_print("file_size/3 : ",file_size/3)
        if((file_size % 3) != 0): # 3으로 떨어지지 않는 경우 3의 배수로 맞춰줌
            file_data += b"\x00" * (3 - (file_size % 3)) # NULL Padding
            file_size = len(file_data)
        file_size = int(file_size/3) # 3으로 나누는 이유는 한 픽셀은 3바이트이다. 따라서 실제 데이터는 3의 배수이기 때문이다.
        debug_print("file_size/3 -2 : ",file_size/3)
        
        height, width = self.getHeightWidth(file_size)
        block_side = 5 # default
        # 값 체크 : 만약 block_size 값보다 더 작은 경우 더 작은 값으로 block_side 설정
        if (height < block_side) or (width < block_side):
            if (width < height):
                block_side = width
            else:
                block_side = height
        
        bmp_file_name += ".bmp"
        self.set_bmp_file_name(BMP_FILE_NAME=bmp_file_name)
        self.set_path(PATH=path)
        self.create_24bmp(file_data, map_row=height, map_column=width, block_row=block_side, block_column=block_side)
        self.save_bmp(bmp_file_name=bmp_file_name)
        self.image_resize(bmp_file_name=bmp_file_name, output_path=output_path)
        self.__init__(BMP_FILE_NAME=bmp_file_name, PATH=path)
 
if __name__ == "__main__":
    bmp = Bmp24()
    '''
    test_width = 1
    test_height = 255
    test_byte = b''
    for i in range(test_height):
        test_byte += bytes([i])*(test_width*3)
    print("test_byte : ",len(test_byte))
    '''
    #bmp.create_24bmp(test_byte, map_row=test_height, map_column=test_width)
    test_byte = open('./sample/00cec16422b4d7b1a28a12ca04dc7f3c.exe', 'rb').read()
    bmp.make(test_byte)

    '''
    test = bmp.block_create(test_byte, row=5, column=5)
    print(test)
    print(len(test[0][0]))

    test1 = bmp.block_combine(test, map_column=25)
    print(test1)

    print(test1.tobytes())
    '''
    '''
    size = bmp.create_pi(test_byte, map_row=25, map_column=25)
    print(bmp.pi)
    print(size)
    '''