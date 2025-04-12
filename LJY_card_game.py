import pygame
import sys
import random
import math

# 初始化 Pygame
pygame.init()

# 设置屏幕大小
screen_width = 1500
screen_height = 800
screen = pygame.display.set_mode((screen_width, screen_height))

# 设置标题
pygame.display.set_caption("ljy唐氏卡牌游戏")

# 定义颜色
COLORS = {
    "background": (30, 30, 60),
    "card_normal": (255, 215, 0),
    "card_selected": (255, 69, 0),
    "border": (255, 255, 255),
    "button": (50, 180, 100),
    "button_hover": (70, 200, 130),
    "text": (255, 255, 255)
}

# 卡牌大小和样式
card_width = 120
card_height = 180
card_radius = 15



# 卡牌数据结构
class Card:
    def __init__(self, x, y, row, col):
        self.rect = pygame.Rect(x, y, card_width, card_height)
        self.selected = False
        self.row = row
        self.col = col
        self.float_offset = 0  # 浮动动画偏移
        self.scale = 1.0
        self.float_phase = random.random() * 2 * math.pi  # 初始化浮动相位

    def update_animation(self):
        # 浮动动画
        self.float_offset = math.sin(self.float_phase) * 5
        self.float_phase += 0.05
        # 选中时的缩放动画
        self.scale = 1.0 + (0.1 if self.selected else 0) * abs(math.sin(pygame.time.get_ticks() / 200))

# 创建卡牌
def create_cards():
    cards = []
    card_count = [3, 6, 9]  # 每行卡牌数量
    for row in range(3):
        start_x = (screen_width - (card_count[row] * (card_width + 30))) // 2
        for col in range(card_count[row]):
            x = start_x + col * (card_width + 30)
            y = 30 + row * (card_height + 50)
            cards.append(Card(x, y, row, col))
    return cards, card_count

# 绘制卡牌
def draw_cards(cards):
    for card in cards:
        # 计算动画效果后的矩形
        scaled_width = int(card_width * card.scale)
        scaled_height = int(card_height * card.scale)
        temp_rect = card.rect.copy()
        temp_rect.inflate_ip(scaled_width - card.rect.width, scaled_height - card.rect.height)
        temp_rect.move_ip(0, card.float_offset)

        # 绘制卡牌
        color = COLORS["card_selected"] if card.selected else COLORS["card_normal"]
        pygame.draw.rect(screen, color, temp_rect, border_radius=card_radius)
        pygame.draw.rect(screen, COLORS["border"], temp_rect, 2, border_radius=card_radius)

# 检测鼠标点击是否在卡牌上
def check_card_click(cards, pos):
    for card in cards:
        if card.rect.collidepoint(pos):
            card.selected = not card.selected
            return True
    return False

# 更新卡牌状态
def update_card_state(cards, card_count):
    for row in range(3):
        card_count[row] = sum(1 for card in cards if card.row == row and not card.selected)

# 检查是否所有卡牌都被选中
def check_all_cards_selected(cards):
    return all(card.selected for card in cards)

# 绘制背景
def draw_background():
    screen.fill(COLORS["background"])
    # 添加动态背景效果
    for i in range(50):
        x = (pygame.time.get_ticks() * 0.05 + i * 30) % screen_width
        y = screen_height // 4 + math.sin(pygame.time.get_ticks() / 500 + i) * 40
        pygame.draw.circle(screen, COLORS["button"], (int(x), int(y)), 5)

