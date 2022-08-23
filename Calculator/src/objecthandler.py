class ObjectHandler():
    def __init__(self, GUI_):
        self.GUI = GUI_
        self.objects = []
        self.buttons = []
        self.line = ''

    def display_objects(self):
        for obj in self.objects:
            obj.display_visuals()

    def update(self, mouse_pos_, left_click_status_):
        self.update_buttons(mouse_pos_, left_click_status_)


    def update_buttons(self, mouse_pos_, left_click_status_):
        for obj in self.buttons:
            obj.mouse_collision(mouse_pos_, left_click_status_)

    '''methods triggered by buttons'''
    def change_GUI_state(self, temp):
        pass

    def quit(self, temp):
        pg.quit()
        sys.exit()

    def counter(self, temp):
        self.bio['counter'] += 1

    def write(self, temp):
        self.handler.line += str(temp)

    def erase(self, temp):
        if temp == 'all':
            self.handler.line = ''
        else:
            self.handler.line = self.handler.line[:-1]

    def eval(self, temp):
        try:
            result = eval(self.handler.line)
            if len(str(result)) > 10:
                    self.handler.line = '{:.4e}'.format(result)
            else:
                self.handler.line = str(result)
        except:
            self.handler.line = 'err'
