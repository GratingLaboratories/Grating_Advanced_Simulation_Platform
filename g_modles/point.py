"""
==============================================
   __  __   __   _     .   ___            __
  / / / /  /  _ |_)   /_\   |   |  |\ |  /  _
 / / / /   \__| | \  /   \  |   |  | \|  \__|
/_/ /_/    L  A  B  O  R  A  T  O  R  I  E  S
==============================================

..............................................
"""
class Point:
    def __init__(self, pos, p_type, r_index, color=0xffaa00):
        if p_type.lower() != 'fake' and p_type.lower() != 'real':
            raise ValueError
        self.pos = pos
        self.p_type = p_type
        self.r_index = r_index
        self.passed = []
        self.color = color

    def __str__(self):
        return repr(self.pos)

    def __repr__(self):
        return repr(self.pos)

    def __hash__(self):
        temp_str = str(self.pos) + str(self.p_type) + str(self.r_index) + str(self.passed)
        return hash(temp_str)
