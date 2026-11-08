# ornith-1_5-35b-a3b-dflash - logo-owayo-eulers (2026-11-08T23:25:25)

## Antwort (16805 Tokens, 253.784 s, Ende: stop, Denken abgebrochen)

### Denkphase

The user wants me to create a logo for an ice hockey team called "Owayo Eulers". The logo should contain an owl and an ice hockey stick. The background should be solid or ideally have no background.

I need to respond with exactly one complete SVG document in a code block (```svg ... ```). No external resources, no scripts.

Let me create an SVG logo with:
1. An owl
2. An ice hockey stick
3. The team name "Owayo Eulers"
4. No background (transparent)

Let me design this carefully. I'll create a nice owl with hockey elements.

Let me build the SVG:
- An owl in the center
- A hockey stick crossed behind or beside it
- The text "Owayo Eulers"

Let me create a detailed, attractive logo.

I'll use a color scheme typical for hockey - maybe dark blue, gold/yellow accents.

Let me draw:
- Owl body with feathers
- Big eyes
- Owl wings
- A hockey stick
- Team name text

Let me write this out.

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 500 500" width="500" height="500">
  <!-- Background circle emblem -->
  ...
</svg>
```

Let me design the owl carefully. I'll make it front-facing owl which is classic for logos.

Let me create the elements:

1. Outer circle (team emblem border)
2. Owl body
3. Owl eyes
4. Owl beak
5. Owl wings
6. Owl ears/tufts
7. Hockey stick
8. Text "Owayo Eulers"

Let me write the full SVG with good detail.

For the owl, I'll use ellipses and paths.

Let me think about the layout:
- Center at 250, 250
- Circle radius ~220
- Owl in the middle
- Hockey stick behind
- Text at bottom or top

Let me build it.

I'll make a nice gradient for the owl body.

Here's my plan:

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 500 500" width="500" height="500">
  <defs>
    <linearGradient id="bodyGrad" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#4a6fa5"/>
      <stop offset="1" stop-color="#2c4a7e"/>
    </linearGradient>
  </defs>
  
  <!-- Outer ring -->
  <circle cx="250" cy="250" r="230" fill="none" stroke="#f5c518" stroke-width="12"/>
  ...
</svg>
```

Let me create a comprehensive design. I'll make the owl with:
- Body ellipse
- Head
- Eye circles (white with dark pupils)
- Beak (triangle/orange)
- Wing shapes
- Ear tufts
- Belly pattern

And a hockey stick.

Let me write it all out now.

For the hockey stick, I'll draw an L-shape path with a blade at the bottom.

Let me finalize:

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 500 500" width="500" height="500">
  <defs>
    <linearGradient id="bodyGrad" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#5a7fb5"/>
      <stop offset="1" stop-color="#2c4a7e"/>
    </linearGradient>
    <radialGradient id="eyeGrad" cx="0.5" cy="0.4" r="0.6">
      <stop offset="0" stop-color="#ffd54f"/>
      <stop offset="1" stop-color="#ff8f00"/>
    </radialGradient>
  </defs>
  
  <!-- Emblem outer ring -->
  <circle cx="250" cy="250" r="235" fill="none" stroke="#f5c518" stroke-width="10"/>
  <circle cx="250" cy="250" r="220" fill="none" stroke="#2c4a7e" stroke-width="6"/>
  
  <!-- Hockey stick -->
  <path d="M 150 90 L 150 380 Q 150 430 100 440 L 60 448 Q 45 451 48 438 L 60 418 Q 70 400 90 395 L 130 383 Q 150 377 150 355 L 150 90 Z" fill="#8d5b2d" stroke="#5c3a1a" stroke-width="2"/>
  ...
</svg>
```

Hmm, this is getting complex. Let me simplify but keep it attractive.

Let me create a cleaner design. I'll place the owl prominently with a hockey stick behind it.

Let me write the complete thing now.

Actually, let me think about the owl design more carefully to make it look good.

Owl front view:
- Two big round eyes near the top
- Small beak between/below eyes
- Round body below
- Wings on sides
- Ear tufts at top corners
- Belly with feather texture

Let me create:

Eyes: two white circles at (200, 200) and (300, 200), radius 45
Pupils: dark circles
Beak: orange triangle at (250, 250)

Body: ellipse at (250, 320), rx 90, ry 100

Wings: paths on left and right

Ear tufts: triangles at top

Let me also add feather details on belly.

For the hockey stick, I'll put it diagonally behind the owl.

Let me write the final SVG.

I'll make it nice and complete. Let me be careful with the paths.

Final design:

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 500 500" width="500" height="500">
  <defs>
    <linearGradient id="bodyGrad" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#5a7fb5"/>
      <stop offset="1" stop-color="#26406b"/>
    </linearGradient>
    <radialGradient id="eyeGrad" cx="0.5" cy="0.35" r="0.7">
      <stop offset="0" stop-color="#ffe082"/>
      <stop offset="0.6" stop-color="#ffc107"/>
      <stop offset="1" stop-color="#e6a700"/>
    </radialGradient>
  </defs>
  
  <!-- Hockey stick (behind) -->
  <g>
    <path d="M 330 70 L 360 90 300 420 Q 290 470 240 480 L 200 488 Q 185 490 188 475 L 200 455 Q 208 440 225 436 L 310 414 Q 335 408 342 375 L 362 90 Z" .../>
  </g>
```

This is getting complicated with the stick. Let me make the hockey stick simpler and cleaner.

A hockey stick viewed from the side:
- Long shaft (rectangle, slightly angled)
- Blade at the bottom (L-shape, curved)

Let me make it a clean diagonal stick.

Actually, for a logo, let me put the hockey stick behind the owl, going diagonally. The blade at bottom-left, handle at top-right.

Let me define the stick with a path:

Shaft: from top-right to bottom-left
Blade: at bottom-left, curving

Let me just create a nice curved hockey stick shape.

I'll make the stick handle a thin rounded rectangle rotated, and the blade a shape.

Let me use a transform rotate approach:

```svg
<g transform="rotate(-35 250 250)">
  <!-- shaft -->
  <rect x="240" y="40" width="20" height="330" rx="10" fill="#a0632e"/>
  <!-- blade -->
  <path d="M 240 360 L 260 360 L 260 410 Q 260 430 240 430 L 190 425 Q 175 423 178 408 L 185 385 Q 188 372 200 370 ..." />
</g>
```

Hmm, let me think about the blade shape. A hockey stick blade is like a curved paddle at the end.

Let me create a simpler version. I'll make the stick:
- Shaft: thin long shape
- Blade: at the bottom, a flat curved paddle

Let me just write clean paths and test mentally.

OK let me just commit to a design. I'll create the owl and a hockey stick.

Let me write the complete SVG now with careful attention.

I'll structure:
1. defs (gradients)
2. Hockey stick (behind owl)
3. Owl
   - Body
   - Head
   - Eyes
   - Beak
   - Wings
   - Ear tufts
   - Belly feathers
4. Text "Owayo Eulers"

Let me write it.

For text, I'll place "Owayo" at top in an arc or straight, and "Eulers" at bottom. Or just put "OWAYO EULERS" straight.

Actually, let me put the team name in a curved path along the bottom, or just straight text.

Let me keep it clean with straight text at the bottom.

Let me finalize the SVG:

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 500 500" width="500" height="500">
  <defs>
    <linearGradient id="bodyGrad" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#5f86bb"/>
      <stop offset="1" stop-color="#243d68"/>
    </linearGradient>
    <radialGradient id="eyeGrad" cx="0.5" cy="0.35" r="0.7">
      <stop offset="0" stop-color="#ffe98c"/>
      <stop offset="0.6" stop-color="#ffc107"/>
      <stop offset="1" stop-color="#cc8f00"/>
    </radialGradient>
    <linearGradient id="stickGrad" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="#b0763c"/>
      <stop offset="1" stop-color="#7a4a20"/>
    </linearGradient>
  </defs>
  
  <!-- Hockey stick -->
  <g transform="rotate(-32 250 260)">
    <rect x="242" y="45" width="18" height="320" rx="9" fill="url(#stickGrad)" stroke="#5c3a1a" stroke-width="1.5"/>
    <path d="M 242 360 
             L 260 360 
             L 262 415 
             Q 262 438 240 440 
             L 205 436 
             Q 190 434 191 418 
             L 196 382 
             Q 198 367 212 366 
             L 242 366 Z" 
          fill="url(#stickGrad)" stroke="#5c3a1a" stroke-width="1.5"/>
    <!-- blade tape -->
    <rect x="193" y="378" width="66" height="8" rx="3" fill="#f0f0f0" opacity="0.85"/>
  </g>
  
  ...
</svg>
```

Wait, the blade should curve. Let me reconsider. The blade of a hockey stick is at the bottom and curves to form a U shape when viewed from the side, but from a 2D front view it looks like a flat paddle.

Let me simplify: the blade is a flat piece at the bottom.

Actually, let me make the stick a clean diagonal with a blade. Let me reconsider the whole thing.

Let me place the stick so it goes from top-right down to bottom-left, with the blade at the bottom-left.

Given the rotation of -32 degrees around (250,260), the vertical stick becomes diagonal.

Let me make the blade point downward (in the rotated frame, at the bottom).

The blade shape (before rotation, pointing down):
- Start at shaft bottom (242, 360)
- The blade extends to the left and curves

Let me make a proper hockey blade:

```
M 242 358
L 262 358
L 262 410
Q 262 432 238 434
L 200 430
Q 186 428 188 412
L 193 378
Q 195 362 210 362
Z
```

Hmm, this makes the blade curve to the left. That's fine for a side view of the blade.

Actually for a logo, let me make it look like a real hockey stick blade. The blade has a slight curve and tape at the top of the blade.

Let me just go with a reasonable design.

Let me reconsider and make the whole thing cleaner. I'll create:

The owl facing forward, with a hockey stick crossed behind it (like a crest/emblem style).

Actually, a single hockey stick behind the owl is cleaner. Let me do that.

Let me write the final complete SVG now. I'll be careful.

Let me reconsider the layout to make it look professional:

- Circular emblem with border
- Owl centered
- Hockey stick behind, diagonal
- "OWAYO" text top arc, "EULERS" text bottom arc
- Or straight text

For text on a circular emblem, curved text looks great. Let me use textPath.

Let me create curved text along the circle.

```svg
<path id="topArc" d="M 70 250 A 180 180 0 0 1 430 250" fill="none"/>
<path id="bottomArc" d="M 75 250 A 175 175 0 0 0 425 250" fill="none"/>
<text><textPath href="#topArc">OWAYO</textPath></text>
```

Wait, but the user said the owl and hockey stick should be in the logo, and the team name. Curved text around the emblem would look professional.

But I need to make sure the text is readable. Let me use a bold font.

Let me finalize. I'll make:
- Top arc text: "OWAYO"
- Bottom arc text: "EULERS"
- Owl in center
- Hockey stick behind

Actually, "Owayo Eulers" as one name. Let me put "OWAYO" on top and "EULERS" on bottom. That works nicely.

Let me write the complete SVG.

Let me be very careful with the owl paths to make it look good.

Owl design (front view, centered around 250, 250):

Head/Body: A large rounded shape. Let me use an ellipse for the body and a circle for the head, or a combined shape.

Let me make:
- Body: ellipse cx=250 cy=300 rx=95 ry=105, fill bodyGrad
- Head: circle cx=250 cy=200 r=85, fill bodyGrad (or slightly different shade)

Actually for an owl, the head and body blend. Let me make one big rounded body shape.

Let me do:
- Main body: path or ellipse from head to body

Let me use an ellipse for the whole body: cx=250 cy=280 rx=100 ry=120

Then eyes on the upper part.

Eyes:
- Left eye: circle cx=205 cy=220 r=42, fill white/eyeGrad
- Right eye: circle cx=295 cy=220 r=42, fill eyeGrad
- Pupils: circle cx=205 cy=222 r=18, fill dark
- Right pupil: circle cx=295 cy=222 r=18, fill dark
- Eye shine: small white circles

Beak:
- Triangle pointing down at (250, 255)
- Left point (235, 245), right point (265, 245), bottom (250, 275)
- fill orange/amber

Ear tufts (owl "horns"):
- Left: path from head top-left
- Right: path from head top-right

Wings:
- Left wing: path on left side
- Right wing: path on right side

Belly feathers:
- V-shaped or chevron patterns in lighter color

Let me write these.

Let me define colors:
- Body dark blue: #243d68
- Body light: #5f86bb
- Belly: #dfe8f5 (light)
- Eyes: yellow gradient
- Beak: #e8912a (orange)
- Wings: #2f4d80

Let me write the full thing.

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 500 500" width="500" height="500">
  <defs>
    <linearGradient id="bodyGrad" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#6b93c9"/>
      <stop offset="0.5" stop-color="#3d6298"/>
      <stop offset="1" stop-color="#243d68"/>
    </linearGradient>
    <radialGradient id="eyeGrad" cx="0.5" cy="0.35" r="0.7">
      <stop offset="0" stop-color="#fff1a8"/>
      <stop offset="0.55" stop-color="#ffca28"/>
      <stop offset="1" stop-color="#c98a00"/>
    </radialGradient>
    <linearGradient id="stickGrad" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="#c48a4a"/>
      <stop offset="1" stop-color="#7d4e22"/>
    </linearGradient>
    <linearGradient id="bellyGrad" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#eef3fb"/>
      <stop offset="1" stop-color="#c7d4ea"/>
    </linearGradient>
  </defs>
  
  <!-- ===== Hockey stick ===== -->
  <g transform="rotate(-34 250 255)">
    <rect x="243" y="52" width="16" height="310" rx="8" fill="url(#stickGrad)" stroke="#5c3a1a" stroke-width="1.5"/>
    <path d="M 243 358 L 259 358 L 261 412 Q 261 434 238 436 L 203 432 Q 189 430 191 414 L 196 381 Q 198 365 213 365 Z"
          fill="url(#stickGrad)" stroke="#5c3a1a" stroke-width="1.5"/>
    <rect x="194" y="376" width="64" height="7" rx="3.5" fill="#f4f4f4" opacity="0.9"/>
  </g>
  
  <!-- ===== Emblem ring ===== -->
  <circle cx="250" cy="250" r="232" fill="none" stroke="#f5c518" stroke-width="12"/>
  <circle cx="250" cy="250" r="216" fill="none" stroke="#243d68" stroke-width="5"/>
  
  <!-- ===== Owl ===== -->
  ...
</svg>
```

Now the owl. Let me place it.

Body ellipse: cx=250 cy=300 rx=96 ry=110

Let me draw the body first (it will partially be behind the ring).

Actually, let me make the owl sit nicely within the circle. The circle inner radius is 216. Let me keep the owl within about 180 radius.

Let me position:
- Body: ellipse cx=250 cy=310 rx=90 ry=100
- Head: circle cx=250 cy=210 r=78

Hmm, but head and body should connect. Let me make the body start from around cy=250 down.

Let me reconsider. An owl's head is large and blends into the body. Let me make:
- A large body ellipse: cx=250 cy=290 rx=95 ry=115
- The eyes and beak on the upper part of this body
- Ear tufts at the top

This gives a rounded owl. Let me go with that.

Eyes on upper body:
- Left eye: cx=210 cy=235 r=40
- Right eye: cx=290 cy=235 r=40

Beak between eyes, below:
- (250, 265) area

Ear tufts at top of head:
- Left tuft: around (185, 175)
- Right tuft: around (315, 175)

Wings on sides:
- Left wing: around (165, 300)
- Right wing: around (335, 300)

Belly: center-lower body, lighter color

Let me write these paths.

Body:
```svg
<ellipse cx="250" cy="300" rx="95" ry="112" fill="url(#bodyGrad)" stroke="#1c3055" stroke-width="2"/>
```

Ear tufts (pointed feather clusters at top):
```svg
<path d="M 188 195 Q 170 150 195 155 Q 205 175 215 195 Z" fill="url(#bodyGrad)" stroke="#1c3055" stroke-width="1.5"/>
<path d="M 312 195 Q 330 150 305 155 Q 295 175 285 195 Z" fill="url(#bodyGrad)" stroke="#1c3055" stroke-width="1.5"/>
```

