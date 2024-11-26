import tkinter as tk
import random

# Constants
WIDTH = 600
HEIGHT = 400
PADDLE_WIDTH = 100
PADDLE_HEIGHT = 10
BALL_SIZE = 10
BRICK_WIDTH = 60
BRICK_HEIGHT = 20
ROWS = 5
COLS = 10

class BrickBreaker:
    def __init__(self, master):
        self.master = master
        self.score = 0  # Initialize score
        self.lives = 3  # Initialize number of lives
        self.master.title(f"🎮 Brick Breaker - Score: {self.score} - Lives: {'❤' * self.lives}")
        self.canvas = tk.Canvas(master, width=WIDTH, height=HEIGHT, bg="#FFB6C1")  # Light pink background
        self.canvas.pack()

        # Create paddle
        self.paddle = self.canvas.create_rectangle((WIDTH - PADDLE_WIDTH) / 2, HEIGHT - PADDLE_HEIGHT,
                                                    (WIDTH + PADDLE_WIDTH) / 2, HEIGHT, fill="#FF69B4")  # Hot pink paddle
        # Create ball
        self.ball = self.canvas.create_oval(WIDTH / 2 - BALL_SIZE / 2, HEIGHT / 2 - BALL_SIZE / 2,
                                             WIDTH / 2 + BALL_SIZE / 2, HEIGHT / 2 + BALL_SIZE / 2, fill="#FF4500")  # Orange-red ball
        self.bricks = []  # List to store bricks
        self.dx = 3  # Ball movement in x-axis
        self.dy = -3  # Ball movement in y-axis
        self.create_bricks()  # Create bricks
        self.update_score()  # Update score in title
        self.move_ball()  # Start ball movement
        self.master.bind("<Left>", self.move_left)  # Move paddle left
        self.master.bind("<Right>", self.move_right)  # Move paddle right

    def create_bricks(self):
        for row in range(ROWS):
            for col in range(COLS):
                x1 = col * BRICK_WIDTH + 5
                y1 = row * BRICK_HEIGHT + 5
                x2 = x1 + BRICK_WIDTH - 5
                y2 = y1 + BRICK_HEIGHT - 5
                brick = self.canvas.create_rectangle(x1, y1, x2, y2, fill="#FF1493")  # Deep pink bricks
                self.bricks.append(brick)

    def move_ball(self):
        self.canvas.move(self.ball, self.dx, self.dy)
        ball_pos = self.canvas.coords(self.ball)
        paddle_pos = self.canvas.coords(self.paddle)

        # Check collision with walls
        if ball_pos[0] <= 0 or ball_pos[2] >= WIDTH:
            self.dx = -self.dx
        if ball_pos[1] <= 0:
            self.dy = -self.dy
        if ball_pos[3] >= HEIGHT:
            self.lives -= 1
            if self.lives == 0:
                self.game_over()  # Call game_over function if lives are zero
            else:
                self.reset_ball()  # Reset ball

        # Check collision with paddle
        if (ball_pos[2] >= paddle_pos[0] and ball_pos[0] <= paddle_pos[2] and
                ball_pos[3] >= paddle_pos[1] and ball_pos[3] <= paddle_pos[3]):
            self.dy = -self.dy

        # Check collision with bricks
        for brick in self.bricks:
            if self.check_collision(ball_pos, self.canvas.coords(brick)):
                self.canvas.delete(brick)
                self.bricks.remove(brick)
                self.dy = -self.dy
                self.score += 10
                self.update_score()
                break

        # Check win condition
        if not self.bricks:
            self.congratulations()  # Call congratulations function if all bricks are destroyed

        self.master.after(20, self.move_ball)  # Repeat move_ball function every 20 ms

    def check_collision(self, ball_pos, brick_pos):
        return (ball_pos[2] >= brick_pos[0] and ball_pos[0] <= brick_pos[2] and
                ball_pos[3] >= brick_pos[1] and ball_pos[1] <= brick_pos[3])

    def move_left(self, event):
        self.canvas.move(self.paddle, -20, 0)  # Move paddle left

    def move_right(self, event):
        self.canvas.move(self.paddle, 20 , 0)  # Move paddle right

    def reset_ball(self):
        self.canvas.coords(self.ball, WIDTH / 2 - BALL_SIZE / 2, HEIGHT / 2 - BALL_SIZE / 2,
                           WIDTH / 2 + BALL_SIZE / 2, HEIGHT / 2 + BALL_SIZE / 2)
        self.dx = 3  # Reset ball movement in x-axis
        self.dy = -3  # Reset ball movement in y-axis

    def update_score(self):
        self.master.title(f"🎮 Brick Breaker - Score: {self.score} - Lives: {'❤' * self.lives}")  # Update title with score and lives

    def game_over(self):
        self.canvas.create_text(WIDTH / 2, HEIGHT / 2, text="Yahh kamu kalah", fill="white", font=("Comic Sans MS", 24, "bold"))
        self.canvas.create_text(WIDTH / 2, HEIGHT / 2 + 30, text=f"Skor Akhir: {self.score}", fill="white", font=("Comic Sans MS", 16))
        self.canvas.create_text(WIDTH / 2, HEIGHT / 2 + 60, text="Tekan 'R' untuk Restart", fill="white", font=("Comic Sans MS", 16))
        self.master.bind("<r>", self.restart_game)  # Bind 'R' key to restart game

    def congratulations(self):
        self.canvas.create_text(WIDTH / 2, HEIGHT / 2, text="Asik Menang!", fill="#FF1493", font=("Comic Sans MS", 24, "bold"))
        self.canvas.create_text(WIDTH / 2, HEIGHT / 2 + 30, text=f"Skor Akhir: {self.score}", fill="#FF1493", font=("Comic Sans MS", 16))
        self.canvas.create_text(WIDTH / 2, HEIGHT / 2 + 60, text="Tekan 'R' untuk Restart", fill="#FF1493", font=("Comic Sans MS", 16))
        self.master.bind("<r>", self.restart_game)  # Bind 'R' key to restart game

    def restart_game(self, event):
        self.canvas.delete("all")  # Delete all objects from canvas
        self.score = 0  # Reset score
        self.lives = 3  # Reset number of lives
        self.dx = 3  # Reset ball movement in x-axis
        self.dy = -3  # Reset ball movement in y-axis
        self.create_bricks()  # Recreate bricks
        self.update_score()  # Update score in title
        self.reset_ball()  # Reset ball
        self.move_ball()  # Start ball movement

if __name__ == "__main__":
    root = tk.Tk()
    game = BrickBreaker(root)  # Create instance of BrickBreaker class
    root.mainloop()  # Start the game loop