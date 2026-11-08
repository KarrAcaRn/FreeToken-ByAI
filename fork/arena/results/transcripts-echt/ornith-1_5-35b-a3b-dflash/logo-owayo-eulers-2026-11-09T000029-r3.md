# ornith-1_5-35b-a3b-dflash - logo-owayo-eulers (2026-11-09T00:00:29)

## Antwort (45789 Tokens, 251.406 s, Ende: stop, Denken abgebrochen)

### Denkphase

The user wants a logo for an ice hockey team called "Owayo Eulers". The logo should contain an owl and an ice hockey stick. The background should be solid/single-colored, or preferably no background at all.

Let me create an SVG document for this. I'll design an owl holding or near an ice hockey stick, with the team name "Owayo Eulers".

Let me think about the design:
- An owl (Eule) - with big eyes, feathers, etc.
- An ice hockey stick (Eishockeyschläger)
- Text "Owayo Eulers"
- No background (transparent)

Let me create a nice SVG logo. I'll use a color scheme that fits an ice hockey team - maybe blues, oranges, whites.

Let me design this carefully with paths.

I'll create an owl with:
- Round body
- Big eyes
- Ears/tufts (owls have ear tufts)
- Beak
- Wings
- Feathers on belly

And an ice hockey stick crossing behind or beside the owl.

Let me write the SVG code.

I'll make it a clean, modern logo design. Let me think about colors - a dark blue/navy background circle would work well for ice hockey, with orange or gold accents.

Let me create this:

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 500 500" width="500" height="500">
  <!-- definitions -->
  <defs>
    <linearGradient id="bodyGrad" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#4A5DA0"/>
      <stop offset="100%" stop-color="#2C3E6B"/>
    </linearGradient>
  </defs>
  
  <!-- Outer circle -->
  ...
</svg>
```

Let me build this out fully. I'll create a circular badge-style logo.

Let me be detailed and create a nice owl. I'll use paths for the owl body, eyes, beak, wings, ear tufts. And a hockey stick.

Here's my plan:
- Circular badge with dark navy background
- Owl in center
- Hockey stick behind the owl (angled)
- Text "OWAYO" at top and "EURLERS" at bottom, or "Owayo Eulers" below

Let me write it.

For the owl:
- Body: an ellipse/rounded shape
- Head: circle
- Eye circles: white with dark pupils
- Beak: triangle/orange
- Ear tufts: triangles
- Wings: shapes on sides
- Belly: lighter feathers

For the hockey stick:
- A long handle (rectangle rotated)
- A blade at the bottom (curved shape)

Let me create this properly.

I'll make the owl sitting, with the hockey stick behind it.

Let me write the full SVG:

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 500 560" width="500" height="560">
  <defs>
    <linearGradient id="bodyGrad" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#5568A8"/>
      <stop offset="1" stop-color="#2E4070"/>
    </linearGradient>
    <radialGradient id="eyeGrad" cx="0.4" cy="0.4" r="0.6">
      <stop offset="0" stop-color="#FFE066"/>
      <stop offset="1" stop-color="#F4A100"/>
    </radialGradient>
  </defs>
  
  <!-- Badge circle -->
  <circle cx="250" cy="250" r="220" fill="#1B2651"/>
  <circle cx="250" cy="250" r="210" fill="none" stroke="#F4A100" stroke-width="4"/>
  
  <!-- Hockey stick -->
  ...
  
  <!-- Owl -->
  ...
  
  <!-- Text -->
  ...
</svg>
```

Let me flesh out the owl and hockey stick in detail.

Hockey stick - I'll draw it as a group rotated. The stick goes from top-left to bottom-right or something. Let me make it behind the owl.

Actually, let me make the hockey stick vertical-ish, behind the owl, with the blade at the bottom.

Let me just write it all out now.

For the owl body, I'll use an ellipse. For eyes, big circles. Let me place the owl in the center.

Let me create the design step by step.

Owl eyes (big round owl eyes):
- Left eye: circle at (205, 220), radius 45, white fill
- Right eye: circle at (295, 220), radius 45, white fill
- Pupils: dark circles
- Yellow ring around eyes

Beak: orange triangle pointing down between eyes at (250, 260)

Body: ellipse centered around (250, 340)

Head/ears: ear tufts at top

Wings: on sides

Belly: lighter area with feather lines

Let me write it all.

I'll make the owl look good. Let me finalize.

Let me write the complete SVG now with careful coordinates.

Actually for a cleaner look, let me make the owl more stylized/geometric.

Here's my final design:

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 500 560" width="500" height="560">
  <defs>
    <linearGradient id="bodyGrad" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#5A6FB0"/>
      <stop offset="1" stop-color="#2E4070"/>
    </linearGradient>
    <radialGradient id="eyeGrad" cx="0.4" cy="0.35" r="0.7">
      <stop offset="0" stop-color="#FFE066"/>
      <stop offset="1" stop-color="#F09000"/>
    </radialGradient>
  </defs>

  <!-- Badge -->
  <circle cx="250" cy="250" r="225" fill="#17224A"/>
  <circle cx="250" cy="250" r="213" fill="none" stroke="#F7B400" stroke-width="5"/>

  <!-- Hockey stick -->
  <g transform="rotate(18 250 250)">
    <rect x="240" y="70" width="16" height="330" rx="8" fill="#C9822E"/>
    ...blade
  </g>
  ...
