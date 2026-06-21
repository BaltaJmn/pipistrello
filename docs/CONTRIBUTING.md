# Contributing

## Flujo de trabajo

1. Clona el repo y crea una rama (`git checkout -b feat/mi-cambio`)
2. Haz tus cambios
3. Asegúrate de que el CI pasa (`validate.py` + tests del APWorld)
4. Abre una PR contra `main`

## Reglas del repo

- **`shared/data/` es la fuente de verdad.** Items, locations y regions se definen ahí. El APWorld, el mod y el tracker los leen desde ahí. No edites esas listas en más de un sitio.
- **No hay PLACEHOLDERs nuevos.** Si añades un item o location, pon el valor real (flag del juego, ID, etc.). Mira `docs/research/game_analysis.md` para los nombres reales.
- **El mod no debe pushear al repo.** `mod/PipistrelloAP/bin/` y `obj/` están en `.gitignore`.

## Áreas de trabajo

### BepInEx mod (`mod/PipistrelloAP/`)

- Lenguaje: C# .NET 6
- Ver sección "Setup: BepInEx mod" en el README para compilar y probar
- El juego usa IL2CPP — los tipos del juego vienen del interop generado por BepInEx en `BepInEx/interop/`
- Patchear con HarmonyX: `[HarmonyPatch(typeof(ClassName), nameof(MethodName))]`

### APWorld (`world/pipistrello/`)

- Lenguaje: Python 3.11
- Seguir la estructura estándar de Archipelago (`AutoWorld`, `Item`, `Location`, `Region`)
- Tests en `world/tests/` — deben pasar antes de hacer merge

### PopTracker (`tracker/`)

- Lua + JSON
- Documentación PopTracker: https://github.com/black-sliver/PopTracker/blob/master/doc/PACKS.md

### Datos compartidos (`shared/data/`)

- Editar `items.json`, `locations.json`, `regions.json`
- Validar con `python shared/scripts/validate.py`
- Los JSON schemas están en `shared/schemas/`

## IDs

| Rango | Uso |
|---|---|
| `7370000 – 7370999` | Items |
| `7371000 – 7372999` | Locations |

Al añadir items o locations nuevas, usar el siguiente ID disponible en cada rango. No reutilizar IDs eliminados.
