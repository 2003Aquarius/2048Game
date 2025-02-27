"""
使用python代码实现2048小游戏
作者：LHN
"""
import pygame
import sys
import random
from typing import List

pygame.init()
width, height = 400, 450                                                #窗口大小
colors = {
        0:(205, 193, 180), 2:(238, 228, 218), 4:(237, 224, 200),
        8:(242, 177, 121), 16:(245, 149, 99),32:(246, 124, 95),
        64:(246, 94, 59), 128:(237, 207, 114), 256:(237, 204, 97),
        512:(237, 200, 80),1024:(237, 197, 63), 2048:(237, 194, 46)
        }                                                               # 定义颜色
font = pygame.font.Font(None, 36)                            # 使用默认字体，字号36
clock = pygame.time.Clock()                                             # 用于控制帧率
screen = pygame.display.set_mode((width, height))

# 创建4x4全0棋盘
def init_board():
    board = [[0] * 4 for _ in range(4)]
    # 随机生成两个初始数字（2或4）
    for _ in range(4):  # 生成4次
        add_new_number(board)
    return board

# 获取所有空白格子的坐标
def add_new_number(board):
    empty_cells = [(x, y) for x in range(4) for y in range(4) if board[x][y] == 0]

    if empty_cells:  # 随机选择一个空白格子
        x, y = random.choice(empty_cells)  # 90%概率生成2，10%生成4
        board[x][y] = 2 if random.random() < 0.9 else 4

# 向左移动
def move_left(board, score):
    moved = False
    for row in board:
        clean_row = [num for num in row if num != 0]
        i = 0
        while i < len(clean_row) - 1:
            if clean_row[i] == clean_row[i + 1]:
                clean_row[i] *= 2
                score += clean_row[i]
                clean_row.pop(i + 1)
                clean_row.append(0)
                moved = True
            i += 1
        clean_row += [0] * (4 - len(clean_row))
        if row != clean_row:
            moved = True
            row[:] = clean_row
    return moved, score

# 向右移动
def move_right(board, score):
    for row in board:
        row.reverse()
    moved, score = move_left(board, score)
    for row in board:
        row.reverse()
    return moved, score

# 向上移动
def move_up(board: List[List[int]], score: int):
    transposed = [list(row) for row in zip(*board)]
    moved, score = move_left(transposed, score)
    new_board = [list(row) for row in zip(*transposed)]
    for i in range(4):
        board[i][:] = new_board[i]
    return moved, score

# 向下移动
def move_down(board: List[List[int]], score: int):
    transposed = [list(row) for row in zip(*board)]
    moved, score = move_right(transposed, score)
    new_board = [list(row) for row in zip(*transposed)]
    for i in range(4):
        board[i][:] = new_board[i]
    return moved, score

# 绘制背景板
def draw_board(board, screen):
    screen.fill((187, 173, 160))  # 背景色
    for y in range(4):
        for x in range(4):
            value = board[y][x]
            # 绘制方块
            pygame.draw.rect(screen, colors.get(value, (0, 0, 0)),
                             (x * 100 + 5, y * 100 + 5, 90, 90))
            if value != 0:
                # 渲染数字文本
                text = font.render(str(value), True, (0, 0, 0))
                text_rect = text.get_rect(center=(x * 100 + 50, y * 100 + 50))
                screen.blit(text, text_rect)
    pygame.display.update()

#在屏幕中显示分数
def score_display(score):
    score_font = pygame.font.Font(None, 36)
    score_text = score_font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (10, 410))  # 位置在棋盘下方

def button(screen):
    screen_width, screen_height = screen.get_size()
    width, height = 120, 40
    margin = 10  # 按钮与屏幕边缘的距离

    # 计算按钮的位置，使其位于右下角
    x = screen_width - width - margin
    y = screen_height - height - margin

    button_rect = pygame.Rect(x, y, width, height)
    button_color = (187, 173, 160)
    border_color = (255, 255, 255)
    text_color = (255, 255, 255)
    button_font = pygame.font.Font(None, 36)
    button_text = button_font.render("Restart", True, text_color)

    # 绘制按钮
    pygame.draw.rect(screen, button_color, button_rect)
    # 绘制边框
    border_width = 3  # 设置边框宽度
    pygame.draw.rect(screen, border_color, button_rect, border_width)
    # 在按钮上显示文本
    screen.blit(button_text,
                (button_rect.centerx - button_text.get_width() /2,
                 button_rect.centery - button_text.get_height() /2))

    return button_rect

# 判断游戏是否结束
def judge_game_over(board):
    for row in board:
        if 0 in row:
            return False
    # 检查是否有相邻相同数字可以合并
    for i in range(4):
        for j in range(4):
            if j < 3 and board[i][j] == board[i][j + 1]:  # 水平方向
                return False
            if i < 3 and board[i][j] == board[i + 1][j]:  # 垂直方向
                return False
    return True

# 绘制游戏结束的标识
def draw_game_over(screen):
    font = pygame.font.Font(None, 48)
    over_text = font.render("Game Over!", True, (255, 0, 0))
    restart_text = font.render("Press R to restart game", True, (255, 0, 0))
    # 获取文本的Rect对象
    over_text_rect = over_text.get_rect()
    restart_text_rect = restart_text.get_rect()
    # 设置文本的中心点，使其相对于屏幕中心定位
    screen_center_x, screen_center_y = screen.get_width() // 2, screen.get_height() // 2
    over_text_rect.center = (screen_center_x, screen_center_y - 30)  # 上移一些
    restart_text_rect.center = (screen_center_x, screen_center_y + 30)  # 下移一些
    # 使用计算好的位置绘制文本
    screen.blit(over_text, over_text_rect)
    screen.blit(restart_text, restart_text_rect)

# 重启游戏
def reset_game(board):
    # 重置棋盘和分数
    for x in range(4):
        for y in range(4):
            board[x][y] = 0

    # 添加4个新的数字到棋盘上
    for _ in range(4):
        add_new_number(board)
    return board

def main():
    board = init_board()
    score = 0
    running = True
    game_over = False
    while running:
        moved = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                # 游戏未结束时允许移动
                if not game_over:
                    if event.key == pygame.K_LEFT:
                        moved, score = move_left(board, score)
                    elif event.key == pygame.K_RIGHT:
                        moved, score = move_right(board, score)
                    elif event.key == pygame.K_UP:
                        moved, score = move_up(board, score)
                    elif event.key == pygame.K_DOWN:
                        moved, score = move_down(board, score)
                # 按下R键时重置游戏
                if game_over and event.key == pygame.K_r:
                    board = reset_game(board)
                    print('您的最终得分为：',score)
                    score = 0
                    game_over = False
            # 在鼠标点击事件中检查是否点击了按钮
            elif event.type == pygame.MOUSEBUTTONDOWN:
                button_rect = button(screen)
                if button_rect.collidepoint(event.pos):
                    board = reset_game(board)
                    score = 0
                    game_over = False
        # 如果发生有效移动，生成新数字
        if moved:
            add_new_number(board)

        if not game_over and judge_game_over(board):
            game_over = True
        draw_board(board, screen)
        score_display(score)
        button(screen)
        # 游戏结束绘制画面
        if game_over:
            screen.fill((255, 255, 255))
            draw_game_over(screen)
        pygame.display.flip()
        clock.tick(30)
    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()