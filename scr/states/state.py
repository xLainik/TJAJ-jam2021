class State:
    def __init__(self, game) -> None:
        self.game = game
        self.previous_state = None        

    def update(self):
        pass
    def render(self):
        pass

    def enter_state(self):
        if len(self.game.state_stack) > 0:
            self.previous_state = self.game.state_stack[-1]
        self.game.transition_timer = 50
        self.game.state_stack.append(self)        

    def exit_state(self, restart = False):
        if restart:
            self.previous_state.__init__(self.game)
        self.game.transition_timer = 50        
        self.game.state_stack.pop()
