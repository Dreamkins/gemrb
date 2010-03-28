# -*-python-*-
# GemRB - Infinity Engine Emulator
# Copyright (C) 2003 The GemRB Project
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#

# GUILOAD.py - Load game window from GUILOAD winpack

###################################################

import GemRB
from LoadScreen import *
from GUICommonWindows import OpenWaitForDiscWindow

LoadWindow = 0
TextAreaControl = 0
GameCount = 0
ScrollBar = 0

def OnLoad ():
	global LoadWindow, TextAreaControl, GameCount, ScrollBar

	GemRB.LoadWindowPack ("GUILOAD")
	LoadWindow = GemRB.LoadWindowObject (0)
	CancelButton=LoadWindow.GetControl (46)
	CancelButton.SetText (4196)
	CancelButton.SetEvent (IE_GUI_BUTTON_ON_PRESS, "CancelPress")
	CancelButton.SetFlags (IE_GUI_BUTTON_CANCEL,OP_OR)

	GemRB.SetVar ("LoadIdx",0)

	for i in range (4):
		Button = LoadWindow.GetControl (14+i)
		Button.SetText (28648)
		Button.SetEvent (IE_GUI_BUTTON_ON_PRESS, "LoadGamePress")
		Button.SetState (IE_GUI_BUTTON_DISABLED)
		Button.SetVarAssoc ("LoadIdx",i)

		Button = LoadWindow.GetControl (18+i)
		Button.SetText (28640)
		Button.SetEvent (IE_GUI_BUTTON_ON_PRESS, "DeleteGamePress")
		Button.SetState (IE_GUI_BUTTON_DISABLED)
		Button.SetVarAssoc ("LoadIdx",i)

		#area previews
		Button = LoadWindow.GetControl (1+i)
		Button.SetState (IE_GUI_BUTTON_LOCKED)
		Button.SetFlags (IE_GUI_BUTTON_NO_IMAGE|IE_GUI_BUTTON_PICTURE,OP_SET)

		#PC portraits
		for j in range (PARTY_SIZE):
			Button = LoadWindow.GetControl (22+i*PARTY_SIZE+j)
			Button.SetState (IE_GUI_BUTTON_LOCKED)
			Button.SetFlags (IE_GUI_BUTTON_NO_IMAGE|IE_GUI_BUTTON_PICTURE,OP_SET)

	ScrollBar=LoadWindow.GetControl (13)
	ScrollBar.SetEvent (IE_GUI_SCROLLBAR_ON_CHANGE, "ScrollBarPress")
	GameCount=GemRB.GetSaveGameCount () #count of games in save folder?
	if GameCount>3:
		TopIndex = GameCount-4
	else:
		TopIndex = 0
	GemRB.SetVar ("TopIndex",TopIndex)
	ScrollBar.SetVarAssoc ("TopIndex", TopIndex+1)
	ScrollBarPress ()
	LoadWindow.SetVisible (WINDOW_VISIBLE)
	return

def ScrollBarPress ():
	#draw load game portraits
	Pos = GemRB.GetVar ("TopIndex")
	for i in range (4):
		ActPos = Pos + i

		Button1 = LoadWindow.GetControl (14+i)
		Button2 = LoadWindow.GetControl (18+i)
		if ActPos<GameCount:
			Button1.SetState (IE_GUI_BUTTON_ENABLED)
			Button2.SetState (IE_GUI_BUTTON_ENABLED)
		else:
			Button1.SetState (IE_GUI_BUTTON_DISABLED)
			Button2.SetState (IE_GUI_BUTTON_DISABLED)

		if ActPos<GameCount:
			Slotname = GemRB.GetSaveGameAttrib (0,ActPos)
		else:
			Slotname = ""
		Label = LoadWindow.GetControl (0x10000004+i)
		Label.SetText (Slotname)

		if ActPos<GameCount:
			Slotname = GemRB.GetSaveGameAttrib (3,ActPos)
		else:
			Slotname = ""
		Label = LoadWindow.GetControl (0x10000008+i)
		Label.SetText (Slotname)

		Button=LoadWindow.GetControl (1+i)
		if ActPos<GameCount:
			Button.SetSaveGamePreview (ActPos)
		else:
			Button.SetPicture ("")
		for j in range (PARTY_SIZE):
			Button=LoadWindow.GetControl (22+i*PARTY_SIZE+j)
			if ActPos<GameCount:
				Button.SetSaveGamePortrait (ActPos,j)
			else:
				Button.SetPicture ("")
	return

def LoadGamePress ():
	if LoadWindow:
		LoadWindow.Unload ()
	Pos = GemRB.GetVar ("TopIndex")+GemRB.GetVar ("LoadIdx")
	StartLoadScreen ()
	GemRB.LoadGame (Pos) # load & start game
	GemRB.EnterGame ()
	return

def DeleteGameConfirm ():
	global GameCount

	TopIndex = GemRB.GetVar ("TopIndex")
	Pos = TopIndex +GemRB.GetVar ("LoadIdx")
	GemRB.DeleteSaveGame (Pos)
	if TopIndex>0:
		GemRB.SetVar ("TopIndex",TopIndex-1)
	GameCount=GemRB.GetSaveGameCount ()
	ScrollBar.SetVarAssoc ("TopIndex", GameCount)
	ScrollBarPress ()
	if ConfirmWindow:
		ConfirmWindow.Unload ()
	LoadWindow.SetVisible (WINDOW_VISIBLE)
	return

def DeleteGameCancel ():
	if ConfirmWindow:
		ConfirmWindow.Unload ()
	LoadWindow.SetVisible (WINDOW_VISIBLE)
	return

def DeleteGamePress ():
	global ConfirmWindow

	LoadWindow.SetVisible (WINDOW_INVISIBLE)
	ConfirmWindow=GemRB.LoadWindowObject (1)

	Text=ConfirmWindow.GetControl (0)
	Text.SetText (28639)

	DeleteButton=ConfirmWindow.GetControl (1)
	DeleteButton.SetText (28640)
	DeleteButton.SetEvent (IE_GUI_BUTTON_ON_PRESS, "DeleteGameConfirm")
	DeleteButton.SetFlags (IE_GUI_BUTTON_DEFAULT,OP_OR)

	CancelButton=ConfirmWindow.GetControl (2)
	CancelButton.SetText (4196)
	CancelButton.SetEvent (IE_GUI_BUTTON_ON_PRESS, "DeleteGameCancel")
	CancelButton.SetFlags (IE_GUI_BUTTON_CANCEL,OP_OR)
	ConfirmWindow.SetVisible (WINDOW_VISIBLE)
	return
	
def CancelPress ():
	if LoadWindow:
		LoadWindow.Unload ()
	GemRB.SetNextScript ("Start")
	return