# 显示文本消息
def draw_text(text, font_size, color, x, y):
    font = pygame.font.Font(None, font_size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    screen.blit(text_surface, text_rect)

# 电脑策略（保持原有逻辑）
strategy_map = {
    (3, 6, 7): (1, 6, 7),
    (2, 6, 9): (2, 6, 4),
    (0, 6, 9): (0, 6, 6),

    (2, 2, 3): (1, 2, 3),  # 123
    (3, 2, 3): (1, 2, 3),

    (1, 3, 3): (1, 2, 3),
    (1, 4, 3): (1, 2, 3),
    (1, 5, 3): (1, 2, 3),
    (1, 6, 3): (1, 2, 3),

    (1, 2, 9): (1, 2, 3),
    (1, 2, 8): (1, 2, 3),
    (1, 2, 7): (1, 2, 3),
    (1, 2, 6): (1, 2, 3),
    (1, 2, 5): (1, 2, 3),
    (1, 2, 4): (1, 2, 3),

    (3, 6, 4): (2, 6, 4),  # 264
    (2, 6, 5): (2, 6, 4),
    (2, 6, 6): (2, 6, 4),
    (2, 6, 7): (2, 6, 4),
    (2, 6, 8): (2, 6, 4),
    (2, 6, 9): (2, 6, 4),

    (3, 4, 6): (2, 4, 6),# 246
    (2, 5, 6): (2, 4, 6),
    (2, 6, 6): (2, 4, 6),
    (2, 4, 7): (2, 4, 6),
    (2, 4, 8): (2, 4, 6),
    (2, 4, 9): (2, 4, 6),

    (1, 5, 5): (1, 4, 5),  # 145
    (1, 6, 5): (1, 4, 5),
    (2, 4, 5): (1, 4, 5),
    (3, 4, 5): (1, 4, 5),
    (1, 4, 6): (1, 4, 5),
    (1, 4, 7): (1, 4, 5),
    (1, 4, 8): (1, 4, 5),
    (1, 4, 9): (1, 4, 5),

    (0, 1, 1): (0, 1, 0),
    (1, 0, 1): (1, 0, 0),
    (1, 1, 0): (1, 0, 0),
    (1, 1, 1): (1, 1, 0),

    (3, 6, 8): (3, 6, 5),
    (0, 4, 9): (1, 4, 5),
    (1, 4, 9): (1, 4, 5),

    (3,6,5):(2,6,5)

    # 可以继续添加更多局势和对应的策略

    }
# 电脑策略（示例）
def computer_strategy(card_count):
    # 打印当前局势
    print("局势：")
    print(card_count)

    target_set145 = {1, 4, 5}
    target_set167 = {1, 6, 7}
    target_set123 = {1, 2, 3}

    card_count_tuple = tuple(card_count)



    if card_count.count(0) == 2:
        # 找到非零的那个数的索引
        remaining_index = card_count.index(max(card_count))
        # 将剩下的那个数变为0
        target_state = list(card_count)
        target_state[remaining_index] = 1
    # 检查是否有0
    elif 0 in card_count:
        print("有0")
        # 找到非零的两个数
        non_zero_counts = [count for count in card_count if count > 0]
        # 找到非零数中的最小值
        min_count = min(non_zero_counts)
        if(min_count == 1):
            print("最小是1")
            n=0
            for count in card_count:
                n+=count
            if n>2:
                target_state = [0 if count != 1 else 1 for count in card_count]
        # 将所有非零数减少到最小值
        else:
            target_state = [min_count if count > 0 else 0 for count in card_count]



        # 检查是否有两个数相等，且这两个数都是1
    elif len(set(card_count)) == 2 and card_count.count(1) == 2:
        # 找到剩下的那个数的索引
        remaining_index = [i for i, count in enumerate(card_count) if count != 1][0]
        # 将剩下的那个数变为1
        target_state = list(card_count)
        target_state[remaining_index] = 1

    elif len(set(card_count)) == 2:
        #找到相等的两个数
        equal_counts = [count for count in card_count if card_count.count(count) > 1]
        # 找到剩下的那个数的索引
        remaining_index = [i for i, count in enumerate(card_count) if count not in equal_counts][0]
        # 将剩下的那个数变为0
        target_state = list(card_count)
        target_state[remaining_index] = 0

    elif len(set(card_count) & target_set123) == 2:
        target_state = list(card_count)
        # 找出1、4、5中未出现在当前状态中的那个数
        remaining_num = list(target_set123 - set(card_count))[0]

        # 找出当前状态中第三个数的索引
        for i, num in enumerate(card_count):
            if num not in target_set123:
                # 比较并更新
                if num > remaining_num:
                    target_state[i] = remaining_num
                    print("进入了123")
                    print(target_state)

    elif len(set(card_count) & target_set145) == 2:
        target_state = list(card_count)
        # 找出1、4、5中未出现在当前状态中的那个数
        remaining_num = list(target_set145 - set(card_count))[0]

        # 找出当前状态中第三个数的索引
        for i, num in enumerate(card_count):
            if num not in target_set145:
                # 比较并更新
                if num > remaining_num:
                    target_state[i] = remaining_num
                    print("进入了145")
                    print(target_state)

    elif len(set(card_count) & target_set167) == 2:
        target_state = list(card_count)
        # 找出1、4、5中未出现在当前状态中的那个数
        remaining_num = list(target_set167 - set(card_count))[0]

        # 找出当前状态中第三个数的索引
        for i, num in enumerate(card_count):
            if num not in target_set167:
                # 比较并更新
                if num > remaining_num:
                    target_state[i] = remaining_num
                    print("进入了167")
                    print(target_state)

    if card_count_tuple in strategy_map:
        target_state = strategy_map[card_count_tuple]
        print("target:")
        print(target_state)

    else:
        card_count_tuple = tuple(card_count)
        if card_count_tuple in strategy_map:
            target_state = strategy_map[card_count_tuple]
            print("target:")
            print(target_state)


    # 计算策略：找到发生变化的行和数量
    print(target_state)
    for row in range(len(card_count)):
        if card_count[row] != target_state[row]:
            n = card_count[row] - target_state[row]
            return [row, n]


# 执行电脑策略
def apply_computer_strategy(cards, strategy):
    row, n = strategy
    selected_cards = [card for card in cards if card.row == row and not card.selected]
    selected_cards = selected_cards[-n:]
    for card in selected_cards:
        card.selected = True

# 主程序
def main():
    clock = pygame.time.Clock()
    cards, card_count = create_cards()
    user_turn = True
    computer_turn = False
    game_over = False

    # 按钮
    button_rect = pygame.Rect(screen_width // 2 - 250, screen_height - 100, 250, 80)  # 将按钮的 y 坐标调整为 screen_height - 200
    replay_button_rect = pygame.Rect(screen_width // 2 + 150, screen_height - 100, 150, 80)  # 同样调整重置按钮的 y 坐标

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos) and user_turn:
                    if any(not card.selected for card in cards):
                        update_card_state(cards, card_count)
                        user_turn = False
                        computer_turn = True
                    else:
                        draw_text("请先选择卡牌", 48, COLORS["card_selected"], screen_width // 2, screen_height // 2)
                elif replay_button_rect.collidepoint(event.pos):
                    cards, card_count = create_cards()
                    user_turn = True
                    computer_turn = False
                    game_over = False
                else:
                    check_card_click(cards, event.pos)

        if computer_turn and not game_over:
            strategy = computer_strategy(card_count)
            apply_computer_strategy(cards, strategy)
            update_card_state(cards, card_count)
            computer_turn = False
            user_turn = True

        if check_all_cards_selected(cards):
            game_over = True

        draw_background()

        draw_cards(cards)

        pygame.draw.rect(screen, COLORS["button"], button_rect, border_radius=10)
        draw_text("SELECT", 48, COLORS["text"], button_rect.centerx, button_rect.centery)

        pygame.draw.rect(screen, COLORS["button"], replay_button_rect, border_radius=10)
        draw_text("REPLAY", 48, COLORS["text"], replay_button_rect.centerx, replay_button_rect.centery)

        if game_over:
            draw_text("You Are Lost!", 72, COLORS["card_selected"], screen_width // 2 +583, screen_height // 2)

        pygame.display.flip()

        clock.tick(60)

if __name__ == "__main__":
    main()
