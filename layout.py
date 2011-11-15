"""
Determines the layout
"""
## beginning of import
from __future__ import division
import os.path

class Layout():
    """Layout class"""
    def __init__(self, layout_file_path):
        self.dimensions = {}
        self.tile_map = {}
        self.rows = []
        self.layout_file_path = layout_file_path
        self.parse_layout_file()
        self.current_row = 0
        self.bottom_of_pattern = False

    def get_next_row(self):
        """gets the next row"""
        if (self.current_row < len(self.rows)):
            self.current_row += 1
            return self.rows[self.current_row - 1]
        else:
            return []

    def parse_layout_file(self):
        """parsing layout file"""
        if not os.path.isfile(self.layout_file_path):
            return False
        else:
            layout_file = open(self.layout_file_path)
            formatting_line = layout_file.readline()
            while (formatting_line != ""):
                if formatting_line == "dimensions:\n":
                    dimension_line = layout_file.readline()
                    while not dimension_line == "$end\n":
                        line_tokens = dimension_line.split()
                        self.dimensions[line_tokens[0]] = int(line_tokens[1])
                        dimension_line = layout_file.readline()

                elif formatting_line == "tiles:\n":
                    tile_name_line = layout_file.readline()
                    while not tile_name_line == "$end\n":
                        line_tokens = tile_name_line.split()
                        self.tile_map[line_tokens[0]] = line_tokens[1]
                        tile_name_line = layout_file.readline()

                elif formatting_line == "layout:\n":
                    layout_line = layout_file.readline()
                    while not layout_line == "$end\n":
                        for word in layout_line.split():
                            current_row_layout = []
                            for i in range(len(word)):
                                current_row_layout.append( \
                                  self.tile_map[word[i]])
                            self.rows.append(current_row_layout)
                        layout_line = layout_file.readline()

                elif formatting_line == "\n":
                    pass

                else:
                    print 'wrong format'
                formatting_line = layout_file.readline()
            self.rows.reverse()
