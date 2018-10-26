import arcade
import random

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
MOVEMENT_SPEED = 5

class Paddle:
    def __init__(self,rect_change_x,lft,rt,tp,btm,clr,otln):
        self.rect_change_x = rect_change_x
        self.lft = lft
        self.rt = rt
        self.tp = tp
        self.btm = btm
        self.clr = clr
        self.otln = otln

    def draw(self):
        arcade.draw_lrtb_rectangle_outline(self.lft,self.rt,self.tp,self.btm,self.clr,self.otln)

    def update(self):
        self.lft += self.rect_change_x
        self.rt += self.rect_change_x

class Ball:
    """ This class manages a ball bouncing on the screen. """

    def __init__(self, position_x, position_y, change_x, change_y, radius, color):
        """ Constructor. """
        self.color_list = [arcade.color.AERO_BLUE, arcade.color.AFRICAN_VIOLET,arcade.color.AMBER,\
                            arcade.color.ASH_GREY,arcade.color.AUBURN,arcade.color.AVOCADO,arcade.color.BALL_BLUE]
        # Take the parameters of the init function above, and create instance variables out of them.
        self.position_x = position_x
        self.position_y = position_y
        self.change_x = change_x
        self.change_y = change_y
        self.radius = radius
        self.color = color

    def ball_moves(self):
        # Move the ball
        self.position_y += self.change_y
        self.position_x += self.change_x

    def draw(self):
        """ Draw the balls with the instance variables we have. """
        arcade.draw_circle_filled(self.position_x, self.position_y, self.radius, self.color)


class BallGame(arcade.Window):
    def __init__(self, width, height,title):
        super().__init__(width,height,title)
        #set set_background_color
        arcade.set_background_color(arcade.color.BLACK)
        # create Paddle
        self.my_paddle = Paddle(0, 250, 450, 50, 50,arcade.color.BABY_PINK, 5)
        #create balls
        ball_1 = Ball(100, 20, 2, 3, 15, arcade.color.AUBURN)
        ball_2 = Ball(20, 40, 3, 2, 7, arcade.color.AVOCADO)
        ball_3 = Ball(50, 30, 2, 2, 3, arcade.color.BALL_BLUE)

        self.ball_list = [ball_1,ball_2,ball_3]


    def on_draw(self):
        '''called when we need to draw to the window'''
        arcade.start_render()
        self.my_paddle.draw()
        for ball in self.ball_list:
            ball.draw()

    def x_paddle_logic(self,x_pos,rad):
        return (self.my_paddle.lft+rad < (x_pos)) and ((x_pos) < self.my_paddle.rt-rad)

    def y_paddle_logic(self,y_pos,rad2):
        return ((y_pos) <= self.my_paddle.tp+rad2 and (y_pos) >= self.my_paddle.btm-rad2)

    def check_pos(self):
        """ Code to control the ball's movement. """
        for ball in self.ball_list:
            ball.ball_moves()

            # See if the balls hit the edge of the screen. If so, change direction
            if ball.position_x < ball.radius:
                ball.change_x *= -1
                ball.color = random.choice(ball.color_list)

            if ball.position_x > SCREEN_WIDTH - ball.radius:
                ball.change_x *= -1.001
                ball.color = random.choice(ball.color_list)

            if ball.position_y < ball.radius:
                ball.change_y *= -1.002
                ball.color = random.choice(ball.color_list)

            if ball.position_y > SCREEN_HEIGHT - ball.radius:
                ball.change_y *= -1.003
                ball.color = random.choice(ball.color_list)

            #ball contact with paddle logic
            if self.x_paddle_logic(ball.position_x,ball.radius) and self.y_paddle_logic(ball.position_y,ball.radius):
                ball.color = random.choice(ball.color_list)
                self.my_paddle.clr = random.choice(ball.color_list)
                ball.change_x *= 1.003
                ball.change_y *= -1
                if ball.position_y > self.my_paddle.tp:
                    ball.position_y = ball.position_y + 1.5*ball.radius
                if ball.position_y < self.my_paddle.tp:
                    ball.position_y = ball.position_y - ball.radius

    def update(self,delta_time):
        """ Called to update our objects. this method is called approximately 60 times per second."""
        #for ball in self.ball_list:
        self.check_pos()
        self.my_paddle.update()

    def on_key_press(self, key, modifiers):
        """ Called whenever the user presses a key. """
        if key == arcade.key.LEFT and self.my_paddle.lft:
            self.my_paddle.rect_change_x = -MOVEMENT_SPEED
        elif key == arcade.key.RIGHT:
            self.my_paddle.rect_change_x = MOVEMENT_SPEED

    def on_key_release(self, key, modifiers):
        """ Called whenever a user releases a key. """
        if key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.my_paddle.rect_change_x = 0


if __name__ == "__main__":
    gm = BallGame(SCREEN_WIDTH,SCREEN_HEIGHT,"test")
    arcade.run()
