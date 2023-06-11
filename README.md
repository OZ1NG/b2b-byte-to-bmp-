# b2b(Byte to BMP)

[*] 악성코드를 CNN을 통해 탐지해보기 위해 바이너리를 bmp 이미지로 바꿔 CNN으로 머신러닝을 하기 위해 만든 BMP Creator 모듈이다.

## [*] 기능

- bmp24 : bmp24로 이미지를 만들어준다.
- bmp gray scale : bmp GrayScale 이미지로 만들어준다.

## [*] How to Usage

```bash
$ python3 b2b.py -h
usage: b2b.py [-h] [--type TYPE] [--path PATH] [--resize_output_path RESIZE_OUTPUT_PATH] [--result_output_path RESULT_OUTPUT_PATH] [--block_side BLOCK_SIDE]
              [--resize_row RESIZE_ROW] [--resize_col RESIZE_COL] [--version]

b2b(Byte to BMP)

optional arguments:
  -h, --help            show this help message and exit
  --type TYPE, -t TYPE  Create bmp type : bmp24, grayscale
  --path PATH, -p PATH  Target byte files directory path.
  --resize_output_path RESIZE_OUTPUT_PATH, -r RESIZE_OUTPUT_PATH
                        Set resize bmp output directory path.
  --result_output_path RESULT_OUTPUT_PATH, -R RESULT_OUTPUT_PATH
                        Set resize bmp output directory path.
  --block_side BLOCK_SIDE, -b BLOCK_SIDE
                        Set Block Side
  --resize_row RESIZE_ROW, -o RESIZE_ROW
                        Set Resize bmp's row size.
  --resize_col RESIZE_COL, -c RESIZE_COL
                        Set Resize bmp's column size.
  --version, -v         Show Version
```

## 추가 설명
- [노션 링크](https://bead-sun-669.notion.site/B2B-Byte-to-BMP-2414073effe74f7785c0d0e2c008377a)

