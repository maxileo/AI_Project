import pygame
import json
import random
import sys

from update_response_scores import update_response_scores

pygame.init()


class Button:
    def __init__(self, rect, fill_color, hover_color, outline_color, text, font_size, should_draw = True):
        self.rect = rect
        self.fill_color = fill_color
        self.hover_color = hover_color
        self.outline_color = outline_color
        self.text = text
        self.font_size = font_size
        self.font = pygame.font.Font(None, self.font_size)
        self.outline_weight = 2

        self.should_draw = should_draw

    def drawTextWrapped(self, surface, text, color, rect, font):
        y = rect.top
        lineSpacing = -2

        fontHeight = font.size("Tg")[1]

        while text:
            i = 1
            if y + fontHeight > rect.bottom:
                break
            while font.size(text[:i])[0] < rect.width and i < len(text):
                i += 1
            if i < len(text): 
                i = text.rfind(" ", 0, i) + 1
            
            image = font.render(text[:i], True, color)

            surface.blit(image, (rect.left, y))
            y += fontHeight + lineSpacing
            text = text[i:]

        return text

    def draw(self, surface, center=False, wrapped=True):
        fill_color = self.fill_color
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if self.clicked(mouse_x, mouse_y):
            fill_color = self.hover_color
        pygame.draw.rect(surface, fill_color, self.rect, self.rect.height // 2, 40, 40, 40, 40)
        pygame.draw.rect(surface, self.outline_color, self.rect, self.outline_weight, 40, 40, 40, 40)

        if wrapped:
            w, h = self.rect.width / 16, self.rect.height / 8
            text_rect = pygame.Rect(self.rect.x + w, self.rect.y + h, self.rect.width - 2 * w, self.rect.height - 2 * h)
            self.drawTextWrapped(surface, self.text, WHITE, text_rect, self.font)
        elif center:
            text_surface = self.font.render(self.text, True, WHITE)
            text_rect = text_surface.get_rect(center=self.rect.center)
            surface.blit(text_surface, text_rect)

    def clicked(self, mouse_x, mouse_y):
        if self.rect.collidepoint((mouse_x, mouse_y)):
            return True
        return False

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BACKGROUND_COLOR = (52, 55, 69)

WIDTH, HEIGHT = 800, 750
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Questions")

class QuestionsManager:
    def __init__(self, file_path):
        self.questions = []
        with open(file_path, "r", encoding="utf-8") as file:
            for line in file:
                try:
                    data = json.loads(line)
                    self.questions.append(data)
                except:
                    print("Error")

    def processEventsWhileWriting(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                    return True
        return False

    def processClick(self, mouseX, mouseY, surface):
        pressedButton = None
        if self.answer1_button.clicked(mouseX, mouseY):
            # process answer press
            pressedButton = self.answer1_button
        if self.answer2_button.clicked(mouseX, mouseY):
            # process answer press
            pressedButton = self.answer2_button
        
        if pressedButton != None and pressedButton.text == self.human_answer:
            w, h = 200, 80
            result_rect = pygame.Rect(WIDTH // 2 - w/2, HEIGHT // 2 - h / 2, w, h)
            self.result_button = Button(result_rect, (163, 73, 38), (163, 73, 38), (45, 45, 45), "GRESIT :(", 18, should_draw=True)
            update_response_scores(self.question_button.text, self.human_answer, self.chatgpt_answer)
        if pressedButton != None and pressedButton.text == self.chatgpt_answer:
            w, h = 200, 80
            result_rect = pygame.Rect(WIDTH // 2 - w/2, HEIGHT // 2 - h / 2, w, h)
            self.result_button = Button(result_rect, (204, 154, 39), (204, 154, 39), (45, 45, 45), "CORECT :)", 18, should_draw=True)
            update_response_scores(self.question_button.text, self.chatgpt_answer, self.human_answer)

        if pressedButton != None:
            self.result_button.draw(surface, center=True, wrapped=False)
            pygame.display.flip()
            pygame.time.delay(1500)
            resetResult = self.resetQuestion()
            while resetResult == False:
                resetResult = self.resetQuestion()
    
    def drawWordByWord(self, surface, button):
        text = button.text
        words = text.split(" ")
        textSoFar = ""
        for word in words:
            textSoFar += word + " "
            button.text = textSoFar
            button.draw(surface, wrapped=True)
            pygame.display.flip()
            pressSkip = self.processEventsWhileWriting()
            if pressSkip:
                break
            pygame.time.delay(self.delayBetweenWords)
            self.delayBetweenWords -= 2
            if self.delayBetweenWords < 40:
                self.delayBetweenWords = 40
        button.text = text
        button.draw(surface, wrapped=True)
        pygame.display.flip()

    def draw(self, surface):
        self.question_button.draw(surface, wrapped=True)
        if self.startedWriting:
            self.delayBetweenWords = 60
            self.drawWordByWord(surface,self.answer1_button)
            self.delayBetweenWords = 60
            self.drawWordByWord(surface,self.answer2_button)
            self.startedWriting = False
        else:
            self.answer1_button.draw(surface, wrapped=True)
            self.answer2_button.draw(surface, wrapped=True)
    
    def resetQuestion(self):
        self.startedWriting = True
        # Choose a random question
        current_question = random.choice(self.questions)
        question_text = current_question["question"]
        if len(current_question["human_answers"]) == 0 or len(current_question["chatgpt_answers"]) == 0:
            return False
        self.human_answer = random.choice(current_question["human_answers"])
        self.chatgpt_answer = random.choice(current_question["chatgpt_answers"])
        self.answers = random.choice([[self.human_answer, self.chatgpt_answer], [self.chatgpt_answer, self.human_answer]])

        w, h = 20, 10
        question_rect = pygame.Rect(w, h, WIDTH - w * 2, HEIGHT // 3 - h * 2)
        self.question_button = Button(question_rect, (96, 97, 115), (96, 97, 115), (45, 45, 45), question_text, 18, should_draw=True)
        answer1_rect = pygame.Rect(WIDTH // 16, HEIGHT // 3 + 10, WIDTH - 2 * WIDTH // 16, HEIGHT // 3 - 10)
        answer2_rect = pygame.Rect(WIDTH // 16, 2 * HEIGHT // 3 + 10, WIDTH - 2 * WIDTH // 16, HEIGHT // 3 - 2 * 10)
        self.answer1_button = Button(answer1_rect, (70, 97, 179), (86, 118, 214), (45, 45, 45), self.answers[0], 18, should_draw=True)
        self.answer2_button = Button(answer2_rect, (186, 106, 74), (235, 127, 84), (45, 45, 45), self.answers[1], 18, should_draw=True)

        return True

questionManager = QuestionsManager("chatgpt.json")
questionManager.resetQuestion()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            questionManager.processClick(mouse_x, mouse_y, screen)

    screen.fill(BACKGROUND_COLOR)
    questionManager.draw(screen)

    pygame.display.flip()

pygame.quit()
