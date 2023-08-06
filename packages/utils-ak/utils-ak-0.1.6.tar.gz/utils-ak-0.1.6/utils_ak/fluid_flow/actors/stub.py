from utils_ak.fluid_flow.actor import Actor


class Stub(Actor):
    def __init__(self, name=None):
        super().__init__(name)

    def update_pressure(self, ts):
        for pipe in self.parents:
            pipe.pressures['in'] = 0
        for pipe in self.children:
            pipe.pressures['out'] = 0

    def __str__(self):
        return f'Stub {self.name}'