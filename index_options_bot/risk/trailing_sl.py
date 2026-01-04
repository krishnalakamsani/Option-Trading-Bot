class TrailingSL:
    def __init__(self, trail_points):
        self.trail_points = trail_points

    def update_sl(self, ltp, current_sl):
        new_sl = ltp - self.trail_points
        return max(current_sl, new_sl)
