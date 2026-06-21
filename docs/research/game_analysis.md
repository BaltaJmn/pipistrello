# Game Analysis: Pipistrello and the Cursed Yoyo

> Fill this document as you investigate the game with dnSpy, Unity Explorer and BepInEx.
> Every PLACEHOLDER_ in shared/data/ should be replaced with real values found here.

## Build Info

- Unity version: _TODO_
- .NET version: _TODO_
- Assembly: `Pipistrello_Data/Managed/Assembly-CSharp.dll`

---

## Key Classes

### GameManager
- Namespace: _TODO_
- Singleton pattern: `GameManager.Instance`
- Relevant methods:
  - `GiveItem(?)` — _TODO: exact signature_
  - `HasItem(?)` — _TODO_

### SaveManager / SaveData
- Class name: _TODO_
- Serialization method: _TODO_ (JSON / BinaryFormatter / PlayerPrefs / other)
- Save file location: _TODO_
- Relevant methods:
  - Set flag: _TODO_
  - Get flag: _TODO_

### ItemManager / InventorySystem
- Class name: _TODO_
- How items are stored: _TODO_
- Internal item identifier type: string / int / enum → _TODO_

### ChestController (or equivalent)
- Class name: _TODO_
- Interaction method: _TODO_
- Hook point (method + approx line): _TODO_
- Event/delegate fired on open: _TODO_

### BossController (or equivalent)
- Class name: _TODO_
- Defeat method/event: _TODO_
- Hook point: _TODO_

---

## Item System

### How items are identified internally
_TODO: string name / int ID / ScriptableObject / other_

### Example: giving the yoyo to the player
```csharp
// TODO: paste real code here
```

### Example: checking if player has an item
```csharp
// TODO: paste real code here
```

---

## Save / Flag System

### How progression flags are stored
_TODO_

### Example: reading a flag
```csharp
// TODO
```

### Example: setting a flag
```csharp
// TODO
```

---

## Identified Locations

> Replace PLACEHOLDER_ values in shared/data/locations.json with these.

| AP Name | Scene | Object Path | Flag Key |
|---------|-------|-------------|----------|
| Starting Area - Tutorial Chest | _TODO_ | _TODO_ | _TODO_ |
| Cursed Forest - Chest 1 | _TODO_ | _TODO_ | _TODO_ |
| Cursed Forest - Boss Reward | _TODO_ | _TODO_ | _TODO_ |

---

## Identified Items

> Replace PLACEHOLDER_ values in shared/data/items.json with these.

| AP Name | mod_internal_name | How to give |
|---------|-------------------|-------------|
| Yoyo | _TODO_ | _TODO_ |
| Double Jump | _TODO_ | _TODO_ |
| Dash | _TODO_ | _TODO_ |

---

## Scene List

| Scene Name | Purpose |
|------------|---------|
| _TODO_ | Starting area |
| _TODO_ | Town hub |
| _TODO_ | Cursed Forest |

---

## Notes & Observations

_Add anything relevant found during investigation here._
