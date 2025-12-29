/* GemRB - Infinity Engine Emulator
 * Copyright (C) 2003-2025 The GemRB Project
 *
 * This program is free software; you can redistribute it and/or
 * modify it under the terms of the GNU General Public License
 * as published by the Free Software Foundation; either version 2
 * of the License, or (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
 * GNU General Public License for more details.
 */

#include "TurnBasedCombatManager.h"
#include "Scriptable/Actor.h"
#include "Game.h"
#include "Interface.h"
#include "DisplayMessage.h"

#include <algorithm>

namespace GemRB {

// =============================================================================
// Slot Access Methods
// =============================================================================

InitiativeSlot& TurnBasedCombatManager::GetCurrentTurnBasedSlot()
{
	static InitiativeSlot emptySlot;
	
	// Validate list index
	if (currentTurnBasedList < 0 || currentTurnBasedList >= MAX_ATTACK_LISTS) {
		return emptySlot;
	}
	
	// Validate list not empty
	if (initiatives[currentTurnBasedList].empty()) {
		return emptySlot;
	}
	
	// Clamp slot index
	size_t slot = static_cast<size_t>(currentTurnBasedSlot);
	if (slot >= initiatives[currentTurnBasedList].size()) {
		slot = initiatives[currentTurnBasedList].size() - 1;
	}
	
	return initiatives[currentTurnBasedList][slot];
}

InitiativeSlot& TurnBasedCombatManager::GetTurnBasedSlot(Actor* actor)
{
	static InitiativeSlot emptySlot;
	
	// Search all lists for the actor
	for (int list = 0; list < MAX_ATTACK_LISTS; list++) {
		for (auto& slot : initiatives[list]) {
			if (slot.actor == actor) {
				return slot;
			}
		}
	}
	
	return emptySlot;
}

InitiativeSlot* TurnBasedCombatManager::GetTurnBasedSlotWithAttack(Actor* actor)
{
	// Find first slot for actor that still has an action available
	for (int list = 0; list < MAX_ATTACK_LISTS; list++) {
		for (auto& slot : initiatives[list]) {
			if (slot.actor == actor && slot.haveaction) {
				return &slot;
			}
		}
	}
	return nullptr;
}

// =============================================================================
// Turn Management
// =============================================================================

void TurnBasedCombatManager::InitTurnBasedSlot()
{
	// Delegate to Interface until full migration
	core->InitTurnBasedSlot();
}

void TurnBasedCombatManager::FirstRoundStart()
{
	// Delegate to Interface until full migration
	core->FirstRoundStart();
}

void TurnBasedCombatManager::EndTurn()
{
	// Delegate to Interface until full migration
	core->EndTurn();
}

void TurnBasedCombatManager::UpdateTurnBased()
{
	// Delegate to Interface until full migration
	core->UpdateTurnBased();
}

void TurnBasedCombatManager::resetTurnBased()
{
	// Clear all initiative lists
	for (int i = 0; i < MAX_ATTACK_LISTS; i++) {
		initiatives[i].clear();
	}
	
	// Reset state variables
	currentTurnBasedSlot = 0;
	currentTurnBasedSlotOld = 0;
	currentTurnBasedList = 0;
	currentTurnBasedListOld = 0;
	currentTurnBasedActor = nullptr;
	currentTurnBasedActorOld = nullptr;
	opportunity = 0;
	opportunists.clear();
	roundTurnBased = 0;
	timeTurnBased = 0;
	timeTurnBasedNeed = 0;
}

bool TurnBasedCombatManager::UseFreeAction()
{
	if (!IsTurnBased() || !currentTurnBasedActor) {
		return true; // Not in TBC, allow action
	}
	InitiativeSlot& slot = GetCurrentTurnBasedSlot();
	if (slot.havefreeaction) {
		slot.havefreeaction = false;
		return true;
	}
	return false; // No free action available
}

void TurnBasedCombatManager::ToggleTurnBased()
{
	turnBasedEnable = !turnBasedEnable;
	
	String text;
	if (turnBasedEnable) {
		text = fmt::format(u"Turn based mode enabled.");
	} else {
		text = fmt::format(u"Turn based mode disabled.");
	}
	displaymsg->DisplayString(std::move(text), GUIColors::GOLD, 0);
}

} // namespace GemRB
