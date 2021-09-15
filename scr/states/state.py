class State:
    def __init__(self, game, first_time):
        self.game = game

        if first_time:
            self.previous_state = None

    def update(self):
        pass
    def render(self):
        pass

    def enter_state(self):
        if len(self.game.state_stack) > 0:
            self.previous_state = self.game.state_stack[-1]
##            print("previous state", self.previous_state)
        self.game.transition_timer = 50
        self.game.state_stack.append(self)

##        print("entering state, state stack is:")
##        print(self.game.state_stack)
##        print(self.game.current_level)

    def exit_state(self, restart):
        if restart:
##            print("Restarting:", self.previous_state)
            self.previous_state.__init__(self.game, False)
            
        self.game.transition_timer = 50        
        self.game.state_stack.pop()

##        print("EXITING state, state stack is:")
##        print(self.game.state_stack)
##        print(self.game.current_level)
