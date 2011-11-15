"""
Tile class
"""
## beginning of import
from __future__ import division
import pygame
import rabbyt
import random
import layout

SECOND_TO_TICK_CONVERSION = 1000

class Background():
    """background class"""
    def __init__(self, screen_width, screen_height, layout_file_name, game):
        self.tile_rows = []
        self.tile_layout = layout.Layout(layout_file_name)

        self.screen_width  = screen_width
        self.screen_height = screen_height

        self.tile_width = self.tile_layout.dimensions["WIDTH"]
        self.tile_height = self.tile_layout.dimensions["HEIGHT"]
        self.background_scroll_time = self.tile_layout.dimensions["SCROLL_TIME"]

        self.number_of_tiles_across = screen_width / self.tile_width
        self.number_of_rows_onscreen = (screen_height / self.tile_height) + 5

        self.row_update_time = (float(self.background_scroll_time) / \
                                float(self.number_of_rows_onscreen)) * \
                                SECOND_TO_TICK_CONVERSION * 1.55
        self.ticks_during_last_add = 0
        self.sample_tile_names = ["1dirt_patch_tile1.png", \
                         "1dirt_patch_tile2.png", "1dirt_patch_tile3.png", \
                         "1dirt_patch_tile4.png"]

        self.game = game

    def initialize(self):
        """initializes the background"""
        for i in range(int(self.number_of_rows_onscreen)):
            row_y_position = (i * self.tile_height) + (self.tile_height / 2) - \
                             (self.screen_height / 2) - 100
            print 'row ', i, 'y_pos: ', row_y_position
            self.tile_rows.append(self.build_independent_row(row_y_position, \
                             self.tile_layout.get_next_row()))
            self.ticks_during_last_add = pygame.time.get_ticks()

    def build_independent_row(self, y_start_position, row_layout=[]):
        """creates one row"""
        current_row = []
        leftmost_tile_x_position = (-1 * (self.number_of_tiles_across / 2) * \
                             self.tile_width) + (self.tile_width / 2)
        maximum_y_travel_distance = self.screen_height + self.tile_height

        if len(row_layout) == 0:
            for i in range(int(self.number_of_tiles_across)):
                rand_num = random.randint(0, len(self.sample_tile_names) - 1)
                row_layout.append(self.sample_tile_names[rand_num])

        for i in range(int(self.number_of_tiles_across)):
            new_tile = rabbyt.Sprite(row_layout[i])
            new_tile.x = leftmost_tile_x_position + (self.tile_width * i)
            if i == 0:
                new_tile.y = rabbyt.lerp(y_start_position, (y_start_position - \
                maximum_y_travel_distance), dt=self.background_scroll_time, \
                extend="extrapolate")
            else:
                new_tile.y = current_row[0].attrgetter('y')
            current_row.append(new_tile)
        return current_row

    def maintain_tile_rows(self):
        """maintains row"""
        current_time = pygame.time.get_ticks()
        if ((current_time - self.ticks_during_last_add) > self.row_update_time):
            highest_current_row = self.tile_rows[-1]


            highest_y_tile_position = \
            highest_current_row[0].convert_offset((0, 0))[1]
            print highest_y_tile_position
            self.tile_rows.append( self.build_independent_row( \
            highest_y_tile_position + 100, self.tile_layout.get_next_row()))
            self.ticks_during_last_add = current_time
            print "number of rows: ", len(self.tile_rows)
            del self.tile_rows[0]

    def render(self):
        """rabbyt render method"""
        for row in self.tile_rows:
            rabbyt.render_unsorted(row)

    def set_motion(self, y_start_position):
        return rabbyt.lerp(y_start_position, (y_start_position - self.screen_height - self.tile_height), dt = self.background_scroll_time, extend="extrapolate")