Hmm, let me make ear tufts look like little pointy ears.

Eyes (white rings + colored iris + pupil):
```svg
<circle cx="210" cy="240" r="42" fill="#f7f9fd" stroke="#1c3055" stroke-width="2"/>
<circle cx="290" cy="240" r="42" fill="#f7f9fd" stroke="#1c3055" stroke-width="2"/>
<circle cx="210" cy="240" r="27" fill="url(#eyeGrad)"/>
<circle cx="290" cy="240" r="27" fill="url(#eyeGrad)"/>
<circle cx="210" cy="240" r="14" fill="#141922"/>
<circle cx="290" cy="240" r="14" fill="#141922"/>
<circle cx="203" cy="232" r="5" fill="#ffffff"/>
<circle cx="283" cy="232" r="5" fill="#ffffff"/>
```

Beak:
```svg
<path d="M 250 262 L 232 268 Q 250 292 268 268 Z" fill="#e8912a" stroke="#b5691a" stroke-width="1.5"/>
```
Actually a two-part beak (upper and lower mandible) looks more owl-like. Let me do a simple triangle or a "heart" shape pointing down.

Let me do:
```svg
<path d="M 233 262 L 267 262 L 250 290 Z" fill="#f0a830" stroke="#b5691a" stroke-width="1.5"/>
```

Hmm, let me make it look like an owl beak - often shown as two small triangles or a downward triangle. A single downward triangle is fine.

Actually, owls have a hooked beak. Let me draw it as a shape:
```svg
<path d="M 235 258 Q 250 252 265 258 Q 262 278 250 288 Q 238 278 235 258 Z" fill="#e8912a" stroke="#b5691a" stroke-width="1.5"/>
```

Wings:
```svg
<path d="M 160 280 Q 130 320 150 380 Q 160 405 185 400 Q 175 350 185 300 Q 188 280 175 275 Z" fill="url(#bodyGrad)" stroke="#1c3055" stroke-width="2"/>
<path d="M 340 280 Q 370 320 350 380 Q 340 405 315 400 Q 325 350 315 300 Q 312 280 325 275 Z" fill="url(#bodyGrad)" stroke="#1c3055" stroke-width="2"/>
```

Belly (lighter area with feather texture):
```svg
<ellipse cx="250" cy="330" rx="58" ry="68" fill="url(#bellyGrad)"/>
```
Then feather chevrons:
```svg
<g stroke="#9fb0cd" stroke-width="2" fill="none" opacity="0.8">
  <path d="M 220 310 Q 250 325 280 310"/>
  <path d="M 222 335 Q 250 350 278 335"/>
  <path d="M 225 360 Q 250 375 275 360"/>
  <path d="M 228 385 Q 250 398 272 385"/>
</g>
```

Now the text.

Top arc: "OWAYO"
Bottom arc: "EULERS"

```svg
<path id="topArc" d="M 72 250 A 178 178 0 0 1 428 250" fill="none"/>
<path id="bottomArc" d="M 78 250 A 172 172 0 0 0 422 250" fill="none"/>

<text font-family="Arial, Helvetica, sans-serif" font-weight="bold" font-size="34" fill="#243d68" letter-spacing="4">
  <textPath href="#topArc" startOffset="50%" text-anchor="middle">OWAYO</textPath>
</text>
<text font-family="Arial, Helvetica, sans-serif" font-weight="bold" font-size="34" fill="#243d68" letter-spacing="6">
  <textPath href="#bottomArc" startOffset="50%" text-anchor="middle">EULERS</textPath>
</text>
```

Wait, the text color - if I use dark blue text on the ring, it might be hard to read against the gold ring. Let me use the gold ring but text in dark blue would contrast OK on... hmm. Actually, let me reconsider the color scheme.

