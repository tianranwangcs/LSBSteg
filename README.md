# LSBSteg
- A simple steganography tool using the least significant bit of every byte in *.bmp files to store hidden data.
- Mainly referenced from [Omiher's work](https://github.com/omriher/LSB_Steganography).

## Usage
- Python 3.x with Tkinter installed
- PIL package (Mention: In Mac, install it by 'sudo pip3 install pillow'.)
- run 'python3 GUI.py'

## Instruction
- This steganography tool is compitable with both 256 gray & 24 bit true color bmp files.
- Apart from the first 1078 bits in header, I use the next 32 bytes to store the length of hidden message.(An int is 32 bits long, which can be hidden in 32 bytes.)
- So a 256 gray bmp file with 'w*h-32<=0' or a 24 bit true color bmp file with 'w*h*3-32<=0' can not hide message using this tool.

## Screenshots
![UI](https://github.com/BIOTONIC/LSBSteg/blob/master/Screenshots/Screen%20Shot%202017-05-27%20at%2017.39.50.png)
![Encrypt Message](https://github.com/BIOTONIC/LSBSteg/blob/master/Screenshots/Screen%20Shot%202017-05-27%20at%2017.43.48.png)
![Decrypt Message](https://github.com/BIOTONIC/LSBSteg/blob/master/Screenshots/Screen%20Shot%202017-05-27%20at%2017.44.10.png)
