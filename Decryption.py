HEADER_SIZE = 1078  # Header size of bmp file : 14 + 40 + 1024 bytes


class Decryption:
    def read_header(self):
        # Read unchanged header
        for i in range(0, HEADER_SIZE):
            self.f.read(1)

    def get_int(self):
        curr_hide_binary = ''
        # Get one hide char from eight bytes
        for i in range(0, 32):
            curr_image_byte = self.f.read(1)
            if len(curr_image_byte) == 0:
                return ''
            curr_image_binary = '{0:08b}'.format(ord(curr_image_byte))
            # In little endian mode, LSB is the first bit
            curr_hide_binary += curr_image_binary[0]
        curr_hide_int = int(curr_hide_binary, 2)
        return curr_hide_int

    def get_char(self):
        curr_hide_binary = ''
        # Get one hide char from eight bytes
        for i in range(0, 8):
            curr_image_byte = self.f.read(1)
            if len(curr_image_byte) == 0:
                return ''
            curr_image_binary = '{0:08b}'.format(ord(curr_image_byte))
            # In little endian mode, LSB is the first bit
            curr_hide_binary += curr_image_binary[0]
        curr_hide_char = chr(int(curr_hide_binary, 2))
        return curr_hide_char

    def get_hide(self):
        curr_hide_int = self.get_int()
        for i in range(0, curr_hide_int):
            curr_hide_char = self.get_char()
            self.hide_msg += curr_hide_char
        self.f.close()

    def run(self):
        self.read_header()
        self.get_hide()
        return self.hide_msg

    def __init__(self, new_file_name):
        self.new_file_name = new_file_name
        self.f = open(self.new_file_name, 'rb')
        self.hide_msg = ''
