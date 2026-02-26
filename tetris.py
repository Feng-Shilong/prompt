import pygame
import random

# 游戏配置
SCREEN_WIDTH, SCREEN_HEIGHT = 300, 600
BLOCK_SIZE = 30
COLUMN_COUNT, ROW_COUNT = SCREEN_WIDTH // BLOCK_SIZE, SCREEN_HEIGHT // BLOCK_SIZE

# 颜色定义
COLORS = [
    (0, 0, 0),        # 空白
    (0, 255, 255),    # I
    (0, 0, 255),      # J
    (255, 165, 0),    # L
    (255, 255, 0),    # O
    (0, 255, 0),      # S
    (255, 0, 0),      # Z
    (128, 0, 128)     # T
]

# 方块形状定义（矩阵）
SHAPES = [
    [[1, 1, 1, 1]],  # I
    [[2, 0, 0], [2, 2, 2]],  # J
    [[0, 0, 3], [3, 3, 3]],  # L
    [[4, 4], [4, 4]],  # O
    [[0, 5, 5], [5, 5, 0]],  # S
    [[6, 6, 0], [0, 6, 6]],  # Z
    [[0, 7, 0], [7, 7, 7]]   # T
]

class Tetris:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("俄罗斯方块")
        self.clock = pygame.time.Clock()
        self.board = [[0 for _ in range(COLUMN_COUNT)] for _ in range(ROW_COUNT)]
        self.current_piece = None
        self.current_pos = [0, 0]
        self.new_piece()
        self.game_over = False

    def new_piece(self):
        self.current_piece = random.choice(SHAPES)
        self.current_pos = [COLUMN_COUNT // 2 - len(self.current_piece[0]) // 2, 0]
        if self.collides(self.current_piece, self.current_pos):
            self.game_over = True

    def collides(self, piece, pos):
        px, py = pos
        for y, row in enumerate(piece):
            for x, cell in enumerate(row):
                if cell:
                    bx, by = px + x, py + y
                    if bx < 0 or bx >= COLUMN_COUNT or by >= ROW_COUNT:
                        return True
                    if by >= 0 and self.board[by][bx] != 0:
                        return True
        return False

    def freeze_piece(self):
        px, py = self.current_pos
        for y, row in enumerate(self.current_piece):
            for x, cell in enumerate(row):
                if cell:
                    self.board[py + y][px + x] = cell
        self.clear_lines()
        self.new_piece()

    def clear_lines(self):
        new_board = [row for row in self.board if any(cell == 0 for cell in row)]
        lines_cleared = ROW_COUNT - len(new_board)
        for _ in range(lines_cleared):
            new_board.insert(0, [0 for _ in range(COLUMN_COUNT)])
        self.board = new_board

    def rotate(self, piece):
        return [[piece[y][x] for y in range(len(piece))] for x in reversed(range(len(piece[0])))]

    def run(self):
        drop_event = pygame.USEREVENT + 1
        pygame.time.set_timer(drop_event, 500)

        while not self.game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_over = True
                elif event.type == drop_event:
                    self.move_down()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.move(-1)
                    elif event.key == pygame.K_RIGHT:
                        self.move(1)
                    elif event.key == pygame.K_DOWN:
                        self.move_down()
                    elif event.key == pygame.K_UP:
                        self.rotate_piece()

            self.draw()
            self.clock.tick(60)

        pygame.quit()

    def move(self, dx):
        new_pos = [self.current_pos[0] + dx, self.current_pos[1]]
        if not self.collides(self.current_piece, new_pos):
            self.current_pos = new_pos

    def move_down(self):
        new_pos = [self.current_pos[0], self.current_pos[1] + 1]
        if not self.collides(self.current_piece, new_pos):
            self.current_pos = new_pos
        else:
            self.freeze_piece()

    def rotate_piece(self):
        rotated = self.rotate(self.current_piece)
        if not self.collides(rotated, self.current_pos):
            self.current_piece = rotated

    def draw(self):
        self.screen.fill((0, 0, 0))
        # 画已固定方块
        for y, row in enumerate(self.board):
            for x, cell in enumerate(row):
                if cell != 0:
                    pygame.draw.rect(
                        self.screen,
                        COLORS[cell],
                        (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE),
                    )

        # 画当前方块
        px, py = self.current_pos
        for y, row in enumerate(self.current_piece):
            for x, cell in enumerate(row):
                if cell != 0 and py + y >= 0:
                    pygame.draw.rect(
                        self.screen,
                        COLORS[cell],
                        ((px + x) * BLOCK_SIZE, (py + y) * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE),
                    )

        pygame.display.flip()


if __name__ == '__main__':
    game = Tetris()
    game.run()
