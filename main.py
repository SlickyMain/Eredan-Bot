import numpy
import time
import pyautogui
import pyscreenshot as image
import cv2 as cv
import pytesseract

pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

play_area = [661, 35, 1225, 1035]
state_text_position = [878, 343, 1003, 380]
start_fight_button = [945, 861]
reroll_button = [941, 710]
cancel_button_position = [789, 914, 1097, 1009]
first_card = [780, 180]
second_card = [774, 439]
third_card = [775, 706]
dices_space_position = [832, 522, 1051, 663]  # 219x141
first_line_dices_y = 11
second_line_dices_y = 88
dices_x = [12, 87, 165]


class Card:
    def __init__(self, x, y):
        self.coord = [x, y]

    @staticmethod
    def throw():
        start_fight()
        time.sleep(1.5)

    def select_card(self):
        pyautogui.click(self.coord[0], self.coord[1], 1, 0, "left")


def start_fight():
    pyautogui.click(start_fight_button[0], start_fight_button[1], 1, 0, "left")


def check_load():
    cancel_button = make_screenshot(*cancel_button_position)
    cv.imwrite("cancel.png", cancel_button)
    cancel_button_image = cv.imread("cancel.png", cv.IMREAD_GRAYSCALE)
    text = pytesseract.image_to_string(cancel_button_image, lang="eng")
    return text


def read_state():
    current_state = make_screenshot(*state_text_position)
    # cv.imshow("window", cv.cvtColor(current_state, cv.COLOR_BGR2GRAY))
    cv.imwrite("image.png", current_state)
    img = cv.imread("image.png")
    text = pytesseract.image_to_string(img, lang="eng")
    return text
    # cv.waitKey(0)


def make_screenshot(x1, y1, x2, y2):
    screen = numpy.array(image.grab(bbox=(x1, y1, x2, y2)))
    return screen


def roll_dices():
    attempts_for_roll = 2
    pinned = 0
    index_pinned = [-1, -1, -1, -1, -1, -1]
    while attempts_for_roll > 0 and pinned < 6:
        skills_space = make_screenshot(*dices_space_position)
        cv.imwrite("dices.png", skills_space)
        skills_image = cv.imread("dices.png", cv.IMREAD_COLOR)
        for i in range(6):
            if i < 3:
                dice_color = skills_image[first_line_dices_y, dices_x[i]]  # y then x
                sum_color = dice_color.sum()
                if sum_color != 221 and index_pinned[i] == -1:
                    pyautogui.click(dices_x[i] + 832, first_line_dices_y + 522, 1, 0, "left")  # x then y
                    index_pinned[i] = i
                    pinned += 1
                    time.sleep(0.5)
            else:
                dice_color = skills_image[second_line_dices_y, dices_x[i - 3]]
                sum_color = dice_color.sum()
                if sum_color != 221 and index_pinned[i] == -1:
                    pyautogui.click(dices_x[i - 3] + 832, second_line_dices_y + 522, 1, 0, "left")  # x then y
                    index_pinned[i] = i
                    pinned += 1
                    time.sleep(0.5)
        pyautogui.click(reroll_button[0], reroll_button[1], 1, 0, "left")
        attempts_for_roll -= 1
        time.sleep(1)


def main():
    time.sleep(3)
    while True:
        start_fight()
        print("Lookin for match")
        time.sleep(2)
        cancel_status = check_load()
        if cancel_status.strip() == "Cancel":
            time.sleep(2)
            print("Still waiting")
        else:
            heroes = 5
            first_warrior = Card(first_card[0], first_card[1])
            second_warrior = Card(second_card[0], second_card[0])
            third_warrior = Card(third_card[0], third_card[1])
            while heroes > 0:
                current_state = read_state()
                play_screen = make_screenshot(*play_area)
                cv.imwrite("end.png", play_screen)
                isEnd = cv.imread("end.png", cv.IMREAD_ANYCOLOR)
                avatar_color = isEnd[297, 129]  # 427
                loot_button = isEnd[955, 200]  # 343
                print(avatar_color.sum())
                print(loot_button.sum())
                time.sleep(4)
                if avatar_color.sum() == 427 and loot_button.sum == 343:
                    time.sleep(4)
                    pyautogui.click(940, 990, 1, 0, "left")
                    time.sleep(2)
                    pyautogui.click(940, 950, 1, 0, "left")
                    time.sleep(3)
                    pyautogui.click(830, 770, 1, 0, "left")
                    time.sleep(3)
                    pyautogui.click(932, 814, 1, 0, "left")
                    time.sleep(0.5)
                    pyautogui.click(940, 875, 1, 0, "left")
                    time.sleep(0.5)
                    pyautogui.click(950, 950, 1, 0, "left")
                    just_check = make_screenshot(747, 814, 784, 878)
                    cv.imwrite("check.png", just_check)
                    isGood = cv.imread("check.png", cv.IMREAD_COLOR)
                    if isGood[32, 16].sum() == 322:
                        pyautogui.click(940, 850, 1, 0, "left")
                        time.sleep(2)
                        pyautogui.click(944, 946, 1, 0, "left")
                        time.sleep(2)
                    break
                print(current_state)
                if heroes == 1:
                    time.sleep(10)
                    roll_dices()
                    heroes -= 1
                    time.sleep(10)
                    print("I am done")
                if current_state.strip() == "ATTACKER":
                    print("I am in attack")
                    first_warrior.select_card()
                    time.sleep(0.5)
                    first_warrior.throw()
                    time.sleep(7)
                    roll_dices()
                    time.sleep(12)
                    heroes -= 1
                    print(f"Now I have {heroes} heroes")
                elif current_state.strip() == "DEFENDEN" or current_state.strip() == "DEFENDES" or current_state.strip() == "DEFENDER":
                    print("I am in def")
                    time.sleep(3)
                    first_warrior.select_card()
                    time.sleep(0.5)
                    first_warrior.throw()
                    time.sleep(2)
                    roll_dices()
                    time.sleep(12)
                    heroes -= 1
                    print(f"Now I have {heroes} heroes")
        time.sleep(7)
        play_screen = make_screenshot(*play_area)
        cv.imwrite("end.png", play_screen)
        isEnd = cv.imread("end.png", cv.IMREAD_ANYCOLOR)
        avatar_color = isEnd[297, 129]  # 427
        loot_button = isEnd[955, 200]  # 343
        if avatar_color.sum() == 427 and loot_button.sum == 343:
            pyautogui.click(940, 990, 1, 0, "left")
            time.sleep(2)
            pyautogui.click(940, 950, 1, 0, "left")
            time.sleep(3)
            pyautogui.click(830, 770, 1, 0, "left")
            time.sleep(3)
            pyautogui.click(932, 814, 1, 0, "left")
            time.sleep(0.5)
            pyautogui.click(940, 875, 1, 0, "left")
            time.sleep(0.5)
            pyautogui.click(950, 950, 1, 0, "left")
            just_check = make_screenshot(747, 814, 784, 878)
            cv.imwrite("check.png", just_check)
            isGood = cv.imread("check.png", cv.IMREAD_COLOR)
            if isGood[32, 16].sum() == 322:
                pyautogui.click(940, 850, 1, 0, "left")
                time.sleep(2)
                pyautogui.click(944, 946, 1, 0, "left")
                time.sleep(2)
    # x, y = pyautogui.position()
    # position_str = 'X:' + str(x).rjust(4) + '  Y:' + str(y).rjust(4)
    # print(position_str, end='')
    # print('\b' * len(position_str), end='', flush=True)
    # time.sleep(10.01)


if __name__ == "__main__":
    main()
