import os
import sys
import time

class TerminalScreen:
    def __init__(self):
        self.width = 0
        self.height = 0
        self.color_mode = 0
        self.screen = []
        self.cursor_x = 0
        self.cursor_y = 0
        self.commands = {
            0x1: self.setup_screen,
            0x2: self.draw_character,
            0x3: self.draw_line,
            0x4: self.render_text,
            0x5: self.move_cursor,
            0x6: self.draw_at_cursor,
            0x7: self.clear_screen,
            0xFF: self.end_of_file
        }

    def setup_screen(self, data):
        self.width = data[0]
        self.height = data[1]
        self.color_mode = data[2]
        self.clear_screen([])
        self.draw_borders()

    def draw_character(self, data):
    # Unpack only 3 values: x, y, and char
        x, y, char = data  
        if 0 <= x < self.width and 0 <= y < self.height:
            self.screen[y][x] = chr(char)



    def draw_line(self, data):
        x1, y1, x2, y2, color, char = data
        char = chr(char)
        if x1 == x2:  # Vertical line
            for y in range(y1, y2 + 1):
                if 0 <= x1 < self.width and 0 <= y < self.height:
                    self.screen[y][x1] = char
        elif y1 == y2:  # Horizontal line
            for x in range(x1, x2 + 1):
                if 0 <= x < self.width and 0 <= y1 < self.height:
                    self.screen[y1][x] = char

    def render_text(self, data):
        x, y, color = data[:3]
        text = data[3:]
        for i, char in enumerate(text):
            if 0 <= x + i < self.width and 0 <= y < self.height:
                self.screen[y][x + i] = chr(char)

    def move_cursor(self, data):
        self.cursor_x, self.cursor_y = data

    def draw_at_cursor(self, data):
        char, color = data
        if 0 <= self.cursor_x < self.width and 0 <= self.cursor_y < self.height:
            self.screen[self.cursor_y][self.cursor_x] = chr(char)

    def clear_screen(self, _):
        self.screen = [[' ' for _ in range(self.width)] for _ in range(self.height)]

    def draw_borders(self):
        # Draw horizontal borders
        for x in range(self.width):
            self.screen[0][x] = '-'
            self.screen[self.height - 1][x] = '-'

        # Draw vertical borders
        for y in range(self.height):
            self.screen[y][0] = '|'
            self.screen[y][self.width - 1] = '|'

        # Add corners
        self.screen[0][0] = '+'
        self.screen[0][self.width - 1] = '+'
        self.screen[self.height - 1][0] = '+'
        self.screen[self.height - 1][self.width - 1] = '+'

    def end_of_file(self, _):
        self.render_screen()
        input("Press Enter to exit...")  # Prevents abrupt closure.

    def render_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        for row in self.screen:
            print(''.join(row))

    def process_commands(self, data_stream):
        i = 0
        while i < len(data_stream):
            command = data_stream[i]
            length = data_stream[i + 1]
            data = data_stream[i + 2:i + 2 + length]
            self.commands.get(command, self.unknown_command)(data)
            i += 2 + length
            self.render_screen()
            time.sleep(0.5)  # Add delay for observation.

    def unknown_command(self, _):
        print("Unknown command!")

def main():
    screen = TerminalScreen()
    
    data_stream = [
        0x1, 3, 40, 15, 0x01,  # Screen setup (40x15, 16 colors)
        0x2, 3, 5, 5, ord('A'),  # Draw character 'A' at (5, 5) - only 3 values (x, y, char)
        0x4, 8, 2, 2, ord('I'), ord('n'), ord('t'), ord('e'), ord('r'), ord('n'), ord('s'), ord(' '), ord('a'), ord('r'), ord('e'), ord(' '), ord('g'), ord('r'), ord('e'), ord('a'), ord('t'),  # Render longer text starting at (2, 2)
        0x3, 6, 10, 5, 15, 5, ord('='),  # Draw a horizontal line from (10, 5) to (15, 5)
        0x3, 6, 20, 2, 20, 10, ord('|'),  # Draw a vertical line from (20, 2) to (20, 10)
        0xFF, 0  # End of file
    ]


    screen.process_commands(data_stream)

if __name__ == "__main__":
    main()
