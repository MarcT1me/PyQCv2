import Engine


class SceneRoster(Engine.arrays.SimpleRoster):
    D2: dict[str, 'Engine.objects.Object']
    D3: dict[str, 'Engine.objects.Object']
    UI: dict[str, 'Engine.objects.Object']


class Scene:
    roster = SceneRoster()
