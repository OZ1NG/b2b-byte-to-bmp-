#!/usr/bin/python3
# byte to bmp (b2b)
from bmp24 import *

class Bmp:
    def __init__(self, PATH="./"):
        self.EXE_FILES = []
        self.PATH = PATH
        self.bmp24 = Bmp24()
        pass

    # 디렉토리의 파일 이름 전부 가져오기
    def get_files_path(self, PATH="./"):
        # 현재 디렉토리에 존재하는 asm 파일 이름 확인
        files = os.listdir(PATH)
        for f in files:
            if(".exe" in f[-4:]):
                #self.EXE_FILES.append(PATH+'/'+f)
                self.EXE_FILES.append(f)

        if(len(self.EXE_FILES)):
            print("[+] exe files count : ", len(self.EXE_FILES))
        else:
            # 파싱할 exe 파일이 없으므로 종료
            print("[!] exe file doesn't exist!")
            exit(0)

if __name__ == "__main__":
    path = "../It's_mine_My_precious/train_1"
    bmp = Bmp(PATH=path)
    bmp.get_files_path(PATH=path)
    count = 0
    for f in bmp.EXE_FILES:
        #print(f)
        file_data = open(path+'/'+f, 'rb').read()
        bmp.bmp24.make(file_data, bmp_file_name=f,output_path="./bi_train_1")
        print(" [%d/%d] Running... %s" %(count ,len(bmp.EXE_FILES), f), end='\r')
        count += 1
    print("\n[+] Done")