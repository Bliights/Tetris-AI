class Status:
    # Initialyse the game status
    def __init__(self):
        self.game_status = "Home"
        self.move_right =  False
        self.move_left =  False
        self.move_down =  False
        self.rotate = False
        self.rotate_limiter = True
    
    def set_game_over(self):
        self.game_status = "Game over"
    
    def set_home(self):
        self.game_status = "Home"
    
    def set_solo(self):
        self.game_status = "Solo"
    
    def set_ai(self):
        self.game_status = "AI"
    
    def is_home(self):
        return self.game_status == "Home"
        
    def is_game_over(self):
        return self.game_status == "Game over"
    
    def is_solo(self):
        return self.game_status == "Solo" 
    
    def is_ai(self):
        return self.game_status == "AI"
    
    # Reset only the control
    def reset_controls(self):
        self.move_right =  False
        self.move_left =  False
        self.move_down =  False
        self.rotate = False
    
    def reset(self):
        self.game_status = "Home"
        self.move_right =  False
        self.move_left =  False
        self.move_down =  False
        self.rotate = False