Let me make the ring gold (#f5c518) and put text in dark blue (#243d68). On gold background, dark blue text is readable. But the arc paths are within the ring area. Let me position the text to sit on the ring.

Actually, the top arc at radius 178 with the ring at radius 216-232... the text baseline should be around the middle of the ring band. Let me adjust.

Hmm, this is getting complicated. Let me simplify the text placement.

Option: Put text straight, not curved. "OWAYO EULERS" as one line, or "OWAYO" top and "EULERS" bottom straight.

Actually curved text around a circular emblem is very classic for sports logos. Let me keep it but make sure it's readable.

Let me reconsider: The ring is gold. Text on the ring. If text is dark blue, it reads well on gold.

Let me position the arcs so text sits in the gold band.

Ring: outer r=232, inner r=216. Middle ~224.

Top arc text baseline should be at about r=224 from center, at the top.
Bottom arc text baseline at r=224, at the bottom.

For top arc, I want the text to follow the top of the circle, reading left to right, upright.
Path: from left (around 20,250) to right (around 480,250) along the top.
`d="M 30 250 A 220 220 0 0 1 470 250"` — this draws the top semicircle.

For bottom arc, text reading left to right at the bottom (upside down relative to top, but text follows the curve):
`d="M 40 250 A 210 210 0 0 0 460 250"` — bottom semicircle.

With text-anchor middle and startOffset 50%, the text centers on the path.

Let me set font size to about 30-34.

Let me refine. I'll make:
- Top: "O WAYO" or "OWAYO" — team is "Owayo Eulers". Let me split as "OWAYO" top, "EULERS" bottom.

Actually, maybe better: top arc "OWAYO", bottom arc "EULERS". Both centered.

Let me set:
Top arc radius 205, bottom arc radius 205.

Top path: `M 45 250 A 205 205 0 0 1 455 250`
Bottom path: `M 55 250 A 195 195 0 0 0 445 250`

Hmm, let me just compute. Center (250,250), radius R. Top point is (250, 250-R). Left point (250-R, 250), right point (250+R, 250).

For top semicircle from left to right going over the top:
`M (250-R) 250 A R R 0 0 1 (250+R) 250`

For bottom semicircle from left to right going under the bottom:
`M (250-R) 250 A R R 0 0 0 (250+R) 250`

Let me use R=200.
Top: `M 50 250 A 200 200 0 0 1 450 250`
Bottom: `M 50 250 A 200 200 0 0 0 450 250`

Text baseline on these paths. Font size 30, bold.

Let me check "OWAYO" width at font-size 30 bold: roughly 5 chars * 18px = 90px. On a circle of radius 200, arc for 90px is angle 90/200 = 0.45 rad = 26 degrees. That's fine, won't overlap.

"EULERS" 6 chars * 18 = 108px, angle 32 degrees. Fine.

Let me finalize.

Now, one concern: the text on the bottom arc will be upside-down-ish (following the curve, so it reads along the bottom with the baseline toward the center). Actually with textPath, the text follows the path direction. For the bottom arc going from left to right (M 50 250 ... to 450 250, going under), the text will be upright and readable if... hmm.

Let me think. The bottom path goes from left (50,250) curving down to bottom (250, 450) then up to right (450,250). The path direction at the bottom point is left-to-right (eastward). Text placed on this path with baseline following... the text will be upright (readable) because the path tangent is horizontal and the text sits above the path (baseline on path, text extends... in the direction of the normal).

Hmm, actually text on a path: the text is placed so its baseline is on the path, and it extends perpendicular to the path in the direction determined by the path. For a path curving downward (bottom of circle), the text baseline is on the path and text extends toward the center (upward visually) or away?

The convention: text is drawn above the baseline in the direction of the path's up. For the bottom arc drawn left-to-right, the text will appear... Let me just make it readable. Typically for bottom text in circular logos, you draw the path from right to left so the text is upright.

To get upright readable text at the bottom, I should draw the bottom path from right to left:
`M 450 250 A 200 200 0 0 1 50 250` (going under the bottom, from right to left)

Wait, let me think again. For bottom text to be upright and readable:
- Path should go from right to left along the bottom
- `M 450 250 A 200 200 0 0 1 50 250` — this goes from right, under the bottom, to left. At the bottom, tangent points leftward (west). Text baseline on path, text extends... 

Ugh, let me just recall the standard technique.

Standard: For text along the bottom of a circle (upright), define the path going clockwise from the right side to the left side along the bottom. Actually, the trick is:

For top text (upright, L-to-R): path goes L-to-R over the top.
For bottom text (upright, L-to-R): path goes R-to-L under the bottom.

So:
Top: `M 50 250 A 200 200 0 0 1 450 250` (L to R over top, sweep=1)
Bottom: `M 450 250 A 200 200 0 0 1 50 250` (R to L under bottom, sweep=1)

Wait, for the bottom, going from right (450,250) to left (50,250) via the bottom. Using large-arc=0, sweep=1:
`M 450 250 A 200 200 0 0 1 50 250`
Sweep=1 means clockwise. From (450,250) going clockwise... clockwise from the right point would go downward first (to bottom) then to left. Yes! That traces the bottom. Good.

Hmm wait, let me double check. In SVG, sweep-flag=1 means "positive angle direction" which is clockwise in the coordinate system (where y points down). 

Point (450, 250) is to the right of center (250,250). Going clockwise from the rightmost point: clockwise in a standard math sense would go up, but in screen coords (y down), clockwise visually... 

Let me think carefully. In screen coordinates (y increases downward), "sweep-flag = 1" draws the arc in the "positive angle" direction, which corresponds to clockwise when viewed normally (as we see the screen).

Starting at rightmost point (450, 250), moving clockwise (as viewed): clockwise means going... at the rightmost point, clockwise motion goes upward (toward top). But we want to go to the bottom.

Hmm, so sweep=1 from rightmost goes up (toward top), sweep=0 goes down (toward bottom).

Let me redo:
Bottom text path from right to left via bottom:
`M 450 250 A 200 200 0 0 0 50 250` — sweep=0, goes counterclockwise-as-viewed, which from rightmost goes down to bottom then to left. 

Wait I need to be careful.

Let me set up: center (250,250). Points at angles (standard, but y-down):
- Right: (450, 250), angle 0°
- Bottom: (250, 450), angle 90° (in y-down, this is "down")
- Left: (50, 250), angle 180°
- Top: (250, 50), angle -90°/270°

SVG arc sweep-flag=1 draws in the direction of increasing angle in the SVG coordinate system. Since y is down, increasing angle goes clockwise as we see it? 

Actually, in SVG, with y-axis pointing down, sweep-flag=1 corresponds to the angle increasing in the standard mathematical sense converted... ugh.

Let me just reason geometrically. sweep-flag = 1 means "positive-angle direction". In SVG's coordinate system (y down), positive angle direction is clockwise when viewed on screen.

Hmm, no. Let me think about it differently. 

Consider drawing an arc from (450,250) [right] to (50,250) [left], radius 200.
- If it bulges downward (through bottom (250,450)): this is the bottom arc.
- If it bulges upward (through top (250,50)): this is the top arc.

For the bottom arc (bulging down):
From right point, going to left point, bulging down. The direction of travel: starting at right, we go down-and-left to reach the bottom, then up-and-left to reach left. 

Is this clockwise or counterclockwise (as viewed on screen)? Starting at 3 o'clock position, moving to 6 o'clock (bottom), then 9 o'clock (left). 3→6→9 o'clock is clockwise (as viewed on a clock: 3, 4, 5, 6 is clockwise). Yes! So bottom arc from right to left is clockwise = sweep-flag=1.

Wait, 3 o'clock to 6 o'clock: on a clock, numbers increase clockwise (12 at top, 3 at right, 6 at bottom, 9 at left). Going 3→6 is clockwise. Yes.

So bottom arc (bulging down) from right(450,250) to left(50,250) is clockwise → sweep-flag=1.
`M 450 250 A 200 200 0 0 1 50 250`

For top arc from left(50,250) to right(450,250), bulging up (through top):
Left(9 o'clock) → top(12 o'clock) → right(3 o'clock). 9→12→3 is clockwise. So top arc from left to right is also clockwise → sweep-flag=1.
`M 50 250 A 200 200 0 0 1 450 250`

OK so both use sweep=1, just different start/end points.

Now, for text readability:
- Top arc, path goes L→R (clockwise over top). At the top point (250,50), the tangent direction is left-to-right (eastward). Text baseline along path, text extends upward (away from center). So text is upright and readable. 

- Bottom arc, path goes R→L (clockwise under bottom). At the bottom point (250,450), the tangent direction is right-to-left (westward). Text baseline along path. Text extends... in the direction away from the path's left side. The text will extend downward (away from center) and be upright and readable. 

Wait, let me double-check the bottom text orientation. When text is placed on a path going R→L (westward) at the bottom, the baseline is on the path (at bottom, y=450), and the text extends perpendicular to the tangent. The "up" direction of the text is 90° counter-clockwise from the path direction in SVG? 

The text's baseline direction is the path direction (westward). The text ascends in the direction perpendicular to the baseline, rotated... In SVG, text is drawn with the baseline and the text goes "up" in the direction obtained by rotating the path direction by -90° (clockwise) or +90°?

Ugh, I'm overcomplicating. Let me just recall the practical result:

For a bottom arc where you want upright readable text, the path should be drawn such that text is on the outside (bottom) and readable. The common approach:

```
<path id="bottom" d="M 60 250 A 190 190 0 0 0 440 250" />
```
This draws from left to right along the bottom (bulging down). Let me check: from (60,250) left to (440,250) right, sweep=0. Sweep=0 is counterclockwise-as-viewed. From left(9 o'clock), counterclockwise goes to 6 o'clock (bottom) then 3 o'clock (right). 9→6→3. Is that counterclockwise? On a clock, 9→6→3 is counterclockwise (reverse of 3→6→9). Yes. So this bulges down through the bottom, from L to R.

With this path (L→R along bottom), at the bottom point the tangent is eastward (L→R). Text ascends... and would point toward the center (upward visually, toward top of circle). That means the text would be upside down (its top pointing toward center = up, but... hmm).

I think I'm overanalyzing. Let me just use the standard known-good approach and verify by reasoning about a real example.

Known fact: In many SVG logos, bottom text that is upright is achieved with the path drawn right-to-left on the bottom, OR the text is placed and it naturally comes out right.

Let me just try to reason with a concrete mental model of how SVG textPath works:

The text is placed along the path. Each character is positioned with its baseline tangent to the path, in the direction of path travel. The character's "up" is perpendicular to the baseline, specifically rotated 90° clockwise from the path direction (in screen coordinates).

Wait, I recall: the text's up direction is the path direction rotated by -90 degrees (in SVG's y-down system, -90° is clockwise on screen). Hmm.

Let me define: path direction vector = (dx, dy). Text "up" vector = rotate path direction by -90°. Rotation by -90° in standard math (y-up) is (x,y)→(y,-x). But in y-down coords it flips.

This is getting too deep. Let me just use a pragmatic approach: I'll write the SVG, and for the bottom text, I'll pick the path direction that makes it readable, and if I'm unsure, I can describe it. But since I can't render, let me use the most common pattern that I'm confident about.

The most common pattern I've seen for circular text logos:

Top text (readable, upright): 
`<path id="top" d="M 50 250 A 200 200 0 0 1 450 250"/>` — L to R over top. Text upright. ✓ (I'm confident)

Bottom text (readable, upright):
`<path id="bottom" d="M 450 250 A 200 200 0 0 1 50 250"/>` — R to L under bottom. Text upright. 

I'm fairly confident the bottom text with R-to-L path gives upright text. Let me go with that.

Actually, you know what, let me reconsider. I've definitely seen that for the bottom, drawing the path from left to right (following the reading direction) gives upside-down text, and drawing right to left gives upright text. So R-to-L for bottom = upright. Good, my choice is correct.

Hmm, but actually I realize I should double-check by thinking about the "text up" direction more carefully, because getting this wrong makes the logo look bad.

Let me use a cleaner mental model. SVG text on a path: the text is rendered so that it reads in the direction of the path. Imagine walking along the path in its forward direction; the text reads as you walk, and you're walking on the "inside" with text above your head... no.

Simplest reliable model: The text baseline lies along the path. The text is on the left side of the direction of travel (because SVG text is drawn to the right of the baseline in the coordinate system, but with the path, it's... ).

OK here's the deal. Let me think about it as: the text is placed on the path such that the baseline follows the path, and the text is on the side such that reading direction is the path direction. The perpendicular "up" for the text is the path direction rotated 90° counterclockwise in SVG screen coordinates... 

In SVG screen coordinates (x right, y down):
- Path direction at a point: tangent vector T.
- The text "up" (toward ascenders) is T rotated by -90° (which in screen coords, rotating a vector (a,b) by -90° gives... rotation by angle θ: (a cosθ - b sinθ, a sinθ + b cosθ). For θ = -90°: cos(-90)=0, sin(-90)=-1. So (a*0 - b*(-1), a*(-1) + b*0) = (b, -a). So T=(a,b) rotated -90° → (b, -a).)

For bottom arc R→L at the bottom point: direction of travel is westward, T = (-1, 0) (a=-1, b=0). Text up = (b, -a) = (0, 1). (0,1) means downward in screen coords. So text extends downward = away from center = outside the circle. That means text is on the outside, and... the ascenders point down (away from center). 

For the text to be readable/upright, ascenders should point up (toward top of screen, -y direction, i.e., (0,-1)). But we got (0,1) = down. So this would be upside down!

Hmm, so R→L gives upside-down text? Let me re-examine.

Wait, let me reconsider which rotation. Maybe text up is T rotated +90°.
+90°: cos90=0, sin90=1. (a*0 - b*1, a*1 + b*0) = (-b, a). For T=(-1,0): (-0, -1) = (0,-1). That's upward. So text ascends upward = upright!

So if text up = T rotated +90°, then R→L bottom gives upright. If text up = T rotated -90°, R→L bottom gives upside-down.

I genuinely don't remember the exact convention. Let me think about the top arc to calibrate.

Top arc L→R at the top point: direction eastward, T = (1, 0). For upright text, we need text up = (0, -1) (upward on screen).
- If text up = T rotated -90° = (b, -a) = (0, -1). ✓ Upright!
- If text up = T rotated +90° = (-b, a) = (0, 1). ✗ Upside down.

So for the top arc (L→R), text up = T rotated -90° gives upright. This matches my confidence that top arc L→R is upright.

Therefore, text up = T rotated -90°.

Now bottom arc R→L at bottom: T = (-1, 0). Text up = (b, -a) = (0, 1) = downward. So text extends downward (outside circle), ascenders point down = upside down relative to us.

Wait, but "ascenders point down" — if the text's top points down (toward bottom of screen) and baseline is at the path (bottom of circle), then the letters hang below the path... no wait. Let me re-think what "text up = (0,1)" means.

If text up direction is (0,1) in screen coords (downward), then the ascenders (top of letters) point downward (toward bottom of screen), and the baseline is above them. So the letters are drawn below the baseline. Since the baseline is at the bottom of the circle (y≈450), the letters extend to y>450, i.e., below the circle. And they're upside down (ascenders pointing down).

Hmm, that means R→L bottom gives upside-down text. So for upright bottom text, I need the opposite: L→R bottom.

Let me verify with L→R bottom arc at bottom: T = (1, 0) (eastward). Text up = (b,-a) = (0,-1) = upward. Ascenders point up = upright! And baseline at bottom, letters extend upward toward center. So letters are inside the circle near the bottom, upright. 

So for upright bottom text, the path should go L→R (left to right) along the bottom.

Wait, but that seems counterintuitive. Let me re-examine. If letters extend upward from the baseline (toward center) and ascenders point up (toward top of screen), the text is upright and located inside the circle at the bottom. Reading direction: L→R along the path. Yes, that's readable and upright. 

So:
- Top arc (upright): L→R, bulging up. `M 50 250 A 200 200 0 0 1 450 250`
- Bottom arc (upright): L→R, bulging down. `M 50 250 A 200 200 0 0 0 450 250`

Wait, let me double check the bottom arc bulging down from L to R. From (50,250) left to (450,250) right, bulging down through bottom. Using sweep flag: I determined earlier that bottom arc from R to L is clockwise (sweep=1). So bottom arc from L to R is counterclockwise (sweep=0). 
`M 50 250 A 200 200 0 0 0 450 250` — sweep=0, counterclockwise, L to R, bulging down. ✓

Hold on, let me re-verify that L→R bulging down is sweep=0.
From left (50,250) [9 o'clock] to right (450,250) [3 o'clock], bulging down through bottom (6 o'clock). Path: 9→6→3. On a clock, 9→6→3 is counterclockwise (going backwards). Counterclockwise in screen view = sweep-flag=0. ✓

Great. So:
- Top: `M 50 250 A 200 200 0 0 1 450 250` (sweep=1, L→R, bulge up)
- Bottom: `M 50 250 A 200 200 0 0 0 450 250` (sweep=0, L→R, bulge down)

Both L→R, both upright. 

But wait, I should double-check my "text up = T rotated -90°" claim once more, because it's crucial. Let me sanity check with a horizontal path going right (T=(1,0)) — plain text should be upright (ascenders up, (0,-1)). Text up = T rotated -90° = (b,-a) = (0,-1). ✓. Yes! Plain horizontal text going right is upright, and my formula gives (0,-1) = up. 

And a horizontal path going left (T=(-1,0)) — text on such a path would be upside down. Text up = (b,-a) = (0,1) = down. ✓ Upside down. Makes sense (you can't read text flowing right-to-left normally).

Great, I'm confident now:
- Top arc: `M 50 250 A 200 200 0 0 1 450 250`
- Bottom arc: `M 50 250 A 200 200 0 0 0 450 250`

Both with text-anchor="middle" and startOffset="50%".

Now, one more consideration: the text should sit within the gold ring band. The ring is between r=216 and r=232. My arcs are at r=200, which is inside the ring (inside the inner edge at 216). That would put text inside the ring, not on it. Let me move the arcs out to sit on the ring.

Actually, let me reconsider the whole emblem structure. Let me make:
- Outer gold ring: r from 218 to 234 (band width 16)
- Text arcs should be within this band.

For top text, the arc should be around r=226 (middle of band), bulging up. At the top, the text baseline at r=226 means baseline y = 250-226 = 24. Text extends up to y≈24-30 = -6 (off screen) — too high. Font size 30, the letters are about 30px tall, so from baseline at y=24 up to y=-6. That's slightly off-screen (clipped). Let me use a smaller radius or accept slight clip, or reduce font.

Hmm. Let me reconsider. Let me make the arcs a bit smaller radius so text fits.

If baseline at r=224 (y=26 for top), and font cap height ~21px (for font-size 30), letters span y=26 down... no, up to y=26-21=5. Slightly clipped at top (svg goes to y=0). y=5 is fine, just barely. Actually the top of the letter would be at y≈5, within the 0-500 viewbox. OK but tight.

Let me reduce font size to 26 and radius to 220. Baseline top: y=250-220=30. Letters up to y=30-19=11. Fine.

Actually, let me reconsider — maybe I'm overcomplicating with the ring. Let me simplify the emblem:

Let me make a cleaner design:
- A filled circle background for the emblem (dark blue), with a gold ring border.
- Owl in the center.
- Text on the ring (gold text or white text).

Wait, but the user said "no background" ideally. A circular emblem with a filled background is part of the logo design, not the page background. I think a circular emblem is fine and looks professional. But to respect "no background," I'll keep the overall SVG background transparent (no full-page rect), and the emblem itself is the logo.

Hmm, but "fondo einfarbig" (solid colored background) OR "no background." Let me interpret: they want either a solid background color or transparency. Since they said "am besten besitzt das Logo gar keinen Hintergrund" (best if the logo has no background at all), I'll make it transparent (no background rect). The emblem will be just the ring + owl + text, no filled circle behind. That respects "no background."

But a ring without a filled center might look a bit sparse. That's OK — it's a clean, transparent-background logo. Many sports logos are just the emblem outline + graphic.

Actually, let me add a subtle filled circle in a dark color to make the owl pop, but keep it as part of the emblem (not page background). Hmm, but that contradicts "no background." 

Let me go with: transparent background, gold ring, owl, text. Clean. The owl has its own colors. This looks good and respects the no-background request.

Let me reconsider text color. On a transparent background, with just a gold ring, the text should be a dark color to be readable. Let me use dark blue (#1c3055) or near-black for the text. Actually, let me use a dark navy so it reads on any background.

Hmm, but if the text is on the gold ring and the text is dark navy, that reads well. Let me use dark navy text.

Wait, actually, let me reconsider the whole color scheme for maximum appeal:
- Gold ring: #f4c20d / #e0a800
- Owl: blues and whites (owl is grey/brown in reality, but for a hockey team let me use a nice palette)
- Text: dark navy

Let me make the owl more owl-like with grey/brown tones, or go with a stylized blue owl. For "Eulers" (owls), a grey/brown owl is natural. But hockey teams often use bold colors. Let me do a nice owl with slate blue/grey body and a gold/amber accent.

Let me finalize the palette:
- Ring: gold (#f5c518 outer, #d99f00 inner shadow)
- Owl body: slate grey-blue (#5a6b7f to #33414f) — like a real owl
- Owl belly: lighter cream (#e8e2d0)
- Eyes: amber/gold (#f4c20d with dark center)
- Beak: dark grey/charcoal
- Wings: darker slate
- Text: deep navy (#1a2740) or gold

Hmm, let me make it cohesive. Let me use:
- Owl: slate blue-grey gradient
- Eyes: bright amber/gold (pop)
- Beak: charcoal
- Ring: gold
- Text: gold on... no. Let me make text navy.

Actually for a hockey team "Eulers," let me go with a bold look:
- Primary: deep navy (#16223b) and gold (#f5c518)
- Owl body: navy gradient with lighter navy highlights
- Eyes: gold
- Belly: lighter (#c8d6ea)
- Beak: gold or charcoal
- Ring: gold
- Text: navy (top and bottom) — reads on gold ring and transparent

Let me go with this. It's clean and sporty.

Let me now write the complete SVG carefully.

Let me reconsider the owl to make it look good. I'll make it a friendly, bold owl.

Let me define the owl elements:

1. Body: ellipse, cx=250, cy=315, rx=92, ry=108. Gradient navy.
2. Head: I'll blend head into body. Eyes placed high.
3. Ear tufts: two pointed shapes at top.
4. Eyes: large circles.
5. Beak: small, between eyes.
6. Wings: two shapes on sides.
7. Belly: lighter ellipse with chevron feathers.
8. Feet: two small feet at bottom (optional).

Let me place eyes at cy=235, cx=208 and cx=292. Radius 40.

Beak at (250, 268).

Let me write it all.

Actually, let me reconsider making the owl more detailed and attractive. Let me add:
- Feather texture on belly (chevrons)
- Eye rings (lighter circle around iris)
- Eye shine highlights
- Wing feather lines

Let me write the full SVG now.

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 500 500" width="500" height="500">
  <defs>
    <linearGradient id="bodyGrad" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#4a5a72"/>
      <stop offset="0.55" stop-color="#33415a"/>
      <stop offset="1" stop-color="#232f42"/>
    </linearGradient>
    <linearGradient id="wingGrad" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#3a485e"/>
      <stop offset="1" stop-color="#212c3d"/>
    </linearGradient>
    <radialGradient id="eyeGrad" cx="0.5" cy="0.35" r="0.7">
      <stop offset="0" stop-color="#ffe08a"/>
      <stop offset="0.55" stop-color="#ffbf21"/>
      <stop offset="1" stop-color="#c98a00"/>
    </radialGradient>
    <linearGradient id="bellyGrad" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#e9edf4"/>
      <stop offset="1" stop-color="#c2cddf"/>
    </linearGradient>
    <linearGradient id="stickGrad" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="#d19a55"/>
      <stop offset="1" stop-color="#8a5522"/>
    </linearGradient>
  </defs>
  
  <!-- ===== Hockey stick ===== -->
  <g transform="rotate(-32 255 250)">
    <rect x="244" y="55" width="16" height="300" rx="8" fill="url(#stickGrad)" stroke="#5c3a1a" stroke-width="1.5"/>
    <path d="M 244 348 L 260 348 L 262 406 Q 262 430 238 432 L 202 428 Q 187 426 189 409 L 194 376 Q 196 359 212 359 Z"
          fill="url(#stickGrad)" stroke="#5c3a1a" stroke-width="1.5"/>
    <rect x="191" y="372" width="66" height="7" rx="3.5" fill="#f6f6f6" opacity="0.92"/>
  </g>
  
  <!-- ===== Emblem ring ===== -->
  <circle cx="250" cy="250" r="234" fill="none" stroke="#f5c518" stroke-width="14"/>
  <circle cx="250" cy="250" r="220" fill="none" stroke="#c99300" stroke-width="3"/>
  
  <!-- ===== Text ===== -->
  <path id="topArc" d="M 48 250 A 202 202 0 0 1 452 250" fill="none"/>
  <path id="bottomArc" d="M 48 250 A 202 202 0 0 0 452 250" fill="none"/>
  <text font-family="'Arial Black', Arial, Helvetica, sans-serif" font-weight="bold" font-size="30" letter-spacing="3" fill="#16223b">
    <textPath href="#topArc" startOffset="50%" text-anchor="middle">OWAYO</textPath>
  </text>
  <text font-family="'Arial Black', Arial, Helvetica, sans-serif" font-weight="bold" font-size="30" letter-spacing="4" fill="#16223b">
    <textPath href="#bottomArc" startOffset="50%" text-anchor="middle">EULERS</textPath>
  </text>
  
  <!-- ===== Owl ===== -->
  <!-- body -->
  <ellipse cx="250" cy="318" rx="94" ry="110" fill="url(#bodyGrad)" stroke="#1a2333" stroke-width="2"/>
  
  <!-- ear tufts -->
  <path d="M 186 208 Q 164 156 196 166 Q 210 190 222 212 Z" fill="url(#bodyGrad)" stroke="#1a2333" stroke-width="1.5"/>
  <path d="M 314 208 Q 336 156 304 166 Q 290 190 278 212 Z" fill="url(#bodyGrad)" stroke="#1a2333" stroke-width="1.5"/>
  
  <!-- wings -->
  <path d="M 164 296 Q 132 336 150 392 Q 160 418 186 410 Q 172 358 186 306 Q 190 288 174 283 Z" fill="url(#wingGrad)" stroke="#1a2333" stroke-width="2"/>
  <path d="M 336 296 Q 368 336 350 392 Q 340 418 314 410 Q 328 358 314 306 Q 310 288 326 283 Z" fill="url(#wingGrad)" stroke="#1a2333" stroke-width="2"/>
  
  <!-- belly -->
  <ellipse cx="250" cy="348" rx="60" ry="72" fill="url(#bellyGrad)"/>
  <g stroke="#99a9c4" stroke-width="2.2" fill="none" opacity="0.85">
    <path d="M 220 326 Q 250 342 280 326"/>
    <path d="M 222 352 Q 250 368 278 352"/>
    <path d="M 225 378 Q 250 394 275 378"/>
    <path d="M 229 402 Q 250 415 271 402"/>
  </g>
  
  <!-- eyes -->
  <circle cx="208" cy="238" r="42" fill="#f3f6fb" stroke="#1a2333" stroke-width="2"/>
  <circle cx="292" cy="238" r="42" fill="#f3f6fb" stroke="#1a2333" stroke-width="2"/>
  <circle cx="208" cy="238" r="28" fill="url(#eyeGrad)"/>
  <circle cx="292" cy="238" r="28" fill="url(#eyeGrad)"/>
  <circle cx="208" cy="240" r="15" fill="#141a26"/>
  <circle cx="292" cy="240" r="15" fill="#141a26"/>
  <circle cx="201" cy="231" r="5.5" fill="#ffffff"/>
  <circle cx="285" cy="231" r="5.5" fill="#ffffff"/>
  
  <!-- beak -->
  <path d="M 234 266 Q 250 258 266 266 Q 262 284 250 294 Q 238 284 234 266 Z" fill="#e0a52a" stroke="#a67713" stroke-width="1.5"/>
  
  <!-- feet -->
  <path d="M 222 420 L 216 442 Q 214 450 222 449 L 232 447" fill="none" stroke="#e0a52a" stroke-width="4" stroke-linecap="round"/>
  <path d="M 278 420 L 284 442 Q 286 450 278 449 L 268 447" fill="none" stroke="#e0a52a" stroke-width="4" stroke-linecap="round"/>
</svg>
```

Wait, the feet at y=442-450 would be below the owl body (body bottom at cy=318+110=428). The feet extend to y=450. But the inner ring is at r=220, so at the bottom, the ring is at y=250+220=470. So feet at y=450 are inside the ring. OK.

But wait, the owl body bottom is at y=428, and the stick blade is around y=432 (in rotated frame). Let me make sure things don't overlap badly. The stick is rotated -32°, so it's diagonal. The blade end... let me check where it ends.

The stick group is rotated -32° around (255, 250). The stick in unrotated coords: shaft from y=55 to y=355, x=244-260. Blade around y=359-432.

After rotating -32° around (255,250):
The blade tip at (210, 430) roughly. Let me compute rotation.

Rotation by -32° (clockwise in screen? -32° is counterclockwise in screen coords since positive is clockwise in SVG... wait, SVG rotate(angle) positive = clockwise on screen). So rotate(-32) = counterclockwise 32°.

Point (210, 430) relative to center (255,250): (-45, 180). Rotate by -32°:
Rotation matrix for angle θ (SVG, clockwise positive): 
x' = x cosθ - y sinθ
y' = x sinθ + y cosθ
For θ = -32°: cos(-32)=0.848, sin(-32)=-0.530.
x' = -45*0.848 - 180*(-0.530) = -38.16 + 95.4 = 57.24
y' = -45*(-0.530) + 180*0.848 = 23.85 + 152.6 = 176.45
Absolute: (255+57.24, 250+176.45) = (312, 426). 

Hmm, that puts the blade around (312, 426). And the top of the stick (250, 55) relative to center (-5, -195):
x' = -5*0.848 - (-195)*(-0.530) = -4.24 - 103.35 = -107.6
y' = -5*(-0.530) + (-195)*0.848 = 2.65 - 165.36 = -162.7
Absolute: (255-107.6, 250-162.7) = (147, 87).

So the stick goes from ~(147, 87) top-right... wait, (147,87) is upper-left, and blade at (312, 426) is lower-right. So the stick is diagonal from upper-left to lower-right. Hmm, that's fine, it's behind the owl.

Actually wait, let me reconsider. The stick handle top is at (147, 87) and blade at (312, 426). So it goes from upper-left to lower-right diagonally. The owl is in the center. This should look OK — a hockey stick held diagonally behind the owl.

But the blade at (312, 426) — is that within the emblem? Inner ring at bottom is y=470, at x=250. At x=312, the ring... the circle x²+y²... point (312,426): distance from center (250,250) = sqrt(62²+176²)=sqrt(3844+30976)=sqrt(34820)=186.6. Inner ring r=220. So 186 < 220, inside. Good, blade is inside the emblem.

The stick handle top at (147,87): distance = sqrt(103²+163²)=sqrt(10609+26569)=sqrt(37178)=193. Inside 220. Good.

OK the stick fits. But it might overlap the owl a lot. Since it's behind the owl (drawn first), the owl covers the middle. The visible parts are the top handle (upper left) and blade (lower right). That's a nice look — like the owl is holding/behind a hockey stick.

Hmm, actually, let me reconsider. Maybe having the stick more visible and clearly a hockey stick is better. Let me make it a bit more prominent, or reconsider.

Actually, a common hockey logo has the hockey stick(s) crossed behind a central emblem. Here we have an owl central. One stick behind, diagonal, is fine and clear.

Let me reconsider the stick length and position so both ends are nicely visible and it looks intentional.

Let me keep it. But let me double check the blade shape looks like a hockey stick blade. My blade path:
`M 244 348 L 260 348 L 262 406 Q 262 430 238 432 L 202 428 Q 187 426 189 409 L 194 376 Q 196 359 212 359 Z`

This creates a blade that extends down and curves left with tape. After rotation it becomes the lower-right portion. Should look like a hockey stick blade. Good enough.

Actually, I realize the blade tape rect (191,372,66x7) is in the unrotated frame, positioned horizontally across the blade. After rotation it'll be diagonal. That represents tape on the blade. Fine.

Hmm, let me reconsider whether the stick looks right. Let me simplify the blade to be more clearly a hockey stick. A hockey stick blade from the side view is like a flat paddle with a curve. From a 2D front-ish view, it's an L-shape: shaft vertical, blade horizontal at the bottom.

Let me make the blade more clearly an L-shape (horizontal blade at bottom):

Unrotated stick (pointing down):
- Shaft: vertical rect
- Blade: horizontal piece at the bottom, curving up at the ends

```
Shaft: rect x=244 y=55 w=16 h=290 (to y=345)
Blade: from x=190 to x=270 at the bottom, y≈340-365, with a slight curve
```

Blade path (L-shape, viewed from front):
```
M 244 340
L 270 340
L 270 360
Q 270 372 258 372
L 212 370
Q 198 368 198 354
L 198 344
L 210 344 L 210 356 L 250 357 L 250 342 Z
```

Hmm, this is getting messy. Let me simplify.

Let me make the blade a simple curved paddle:
```
M 244 342 
L 268 342 
L 268 362 
Q 268 374 250 374 
L 214 372 
Q 198 370 198 356 
L 198 344 
L 210 344 
L 210 354 
L 244 355 Z
```

This makes an L-shape blade. The tape line across it. OK.

Actually, let me step back. I'm spending too much effort on the stick. Let me make a clean, recognizable hockey stick and move on.

Let me define the hockey stick as:
- A long shaft (thin rounded rect), rotated.
- A blade at one end (a flat curved piece).

I'll place it diagonally. Let me use a cleaner blade.

Final stick (unrotated, pointing down, centered around x=252):
```svg
<g transform="rotate(-30 252 248)">
  <!-- shaft -->
  <rect x="246" y="60" width="14" height="290" rx="7" fill="url(#stickGrad)" stroke="#5c3a1a" stroke-width="1.5"/>
  <!-- blade -->
  <path d="M 246 346 L 266 346 L 266 396 Q 266 414 246 414 L 214 410 Q 198 408 199 392 L 201 362 Q 202 349 214 349 L 246 349 Z" 
        fill="url(#stickGrad)" stroke="#5c3a1a" stroke-width="1.5"/>
  <!-- tape -->
  <rect x="200" y="357" width="64" height="7" rx="3.5" fill="#f4f4f4" opacity="0.9"/>
</g>
```

This blade: at the shaft bottom (y=346), it widens and curves down into a blade that bulges left and down, with rounded bottom. Tape is a horizontal bar. After rotation -30°, it's diagonal. Looks like a hockey stick. Good.

Let me verify the blade is recognizable: it's an L-shape (vertical shaft + horizontal-ish blade that curves). Yes.

Now let me reconsider: with the stick behind the owl, and the owl body from cy=318 ry=110 (so y=208 to 428), x from 156 to 344. The stick diagonal passes through. The visible stick parts: upper-left (handle) and lower-right (blade). Should be OK.

Hmm, wait. Let me reconsider the rotation center and make sure the stick looks balanced. Let me use rotate(-30 250 250).

Let me also reconsider: maybe the stick should be in front of nothing and clearly visible. Let me make sure the owl doesn't completely cover it. The owl body is centered; the stick diagonal from upper-left to lower-right. The owl covers the center. So handle (upper-left, ~150,90) and blade (lower-right, ~350,410) are visible. Good.

Actually, let me reconsider the direction. I want the stick to look like it's behind the owl, going from lower-left to upper-right perhaps, or it doesn't matter much. Let me keep upper-left handle to lower-right blade.

Hmm, actually for a "held by the owl" look, maybe two sticks crossed would be cooler, but one is cleaner and the user asked for "Eishockeyschläger" (singular-ish, could be one). Let me do one stick. Actually "Eishockeyschläger" is the noun for hockey stick/sticks. One is fine.

Wait, let me reconsider — maybe I should make the stick clearly visible and prominent, not hidden behind the owl. Let me reconsider the composition.

Alternative: Put the hockey stick to one side, not behind the owl. Like the owl on the left, stick on the right, or stick diagonal behind with both ends showing.

Actually, a nice composition: owl centered, hockey stick diagonal behind, both ends peeking out. This is classic. Let me keep it.

But let me make sure the stick is long enough that both ends clearly show outside the owl. Handle end at ~(150, 90) — that's well clear of the owl (owl top at y=208). Blade end at ~(350, 410) — owl right edge at x=344, bottom at y=428. So blade at (350,410) is just outside the owl to the right. Hmm, might be partially covered. Let me adjust so the blade is clearly outside.

Let me increase the stick length or adjust rotation so the blade is more clearly visible. Let me extend the shaft so the blade end is further out.

Actually, let me reconsider by making the stick longer and the rotation such that it's clearly visible.

Let me reconsider: I want the stick to go from upper-left to lower-right, with:
- Handle end: upper-left, clearly visible (e.g., around (140, 95))
- Blade end: lower-right, clearly visible (e.g., around (360, 415))

With rotation -30° around (250,250), and I want blade end at ~(360,415).
(360,415) relative to center: (110, 165). To find unrotated position, rotate by +30°:
cos30=0.866, sin30=0.5.
x = 110*0.866 + 165*0.5 = 95.26 + 82.5 = 177.76
y = -110*0.5 + 165*0.866 = -55 + 142.89 = 87.89
So unrotated blade end at (250+177.76, 250+87.89) = (428, 338). 

Hmm, that means in unrotated frame, the blade is at x=428 (far right) and y=338. That's a very long/offset stick. That doesn't match a downward-pointing stick.

I think I'm overcomplicating. Let me just pick a rotation and stick, render mentally, and adjust if needed. Since I can't actually render, let me make reasonable choices.

Let me use a simpler, robust approach: place the stick as a clear diagonal line shape without worrying too much about exact coordinates, centered in the emblem.

Let me define the stick in a rotated coordinate system directly using a transform, and make it symmetric-ish.

Actually, the cleanest: define the stick pointing straight down (shaft vertical, blade at bottom), then rotate the whole group. The rotation makes it diagonal. The center of rotation should be near the owl center so it's centered.

Let me set rotation center at (250, 245) and angle -28°.

Stick (unrotated):
- Shaft: x from 245 to 255, y from 70 to 350. (centered x=250)
- Blade: centered around x=250, y from 345 to 410, extending left.

After rotate(-28° 250 245):
Top of shaft (250,70): rel (0,-175), rotate -28: 
x' = 0*cos(-28) - (-175)*sin(-28) = 0 - (-175)*(-0.469) = -82.1
y' = 0*sin(-28) + (-175)*cos(-28) = 0 + (-175)*(0.883) = -154.5
abs: (250-82, 245-154) = (168, 91). Top handle at (168,91). Clear of owl (owl top y=208). 

Blade center (235, 400): rel (-15, 155), rotate -28:
x' = -15*0.883 - 155*(-0.469) = -13.2 + 72.7 = 59.5
y' = -15*(-0.469) + 155*0.883 = 7.0 + 136.9 = 143.9
abs: (309, 389). Blade at (309, 389). Owl right edge ~x=344, so x=309 is inside owl width. Owl bottom y=428, so y=389 inside. Hmm, blade at (309,389) is inside the owl (owl spans x 156-344, y 208-428). So the blade would be covered by the owl. Not good.

The problem: the stick is too short / positioned so the blade is behind the owl's body.

I need the stick longer so the blade extends beyond the owl, OR position the owl smaller, OR put the stick more to the side.

Let me make the stick longer. Extend shaft to y=400 (unrotated), blade at y=400-445.

Blade center (235, 430): rel (-15, 185), rotate -28:
x' = -15*0.883 - 185*(-0.469) = -13.2 + 86.8 = 73.6
y' = -15*(-0.469) + 185*0.883 = 7.0 + 163.4 = 170.4
abs: (323, 415). Still inside owl (x<344, y<428). Barely.

Hmm. The owl is big. Let me reduce owl size or move stick.

Alternative approach: Don't rotate the stick into the owl. Instead, place the stick diagonally such that it's clearly behind and both ends outside the owl, by making the owl smaller and the stick longer, OR by placing the stick to the side.

Let me reconsider the whole composition. Options:

Option A: Owl centered and large, hockey stick diagonal behind with ends outside. Requires long stick + appropriately sized owl.

Option B: Owl on one side, hockey stick on the other side, side by side within the emblem.

Option C: Owl centered, hockey stick behind but mostly hidden, just handle poking out top and blade poking out bottom-right.

Let me go with a cleaner Option A but tune sizes.

Let me make the owl a bit smaller: body rx=80, ry=95, cy=320. So owl spans x 170-330, y 225-415.

Stick: longer. Shaft x=246-254, y=65 to 380. Blade at y=380-430, extending left to x=205.

Rotate(-26° 250 248):
Shaft top (250,65): rel (0,-183), rotate -26 (cos26=0.898, sin26=0.438):
x' = 0 - (-183)*(-0.438) = -80.2
y' = 0 + (-183)*0.898 = -164.3
abs: (170, 84). Handle top at (170,84). Clear.

Blade center (220, 415): rel (-30, 167), rotate -26:
x' = -30*0.898 - 167*(-0.438) = -26.9 + 73.1 = 46.2
y' = -30*(-0.438) + 167*0.898 = 13.1 + 149.9 = 163
abs: (296, 411). Blade at (296,411). Owl: x 170-330 (296 inside), y 225-415 (411 inside, just). So blade bottom near owl bottom edge. Partially covered.

This is frustrating. The issue is the diagonal stick's lower end lands inside the owl's footprint.

Let me think differently. The owl occupies roughly a circle of radius ~95 centered at (250, 310) (lower center). The emblem circle radius ~220. For a diagonal stick to have both ends outside the owl, the stick must pass such that its ends are in the ring area.

If the stick goes from upper-left (near top-left of ring) to lower-right (near bottom-right of ring), it passes through the center where the owl is. The owl (radius 95) covers the center. So the middle of the stick is covered, but the ends (in the ring area, radius 190-220) stick out. Let me check: upper-left end at radius ~190 (handle at (170,84), distance from owl center (250,310): sqrt(80²+226²)=sqrt(6400+51076)=sqrt(57476)=240). So handle is at distance 240 from owl center, well outside owl (radius 95). Good, handle fully clear.

Lower-right blade end: I computed (296,411), distance from owl center (250,310): sqrt(46²+101²)=sqrt(2116+10201)=sqrt(12317)=111. That's just outside owl radius 95. So blade is barely clear (111 > 95). OK so it's clear but close. The blade has some width, so part might overlap. Let me push it a bit more by making the stick longer or owl smaller.

Let me make owl body rx=78, ry=90, cy=315. And stick longer (blade at unrotated y=430).

Actually, let me just make the stick end clearly outside by extending it, and accept the blade will be in the lower-right ring area. Let me compute with a longer stick.

Shaft y=60 to 375. Blade extends to unrotated (215, 440).
Rotate(-26° 250 248):
Blade (215,440): rel (-35, 192), rotate -26:
x' = -35*0.898 - 192*(-0.438) = -31.4 + 84.1 = 52.7
y' = -35*(-0.438) + 192*0.898 = 15.3 + 172.4 = 187.7
abs: (303, 436). Distance from owl center (250,315): sqrt(53²+121²)=sqrt(2809+14641)=sqrt(17450)=132. Clear (132>90). 

So with a longer stick (blade at unrotated ~440) and owl cy=315 ry=90, the blade is clear. Let me use that.

But wait, I also need the blade to not go outside the emblem ring (radius 220). Blade at (303,436): distance from emblem center (250,250): sqrt(53²+186²)=sqrt(2809+34596)=sqrt(37405)=193.4. Under 220. Good, inside ring.

And handle at (170,84): distance from (250,250): sqrt(80²+166²)=sqrt(6400+27556)=sqrt(33956)=184.3. Under 220. Good.

So both ends are within the ring and clear of the owl. 

Let me set:
- Owl body: cx=250, cy=315, rx=78, ry=90.

Hmm wait, but I had eyes at cy=238 and the body top should include the head. Let me reconsider owl proportions. Let me make the owl head and body as one rounded shape.

Let me redefine the owl as a cohesive shape:
- Body/head: one big rounded ellipse cx=250, cy=300, rx=88, ry=110. This spans y=190 to 410, x=162 to 338.
- Eyes at cy=235.
- Belly lower.

But then the body top (y=190) is above the eyes. And ear tufts at top.

Let me reconsider. For the stick clearance, the owl should not extend too far down-right. Body cy=300 ry=110 → bottom y=410. At the lower right, the owl edge... the blade at (303,436) is below and right. Distance from body center (250,300): sqrt(53²+136²)=sqrt(2809+18496)=sqrt(21305)=146. Body rx=88, ry=110. The point (303,436) relative: dx=53, dy=136. In ellipse terms: (53/88)²+(136/110)² = 0.362 + 1.526 = 1.89 > 1, so outside the ellipse. Good, clear.

OK let me finalize owl body: cx=250, cy=300, rx=88, ry=110.

Hmm, but earlier I wanted belly lower. Let me just make body cx=250 cy=305 rx=85 ry=110. Bottom y=415.

Let me not overthink and just write it, then sanity check overlaps.

Let me also reconsider: do I even want the stick behind, or should I make it more prominent in front? Let me put it behind (drawn first) so the owl is the star. Both ends visible. Good.

Let me also add a subtle shadow or make the owl pop. I'll keep it flat/clean.

Let me also reconsider adding a small hockey puck for fun. Optional. Maybe add a puck near the blade. Let me add a black ellipse (puck) near the blade for context. Actually, let me keep it minimal — owl + stick + text. Adding a puck could be a nice touch but might clutter. Let me add a small puck near the blade; it reinforces "hockey." Actually, let me skip the puck to keep it clean, or add it. I'll add a small puck — it's a nice detail. Hmm, but it might look like it's floating. Let me place it right at the blade tip. Actually, let me skip the puck; the stick is enough.

Let me reconsider the design once more and then write final.

Final composition:
1. Transparent background.
2. Gold ring (outer thick + thin inner line).
3. Curved text: "OWAYO" top, "EULERS" bottom, dark navy.
4. Hockey stick diagonal behind (handle upper-left, blade lower-right), wood gradient with tape.
5. Owl centered:
   - Body ellipse (navy gradient)
   - Ear tufts
   - Wings
   - Belly (light) with chevron feathers
   - Two big eyes (white ring, amber iris, dark pupil, shine)
   - Beak (amber)
   - Feet (amber) at bottom

Let me write it all out cleanly now.

Let me refine the owl body to look more owl-like. I'll add a slightly darker outline and maybe eyebrow bumps.

Actually, let me make the head a distinct rounder shape and body a bit narrower at the bottom (like an owl sitting). I could use a path for the body. But an ellipse is simpler and looks fine. Let me use ellipse.

Let me write final SVG.

For the eyes, let me make them a bit more striking with a thin dark ring and lighter eyelid.

Let me also make sure the beak is visible between the eyes. Eyes at cx=212 and cx=288, cy=235, r=40. So inner edges at x=252 and x=248. Gap between eyes is only 4px (248 to 252). That's too close; beak won't fit. Let me move eyes wider: cx=206 and cx=294, cy=235, r=38. Inner edges at x=244 and x=256. Gap 12px. Beak width ~20. Still tight. Let me move eyes to cx=202 and cx=298, r=38. Inner edges at 240 and 256, gap 16px. Beak from x=238 to 262. Overlaps eyes slightly. Hmm.

Let me make eyes smaller and positioned so beak fits. Eyes cx=205, cx=295, cy=232, r=36. Inner edges at 241 and 255. Gap 14. Beak: triangle from (243,255) to (257,255) to (250,278). Beak top at y=255, below the eyes (eyes center 232, bottom at 268). Wait eyes bottom at cy+r=232+36=268. So beak at y=255 would overlap eyes bottom. Let me put beak lower, at y=262-285.

Let me place beak as a small shape at (250, 268): from (240,262) to (260,262) to (250,288). This is below the eye centers and between them. Eyes bottom at 268, beak top at 262 — slight overlap but beak is narrow. Should look OK (beak sits between/just below eyes).

Actually owls' beaks are below the eyes, in the center of the face. Let me place beak at cy≈268, clearly below eyes. Eyes cy=230, r=36, bottom at 266. Beak top at 266, so beak starts right at eye bottom. Beak from y=266 to y=290. That works — beak just below eyes.

Let me set:
- Eyes: cx=205 & 295, cy=228, r=37.
- Beak: (250, 268) area, small downward triangle/paddle.

Let me finalize coordinates:
- Eyes left: cx=205, cy=228, r=37. Right: cx=295, cy=228, r=37.
- Iris r=25, pupil r=13.
- Beak: path from (240,258) to (260,258) curving to (250,286).

Let me write the beak:
`M 240 258 Q 250 252 260 258 Q 257 274 250 283 Q 243 274 240 258 Z`
Fill amber, stroke darker.

Now ear tufts. Head is the body ellipse top. Body cx=250 cy=300 rx=88 ry=110 → top at y=190. Ear tufts at top corners, around (180,175) and (320,175).

Ear tuft left: `M 188 196 Q 165 150 194 160 Q 206 182 216 202 Z` — a pointed feather. Let me make it look like an ear/fuft.

Hmm, let me make ear tufts as two pointed shapes sticking up from the top of the head:
Left: from ~(190,195) up to a point at ~(172,155).
`M 192 198 L 172 156 L 206 190 Z` — a triangle-ish fuft.
Right: `M 308 198 L 328 156 L 294 190 Z`.

Let me refine to look natural. Owl ear tufts are like pointed hair clusters. Let me do:
Left: `M 190 196 Q 174 162 196 166 Q 206 182 214 200 Z`
Right: `M 310 196 Q 326 162 304 166 Q 194... ` let me mirror: `M 310 196 Q 326 162 304 166 Q 294 182 286 200 Z`

OK.

Wings: on the sides of the body. Left wing around x=165-190, y=280-380. Right mirror.

Left: `M 172 288 Q 142 320 154 372 Q 162 396 184 388 Q 172 342 182 300 Q 186 284 172 288 Z`
Right: `M 328 288 Q 358 320 346 372 Q 338 396 316 388 Q 328 342 318 300 Q 314 284 328 288 Z`

Belly: ellipse cx=250 cy=340 rx=55 ry=64, light fill. Chevron feathers inside.

Feet: at bottom of body, y≈408. Two amber feet.
Left: from (232,408) down. Right: from (268,408) down.
`M 232 406 L 228 428 Q 226 436 234 435 L 244 433` etc. Let me make simple clawed feet.

Actually, feet might stick out below the body and look odd. Let me place feet at the very bottom, peeking out. Body bottom at y=410. Feet from y=408 to y=432. They'll be below the body, inside the ring (ring bottom at y=470). OK.

Let me finalize everything and write it.

Let me reconsider the belly position. Body cx=250 cy=300. Belly ellipse cx=250 cy=345 rx=52 ry=60. This is in the lower body. Chevrons inside.

Chevrons (y around 325-395):
```
<path d="M 224 328 Q 250 342 276 328"/>
<path d="M 226 352 Q 250 366 274 352"/>
<path d="M 228 376 Q 250 390 272 376"/>
<path d="M 231 400 Q 250 411 269 400"/>
```

OK. Let me write the complete SVG now. I'll assemble all parts.

Let me also double check the text arcs fit and don't overlap the owl. Text arcs at radius 202. Owl body top at y=190 (radius from center 250: 60 up... wait body top y=190, that's radius 60 above center, but the body is an ellipse so at the top center it's at y=190). The text top arc at radius 202, at the top is y=250-202=48. So top text baseline at y=48, letters extend up to y≈48-21=27. The owl top at y=190 is well below. No overlap. Good.

Bottom text arc at radius 202, at bottom y=250+202=452. Letters extend down to y≈452+... no wait, for bottom text L→R, ascenders point up (toward center), so letters extend from baseline (y=452) upward to y≈452-21=431. Wait, that means letters are between y=431 and y=452, just inside the ring (ring inner at 220 → bottom y=470). And the owl bottom at y=410. So text (y=431-452) is below owl bottom (410). No overlap. Good. But the stick blade is around (303,436) — that's near the bottom text area (y=431-452, x=303). The bottom text at x=303... the text "EULERS" is centered at bottom (x=250), spanning maybe x=195-305. So at x=303 there might be the end of "EULERS" or near it. The blade at (303,436) could overlap the text "EULERS" near its end. Hmm.

Let me check: "EULERS" 6 chars, font-size 30, letter-spacing 4. Approx width = 6*~18 + 5*4 = 108+20 = 128px, centered at x=250, so spans x=186 to 314. The blade at x=303 is near the right end of the text (R is around x=305). Overlap possible.

To avoid, let me either shorten the stick blade or move it, or reduce text size, or make the stick end before reaching the text.

The blade center at (303,436). The bottom text is at y=431-452. So the blade is at the same height as the text. Overlap.

Options:
1. Make the stick shorter so blade doesn't reach x=303.
2. Rotate more steeply so blade is lower/right, away from text.
3. Move text to not be at the very bottom (but it should be).

Let me reconsider the rotation to place the blade lower and to the right, away from the bottom text.

If I rotate the stick more (e.g., -40°), the blade end moves. Let me compute blade position with different rotation.

Actually, the issue is the blade is at the bottom-right, and the bottom text spans the bottom. Any stick end in the bottom region overlaps text.

Solution: make the stick's blade end point more toward the right side (3 o'clock) rather than bottom (6 o'clock), so it's near the text's right area but... the text is at the bottom. Hmm.

Alternatively, put the stick handle (plain end) at bottom-right and blade elsewhere. Or just make the stick shorter.

Let me make the stick shorter so both ends are in the upper portion, away from bottom text. But then it might not look like a full hockey stick.

Alternatively, accept that the stick is behind and the text is in front (text drawn after stick), so text covers the stick where they overlap. Since I draw the stick first, then the owl, then the text last, the text would be on top. So even if they overlap, text is visible. But the stick over the text looks messy.

Let me reorder: stick → owl → text. Text on top. Where stick and text overlap, text shows. The stick blade at (303,436) over text "EULERS" end — text on top, so text visible, stick hidden behind text. That's acceptable! The stick just won't be visible under the text. Fine.

But actually, cleaner to avoid overlap entirely. Let me make the stick end before the text region.

Let me reduce the stick length. Shorter stick: blade end at unrotated (220, 400).
Rotate(-26° 250 248):
(220,400): rel (-30,152), rotate -26:
x' = -30*0.898 - 152*(-0.438) = -26.9 + 66.6 = 39.7
y' = -30*(-0.438) + 152*0.898 = 13.1 + 136.5 = 149.6
abs: (290, 398). Blade at (290,398). Text at y=431-452. Blade at y=398 is above text. No vertical overlap! Good.

And handle end: shaft top at unrotated (250,65). Rotate(-26): computed earlier (170,84). Clear.

So with a shorter stick (shaft y=65 to ~360, blade to y=400), blade end at (290,398), which is above the bottom text (y≥431). No overlap. 

Let me set stick: shaft x=246-254, y=65 to 355. Blade from y=355 to y=400.

Let me define:
```svg
<g transform="rotate(-26 250 248)">
  <rect x="246" y="65" width="14" height="292" rx="7" fill="url(#stickGrad)" stroke="#5c3a1a" stroke-width="1.5"/>
  <path d="M 246 350 L 260 350 L 260 396 Q 260 412 242 412 L 214 408 Q 200 406 201 392 L 203 366 Q 204 353 216 353 L 246 353 Z" fill="url(#stickGrad)" stroke="#5c3a1a" stroke-width="1.5"/>
  <rect x="203" y="360" width="54" height="6" rx="3" fill="#f4f4f4" opacity="0.9"/>
</g>
```

Blade end ~ (214, 410) unrotated → rotate(-26):
(214,410): rel (-36,162), rotate -26:
x' = -36*0.898 - 162*(-0.438) = -32.3 + 70.9 = 38.6
y' = -36*(-0.438) + 162*0.898 = 15.8 + 145.5 = 161.3
abs: (289, 409). Blade tip at (289,409). Text at y=431+. Clear (409<431). 

And the blade's right part at unrotated (260,396) → rotate:
(260,396): rel (10,148), rotate -26:
x' = 10*0.898 - 148*(-0.438) = 8.98 + 64.8 = 73.8
y' = 10*(-0.438) + 148*0.898 = -4.38 + 132.9 = 128.5
abs: (324, 377). So blade upper-right corner at (324,377). That's to the right, at y=377 (above text). Owl right edge ~x=338 at y=377? Body rx=88, at y=377 (dy=77 from center 300): ellipse x extent = 88*sqrt(1-(77/110)²)=88*sqrt(1-0.49)=88*0.714=62.8. So owl right edge at y=377 is x=250+62.8=312. Blade corner at x=324 > 312, so it's just outside the owl to the right. Good, visible.

Hmm, but is (324,377) inside the emblem ring? Distance from (250,250): sqrt(74²+127²)=sqrt(5476+16129)=sqrt(21605)=147 < 220. Inside ring. Good.

OK so the stick: handle upper-left (~170,84), blade lower-right with tip at (289,409) and corner at (324,377). Both clear of owl and text. 

Wait, I should double-check the handle doesn't overlap the top text. Handle at (170,84). Top text at y=27-48. Handle at y=84 is below. No overlap. And handle x=170, top text "OWAYO" centered at x=250 spanning maybe x=200-300. So handle at x=170 is left of the text. Good.

Alright, let me also reconsider: is the stick too thin/short to be recognizable? Shaft length ~292px (unrotated), that's long. Blade is there. Should be recognizable as a hockey stick. Good.

Now let me write the complete SVG. Let me assemble.

Actually, let me reconsider the belly and feet. Feet at the bottom might look like the owl is standing. Let me add simple feet. Body bottom at y=410. Feet from y=406 to y=428.

Left foot: `M 234 406 L 228 426 Q 225 434 233 433 L 244 431` — a foot with toes. Let me simplify: just a small claw shape.

Actually, let me skip detailed feet to avoid clutter, or add minimal. Let me add minimal feet:
`<path d="M 232 408 q -6 14 4 18 M 232 408 q 0 16 -4 20" .../>` — too complex.

Let me do simple: two small triangles/lines at the bottom.
Left: `M 233 408 L 229 430` and a small foot. 
Honestly, let me just add two small feet as simple strokes:
```svg
<g stroke="#d1922a" stroke-width="4" fill="none" stroke-linecap="round">
  <path d="M 234 408 L 230 430"/>
  <path d="M 266 408 L 270 430"/>
</g>
```
And small toe lines. Let me keep it minimal. Actually, let me add small three-toe feet:
Left foot at (233, 430): three short lines going down-left, down, down-right.
This is getting detailed. Let me just do simple feet or skip. I'll add simple feet (short strokes with tiny toes).

Let me finalize and write. I'll include simple feet.

Let me write the final SVG now.

One more: let me add a subtle inner glow or make the eyes pop more. I'll add a thin dark outline around the body for definition.

Also, let me reconsider the eye design for a cooler look. Owl eyes are big and round. Let me keep the classic look: white eye circles, colored iris, black pupil with shine.

Let me write it all:

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 500 500" width="500" height="500">
  <defs>
    <linearGradient id="bodyGrad" x1="0" y1="0" x2="0.2" y2="1">
      <stop offset="0" stop-color="#55667f"/>
      <stop offset="0.5" stop-color="#38465c"/>
      <stop offset="1" stop-color="#252f40"/>
    </linearGradient>
    <linearGradient id="wingGrad" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#3f4e64"/>
      <stop offset="1" stop-color="#26314"/>
    </linearGradient>
    ...
```

Wait, I made a typo "#26314" — should be "#263142" or similar. Let me fix.

Let me write carefully.

Let me reconsider wing color: slightly darker than body. bodyGrad goes #55667f → #252f40. wingGrad: #3a485c → #232d3d.

Belly: #eef2f8 → #c3cfe2.

Eye gradient: #fff0a8 → #ffbf1e → #c98800.

Stick: #d69c52 → #8a5522.

Let me write the final.

Also, I want to make sure the text is bold and readable. Use font-family with a heavy sans-serif. "Arial Black" may not be available everywhere; let me use a generic with font-weight bold and a large font. Let me use font-family="'Arial', 'Helvetica Neue', Helvetica, sans-serif" font-weight="900".

Let me write it.

Also I realize I should double-check: the user wrote the team name "Owayo Eulers". Let me render exactly: "OWAYO" and "EULERS" (uppercase) or "Owayo Eulers"? For a logo, uppercase is more impactful. Let me use "OWAYO" on top and "EULERS" on bottom. Or I could write "Owayo Eulers" but split. Uppercase looks better for sports logos. Let me use uppercase.

Hmm, but the exact name is "Owayo Eulers". Uppercase "OWAYO EULERS" preserves it. Good.

Let me write the final SVG.

Let me reconsider one thing: I want the design to look polished. Let me add:
- A thin gold inner ring.
- Maybe small stars or dots, but let me keep clean.

Let me also add feather detail lines on the wings (a few curved lines) for texture. Optional. Let me add a couple.

Final SVG:

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 500 500" width="500" height="500">
  <defs>
    <linearGradient id="bodyGrad" x1="0" y1="0" x2="0.15" y2="1">
      <stop offset="0" stop-color="#5869810"/>
    ...
```

Oops, typo again. Let me be careful.

Let me write the final clean version:

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 500 500" width="500" height="500">
  <defs>
    <linearGradient id="bodyGrad" x1="0" y1="0" x2="0.15" y2="1">
      <stop offset="0" stop-color="#5a6b83"/>
      <stop offset="0.55" stop-color="#3d4c62"/>
      <stop offset="1" stop-color="#263243"/>
    </linearGradient>
    <linearGradient id="wingGrad" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#41516a"/>
      <stop offset="1" stop-color="#2a3547"/>
    </linearGradient>
    <radialGradient id="eyeGrad" cx="0.5" cy="0.35" r="0.7">
      <stop offset="0" stop-color="#fff0a6"/>
      <stop offset="0.55" stop-color="#ffbf1e"/>
      <stop offset="1" stop-color="#c48600"/>
    </radialGradient>
    <linearGradient id="bellyGrad" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#eef2f8"/>
      <stop offset="1" stop-color="#c4cfe3"/>
    </linearGradient>
    <linearGradient id="stickGrad" x1="0" y1="0" x2="1" y2="0.3">
      <stop offset="0" stop-color="#dca05a"/>
      <stop offset="1" stop-color="#8a5522"/>
    </linearGradient>
  </defs>

  <!-- Hockey stick (behind the owl) -->
  <g transform="rotate(-26 250 248)">
    <rect x="246" y="66" width="14" height="288" rx="7"
          fill="url(#stickGrad)" stroke="#5c3a1a" stroke-width="1.5"/>
    <path d="M 246 348 L 260 348 L 260 394 Q 260 411 242 411
             L 214 407 Q 200 405 201 391 L 203 366
             Q 204 353 216 353 L 246 353 Z"
          fill="url(#stickGrad)" stroke="#5c3a1a" stroke-width="1.5"/>
    <rect x="204" y="359" width="52" height="6" rx="3"
          fill="#f4f4f4" opacity="0.9"/>
  </g>

  <!-- Emblem rings -->
  <circle cx="250" cy="250" r="234" fill="none" stroke="#f5c518" stroke-width="14"/>
  <circle cx="250" cy="250" r="220" fill="none" stroke="#c99300" stroke-width="3"/>

  <!-- Curved team name -->
  <path id="topArc" d="M 48 250 A 202 202 0 0 1 452 250" fill="none"/>
  <path id="bottomArc" d="M 48 250 A 202 202 0 0 0 452 250" fill="none"/>
  <text font-family="'Arial Black', Arial, Helvetica, sans-serif"
        font-weight="900" font-size="30" letter-spacing="3"
        fill="#16223b">
    <textPath href="#topArc" startOffset="50%" text-anchor="middle">OWAYO</textPath>
  </text>
  <text font-family="'Arial Black', Arial, Helvetica, sans-serif"
        font-weight="900" font-size="30" letter-spacing="4"
        fill="#16223b">
    <textPath href="#bottomArc" startOffset="50%" text-anchor="middle">EULERS</textPath>
  </text>

  <!-- Owl -->
  <ellipse cx="250" cy="302" rx="90" ry="112"
           fill="url(#bodyGrad)" stroke="#1c2634" stroke-width="2"/>

  <!-- Ear tufts -->
  <path d="M 190 198 Q 170 156 197 164 Q 210 184 220 204 Z"
        fill="url(#bodyGrad)" stroke="#1c2634" stroke-width="1.5"/>
  <path d="M 310 198 Q 330 156 303 164 Q 290 184 280 204 Z"
        fill="url(#bodyGrad)" stroke="#1c2634" stroke-width="1.5"/>

  <!-- Wings -->
  <path d="M 172 290 Q 140 322 153 376 Q 162 400 185 392
           Q 172 344 184 300 Q 188 284 172 290 Z"
        fill="url(#wingGrad)" stroke="#1c2634" stroke-width="2"/>
  <path d="M 328 290 Q 360 322 347 376 Q 338 400 315 392
           Q 328 344 316 300 Q 312 284 328 290 Z"
        fill="url(#wingGrad)" stroke="#1c2634" stroke-width="2"/>

  <!-- Belly -->
  <ellipse cx="250" cy="344" rx="56" ry="66"
           fill="url(#bellyGrad)"/>
  <g stroke="#99a9c4" stroke-width="2.2" fill="none" opacity="0.85">
    <path d="M 223 326 Q 250 341 277 326"/>
    <path d="M 225 351 Q 250 366 275 351"/>
    <path d="M 227 376 Q 250 391 273 376"/>
    <path d="M 230 400 Q 250 411 270 400"/>
  </g>

  <!-- Eyes -->
  <circle cx="205" cy="228" r="38" fill="#f3f6fb" stroke="#1c2634" stroke-width="2"/>
  <circle cx="295" cy="228" r="38" fill="#f3f6fb" stroke="#1c2634" stroke-width="2"/>
  <circle cx="205" cy="228" r="25" fill="url(#eyeGrad)"/>
  <circle cx="295" cy="228" r="25" fill="url(#eyeGrad)"/>
  <circle cx="205" cy="230" r="13" fill="#141a26"/>
  <circle cx="295" cy="230" r="13" fill="#141a26"/>
  <circle cx="199" cy="221" r="5" fill="#ffffff"/>
  <circle cx="289" cy="221" r="5" fill="#ffffff"/>

  <!-- Beak -->
  <path d="M 239 258 Q 250 251 261 258 Q 258 275 250 284
           Q 242 275 239 258 Z"
        fill="#e3a327" stroke="#a67713" stroke-width="1.5"/>

  <!-- Feet -->
  <g stroke="#d6922a" stroke-width="4" fill="none" stroke-linecap="round">
    <path d="M 234 406 L 229 428"/>
    <path d="M 266 406 L 271 428"/>
    <path d="M 223 431 L 229 428 L 235 431"/>
    <path d="M 265 431 L 271 428 L 277 431"/>
  </g>
</svg>
```

Wait, the feet paths: `M 223 431 L 229 428 L 235 431` draws a small V (toes). Combined with the leg `M 234 406 L 229 428`. OK.

Let me double check the feet are within the emblem. At y=431, emblem inner ring: circle r=220 at y=431 → x offset = sqrt(220²-181²)=sqrt(48400-32761)=sqrt(15639)=125. So inner ring at y=431 spans x=125 to 375. Feet at x=223-235 and 265-277, within. Good.

Now, let me reconsider the stick blade overlap with the owl body. Blade corner at (324,377) — I said it's just outside owl right edge (312). Let me double check owl right edge at y=377. Body ellipse cx=250 cy=302 rx=90 ry=112. At y=377, dy=75. x extent = 90*sqrt(1-(75/112)²)=90*sqrt(1-0.448)=90*sqrt(0.552)=90*0.743=66.9. So owl right edge at y=377 is x=250+66.9=316.9. Blade corner at x=324 > 317. So blade corner is ~7px outside the owl. Visible. Good, but close. The blade also has the tip at (289,409) which is inside owl width but below... at y=409, dy=107, x extent=90*sqrt(1-(107/112)²)=90*sqrt(1-0.913)=90*sqrt(0.087)=90*0.295=26.5. Owl right edge at y=409 is x=276.5. Blade tip at x=289 > 276.5, so outside owl. Good.

So the blade pokes out to the right of the owl. 

But wait, is any part of the blade inside the owl (covered)? The blade spans from unrotated (201-260, 348-411). After rotation, it occupies roughly x=260-324, y=360-411 region. Part of this might overlap the owl's lower-right. Since the owl is drawn after the stick, the covered parts are hidden. The visible parts poke out. That's fine — looks like the stick is behind with the blade sticking out to the side. Acceptable.

Hmm, but actually if a good chunk of the blade is behind the owl, it might look odd (like a broken stick). Let me reconsider. The blade is at the lower-right, poking out from behind the owl's lower-right side. Actually it might look like the owl is holding the stick. That's fine and looks intentional.

Alternatively, let me make the stick go the other diagonal (upper-right to lower-left) so it frames the owl nicely. Let me try rotate(+26) instead, so handle is upper-right and blade lower-left. Symmetric, might look better. Let me use rotate(26 250 248). Actually, let me keep -26; it's fine.

Hmm, let me reconsider. With rotate(-26), handle upper-left, blade lower-right. The blade poking out lower-right. The owl's right wing is around x=328-360, y=290-392. The blade at (324,377) is near the right wing. Might look like the stick is behind the wing. OK.

Let me just go with it. It should look decent.

Actually, let me reconsider making the stick more clearly a hockey stick and more visible. Let me lengthen the shaft a bit and make the blade more distinct, and ensure both ends clearly show.

Let me also reconsider: maybe put the stick so it's clearly behind and both ends clearly outside the owl and rings. Let me verify handle end (170,84): within ring (dist 184<220), clear of owl (dist from owl center (250,302)=sqrt(80²+218²)=234>112). Good, handle fully visible upper-left.

Blade end visible lower-right. Good.

I think it's fine. Let me finalize.

Let me reconsider the overall look once more and maybe add a couple of refinements:
- Add a subtle outline highlight to the body.
- Make eyes a bit bigger/more striking.

Let me also reconsider eye size: r=38, that's decent. Pupil r=13. Shine r=5.

Let me also make sure the beak is visible: at (250,258-284), between the eyes (eyes at cy=228, bottom at 266). Beak top at 258, which is within the eye region vertically (eyes span 190-266). Beak is narrow (x 239-261), centered. So beak sits in the gap between the eyes, slightly overlapping the lower inner parts of the eyes. That's typical owl look (beak below/between eyes). Should look fine.

Hmm, actually the beak top at y=258 and eyes bottom at y=266 — the beak is above the eye bottom, so it overlaps the lower part of the eye circles. Since beak is drawn after eyes, it covers the eyes there. That might look like the beak is in front of the eyes. For owls, the beak is below the eyes, not overlapping. Let me move the beak lower so it's below the eyes.

Eyes bottom at cy+r=228+38=266. Let me put beak starting at y=268 (just below eyes). Beak: `M 240 266 Q 250 260 260 266 Q 257 282 250 290 Q 243 282 240 266 Z`. Top at y=266, right at eye bottom. Good, beak just below eyes.

Wait, but then the beak is very close to the eye bottoms. Let me give a small gap. Eyes bottom 266, beak top 270. Small gap. Beak: `M 240 270 Q 250 264 260 270 Q 257 287 250 296 Q 243 287 240 270 Z`. Hmm, let me just make it clean.

Let me set beak: top edge around y=268, pointing down to y=292.
`M 241 268 Q 250 262 259 268 Q 256 284 250 292 Q 244 284 241 268 Z`

OK. Let me finalize.

Let me also reconsider: should the owl look more like an owl (with facial disc)? The big eyes on light circles already give an owl look. Good.

Let me write the final version. Let me also add a subtle stroke to the belly or nothing.

Let me also reconsider the "EULERS" text length vs arc. "EULERS" 6 chars at font-size 30, letter-spacing 4. On radius 202 arc. The arc length for the text: 6*~17 + 5*4 ≈ 102+20=122px. Arc angle = 122/202 = 0.604 rad = 34.6°. So text spans ±17° from bottom center. At the ends, y = 250 + 202*cos(17°)=250+202*0.956=250+193=443, x=250±202*sin(17°)=250±59 = 191 and 309. So text spans x=191 to 309 at the bottom, y from 452 (center) to 443 (ends). Wait, at center (bottom) y=250+202=452. At ±17°, y=443. So text is a shallow arc at the bottom, y≈443-452. The stick blade tip at (289,409) is above this (409<443). No overlap. Good. And "EULERS" right end at x=309, blade corner at (324,377) — different location (blade is up and right). No overlap. Good.

Similarly "OWAYO" 5 chars at font-size 30, letter-spacing 3: width ≈ 5*17+4*3=85+12=97px. Arc angle 97/202=0.48rad=27.5°, ±13.75°. Ends at x=250±202*sin(13.75°)=250±48=202,302. y=250+202*cos(13.75°)... top arc: y=250-202*cos(13.75°)=250-196=54. So top text y≈48-54. Handle at (170,84) is left and below. Handle x=170 < 202 (text left end). So handle is left of the text. But handle is at y=84, text at y=48-54. Different height. The handle top is at (170,84), text starts at x=202. Gap. Good, no overlap.

Alright, I'm confident. Let me write the final SVG.

Actually, let me reconsider whether to draw the stick before or after the owl. If stick is before owl (behind), the owl covers the middle of the stick. The handle (upper-left) and blade (lower-right) stick out. Good. Let me keep stick first.

But wait, I should double-check the handle doesn't get covered. Handle is at upper-left, well clear of the owl. Good.

Let me also reconsider: the inner gold ring (r=220) — the stick handle at dist 184 and blade at dist ~147-193 are both inside r=220, so inside the inner ring. Good, stick is inside the emblem.

Now let me write the final clean SVG.

Let me reconsider colors one more time for a cohesive, appealing hockey logo:
- Gold ring: #f5c518 (bright gold)
- Navy text: #16223b
- Owl body: slate blue-grey gradient (#58697f → #263243)
- Owl belly: cream/light (#eef2f8 → #c4cfe3)
- Eyes: amber/gold (#ffbf1e) — ties in with gold ring
- Beak: gold/amber (#e3a327)
- Wings: darker slate (#2a3547)
- Stick: wood brown (#dca05a → #8a5522)
- Tape: white

This is cohesive: gold + navy + slate blue + wood. Very hockey. 

Let me finalize.

Let me write it out completely and carefully, checking for typos.

Actually, let me reconsider the wing feather detail. Let me add a few curved lines on the wings to suggest feathers. Optional but nice. Let me add 2-3 short arcs on each wing.

Left wing inner: `<path d="M 178 310 Q 195 320 205 315" .../>` etc. Let me add subtle ones.

Actually, let me keep wings clean with just the outline. Adding feather lines might clutter at this scale. Let me skip or add very subtle.

Let me add subtle feather lines to the belly only (already have chevrons). Wings clean. Good.

Final answer time. Let me write it.

Let me reconsider the exact beak path to make it look like a nice owl beak (small, hooked). A common stylized owl beak is two small triangles forming a "V" or a small heart/triangle pointing down. Let me use a downward triangle with slightly curved sides:
`M 241 268 Q 250 263 259 268 Q 256 283 250 291 Q 244 283 241 268 Z`
This is a downward-pointing shape with curved sides, tip at (250,291). Good.

Hmm, let me make the beak a bit more distinct — maybe split into upper and lower mandible. Actually, the single shape is fine and clean.

Let me write the final SVG now.

Let me also double check: I have the stick tape rect at x=204 w=52 (so x=204 to 256), y=359 h=6. In unrotated frame. After rotation, it's the tape on the blade. Good.

Wait, the tape should be on the blade, near where shaft meets blade. Unrotated, blade top at y=348-353. Tape at y=359. That's on the blade, near top. Good.

Let me finalize.

Also, I want to make sure the viewBox and dimensions are set. viewBox="0 0 500 500", width/height 500. Good.

Let me write it out.

Let me reconsider if I should include a comment or not. The user wants exactly one complete SVG in a code block. Comments are fine. Let me include a few for clarity.

Let me write the final version:

Actually, let me reconsider the stick orientation for best look. Let me think about what looks best: an owl holding a hockey stick, or a hockey stick behind the owl as part of a crest.

I'll go with: hockey stick diagonal behind the owl (crest style). Handle upper-left, blade lower-right, poking out. This is clean and recognizable.

Let me write final.

Let me reconsider the rotation angle. -26° gives a moderate diagonal. Let me use -30° for a bit more drama. Let me recompute blade position with -30° to ensure no text overlap.

rotate(-30 250 248):
Shaft top (250,66): rel (0,-182), rotate -30 (cos30=0.866, sin30=0.5):
x' = 0*0.866 - (-182)*(-0.5) = -91
y' = 0*(-0.5) + (-182)*0.866 = -157.6
abs: (159, 90). Handle at (159,90). Clear.

Blade tip (214,407): rel (-36,159), rotate -30:
x' = -36*0.866 - 159*(-0.5) = -31.2 + 79.5 = 48.3
y' = -36*(-0.5) + 159*0.866 = 18 + 137.7 = 155.7
abs: (298, 404). Blade tip at (298,404). Text at y≥443. Clear (404<443). Good.

Blade corner (260,394): rel (10,146), rotate -30:
x' = 10*0.866 - 146*(-0.5) = 8.66 + 73 = 81.7
y' = 10*(-0.5) + 146*0.866 = -5 + 126.4 = 121.4
abs: (332, 371). Blade corner at (332,371). Owl right edge at y=371: dy=69, x extent=90*sqrt(1-(69/112)²)=90*sqrt(1-0.379)=90*0.791=71.2. Owl right edge x=321. Blade corner x=332>321. Visible. Good.

So with -30°, handle (159,90), blade tip (298,404), corner (332,371). All clear. Let me use -30°.

Hmm, but blade corner at (332,371) — is it within the emblem ring? Dist from (250,250): sqrt(82²+121²)=sqrt(6724+14641)=sqrt(21365)=146<220. Inside. Good.

And blade tip (298,404): dist sqrt(48²+154²)=sqrt(2304+23716)=sqrt(26020)=161<220. Good.

Let me use rotate(-30 250 248).

Let me finalize the SVG with -30°.

Actually, I realize I keep going back and forth. Let me just commit: rotate(-30 250 248), stick as defined.

Let me write the final SVG.

Let me also reconsider: should the stick be behind or should I make it more prominent by putting it in front on one side? Behind is cleaner. Commit.

Final SVG:

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 500 500" width="500" height="500">
  <defs>
    <linearGradient id="bodyGrad" x1="0" y1="0" x2="0.15" y2="1">
      <stop offset="0" stop-color="#58697f"/>
      <stop offset="0.55" stop-color="#3d4c62"/>
      <stop offset="1" stop-color="#263243"/>
    </linearGradient>
    <linearGradient id="wingGrad" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#41516a"/>
      <stop offset="1" stop-color="#2a3547"/>
    </linearGradient>
    <radialGradient id="eyeGrad" cx="0.5" cy="0.35" r="0.7">
      <stop offset="0" stop-color="#fff0a6"/>
      <stop offset="0.55" stop-color="#ffbf1e"/>
      <stop offset="1" stop-color="#c48600"/>
    </radialGradient>
    <linearGradient id="bellyGrad" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#eef2f8"/>
      <stop offset="1" stop-color="#c4cfe3"/>
    </linearGradient>
    <linearGradient id="stickGrad" x1="0" y1="0" x2="1" y2="0.3">
      <stop offset="0" stop-color="#dca05a"/>
      <stop offset="1" stop-color="#8a5522"/>
    </linearGradient>
  </defs>

  <!-- Eishockey-Schläger hinter der Eule -->
  <g transform="rotate(-30 250 248)">
    <rect x="246" y="66" width="14" height="288" rx="7"
          fill="url(#stickGrad)" stroke="#5c3a1a" stroke-width="1.5"/>
    <path d="M 246 348 L 260 348 L 260 394 Q 260 411 242 411
             L 214 407 Q 200 405 201 391 L 203 366
             Q 204 353 216 353 L 246 353 Z"
          fill="url(#stickGrad)" stroke="#5c3a1a" stroke-width="1.5"/>
    <rect x="204" y="359" width="52" height="6" rx="3"
          fill="#f4f4f4" opacity="0.9"/>
  </g>

  <!-- Emblem-Ringe -->
  <circle cx="250" cy="250" r="234" fill="none" stroke="#f5c518" stroke-width="14"/>
  <circle cx="250" cy="250" r="220" fill="none" stroke="#c99300" stroke-width="3"/>

  <!-- Team-Name -->
  <path id="topArc" d="M 48 250 A 202 202 0 0 1 452 250" fill="none"/>
  <path id="bottomArc" d="M 48 250 A 202 202 0 0 0 452 250" fill="none"/>
  <text font-family="'Arial Black', Arial, Helvetica, sans-serif"
        font-weight="900" font-size="30" letter-spacing="3"
        fill="#16223b"><textPath href="#topArc" startOffset="50%" text-anchor="middle">OWAYO</textPath></text>
  <text font-family="'Arial Black', Arial, Helvetica, sans-serif"
        font-weight="900" font-size="30" letter-spacing="4"
        fill="#16223b"><textPath href="#bottomArc" startOffset="50%" text-anchor="middle">EULERS</textPath></text>

  <!-- Eule -->
  <ellipse cx="250" cy="302" rx="90" ry="112"
           fill="url(#bodyGrad)" stroke="#1c2634" stroke-width="2"/>

  <!-- Ohrenbüschel -->
  <path d="M 190 198 Q 170 156 197 164 Q 210 184 220 204 Z"
        fill="url(#bodyGrad)" stroke="#1c2634" stroke-width="1.5"/>
  <path d="M 310 198 Q 330 156 303 164 Q 290 184 280 204 Z"
        fill="url(#bodyGrad)" stroke="#1c2634" stroke-width="1.5"/>

  <!-- Flügel -->
  <path d="M 172 290 Q 140 322 153 376 Q 162 400 185 392
           Q 172 344 184 300 Q 188 284 172 290 Z"
        fill="url(#wingGrad)" stroke="#1c2634" stroke-width="2"/>
  <path d="M 328 290 Q 360 322 347 376 Q 338 400 315 392
           Q 328 344 316 300 Q 312 284 328 290 Z"
        fill="url(#wingGrad)" stroke="#1c2634" stroke-width="2"/>

  <!-- Brust / Bauch -->
  <ellipse cx="250" cy="344" rx="56" ry="66" fill="url(#bellyGrad)"/>
  <g stroke="#99a9c4" stroke-width="2.2" fill="none" opacity="0.85">
    <path d="M 223 326 Q 250 341 277 326"/>
    <path d="M 225 351 Q 250 366 275 351"/>
    <path d="M 227 376 Q 250 391 273 376"/>
    <path d="M 230 400 Q 250 411 270 400"/>
  </g>

  <!-- Augen -->
  <circle cx="205" cy="228" r="38" fill="#f3f6fb" stroke="#1c2634" stroke-width="2"/>
  <circle cx="295" cy="228" r="38" fill="#f3f6fb" stroke="#1c2634" stroke-width="2"/>
  <circle cx="205" cy="228" r="25" fill="url(#eyeGrad)"/>
  <circle cx="295" cy="228" r="25" fill="url(#eyeGrad)"/>
  <circle cx="205" cy="230" r="13" fill="#141a26"/>
  <circle cx="295" cy="230" r="13" fill="#141a26"/>
  <circle cx="199" cy="221" r="5" fill="#ffffff"/>
  <circle cx="289" cy="221" r="5" fill="#ffffff"/>

  <!-- Schnabel -->
  <path d="M 241 268 Q 250 262 259 268 Q 256 284 250 292
           Q 244 284 241 268 Z"
        fill="#e3a327" stroke="#a67713" stroke-width="1.5"/>

  <!-- Füße -->
  <g stroke="#d6922a" stroke-width="4" fill="none" stroke-linecap="round">
    <path d="M 234 406 L 229 428"/>
    <path d="M 266 406 L 271 428"/>
    <path d="M 223 431 L 229 428 L 235 431"/>
    <path d="M 265 431 L 271 428 L 277 431"/>
  </g>
</svg>
```

Wait, I should double check the feet overlap with the belly/bottom of owl. Feet at y=428-431. Owl body bottom at cy+ry=302+112=414. So feet (y=428-431) extend below the body bottom (414). They poke out below. Within emblem (ring bottom y=470). Good. But the chevron feathers go to y=411 (250,411). Feet at y=428 are below. Good.

Hmm, but the feet poking out below the body — do they look like the owl is standing on something? In a circular emblem, feet at the bottom peeking out is fine (like a mascot standing). OK.

Let me reconsider the feet design. `M 234 406 L 229 428` is a leg. `M 223 431 L 229 428 L 235 431` is a three-toe foot (a shallow V). Together they look like a bird foot. Good.

Actually, owl feet are more like grasping claws. But for a simple logo, the stylized foot is fine.

Let me reconsider whether the feet should be there at all. They add detail. Keep them.

Now, let me reconsider the whole composition balance. The owl is centered-lower (body cy=302). Eyes at cy=228. The head area (top of body) is at y=190, with ear tufts up to y=156. The emblem center is (250,250). The owl is slightly low, which is fine (owls have big heads up top).

Let me check the top of the owl (ear tufts at y=156) vs inner ring. At x=183 (tuft left), inner ring y: circle r=220, at x=183, dy=sqrt(220²-67²)=sqrt(48400-4489)=sqrt(43911)=209.6. So inner ring at x=183 is at y=250-209.6=40.4 (top) — wait, that's the top of the circle at x=183. The circle at x=183 spans y=250±209.6 → y=40.4 to 459.6. So the ring boundary at x=183 is y≈40 (top). Ear tuft at (183,156) — is it inside the ring? At x=183, the inner boundary top is y=40.4. The tuft at y=156 is below 40.4, so inside the circle (inside the ring). Wait, I need to check if the tuft is inside the inner circle (r=220). Distance from center (250,250) to tuft tip (183,156): sqrt(67²+94²)=sqrt(4489+8836)=sqrt(13325)=115.4 < 220. Inside. Good, tufts are inside the emblem. And they don't touch the ring. Good.

Alright. Let me also verify the eyes are inside the ring. Eye centers at (205,228): dist from (250,250)=sqrt(45²+22²)=sqrt(2025+484)=sqrt(2509)=50 < 220. Good.

Everything checks out. Let me finalize.

Oh wait, I should double-check that the "EULERS" text and the stick blade don't overlap, and "OWAYO" and stick handle don't overlap, considering I changed rotation to -30.

Handle at (159,90). "OWAYO" text spans x=202-302, y≈48-54. Handle at x=159 (left of 202), y=90 (below 54). No overlap. Good.

Blade tip at (298,404). "EULERS" spans x=191-309, y≈443-452. Blade tip at y=404 (above 443). No overlap. Good.

Blade corner at (332,371). "EULERS" right end at x=309. Corner at x=332 (right of 309), y=371 (above 443). No overlap. Good.

Great.

Now, let me reconsider: is the stick too hidden? The visible parts: handle (upper-left, from (159,90) going down-right into the owl) and blade (lower-right poking out). The handle is a long thin line from (159,90) toward the owl. The blade is a small shape at lower-right. This should be recognizable as a hockey stick held behind/diagonally. Good.

Hmm, actually, let me reconsider — the handle part that's visible is just the shaft (thin rect) from (159,90) to where it enters the owl. Where does the shaft enter the owl? The shaft is at x=246-256 (unrotated), which after rotation... the shaft top is at (159,90), and the shaft goes toward the owl center. The shaft would enter the owl around the owl's upper-left. So visible handle is from (159,90) to maybe (210,150) or so. That's a decent-length visible handle. Good.

Let me verify the shaft line. Unrotated shaft: x=246-256, y=66 to 354. It's a vertical line at x≈251. After rotate(-30 250 248), this vertical line becomes a diagonal line. The top (251,66) → let me compute: rel (1,-182), rotate -30: x'=1*0.866-(-182)(-0.5)=0.866-91=-90.1, y'=1*(-0.5)+(-182)(0.866)=-0.5-157.6=-158.1. abs (160,90). Bottom of shaft (251,354): rel(1,106), rotate-30: x'=0.866-53=-52.1, y'=-0.5+91.7=91.2. abs(198,339). So shaft from (160,90) to (198,339). At (198,339), is it inside the owl? Owl body cx=250 cy=302. dist from center: sqrt(52²+37²)=sqrt(2704+1369)=sqrt(4073)=63.8 < 112 (in ellipse). So (198,339) is inside the owl. So the shaft enters the owl around there and is covered. Visible shaft: from (160,90) to ~(198,339) but the part inside the owl is covered. The owl's upper-left boundary... the shaft at (198,339) is inside. Where does it cross the owl boundary? Somewhere around (185,280) maybe. So visible shaft from (160,90) to ~(185,280). That's a good visible handle length. Good.

Alright, I'm confident the design works. Let me write the final answer.

Actually, let me reconsider making the stick a bit more prominent/visible by shortening the covered part. But it's fine. The current design has a nice visible handle and blade.

Let me also reconsider: maybe I should add a second stick crossed, to make it more "hockey." But the user said "Eishockeyschläger" which can be singular. One stick is cleaner. I'll keep one.

Hmm, let me reconsider — actually two crossed sticks behind the owl (an "X") is a very common hockey logo element and looks great. But it might complicate. Let me do one stick to keep it clean and clearly recognizable. If I add a second, it could look cluttered behind the owl. One is fine.

Let me finalize.

Wait, I realize I should double-check the eye shine positions and make them consistent. Left eye center (205,228), shine at (199,221) — upper-left of center. Right eye center (295,228), shine at (289,221) — upper-left of center. Both shines upper-left, consistent lighting. Good. Actually, let me put shines upper-left for both (as if light from top-left). (199,221) is up-left of (205,228). (289,221) is up-left of (295,228). Consistent. Good.

Let me write the final SVG. I'll present it cleanly.

Let me reconsider font-size and whether text fits the arc nicely. I computed "OWAYO" spans ±13.75°, "EULERS" ±17°. Both fit within the ring band nicely. Good.

Let me also make sure the text baseline sits on the arc (radius 202) and text is within the ring band (216-234). The arc is at radius 202, which is inside the inner ring (216). So the text baseline is at radius 202, and text extends outward (top text up, bottom text up-toward-center). 

For top text: baseline at r=202 (y=48), text extends up to y≈27. The ring band is y=16-34 at the top (r=216 to 234 → y=250-216=34 to 250-234=16). So the ring band at top is y=16-34. Text baseline at y=48 is just below the ring (outside the band, toward center). Text extends up to y=27, which overlaps the ring band (16-34) partially. Hmm, so the top text would overlap the gold ring. Text is dark navy on gold — readable, but the text is positioned just inside the ring.

Actually, this is fine — the text sits just inside the ring, which is a common layout. But let me reconsider: I want the text to appear to be on/within the ring band for a clean look. Let me move the arcs to radius ~224 (middle of band).

If arcs at r=224: top text baseline at y=250-224=26, extends up to y≈5. Ring band top is y=16-34. Text baseline at 26 is within band, text extends up to 5 (above band, in the outer area/off). Hmm, text would extend above the ring.

This is the classic tension: text on a circular ring. Let me just position the arcs so the text is centered in the band.

Band: r=216 to 234, middle=225. At the top, band is y=15 to 34 (250-234=16, 250-216=34). Text cap height ~21px (font-size 30). To center 21px tall text in a band from y=16 to 34 (18px tall)... the band is only 18px wide but text is 21px tall. Slight mismatch. Let me reduce font size to 26, cap height ~18px. Then text fits the 18px band if centered.

Let me set arcs at r=225, font-size=26.
Top text: baseline at y=250-225=25. Text extends up by ~18px to y=7. Band is y=16-34. So text from y=7 to 25. Overlaps band (16-25) and slightly above (7-16). Hmm.

The issue: text baseline should be in the middle of the band, with text going outward (up for top). For top text, the text extends outward (away from center) = upward. Baseline at r=225 (y=25), text up to y=7. But band is at y=16-34. So baseline at y=25 is in the band, text extends from 25 up to 7 (outward), crossing the outer ring edge at y=16 and going beyond.

This means the top of the letters pokes outside the outer ring. That's actually fine and common — text follows the ring, letters can cross the ring lines. But for cleanliness, let me just accept it or adjust.

Alternatively, put the text inside the ring (smaller radius), fully within the circle. Let me put arcs at r=205, font-size=28. Top text baseline at y=45, extends up to y=27. Inner ring at y=34. So text from y=27 to 45 — mostly inside the circle (below the inner ring line at 34), with the top of letters (y=27-34) overlapping the inner ring line. Hmm.

You know, this level of perfection isn't necessary. Let me just place the text at a radius that looks good and not worry about exact band alignment. A common approach: text sits inside the ring, following a circle just inside the inner ring line. Let me use r=205, font-size=28.

Top text baseline at y=45, letters up to y=27. The inner gold ring line is at y=34. So the upper letters (y=27-34) are drawn over the inner ring line. Since text is on top (drawn after ring), the text covers part of the inner ring line. That might look slightly off (text over the ring line).

To avoid text over ring lines, let me put text fully inside: r=195, font-size=28. Top baseline at y=55, letters up to y=37. Inner ring line at y=34. Letters (37-55) are below the ring line (34), so fully inside, no overlap. 

Wait, letters from y=37 (top) to y=55 (baseline). Ring line at y=34. 37 > 34, so letters are below the ring line (inside the circle). No overlap. 

Bottom text: baseline at y=250+195=445, letters extend up (toward center) to y=427. Inner ring line at bottom y=250+216=466. Letters (427-445) are above 466 (inside circle). No overlap. 

So r=195, font-size=28 puts text fully inside the inner ring, no overlap with ring lines. Let me use r=195.

Let me recompute text span with r=195:
"OWAYO": width ~97px, angle=97/195=0.497rad=28.5°, ±14.25°. Ends at x=250±195*sin(14.25°)=250±48=202,302. y=250-195*cos(14.25°)=250-189=61. So top text spans x=202-302, y≈55-61. Clear of owl (owl top y=190). Clear of ring (ring line y=34). Good.

"EULERS": width ~122px, angle=122/195=0.626rad=35.9°, ±18°. Ends at x=250±195*sin(18°)=250±60=190,310. y=250+195*cos(18°)=250+185=435 (at ends), 445 (center). So bottom text spans x=190-310, y≈435-445. Clear of stick blade (tip at 404). Clear of ring (line at 466). Good.

Great, r=195 works. Let me update the arcs to r=195.

Actually, let me reconsider font-size 28 vs 30. Let me use 28 for cleaner fit. letter-spacing 3 and 4.

Let me update:
```svg
<path id="topArc" d="M 55 250 A 195 195 0 0 1 445 250" fill="none"/>
<path id="bottomArc" d="M 55 250 A 195 195 0 0 0 445 250" fill="none"/>
```
And font-size=28.

Wait, at r=195, the arc endpoints: left (55,250), right (445,250). These are on the horizontal diameter. The arc bulges up (top) or down (bottom). Good.

Let me finalize with r=195, font-size=28.

Hmm, let me reconsider — I want the text to be reasonably large and prominent. font-size 28 is good. Let me maybe bump to 30 but ensure fit. With 30, cap height ~21px. Top text baseline at y=55, up to y=34. Ring line at y=34. So top letters reach y=34, exactly touching the ring line. Slight overlap risk. Let me keep 28 to be safe. Or 29. Let me use 28.

Actually, let me reconsider the cap height. For font-size 30, typical cap height is ~0.7*30=21px. Baseline at 55, top of caps at 34. Ring inner line at 34. Touching. With font-size 28, cap height ~20px, top at 35, ring line at 34. Gap of 1px. Fine. Let me use 28.

Hmm, wait, I need to double-check: is the top text baseline really at y=55? Arc r=195, top of circle at y=250-195=55. So the arc's highest point is y=55. With text-anchor middle and startOffset 50%, the text center is at the arc's highest point (top, y=55). The baseline is at y=55. Text extends upward from baseline. So top of caps at y=55-20=35. Ring inner line at top: y=250-216=34. So caps top at 35, ring line at 34. Gap 1px. Good, no overlap.

Let me finalize.

Actually, let me reconsider — maybe I'm overthinking the ring overlap. It's a minor aesthetic. Let me just go with r=195, font-size=28, and it'll look good.

Let me write the final SVG now. For real this time.

Let me also add a subtle drop shadow to the owl for depth? That might require filters. Let me add a simple shadow using a slightly offset dark ellipse with low opacity. Actually, filters are allowed (not scripts). But let me keep it simple without filters for maximum compatibility. I'll skip the shadow.

Final SVG (writing it out completely):

Let me reconsider the belly chevron positions to ensure they're within the belly ellipse. Belly ellipse cx=250 cy=344 rx=56 ry=66. Chevrons at y=326,351,376,400. At y=326, dy=-18, x extent=56*sqrt(1-(18/66)²)=56*sqrt(1-0.074)=56*0.961=53.8. Chevron from x=223 to 277 (width 54), centered. Fits (54<53.8, close). Let me shorten chevrons slightly: from 225 to 275. Let me adjust: `M 225 326 Q 250 340 275 326`. Good.

At y=400, dy=56, x extent=56*sqrt(1-(56/66)²)=56*sqrt(1-0.72)=56*0.529=29.6. Chevron from 230 to 270 (width 40) — exceeds 29.6! So the bottom chevron pokes out of the belly ellipse. Let me shorten it: from 237 to 263 (width 26). `M 237 400 Q 250 410 263 400`. Good.

Let me adjust all chevrons to fit:
- y=326: 225 to 275 (width 50, extent 53.8) OK
- y=351: dy=7, extent=56*sqrt(1-(7/66)²)=56*0.994=55.7. 225-275 width 50 OK
- y=376: dy=32, extent=56*sqrt(1-(32/66)²)=56*sqrt(1-0.235)=56*0.875=49. 226-274 width 48 OK
- y=400: dy=56, extent=29.6. 237-263 width 26 OK

Let me update chevrons:
```
<path d="M 225 326 Q 250 340 275 326"/>
<path d="M 225 351 Q 250 365 275 351"/>
<path d="M 226 376 Q 250 390 274 376"/>
<path d="M 237 400 Q 250 410 263 400"/>
```

Good.

Now let me also reconsider the wings fit within the emblem. Left wing spans x=140-185, y=284-400. At x=140 (leftmost), is it inside the emblem? Dist from center (250,250): the wing leftmost point ~ (140,330). dist=sqrt(110²+80²)=sqrt(12100+6400)=sqrt(18500)=136 < 220. Inside. Good.

Alright, finalizing. Let me write it out.

Let me reconsider the overall size of the owl within the emblem. Owl body rx=90 ry=112, centered at (250,302). Extents: x 160-340, y 190-414. Plus ear tufts to y=156. Plus feet to y=431. All within emblem (ring inner r=220: at bottom y=470, so feet at 431 fit; at sides x=160, ring at x=160 → y=250±sqrt(220²-90²)=250±191 → y=59 to 441. So at x=160, ring spans y=59-441. Owl at x=160 is only the body edge at y=302. Inside. Good.)

Everything fits. Final answer.

Let me write it cleanly with good formatting.

Actually, let me reconsider the color of the beak — amber #e3a327 with stroke #a67713. And feet #d6922a. Consistent amber palette. Good.

Let me also reconsider adding a small highlight to make the owl's head look rounded. Optional. I'll add a subtle lighter ellipse on the upper head. Actually, let me add a subtle highlight to the body top. Hmm, might not be necessary. Let me keep it clean.

Let me write the final SVG.

One more consideration: the user asked in German, so I could add a brief German note. But the instruction says "Antworte mit genau einem vollständigen SVG-Dokument in einem Codeblock." This suggests the response should be exactly one SVG document in a code block. It might be safest to provide just the code block, or a brief intro + code block. The instruction emphasizes responding with exactly one complete SVG in a code block. Let me provide the code block, perhaps with a very brief intro sentence. Actually, "Antworte mit genau einem vollständigen SVG-Dokument in einem Codeblock" = "Respond with exactly one complete SVG document in a code block." I'll provide the SVG in a code block. I can add a tiny note but let me keep it minimal — maybe just the code block, or one line. To be safe and follow instructions, I'll put the SVG in the code block and keep any text minimal. Let me add a short German sentence before it. Actually, the instruction is quite specific about the format. Let me just give the code block with maybe a one-line intro. I'll keep it clean.

Let me produce the final answer.

Let me write out the final SVG carefully, checking all syntax.

Final check on the stick blade path — let me make sure it's a valid closed path and looks like a blade:
`M 246 348 L 260 348 L 260 394 Q 260 411 242 411 L 214 407 Q 200 405 201 391 L 203 366 Q 204 353 216 353 L 246 353 Z`

Let me trace:
- Start (246,348)
- L (260,348): top edge of blade, going right
- L (260,394): right side going down
- Q (260,411) (242,411): curve — control (260,411), end (242,411): bottom-right curves to bottom
- L (214,407): bottom edge going left (slightly up)
- Q (200,405) (201,391): control (200,405), end (201,391): bottom-left curves up
- L (203,366): left side going up
- Q (204,353) (216,353): control (204,353), end (216,353): top-left curve
- L (246,353): top edge going right back toward start
- Z: close

This forms a blade shape: a vertical right side, curved bottom, and the top connects to the shaft. It looks like a hockey stick blade (the blade part that was cut from the shaft). Actually, the shaft is separate (the rect above). The blade here is the lower widened part. When combined with the shaft rect (x=246-256, y=66-354), the blade top at y=348-353 connects. Good. The blade is wider than the shaft (x=201-260 vs 246-256), forming the characteristic blade shape. Good.

The tape rect x=204 y=359 w=52 h=6 → x=204-256, y=359-365. This is across the blade top area. Represents blade tape. Good.

Alright, writing final answer.

Let me reconsider: should I name it something or add metadata? Not needed. Just the SVG.

Let me write it.

Actually, let me reconsider the eyes one more time — I want them to look striking. Let me add a thin dark ring around the iris too, or keep simple. Current: white circle r=38, iris r=25 (amber gradient), pupil r=13 (dark), shine r=5 (white). That's a classic striking eye. Good.

Also, let me add a subtle eyelid/ridge above each eye for more owl character. Two small arcs above the eyes. Optional. Let me add thin brow lines:
Left: `M 178 205

### Antwort

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 500 500" width="500" height="500">
  <defs>
    <linearGradient id="bodyGrad" x1="0" y1="0" x2="0.15" y2="1">
      <stop offset="0" stop-color="#58697f"/>
      <stop offset="0.55" stop-color="#3d4c62"/>
      <stop offset="1" stop-color="#263243"/>
    </linearGradient>
    <linearGradient id="wingGrad" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#41516a"/>
      <stop offset="1" stop-color="#2a3547"/>
    </linearGradient>
    <radialGradient id="eyeGrad" cx="0.5" cy="0.35" r="0.7">
      <stop offset="0" stop-color="#fff0a6"/>
      <stop offset="0.55" stop-color="#ffbf1e"/>
      <stop offset="1" stop-color="#c48600"/>
    </radialGradient>
    <linearGradient id="bellyGrad" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#eef2f8"/>
      <stop offset="1" stop-color="#c4cfe3"/>
    </linearGradient>
    <linearGradient id="stickGrad" x1="0" y1="0" x2="1" y2="0.3">
      <stop offset="0" stop-color="#dca05a"/>
      <stop offset="1" stop-color="#8a5522"/>
    </linearGradient>
  </defs>

  <!-- Eishockey-Schläger hinter der Eule -->
  <g transform="rotate(-30 250 248)">
    <rect x="246" y="66" width="14" height="288" rx="7"
          fill="url(#stickGrad)" stroke="#5c3a1a" stroke-width="1.5"/>
    <path d="M 246 348 L 260 348 L 260 394 Q 260 411 242 411
             L 214 407 Q 200 405 201 391 L 203 366
             Q 204 353 216 353 L 246 353 Z"
          fill="url(#stickGrad)" stroke="#5c3a1a" stroke-width="1.5"/>
    <rect x="204" y="359" width="52" height="6" rx="3"
          fill="#f4f4f4" opacity="0.9"/>
  </g>

  <!-- Emblem-Ringe -->
  <circle cx="250" cy="250" r="234" fill="none" stroke="#f5c518" stroke-width="14"/>
  <circle cx="250" cy="250" r="220" fill="none" stroke="#c99300" stroke-width="3"/>

  <!-- Team-Name -->
  <path id="topArc" d="M 55 250 A 195 195 0 0 1 445 250" fill="none"/>
  <path id="bottomArc" d="M 55 250 A 195 195 0 0 0 445 250" fill="none"/>
  <text font-family="'Arial Black', Arial, Helvetica, sans-serif"
        font-weight="900" font-size="28" letter-spacing="3"
        fill="#16223b"><textPath href="#topArc" startOffset="50%" text-anchor="middle">OWAYO</textPath></text>
  <text font-family="'Arial Black', Arial, Helvetica, sans-serif"
        font-weight="900" font-size="28" letter-spacing="4"
        fill="#16223b"><textPath href="#bottomArc" startOffset="50%" text-anchor="middle">EULERS</textPath></text>

  <!-- Eule -->
  <ellipse cx="250" cy="302" rx="90" ry="112"
           fill="url(#bodyGrad)" stroke="#1c2634" stroke-width="2"/>

  <!-- Ohrenbüschel -->
  <path d="M 190 198 Q 170 156 197 164 Q 210 184 220 204 Z"
        fill="url(#bodyGrad)" stroke="#1c2634" stroke-width="1.5"/>
  <path d="M 310 198 Q 330 156 303 164 Q 290 184 280 204 Z"
        fill="url(#bodyGrad)" stroke="#1c2634" stroke-width="1.5"/>

  <!-- Flügel -->
  <path d="M 172 290 Q 140 322 153 376 Q 162 400 185 392
           Q 172 344 184 300 Q 188 284 172 290 Z"
        fill="url(#wingGrad)" stroke="#1c2634" stroke-width="2"/>
  <path d="M 328 290 Q 360 322 347 376 Q 338 400 315 392
           Q 328 344 316 300 Q 312 284 328 290 Z"
        fill="url(#wingGrad)" stroke="#1c2634" stroke-width="2"/>

  <!-- Brust / Bauch -->
  <ellipse cx="250" cy="344" rx="56" ry="66" fill="url(#bellyGrad)"/>
  <g stroke="#99a9c4" stroke-width="2.2" fill="none" opacity="0.85">
    <path d="M 225 326 Q 250 340 275 326"/>
    <path d="M 225 351 Q 250 365 275 351"/>
    <path d="M 226 376 Q 250 390 274 376"/>
    <path d="M 237 400 Q 250 410 263 400"/>
  </g>

  <!-- Augen -->
  <circle cx="205" cy="228" r="38" fill="#f3f6fb" stroke="#1c2634" stroke-width="2"/>
  <circle cx="295" cy="228" r="38" fill="#f3f6fb" stroke="#1c2634" stroke-width="2"/>
  <circle cx="205" cy="228" r="25" fill="url(#eyeGrad)"/>
  <circle cx="295" cy="228" r="25" fill="url(#eyeGrad)"/>
  <circle cx="205" cy="230" r="13" fill="#141a26"/>
  <circle cx="295" cy="230" r="13" fill="#141a26"/>
  <circle cx="199" cy="221" r="5" fill="#ffffff"/>
  <circle cx="289" cy="221" r="5" fill="#ffffff"/>

  <!-- Schnabel -->
  <path d="M 241 268 Q 250 262 259 268 Q 256 284 250 292
           Q 244 284 241 268 Z"
        fill="#e3a327" stroke="#a67713" stroke-width="1.5"/>

  <!-- Füße -->
  <g stroke="#d6922a" stroke-width="4" fill="none" stroke-linecap="round">
    <path d="M 234 406 L 229 428"/>
    <path d="M 266 406 L 271 428"/>
    <path d="M 223 431 L 229 428 L 235 431"/>
    <path d="M 265 431 L 271 428 L 277 431"/>
  </g>
</svg>
```