</svg>
```

Hmm, the hockey stick blade is tricky. Let me draw it as a path.

Let me make the hockey stick behind the owl. I'll create the stick handle as a long thin rounded rectangle, and the blade as a curved shape at the bottom.

Let me place the stick diagonally behind the owl.

Actually, let me keep it simpler and cleaner. Let me draw:

Hockey stick (behind owl):
- Handle: long thin shape
- Blade: at the bottom, the characteristic hockey stick blade shape

Let me define the hockey stick in its own coordinate and rotate it.

I'll write the blade as a path. A hockey stick blade looks like an L or hook shape - the blade is flat and curves up at the front.

Let me create the blade path relative to a stick going straight down:
- Handle ends at some point
- Blade extends forward and curves

For a vertical stick with handle at top and blade at bottom:
- Handle: from (248, 80) to (252, 380) approximately
- Blade: at bottom, extends to the right and has the curved toe

Let me define blade path:
Starting at handle bottom around (250, 380), the blade goes:
- down to (255, 400)
- then out to the right along the bottom: (255, 400) to (310, 400)
- curve up at toe: to (315, 385)
- back up: to (290, 380)
- back to handle: (260, 380)

Something like that. Let me refine.

Actually, let me just make a nice hockey stick. I'll draw it as one path.

Let me reconsider the whole composition. I want:
1. A circular badge
2. A hockey stick behind the owl
3. An owl in the front
4. Text "Owayo Eulers"

Let me make the text curved along the top and bottom of the circle, or just place "OWAYO" at top and "EURLERS" at bottom. Actually the team name is "Owayo Eulers" - I could put it as one line at the bottom, or split. Let me put "OWAYO" on top arc and "EURLERS" on bottom arc for a badge look. Or simpler: put "Owayo Eulers" as text below the circle.

Let me do a badge style with text on arcs - that looks more like a sports logo. But curved text requires path-based text. Let me do that.

Actually, to keep it robust, let me use textPath for curved text.

Let me define a circular path for the text.

Top text path: a semicircle at the top
Bottom text path: a semicircle at the bottom (reversed)

Let me define:
- Top arc path: M 60 250 A 190 190 0 0 1 440 250 (this goes over the top)
- Bottom arc path: M 70 250 A 180 180 0 0 0 430 250 (this goes under the bottom)

Hmm, let me think about the arc directions.

For text along the top of a circle, going left to right over the top:
Path: M 60 250 A 190 190 0 0 1 440 250
This starts at left (60,250), arcs over the top to right (440,250). With large-arc-flag=0 and sweep-flag=1, it goes clockwise from left... let me think.

Actually, sweep-flag=1 means clockwise. Starting at (60,250) which is left side, going clockwise would go downward first. To go over the top (counterclockwise from left perspective), I need... hmm.

Let me think again. Point (60, 250) is to the left of center (250,250). Point (440, 250) is to the right. 

If I want text over the top (through y < 250, the upper area), the path should bulge upward.

Path M 60 250 A 190 190 0 0 1 440 250:
- Starting point (60,250), ending (440,250)
- radius 190
- large-arc-flag 0 (smaller arc)
- sweep-flag 1 (clockwise)

From (60,250) going clockwise with these params... Clockwise from the left point would go down and around. That's the bottom. So this bulges downward.

For bulging upward (top), I need sweep-flag 0:
Path M 60 250 A 190 190 0 0 0 440 250
This goes counterclockwise from left point, which bulges upward. 

Wait, let me reconsider. Counterclockwise from (60,250)... Starting at left, counterclockwise means going up first (toward top). Yes, that bulges upward through the top. Good.

Hmm, actually I need to double check. In SVG, y increases downward. Sweep-flag=1 is "positive angle direction" which in SVG's coordinate system (y-down) appears as clockwise on screen.

From point (60,250) [left of center], moving along a circle:
- Clockwise (sweep=1): from left, clockwise goes UP... no wait.

Let me think physically. A clock. 9 o'clock position is left (60,250). Moving clockwise from 9 o'clock: 9 → 10 → 11 → 12 (top). So clockwise from left goes UP to the top. 

So sweep-flag=1 (clockwise) from (60,250) goes over the top. 

So top text: M 60 250 A 190 190 0 0 1 440 250 ✓ (over the top)

For bottom text, I want it along the bottom, and it should be readable (not upside down). Text along a path reads in the direction of the path. For bottom text to read left-to-right normally, the path should go from right to left along the bottom... no.

Hmm, text along path: the text follows the path direction, with the baseline along the path. For bottom text that reads normally (left to right), I want the path to go from left to right along the bottom, but then the text would be upside down (because the path is below and text sits on top of the path going in path direction, but the path curves... ).

This is getting complicated. Let me simplify: for bottom text, I'll make the path go from right to left along the bottom, so that text reads left-to-right when placed on it. Wait no.

Let me just think about it differently. Standard approach:

Top text (reads left to right, over the top):
path: M 70 250 A 180 180 0 0 1 430 250
- sweep=1, clockwise, over the top ✓

Bottom text (reads left to right, under the bottom):
path: M 430 250 A 180 180 0 0 1 70 250
- Start at right (430,250), clockwise to left (70,250). Clockwise from 3 o'clock (right): 3 → 4 → 5 → 6 (bottom). So it goes over the bottom, from right to left. Text placed on this reads left-to-right? No, text follows path direction, so it would read from the start (right) to end (left), meaning it reads right-to-left along the bottom... which appears as reversed.

Hmm. Let me reconsider. When you use textPath, the text starts at the beginning of the path and flows toward the end. So if the path starts at right (430,250) and ends at left (70,250), the text reads from right to left, i.e., first letter at right. That's reversed for reading.

I want first letter at left. So path should start at left (70,250) and flow along the bottom to the right. But flowing from left to right along the bottom (through the bottom, 6 o'clock)... 

Path: M 70 250 A 180 180 0 0 0 430 250
- Start left (70,250), sweep=0 (counterclockwise). Counterclockwise from 9 o'clock (left): 9 → 8 → 7 → 6 (bottom). So it goes over the bottom, left to right. Text reads left to right ✓. But the text would be upside down because... no.

Wait, the issue is whether text is above or below the path. When text is placed on a path, it sits on the "top" side of the path (to the left of the direction of travel in standard orientation, but with y-down it's... ugh).

Let me just think about the bottom text being right-side up. For text at the bottom of a badge to be right-side up and readable, it typically reads left-to-right but the letters are... no, they're right side up, just positioned at the bottom.

Hmm, actually in most circular badges, the bottom text reads left-to-right and is right-side up. To achieve this with textPath, the path should be drawn such that text comes out right-side up.

Let me just try: for bottom text, draw the path from right to left along the bottom (so it's like the top path but flipped). 

Actually, you know what, let me just make the bottom text path go from right to left and it will appear right-side up. Let me reason:

If I draw path from (430,250) to (70,250) along the bottom (over 6 o'clock), with sweep such that it bulges down:
Path: M 430 250 A 180 180 0 0 1 70 250
- Start right (430,250), sweep=1 (clockwise). Clockwise from 3 o'clock (right): 3→4→5→6→7→8→9 (left), going through bottom. So it bulges down through the bottom. ✓
- Text flows from right (start) to left (end). So first char at right. That's reversed.

Ugh, still reversed.

OK here's the thing. Let me reconsider what "right side up" means for curved text.

In a circular logo, bottom text usually reads left-to-right and is right-side up (not mirrored, not upside down). To get this:

The text path for the bottom should go from left to right, but the text needs to be on the outside (below) the path. When text is on the outside of a bottom path going left-to-right, the text is right-side up.

Wait, I think I'm overcomplicating. Let me just recall the standard recipe:

Top arc: `<path id="top" d="M 60 250 A 190 190 0 0 1 440 250" />` — text reads L-to-R over the top.

Bottom arc: `<path id="bottom" d="M 60 250 A 190 190 0 0 0 440 250" />` — hmm.

Let me reconsider by actually thinking about the geometry.

Circle center (250,250), radius 190.

Top path over the top from left to right: starts (60,250), ends (440,250), passes through (250, 60). This is the upper semicircle. Direction: left to right.
- From (60,250) to (440,250) through (250,60).
- This is counterclockwise? Let's see: (60,250) is at angle 180° (pointing left). (250,60) is at angle 270°/−90° (pointing up in screen, but in standard math angle it's -90°). (440,250) is at angle 0° (pointing right).
- Going from 180° to 270°(up) to 360°/0°... in terms of screen, going from left, up, to right. In SVG angle convention (clockwise positive, y-down), angle increases clockwise. Left is 180°. Going up (to top) means... in y-down coordinates, top is -90° or 270°. 

I'm confusing myself. Let me just use the sweep flag rules directly.

SVG arc: A rx ry x-axis-rotation large-arc-flag sweep-flag x y
- sweep-flag = 1: positive-angle direction (clockwise in standard math, but in SVG with y-down it looks clockwise on screen)

Rule of thumb: sweep-flag=1 draws the arc in the clockwise direction as seen on screen.

Top arc, left to right, over the top:
On screen, going from left point, over the top, to right point. Is that clockwise or counterclockwise? From 9 o'clock (left), to 12 o'clock (top), to 3 o'clock (right). That's 9→12→3, which is clockwise! So sweep-flag=1.
Top: M 60 250 A 190 190 0 0 1 440 250 ✓ (matches what I said)

Bottom arc, for text to read left-to-right and be right-side up:
We want text along the bottom. The text should read left-to-right. For the letters to be right-side up (not upside down), the path direction at the bottom should be... 

When text flows along a path, each glyph is oriented so its top points to the left of the path direction (in screen coords, the "up" of the glyph is 90° counterclockwise from path direction... in y-down it's complicated).

Let me think about the bottom of the circle. If path goes from left (9 o'clock) to right (3 o'clock) along the bottom (through 6 o'clock): direction at 6 o'clock is... moving from 9→6→3, at 6 o'clock the direction is toward 3 o'clock, i.e., to the right (east). So at the bottom, moving rightward. Glyph "up" would be... perpendicular to direction. If moving east (right), glyph up is north (up) if we rotate the right way, or south (down) if the other way.

For text to be right-side up at the bottom (glyph up = screen up = north), we need the path direction at the bottom to be east (moving right). So path goes left-to-right along the bottom.

Path from (60,250) to (440,250) along the bottom (through 250,440):
On screen: from 9 o'clock, through 6 o'clock, to 3 o'clock. That's 9→6→3, counterclockwise! So sweep-flag=0.
Bottom: M 60 250 A 190 190 0 0 0 440 250

But wait, if the glyph "up" points north at the bottom of the circle, the text would be right-side up but positioned at the bottom. But actually, for a badge, bottom text is usually right-side up. Let me go with this.

Hmm, but actually there's a subtlety. Let me reconsider. When text is placed on a path, the baseline of the text sits ON the path, and the text extends upward (in glyph coordinates) from the baseline. The glyph "up" direction is determined by the path's normal.

For the bottom arc going left-to-right (through 6 o'clock), at 6 o'clock the path direction is east (rightward). The text baseline is tangent to the path (horizontal at 6 o'clock), and text extends... in the direction 90° from path direction. Which side? SVG places text to the left of the path direction (when walking along the path, text is on your left). Walking east (rightward), left is north (up). So text extends upward from the baseline. At the bottom of the circle, "upward" (north) is toward the center of the circle. So the text would be inside the circle, right-side up. 

Wait, that means the text sits just inside the bottom arc, right-side up. That's what we want for a badge!

Hold on, let me double check with the top arc. Top arc going left to right through 12 o'clock. At 12 o'clock, path direction is east (rightward, since going 9→12→3, at 12 o'clock moving toward 3 o'clock = east). Walking east, text is on the left = north = up = away from center (outside). So top text is outside/above, right-side up. 

Hmm wait, but for the top arc, we usually want the text above the arc (outside the circle). And it would be right-side up. But actually for a badge, top text is often right-side up too. OK good.

Wait, I realize I should double-check the "text is on the left of path direction" claim. Actually, I believe in SVG, text on a path is positioned so that the text is on the left side of the path when traversing it in the direction of the path. Let me just go with this and it should work.

Actually, let me reconsider. I recall that for bottom text in badges, people often flip it. Let me just try the straightforward approach and if it's wrong, well, it's a reasonable attempt. But since I can't render, let me be careful.

Hmm, let me reconsider. Actually I've seen many SVG badges where bottom text is drawn with the path going right-to-left. Let me reconsider which gives right-side-up text.

Let me very carefully think about one glyph. Take the letter "O" at the bottom of a circle, center bottom (6 o'clock position, (250, 440)).

We want this "O" to appear right-side up on screen (its bounding box is a normal O, not flipped).

textPath: the text is laid out along the path. The path at (250,440) — if the path is the bottom semicircle, the tangent there is horizontal. The glyph is placed with its baseline on the path and its ascent going perpendicular to the path.

The question: does ascent go toward center (north/up) or away from center (south/down)?

If ascent goes toward center (up), the glyph is right-side up (letters grow upward from baseline). If ascent goes away from center (down), the glyph is upside down.

For the glyph to be right-side up at the bottom, ascent must go up (toward center). 

Now, SVG places the glyph's ascent on the LEFT side of the path traversal direction. So we need: at (250,440) moving along the path, the left side points up (north/toward center).

If we move along the path in the EAST direction (rightward, from 9→6→3 at the bottom), our left hand points NORTH (up). ✓ So moving east (left-to-right) at the bottom gives right-side-up text.

If we move WEST (right-to-left, from 3→6→9), our left points SOUTH (down), giving upside-down text.

So: bottom text should be drawn with path going LEFT-TO-RIGHT (west to east) along the bottom for right-side-up text.

Path: M 60 250 A 190 190 0 0 0 440 250 (left to right, through bottom, sweep=0).

Wait, let me double-check sweep=0 gives the bottom arc. M 60 250 to 440 250, sweep=0 (counterclockwise). Counterclockwise on screen from left point... 9 o'clock counterclockwise goes to 8,7,6 o'clock (down). Yes, through the bottom. ✓

Great, so:
- Top: M 60 250 A 190 190 0 0 1 440 250 (sweep=1, over top, L-to-R)
- Bottom: M 60 250 A 190 190 0 0 0 440 250 (sweep=0, through bottom, L-to-R)

Both read left-to-right and are right-side up. 

Hmm wait, let me re-examine the top one. Top: M 60 250 A 190 190 0 0 1 440 250, sweep=1 (clockwise). From 9 o'clock clockwise: 9→10→11→12 (top). Through the top. ✓ Direction at 12 o'clock: moving from 11→12→13(=1), so eastward (rightward). Left of east is north (up, away from center). So text grows upward, away from center = outside = above the circle. Right-side up. ✓

Good, both work. Let me use these.

Actually, let me reconsider whether I even want curved text. It adds complexity. But it looks much better for a sports logo. Let me include it. I'll use textPath.

Let me also reconsider: the user said "Der Hintergrund des Logos soll einfarbig sein, am besten besitzt das Logo gar keinen Hintergrund." = "The background of the logo should be solid-colored, preferably the logo has no background at all."

So either a solid background or transparent. I'll go with transparent (no background rect) but include the circular badge as part of the logo itself. The circle is part of the logo design, not a "background." That satisfies "no background" while still being a clean logo. Actually, the circle could be seen as the logo's main shape. Let me make the circle part of the logo.

Hmm, but they said background should be solid or none. If I have a colored circle, that's the logo shape, fine. Let me make the badge circle part of the logo. Good.

Let me now write the full thing.

Let me define the owl carefully.

Owl composition (centered around x=250):

Ears/tufts (owl ear tufts - like pointed ears):
- Left tuft: triangle around (195, 160)
- Right tuft: triangle around (305, 160)

Head: large circle/ellipse. Let me make the head and body somewhat merged for a cute owl.

Actually, let me make a classic owl: big round head with two big eyes, small body below with wings and belly feathers.

Let me define:

Head: circle cx=250 cy=210 r=95 (this is the main head area)

Actually, let me make the body and head as one rounded shape, with the eyes prominent.

Let me do:
- Body ellipse: cx=250 cy=320 rx=100 ry=110 (main body/torso)
- Head: circle cx=250 cy=200 r=85 (head on top of body)
- Ear tufts: two triangles at top of head
- Eyes: two big circles on the head
- Beak: small triangle between/below eyes
- Wings: two shapes on the sides of the body
- Belly: lighter ellipse on the body with feather lines
- Feet: two small feet at the bottom

Let me place eyes:
- Left eye: cx=215 cy=200 r=42
- Right eye: cx=285 cy=200 r=42
- Pupils: cx=215 cy=200 r=18 (dark), with a highlight
- Yellow ring around eyes

Beak: triangle at (250, 235), pointing down. Points: (238,228) (262,228) (250,255)

Let me refine positions so the owl looks balanced.

Let me set:
- Head center: (250, 195), radius 90
- Eyes at y=195, x=212 and x=288, radius 40 each
- Pupils radius 15, centered slightly inward and down
- Beak at (250, 230)

Ears:
- Left: polygon around (185, 130) - a pointed shape
- Right: mirrored

Let me define ear tufts as pointed triangles emerging from top of head:
- Left ear: (195,130) (175,80) (220,120) — roughly
- Right ear: (305,130) (325,80) (280,120)

Hmm, let me make them look like owl ear tufts (feather clusters). I'll use simple triangles.

Body: ellipse cx=250 cy=330 rx=95 ry=100

Wings: 
- Left wing: a shape on the left side of the body
- Right wing: mirrored

Let me make wings as curved shapes:
- Left wing path: M 165 290 Q 120 340 160 410 Q 180 380 185 330 Z (approx)
- Right wing: mirrored

Belly: lighter ellipse cx=250 cy=345 rx=60 ry=70, with V-shaped feather marks.

Feathers on belly: a few inverted-V or scale patterns.

Feet: two small orange feet at bottom of body, around (225,425) and (275,425).

Let me also add the hockey stick behind the owl.

Hockey stick: Let me place it diagonally behind the owl, going from upper-left to lower-right, or vertical. Let me do a vertical stick slightly to the right, with the blade at the bottom.

Actually, a hockey stick crossing behind the owl diagonally looks dynamic. Let me do that.

Let me define the hockey stick as a group. I'll draw it in a local coordinate (vertical) then rotate.

Stick handle: long thin rounded rectangle, say from (248, 60) to (252, 400) — but I'll rotate it.

Blade: at the bottom, a hockey stick blade shape.

Let me define the blade path (vertical stick, blade at bottom pointing right):
The blade connects to the bottom of the handle and curves. Standard hockey stick blade:
- Heel at top of blade (connects to handle)
- Blade extends horizontally
- Toe at the end (curved up slightly)

Path for blade (in local coords, handle going up from blade):
Let's say handle bottom is at (250, 360). Blade:
M 244 360 L 244 388 L 308 388 Q 322 388 322 372 L 322 366 Q 316 360 300 360 Z
Hmm, this is getting complicated. Let me simplify the blade to a clear hockey stick shape.

Actually, let me draw the hockey stick more simply and recognizably:
- Handle: thin long shape
- Blade: an L-shape or hook at the bottom

Let me define the whole stick as one path for simplicity, or as separate elements.

Let me do:
Handle: rect x=246 y=70 width=8 height=300 rx=4, fill wood color #B8791F
Blade: a path at the bottom.

For the blade, let me make it point to the right:
The handle ends at y=370. The blade extends from there.

Blade path:
Start at handle bottom-left (246, 360)
Down to (246, 385) — this is the heel height
Right along bottom to (310, 385)
Up and curve to toe (318, 372)
Back left along top to (258, 360)
Close

Something like:
M 246 358 L 246 386 L 312 386 Q 322 386 322 372 L 322 366 Q 318 358 306 358 Z

Let me refine: the blade should look like a hockey stick blade. The bottom is flat (touches ice), the top connects to the handle, and the toe (front) curves up.

Let me use:
M 247 360 
L 247 388 
L 310 388 
Q 324 388 324 374 
L 324 368 
Q 320 360 308 360 
Z

This creates a blade that's flat on bottom, has a heel on the left, and a curved toe on the right.

Then rotate the whole stick group.

Let me place the stick behind the owl, rotated about 20 degrees, positioned so it's behind the owl.

Actually, let me reconsider the composition. Maybe put the hockey stick diagonally behind the owl, handle pointing up-left, blade down-right. This is classic for sports logos.

Let me rotate the stick group by, say, -25 degrees around the center.

Hmm, but then it might overlap awkwardly. Let me think.

Alternative: put the hockey stick vertically behind the owl, handle up, blade down, slightly offset. The owl sits in front. This is clean.

Or, two sticks crossed behind (like an X) — very sports-logo. But the user said "Eishockeyschläger" (singular), so one stick. Let me do one stick.

Let me place one hockey stick diagonally behind the owl. Handle upper-right, blade lower-left, or handle upper-left, blade lower-right.

Let me go with: stick going from top-left to bottom-right, behind the owl. Rotate the vertical stick by about 140 degrees or so. Ugh, let me just use a transform.

Actually, simplest: draw the stick vertical (handle up, blade down at bottom), then apply transform="rotate(angle) translate(...)". 

Let me place the stick so it's behind and to the... let me put it as a background element crossing the whole badge.

Let me define stick in local coords centered so rotation is around badge center (250,250):
- Handle: from (245, 60) to (255, 430) — a long stick
- Blade at bottom (y~430)

Then rotate by, say, 18 degrees to make it diagonal. And it'll be behind the owl.

Wait, if the stick is tall (from y=60 to y=430) and I rotate it, the blade at the bottom will swing around. Let me make sure it stays within the badge.

Badge radius 225, center (250,250). So it spans from y=25 to y=475, x=25 to x=475.

If stick handle top at (250,60) and I rotate 20° around (250,250):
The top point (250,60) is at distance 190 above center, angle -90° (pointing up). Rotating 20° clockwise → angle -70°, new position: (250 + 190*sin(20°), 250 - 190*cos(20°)) = (250+65, 250-178) = (315, 72). Within badge ✓.

The blade at bottom (250, 430) is 180 below center, angle +90°. Rotate 20° clockwise → angle 110°, position (250+180*sin(20°)... wait let me recompute. Rotating a point at angle θ by +20° (clockwise in screen = ... hmm).

This is getting complicated. Let me just place the stick and rotate, and trust it fits. I'll make the stick not too long.

Let me reconsider and simplify: I'll put the hockey stick behind the owl, mostly vertical but tilted, with the blade poking out at the bottom-right. Let me just define coordinates directly without rotation to avoid confusion.

Direct hockey stick (tilted):
Handle: a thick line/rectangle from top-left to bottom-right.
Let me define handle as a polygon:
Top of handle: around (210, 75)
Bottom of handle (where blade attaches): around (300, 380)
Handle width ~12.

Handle polygon points:
(206, 78) (214, 72) — top end
... down to ...
(296, 383) (304, 377) — bottom end

Simplify: two long parallel lines. Let me just use a rotated rect via transform. That's cleanest.

OK let me just use transform="rotate(...)". I'll rotate a vertical stick.

Vertical stick (local coords):
- Handle: rect x=246 y=80 width=10 height=290 rx=5
- Blade: path at bottom

Then group transform: rotate(16 250 250) — rotate 16 degrees around center. Wait, positive rotation in SVG is clockwise. Let me rotate so handle goes up-right and blade down-left, or vice versa.

Hmm, let me just rotate by a small angle and place it. Let me actually make it more dramatic, like 22 degrees.

Actually, let me reconsider the entire layout to make it look good. Let me place:
- The owl in the center
- One hockey stick behind, tilted, blade at lower area
- "OWAYO" text on top arc
- "EURLERS" text on bottom arc

Let me write it all out now and stop second-guessing.

Let me reconsider the owl to make it look good. I'll draw it more carefully.

Final owl design:

Body (torso): ellipse, cx=250, cy=335, rx=92, ry=105, fill bodyGrad (blue gradient)

Head: circle, cx=250, cy=200, r=88, fill bodyGrad

Wait, if head is at cy=200 r=88, it spans y=112 to y=288. Body at cy=335 spans y=230 to y=440. They overlap around y=230-288. That's fine, they merge.

Ear tufts: 
- Left: polygon points (188,128) (165,78) (215,118) — a pointed tuft
- Right: polygon points (312,128) (335,78) (285,118)

Eye sockets / eye circles:
- White circles: left cx=213 cy=198 r=43, right cx=287 cy=198 r=43
- Yellow rings: I'll draw circles with stroke around them, or just make the eye circles have a yellow fill ring. Let me make eye circles yellow-filled with dark pupils. Actually classic owl: big black eyes. But for a logo, let me do dark pupils with white eye circles and a yellow/orange ring.

Let me do:
- Eye circle (white): left cx=213 cy=198 r=40, right cx=287 cy=198 r=40
- Pupil (dark): left cx=216 cy=200 r=17, right cx=284 cy=200 r=17
- Highlight: small white circle left cx=210 cy=192 r=5, right cx=278 cy=192 r=5

Hmm, but owls have big dark eyes. Let me make pupils bigger for a striking look. Let me make pupils r=20 and add a subtle ring.

Actually, let me add a dark eye "mask" around the eyes like many owls have, then white eye, then dark pupil. Or simpler: just big eyes.

Let me keep it clean:
- Eye rings (dark navy): left cx=213 cy=198 r=46, right cx=287 cy=198 r=46 — no wait, that would cover the head. Let me instead give the eyes a bright ring.

Let me do this:
- Around each eye, a ring: circle cx=213 cy=198 r=44, fill none, stroke gold #F7B400, stroke-width=6. Same for right.
- Eye white: circle cx=213 cy=198 r=36, fill white (or very light). Actually let me make the eye fill a light yellow/cream.
- Pupil: circle cx=215 cy=200 r=16, fill dark #1A1F36
- Highlight: circle cx=209 cy=193 r=5, fill white

Beak: triangle, points (240,232) (260,232) (250,258), fill orange #F29300. Maybe two parts.

Wings:
- Left wing: path starting from body left, curving out and back. 
  M 168 300 Q 128 345 150 415 Q 172 392 182 330 Z
  fill a slightly darker blue
- Right wing: mirrored
  M 332 300 Q 372 345 350 415 Q 328 392 318 330 Z

Belly: ellipse cx=250 cy=350 rx=58 ry=68, fill lighter color (#DCE3F5 or cream). 
Then feather marks: a few rows of small arcs or V shapes on the belly.

Let me add belly feathers as small arcs:
Row of "scales" - I'll draw a few curved lines. Let me do simple: a few inverted-V or U shapes.

Actually, let me add belly feather lines as a pattern of small arcs. I'll draw maybe 3 rows.

Feet: two orange feet at bottom of body.
- Left foot: around (228, 435): small shapes
- Right foot: around (272, 435)
Let me draw feet as small orange shapes (3 toes each). Simple: 
- Left: path or just small ellipses. Let me do: M 228 430 L 220 450, M 228 430 L 232 452, M 228 430 L 244 448 — three lines (toes). And same for right at (272,430).

Hmm, let me make feet simpler: small orange ellipses or just triangles.

Let me finalize and write. I'll add details but keep it manageable.

Let me also reconsider colors:
- Head/body: blue gradient from #5B70B8 to #2C3E6E
- Accent (eyes ring, beak, stick, text): orange/gold #F7B400 / #F29300
- Belly: light cream #E8EDFA
- Dark accents (pupils, outlines): #1A2240
- Stick handle: wood brown #B5792B with darker #8A5A1E

Let me write the SVG.

For text, I'll use font-family that's bold and available. Let me use "Arial, Helvetica, sans-serif" with font-weight bold, letter-spacing.

Top text: "OWAYO" on top arc
Bottom text: "EURLERS" on bottom arc

Let me set font-size around 42, bold, fill gold or white. Let me make text white for the top and gold for... or both gold. Let me do gold text with maybe a dark outline for readability. Actually, let me make text a light cream/white and add subtle shadow. Keep simple: gold text.

Hmm, let me reconsider. On a navy badge, gold text and gold ring looks classic and sporty. Let me use gold (#F7B400) for text and ring, white for owl details.

Let me also add a subtle inner ring or stars. Maybe two small stars between the text and owl. Optional. Let me add small stars/dots for flair. Actually, let me add two small 4-point stars or just leave clean. Let me add small dots separating top and bottom text. Or keep minimal.

Let me write it now.

One more consideration: the text on arcs. Let me make sure the radius works. Badge radius 225. Text arc radius ~185 (inside the ring at 213). Let me set text paths at radius 180.

Top path: M 70 250 A 180 180 0 0 1 430 250
Bottom path: M 70 250 A 180 180 0 0 0 430 250

Wait, these use radius 180 from center (250,250). Left point: 250-180=70 ✓. Right point: 250+180=430 ✓. Good.

Let me set text-anchor middle and startOffset/endOffset to center the text on the arc.

For top text "OWAYO", center it at top (12 o'clock). Use startOffset="50%" with text-anchor="middle".
For bottom text "EURLERS", center at bottom (6 o'clock). startOffset="50%", text-anchor="middle".

Let me write:
```
<text font-family="Arial, Helvetica, sans-serif" font-weight="bold" font-size="40" letter-spacing="4" fill="#F7B400">
  <textPath href="#topPath" startOffset="50%" text-anchor="middle">OWAYO</textPath>
