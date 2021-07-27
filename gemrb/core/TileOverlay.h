/* GemRB - Infinity Engine Emulator
 * Copyright (C) 2003 The GemRB Project
 *
 * This program is free software; you can redistribute it and/or
 * modify it under the terms of the GNU General Public License
 * as published by the Free Software Foundation; either version 2
 * of the License, or (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program; if not, write to the Free Software
 * Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
 *
 *
 */

#ifndef TILEOVERLAY_H
#define TILEOVERLAY_H

#include "exports.h"

#include "Holder.h"
#include "Tile.h"
#include "Video/Video.h"

#include <vector>

namespace GemRB {

class GEM_EXPORT TileOverlay : public Held<TileOverlay> {
public:
	Size size;
	std::vector<Tile> tiles;
public:
	using TileOverlayPtr = Holder<TileOverlay>;

	TileOverlay(Size size);

	void AddTile(Tile tile);
	void Draw(const Region& viewport, std::vector<TileOverlayPtr> &overlays, BlitFlags flags) const;
};

}

#endif
