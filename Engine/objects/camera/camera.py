import Engine


class Camera:
    def __init__(self, pos=0, speed: float = 1):
        self.pos: Engine.math.vec3 = Engine.math.vec3(pos) + Engine.math.vec3(
            *(Engine.graphic.Graphics.window.get_size() // 2), 0)
        self.vel: Engine.math.vec3 = Engine.math.vec3(0)
        self.speed: float = speed

    def __event__(self, _):
        self.vel = Engine.math.vec3(0)

        key_ues = False
        if Engine.app.App.key_list[Engine.pg.K_w]:
            self.vel.y -= 1
            key_ues = True
        if Engine.app.App.key_list[Engine.pg.K_s]:
            self.vel.y += 1
            key_ues = True
        if Engine.app.App.key_list[Engine.pg.K_a]:
            self.vel.x -= 1
            key_ues = True
        if Engine.app.App.key_list[Engine.pg.K_d]:
            self.vel.x += 1
            key_ues = True

        n_vec = Engine.math.normalize(self.vel)
        self.vel = Engine.math.vec3(0) if Engine.math.isnan(n_vec)[0] else n_vec

        if not key_ues:
            for key, joystick in Engine.app.App.joysticks.items():
                self.vel.x += joystick.get_axis(0)
                self.vel.y += joystick.get_axis(1)

    def __update__(self):
        self.pos += self.vel * self.speed * Engine.app.App.clock.delta