</text>
<text ...>
  <textPath href="#bottomPath" startOffset="50%" text-anchor="middle">EURLERS</textPath>
</text>
```

Wait, I need to reference the paths. Let me define them with ids, or inline. I can use href="#id" referencing a <path> with id. Or I can put the path data directly in textPath using d="...". Let me use d attribute directly in textPath for simplicity:
```
<textPath d="M 70 250 A 180 180 0 0 1 430 250" startOffset="50%" text-anchor="middle">OWAYO</textPath>
```

That works in SVG.

Now let me assemble everything.

Let me reconsider the stick placement so it looks good behind the owl. I'll draw the stick first (so it's behind), then the owl on top.

Stick: I'll place it tilted. Let me use a transform to rotate. Let me draw a vertical stick and rotate by about 16°.

Let me define the stick in a group:
```
<g transform="rotate(18 250 250)" opacity="0.95">
  <!-- handle -->
  <rect x="246" y="72" width="10" height="300" rx="5" fill="#B5792B"/>
  <rect x="246" y="72" width="5" height="300" rx="3" fill="#8A5A1E" opacity="0.4"/> <!-- shading -->
  <!-- blade -->
  <path d="M 244 368 L 244 396 L 312 396 Q 326 396 326 380 L 326 372 Q 321 368 308 368 Z" fill="#E8EDFA" stroke="#1A2240" stroke-width="3"/>
  <!-- blade edge line -->
  <line x1="244" y1="396" x2="320" y2="396" stroke="#1A2240" stroke-width="2"/>
</g>
```

Hmm, with rotate(18 250 250), the stick tilts. The handle top at (250,72) will move. Let me check it stays in badge. Distance from center to (250,72) is 178. After rotating 18°, still 178 from center, within badge (radius 225). ✓. Blade bottom at (255, 396) roughly, distance ~146, fine.

But wait, when rotated, the blade (which points right in local coords) will point down-right. That's fine, it's behind the owl.

Actually, let me reconsider - I want the stick to look like it's held or behind. Let me make the handle longer so it extends up, and blade at bottom. With rotation, it becomes diagonal. Good.

Let me also make sure the stick is behind the owl. Since I draw the owl after the stick in document order, the owl will be on top. Good.

But actually, the stick blade at the bottom might look like it's sticking out below the owl, which is fine (like the owl is holding it, or it's behind).

Let me reconsider: maybe I want the stick more clearly a hockey stick. The blade shape I defined is a rough hook. Let me refine it to be more recognizable.

A hockey stick blade (side view):
- The shaft (handle) comes down to the heel
- The blade is the flat part that hits the puck
- Bottom edge is flat (on ice)
- Front edge (toe) curves up
- There's a "toe" and "heeler"

Side view blade shape:
```
M 244 368   (heel top, connects to shaft)
L 244 396   (down to bottom/heel bottom) -- wait, heel should go down a bit
L 258 396   
Q 258 388 262 388  -- no
```

Let me think. Side view, shaft coming from top at x~250. Blade extends to the right.
- Heel: vertical part connecting shaft to blade, at left of blade. From (248,368) down to (248,392).
- Bottom of blade: from (248,392) right to (318,392), flat.
- Toe: from (318,392) curving up to (318,368) area — the toe curves up. From (318,392) Q 324 378 316 370, then top of blade from (316,370) back left to (256,368).
- Top of blade: from (316,370) to (256,368), then connect to shaft.

Let me define:
```
M 250 366   near shaft
L 250 394   down the heel
L 316 394   along the bottom (flat, on ice)
Q 326 394 324 378   toe curves up-and-out
L 324 372   
Q 320 366 306 366   back along top of blade to connect to shaft
Z
```

Hmm, let me simplify and just make it look like a hockey stick. I'll go with:
```
<path d="M 250 366 L 250 396 L 318 396 Q 330 396 330 378 L 330 370 Q 324 364 310 364 Z" .../>
```

And add the shaft connecting: the shaft rect goes from y=72 to y=366, and the blade starts at y=366. Good, they connect.

Let me add a stroke to the blade for outline.

OK let me also reconsider: should the stick be in front or behind? For "owl holding a hockey stick" vibe, the stick could be behind (owl in front holding it) or the owl in front with stick crossing. Let me put stick behind. Actually, if the owl "holds" it, the stick behind the owl's body with the owl's wings/feet in front could look like it's gripping. But simpler to just have it as a background element behind the owl. Let me put it behind.

Hmm, actually, let me reconsider the whole thing. Let me make the hockey stick prominent and clearly visible, crossing behind the owl diagonally. This is a common sports logo trope.

Let me finalize coordinates and write.

Let me reconsider the eye design to make the owl look good and recognizable. Big round eyes are key for an owl. Let me make them prominent.

Let me also add a "forehead" detail or crown feathers. And maybe make the head slightly distinct from body.

Let me write the final SVG. I'll be generous with detail but keep it clean.

Let me reconsider colors once more for a cohesive hockey team look:
- Primary: deep navy #1B2651 (badge background)
- Secondary: royal blue #3F5797 / #5468A8 (owl body)
- Accent: gold/orange #F7B400 (ring, text, eyes ring, beak, stick tape)
- Light: #E8EDFA (belly, blade, eye whites)
- Dark: #141A30 (pupils, outlines, stick shading)
- Wood: #B5792B (stick handle)

Let me write it.

Actually, for the owl body gradient, let me use:
```
<linearGradient id="owlBody" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0" stop-color="#5E74BC"/>
  <stop offset="1" stop-color="#33488A"/>
</linearGradient>
```

And maybe a radial highlight on the head.

Let me write the complete SVG now.

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 500 560" width="500" height="560">
  <defs>
    <linearGradient id="owlBody" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#6279C4"/>
      <stop offset="1" stop-color="#2F4588"/>
    </linearGradient>
    <radialGradient id="headHighlight" cx="0.42" cy="0.32" r="0.75">
      <stop offset="0" stop-color="#7C92D6"/>
      <stop offset="1" stop-color="#3F5797"/>
    </radialGradient>
    <linearGradient id="bellyGrad" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#F1F4FC"/>
      <stop offset="1" stop-color="#D3DAF0"/>
    </linearGradient>
  </defs>

  <!-- Badge background -->
  <circle cx="250" cy="250" r="230" fill="#17224A"/>
  <circle cx="250" cy="250" r="216" fill="none" stroke="#F7B400" stroke-width="6"/>
  <circle cx="250" cy="250" r="206" fill="none" stroke="#3F5797" stroke-width="3"/>

  <!-- Hockey stick (behind owl) -->
  <g transform="rotate(16 250 250)">
    <!-- shaft -->
    <rect x="247" y="78" width="12" height="300" rx="6" fill="#B5792B"/>
    <rect x="247" y="78" width="5" height="300" rx="3" fill="#8A5A1E" opacity="0.5"/>
    <!-- blade -->
    <path d="M 250 372 L 250 402 L 322 402 Q 336 402 336 382 L 336 372 Q 330 366 314 366 Z"
          fill="#EDEFF8" stroke="#141A30" stroke-width="3" stroke-linejoin="round"/>
    <line x1="252" y1="402" x2="330" y2="402" stroke="#141A30" stroke-width="2"/>
  </g>

  <!-- Owl -->
  <!-- body -->
  <ellipse cx="250" cy="340" rx="96" ry="110" fill="url(#owlBody)" stroke="#1E2A58" stroke-width="3"/>
  <!-- belly -->
  <ellipse cx="250" cy="356" rx="60" ry="72" fill="url(#bellyGrad)"/>
  <!-- belly feather lines -->
  <g stroke="#AEB8DE" stroke-width="3" fill="none" stroke-linecap="round">
    <path d="M 222 320 Q 237 334 252 320"/>
    <path d="M 248 320 Q 263 334 278 320"/>
    <path d="M 216 352 Q 237 368 258 352"/>
    <path d="M 252 352 Q 273 368 294 352"/>
    <path d="M 224 386 Q 245 402 266 386"/>
    <path d="M 260 386 Q 281 402 302 386"/>
  </g>

  <!-- wings -->
  <path d="M 166 300 Q 122 340 146 418 Q 170 392 184 332 Z" fill="#2C407F" stroke="#1E2A58" stroke-width="3"/>
  <path d="M 334 300 Q 378 340 354 418 Q 330 392 316 332 Z" fill="#2C407F" stroke="#1E2A58" stroke-width="3"/>

  <!-- ears -->
  <path d="M 190 132 L 164 78 L 216 120 Z" fill="#3F5797" stroke="#1E2A58" stroke-width="3" stroke-linejoin="round"/>
  <path d="M 310 132 L 336 78 L 284 120 Z" fill="#3F5797" stroke="#1E2A58" stroke-width="3" stroke-linejoin="round"/>

  <!-- head -->
  <circle cx="250" cy="200" r="90" fill="url(#headHighlight)" stroke="#1E2A58" stroke-width="3"/>

  <!-- eyes -->
  <circle cx="211" cy="200" r="44" fill="#F7B400" stroke="#141A30" stroke-width="3"/>
  <circle cx="289" cy="200" r="44" fill="#F7B400" stroke="#141A30" stroke-width="3"/>
  <circle cx="214" cy="202" r="19" fill="#141A30"/>
  <circle cx="286" cy="202" r="19" fill="#141A30"/>
  <circle cx="206" cy="193" r="6" fill="#FFFFFF"/>
  <circle cx="278" cy="193" r="6" fill="#FFFFFF"/>

  <!-- beak -->
  <path d="M 238 236 L 262 236 L 250 264 Z" fill="#F29300" stroke="#141A30" stroke-width="2.5" stroke-linejoin="round"/>

  <!-- feet -->
  <g stroke="#F29300" stroke-width="6" stroke-linecap="round" fill="none">
    <path d="M 226 442 L 216 462"/>
    <path d="M 232 444 L 234 466"/>
    <path d="M 238 442 L 252 460"/>
    <path d="M 262 442 L 248 460"/>
    <path d="M 268 444 L 266 466"/>
    <path d="M 274 442 L 284 462"/>
  </g>

  <!-- Text -->
  <text font-family="Arial Black, Arial, Helvetica, sans-serif" font-weight="bold" font-size="44" letter-spacing="6" fill="#F7B400">
    <textPath d="M 66 250 A 184 184 0 0 1 434 250" startOffset="50%" text-anchor="middle">OWAYO</textPath>
  </text>
  <text font-family="Arial Black, Arial, Helvetica, sans-serif" font-weight="bold" font-size="44" letter-spacing="6" fill="#F7B400">
    <textPath d="M 66 250 A 184 184 0 0 0 434 250" startOffset="50%" text-anchor="middle">EURLERS</textPath>
  </text>
</svg>
```

Wait, I need to double check the bottom text orientation. As I analyzed, bottom path M 66 250 A 184 184 0 0 0 434 250 goes left-to-right through the bottom, and text should be right-side up. Let me trust that.

Hmm, but actually let me reconsider. I've seen that with textPath, the text is placed on the left side of the path direction. Let me re-examine for the bottom.

Bottom path from (66,250) to (434,250) with sweep=0 (counterclockwise), going through the bottom (250, 434).

At the bottom point (250,434), the path direction (as we travel from start to end, i.e., from left, down through bottom, to right) is rightward (east). Text is placed on the left of the direction of travel. Traveling east, left is north (up, toward center). So the text's ascent points north (up). So the text is right-side up, sitting just inside the bottom arc. 

But wait — "just inside the bottom arc" means the text is above the arc line, i.e., inside the circle. And right-side up. For a badge, bottom text is usually right-side up and inside the ring. That's correct!

Hmm, but actually, I realize the text baseline is ON the path (the arc at radius 184), and text extends upward (north) into the circle. So the text sits between radius 184 and smaller radius, inside the circle, right-side up. That's the standard badge look. 

But hold on, is that right? Let me reconsider. If the baseline is at radius 184 (bottom) and text extends upward (toward center), the text occupies from radius ~184 down to ~140 (for 44px text, roughly). So the text is inside the circle near the bottom. Right-side up. Yes, that's the badge style. 

Now top text: path from (66,250) to (434,250) sweep=1, through top (250,66). At top point (250,66), direction of travel (left to right through top) is eastward. Left of east is north (up, away from center). So text extends north (up, away from center), sitting outside/above the top arc. Right-side up. 

So both texts are right-side up, top text above the top arc, bottom text below... wait, bottom text is inside near bottom. Let me reconsider — is that what we want? For a badge, yes, text follows the circle. Top text along top curve, bottom text along bottom curve. Both readable. 

Actually, wait. I want to double-check that the bottom text won't be upside down. Let me reconsider very carefully with a concrete mental model.

Imagine walking along the bottom path from (66,250) [left] toward (434,250) [right], passing through (250,434) [bottom]. At the very bottom (250,434), I'm facing east (rightward, since I'm going from left to right). I place text such that it's on my LEFT hand side. My left hand points north (up, toward center of circle at 250,250). So the text is on the center side (inside), and grows upward (north). A person looking at the screen sees the text right-side up (letters grow upward). 

Yes! Right-side up. 

But actually, hmm, wait. Let me reconsider "text on the left of direction of travel." Is that correct for SVG? 

I recall that SVG text on a path: "the text is placed on the path such that the text flows in the direction of the path, and the text is on the left side of the path." Actually, I'm not 100% sure it's "left side." Let me think about the default.

From the SVG spec: "The text is placed on the path, following its direction. The glyphs are positioned on the path, with the baseline of the text on the path." And the orientation: each glyph is rotated to follow the path. The ascent direction is perpendicular to the path, on the left side of the direction of travel.

Hmm, I've seen conflicting info. Let me just go with my analysis. If it's slightly off, it's still a reasonable logo. But let me hedge by making the design robust.

