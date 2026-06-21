# Game Analysis: Pipistrello and the Cursed Yoyo

## Build Info

- Engine: Unity (IL2CPP) — NO es Mono
- Ensamblado nativo: `GameAssembly.dll`
- Interop generado por Cpp2IL: `BepInEx/interop/Assembly-CSharp.dll`
- Namespace principal: `Pipistrello`

---

## Clases clave

### `Pipistrello.Game`

Clase de estado global del juego. Métodos relevantes:

```csharp
// Establece un flag de progresión
Game.SetFlag(Il2CppSystem.Collections.Generic.Dictionary<string,int> flags, string flagName, ...)

// Estado de equips
Game.SetEquipAcquired(Game.Equip equip, bool acquired, bool notify) → bool
Game.SetUpgradeAcquired(Game.Upgrade upgrade, bool acquired) → bool
Game.SetPetalContainerAcquired(string id, int petalNum, bool acquired) → bool
Game.SetBpContainerAcquired(string id, ...) → bool
```

> El primer parámetro de `SetFlag` es `Il2CppSystem.Collections.Generic.Dictionary<string,int>`, no `string`. En Harmony se referencia como `__0` (Il2CppDict) y `__1` (string flagName).

### `Pipistrello.Scripting.ExternalFunctions`

Scripting del juego. Método relevante:

```csharp
ExternalFunctions.BossEnd()  // Se llama al terminar un boss fight
```

---

## Sistema de flags

Toda la progresión del juego se gestiona mediante `Game.SetFlag`. Al morir/respawnear, el juego replaya **todos** los flags persistentes para restaurar el estado — esto significa que el mismo flag puede aparecer múltiples veces en el log. El mod debe deduplicar.

### Vocabulario completo de flags

#### Equips (items de equipamiento)
```
g:equip:<nombre>:acquired    → primera vez que se recoge (AP: location check)
g:equip:<nombre>:equipped    → equipado en un slot (ignorar)
g:equip:<nombre>:refined     → refinado/mejorado (ignorar)
```
Ejemplos vistos: `seeEnemyLife`, `projectileReflect`

#### Upgrades
```
g:upgrade:<nombre>:acquired  → recogido (AP: location check)
```
Ejemplos vistos: `bpUp`

#### Petal containers (ampliaciones de vida)
```
g:petalContainer:<ruta>:acquired  → recogido (AP: location check)
```
La `<ruta>` incluye el path de sala, ej: `city_interiors/ren24/ren66`

#### Key items (baterías)
```
g:tunnels:gotBattery1
g:tunnels:gotBattery2
```

#### Habilidades del jugador
```
g:ability:<nombre>   → concede la habilidad al jugador (AP: estos son los AP items)
```

Lista completa descubierta (sala `policedep/lor124` — tutorial de habilidades):

| Flag | Tipo |
|---|---|
| `g:ability:menu` | base (siempre activa) |
| `g:ability:move` | base |
| `g:ability:receiveDamage` | base |
| `g:ability:jump` | base |
| `g:ability:attack` | base |
| `g:ability:throw` | movimiento/combate |
| `g:ability:wallDash` | movimiento |
| `g:ability:walkTheDog` | movimiento |
| `g:ability:wallRailing` | movimiento |
| `g:ability:helix` | movimiento |
| `g:ability:chargedAction` | slot cargado |
| `g:ability:chargedSleeper` | charged move |
| `g:ability:chargedFlurry` | charged move |
| `g:ability:chargedSpread` | charged move |
| `g:ability:chargedSpin` | charged move |
| `g:ability:specialAction` | slot especial |
| `g:ability:specialParry` | special move |
| `g:ability:specialSpin` | special move |
| `g:ability:specialCoinFlip` | special move |

Las habilidades `menu`, `move`, `receiveDamage`, `jump`, `attack` parecen ser base y se conceden desde el inicio. Las demás son progresión.

#### Área/boss completado
```
g:<area>Complete     → AP: location check de boss/área
```
Ejemplos: `g:policedepComplete`, `g:prologue`

#### Slots equipados (loadout actual)
```
g:equipped:chargedAction   → qué está en el slot de cargado
g:equipped:specialAction   → qué está en el slot especial
```

#### Progresión de área
```
g:<area>Reached     → llegada a área (ej. g:policedepReached)
g:<area>Sighted     → área vista
```

#### Flags de sala y navegación (ignorar)
```
g:visited:<sala>         → sala visitada
g:passed:<desde>/<hasta> → transición completada
```

#### Estadísticas (ignorar)
```
g:stat:*
```

#### Flags temporales (ignorar siempre)
```
t:battle    → en combate activo
t:sighted   → enemigo a la vista
```

---

## Áreas conocidas

| Área | Flag de completion | Notas |
|---|---|---|
| Policía (police dep) | `g:policedepComplete` | Primer dungeon. Flag de boss tras limpiar la sala de waves. |
| Prólogo | `g:prologue` | Tutorial inicial |

Salas identificadas:
- `policedep/lor124` — sala de tutorial de habilidades (se activan todas en esta sala)
- `policedep/lor288` — sala de premio del boss (`g:policedep/lor288:prize`)
- `city_interiors/ren24/ren66` — sala con petal container
- `city_interiors/ren925/yug711` — sala con petal container

---

## Items por recoger (locations)

Método de detección: hookear `Game.SetFlag` y filtrar por patrón.

Los métodos `Set*Acquired` (`SetEquipAcquired`, `SetUpgradeAcquired`, etc.) **no parecen dispararse** al recoger items — el juego parece ir directamente a `SetFlag`. El hook de `SetFlag` con filtro por patrón es el método fiable.

---

## Items por dar (recibidos desde AP)

Para dar una habilidad al jugador desde el mod: llamar `Game.SetFlag` con el flag correspondiente `g:ability:<nombre>`.

Para dar un equip: explorar si `SetEquipAcquired(equip, acquired: true, notify: true)` es el camino correcto, o si basta con `SetFlag("g:equip:<nombre>:acquired")`.

---

## Notas de reverse engineering

- El juego usa IL2CPP — no se puede usar dnSpy directamente sobre `GameAssembly.dll`. Opciones: Cpp2IL, Il2CppDumper, o inspeccionar los ensamblados de interop generados por BepInEx en `BepInEx/interop/`.
- Los interop assemblies en `BepInEx/interop/` son los que se referencian en el `.csproj` del mod y los que se pueden abrir con ILSpy/dnSpy para explorar la API.
