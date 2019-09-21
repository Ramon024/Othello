class Point:
    def __init__(self,pixel_x: float, pixel_y: float, width: float, height: float, row:int, column:int):

        self._frac_x = pixel_x
        self._frac_y = pixel_y
        self.width = width
        self.height = height
        self.row = row
        self.column = column
        
    def check_column(self):
        change_x = self.width / self.column
        count = 0
        for x in range(self.column): 
            if ((change_x + count) >= self._frac_x and self._frac_x >= count): 
                return x
            count += change_x 
           
    def check_row(self):
        change_y = self.height / self.row
        count = 0
        for y in range(self.row): 
            if ((change_y + count) >= self._frac_y and self._frac_y >= count): 
                return y
            count += change_y
            