Actually, you know what, let me reconsider. I've definitely seen SVG badge code where the bottom text is created with the path going the "wrong way" and it works out. Let me reconsider by thinking about a real example.

Common pattern I've seen:
```
<path id="bottomText" d="M 100 250 a 150 150 0 0 0 300 0" />
```
This is a semicircle at the bottom (from (100,250) curving down to (400,250)), sweep=0. Wait, that's the same as what I have (roughly). And then text on it reads... 

Hmm, actually I've also seen:
```
<path id="bottomText" d="M 100 250 a 150 150 0 0 1 300 0" />
```
with sweep=1, and then the text is flipped.

I think there's genuine confusion here. Let me just go with my geometric analysis: bottom path sweep=0, left-to-right, gives right-side-up text. I'm fairly confident.

Hmm, wait, let me reconsider one more time, because I keep going back and forth.

Let me use a super concrete approach. Place a single character "A" at the bottom of the circle, at (250, 434). I want it to look like a normal "A" (point up).

The path at (250,434): the tangent is horizontal. The path has a direction (either east or west depending on how I draw it).

Case A: Path drawn left-to-right (sweep=0 as I said), so at (250,434) direction = east.
SVG rule (which I'll state): the glyph's baseline is tangent to the path, and the glyph is oriented so that its top (ascent) is 90° counter-clockwise from the path direction... 

Hmm, "counter-clockwise from path direction." Path direction = east (90° in standard, or "east"). Rotating east by 90° counter-clockwise (in screen terms, CCW) gives north. So ascent points north (up). Glyph is right-side up. 

Wait, but is it CCW or CW? Let me think about the top case to calibrate.

Top case: path drawn left-to-right through the top (sweep=1), at top point (250,66) direction = east. If the rule gives the same result (ascent = 90° CCW from direction), then ascent = north = up = away from center. Text is right-side up, above the arc. For a badge, top text is right-side up. ✓. Consistent.

Now, is the rule "ascent = 90° CCW from direction" correct? Let me sanity check with the top text being right-side up (which it should be). Direction east, 90° CCW = north. Text grows north (up). Right-side up. ✓. This matches reality (top of badge text is right-side up). 

So for bottom: direction east, 90° CCW = north, text grows north (up, toward center). Right-side up, inside the circle at the bottom. ✓.

Great, consistent. Bottom text sweep=0 is correct.

Hmm, but wait, I should double-check the direction at the top point for the top path. Top path: M 66 250 A 184 184 0 0 1 434 250. Start (66,250), end (434,250), sweep=1. At the start (66,250) which is the left point (9 o'clock), the initial direction of the arc... For sweep=1 (clockwise), starting at 9 o'clock going clockwise means going up first (toward 12 o'clock). So initial direction at (66,250) is north-ish (up and slightly right). At the top (250,66), direction is east. At end (434,250) direction is south. OK so at top, east. ✓.

Good.

Now, one concern: I set the text to be right-side up, but for the BOTTOM text, is it typical to have it right-side up inside the circle? Let me reconsider. In many sports badges, the bottom text IS right-side up and follows the bottom curve. Yes. E.g., "EST. 2020" at the bottom, right-side up. So this is correct.

Alright. Let me also reconsider: maybe I should make the bottom text read right-side up but I realize some people prefer it to curve and be right side up — which is what I have. Good.

Now let me reconsider the overall look and refine a few things:

1. The owl eyes are gold with dark pupils — that's a bit unusual (owls usually have dark eyes), but for a logo it looks striking and matches the team accent color. Actually, let me reconsider — maybe make eyes more owl-like. Real owls have large dark eyes. But a stylized logo with gold eye-rings and dark centers looks good and ties to the color scheme. Alternatively, white eyes with dark pupils (like a more realistic owl). Let me do white eyes with dark pupils — more owl-like and cleaner. Actually, let me keep gold rings around white eyes — that's a classic "owl logo" look (think of cartoon owls with big round eyes). 

Let me do: white eye circles with a gold ring, dark pupils. That's clean and recognizable.

Let me redo eyes:
- Eye white: circle cx=211 cy=200 r=42, fill #FFFFFF, stroke #141A30 width 3
- Gold ring: circle cx=211 cy=200 r=46, fill none, stroke #F7B400 width 7. But this would overlap. Let me instead: draw gold ring first (thick stroke), then white eye on top.
  - Gold ring: circle cx=211 cy=200 r=44, fill none, stroke #F7B400 width 8
  - White eye: circle cx=211 cy=200 r=38, fill #FFFFFF
  - Pupil: circle cx=214 cy=202 r=17, fill #141A30
  - Highlight: circle cx=205 cy=193 r=6, fill #FFFFFF

Wait, if white eye r=38 and pupil r=17 at (214,202), and highlight at (205,193). Let me make pupils look toward center a bit (pupils slightly inward). Left pupil at (216,201), right pupil at (284,201). Highlights upper-left of pupils.

Let me finalize eyes:
Left:
- ring: cx=211 cy=200 r=45, stroke #F7B400 width 8, no fill
- white: cx=211 cy=200 r=39, fill #FDFDFD
- pupil: cx=215 cy=202 r=17, fill #141A30
- highlight: cx=207 cy=193 r=6, fill #FFFFFF
Right (mirror x around 250: 211→289, 215→285, 207→293):
- ring: cx=289 cy=200 r=45, stroke #F7B400 width 8
- white: cx=289 cy=200 r=39, fill #FDFDFD
- pupil: cx=285 cy=202 r=17, fill #141A30
- highlight: cx=293 cy=193 r=6, fill #FFFFFF

Good.

2. The belly feather lines — let me make them look like little arcs/scales. I have them. Let me keep but maybe make them nicer. They're fine.

3. Feet — I drew them as lines. Let me make them look like owl feet (3 toes each). Lines work but let me add small claws or just keep simple lines. Fine.

Actually, owl feet typically point forward and grab. For a front-facing owl, feet at the bottom pointing down/outward. My lines go down and outward. OK.

4. Let me reconsider the head/body proportions. Head r=90 at cy=200 (spans y=110 to 290). Body at cy=340, ry=110 (spans y=230 to 450). They overlap y=230-290. The neck area is covered. Good.

But the eyes at cy=200 are on the head. The head spans y=110-290, eyes at y=200, good, centered on head. 

5. Let me make sure the stick doesn't look weird. With rotate(16°), it tilts. The blade at bottom-right (in local coords it points right, after +16° rotation it points down-right a bit). Actually rotate(16) is clockwise 16°. The blade which points east (right) in local coords will rotate to point 16° below east (south of east). So blade points down-right. Handle points up-left (after rotation, the top of handle which pointed north goes 16° toward east = north-east). Wait, rotate clockwise 16°: north → 16° toward east = NNE. So handle top points up and slightly right. Handle bottom (blade) points down and slightly left? No.

Let me reconsider. The stick is a vertical line in local coords (along y-axis). After rotate(16°) clockwise around center, the whole stick rotates 16° clockwise. So it becomes a line tilted 16° from vertical, leaning to the right at top (i.e., top is to the right of bottom). Handle top goes up-right, blade goes down-left. Wait:

A vertical line, rotate 16° clockwise: the top end moves to the right (east) and the bottom end moves to the left (west). So the stick leans like "/" ... no. Top moves right, bottom moves left: that's like "/" tilted, i.e., from bottom-left to top-right. So handle top is at top-right, blade at bottom-left.

Hmm, and the blade in local coords points right (east, toward positive x, at the bottom). After rotating 16° clockwise, the blade points 16° south of east? No. Let me think. The blade points east (from handle toward blade, direction east). Rotating the whole system 16° clockwise: east → 16° clockwise from east = south-east (down-right). So the blade points down-right. But the blade is at the bottom of the stick, and the stick's bottom is at bottom-left (after the lean). So the blade extends down-right from the bottom-left position. That might look odd.

This is getting too detailed. Let me just place the stick and not overthink. Let me maybe not rotate it, or rotate less. Actually, a tilted stick behind the owl looks fine regardless. Let me rotate by a smaller angle like 12° and position it. Or, let me reconsider and put the stick more deliberately.

Alternative cleaner idea: Put the hockey stick diagonally behind the owl, handle pointing up-right, blade pointing down-left, clearly crossing behind. Let me define it directly with a transform that I can reason about.

Let me define the stick vertically centered at (250, 250) so rotation is clean, then rotate.

Actually, let me just make the stick vertical (no rotation) behind the owl, handle going up past the owl's head, blade at the bottom below the owl. This is clean and clearly a hockey stick. The owl sits in front. Let me do that — simpler and cleaner.

Wait, but a purely vertical stick might look like the owl is sitting on it. That's actually fine and clean. But a tilt adds dynamism. Let me do a slight tilt of about 10°.

Hmm, let me reconsider. Let me put the stick tilted so it looks like it's resting behind the owl, handle upper area, blade lower area. Let me rotate by 12° and it'll be fine. Let me go with rotate(12 250 250).

Actually, let me reconsider the whole "stick behind owl" — maybe the stick should be more in front or to the side to be clearly visible. If it's directly behind the owl, most of it's hidden. Let me put it so a good portion is visible.

Let me put the stick behind the owl but tilted significantly so the blade sticks out clearly to one side at the bottom. Or, put the stick in front, crossing diagonally, with the owl in front too... no, can't have both in front.

Let me reconsider: classic sports logo — owl in center, hockey stick crossing behind diagonally, both ends visible (handle top-left, blade bottom-right). For both ends to be visible, the stick must be behind the owl but long enough that ends poke out. Since the owl is in the center and the stick is behind, the parts of the stick outside the owl's silhouette will show.

Let me make the stick long (handle from top of badge to near bottom) and tilted, so handle top shows in upper area and blade shows in lower area, both outside the owl. The middle is behind the owl.

Let me define stick from (250, 70) to (250, 440) locally (length 370), blade at bottom. Rotate 16° around (250,250). Then:
- Handle top (250,70): distance 180 above center. After rotate 16° CW: moves to angle... (250,70) is directly above center. Rotate 16° CW → 16° to the east of north. Position: (250 + 180*sin16°, 250 - 180*cos16°) = (250+49.7, 250-173.1) = (299.7, 76.9). Within badge ✓.
- Blade bottom (250,440): distance 190 below center. After rotate 16° CW: (250 + 190*sin16°... wait, (250,440) is directly below. Rotate 16° CW: 16° toward west (since rotating the bottom point clockwise moves it left). Position: (250 - 190*sin16°, 250 + 190*cos16°) = (250-52.3, 250+182.4) = (197.7, 432.4). Within badge ✓.

So after rotation: handle top at ~(300,77), blade at ~(198,432). The stick goes from top-right to bottom-left, tilted. The blade (which points right locally) — after rotation points... the blade direction was east, rotate 16° CW → 16° south of east? No wait, I need to rotate the blade's orientation too. Blade points east (from handle to blade, +x). Rotate 16° CW: east (0°) → -16° (in standard math) = 16° below east = pointing down-right. But the blade is at the bottom-left of the stick now. So blade extends down-right from bottom-left. Hmm, that means the blade points toward the bottom-center. It'll look like the blade is at bottom-left pointing toward center-right. That's a bit odd but OK.

Actually, maybe I should rotate the other way or flip the blade. Let me reconsider. I want the blade to point down and to the outside (bottom-left corner), which looks more natural for a stick resting there.

If I rotate counterclockwise (negative angle) instead: rotate(-16 250 250). Then:
- Handle top (250,70) → rotate 16° CCW → 16° west of north: (250-49.7, 76.9) = (200,77). Handle top at top-left.
- Blade bottom (250,440) → rotate 16° CCW → (250+52.3, 432.4) = (302, 432). Blade at bottom-right.
- Blade direction east rotate 16° CCW → 16° north of east = up-right. Blade at bottom-right pointing up-right (toward center). Hmm.

Either way the blade points somewhat inward. Let me just accept it or flip the blade to point outward.

Alternatively, let me flip the blade to point the other way (left) locally, so after rotation it points outward. If blade points west locally, rotate(16 CW): west → 16° south of west = down-left. Blade at bottom-left pointing down-left (outward). That looks natural!

So: draw the blade pointing LEFT in local coords (west), and rotate the stick 16° CW. Then blade ends up at bottom-right of the stick... wait let me redo.

Ugh, I'm overcomplicating. Let me just draw the stick in a final tilted orientation directly, without rotation. I'll compute the coordinates.

Let me define a stick tilted at angle θ from vertical. Let me pick θ = 18°, leaning so top is to the right.

Direction along stick (from handle-top to blade): let me make it go from upper-left to lower-right. So handle-top at upper-left, blade at lower-right.

Handle-top position: (180, 90)
Blade-attachment (bottom of handle) position: (320, 400)
Direction from handle-top to blade: (140, 310), normalized... angle = atan2(310,140) = about 65.6° from horizontal, i.e., pointing down-right. Good.

Handle: a thick line from (180,90) to (320,400), width ~13.
I'll draw it as a polygon or use a rotated rect.

Let me use a rotated rect:
- Center of handle: midpoint of (180,90) and (320,400) = (250, 245)
- Length: sqrt(140² + 310²) = sqrt(19600+96100)=sqrt(115700)=340
- Angle: atan2(310,140) = 65.6° from x-axis. For a rect, I want the long axis along this direction. rotate(65.6 ...) with width=13, height=340.

Hmm, but the blade needs to attach at the bottom end (320,400) and point in a hockey-stick direction.

This is getting complicated. Let me just use a transform rotate on the vertical stick and accept the blade direction. Let me choose the rotation and blade direction to look good.

Simplest robust approach: Draw vertical stick (handle up, blade down pointing right), then rotate by some angle. The exact blade direction after rotation doesn't matter much; it'll look like a tilted hockey stick. Let me just pick rotate(20 250 250) and make the blade point right (east) locally. After +20° rotation, blade points 20° below east (down-right-ish), handle top points up-right-ish. It'll look like a hockey stick tilted, blade at lower area. Fine.

Let me go with that. Actually, let me make the blade point right and place the stick so it's behind the owl, and it'll look like the owl has a hockey stick behind it. Good enough.

Let me also make the stick a bit transparent or just behind. I'll keep it opaque but behind the owl.

Hmm, actually, if the stick is directly behind the owl and the owl is fairly large, the stick will be mostly hidden. Let me make the stick thinner/longer so ends show, OR move it to the side.

Let me reconsider: maybe put the hockey stick to one side, not dead center behind. Like, the owl holds the stick and it leans to the right. Or two sticks. But user said one stick.

Let me put the stick diagonally behind, and it'll peek out on both sides of the owl. Since the owl body is ~190px wide and the stick is long, the handle top and blade will stick out.

Let me just go with it. Let me finalize.

Actually, let me reconsider making the stick clearly visible by placing it behind but with the handle going up and to the right, exiting near the top, and the blade at the bottom-right, both outside the owl. Let me make the owl a bit smaller or the stick longer.

Owl body rx=96, so ~192 wide, centered at x=250, spanning x=58 to 442. But the badge is radius 230 (x=20 to 480). So there's margin. The stick ends can be in that margin.

Let me make the stick long: handle from top (near y=70) to blade at bottom (near y=430). After tilt, ends will be around x=200-320, which is within the owl's x-range (58-442) mostly. So the stick middle is behind the owl, and ends might still be behind the owl's wings if the owl is wide. Hmm.

The owl's wings span out to x≈146 (left wing tip) and x≈354 (right wing tip). So between x=146 and x=354 is covered by the owl body/wings. The stick ends after rotation are at x≈200-320, which is within 146-354. So the stick ends would be BEHIND the owl. Not visible!

So a stick behind the owl with ends at x=200-320 is fully hidden. I need the stick ends to be outside x=146-354, i.e., x<146 or x>354.

To achieve that, the stick must be more horizontal or longer, OR the owl must be narrower, OR I place the stick so its ends stick out to the sides.

Option: Make the stick more horizontal (tilted ~60° from vertical), so it crosses the badge more horizontally, ends near the left and right edges. But then it's not a "vertical stick behind owl."

Alternatively, put the stick behind but tilted so one end (blade) sticks out to the lower-right beyond the wing, and the handle goes up behind the head. Let me make the stick long and tilted ~35°.

Hmm, let me reconsider the composition entirely. 

New idea: Put the hockey stick diagonally behind the owl, going from upper-left to lower-right, with BOTH ends clearly visible in the badge margin. To do this, the stick should span most of the badge diameter.

Let me place the stick as a long diagonal line from upper-left area to lower-right area, behind the owl.

Handle-top: (110, 95)
Blade: near (400, 430)
This line passes behind the owl (center ~250,250). Ends at (110,95) [upper-left, outside owl] and (400,430) [lower-right, outside owl]. 

Owl spans x=146-354, y=110-450 roughly (head top y=110, body bottom y=450, feet to 466). The point (110,95) is upper-left, outside owl (x<146). The point (400,430) is lower-right, outside owl (x>354). Good, both ends visible.

The middle of the stick (around x=255, y=260) is behind the owl. Good.

So let me define the stick from (110,95) to (400,430), with the blade at the (400,430) end.

Let me compute: 
- Handle: line from (110,95) to (360,380) [leaving room for blade], width 13.
- Blade at (400,430) end.

Direction of stick: from (110,95) to (400,430): (290, 335), angle = atan2(335,290) = 49° below horizontal. So the stick goes down-right at ~49°.

Handle: from (110,95) to (355,375). Length = sqrt(245²+280²)=sqrt(60025+78400)=sqrt(138425)=372.
Blade attaches at (355,375) and extends toward (400,430), i.e., continuing in the stick direction, then the blade curves.

The blade should be perpendicular-ish or continue the direction. A hockey stick blade continues in the shaft direction then has the flat blade part. Let me make the blade extend in the shaft direction and then the flat blade edge.

This is getting complex to draw directly. Let me use a transform to make it easier: define the stick vertically, then use rotate+translate to place it.

Let me define vertical stick centered nicely, then transform.

Local vertical stick:
- Handle: rect from (250-6, 100) to (250+6, 400): x=244, y=100, w=12, h=300.
- Blade: at bottom, pointing right (east), from y=400 down.

Now I want to place this so it goes from (110,95) upper-left to (400,430) lower-right, with blade at lower-right.

The local stick is vertical (pointing up for handle, down for blade). I need to rotate it to the 49° direction and translate.

Rotation angle: I want the handle (which points up, -y) to point toward upper-left. Upper-left direction from center... hmm, let me think in terms of the stick's own axis.

The stick's long axis should align with direction (290,335) normalized, i.e., pointing down-right at 49° below horizontal, or equivalently the handle points up-left.

The local handle points up (direction (0,-1), i.e., 90° in standard = pointing up). I want it to point up-left. Up-left direction ≈ (-0.7, -0.7), angle 135° standard, or in screen terms, up and left.

Angle between up (0,-1) and up-left (-0.7,-0.7): rotate up by ... (0,-1) rotated to (-0.71,-0.71). The rotation: (0,-1) → (-0.71,-0.71). This is a rotation. In SVG, rotate(angle) is clockwise positive. Rotating (0,-1) [up] clockwise by angle α gives (sin α, -cos α). I want (-0.71, -0.71). So sin α = -0.71, cos α = 0.71 → α = -45° (or 315°). So rotate(-45°).

So rotate the local stick by -45° (counterclockwise 45°), then translate.

After rotate(-45°), the handle points up-left (-0.71,-0.71), blade points down-right (0.71,0.71). 

Now translate so the stick is positioned. The stick's center (local (250, 250)) should map to the badge center-ish, but let me position the stick so it's centered. Actually, let me map local center (250,250) to badge center (250,250). Then no translation needed (rotation about center). Wait, rotate(-45) alone rotates about origin (0,0). I need rotate about (250,250). So transform="rotate(-45 250 250)".

After rotate(-45 250 250):
- Local (250,100) [handle top] → rotates about (250,250). Relative to center: (0,-150). Rotate -45°: (x',y') = (cos(-45)*0 - sin(-45)*(-150), sin(-45)*0 + cos(-45)*(-150)) = (-sin(-45)*(-150), cos(-45)*(-150)) = (sin(45)*(-150)... let me just compute. 

Rotation by angle θ (SVG, clockwise positive) of point (x,y) about center (cx,cy):
x' = cx + (x-cx)cos θ - (y-cy) sin θ
y' = cy + (x-cx) sin θ + (y-cy) cos θ

θ = -45°, cos(-45)=0.707, sin(-45)=-0.707.
Handle top local (250,100): (x-cx, y-cy) = (0, -150).
x' = 250 + 0*0.707 - (-150)*(-0.707) = 250 - 106.05 = 143.95
y' = 250 + 0*(-0.707) + (-150)*0.707 = 250 - 106.05 = 143.95
So handle top → (144, 144). 

Blade local (250, 430) [bottom]: (0, 180).
x' = 250 + 0 - 180*(-0.707) = 250 + 127.3 = 377.3
y' = 250 + 0 + 180*0.707 = 250 + 127.3 = 377.3
So blade → (377, 377).

So after rotate(-45 250 250), the stick goes from (144,144) [handle top, upper-left] to (377,377) [blade, lower-right]. Both outside the owl? (144,144): owl head spans x=160-340 (head cx=250 r=90 → x=160-340), y=110-290. Point (144,144) is x=144 <160, so just outside the head's left edge, and y=144 within head's y-range. So it's to the left of the head, visible. ✓. (377,377): owl body spans x=146-354, y=230-450. Point (377,377) x=377>354, outside body right edge, visible. ✓.

The blade at (377,377) pointing... locally the blade pointed east (+x). After rotate(-45°), east (1,0) → (cos(-45)*1 - sin(-45)*0, sin(-45)*1 + cos(-45)*0) = (0.707, -0.707) = down... wait that's up-right? (0.707, -0.707): x positive (right), y negative (up). So up-right. Hmm, blade points up-right at the lower-right position. That means the blade points back toward the center/upper-right. 

Actually for a hockey stick, the blade pointing up-right while at lower-right... the flat part of the blade would face... let me not overthink. It'll look like a hockey stick. Let me just make the blade a clear hockey shape.

Hmm, but actually the blade direction matters for recognizability. Let me reconsider. In local coords, blade points east (right), flat bottom edge is at the bottom (the part that hits the puck on ice). After rotate(-45°), the blade's flat bottom edge (which was at bottom, -y direction normal) now points... 

Let me reconsider the blade geometry. Let me define the blade in local coords clearly:
- Shaft bottom at (250, 400).
- Blade extends east (right) from there.
- Blade bottom edge (puck-contact) at y=420 (below shaft bottom).
- Blade top edge at y=400.
- Blade toe (right end) curves up.

So blade is a horizontal bar from x=250 to x=320, y=400 to y=420, with the right end (toe) curving.

After rotate(-45°), this horizontal blade (pointing east) rotates to point up-right, and the blade's "thickness" direction (north-south) rotates to north-east/south-west. It'll look like a tilted hockey stick blade. Should be recognizable enough.

OK, I think I'm way overthinking the stick. Let me just draw it and move on. The key is it should look like a hockey stick. Let me make a clean hockey stick shape and place it tilted behind the owl.

Let me simplify: I'll draw the stick as:
1. A long shaft (thin rectangle) tilted.
2. A blade (the hook) at one end.

Let me define using a group with transform="rotate(-45 250 250)" and draw vertical shaft + right-pointing blade. Done.

Let me write the stick:
```
<g transform="rotate(-45 250 250)">
  <!-- shaft -->
  <rect x="244" y="95" width="12" height="305" rx="6" fill="#C68A34"/>
  <rect x="244" y="95" width="5" height="305" rx="3" fill="#8A5A1E" opacity="0.5"/>
  <!-- blade -->
  <path d="M 244 392 
           L 244 420 
           L 322 420 
           Q 334 420 334 402 
           L 334 392 
           Q 328 388 316 388 
           L 258 388 
           Q 244 388 244 392 Z"
        fill="#F4F6FC" stroke="#141A30" stroke-width="3" stroke-linejoin="round"/>
  <!-- blade bottom edge (tape) -->
  <line x1="246" y1="420" x2="330" y2="420" stroke="#141A30" stroke-width="2.5"/>
</g>
```

Wait, the blade connects to the shaft at x=244-256 (shaft is x=244 w=12, so x from 244 to 256). The blade path starts at (244,392) and the top edge goes to (258,388)... there's a slight mismatch (shaft right edge at x=256, blade top starts at x=258). Let me align: blade should connect to shaft bottom. Shaft bottom is at y=400 (y=95 to 400). Let me make blade start at y=392 (just below shaft) and connect.

Let me adjust: shaft y=95 to y=395 (height 300). Blade at y ~392-420.

Let me redefine:
- Shaft: rect x=244 y=95 w=12 h=300 (to y=395), rx=6.
- Blade: connects at bottom of shaft (y≈395), extends east.

Blade path:
```
M 244 392
L 244 418
L 320 418
Q 332 418 332 401
L 332 393
Q 327 388 315 388
L 256 388
Z
```
Hmm, let me make it cleaner. The blade:
- Left side (heel): from (246,390) down to (246,416)
- Bottom: from (246,416) right to (318,416)
- Toe: from (318,416) curve up to (320,396)
- Top: from (320,396) left back to (254,390)
- Close to heel.

```
M 246 390 L 246 416 L 318 416 Q 331 416 330 398 L 330 393 Q 325 388 313 388 L 256 388 Z
```

Let me just go with a reasonable blade. I'll add stroke for outline.

OK, let me also reconsider: after rotate(-45 250 250), the blade is at lower-right (377,377) pointing up-right. The flat bottom edge of the blade (was at y=416, the "down" side) — after rotation, "down" (-y... no, +y in screen is down) direction... the blade bottom was at larger y (416 > 390), i.e., "south." After rotate(-45°), south (+y) direction rotates. South (0,1) rotated by -45°: (cos(-45)*0 - sin(-45)*1, sin(-45)*0 + cos(-45)*1) = (-sin(-45), cos(-45)) = (0.707, 0.707) = south-east (down-right). So the blade's flat bottom edge faces down-right. That means the flat puck-contact surface faces down-right (toward the ground if the stick were resting). That's actually correct for a hockey stick! Good.

Alright, I'm confident enough. Let me finalize.

Actually, let me reconsider whether the blade should be at the lower-right or if it's cleaner to have the handle at lower and blade... no, handle at top, blade at bottom is standard. Handle top at (144,144) upper-left, blade at (377,377) lower-right. Good.

Hmm, wait, but the owl's head is around (250,200) and body (250,340). The stick passes through (250,250) center area, behind the owl's midsection. The handle from (144,144) to (250,250) passes behind the head's lower-left. The blade from (250,250) to (377,377) passes behind the body's lower-right. Both ends stick out. Good.

Let me now also double check the owl doesn't completely cover the stick in a weird way. The stick is behind, so it's fine — it's a background element adding to the design.

Let me write the final SVG. Let me assemble all parts in order:
1. defs (gradients)
2. Badge circles
3. Hockey stick (behind)
4. Owl (body, belly, feathers, wings, ears, head, eyes, beak, feet)
5. Text

Let me write it out cleanly.

Actually, I realize I should double-check the text readability and that the arc text won't overlap the owl. Top text at radius 184, around the top. The owl head top is at y=110 (cy=200, r=90). The top text arc at radius 184 passes through (250, 66) at the very top. The text "OWAYO" is centered at top. At the top, the text is around y=66±text height. The owl head top is at y=110. So text (around y=40-70) is above the head (y=110). No overlap. Good.

Bottom text at radius 184 passes through (250,434). The owl feet go to y=466, and body bottom at y=450. The bottom text is at radius 184 (y=434 at center), and extends upward (toward center) into the circle. So the text occupies from y=434 up to ~y=434-40=394 (for 40px cap height, roughly the text baseline at 434, extending up 40px to 394). The owl body at that x-range (center) spans y=230-450. So the text (y=394-434) would overlap the owl body (which is at y up to 450)! 

Hmm, that's a problem. The bottom text would overlap the owl's lower body/feet.

Let me reconsider. The bottom text baseline is at radius 184 (y=434 at center x). The text extends upward (toward center) by about the cap height (~30px for 40px font). So text spans y≈394 to 434. The owl body at center x spans y=230-450. So yes, overlap in y=394-434.

But wait, the owl body at the center is the belly area. The text would be drawn over the belly. That looks bad.

Solutions:
- Move the bottom text to a smaller radius? No, that's closer to center, worse.
- Make the owl shorter so its bottom is above y=394. But then the badge looks odd.
- Put the text outside a separate area.
- Reduce owl size.
- Move text arc to larger radius (closer to the ring) so it's below the owl. But larger radius at the bottom means larger y (further down), e.g., radius 200 → y=450. Even worse (more overlap, and might exceed badge).

Hmm. The issue is the owl is tall and reaches down to y=450, while the bottom text needs to be near the bottom ring (y≈450+).

Let me reconsider the whole layout. Maybe the owl should be smaller/higher, leaving room at the bottom for text. Or the text should be in an arc that's above the owl's body.

Alternative: Make the owl smaller and positioned higher, so there's room at the bottom for "EURLERS" text, and room at top for "OWAYO".

Let me scale down the owl and move it up a bit.

Let me reconsider dimensions:
- Badge radius 230, center (250,250).
- Top text arc: radius ~185, centered at top.
- Bottom text arc: radius ~185, centered at bottom.
- Owl: should fit between the text arcs, i.e., roughly y from 130 to 380, centered around y=255.

Let me make the owl:
- Head: cx=250, cy=195, r=78. Top at y=117.
- Body: cx=250, cy=310, rx=80, ry=90. Bottom at y=400. Hmm still reaches 400.

The bottom text at radius 185 is at y=435 (center) extending up to ~405. Owl body bottom at 400 overlaps.

Let me make the owl shorter. Body ry=75, cy=300 → bottom at 375. Head cy=190 r=72 → top at 118.
- Belly feathers and feet: feet at bottom of body ~y=375+15=390.

Bottom text baseline at y=435, extending up to ~405. Still overlaps feet (390-390) and belly bottom (375). The text (405-435) vs body (up to 375) — if body bottom is 375 and text starts at 405, no overlap! Let me make sure body bottom is well above 405.

Let me set body: cx=250, cy=300, rx=78, ry=78 → bottom at 378. Feet from y=378 to y=395. Text baseline at 435, text height ~30, so text spans 405-435. Feet (378-395) and text (405-435): small gap, no overlap. 

But wait, the feet are at x≈220-280 (center), and the text "EURLERS" is centered at bottom (x=250). At the bottom center, the text is directly below the feet. If feet bottom at 395 and text top at 405, there's a 10px gap. OK but tight. Let me increase gap by making text baseline a bit lower or owl a bit higher.

Alternatively, reduce font size for bottom text or increase badge. Let me just tune.

Hmm, let me reconsider. Maybe it's cleaner to NOT put text on the bottom arc, and instead put the whole team name "OWAYO EURLERS" as a single line below the owl, or split "OWAYO" top arc and "EURLERS" as a straight line at the bottom.

Actually, a common clean approach: curved "OWAYO" at top, and "EURLERS" as a straight bold line at the bottom (below the owl, within the badge). But the straight line at the bottom would still be near the owl's feet.

Let me reconsider. Maybe put the owl in the upper portion and the text in the lower portion, with the badge being taller. Or accept some overlap with the text having a contrasting stroke so it's readable over the owl.

Option: Give the text a dark outline/stroke so it's readable even over the owl. That's a common technique. Let me add a dark stroke to the text (or a subtle drop shadow) so it's legible over any background.

Actually, the cleanest solution: make the owl smaller and higher, and put both text arcs (top and bottom) clearly. Let me carefully size things.

Let me define the badge with center (250, 270) instead of (250,250), making it taller, viewBox 500x560. Then:
- Badge center (250, 270), radius 225. Top of badge at y=45, bottom at y=495.
- Top text arc radius 180: through (250, 90).
- Bottom text arc radius 180: through (250, 450).
- Owl: head cy=185 r=75 (top at 110), body cy=300 rx=75 ry=80 (bottom at 380), feet to 395.

Text top: baseline ~radius 175, at (250, 95), text extends up to ~65. Head top at 110. Gap ✓.
Text bottom: baseline at (250, 445), extends up to ~415. Feet bottom at 395. Gap (395 to 415) = 20px ✓.

This works better with a taller badge. Let me use viewBox 0 0 500 560, badge center (250, 275).

Let me recompute text arcs with center (250,275):
- Top: M 70 275 A 180 180 0 0 1 430 275 (through (250, 95))
- Bottom: M 70 275 A 180 180 0 0 0 430 275 (through (250, 455))

Owl (centered around x=250):
- Ears: around y=120-160
- Head: cx=250 cy=190 r=78 (top 112, bottom 268)
- Eyes: cy=190
- Beak: cy~220
- Body: cx=250 cy=315 rx=78 ry=82 (top 233, bottom 397)
- Belly: cx=250 cy=325 rx=55 ry=62
- Wings: sides
- Feet: y~397-415

Text bottom baseline at (250,455), extends up to ~425. Feet bottom at 415. Gap 10px. Tight but OK. Let me make feet a bit shorter or body a bit shorter.

Let me set body cy=310 ry=78 → bottom 388. Feet 388-405. Text baseline 455, extends up to 425. Gap 20px. Good.

Head cy=185 r=76 → top 109. Text top baseline at (250,95) extends up to 65. Gap from 65 to 109 = 44px. Good.

Alright, let me also reconsider the stick with the new center (250,275). The stick rotate center should be (250,275) now. Let me redo:
rotate(-45 250 275):
- Handle top local (250,95): relative (0,-180). Rotated -45°: 
  x' = 250 + 0 - (-180)*(-0.707) = 250 - 127.3 = 122.7
  y' = 275 + 0 + (-180)*0.707 = 275 - 127.3 = 147.7
  → (123, 148). Within badge (radius 225 from (250,275): distance = sqrt(127²+127²)=180 <225) ✓.
- Blade local (250,430): relative (0,155). Rotated -45°:
  x' = 250 + 0 - 155*(-0.707) = 250 + 109.6 = 359.6
  y' = 275 + 0 + 155*0.707 = 275 + 109.6 = 384.6
  → (360, 385). Distance from center: sqrt(110²+110²)=155 <225 ✓.

So handle top at (123,148), blade at (360,385). Both outside the owl? 
- (123,148): owl head spans x=174-326 (cx=250 r=76). x=123<174, outside head. But y=148 is within head's y-range (109-268). So (123,148) is to the left of the head, visible. ✓.
- (360,385): owl body spans x=172-328 (rx=78). x=360>328, outside body. y=385 within body y-range (232-388). So to the right of body, visible. ✓.

Good.

Now the stick shaft from (123,148) to (360,385) passes behind the owl. Good.

Let me finalize the stick local coordinates (before rotation) with center-based drawing. Actually, I'll just draw it vertically centered at (250, 275) in local coords, then rotate.

Local stick:
- Shaft: rect x=244 y=100 w=12 h=300 (y=100 to 400), rx=6. Wait, I want the shaft to span nicely. Let me make shaft from y=100 to y=400 (local), centered around (250,250) local... but badge center is (250,275). Let me just make the shaft long enough.

Hmm, let me reconsider. In local coords (before rotation), I'll draw the stick vertically. The rotation is about (250,275). Let me place the stick symmetric about y=275 locally.

Shaft: y from 100 to 430 (centered at 265, close enough). Actually let me center at 275: y from 100 to 450 (center 275). Length 350.
- Shaft: rect x=244 y=100 w=12 h=350 rx=6.
- Blade at bottom (y=450), pointing east.

After rotate(-45 250 275):
- Shaft top (250,100): rel (0,-175). x'=250-175*0.707=250-123.7=126.3, y'=275-123.7=151.3 → (126,151).
- Shaft bottom/blade (250,450): rel (0,175). x'=250+123.7=373.7, y'=275+123.7=398.7 → (374,399).

Blade at (374,399). Distance from center sqrt(124²+124²)=175<225 ✓. x=374 >328 (body right), visible ✓.

OK let me just go with shaft y=100 to 440, blade at bottom.

Blade local (pointing east, at bottom y≈435):
- Shaft bottom at y=435 (shaft y=100 to 435).
- Blade: from (246,430) to (325,430) area, with the hook shape.

Let me define blade:
```
M 246 428
L 246 456
L 322 456
Q 335 456 335 437
L 335 428
Q 330 423 318 423
L 258 423
Z
```
Hmm, let me make the blade cleaner. The blade is a horizontal bar:
- Top edge: y=426, from x=246 (heel) to x=320 (toe)
- Bottom edge: y=452, from x=246 to x=322 (toe curves up)
- Heel: left edge x=246, from y=426 to y=452
- Toe: right side curves from (322,452) up to (324,430)

Path:
```
M 246 426
L 246 452
L 320 452
Q 334 452 333 434
L 333 428
Q 328 424 316 424
L 256 424
Z
```
Wait, I need the top edge to connect to the shaft. Shaft bottom is at x=244-256, y=435. The blade top edge at y=424-426, x=256-316. There's a gap between shaft bottom (y=435) and blade top (y=424). Let me make the blade connect directly to the shaft.

Let me set shaft y=100 to y=428 (bottom at 428). Blade top edge at y=424 (slightly above shaft bottom to overlap) or y=428.

Let me simplify: shaft bottom at y=426. Blade:
```
M 246 426
L 246 452
L 318 452
Q 332 452 331 433
L 331 426
Q 326 422 315 422
L 254 422
Z
```
The top edge from (254,422) to (315,422)... but shaft bottom is at y=426, x=244-256. The blade top-left is at (254,422), near shaft bottom-right. Close enough; they'll connect visually. Let me add a small connection.

Actually, let me make the blade's left part connect to the shaft properly. The shaft is x=244-256. The blade heel should be at x=244-256. Let me make the blade:
```
M 244 424       (heel top-left, connects to shaft)
L 244 452       (heel down)
L 318 452       (bottom to toe)
Q 332 452 331 434   (toe curve up)
L 331 425       (toe top)
Q 326 421 315 421   (top of blade back toward heel)
L 256 421       (top of blade to heel)
Z
```
The top edge from (256,421) to (315,421). Shaft bottom at y=426 (shaft y=100-426). So blade top (y=421) is slightly above shaft bottom (y=426). They overlap in the region x=244-256, y=421-426. Good, connected.

Let me finalize with this. I'll add stroke.

Hmm, this is getting really detailed. Let me just write it and trust it looks like a hockey stick.

Let me reconsider if I even need the blade to be super accurate. A hockey stick is recognizable by: long shaft + a curved blade at the end. My shape has that. Good.

Let me write the final SVG now. I'll include:
- Gradients
- Badge (2 circles)
- Stick (behind)
- Owl
- Text

Let me also add small decorative stars or dots between text and owl for flair. Maybe two small 4-pointed stars flanking the owl or between text. Let me add small stars near the text arcs. Actually, let me add two small stars on either side of the owl's head, near the text. Or skip. Let me add subtle stars for sportiness. I'll add 2 small 4-point stars at the sides (around x=70,y=275 area and x=430,y=275). Hmm, those are at the text start/end points. Let me place small stars at left and right middle, like separators between top and bottom text. 

Actually, let me place two small stars: one at left (~75,275) and one at right (~425,275), separating the "OWAYO" top text from "EURLERS" bottom text. These sit at the sides of the badge. Nice touch.

Let me define a 4-point star path (sparkle):
```
<path d="M 0 -8 L 2 -2 L 8 0 L 2 2 L 0 8 L -2 2 L -8 0 L -2 -2 Z" fill="#F7B400"/>
```
Then use <use> or inline with transform.

Let me place at (72, 275) and (428, 275) with a scale.

OK let me write everything now.

Let me reconsider colors for final:
- Badge fill: #17224A (deep navy)
- Outer ring: #F7B400 (gold), width 6
- Inner ring: #4A60A0, width 2
- Owl body gradient: #6279C4 → #2F4588
- Head gradient: radial #7C92D6 → #3F5797
- Belly: #EDF0FB gradient to #D0D7EF
- Belly feather lines: #AEB8DE
- Wings: #2C407F
- Ears: #3F5797
- Eye rings: #F7B400
- Eye white: #FDFDFD
- Pupils: #141A30
- Highlights: #FFFFFF
- Beak: #F29300
- Feet: #F29300
- Shaft: #C68A34 with #8A5A1E shading
- Blade: #F4F6FC with #141A30 stroke
- Text: #F7B400
- Stars: #F7B400

Let me write it.

Actually, for the belly feather lines, let me make them look like little scallops (owls have scaly bellies). I'll draw arcs. Let me refine:
```
<path d="M 218 300 Q 235 316 252 300" .../>
<path d="M 250 300 Q 267 316 284 300" .../>
<path d="M 214 332 Q 235 350 256 332" .../>
<path d="M 254 332 Q 275 350 296 332" .../>
<path d="M 220 366 Q 240 382 260 366" .../>
<path d="M 258 366 Q 278 382 298 366" .../>
```
These are rows of upward-curving arcs (like fish scales / owl belly feathers). Good.

Wait, owl belly feathers are usually V-shaped or scale-like. Upward arcs (∩ shape, opening down) look like scales. Let me use arcs that curve like a frown (∩) — no, scales look like scales (overlapping arcs opening upward, like ⋀ repeated, or like scallop shells ∪). Let me use ∪-ish or half-circles. Let me just use gentle arcs; it'll read as feather texture.

Let me use arcs curving downward (like a smile ∪) which look like scale rows. Actually, let me use a mix; it's texture. I'll go with arcs.

Let me finalize. Writing now.

Let me reconsider eye position relative to head. Head cx=250 cy=185 r=76. Eyes should be in the upper-middle of the head. Let me place eyes at cy=188, x=213 and 287 (offset 37 from center). Eye radius 40 (white), ring radius 44. Pupils radius 16.

Wait, head r=76 spans x=174-326. Eyes at x=213 and 287, within. Good. Eye white r=40 spans x=173-253 (left eye) — that reaches to x=173, near head edge (174). Might slightly overflow. Let me reduce eye white to r=37. Ring r=41.

Let me set:
- Eye ring: r=42, stroke gold width 8 → outer radius 46. Left at x=213: spans 167-259. Head left edge at 174. So the ring slightly overflows head on the left (167<174). Hmm. Let me move eyes inward: x=215 and 285. Then left eye ring spans 169-261, still slightly over 174? 169<174, overflow 5px. Let me reduce ring outer to fit. Head left edge 174. Eye center must be ≥ 174+46=220 for the ring to fit. So eye center x ≥ 220. Let me place eyes at x=218 and 282. Then left ring spans 172-264. 172<174, still 2px over. Close enough, or reduce ring.

Let me just place eyes at x=218 and 282, ring r=40 (outer 44 with stroke 8), so left ring spans 174-262. Fits exactly at head edge 174. 

Hmm, let me make head a bit bigger or eyes a bit smaller to be safe. Let me make head r=80 (spans 170-330). Eyes at x=218/282, ring r=40 outer 44: left spans 174-262. Head edge 170. So ring at 174 is inside head (170). ✓ 4px margin. Good.

Let me set head r=80, cy=185. Eyes x=218,282, ring r=40 (stroke width 8 → outer 44), white r=36, pupil r=15.

Beak: below eyes, at center. Points: (240,218) (260,218) (250,242). Orange.

Let me reconsider: eyes at cy=188, beak at cy~230. Head spans y=105-265. Beak at y=218-242, within head. Good.

Ears: at top of head, around y=105-140. Head top at y=105. Ears emerge from top.
- Left ear: polygon (205,118) (178,68) (228,108). 
- Right ear: (295,118) (322,68) (272,108).
These are above the head (y<105 partly). Good, like owl tufts.

Body: cx=250, cy=315, rx=80, ry=85. Spans x=170-330, y=230-400.
Belly: cx=250, cy=325, rx=55, ry=62. Spans y=263-387.
Wings: 
- Left: M 172 295 Q 128 340 150 410 Q 174 388 186 330 Z
- Right: M 328 295 Q 372 340 350 410 Q 326 388 314 330 Z
Feet: at body bottom y=400.
- Left foot: from (228,400)
- Right foot: from (272,400)
Let me draw feet as 3-toed shapes.

Let me draw feet as paths (orange, stroke):
- Left: M 228 400 L 218 420, M 228 400 L 232 424, M 228 400 L 246 418
- Right: M 272 400 L 254 418, M 272 400 L 268 424, M 272 400 L 282 420

Hmm, these are just lines. Let me add small circles at toe tips or make them thicker. Let me use stroke-width 5, round caps. Good enough for feet.

Actually, let me make feet a bit more like claws with a slight curve. Lines are fine.

Now text:
- Top: "OWAYO", font-size 42, at arc radius 178.
- Bottom: "EURLERS", font-size 42, at arc radius 178.

Arc paths (center 250,275, radius 178):
- Top: M 72 275 A 178 178 0 0 1 428 275
- Bottom: M 72 275 A 178 178 0 0 0 428 275

Let me verify top text doesn't overlap head. Top arc at (250,97). Text baseline at 97, extends up ~30px to 67. Head top at 105. Gap 67-105 = 38px. ✓.

Bottom text baseline at (250,473), extends up ~30px to 443. Feet bottom at 424. Gap 424-443 = 19px. ✓. Good.

Wait, bottom arc radius 178 from center (250,275): bottom point at y=275+178=453, not 473. Let me recompute. Center y=275, radius 178, bottom point y=275+178=453. So baseline at y=453, extends up to 423. Feet bottom at 424. Overlap! (feet to 424, text from 423). Tight overlap.

Let me increase the gap. Options: reduce feet length (feet to 415) or move text down (larger radius). Let me make radius 182 → bottom at 457, text up to 427. Feet to 424. Overlap 3px. Still tight.

Let me shorten the feet. Feet from y=400 to y=416 (shorter). Then text (423-453) vs feet (400-416): gap 7px. OK.

Or make body shorter. Let me make body ry=78, cy=312 → bottom 390. Feet from 390 to 408. Then text (423-453) vs feet (390-408): gap 15px. 

Let me set body cy=312, ry=80 → bottom 392. Feet 392-412. Text baseline 453, up to 423. Gap 11px. OK.

Hmm, let me just make the text a bit smaller (font-size 38) and reduce its height, and shorten feet. Let me finalize with:
- Body: cy=312, rx=78, ry=80 (bottom 392)
- Feet: 392 to 412
- Text: font-size 38, baseline at bottom arc (y=453), extends up to ~425. Gap ~13px. Good.

Actually, let me reconsider — maybe I'm overcomplicating. Let me just make the owl compact and give clear margins. Let me also reconsider using a slightly different approach for the bottom text: put it on a straight baseline below the owl but inside the badge. But curved is nicer. Let me keep curved and just size appropriately.

Let me write the final SVG. I'll tune as I go.

Let me reconsider the whole thing one more time and just produce clean code.

Final layout:
- viewBox 0 0 500 560
- Badge center (250, 278), radius 228. (Let me use 278 to give a bit more bottom room.)

Hmm, let me recompute with center (250,278):
- Top arc bottom of text area: y=278-178=100. Text up to 70. Head top 105. Gap 35. ✓
- Bottom arc: y=278+178=456. Text up to 428. Feet need to be above 428, say feet to 412. Gap 16. ✓

Owl:
- Head: cy=188, r=78 (top 110, bottom 266)
- Body: cy=315, rx=78, ry=78 (top 237, bottom 393)
- Feet: 393 to 413

Wait, head bottom 266 and body top 237 overlap (good, merged). 

Let me set:
- Head: cx=250 cy=188 r=78
- Body: cx=250 cy=318 rx=78 ry=76 (bottom 394)
- Belly: cx=250 cy=328 rx=53 ry=58 (bottom 386)
- Feet: from y=394 to 414

Text bottom baseline at y=456, up to 428. Feet to 414. Gap 14. ✓.

OK good. Let me write it.

Actually, let me reconsider the vertical centering. Badge center (250,278), but the visual content (owl) is centered around y=(188+318)/2 ≈ 253, plus feet to 414. The owl is a bit low. Let me shift owl up slightly. Head cy=182, body cy=310. Owl center ~246. Text arcs at radius 178 from (250,278). Hmm, the text is centered at 278, owl at 246. Slight mismatch but OK since text follows the circle.

Let me not over-optimize. Let me write it.

Let me write the final code:

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 500 560" width="500" height="560">
  <defs>
    <linearGradient id="bodyGrad" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#657BC8"/>
      <stop offset="1" stop-color="#30478C"/>
    </linearGradient>
    <radialGradient id="headGrad" cx="0.42" cy="0.35" r="0.75">
      <stop offset="0" stop-color="#8298DC"/>
      <stop offset="1" stop-color="#415A9C"/>
    </radialGradient>
    <linearGradient id="bellyGrad" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#F2F5FD"/>
      <stop offset="1" stop-color="#D4DBF2"/>
    </linearGradient>
  </defs>

  <!-- Badge -->
  <circle cx="250" cy="278" r="230" fill="#17224A"/>
  <circle cx="250" cy="278" r="216" fill="none" stroke="#F7B400" stroke-width="7"/>
  <circle cx="250" cy="278" r="205" fill="none" stroke="#4A62A6" stroke-width="2.5"/>

  <!-- Hockey stick -->
  <g transform="rotate(-45 250 278)">
    <rect x="244" y="104" width="12" height="330" rx="6" fill="#C68A34"/>
    <rect x="244" y="104" width="5" height="330" rx="3" fill="#8A5A1E" opacity="0.55"/>
    <path d="M 244 430 L 244 458 L 320 458 Q 334 458 333 439 L 333 430 Q 327 424 315 424 L 256 424 Z"
          fill="#F4F6FC" stroke="#141A30" stroke-width="3" stroke-linejoin="round"/>
    <line x1="246" y1="458" x2="328" y2="458" stroke="#141A30" stroke-width="2.5"/>
  </g>

  <!-- Owl -->
  <!-- body -->
  <ellipse cx="250" cy="318" rx="78" ry="76" fill="url(#bodyGrad)" stroke="#202C5C" stroke-width="3"/>
  <!-- belly -->
  <ellipse cx="250" cy="330" rx="53" ry="58" fill="url(#bellyGrad)"/>
  <!-- belly feathers -->
  <g stroke="#AEB8DE" stroke-width="3.5" fill="none" stroke-linecap="round">
    <path d="M 220 306 Q 237 322 254 306"/>
    <path d="M 252 306 Q 269 322 286 306"/>
    <path d="M 216 338 Q 237 356 258 338"/>
    <path d="M 256 338 Q 277 356 298 338"/>
    <path d="M 222 372 Q 241 388 260 372"/>
    <path d="M 258 372 Q 277 388 296 372"/>
  </g>
  <!-- wings -->
  <path d="M 174 292 Q 130 336 152 408 Q 176 386 188 326 Z" fill="#2C407F" stroke="#202C5C" stroke-width="3"/>
  <path d="M 326 292 Q 370 336 348 408 Q 324 386 312 326 Z" fill="#2C407F" stroke="#202C5C" stroke-width="3"/>
  <!-- ears -->
  <path d="M 206 120 L 178 68 L 230 110 Z" fill="#415A9C" stroke="#202C5C" stroke-width="3" stroke-linejoin="round"/>
  <path d="M 294 120 L 322 68 L 270 110 Z" fill="#415A9C" stroke="#202C5C" stroke-width="3" stroke-linejoin="round"/>
  <!-- head -->
  <circle cx="250" cy="188" r="78" fill="url(#headGrad)" stroke="#202C5C" stroke-width="3"/>
  <!-- eyes -->
  <circle cx="218" cy="190" r="42" fill="none" stroke="#F7B400" stroke-width="8"/>
  <circle cx="282" cy="190" r="42" fill="none" stroke="#F7B400" stroke-width="8"/>
  <circle cx="218" cy="190" r="36" fill="#FDFDFD"/>
  <circle cx="282" cy="190" r="36" fill="#FDFDFD"/>
  <circle cx="221" cy="192" r="16" fill="#141A30"/>
  <circle cx="279" cy="192" r="16" fill="#141A30"/>
  <circle cx="212" cy="183" r="6" fill="#FFFFFF"/>
  <circle cx="288" cy="183" r="6" fill="#FFFFFF"/>
  <!-- beak -->
  <path d="M 240 218 L 260 218 L 250 246 Z" fill="#F29300" stroke="#141A30" stroke-width="2.5" stroke-linejoin="round"/>
  <!-- feet -->
  <g stroke="#F29300" stroke-width="5.5" fill="none" stroke-linecap="round">
    <path d="M 228 392 L 218 412"/>
    <path d="M 233 394 L 235 416"/>
    <path d="M 238 392 L 252 410"/>
    <path d="M 262 392 L 248 410"/>
    <path d="M 267 394 L 265 416"/>
    <path d="M 272 392 L 282 412"/>
  </g>

  <!-- Stars -->
  <g fill="#F7B400">
    <path d="M 74 278 L 78 272 L 82 278 L 88 282 L 82 286 L 78 292 L 74 286 L 68 282 Z"/>
    <path d="M 426 278 L 430 272 L 434 278 L 440 282 L 434 286 L 430 292 L 426 286 L 420 282 Z"/>
  </g>

  <!-- Text -->
  <text font-family="Arial Black, Arial, Helvetica, sans-serif" font-weight="bold" font-size="40" letter-spacing="5" fill="#F7B400">
    <textPath d="M 72 278 A 178 178 0 0 1 428 278" startOffset="50%" text-anchor="middle">OWAYO</textPath>
  </text>
  <text font-family="Arial Black, Arial, Helvetica, sans-serif" font-weight="bold" font-size="40" letter-spacing="5" fill="#F7B400">
    <textPath d="M 72 278 A 178 178 0 0 0 428 278" startOffset="50%" text-anchor="middle">EURLERS</textPath>
  </text>
</svg>
```

Wait, I need to double-check the stars position. At (74,278) and (426,278) — these are at the left and right middle of the badge, at the same y as center. The text arcs pass through these points? Top arc at (72,278) is the start point (left), and bottom arc also starts at (72,278). So the stars at (74,278) and (426,278) are exactly where the text starts/ends on the sides. They'll be between the top and bottom text on the sides. Good, they act as separators. But they might overlap the text start. Let me place them slightly outside or between. Actually at (74,278), the top text "OWAYO" starts there (going up-right) and bottom text "EURLERS" starts there (going down-right). The star in the middle separates them. Good.

Hmm, but the star at (74,278) — is that inside the badge? Badge radius 230, center (250,278). Distance from center to (74,278) = 176 < 230. Inside. And outside the inner ring (205)? 176<205, so it's inside the inner ring, near the left edge area. The text also is around there. The star sits at the left, between texts. Should be fine.

Let me reconsider star size — my star path spans from x=68 to x=88 (20px wide) and y=272 to 292 (20px tall). At (74,278) center... wait, my star path isn't centered at (74,278). Let me check: the path d="M 74 278 L 78 272 ..." — the star's center is around (78, 282)? Let me recompute. The star points: top (78,272), right (88,282), bottom (78,292), left (68,282). Center = ((78+78+78+68)/4... average of extremes: x from 68-88, center 78; y from 272-292, center 282). So star center is (78,282), not (74,278). Let me reposition. I'll translate the star so its center is at (74,278). Let me redefine the star centered at origin then translate.

Star centered at origin (pointing up):
- Top: (0,-9)
- Upper-right: (3,-3)
- Right: (9,0)
- Lower-right: (3,3)
- Bottom: (0,9)
- Lower-left: (-3,3)
- Left: (-9,0)
- Upper-left: (-3,-3)

Path: M 0 -9 L 3 -3 L 9 0 L 3 3 L 0 9 L -3 3 L -9 0 L -3 -3 Z

Then place with transform="translate(74,278)" and scale.

Let me use:
```
<g transform="translate(74 278)" fill="#F7B400">
  <path d="M 0 -9 L 3 -3 L 9 0 L 3 3 L 0 9 L -3 3 L -9 0 L -3 -3 Z"/>
</g>
<g transform="translate(426 278)" fill="#F7B400">
  <path d="M 0 -9 L 3 -3 L 9 0 L 3 3 L 0 9 L -3 3 L -9 0 L -3 -3 Z"/>
</g>
```

Good.

Now let me reconsider the stick once more. After rotate(-45 250 278):
- Shaft top local (250,104): rel (0,-174). x'=250 -174*0.707=250-123=127, y'=278-123=155 → (127,155).
- Shaft bottom local (250,434): rel (0,156). x'=250+110=360, y'=278+110=388 → (360,388).

Wait, shaft y=104 to 434 (height 330). Bottom at 434. Blade attached at y=430-458 (extends below shaft bottom). Blade local (250,458): rel (0,180). x'=250+127=377, y'=278+127=405 → (377,405).

Blade at (377,405). x=377 > body right (330), visible ✓. y=405, within badge. Good.

Shaft top (127,155): x=127 < head left (172), visible ✓.

Good.

But wait, the blade extends below the shaft (y=430-458 locally), so after rotation it's at the lower-right, pointing... the blade's flat bottom edge (y=458, the +y/down side) rotates to face down-right (as computed earlier). Good.

Now, the blade is at (377,405) area, pointing up-right (the blade's long axis was east, now up-right after -45°). The flat surface faces down-right. Looks like a hockey stick. 

Let me double-check the shaft and blade connect. Shaft bottom at local (250,434). Blade top at local y=424-430, x=256-315. Shaft bottom center x=250. Blade left edge x=244. So blade overlaps shaft bottom. After rotation they rotate together, so they stay connected. Good.

Hmm wait, in local coords, the shaft is x=244-256, and the blade path starts at x=244 (left edge) going to x=315. The blade top edge is at y=424, and shaft bottom at y=434. So the blade is slightly above the shaft bottom in local coords, but the blade left edge (x=244) aligns with shaft left edge. They connect at the junction. After rotation, connected. Good.

Let me reconsider: is the blade too far right / does it look like it continues the shaft? The shaft direction (after rotation) is up-left to down-right (from (127,155) to (360,388)). The blade continues in that direction and curves. Should look fine.

Alright. Let me also add a subtle inner shadow or make the owl pop. Let me add a thin dark stroke to the head and body (already have). Good.

Let me reconsider the eyes — gold rings with white centers and dark pupils. The pupils at (221,192) and (279,192), slightly inward and down from eye centers (218,190) and (282,190). Left pupil x=221 > eye center x=218, so pupil is slightly to the right (toward center) — both pupils look inward. Good, gives a slightly cross-eyed cute look. Highlights at (212,183) and (288,183) — upper-left of pupils. Left highlight x=212 < pupil 221, so up-left. Good.

Now let me reconsider: the gold eye rings (r=42, stroke 8 → outer 46) at (218,190): left spans x=172-264, y=144-236. Head r=78 at (250,188): x=172-328, y=110-266. Left eye ring left edge x=172 = head left edge 172. Fits exactly. Good. Right eye ring right edge x=328 = head right edge. Fits. Good.

Eye white r=36 at (218,190): x=182-254. Within ring. Good.
Pupil r=16 at (221,192): x=205-237. Within white. Good.

Beak at (240,218)-(260,218)-(250,246). Between the eyes, below. Eyes at y=190, beak at y=218-246. Head spans to y=266. Beak within. Good.

Ears: (206,120)(178,68)(230,110) left. Head top at y=110. Ear tip at y=68 (above head). Good, tufts sticking up.

Body: cy=318, rx=78, ry=76. Top y=242, bottom y=394. Head bottom y=266. Overlap 242-266. Good merge.

Belly: cy=330, rx=53, ry=58. y=272-388. Within body. Good.

Feathers at y=306,338,372. Within belly (272-388). Good.

Wings: left M174,292 ... to (152,408). Body left edge at x=172 (cy=318). Wing starts at x=174 (on body edge) and curves out to x=130 then back to 188. So wing sticks out to the left of the body. Good. Bottom at y=408, below body bottom (394). Slightly below. OK.

Feet: from y=392 (body bottom area) to 416. Below body. Good.

Text bottom baseline at y=278+178=456. Text extends up to ~428 (for font-size 40, cap height ~29). Feet to 416. Gap 12px. ✓.

Text top baseline at y=278-178=100. Extends up to ~71. Head top 110. Gap 39px. ✓.

Stars at (74,278) and (426,278). At the sides. The text "OWAYO" top arc starts at (72,278) and "EURLERS" bottom arc starts at (72,278). The star at (74,278) is right there. It might overlap the text starts. Let me move stars slightly inward or make them smaller, or accept. Actually, the text starts at (72,278) and curves away (up for top, down for bottom). The star at (74,278) is between them. The "O" of OWAYO starts at (72,278) and the "S" of EURLERS starts at (72,278) going down. The star sits at the junction. It might slightly overlap the first letters. Let me reduce star size (scale 0.8) and place at (76,278) and (424,278). Or move to (80,278). Let me place stars at (80,278) and (420,278), scaled 0.85. Should be clear of text.

Hmm, actually the text starts exactly at the arc endpoints (72,278) and (428,278). The star at (74,278) would be right at the start. Let me place stars a bit further from the text, at (85,278) and (415,278), scaled ~0.8. Let me verify these are inside the badge and not overlapping owl. (85,278): distance from center (250,278) = 165 <205 (inner ring). Inside. Not overlapping owl (owl left edge ~130-172). 85<130, clear. Good.

Actually, let me reconsider — do I even need the stars? They add a bit of flair. Let me keep them but place them well. Let me put them at (88,278) and (412,278), scale 0.8.

Hmm, let me reconsider. Actually the stars at the sides between the text might look cluttered. Let me instead place two small stars above the owl or as part of the design. Or just skip the stars for cleanliness. 

Let me keep them minimal — two small stars flanking, it looks sporty. Let me finalize at (90,278) and (410,278), scale 0.8.

Wait, I realize the text might not have enough clearance if stars are too close. Let me just place stars clearly and move on.

Let me reconsider the font. "Arial Black" might not be available everywhere, but it's common. Let me use "Arial, Helvetica, sans-serif" with font-weight bold, which is safer. Actually Arial Black gives a chunky sporty look. Let me use "Arial Black, Arial, sans-serif" as fallback.

Let me also reconsider letter-spacing for the curved text — it should look good. 5px is fine.

Let me finalize and write the SVG. Let me also add a subtle drop shadow to the owl for depth? Optional. Let me add a slight shadow to make it pop. Actually, let me keep it flat/clean (modern logo style). No shadow.

Let me write the final version.

Oh wait, I should double check: the user wants "Eishockeyschläger" = ice hockey stick. My stick has a shaft and a blade — that's a hockey stick. Good. (Ice hockey sticks have a blade, unlike field hockey which has a different curve. My blade is flat with a slight toe curl, typical of ice hockey.) Good.

Also "Eule" = owl. My design is an owl. Good.

Let me also make sure I include both elements clearly. Yes.

Let me write the final SVG.

Let me reconsider the belly feather pattern once more. I'll make them look like neat scale rows. Current arcs open downward (∩ shape, i.e., Q curves up then down — actually "M 220 306 Q 237 322 254 306" — this starts at (220,306), control point (237,322) which is below, ends at (254,306). So it curves DOWNWARD (a frown ∩... no). A quadratic from (220,306) to (254,306) with control at (237,322) [below]: the curve bulges downward. So it's a ∪-shaped... no. If control point is below the line, the curve bulges toward the control point (downward). So the arc bulges down, like a smile (∪)? No wait.

Point (220,306) and (254,306) are at the same height. Control (237,322) is below (larger y). The curve starts at (220,306), is pulled toward (237,322) at the middle, so the middle of the curve dips down to near (237,322). So the curve is a downward bulge = like a frown inverted... it's a "U" shape (smile), opening upward. Wait: the curve goes from (220,306) down to ~(237,322) and back up to (254,306). That's a U shape (smile), opening upward. 

For owl belly feathers (scales), I want overlapping scale shapes, like fish scales, which are like arcs opening upward (∪) stacked. Actually scale rows look like ∩ ∩ ∩ (frowns) or the scales curve. Let me just make them look like gentle arcs; it'll read as texture. The U-shapes stacked in rows look like a scaly belly, which is appropriate for an owl. Good.

Actually, owls have a scaly/flecked belly. The U-shaped arcs (opening up) stacked look reasonable. Let me keep them.

Let me finalize.

One more: let me make sure the SVG is valid — close all tags, correct attributes.

Let me write it out.

Actually, let me reconsider the stick shaft length and position so it doesn't look like it floats. The shaft from (127,155) to (360,388) locally rotated. The blade at the end. Let me make sure the blade is clearly at the bottom-right end.

In local coords, shaft y=104 to 434, blade at y=424-458 (bottom). After rotate(-45 250 278), the bottom (blade) goes to lower-right (377,405). The shaft top goes to upper-left (127,155). So the stick goes from upper-left to lower-right, blade at lower-right. Good.

Let me write final code.

Let me reconsider: should I add the word differently? "Owayo Eulers" — I split into "OWAYO" (top) and "EURLERS" (bottom). That represents the full name. Good. Alternatively, I could write "OWAYO EURLERS" but splitting on top/bottom arcs is cleaner and more logo-like.

Let me finalize.

Actually, I want to reconsider whether the bottom text will render right-side up. Let me reconsider by thinking about a concrete known-good example.

Known good SVG badge text (from many examples online):
```
<svg>
  <path id="top" d="M 20 100 A 80 80 0 0 1 180 100" />  <!-- top arc, left to right over top -->
  <path id="bottom" d="M 20 100 A 80 80 0 0 0 180 100" />  <!-- hmm -->
</svg>
```

Hmm, I've seen both. Let me think about it via the "text grows to the left of path direction" rule, which I'm fairly confident about.

For bottom text to be right-side up: at the bottom of the circle, path direction should be such that "left of direction" = "up" (toward center). 

If I walk the bottom arc from left to right (through the bottom), at the bottom I'm facing right (east). Left of east = north = up (toward center). So text grows toward center (up). Right-side up. ✓. This requires path from left to right through bottom = sweep=0 (as I have).

I'm confident. Bottom text sweep=0, right-side up.

But actually, wait. Let me reconsider "text grows to the left of path direction." Is it left or right?

Let me think about the TOP arc, which I KNOW should be right-side up in a badge (text over the top, readable). Top arc, left to right through top, at the top I face east (right). If text grows to the LEFT of direction = north = up = away from center. So text is above the arc, right-side up. ✓. This matches reality. So "text grows to the left of path direction" is correct.

Therefore bottom text (left to right through bottom, facing east at bottom, left = north = up = toward center) grows up (toward center), right-side up, inside the circle. ✓.

Great, confident.

Hmm, but actually now I doubt whether bottom text "inside the circle, right side up" is what we see in real badges. In real badges, bottom text IS right-side up and sits along the bottom curve. Yes. Confirmed.

Wait, one concern: "right side up" for bottom text in a badge — is it right side up or upside down? Let me think of a real example: a baseball team badge "NEW YORK" at top (right side up, over the top) and "YANKEES" at bottom. Is "YANKEES" at the bottom right-side up or upside down (reading along the bottom curve)?

In real badges, the bottom text is RIGHT SIDE UP (you can read it normally), positioned along the bottom curve. It's NOT upside down. So my rendering (right-side up) is correct. 

Wait, actually, hmm. Let me reconsider. I've seen badges where the bottom text is right-side up (like "EST. 1990" at the bottom, readable normally). Yes. So right-side up is correct. My design is correct.

Hmm, but actually, let me reconsider ONE more time, because I've also seen badges where bottom text appears to curve and be right-side up, which requires the text baseline to be on the inside of the bottom arc with text growing outward (downward)... no.

Ugh. OK let me think very concretely about a specific letter.

Take the letter "Y" in "YANKEES" at the very bottom of a badge, at position (100, 180) if badge center is (100,100) radius 80. So bottom point is (100, 180). The letter "Y" should be right-side up.

For it to be right-side up, its stem goes down (toward (100,195)) and the two arms go up (toward (100,155) area). Wait, no. A right-side up "Y": the junction is at top, stem goes down, arms go up-outward. So "Y" occupies from about y=150 (arms top) to y=175 (stem bottom), if centered at y=162... 

Hmm, but the bottom of the badge is at (100,180). If the "Y" is right-side up and its bottom (stem end) is at y=175, that's near the badge bottom (180). And its arms go up to y=150 (toward center). So the "Y" sits with stem pointing toward the badge edge (down/out) and arms toward center (up/in). 

Wait, that means the stem points OUTWARD (down, toward badge edge) and arms point INWARD (up, toward center). Is that right-side up? A right-side up "Y" has the junction at top and stem at bottom. If junction is toward center (up) and stem toward edge (down), then yes it's right-side up. ✓.

Now, in my textPath rendering: the baseline is on the arc (at the bottom, y=180 area... wait the arc is at radius 80, so bottom of arc is (100,180)). The text baseline is at (100,180)? No — the baseline is where the text sits. For bottom text, the baseline is on the arc, and text grows upward (toward center, north) from the baseline. So the baseline is at the bottom (y=180) and text grows up (toward center). So the BOTTOM of the letters (baseline) is at the badge bottom, and letters grow up toward center.

For "Y": baseline at y=180 (bottom), so the stem bottom is at y=180, and the stem goes up to y=165, junction at y=165, arms from y=165 up to y=155. So the "Y" has stem from 180 to 165, arms at top. That's right-side up (stem at bottom, arms at top). ✓.

Wait, that doesn't match what I said before (stem toward edge). Let me redo. If baseline (bottom of all letters) is at y=180 and letters grow up (decreasing y), then for "Y": the stem bottom is at baseline y=180, stem goes up to ~y=168, junction at y=168, arms branch up from y=168 to ~y=158. So stem is at the bottom (near badge edge), arms at top (near center). Right-side up. ✓.

Yes! This is right-side up. My rendering produces right-side up bottom text. 

So I'm confident. Let me finalize.

Actually hold on, I realize there might be an issue with which side the text grows. Let me re-examine with the rule "text grows to the left of path direction."

Bottom arc, left-to-right through bottom. At the bottom point (100,180), direction of travel: I'm moving from left to right, so at the bottom I'm moving east (rightward). "Left of east" (turning left from facing east) = north (up). So text grows north (up, toward center). ✓. Matches.

Good. Confident.

Now, let me also reconsider: is my bottom arc path actually going left-to-right through the bottom? Path: M 72 278 A 178 178 0 0 0 428 278. Start (72,278) [left], end (428,278) [right], sweep=0. As established, sweep=0 from left point goes counterclockwise, which on screen (y-down) means going downward first (toward bottom). So it passes through the bottom (250, 456). Direction at bottom: from left, through bottom, to right = eastward at bottom. ✓. Left-to-right. Good.

Alright, writing final.

Let me reconsider the stroke widths and make sure everything is visible. Let me also add a subtle outline to the beak and make the owl details pop.

Let me also reconsider: the inner ring at r=205 with stroke 2.5 color #4A62A6 — it's a thin decorative ring inside the gold ring. Good.

Let me write the final SVG now. I'll clean it up.

Actually, let me reconsider the overall composition balance. The owl is centered around x=250, y≈250-320. Text top at y≈100, bottom at y≈456. Badge center (250,278). The visual weight is a bit low (owl + bottom text). But it's fine for a badge.

Let me also make sure the owl isn't too big for the badge. Owl head r=78, body 78x76. Plus ears to y=68, feet to y=416. Text arcs at radius 178. The owl's feet (y=416) and ears (y=68) are within the badge (radius 230, y from 48 to 508). Good. The owl's widest point (wings to x=130 and x=370) within badge (x from 20 to 480). Good.

Alright, final code:

Let me write it out cleanly and check for errors.

I'll also reconsider adding a subtle gradient to the badge background for depth. Let me use a radial gradient for the badge: darker at edges, slightly lighter center. Or keep flat navy. Let me keep it mostly flat but maybe a subtle radial. Let me add a subtle radial gradient:
```
<radialGradient id="badgeGrad" cx="0.5" cy="0.4" r="0.65">
  <stop offset="0" stop-color="#222F5C"/>
  <stop offset="1" stop-color="#141D40"/>
</radialGradient>
```
And use it for the badge circle. Adds depth. Good.

Let me finalize.

Let me write the complete SVG:

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 500 560" width="500" height="560">
  <defs>
    <radialGradient id="badgeGrad" cx="0.5" cy="0.42" r="0.68">
      <stop offset="0" stop-color="#24315E"/>
      <stop offset="1" stop-color="#141D40"/>
    </radialGradient>
    <linearGradient id="bodyGrad" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#657BC8"/>
      <stop offset="1" stop-color="#30478C"/>
    </linearGradient>
    <radialGradient id="headGrad" cx="0.42" cy="0.35" r="0.75">
      <stop offset="0" stop-color="#8298DC"/>
      <stop offset="1" stop-color="#415A9C"/>
    </radialGradient>
    <linearGradient id="bellyGrad" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#F2F5FD"/>
      <stop offset="1" stop-color="#D4DBF2"/>
    </linearGradient>
  </defs>

  <!-- Badge -->
  <circle cx="250" cy="278" r="230" fill="url(#badgeGrad)"/>
  <circle cx="250" cy="278" r="216" fill="none" stroke="#F7B400" stroke-width="7"/>
  <circle cx="250" cy="278" r="204" fill="none" stroke="#4A62A6" stroke-width="2.5"/>

  <!-- Hockey stick -->
  <g transform="rotate(-45 250 278)">
    <rect x="244" y="104" width="12" height="330" rx="6" fill="#C68A34"/>
    <rect x="244" y="104" width="5" height="330" rx="3" fill="#8A5A1E" opacity="0.55"/>
    <path d="M 244 430 L 244 458 L 320 458 Q 334 458 333 439 L 333 430 Q 327 424 315 424 L 256 424 Z"
          fill="#F4F6FC" stroke="#141A30" stroke-width="3" stroke-linejoin="round"/>
    <line x1="246" y1="458" x2="328" y2="458" stroke="#141A30" stroke-width="2.5"/>
  </g>

  <!-- Owl -->
  <ellipse cx="250" cy="318" rx="78" ry="76" fill="url(#bodyGrad)" stroke="#202C5C" stroke-width="3"/>
  <ellipse cx="250" cy="330" rx="53" ry="58" fill="url(#bellyGrad)"/>
  <g

### Antwort

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 500 560" width="500" height="560">
  <defs>
    <radialGradient id="badgeGrad" cx="0.5" cy="0.42" r="0.68">
      <stop offset="0" stop-color="#24315E"/>
      <stop offset="1" stop-color="#141D40"/>
    </radialGradient>
    <linearGradient id="bodyGrad" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#657BC8"/>
      <stop offset="1" stop-color="#30478C"/>
    </linearGradient>
    <radialGradient id="headGrad" cx="0.42" cy="0.35" r="0.75">
      <stop offset="0" stop-color="#8298DC"/>
      <stop offset="1" stop-color="#415A9C"/>
    </radialGradient>
    <linearGradient id="bellyGrad" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#F2F5FD"/>
      <stop offset="1" stop-color="#D4DBF2"/>
    </linearGradient>
  </defs>

  <!-- Badge -->
  <circle cx="250" cy="278" r="230" fill="url(#badgeGrad)"/>
  <circle cx="250" cy="278" r="216" fill="none" stroke="#F7B400" stroke-width="7"/>
  <circle cx="250" cy="278" r="204" fill="none" stroke="#4A62A6" stroke-width="2.5"/>

  <!-- Hockey stick (behind owl) -->
  <g transform="rotate(-45 250 278)">
    <rect x="244" y="104" width="12" height="330" rx="6" fill="#C68A34"/>
    <rect x="244" y="104" width="5" height="330" rx="3" fill="#8A5A1E" opacity="0.55"/>
    <path d="M 244 430 L 244 458 L 320 458 Q 334 458 333 439 L 333 430 Q 327 424 315 424 L 256 424 Z"
          fill="#F4F6FC" stroke="#141A30" stroke-width="3" stroke-linejoin="round"/>
    <line x1="246" y1="458" x2="328" y2="458" stroke="#141A30" stroke-width="2.5"/>
  </g>

  <!-- Owl -->
  <ellipse cx="250" cy="318" rx="78" ry="76" fill="url(#bodyGrad)" stroke="#202C5C" stroke-width="3"/>
  <ellipse cx="250" cy="330" rx="53" ry="58" fill="url(#bellyGrad)"/>
  <g stroke="#AEB8DE" stroke-width="3.5" fill="none" stroke-linecap="round">
    <path d="M 220 306 Q 237 322 254 306"/>
    <path d="M 252 306 Q 269 322 286 306"/>
    <path d="M 216 338 Q 237 356 258 338"/>
    <path d="M 256 338 Q 277 356 298 338"/>
    <path d="M 222 372 Q 241 388 260 372"/>
    <path d="M 258 372 Q 277 388 296 372"/>
  </g>
  <path d="M 174 292 Q 130 336 152 408 Q 176 386 188 326 Z" fill="#2C407F" stroke="#202C5C" stroke-width="3"/>
  <path d="M 326 292 Q 370 336 348 408 Q 324 386 312 326 Z" fill="#2C407F" stroke="#202C5C" stroke-width="3"/>
  <path d="M 206 120 L 178 68 L 230 110 Z" fill="#415A9C" stroke="#202C5C" stroke-width="3" stroke-linejoin="round"/>
  <path d="M 294 120 L 322 68 L 270 110 Z" fill="#415A9C" stroke="#202C5C" stroke-width="3" stroke-linejoin="round"/>
  <circle cx="250" cy="188" r="78" fill="url(#headGrad)" stroke="#202C5C" stroke-width="3"/>
  <circle cx="218" cy="190" r="42" fill="none" stroke="#F7B400" stroke-width="8"/>
  <circle cx="282" cy="190" r="42" fill="none" stroke="#F7B400" stroke-width="8"/>
  <circle cx="218" cy="190" r="36" fill="#FDFDFD"/>
  <circle cx="282" cy="190" r="36" fill="#FDFDFD"/>
  <circle cx="221" cy="192" r="16" fill="#141A30"/>
  <circle cx="279" cy="192" r="16" fill="#141A30"/>
  <circle cx="212" cy="183" r="6" fill="#FFFFFF"/>
  <circle cx="288" cy="183" r="6" fill="#FFFFFF"/>
  <path d="M 240 218 L 260 218 L 250 246 Z" fill="#F29300" stroke="#141A30" stroke-width="2.5" stroke-linejoin="round"/>
  <g stroke="#F29300" stroke-width="5.5" fill="none" stroke-linecap="round">
    <path d="M 228 392 L 218 412"/>
    <path d="M 233 394 L 235 416"/>
    <path d="M 238 392 L 252 410"/>
    <path d="M 262 392 L 248 410"/>
    <path d="M 267 394 L 265 416"/>
    <path d="M 272 392 L 282 412"/>
  </g>

  <!-- Decorative stars -->
  <g transform="translate(90 278)" fill="#F7B400">
    <path d="M 0 -8 L 2.5 -2.5 L 8 0 L 2.5 2.5 L 0 8 L -2.5 2.5 L -8 0 L -2.5 -2.5 Z"/>
  </g>
  <g transform="translate(410 278)" fill="#F7B400">
    <path d="M 0 -8 L 2.5 -2.5 L 8 0 L 2.5 2.5 L 0 8 L -2.5 2.5 L -8 0 L -2.5 -2.5 Z"/>
  </g>

  <!-- Team name -->
  <text font-family="Arial Black, Arial, Helvetica, sans-serif" font-weight="bold" font-size="40" letter-spacing="5" fill="#F7B400">
    <textPath d="M 72 278 A 178 178 0 0 1 428 278" startOffset="50%" text-anchor="middle">OWAYO</textPath>
  </text>
  <text font-family="Arial Black, Arial, Helvetica, sans-serif" font-weight="bold" font-size="40" letter-spacing="5" fill="#F7B400">
    <textPath d="M 72 278 A 178 178 0 0 0 428 278" startOffset="50%" text-anchor="middle">EURLERS</textPath>
  </text>
</svg>
```
