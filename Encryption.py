# http://www.cnblogs.com/Matrix_Yao/archive/2009/12/02/1615295.html

# Low address stores small value
# Little endian

# Take cat.bmp as example

# bmp file header:      14 byte
#   bfType:             2 byte      424d
#   bfSize:             4 byte      3699 0100
#   bfReversed1:        2 byte      0000
#   bfReversed2:        2 byte      0000
#   bfOffBits:          4 byte      3604 0000       436     1078
# bitmap info header:   40 byte
#   biSize:             4 byte      2800 0000       28      40
#   biWidth:            4 byte      6801 0000       168     360
#   biHeight:           4 byte      2001 0000       128     296
#   biPlanes:           2 byte      0100
#   biBitCount:         2 byte      0800            8       8
#   biCompression:      4 byte      0000 0000       8       8
#   biSizeImage:        4 byte      00bf 0400
#   biXPelsPerMeter:    4 byte      c40e 0000
#   biYPelsPerMeter:    4 byte      c40e 0000
#   biClrUsed:          4 byte      0000 0000
#   biClrImportant:     4 byte      0000 0000

HEADER_SIZE = 1078  # Header size of bmp file : 14 + 40 + 1024 bytes


class Encryption:
    def open_file(self):
        with open(self.origin_file_name, 'rb') as f:
            # Read image file into bytes
            self.origin_image_data = f.read()

    def copy_header(self):
        # Read bmp file header (14) and bitmap info header (40) and palette (1024)
        # Copy them into new image
        for i in range(0, HEADER_SIZE):
            self.new_image_data.append(self.origin_image_data[i])
            self.bytes_counter += 1

    def hide_int(self, curr_hide_int):
        curr_hide_binary = '{:032b}'.format(curr_hide_int)
        for i in range(0, 32):
            curr_image_binary = '{0:08b}'.format(self.origin_image_data[self.bytes_counter])
            # In little endian mode, LSB is the first bit
            new_image_binary = curr_hide_binary[i] + curr_image_binary[1:]
            new_image_int = int(new_image_binary, 2)
            self.new_image_data.append(new_image_int)
            self.bytes_counter += 1

    def hide_char(self, curr_hide_byte):
        # ord(): convert char to int
        # Then get binary value of one byte
        # Example:
        # a = '{0:08b}'.format(255)
        # print(a) # '1111111'
        curr_hide_binary = '{0:08b}'.format(ord(curr_hide_byte))

        # Hide one byte in eight bytes
        for i in range(0, len(curr_hide_binary)):
            curr_image_binary = '{0:08b}'.format(self.origin_image_data[self.bytes_counter])
            # In little endian mode, LSB is the first bit
            new_image_binary = curr_hide_binary[i] + curr_image_binary[1:]
            new_image_int = int(new_image_binary, 2)
            self.new_image_data.append(new_image_int)
            self.bytes_counter += 1

    def do_hide(self):
        # Hide length of message
        self.hide_int(len(self.hide_msg))
        # Hide message byte by byte
        for i in range(0, len(self.hide_msg)):
            self.hide_char(self.hide_msg[i])

    def copy_rest(self):
        # Copy rest data into new image
        left_data = self.origin_image_data[self.bytes_counter:]
        for left_byte in left_data:
            self.new_image_data.append(left_byte)

    def write_file(self):
        with open(self.new_file_name, 'wb') as out:
            new_image_bytes = bytearray(self.new_image_data)
            out.write(new_image_bytes)

    def run(self):
        self.open_file()
        self.copy_header()
        self.do_hide()
        self.copy_rest()
        self.write_file()

    def __init__(self, origin_file_name, new_file_name, hide_msg):
        self.origin_file_name = origin_file_name
        self.new_file_name = new_file_name
        self.hide_msg = hide_msg
        self.bytes_counter = 0  # Function as a pointer
        self.origin_image_data = ''  # Type: bytes
        self.new_image_data = []  # Type: int array
