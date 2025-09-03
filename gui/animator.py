import pygame
import sys
import random
from buddy_system import BuddySystem  # <- importamos la lógica desde otro archivo

# ------------------------------
# Interfaz gráfica Pygame
# ------------------------------
WINDOW_WIDTH = 1100
WINDOW_HEIGHT = 720
PADDING = 240
BAR_TOP = 180
BAR_HEIGHT = 140
FONT_NAME = "Arial"

FREE_COLOR = (92, 199, 122)
USED_COLOR = (232, 97, 97)
BORDER_COLOR = (40, 40, 40)
BG_COLOR = (248, 248, 248)
TEXT_COLOR = (20, 20, 20)
HINT_COLOR = (90, 90, 90)
INPUT_BG_COLOR = (255, 255, 255)
INPUT_BORDER_COLOR = (180, 180, 180)

TOTAL_MEMORY = 1024  # en KB (potencia de 2)

class BuddyUI:
    def __init__(self, buddy: BuddySystem):
        pygame.init()
        pygame.display.set_caption("Simulador Buddy System - KB")
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(FONT_NAME, 18)
        self.font_small = pygame.font.SysFont(FONT_NAME, 14)
        self.font_big = pygame.font.SysFont(FONT_NAME, 24, bold=True)
        self.buddy = buddy
        self.input_text = ""
        self.message = ""
        self.message_timer = 0
        self.input_active = False
        self.input_rect = pygame.Rect(WINDOW_WIDTH - 320, 100, 200, 36)
        self.block_positions = []

    def draw_text(self, text, x, y, font=None, color=TEXT_COLOR, centered=False):
        if font is None:
            font = self.font
        surf = font.render(text, True, color)
        if centered:
            self.screen.blit(surf, (x - surf.get_width() // 2, y))
        else:
            self.screen.blit(surf, (x, y))

    def get_leaves(self):
        leaves = []
        def traverse(node, start):
            if node is None:
                return
            if node["left"] or node["right"]:
                traverse(node["left"], start)
                if node["left"]:
                    start += node["left"]["size"]
                traverse(node["right"], start)
            else:
                leaves.append({
                    "start": start,
                    "size": node["size"],
                    "is_free": node["is_free"],
                    "process": node["process"]
                })
        traverse(self.buddy.get_tree(), 0)
        leaves.sort(key=lambda b: b["start"])
        return leaves

    def draw_memory_bar(self):
        leaves = self.get_leaves()
        total = TOTAL_MEMORY
        x0 = PADDING
        y0 = BAR_TOP
        w_total = WINDOW_WIDTH - 2 * PADDING

        pygame.draw.rect(self.screen, BORDER_COLOR, (x0, y0, w_total, BAR_HEIGHT), width=2, border_radius=8)
        self.block_positions.clear()

        for leaf in leaves:
            x = x0 + int((leaf["start"] / total) * w_total)
            w = int((leaf["size"] / total) * w_total)
            rect = pygame.Rect(x + 1, y0 + 1, max(1, w - 2), BAR_HEIGHT - 2)
            color = FREE_COLOR if leaf["is_free"] else USED_COLOR
            pygame.draw.rect(self.screen, color, rect, border_radius=4)
            pygame.draw.rect(self.screen, BORDER_COLOR, rect, width=1, border_radius=4)

            if not leaf["is_free"] and leaf["process"]:
                self.block_positions.append((rect, leaf["process"]))

            if w > 40:
                label = f"{leaf['size']}KB" if leaf["is_free"] else f"{leaf['process']}"
                text_color = (20, 20, 20) if leaf["is_free"] else (240, 240, 240)
                surf = self.font_small.render(label, True, text_color)
                if surf.get_width() < w - 6:
                    self.screen.blit(surf, (x + (w - surf.get_width()) // 2,
                                             y0 + (BAR_HEIGHT - surf.get_height()) // 2))

    def draw_sidebar(self):
        self.draw_text("Simulador Buddy System (KB)", WINDOW_WIDTH // 2, 20, self.font_big, centered=True)
        instructions = [
            "INSTRUCCIONES:",
            "- Escribe tamaño en KB y presiona ENTER o botón para asignar",
            "- Haz clic en bloque rojo para liberar",
            "- R: asignar bloque aleatorio, C: reiniciar"
        ]
        for i, line in enumerate(instructions):
            self.draw_text(line, PADDING, 60 + i * 24, self.font_small, HINT_COLOR)

        used = self.get_used_memory()
        free = TOTAL_MEMORY - used
        self.draw_text(f"Memoria Total: {TOTAL_MEMORY}KB", PADDING, BAR_TOP - 30)
        self.draw_text(f"Memoria Usada: {used}KB", PADDING + 200, BAR_TOP - 30)
        self.draw_text(f"Memoria Libre: {free}KB", PADDING + 400, BAR_TOP - 30)

        pygame.draw.rect(self.screen, INPUT_BG_COLOR, self.input_rect, border_radius=6)
        pygame.draw.rect(self.screen,
                         INPUT_BORDER_COLOR if not self.input_active else (100, 100, 200),
                         self.input_rect, width=2, border_radius=6)
        prompt = "Tamaño (KB): " + self.input_text
        self.draw_text(prompt, self.input_rect.x + 10, self.input_rect.y + 8)

        button_rect = pygame.Rect(self.input_rect.x + self.input_rect.width + 10,
                                  self.input_rect.y, 80, self.input_rect.height)
        pygame.draw.rect(self.screen, (70, 130, 180), button_rect, border_radius=6)
        self.draw_text("Asignar", button_rect.x + button_rect.width // 2,
                       button_rect.y + 8, centered=True, color=(255, 255, 255))
        return button_rect

    def get_used_memory(self):
        total = 0
        def traverse(node):
            nonlocal total
            if node is None:
                return
            if node["left"] or node["right"]:
                traverse(node["left"])
                traverse(node["right"])
            else:
                if not node["is_free"]:
                    total += node["size"]
        traverse(self.buddy.get_tree())
        return total

    def run(self):
        running = True
        while running:
            mouse_pos = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    for rect, process_name in self.block_positions:
                        if rect.collidepoint(mouse_pos):
                            if self.buddy.deallocate(process_name):
                                self.message = f"Liberado {process_name}"
                                self.message_timer = 120
                    if self.input_rect.collidepoint(mouse_pos):
                        self.input_active = True
                    else:
                        self.input_active = False
                    button_rect = pygame.Rect(self.input_rect.x + self.input_rect.width + 10,
                                              self.input_rect.y, 80, self.input_rect.height)
                    if button_rect.collidepoint(mouse_pos) and self.input_text:
                        self.assign_process()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    elif event.key == pygame.K_RETURN and self.input_text:
                        self.assign_process()
                    elif event.key == pygame.K_BACKSPACE:
                        self.input_text = self.input_text[:-1]
                    elif event.key == pygame.K_c:
                        self.buddy.reset_memory()
                        self.message = "Memoria reiniciada"
                        self.message_timer = 120
                    elif event.key == pygame.K_r:
                        size = random.randint(1, 1024)
                        name = f"P{random.randint(1, 99)}"
                        ok, rounded = self.buddy.allocate(name, size)
                        if ok:
                            self.message = f"Asignado {name} (solicitado {size}KB → asignado {rounded}KB)"
                        else:
                            self.message = f"No hay espacio para {size}KB"
                        self.message_timer = 120
                    else:
                        if event.unicode.isdigit() and len(self.input_text) < 6:
                            self.input_text += event.unicode

            self.screen.fill(BG_COLOR)
            self.draw_sidebar()
            self.draw_memory_bar()

            if self.message and self.message_timer > 0:
                self.draw_text(self.message, WINDOW_WIDTH // 2,
                               BAR_TOP + BAR_HEIGHT + 20,
                               self.font, centered=True, color=(200, 60, 60))
                self.message_timer -= 1

            processes_y = BAR_TOP + BAR_HEIGHT + 60
            self.draw_text("PROCESOS ACTIVOS:", PADDING, processes_y, self.font_big)
            processes = self.get_active_processes()
            if processes:
                for i, p in enumerate(processes):
                    self.draw_text(p, PADDING, processes_y + 30 + i * 24, self.font_small)
            else:
                self.draw_text("No hay procesos activos",
                               PADDING, processes_y + 30, self.font_small, HINT_COLOR)

            if self.input_active and pygame.time.get_ticks() % 1000 < 500:
                cursor_x = self.input_rect.x + 10 + self.font.size("Tamaño (KB): " + self.input_text)[0]
                pygame.draw.line(self.screen, TEXT_COLOR,
                                 (cursor_x, self.input_rect.y + 8),
                                 (cursor_x, self.input_rect.y + self.input_rect.height - 8), 2)

            pygame.display.flip()
            self.clock.tick(60)
        pygame.quit()

    def assign_process(self):
        try:
            if not self.input_text.strip():
                self.message = "Ingrese un número válido"
                self.message_timer = 120
                return

            size = int(self.input_text)
            if size <= 0:
                self.message = "El tamaño debe ser mayor a 0"
                self.input_text = ""
                self.message_timer = 120
                return

            name = f"P{random.randint(1, 99)}"
            ok, rounded = self.buddy.allocate(name, size)
            if ok:
                self.message = f"Asignado {name} (solicitado {size}KB → asignado {rounded}KB)"
            else:
                self.message = f"No hay espacio para {size}KB"
        except ValueError:
            self.message = "Entrada inválida, use solo números"
        finally:
            self.input_text = ""
            self.message_timer = 120

    def get_active_processes(self):
        processes = []
        def traverse(node):
            if node is None:
                return
            if node["left"] or node["right"]:
                traverse(node["left"])
                traverse(node["right"])
            else:
                if not node["is_free"] and node["process"]:
                    processes.append(f"{node['process']} ({node['size']}KB)")
        traverse(self.buddy.get_tree())
        return processes

# ------------------------------
# Main
# ------------------------------
if __name__ == "__main__":
    buddy = BuddySystem(TOTAL_MEMORY)  # se importa desde buddy_system.py
    ui = BuddyUI(buddy)
    try:
        ui.run()
    except Exception as e:
        pygame.quit()
        print("Error:", e)
        import traceback
        traceback.print_exc()
        sys.exit(1)
