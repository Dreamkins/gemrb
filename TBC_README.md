# Turn-Based Combat Mod for GemRB

Turn-Based Combat (TBC) is a mod for the GemRB engine that adds a full turn-based combat mode to classic Infinity Engine games: Baldur's Gate, Icewind Dale, and Planescape: Torment. The system is inspired by D&D 5e while preserving the original AD&D 2e mechanics.

---

## Controls

| Key | Action |
|-----|--------|
| `Enter` | Toggle turn-based mode (enabled by default). If something goes wrong, you can continue the battle in real-time with active pause |
| `Space` | End current character's turn |
| `Mouse wheel` | Scroll the initiative panel |

---

## Initiative Panel

A horizontal panel at the top of the screen displays portraits of all combat participants. First to act is on the left.

**Slot Elements:**
- **Character portrait** — clickable for selection
- **Movement bar** (below portrait) — shows remaining movement distance
- **Green square** — main action available
- **Yellow square** — free action available
- **Line** — connects attacker and target during opportunity attack (when active)

Characters with multiple attacks per round appear multiple times in the list — each appearance corresponds to one attack phase. Phases are separated by a vertical line.

---

## Initiative

At the start of each round, turn order is determined:

```
Initiative = Weapon Speed + d10 - Dexterity bonus + Size modifier
```

The **lower** the result, the **earlier** the character acts.

| Factor | Modifier |
|--------|----------|
| Weapon Speed | +Speed |
| Dice roll | +1d10 |
| Dexterity bonus | -reaction bonus |
| Haste | -2 |
| Slow | +2 |
| Size Tiny | -2 |
| Size Small | -1 |
| Size Medium | 0 |
| Size Large | +1 |
| Size Huge | +2 |

---

## Action System

### Main Action (green square)

One per attack phase. Used for:

| Action | Note |
|--------|------|
| Weapon attack | One attack per phase |
| Cast spell | Cancels all subsequent attack phases |
| Use scroll | Treated as spell |
| Item from inventory | Any item used outside quick slots |
| Disarm Trap | Thief skill |
| Pick Lock | Thief skill |
| Pick Pocket | Thief skill |
| Turn Undead | Cleric/Paladin ability |
| Stealth (non-thief) | For characters without thief levels |

### Free Action (yellow square)

One per entire turn (all attack phases). If unused — carries over to the next phase.

| Action | Note |
|--------|------|
| Potion/item from quick slot | Except scrolls |
| Switch active weapon | Toggle between weapon sets |
| Stealth (thief) | For characters with thief levels |
| Exit stealth | Deactivate Stealth mode |

### Movement

- Each character can move a distance based on their speed
- Movement bar below portrait shows remaining allowance
- Movement does not cost actions — you can move and attack in any order

---

## Attack Phases

Characters with multiple attacks per round receive additional phases:

- **Phase 0** — main phase, available to all
- **Phases 1-5** — additional attacks

**Notes:**
- Each phase grants one main action
- Free action — one for all phases, carries over if unused
- Long-casting spells can only be cast in **Phase 0** and they **cancel all subsequent phases**

---

## Opportunity Attacks

When a character **leaves the reach** of an enemy with a melee weapon:

1. Movement is interrupted
2. All enemies within striking range get a chance to attack
3. A line appears on the panel connecting attacker and target
4. Enemies attack in sequence
5. After opportunity attacks complete, turn returns to the original character

**Trigger conditions:**
- Enemy has a melee weapon
- Enemy has an unused attack
- Enemy can see the target
- Enemy is able to attack (not stunned, asleep, etc.)

---

## Modal Abilities

| Ability | Activation | Deactivation |
|---------|------------|--------------|
| Stealth (thief) | Yellow action | Yellow action |
| Stealth (others) | Green action | Yellow action |
| Detect Traps | Green action | Yellow action |
| Bard Song | Green action | Yellow action |
| Turn Undead | Green action | Yellow action |
