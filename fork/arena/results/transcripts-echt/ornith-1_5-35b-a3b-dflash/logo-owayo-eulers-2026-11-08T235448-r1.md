# ornith-1_5-35b-a3b-dflash - logo-owayo-eulers (2026-11-08T23:54:48)

## Antwort (46584 Tokens, 251.723 s, Ende: stop, Denken abgebrochen)

### Denkphase

The user wants a logo for an ice hockey team called "Owayo Eulers". The logo should contain an owl (Eule) and an ice hockey stick (Eishockeyschläger). The background should be solid or preferably no background.

Let me create an SVG logo. I'll design an owl combined with ice hockey elements.

Let me think about the design:
- An owl (the mascot)
- Ice hockey sticks (crossed behind perhaps)
- The team name "Owayo Eulers"

Let me create a clean, stylized SVG. I'll make an owl with hockey sticks crossed behind it.

Let me build this carefully with SVG paths.

I'll create:
1. Crossed hockey sticks in the background
2. An owl in the center
3. The text "Owayo Eulers"

Let me write the SVG.

For the owl, I'll create a stylized front-facing owl with:
- Body
- Head
- Eyes (large circles)
- Beak
- Ears/tufts
- Wings
- Belly pattern

For hockey sticks, I'll create two crossed sticks.

Let me make this look good.

I'll use a color scheme - maybe dark blue/green for the owl with white accents.

Let me construct the SVG:

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 500 500" width="500" height="500">
  <!-- Hockey sticks -->
  ...
  <!-- Owl -->
  ...
  <!-- Text -->
  ...
</svg>
```

Let me design each element.

Hockey stick: A long shaft with a blade at the bottom. I'll make two crossed.

Let me create the paths.

For a hockey stick rotated, I can use a group with rotation.

Let me define a hockey stick shape pointing up, then rotate it.

A hockey stick:
- Shaft: a long thin rectangle/line
- Blade: a hook shape at the bottom

Let me create it pointing downward actually, crossed in an X pattern.

Let me think of the blade. The blade is at the bottom, curving. 

Stylized hockey stick:
- Vertical shaft
- At the bottom, a horizontal blade that curves

Let me use a path for the whole stick.

Actually, let me make it simpler and cleaner. I'll draw the stick as a filled shape.

Hockey stick path (pointing down, blade at bottom):
- Start at top of shaft
- Down the shaft
- Curve into blade

Let me create a nice owl first.

Owl design (front-facing):
- Body: oval/rounded shape
- Two ear tufts
- Face disc
- Two large eyes with pupils
- Small beak
- Belly feathers (lines or arcs)
- Wings on sides

Let me write it out.

Colors:
- Owl body: #2E5A4B (dark teal/green) or maybe a nice color
- Let me use a deep green/teal with lighter belly
- Eyes: gold/yellow with dark pupils
- Beak: orange

Let me go with a professional look.

Let me build the full SVG now.

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 600" width="600" height="600">
  <defs>
    <linearGradient id="bodyGrad" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#3A7D5C"/>
      <stop offset="1" stop-color="#1E4D3A"/>
    </linearGradient>
  </defs>
  
  <!-- Hockey sticks -->
  ...
</svg>
```

Let me create the hockey sticks. I'll make them crossed behind the owl.

Hockey stick 1 - going from top-left to bottom-right
Hockey stick 2 - going from top-right to bottom-left

Let me create a single stick shape and use it twice with different rotations.

A hockey stick pointing straight down:
- Shaft from y=50 to y=400 (vertical line, centered at x=250)
- Blade at bottom

Let me define the stick as a group.

Actually for crossed sticks, let me make the stick point upward with blade at bottom, then rotate.

Let me define a stick centered at origin, pointing down:

Shaft: rect from (-8, -150) to (8, 50) — a vertical rectangle
Blade: a curved shape at the bottom

Hmm, let me think about the blade shape. The blade of a hockey stick is like a curved paddle.

Blade shape (at bottom of stick):
- It extends horizontally and curves up at the front (heel and toe)

Let me create a path:
```
M -8 50 
L 8 50 
L 10 70 
L 15 90 
C 20 100, 15 108, 5 108 
L -10 105 
L -12 85 
Z
```

This is getting complex. Let me simplify.

Actually, let me make a cleaner design. I'll draw the hockey stick as:
- A long thin shaft (rounded rectangle)
- A blade (a curved path)

Let me use simpler geometric shapes.

For the shaft, a rounded rectangle. For the blade, a simple hook.

Let me reconsider the whole layout. I want:
- Two crossed hockey sticks behind
- An owl in front
- Text "Owayo Eulers" at the bottom or top

Let me place text at the bottom.

Let me write the full thing.

I'll create the owl centered around (300, 250), and sticks crossed behind, text at bottom.

Let me define the hockey stick carefully.

A hockey stick, I'll draw it pointing up-left to down-right.

Let me create the stick shape pointing straight down, then I'll rotate the group.

Stick pointing down, centered at x=0:
- Shaft: rounded rect, x from -6 to 6, y from -180 to 60
- Blade: at the bottom

Blade path (the curved part):
The blade connects to the shaft at around y=60 and extends to the right and curves.

```
Blade:
M -6 55
L 6 55
L 8 70
L 20 80
C 28 85, 30 95, 24 100
C 18 104, 8 100, 6 92
L 2 88
L -2 70
Z
```

Hmm, let me make it cleaner. Actually the blade should curve up at the toe.

Let me simplify to a common representation:

The blade looks like this (side view):
- Bottom is flat (touches ice)
- Front (toe) curves up
- Back (heel) connects to shaft

```
M -6 55
L 6 55
L 6 88
L 22 88
C 30 88, 32 95, 28 100
C 24 105, 16 103, 15 96
L 12 92
L 6 92
Z
```

This is getting complicated. Let me just make a simple blade:

```
Blade:
M -6 55
L 6 55
L 6 90
L 24 90
L 24 98
C 24 106, 14 108, 8 104
L 4 100
L -6 100
L -6 55
Z
```

OK let me just go with something reasonable. I'll make it look like a hockey stick.

Actually, let me reconsider. Maybe I should make the design cleaner and more iconic. Let me think about what makes a good hockey owl logo.

Common hockey logos: shield/circle shape, animal mascot, crossed sticks.

Let me do:
- A circular badge outline (optional)
- Two crossed hockey sticks
- An owl in the center
- Text around or below

Since they said background should be solid or none, I'll make it transparent background with the design elements.

Let me create a nice design.

Let me build the owl more carefully. Front-facing owl:

Body: A rounded shape. Let me use an ellipse or a path.

Head with ear tufts.

Let me define coordinates. Center at (300, 240).

Owl body path (main body):
```
M 300 150  (top of head)
...
```

Let me build it piece by piece.

Ear tufts (two triangles pointing up):
- Left: (255, 155) to (240, 110) to (280, 145)
- Right: (345, 155) to (360, 110) to (320, 145)

Head/face disc: A rounded shape.

Eyes: two large circles.
- Left eye center: (265, 200), radius 32
- Right eye center: (335, 200), radius 32
- Pupils: dark, slightly toward center
- Eye rings: lighter color

Beak: a small triangle/shape between eyes, below.
- Beak at (300, 235)

Body: below the head, a rounded belly.
- From around y=260 down to y=400

Wings: on left and right sides.

Belly feather pattern: arcs or V shapes.

Let me write this out.

```svg
<!-- Body -->
<ellipse cx="300" cy="320" rx="90" ry="110" fill="url(#bodyGrad)"/>

<!-- Belly -->
<ellipse cx="300" cy="340" rx="60" ry="80" fill="#E8F3E0"/>

<!-- Belly feather lines -->
...
```

Hmm, let me make it more owl-like. Owls have a heart-shaped face disc.

Let me refine.

Actually, let me create a cleaner, more stylized owl. Let me just go with a good design.

Let me write the complete SVG now. I'll iterate on the design.

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 640" width="600" height="640">
  <defs>
    <linearGradient id="owlBody" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#4C8C6B"/>
      <stop offset="1" stop-color="#1F4D3B"/>
    </linearGradient>
    <linearGradient id="stickGrad" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="#C8964A"/>
      <stop offset="1" stop-color="#8B5A24"/>
    </linearGradient>
  </defs>
  
  <!-- Hockey Stick 1 (backslash direction \) -->
  <g transform="rotate(35 300 300)">
    <!-- shaft -->
    <rect x="293" y="70" width="14" height="330" rx="7" fill="url(#stickGrad)"/>
    <!-- blade -->
    <path d="M 293 395 L 307 395 L 310 420 L 335 435 C 348 443, 345 458, 332 460 L 300 458 L 296 440 L 293 420 Z" fill="url(#stickGrad)"/>
  </g>
  
  <!-- Hockey Stick 2 (slash direction /) -->
  <g transform="rotate(-35 300 300)">
    <rect x="293" y="70" width="14" height="330" rx="7" fill="url(#stickGrad)"/>
    <path d="M 293 395 L 307 395 L 310 420 L 335 435 C 348 443, 345 458, 332 460 L 300 458 L 296 440 L 293 420 Z" fill="url(#stickGrad)"/>
  </g>
  
  <!-- Owl -->
  ...
  
  <!-- Text -->
  <text x="300" y="560" ...>Owayo Eulers</text>
</svg>
```

Wait, I need to reconsider the stick blade. When rotated, the blade should be at the bottom. Let me make the blade point in the right direction.

Actually, let me reconsider. The blade is at the bottom of the stick. When I rotate the stick, the blade rotates too. For crossed sticks, both blades should be at the bottom.

Let me make the stick point straight down with blade at bottom, then rotate ±35 degrees around center.

The blade: I want it to look like a hockey stick blade. Let me make it extend to one side (the toe curves up).

Hmm, actually for a clean look, let me make both blades point outward/downward symmetrically.

Let me reconsider. When two sticks cross and rotate ±35°, the blades at the bottom will splay outward a bit. That looks good.

Let me refine the blade shape. The blade should have:
- Heel (top, connects to shaft)
- Flat bottom
- Toe (front) that curves up

Let me make the blade:
```
M 293 395 
L 307 395 
L 307 425 
L 330 428 
C 342 429, 345 442, 336 448 
C 328 453, 316 450, 314 441 
L 308 435 
L 293 430 
Z
```

Hmm, this is getting complicated. Let me simplify.

Let me just make a simple curved blade:
```
Blade:
M 293 393
L 307 393
L 307 430
L 332 432
C 340 432, 342 442, 334 447
C 326 452, 315 449, 314 441
L 310 433
L 293 430
Z
```

Actually, let me step back and make the whole stick cleaner. Let me draw it as one continuous path or use simpler shapes.

Let me define the stick pointing down:
- Shaft: rounded rect, width 14, from y=60 to y=400
- Blade: a shape at the bottom

For the blade, let me make it extend to the right and curve up at the toe. This is a typical hockey stick.

Actually, you know what, let me make the blade symmetrical-ish and simple. A hockey stick blade viewed from the side:

```
The blade is like a "J" or hook shape rotated.
```

Let me just create a reasonable one. I'll make the blade extend to the right:

```
M 293 393
L 307 393
L 307 428
L 333 430
L 333 446
C 333 456, 320 460, 308 456
L 305 448
L 293 438
Z
```

OK, I'll go with this. When rotated, it'll look like a hockey stick.

Hmm, but when I rotate the whole stick by ±35°, the blade which points right will also rotate. Let me think about whether this looks good.

Stick 1 rotated +35° (clockwise): the shaft goes from top-left to bottom-right, blade at bottom-right pointing... 

Actually this might look messy. Let me reconsider.

Maybe I should make the blades point outward (away from center) for a cleaner crossed-stick look. 

Alternatively, let me make the stick blade point to the left for one and right for the other, but that requires different blade shapes.

Let me simplify: I'll make both sticks with the blade at the very bottom, and just have the blade extend symmetrically or just be a simple flat bottom with a slight curve.

Actually, the cleanest crossed hockey stick logo has both blades at the bottom, pointing outward (left blade's toe points left, right blade's toe points right). But since I'm rotating, let me just make the blade point right and rotate.

Let me trace through:
- Stick 1: rotation +35° around (300, 300). The stick points down. Blade at bottom pointing right. After +35° rotation, the bottom of the stick moves to the right, so the blade (pointing right) now points down-right. The shaft goes from top-left to bottom-right.
- Stick 2: rotation -35°. Blade pointing right, after -35° rotation, points up-right. Hmm.

This asymmetry might look odd. Let me make the blade point left for stick 2, or make blades symmetric.

Alternatively, let me not rotate the blade separately. Let me just make both blades point outward by using different rotations.

Hmm, let me think differently. Let me make the whole thing symmetric by:
- Stick 1: blade at bottom, I'll rotate so it looks natural
- For symmetry, maybe I should draw stick 2 as a mirror of stick 1.

Let me use a mirror. Stick 1 is the stick with blade pointing right. Stick 2 is the mirror image (blade pointing left), then rotated.

Actually, let me reconsider the entire approach. Let me place the crossing point lower, and have both sticks diverge upward, with blades at the bottom pointing outward.

Let me define:
- Stick A: shaft going up-left, blade at bottom-right... 

Ugh, this is getting complicated. Let me just go with a clean crossed design and not overthink the blade direction. I'll make both blades point outward.

Approach: 
- Create a stick shape pointing straight down with blade at bottom-right (toe pointing right).
- Stick 1: rotate 35° clockwise. 
- Stick 2: mirror horizontally (scale -1, 1) then rotate 35° clockwise. This makes the blade point bottom-left.

Wait, mirroring then rotating... let me think.

If I mirror the stick (blade was pointing right, now points left), then rotate 35° clockwise, the blade (now pointing left) goes to bottom-left. And stick 1's blade (pointing right) rotated 35° clockwise goes to bottom-right. 

So both blades point outward at the bottom. That's the classic crossed hockey stick look. 

Let me do that.

Stick 1: `transform="rotate(35 300 300)"`
Stick 2: `transform="translate(600 0) scale(-1 1) rotate(35 300 300)"` — this mirrors around x=300.

Hmm, let me simplify. `transform="translate(600,0) scale(-1,1) rotate(35,300,300)"`.

Actually, the order of transforms matters. Let me use: first rotate, then mirror. Or combine.

Let me just do:
Stick 2: `transform="scale(-1 1) translate(600 0) rotate(35 300 300)"`

Hmm, I need to be careful. Let me think in terms of the final effect.

I want stick 2 to be the mirror image of stick 1 across the vertical line x=300, but also rotated 35° clockwise.

Actually, simpler: I want stick 2 to be stick 1 mirrored, then both rotated. But if I mirror first then rotate, the rotation center matters.

Let me just place them independently. Let me reconsider.

You know what, let me simplify the whole thing. Let me make the two sticks cross, and I'll just draw them with explicit paths for each, no rotation complexity. Or use rotation but make it work.

Let me define a base stick pointing straight down with blade at bottom, centered at x=300.

Base stick (blade pointing right):
```
<g>
  <rect x="293" y="60" width="14" height="340" rx="7" fill="url(#stickGrad)"/>
  <path d="M 293 392 L 307 392 L 307 430 L 334 433 C 344 434, 346 447, 337 452 C 329 456, 318 452, 316 443 L 311 434 L 293 432 Z" fill="url(#stickGrad)"/>
</g>
```

Now, stick 1 rotated 40° clockwise around (300, 380):
`transform="rotate(40 300 380)"`

Stick 2: I want it mirrored. Let me create it as mirror of base then rotate -40°? 

Hmm, let me think about what "crossed hockey sticks" should look like:
- Like an X
- Both sticks have their blades at the bottom
- The blades point outward (away from center)
- The tops of the sticks point up and outward

So stick 1 (left side): top points up-left, blade at bottom-right... no wait.

Let me think. In an X made of two hockey sticks:
- One stick goes from bottom-left to top-right
- Other stick goes from bottom-right to top-left
- The blades are at the bottom, near the center-bottom
- The handles/grips are at the top, pointing up and outward

So:
- Stick A: from bottom-center to top-right. Blade at bottom, handle at top-right.
- Stick B: from bottom-center to top-left. Blade at bottom, handle at top-left.

For stick A (blade at bottom-center, pointing right/outward, handle top-right):
- Base stick points down, blade at bottom pointing right.
- Rotate so blade stays near bottom-center and handle goes to top-right.
- That's a counterclockwise rotation... let me see. Base: handle at top, blade at bottom-right. Rotate counterclockwise (negative angle): handle goes to top-right? No.

Ugh, let me just carefully think.

Base stick: handle at top (12 o'clock), blade at bottom pointing right (toward 3 o'clock direction from the blade).

I want Stick A: handle at top-right (about 1-2 o'clock), blade at bottom (about 5-6 o'clock).

To move handle from 12 o'clock to 2 o'clock, that's clockwise rotation. So rotate clockwise (positive angle in SVG since y is down, but let me use visual).

In SVG, positive rotation is clockwise (because y-axis points down). So rotate(+angle) is clockwise visually.

Base handle at top (12 o'clock). Rotate +25° (clockwise): handle moves to 1-2 o'clock (top-right). Good, that's Stick A.

Base blade at bottom pointing right (3 o'clock from blade center). After rotate +25°, blade points to about 4-5 o'clock. Good, Stick A blade at bottom-right pointing outward-right. 

Stick B: handle at top-left (10-11 o'clock), blade at bottom-left pointing outward-left.
For this, I mirror the base stick (so blade points left), then... 

If I mirror the base horizontally, handle still at top, blade at bottom pointing left. Then rotate -25° (counterclockwise): handle moves to 11 o'clock (top-left). Blade moves to 7-8 o'clock (bottom-left) pointing outward-left. 

So Stick B = mirror(base) then rotate(-25°).

To mirror around x=300: transform = translate(600, 0) scale(-1, 1), then rotate(-25, 300, 380).

Combined transform for Stick B: `translate(600,0) scale(-1,1) rotate(-25,300,380)`

Wait, transform order: they apply right-to-left in terms of the coordinate system, but the way SVG works, the transform list is applied left to right as matrix multiplications on the left of the point... Actually, transforms are applied in the order listed, each transforming the coordinate system. Let me just use the standard approach.

`transform="translate(600,0) scale(-1,1) rotate(-25,300,380)"`

This means: first translate, then scale (mirror), then rotate. Hmm, actually the way it composes: the last transform in the list is applied first to the coordinates. Let me think again.

For a point P, the transformed point is: translate · scale · rotate · P (matrix multiplication, left to right as written, but the rightmost is applied first to P).

So P' = Translate(600,0) · Scale(-1,1) · Rotate(-25,300,380) · P

Applied to P:
1. Rotate P by -25° around (300,380)
2. Scale by (-1,1): mirrors x around 0
3. Translate by (600,0)

Let me verify with the handle at top (300, 60):
1. Rotate -25° around (300,380): The handle is directly above center. Rotating -25° (counterclockwise) moves it to the left. New position: rotate point (300,60) around (300,380) by -25°. Vector from center: (0, -320). Rotate by -25°: x' = 0·cos(-25) - (-320)·sin(-25) = -320·sin(-25)... 

sin(-25°) = -0.4226. x' = 0·cos - (-320)·(-0.4226) = -320·0.4226 = -135.2. y' = 0·sin(-25) + (-320)·cos(-25) = -320·0.9063 = -289.

So rotated handle position: (300 + (-135.2), 380 + (-289)) = (164.8, 91). 

Wait let me redo. Rotation of point (x,y) around center (cx,cy) by angle θ:
x' = cx + (x-cx)cosθ - (y-cy)sinθ
y' = cy + (x-cx)sinθ + (y-cy)cosθ

(x,y) = (300, 60), (cx,cy) = (300, 380), θ = -25°:
x-cx = 0, y-cy = -320
x' = 300 + 0·cos(-25) - (-320)·sin(-25) = 300 - (-320)·(-0.4226) = 300 - 135.2 = 164.8
y' = 380 + 0·sin(-25) + (-320)·cos(-25) = 380 + (-320)(0.9063) = 380 - 289 = 91

So after rotation: (164.8, 91). This is top-left. Good.
2. Scale(-1,1): (164.8, 91) → (-164.8, 91)
3. Translate(600,0): (-164.8+600, 91) = (435.2, 91). Top-right!

Hmm, that put the handle at top-right, not top-left. So my Stick B ends up on the right side. That's wrong.

Let me reconsider. I think I overcomplicated. Let me just make Stick B the mirror of Stick A after all, which would naturally be symmetric.

Actually, the issue: I want Stick A and Stick B to be mirror images of each other across x=300, and both rotated.

Simplest: Draw Stick A with transform T. Draw Stick B with transform = mirror ∘ T ∘ mirror (conjugate), which gives the mirror image of Stick A.

If T = rotate(40, 300, 380), then mirror-image of Stick A = mirror(300) · T · mirror(300) · ... 

This is getting too complex. Let me just manually create two stick paths, or use a simpler rotation approach.

Alternative simpler approach: Don't rotate. Just draw two hockey sticks as static paths that cross. This gives me full control.

Let me draw:
- Stick 1: from top-left area down to bottom-center, blade at bottom pointing right-ish.
- Stick 2: from top-right area down to bottom-center, blade at bottom pointing left-ish.

Actually, let me reconsider and just make them cross in an X with blades at bottom.

Hmm, let me just use rotation but figure out the mirror properly.

Let me define base stick pointing down with blade at bottom pointing RIGHT.

I want:
- Stick A: base rotated by +30° (clockwise). Handle goes top-right, blade goes bottom-right pointing... let me just check.

Base handle at (300, 60) [top], blade at (300, 420) [bottom, pointing right toward (340, 440)].

Rotate +30° around (300, 380):
Handle (300,60): 
x' = 300 + 0·cos30 - (-320)·sin30 = 300 + 320·0.5 = 300+160 = 460
y' = 380 + 0·sin30 + (-320)·cos30 = 380 - 320·0.866 = 380 - 277 = 103
Handle → (460, 103). Top-right. 

Blade (300, 420):
x' = 300 + 0·cos30 - 40·sin30 = 300 - 20 = 280
y' = 380 + 0 + 40·cos30 = 380 + 34.6 = 414.6
Blade center → (280, 414.6). Bottom-center-left.
Blade toe was at (340, 440):
x' = 300 + 40·cos30 - 60·sin30 = 300 + 34.6 - 30 = 304.6
y' = 380 + 40·sin30 + 60·cos30 = 380 + 20 + 51.9 = 451.9
Toe → (304.6, 451.9). 

So Stick A: handle top-right (460,103), blade at bottom around (280-305, 415-452). The blade points down and slightly right. Handle up-right. So the stick goes from top-right to bottom-center. This is the "/" ... no, from top-right to bottom-center-left is like the backslash "\" direction? Top-right to bottom-left is "\". Yes Stick A is "\".

Hmm wait, that means Stick A's handle is at top-right and blade at bottom. So it's a stick leaning like "\" (top-right to bottom-left). 

Stick B should be the mirror: handle top-left, blade bottom-right, like "/".

To get Stick B as mirror of Stick A across x=300: I can take the base stick, and create its mirror, then rotate the same +30°.

Mirror of base stick across x=300: handle at (300,60) stays (since x=300), blade at (300,420) stays, blade toe at (340,440) → (260, 440). So mirrored base has blade pointing LEFT.

Then rotate mirrored base by +30° around (300,380):
Handle (300,60) → (460,103) as before? No wait, handle is at x=300, same as before. So handle → (460, 103) again. That's top-right, not top-left.

Hmm, that doesn't give top-left handle. The problem is the handle is on the axis of rotation, so it doesn't move with mirroring, but after rotation it goes to the same place.

I think the issue is that rotating around (300,380) moves the handle (which is on the vertical line x=300) to the right for +30° rotation regardless.

So both sticks would have handles at top-right. That's not what I want.

Let me reconsider. For a symmetric X, I need:
- Stick A: rotate base by +30° → handle top-right
- Stick B: rotate base by -30°... but then blade direction...

Let me try Stick B = base rotated by -30°:
Handle (300,60) rotated -30° around (300,380):
x' = 300 + 0·cos(-30) - (-320)·sin(-30) = 300 - 320·0.5 = 300-160 = 140
y' = 380 + 0 + (-320)·cos(-30) = 380 - 277 = 103
Handle → (140, 103). Top-left. 

Blade (300,420) rotated -30°:
x' = 300 + 0 - 40·sin(-30) = 300 - 40·(-0.5) = 300+20 = 320
y' = 380 + 0 + 40·cos(-30) = 380+34.6 = 414.6
Blade center → (320, 414.6).

Blade toe (340,440) rotated -30°:
x' = 300 + 40·cos(-30) - 60·sin(-30) = 300 + 34.6 + 30 = 364.6
y' = 380 + 40·sin(-30) + 60·cos(-30) = 380 - 20 + 51.9 = 411.9
Toe → (364.6, 411.9).

So Stick B: handle top-left (140,103), blade at bottom-center-right (320, 415), toe at (364, 412) pointing right.

So Stick B goes from top-left to bottom-center-right. That's the "/" direction. Good.

But now compare:
- Stick A: handle top-right (460,103), blade center bottom-left (280,415), toe (305, 452) pointing down.
- Stick B: handle top-left (140,103), blade center bottom-right (320,415), toe (365,412) pointing right.

Hmm, these cross but the blades aren't symmetric. Stick A's blade points down (toe at 305,452, below center), Stick B's blade toe points right (365, 412).

The crossing point: Stick A from (460,103) to ~(280,452). Stick B from (140,103) to ~(365,412). 

Do they cross? Stick A goes from top-right to bottom-center-left. Stick B goes from top-left to bottom-center-right. Yes, they cross in the middle around (300, 250).

The blades: Stick A blade at bottom around (280-305, 415-452). Stick B blade at (320-365, 412-415). So both blades are at the bottom, spread out a bit. Stick A's toe points down (452), Stick B's toe points right (365,412).

This is asymmetric but might look OK-ish. The blades point in different directions which looks a bit odd for a logo.

Let me reconsider. For a clean logo, I'd want both blades to point outward symmetrically. 

Stick A blade toe should point down-right (outward), Stick B blade toe should point down-left (outward).

For Stick A (handle top-right, i.e., "\" stick), the toe should point down-right, away from center. Currently Stick A toe points down. Let me adjust the rotation.

Hmm, actually the blade is attached to the shaft at the bottom. The toe is the tip. For the blade to point "outward" (away from the crossing center), I need the blade to extend away from center.

For Stick A (which goes top-right to bottom-left, "\"), the bottom is on the left side, so outward = down-left. But my Stick A blade toe is at (305,452), which is below-center, and blade center at (280,415). So the blade extends from (280,415) to (305,452), i.e., down and slightly right. That's toward center, not outward. Not ideal.

The problem is the base blade points right (toward 3 o'clock), and when I rotate, it doesn't point outward.

Let me reconsider the base blade direction. For the crossed sticks to have blades pointing outward:

Stick A is "\" (top-right to bottom-left). At the bottom, outward is down-left. So Stick A's blade toe should point down-left.

Base stick has handle at top, blade at bottom. If I want, after rotation, the blade toe to point down-left for Stick A...

This is getting complicated. Let me just make the base blade point DOWN (symmetric blade, like a flat bottom with slight curves), so after rotation it points outward naturally.

A symmetric blade: flat bottom, maybe with a tiny curve up at both ends. Like a hockey blade but symmetric. Then:
- Stick A rotated +30°: blade points down, after rotation the flat bottom faces down-left-ish. Toe tips point outward.
- Actually a symmetric flat-bottom blade rotated would have both tips pointing down and outward. 

Hmm, but real hockey blades aren't symmetric. But for a logo, a symmetric-ish blade is fine.

Let me make the blade a symmetric shape: a flat bottom with the two ends curving up slightly. Like:

```
Blade (symmetric):
M 293 393
L 307 393
L 307 425
C 307 435, 293 435, 293 425  ... 
```

Hmm, let me make it like a shallow "U" or a flat blade:

```
M 290 393
L 310 393
L 310 428
L 325 430
C 332 431, 332 443, 324 445
L 276 445
C 268 443, 268 431, 276 430
L 290 428
Z
```

This makes a blade that's flat at the bottom, extending from x=276 to x=324, with the ends curving up. Symmetric around x=300.

Then:
- Stick A rotate +30°: blade flat bottom now faces down-right, tips point down and outward (left tip points down-left, right tip points down-right). 

Hmm, actually if the blade is symmetric and I rotate the whole stick, the blade flat part stays perpendicular to the shaft. For Stick A ("\"), the shaft goes top-right to bottom-left, so perpendicular to it at the bottom points down-left to up-right. The blade flat face would point down-left. The tips: left tip (was at 276) and right tip (was at 324). After rotation...

This is really getting into the weeds. Let me just go with a reasonable design and stop overanalyzing. The key visual is: two crossed sticks forming an X, blades at the bottom. Even if slightly asymmetric, it'll read as crossed hockey sticks.

Let me use symmetric blades and rotations ±30° or so. Let me just build it and see.

Actually, let me simplify even more. Let me make the design where the sticks are crossed but I'll draw them as clean paths. Let me reconsider using a simpler, more iconic approach.

New plan: I'll make the crossed sticks simpler. Each stick is:
- A long shaft (thin rounded rect or line)
- A blade at one end

I'll position them with rotation. Let me use rotation ±35° and symmetric blades.

Let me just write it and trust it'll look reasonable.

Let me define the base stick pointing down with a symmetric blade:

```
<g id="stick">
  <!-- shaft -->
  <rect x="294" y="55" width="12" height="345" rx="6" fill="url(#stickGrad)"/>
  <!-- blade -->
  <path d="M 290 395 L 310 395 L 312 430 L 330 434 C 338 435, 340 447, 331 451 L 269 451 C 260 447, 262 435, 270 434 L 288 430 Z" fill="url(#stickGrad)"/>
</g>
```

Then:
- Stick 1: `<use href="#stick" transform="rotate(32 300 380)"/>`
- Stick 2: `<use href="#stick" transform="rotate(-32 300 380)"/>`

Wait, but if both use the same base and just rotate differently, and the blade is symmetric, then:
- Stick 1 (rotate +32°): handle top-right, blade bottom pointing... symmetric blade, so it points down-ish.
- Stick 2 (rotate -32°): handle top-left, blade bottom pointing down-ish.

Both blades point down. They'd be close together at the bottom. That might look like both blades at bottom-center. That's OK for crossed sticks actually.

Hmm, but actually with symmetric blades and these rotations, the two blades would overlap a lot in the center. Let me think...

Stick 1 blade center after +32°: around (300+something, 415). Stick 2 blade center after -32°: around (300-something, 415). They'd be near each other. The blades (each ~70 wide) would overlap. That looks like a bunch of blades at the bottom, which is actually fine and common in hockey logos.

Actually, you know, let me reconsider. Many hockey logos have the blades crossing/overlapping at the bottom. That's the classic look. So overlapping blades at the bottom-center is good.

Let me go with symmetric blades and rotations. Let me use a slightly larger rotation so the handles spread out more: ±35°.

OK here's my concern though: with rotation ±35° and symmetric blades, the blades will point outward and down, spreading apart. Let me just check:

Stick 1 blade, symmetric, from x=269 to x=331 (width 62), centered at 300, at y≈440. Rotate +35° around (300,380):
- Left tip (269, 445): 
  x' = 300 + (269-300)cos35 - (445-380)sin35 = 300 + (-31)(0.819) - (65)(0.574) = 300 - 25.4 - 37.3 = 237.3
  y' = 380 + (-31)(0.574) + (65)(0.819) = 380 - 17.8 + 53.2 = 415.4
  Left tip → (237, 415)
- Right tip (331, 445):
  x' = 300 + 31·cos35 - 65·sin35 = 300 - 25.4 - 37.3 = 237.3
  
  Wait that's the same. Let me redo. cos35=0.819, sin35=0.574.
  Right tip (331,445): x-cx=31, y-cy=65.
  x' = 300 + 31·0.819 - 65·0.574 = 300 + 25.4 - 37.3 = 288.1
  y' = 380 + 31·0.574 + 65·0.819 = 380 + 17.8 + 53.2 = 451
  Right tip → (288, 451)

So Stick 1 blade spans from (237,415) to (288,451). Points down-left. 
Stick 1 handle (300,55): 
  x' = 300 + 0 - (55-380)·sin35 = 300 - (-325)(0.574) = 300 + 186.6 = 486.6
  y' = 380 + 0 + (-325)(0.819) = 380 - 266.2 = 113.8
  Handle → (487, 114). Top-right.

So Stick 1: handle top-right (487,114), blade down-left from (237,415) to (288,451). This is a "\" stick. The blade is at bottom-left, pointing down-left (outward). 

Stick 2 (rotate -35°): by symmetry, handle top-left (113, 114), blade at bottom-right from (312,415) to (363,451), pointing down-right (outward). 

So the two blades: Stick 1 blade at bottom-left (237-288), Stick 2 blade at bottom-right (312-363). They're separated, both pointing outward-down. And they cross in the middle. This looks like proper crossed hockey sticks! 

The crossing point: Stick 1 from (487,114) to ~(260,433) [blade midpoint]. Stick 2 from (113,114) to ~(340,433). They cross around (300, 270) or so. Good.

Great, this design works. Let me use rotation ±35° with symmetric blades.

Wait, I realize the blades point outward and there's a gap between them at the bottom. Some logos have blades overlapping. But separated blades pointing outward is also fine and clean. Let me keep it.

Hmm, actually, let me reconsider—maybe I want the blades closer/overlapping for the classic look. But let me go with what I calculated; it looks clean.

Actually, let me reconsider the whole composition. The owl will be in front, centered around (300, 250-350). The sticks cross behind. The blades are at the bottom around y=415-451. The owl body would be around y=260-400. So the owl covers the crossing area and the blades are below/around the owl. That should look fine.

Wait, but the owl is in FRONT of the sticks. So the sticks are behind the owl. The blades at the bottom would be visible below the owl, sticking out on both sides. That looks good—like the owl is holding/standing with crossed sticks behind.

Let me set the owl body to end around y=400, and the blades at y=415-451 would show below. Good.

Now let me design the owl.

Owl centered at x=300.
- Head/eyes area: y=150-260
- Body: y=260-400
- Ear tufts: top around y=130-155

Let me design:

Ear tufts (two pointed shapes):
- Left: path from (258,155) up to a point at (238,115) and back to (278,150)
- Right: mirrored

Head (main circle/oval for the head):
- Center (300, 195), radius ~70. So from y=125 to y=265, x=230 to 370.

Actually, let me make the head and body flow together. Owls have a body that widens at the bottom.

Let me make the body:
- A rounded shape from the head down to a rounded belly.

Let me define the body path:
```
Start at top of head (300, 140)
Curve out to left ear area, around (240, 160)
Down the left wing/side to (225, 300)
Curve to bottom belly (300, 405)
Up the right side to (375, 300)
To right ear area (360, 160)
Back to top (300, 140)
```

Hmm, let me make it cleaner with an ellipse for the body and a circle for the head, overlapping.

Actually, let me make a unified body shape:

```
<body>
M 300 145
C 260 145, 235 170, 235 210  (left side going down from head)
C 235 250, 225 300, 245 340  (left wing to belly)
C 260 375, 280 395, 300 395  (bottom belly)
C 320 395, 340 375, 355 340  (right side up)
C 375 300, 365 250, 365 210  (right wing)
C 365 170, 340 145, 300 145  (top back to head)
Z
```

This makes a rounded body. Good.

Eyes: two large circles.
- Left eye: center (265, 195), radius 34
- Right eye: center (335, 195), radius 34

Eye whites: white circles.
Iris: colored circle (gold/orange), radius ~22.
Pupil: dark circle, radius ~12, centered or slightly inward.
Eye highlight: small white circle.

Beak: small triangle or shield shape between the eyes, below.
- Beak: from (285, 225) to (315, 225) to (300, 250). A downward triangle. Or a small shield.

Let me make the beak a small shape:
```
<path d="M 288 226 L 312 226 L 300 252 Z" fill="#F4A63A"/>
```
Actually owl beaks are often covered by feathers. Let me make it a small inverted triangle or shield. Belly:

Belly: a lighter-colored shape in the lower body.
- Ellipse at (300, 330), rx=55, ry=65, fill light color.

Belly feather lines: small arcs or V shapes on the belly.
Let me add a few curved lines.

Wings: two wing shapes on the sides, slightly darker.
- Left wing: a shape on the left side.
- Right wing: mirrored.

Let me add wings as paths:
```
<path d="M 240 250 C 220 280, 220 330, 245 360 C 235 330, 240 280, 258 255 Z" fill="..."/>
```
Hmm, let me make wings simpler. Maybe just darker shapes on the sides.

Actually, let me add wing details as curved lines rather than separate shapes, to keep it clean.

Let me also add feather texture on the belly with small arcs.

Let me also add the face disc (the heart-shaped lighter area around the eyes). Owls have a distinct face disc. Let me add a lighter circle behind the eyes.

OK let me just write the whole thing and refine.

Let me also add text "Owayo Eulers" at the bottom.

For text, I'll use a bold font. Let me use font-family="Arial, sans-serif" font-weight="bold". I'll center it.

"Owayo Eulers" — let me place it at y=540 or so, centered at x=300. But the text might be wide. Let me size it appropriately. At font-size 42, "Owayo Eulers" (14 chars) is roughly 14*24 = 336px wide, which fits in 600. Let me use font-size 40.

Actually, let me reconsider the layout. Maybe put text at the bottom, and have the owl + sticks above. Total height ~640.

Let me set:
- Sticks and owl: y from 50 to 460
- Text: y=540 (baseline), so text occupies ~500-545.

Let me finalize dimensions: viewBox="0 0 600 640".

Let me also consider adding a subtle outline or a circular badge. The user said solid background or no background. I'll go with no background (transparent). But maybe add a thin circular border to frame it like a logo. Actually, a badge circle is common for sports logos. Let me add a thin circle outline around the design. But the user said no background preferred. A thin ring outline isn't a background, so it's fine. Let me add a subtle ring.

Hmm, but they said "am besten besitzt das Logo gar keinen Hintergrund" (preferably the logo has no background at all). So I'll keep it transparent. I can still add a decorative ring/border as part of the design (not background). Let me add a thin ring to frame it, which is typical for logos. Actually, let me add the ring as it makes it look more like a proper logo/emblem. But I'll keep it subtle.

Let me reconsider—maybe I'll add a ring. Let me add a circle outline at radius ~255 centered at (300, 290). Hmm, but the text is below. Let me make the ring around the owl/sticks area only, and text below outside the ring. Or put text inside/over the ring.

Let me do: ring around the emblem (owl + sticks), text below the ring.

Ring: circle at (300, 285), r=250, stroke, no fill. But that would extend to y=35 and y=535, overlapping text area. Let me adjust.

Actually, let me make the emblem fit in the ring and text inside the ring at the bottom, or text below.

Let me reconsider layout:
- Ring centered at (300, 300), r=255. Extends x from 45 to 555, y from 45 to 555.
- Owl and sticks inside.
- Text "Owayo Eulers" along the bottom inside the ring, or below.

Putting curved text inside a ring is complex (needs textPath). Let me avoid curved text. Let me put straight text below the ring.

Layout:
- Ring: (300, 270), r=240. y from 30 to 510.
- Owl + sticks: inside ring, y from ~60 to ~460.
- Text: at y=545, below ring.

Hmm, the ring at r=240 centered y=270 goes to y=510. Text at y=545 is just below. OK.

Actually, let me simplify and not use a ring, or use a simpler frame. Let me reconsider.

Given the complexity, let me just make a clean emblem without a full ring, but maybe with a subtle circular border. Or I'll skip the ring and just have the owl + sticks + text, which is clean and matches "no background."

Let me go with: crossed sticks behind, owl in front, text below. Maybe a thin decorative ring. I'll add the ring as it looks more "logo-like."

Let me finalize the design and write the SVG.

Let me reconsider colors:
- Owl body: deep green (#2E6B53 to #16402F gradient) — nice forest green, owl-like.
- Owl belly: lighter (#D9E8D0 or cream).
- Eyes: gold (#F2B705) with dark pupils.
- Beak: orange (#F2931A).
- Hockey sticks: wood brown (#B8860B / #8B5A2B) or maybe a team color. Let me use a gold/wood tone.
- Text: dark green or a contrasting color. Let me use dark green (#16402F) or gold.

Let me pick a cohesive palette:
- Primary green: #1E5644 (dark), #2E7D5F (mid), #4CAF7F (light)
- Gold: #F4C211 / #E0A400
- Wood stick: #A06A3A / #6E4B24
- Belly: #EAF2E2 / cream
- Eyes: #F4C211 gold

Let me write it.

Actually, let me reconsider the owl eye color. Golden eyes look great for an owl. Let me use gold irises.

Let me now also think about making the owl look good. Key features:
1. Large forward-facing eyes (owl characteristic)
2. Ear tufts (some owls have them, like eagle owls)
3. Small beak between eyes
4. Rounded body
5. Belly feather pattern

Let me write the SVG.

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 640" width="600" height="640">
  <defs>
    <linearGradient id="bodyGrad" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#3E8E6B"/>
      <stop offset="1" stop-color="#1B5441"/>
    </linearGradient>
    <linearGradient id="bellyGrad" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#EFF5E8"/>
      <stop offset="1" stop-color="#CFE0C6"/>
    </linearGradient>
    <linearGradient id="stickGrad" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="#C68A4A"/>
      <stop offset="0.5" stop-color="#A86E32"/>
      <stop offset="1" stop-color="#7A4E20"/>
    </linearGradient>
    <radialGradient id="irisGrad" cx="0.5" cy="0.4" r="0.6">
      <stop offset="0" stop-color="#FCE89A"/>
      <stop offset="0.5" stop-color="#F4C211"/>
      <stop offset="1" stop-color="#C8960A"/>
    </radialGradient>
  </defs>
  
  <!-- ===== Hockey Sticks ===== -->
  <g>
    <!-- Stick 1 -->
    <g transform="rotate(35 300 300)">
      <rect x="294" y="60" width="12" height="340" rx="6" fill="url(#stickGrad)"/>
      <path d="M 288 396 L 312 396 L 313 432 L 332 437 C 341 439, 342 451, 333 455 L 267 455 C 258 451, 259 439, 268 437 L 287 432 Z" fill="url(#stickGrad)"/>
    </g>
    <!-- Stick 2 -->
    <g transform="rotate(-35 300 300)">
      <rect x="294" y="60" width="12" height="340" rx="6" fill="url(#stickGrad)"/>
      <path d="M 288 396 L 312 396 L 313 432 L 332 437 C 341 439, 342 451, 333 455 L 267 455 C 258 451, 259 439, 268 437 L 287 432 Z" fill="url(#stickGrad)"/>
    </g>
  </g>
  
  <!-- ===== Owl ===== -->
  ...
  
  <!-- ===== Text ===== -->
  <text x="300" y="560" text-anchor="middle" font-family="Arial, Helvetica, sans-serif" font-size="46" font-weight="bold" fill="#1B5441" letter-spacing="1">Owayo Eulers</text>
</svg>
```

Wait, I need to double check the stick rotation. Earlier I calculated with rotation center (300,380) and handle at y=55. Now I have handle at y=60 and rotation center (300,300). Let me recompute to make sure the sticks look right.

Actually, the rotation center affects where they cross. Let me use (300, 300) as center. The handle is at y=60 (distance 240 above center), blade at y=455 (distance 155 below center).

Hmm, with center at (300,300):
Stick 1 (rotate +35°):
Handle (300,60): 
  x' = 300 + 0 - (60-300)sin35 = 300 - (-240)(0.574) = 300 + 137.7 = 437.7
  y' = 300 + 0 + (-240)cos35 = 300 - 196.5 = 103.5
  Handle → (438, 104). Top-right. Good.
Blade center (300, 425) [midpoint of blade]:
  x' = 300 + 0 - (425-300)sin35 = 300 - 125·0.574 = 300 - 71.75 = 228.25
  y' = 300 + 0 + 125·cos35 = 300 + 102.4 = 402.4
  Blade center → (228, 402). Bottom-left. Good.

So Stick 1: handle top-right (438,104), blade bottom-left (228,402). "\" direction. 

Stick 2 (rotate -35°): by symmetry, handle top-left (162,104), blade bottom-right (372,402). "/" direction. 

They cross around (300, 250). Blades at bottom, spread out (228 left, 372 right). 

The owl is centered at (300, ~270). The crossing is at (300,250), behind the owl. The blades at (228,402) and (372,402) are at the bottom, below and to the sides of the owl. Good.

Now the owl body should cover the crossing area. Let me make the owl body extend from y≈140 to y≈400. The blades at y≈402 would be just below the owl body bottom. And the blades' x-extent: Stick 1 blade spans roughly from (228,402) outward. The blade is ~54 wide (from 267 to 332 in base, width 65). After rotation, it's spread. Let me estimate: Stick 1 blade tips were at (267,455) and (333,455). After rotate +35°:
  (267,455): x' = 300 + (267-300)cos35 - (455-300)sin35 = 300 + (-33)(0.819) - (155)(0.574) = 300 - 27 - 89 = 184; y' = 300 + (-33)(0.574) + (155)(0.819) = 300 - 19 + 127 = 408. → (184, 408)
  (333,455): x' = 300 + 33·0.819 - 155·0.574 = 300 + 27 - 89 = 238; y' = 300 + 33·0.574 + 155·0.819 = 300 + 19 + 127 = 446 → (238, 446)
  
So Stick 1 blade spans (184,408) to (238,446). It's at the bottom-left, pointing down-left (outward). Good.
Stick 2 blade spans (362,408) to (416,446) by symmetry, bottom-right, pointing down-right. Good.

So the blades stick out at the bottom-left and bottom-right, below the owl. 

The owl body bottom should be around y=400 so it overlaps the top of the blades (where they cross). Let me make owl body bottom at y≈395. The blades cross around y=250 and spread down to y=446 at the tips. The owl covers the center. Good.

Now let me design the owl.

Owl:
- Body: from head top (~140) to belly bottom (~395), centered x=300.

Let me define body path:
```
M 300 148
C 268 148, 246 168, 242 200   (left head/ear)
C 236 240, 228 300, 248 342    (left side/wing down)
C 262 374, 280 392, 300 392    (bottom belly)
C 320 392, 338 374, 352 342    (right side)
C 372 300, 364 240, 358 200    (right head/ear)
C 354 168, 332 148, 300 148
Z
```

This gives a rounded body. Let me verify it looks owl-like. The top has a slight indentation where the ear tufts are. Actually, let me add ear tufts separately.

Ear tufts:
```
Left ear: <path d="M 256 168 L 232 120 L 282 158 Z" fill="url(#bodyGrad)"/>
Right ear: <path d="M 344 168 L 368 120 L 318 158 Z" fill="url(#bodyGrad)"/>
```

Hmm, let me make them more like feather tufts.

Eyes:
- Eye sockets/whites: two circles.
- Left: center (266, 198), r=36, white fill, dark stroke.
- Right: center (334, 198), r=36, white fill.
- Iris: same centers, r=24, gold radial gradient.
- Pupil: same centers, r=12, dark (#1a1a1a).
- Highlight: small white circle at offset.

Actually, for a striking owl, let me make the eyes large and golden. Let me also add a dark ring around the eyes (eye rings).

Beak:
- Small shape below and between eyes, pointing down.
- Center (300, 232).
- Path: M 286 228 L 314 228 L 300 256 Z (triangle), fill orange. Maybe with a slight curve.

Let me make beak a shield shape:
```
<path d="M 285 226 Q 300 222 315 226 Q 308 248 300 256 Q 292 248 285 226 Z" fill="#F0931E"/>
```

Belly:
- Lighter ellipse: center (300, 330), rx=52, ry=62, fill bellyGrad.

Belly feather lines: small V or arc shapes. Let me add a few.
```
<path d="M 270 300 Q 300 315 330 300" fill="none" stroke="#B7CBA9" stroke-width="3"/>
<path d="M 268 330 Q 300 347 332 330" fill="none" stroke="#B7CBA9" stroke-width="3"/>
<path d="M 272 360 Q 300 377 328 360" fill="none" stroke="#B7CBA9" stroke-width="3"/>
```

Wings:
- Left wing: a darker shape on the left side of the body.
- Let me add wing shapes:
```
<path d="M 246 255 C 222 275, 218 320, 240 350 C 232 315, 240 280, 262 262 Z" fill="#1B5441"/>
<path d="M 354 255 C 378 275, 382 320, 360 350 C 368 315, 360 280, 338 262 Z" fill="#1B5441"/>
```

Hmm, let me refine. Wings should look like they attach to the side and point down.

Actually, let me reconsider the whole owl to make it cohesive. Let me draw it as:
1. Body (main shape)
2. Ear tufts
3. Face disc (lighter area around eyes) - optional
4. Eyes
5. Beak
6. Belly (lighter) + feather lines
7. Wings (darker shapes on sides)

Let me write it all out.

Let me reconsider the belly. If I put a light belly ellipse over the body, and the wings on the sides, it should look like an owl. Let me make sure the belly ellipse is within the body.

Body at y=330: the body width there. Body path at y=330... the body goes from x≈240 (left) to x≈360 (right) around y=300, narrowing toward bottom. At y=330, maybe x from 250 to 350. Belly ellipse rx=52 centered at 300 → x from 248 to 352. OK fits.

Let me also add a subtle outline to the owl body for definition.

Let me write the full SVG now.

Also, I should double-check: the user wants the logo to contain an owl AND a hockey stick. I have both. Good. Team name "Owayo Eulers" in text. Good.

Let me also reconsider: "Euler" is a play on "owl" (Eule in German) and the mathematician Euler. "Owayo" might be a made-up word or a place. Anyway, the text is "Owayo Eulers".

Let me finalize.

One more consideration: the text "Owayo Eulers" — I should make sure it's readable and looks good. Let me use a bold sans-serif. Maybe add a small decorative line under it or a subtitle. Let me keep it simple: just the text, maybe with the sticks' design.

Let me also think about whether to add a year or slogan. The user didn't ask, so I'll keep it minimal: just "Owayo Eulers".

Let me write the final SVG.

Actually, let me reconsider the eyes to make them look more owl-like and cool. Let me add:
- Dark outline around each eye
- Golden iris
- Large black pupil
- Two white highlights (catchlights)

Let me make the eyes really pop.

Also, let me add a "brow" — owls have a distinctive brow ridge. Let me add a slight darker shape above the eyes.

Let me refine the eye area. I'll add a lighter face disc (the heart/round lighter feathers around eyes) to make it look more owl-like.

Face disc: lighter colored circles behind the eyes, blending into the head. Let me add two lighter circles behind each eye, or a lighter head shape.

Hmm, let me keep it clean. I'll add subtle eye rings and brows.

Let me write it out now. I'll iterate.

Final SVG:

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 640" width="600" height="640">
  <defs>
    <linearGradient id="bodyGrad" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#459E76"/>
      <stop offset="0.5" stop-color="#2B7054"/>
      <stop offset="1" stop-color="#184B3B"/>
    </linearGradient>
    <linearGradient id="bellyGrad" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#EFF5E8"/>
      <stop offset="1" stop-color="#CDE0C2"/>
    </linearGradient>
    <linearGradient id="stickGrad" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="#CE9A58"/>
      <stop offset="0.5" stop-color="#AE7636"/>
      <stop offset="1" stop-color="#7C4E1F"/>
    </linearGradient>
    <radialGradient id="irisGrad" cx="0.5" cy="0.35" r="0.65">
      <stop offset="0" stop-color="#FDF0B8"/>
      <stop offset="0.45" stop-color="#F5C518"/>
      <stop offset="1" stop-color="#C4900A"/>
    </radialGradient>
  </defs>

  <!-- Hockey Sticks (behind owl) -->
  <g>
    <g transform="rotate(35 300 300)">
      <rect x="294" y="60" width="12" height="340" rx="6" fill="url(#stickGrad)"/>
      <path d="M 287 396 L 313 396 L 314 433 L 333 438 C 342 440, 343 452, 334 456 L 266 456 C 257 452, 258 440, 267 438 L 286 433 Z" fill="url(#stickGrad)"/>
    </g>
    <g transform="rotate(-35 300 300)">
      <rect x="294" y="60" width="12" height="340" rx="6" fill="url(#stickGrad)"/>
      <path d="M 287 396 L 313 396 L 314 433 L 333 438 C 342 440, 343 452, 334 456 L 266 456 C 257 452, 258 440, 267 438 L 286 433 Z" fill="url(#stickGrad)"/>
    </g>
  </g>

  <!-- Owl -->
  <g>
    <!-- Body -->
    <path d="M 300 150
             C 266 150, 244 172, 240 206
             C 234 248, 226 302, 248 344
             C 264 376, 283 394, 300 394
             C 317 394, 336 376, 352 344
             C 374 302, 366 248, 360 206
             C 356 172, 334 150, 300 150 Z"
          fill="url(#bodyGrad)" stroke="#12382c" stroke-width="3"/>

    <!-- Ear tufts -->
    <path d="M 258 170 L 232 118 L 286 158 Z" fill="url(#bodyGrad)" stroke="#12382c" stroke-width="2.5"/>
    <path d="M 342 170 L 368 118 L 314 158 Z" fill="url(#bodyGrad)" stroke="#12382c" stroke-width="2.5"/>

    <!-- Belly -->
    <ellipse cx="300" cy="332" rx="52" ry="64" fill="url(#bellyGrad)"/>

    <!-- Belly feather lines -->
    <g stroke="#B3C8A4" stroke-width="3" fill="none" stroke-linecap="round">
      <path d="M 270 302 Q 300 318 330 302"/>
      <path d="M 266 334 Q 300 352 334 334"/>
      <path d="M 271 366 Q 300 383 329 366"/>
    </g>

    <!-- Wings -->
    <path d="M 246 258 C 220 278, 216 324, 240 356 C 230 316, 240 282, 264 266 Z" fill="#184B3B"/>
    <path d="M 354 258 C 380 278, 384 324, 360 356 C 370 316, 360 282, 336 266 Z" fill="#184B3B"/>

    <!-- Eye rings -->
    <circle cx="266" cy="198" r="40" fill="#E7F0DE" stroke="#12382c" stroke-width="3"/>
    <circle cx="334" cy="198" r="40" fill="#E7F0DE" stroke="#12382c" stroke-width="3"/>

    <!-- Irises -->
    <circle cx="266" cy="198" r="26" fill="url(#irisGrad)"/>
    <circle cx="334" cy="198" r="26" fill="url(#irisGrad)"/>

    <!-- Pupils -->
    <circle cx="266" cy="198" r="13" fill="#141414"/>
    <circle cx="334" cy="198" r="13" fill="#141414"/>

    <!-- Highlights -->
    <circle cx="258" cy="189" r="6" fill="#FFFFFF"/>
    <circle cx="326" cy="189" r="6" fill="#FFFFFF"/>
    <circle cx="272" cy="205" r="3" fill="#FFFFFF" opacity="0.7"/>
    <circle cx="340" cy="205" r="3" fill="#FFFFFF" opacity="0.7"/>

    <!-- Beak -->
    <path d="M 285 228 Q 300 224 315 228 Q 308 250 300 260 Q 292 250 285 228 Z" fill="#F0931E" stroke="#B5660F" stroke-width="2"/>
  </g>

  <!-- Text -->
  <text x="300" y="558" text-anchor="middle" font-family="Arial, Helvetica, sans-serif" font-size="50" font-weight="bold" fill="#184B3B" letter-spacing="2">Owayo Eulers</text>
</svg>
```

Let me review this. The owl looks reasonable. Let me check a few things:

1. The eyes are at y=198, which is within the head area. Good.
2. The beak at y=228-260, between and below eyes. Good.
3. The belly at y=332, below the eyes. Good.
4. Wings on the sides. Good.
5. Ear tufts at top. Good.

The sticks cross behind. The blades at the bottom. Good.

Text at y=558.

Let me reconsider the proportions. The owl body goes from y=150 to y=394. The sticks go from y=60 to y=456. So the stick handles stick up above the owl (to y=60, rotated to ~104), and blades at bottom (~402-456). The owl is in front.

Wait, the stick handles are rotated to top-right/top-left around (438,104) and (162,104). The owl head top is at y=150. So the stick handles stick out above and to the sides of the owl. Good, that looks like crossed sticks behind the owl.

Let me double check the stick handles don't overlap the owl's head awkwardly. The handle ends at (438,104) and (162,104). The owl head is around x=240-360, y=150-260. So the handles are above and outside the head. Good.

The shafts go from the handles down to the crossing point (~300,250) and continue to the blades. The shafts are behind the owl, visible on the sides (from x=162-240 on left, x=360-438 on right). Good.

Now, let me reconsider: is the crossing point behind the owl? The crossing is at ~(300,250). The owl body covers x=240-360, y=150-394. So yes, the crossing is behind the owl's chest. Good. The shafts are visible on the sides.

Let me reconsider the blade positions. Stick 1 blade at bottom-left ~(184-238, 408-446). Stick 2 blade at bottom-right ~(362-416, 408-446). These are below the owl body (which ends at y=394) and to the sides. Good.

Hmm wait, the owl body bottom is at y=394 (the path's lowest point is 300,394). The blades are at y=408-446. So there's a small gap between the owl bottom and the blades. The blades are below the owl, sticking out. That's fine and looks intentional (like the owl stands on/behind the crossed sticks).

Actually, let me make the owl body extend a bit lower or the blades start higher so they overlap nicely. Let me check: the shafts continue past the crossing to the blades. The shaft is at x=294-306 (base), rotated. After rotation, the shaft bottom (y=400 in base) goes to... 

Base shaft bottom at (300, 400). Rotate +35° around (300,300):
  x' = 300 + 0 - 100·sin35 = 300 - 57.4 = 242.6
  y' = 300 + 100·cos35 = 300 + 81.9 = 381.9
  → (243, 382)

So the shaft bottom is at (243, 382) for stick 1, then the blade extends from there down-left to ~(184-238, 408-446). The owl body bottom is at (300,394). So the shaft bottom (243,382) is to the left and slightly above the owl bottom. The owl body at x=243 is around... the body left edge at y=382 is around x=258 (since body narrows). Hmm, so the shaft bottom at (243,382) might stick out slightly to the left of the body. Let me check body left edge at y=382.

Body path near bottom: "C 264 376, 283 394, 300 394" on the right, and "C 317 394, 336 376, 352 344"... the left side is "C 234 248, 226 302, 248 344 C 264 376, 283 394, 300 394". At y=382, the left edge is around x=262 (between 248 at y=344 and 283 at y=376... interpolating, at y=382 maybe x≈258). 

So the shaft bottom at x=243 is to the left of the body edge (258) at that height. So the shaft would stick out slightly to the left. That might look a bit odd but is probably OK since it's behind. Actually, since it's behind the owl, and the owl body is drawn after (in front), the shaft would be hidden where it overlaps the body. Only the part sticking out to the left would show. That's fine—it looks like the stick handle/shaft poking out behind the owl.

Hmm, actually I realize the shafts might look weird poking out. Let me reconsider. In a good crossed-stick-behind-owl logo, the sticks should be mostly hidden behind the owl, with just the handles sticking out at top and blades at bottom. Let me make sure the shafts are hidden.

The shafts go from handles (top, outside the owl) down through the crossing (behind owl) to the blades (bottom, outside the owl). The middle parts are behind the owl (hidden). The handles and blades stick out. This is the desired look. The only issue is if the shafts poke out the sides. Let me check.

Stick 1 shaft: from handle (438,104) to shaft bottom (243,382), passing through crossing (~300,250). The part from (438,104) to (~300,250) is to the right of center, outside the owl (owl right edge ~360). So this part sticks out to the right. Then from (~300,250) to (243,382) is behind the owl (hidden). 

Wait, that means a long part of the shaft sticks out to the top-right. That's the handle area, which is fine (the handle/grip sticks out top-right). And the lower shaft is hidden. Then the blade sticks out bottom-left. 

Hmm, so Stick 1: handle top-right (sticks out), shaft hidden in middle, blade bottom-left (sticks out). Similarly Stick 2: handle top-left, blade bottom-right. This is the classic crossed-stick look. 

But wait, I need to double-check that the shafts don't poke out the sides awkwardly. The shaft from (438,104) to (300,250): this line, does it cross the owl's right side? The owl's right side (shoulder) is around x=360 at y=250. The shaft at y=250 is at x=300 (crossing point). So at y=250, shaft is at x=300, inside the owl. As we go up to (438,104), the shaft moves right and up, exiting the owl's top-right area around... where the shaft crosses the owl boundary. The owl top-right is around (350,160) to (360,200). The shaft line from (300,250) to (438,104): at what y does x=360? 

Parametrize: from (300,250) to (438,104), t from 0 to 1. x = 300 + 138t, y = 250 - 146t. x=360 → t=0.43, y=250-63=187. So at (360,187), the shaft exits the owl. Above that (t>0.43), the shaft is outside the owl to the right. So the shaft sticks out from (360,187) up to (438,104). That's a visible shaft segment on the top-right. 

Is that a problem? It looks like the stick handle sticking out to the top-right, behind the owl. That's actually fine and expected. The visible part is the upper shaft + handle. Good.

Similarly for stick 2, visible shaft on top-left.

And the blades at bottom-left (stick 1) and bottom-right (stick 2) stick out below the owl. Good.

So the overall look: owl in center, two stick handles sticking out top-left and top-right, two blades sticking out bottom-left and bottom-right. Classic hockey owl logo. 

Now, let me reconsider the blade visibility. Stick 1 blade at bottom-left ~(184-238, 408-446). The owl body bottom is at (300,394). At the blade's x-range (184-238), the owl body doesn't extend that low (owl body bottom is only at x=300). So the blade is fully visible at bottom-left. Good.

Alright, the design should work. Let me also reconsider whether the owl eyes should look in a particular direction. Currently pupils centered. Let me make them look forward/slightly toward each other or toward the viewer. Centered is fine, or slightly inward. Let me keep centered or move pupils slightly toward center (toward the beak). Owls looking straight ahead. Let me move pupils slightly down and toward center. Actually, let me put pupils centered for a direct stare, or slightly toward the beak (down). Let me move them slightly down and toward center for a focused look.

Let me set pupils at (270, 200) and (330, 200) — slightly toward center and down. Hmm, or keep at eye center. Let me keep them at eye center (266,198) and (334,198) for a straight-ahead stare. Actually, let me shift slightly toward the beak (down and center): pupils at (270, 202) and (330, 202). This gives a focused forward-down gaze. Let me do that. Actually, simpler to keep centered. Let me keep at eye center.

Hmm, let me reconsider—maybe make the pupils look a bit more "cool"/focused. Let me shift them slightly toward center: (271, 197) and (329, 197). And keep highlights in upper-left. This gives a determined look. Let me do that.

Actually, let me not overthink. Let me keep pupils at eye center for symmetry. Direct stare.

Let me reconsider the overall composition once more and finalize.

Actually, I want to reconsider the eye size and position relative to the head. Eyes at (266,198) and (334,198), radius 40 for the white ring. So eyes span x from 226 to 306 (left eye) and 294 to 374 (right eye). The gap between eyes is from 306 to 294, i.e., they're close together (12px gap). Good, owls have close eyes.

The head is from x=240 to 360 (at eye level y=198). Wait, at y=198, the head (body path) spans... the body path at y=198: left side "C 266 150, 244 172, 240 206" — at y=198, x≈241. Right side x≈359. So head spans x=241-359 at y=198. The eyes (226-306 and 294-374) slightly extend beyond the head (241-359) on the outer sides. The outer edges of eyes at x=226 and x=374, but head edge at 241 and 359. So the outer 15px of each eye extends slightly beyond the head. That might look like the eyes are slightly outside the head, which is fine for a stylized owl (big eyes). Actually, it might look better if eyes are fully within the head. Let me shrink eyes slightly or move them in.

Let me move eyes to (268,198) and (332,198) with radius 36. Then eyes span 232-304 and 296-368. Head spans 241-359. So left eye outer edge at 232 is still slightly left of head edge 241. Hmm. Let me reduce eye radius to 34 and move to (270,198),(330,198). Eyes span 236-304 and 296-364. Still slightly outside. 

Actually, for an owl, big eyes that nearly touch and are large is the look. Slightly extending the eyes beyond the head outline is acceptable in stylized designs. But to be safe, let me make the head a bit wider or eyes a bit smaller. 

Alternatively, let me not have a strict head outline separate from body—since the body path IS the head+body. The eyes are drawn on top. If eyes extend slightly beyond the body outline at the sides, it just means the eyes are large. For a cartoon owl, that's fine and looks good (big owl eyes). Let me keep eyes at radius 38, centered (267,197) and (333,197). Actually, let me keep them a bit inside to look clean. Let me use radius 35, centers (268,197) and (332,197).

Hmm, I'll go with eyes radius 37, centers (267,197) and (333,197). The white ring radius 37 spans 230-304 and 296-370. Head at y=197 spans ~241-359. So eyes extend ~11px beyond head on outer sides. I think that's OK—it gives big striking owl eyes. Let me keep it. Actually, let me reduce to make it cleaner: radius 34.

You know, let me just go with it. Big owl eyes are iconic. Let me use radius 36 for the white part.

Let me also reconsider: should there be a face disc (lighter area)? I added white circles (E7F0DE) behind the eyes as "eye rings/disc". That works as a face disc. Good.

Let me finalize. Let me also add a subtle stroke to the belly to define it.

Let me also reconsider the belly feather lines color—#B3C8A4 is a muted green-gray, might be too subtle on the light belly. Let me use a slightly darker/brownish line, like #A8B896 or a warm #C4A877. Let me use #B0A888 (warm gray) for feather lines, more feather-like.

Let me finalize the SVG.

Let me also reconsider the text. "Owayo Eulers" at font-size 50, letter-spacing 2. Width estimate: roughly 14 characters. At font-size 50 bold Arial, avg char width ~30px, so ~420px. Centered at x=300, spans x=90 to 510. Fits within 600. Good.

Let me also maybe add a small decorative element under the text, like a thin line or the sticks' continuation. Let me keep it simple with just text, but maybe add a small underline accent. Actually, let me add two small horizontal lines/flourish beside or under. Hmm, let me keep minimal—just the text. Or I could add a thin line under the text. Let me add a subtle line.

Actually, let me reconsider adding a ring/badge to frame it as a proper logo. Let me add a thin circular ring around the owl+sticks, and put the text along the bottom or below. Given the user wants a logo, a ring/emblem frame would make it look more complete. But they also said no background. A ring isn't a background. Let me add a subtle ring.

Hmm, but a full ring around might clip the sticks (which stick out). Let me think. The sticks extend from ~(162,104) to ~(438,104) at top, and blades at ~(184-416, 446) at bottom. A ring centered at (300,290) with radius 250 would span x=50-550, y=40-540. The stick handles at (162,104) and (438,104) are within this (distance from center: sqrt(138²+186²)=232 < 250, so inside). Blades at (184,446): distance from (300,290) = sqrt(116²+156²)=194 <250, inside. So all within ring. The ring would frame everything. But then the text "Owayo Eulers" at y=558 is below the ring (ring bottom at y=540). 

Hmm, let me place the ring and integrate text. Let me put the ring centered at (300, 285), radius 245. Ring bottom at y=530. Text at y=560 (below ring). Or put text inside the ring at the bottom.

Actually, let me reconsider. A ring might complicate the "no background" aesthetic and the clean look. Let me skip the ring and keep it clean: owl + sticks + text. This directly satisfies "owl and hockey stick, no background." Clean and modern.

Wait, but a logo usually has some framing. Let me add a subtle ring but make it optional-looking. Actually, let me add a thin ring—it does make it look more like a team logo/emblem, which is what they asked for ("Logo für eine Eishockeymannschaft"). I'll add a thin ring.

Let me place the ring centered at (300, 285), r=248, stroke width 6, color dark green. And text below at y=560. But the ring bottom (y=537) and text at y=560 — close. Let me adjust.

Alternatively, put the text INSIDE the ring at the bottom, following a curve. That requires textPath. Let me do straight text inside the ring near the bottom.

Hmm, let me reconsider the whole layout with a ring:
- Ring: center (300, 290), r=250.
- Inside ring: owl + sticks.
- Bottom inside ring: text "Owayo Eulers" straight, at y=470 maybe.

But the owl is big and would fill most of the ring, leaving little room for text at the bottom inside. Let me make the owl a bit smaller to leave room, or put text below the ring.

Let me put text below the ring. Layout:
- Ring: center (300, 285), r=245. Bottom at y=530.
- Text: at y=565, below ring. But that's very close to ring bottom. Let me lower the ring center or increase spacing.

Let me reconsider. Total viewBox height 640. Let me allocate:
- Ring/emblem: y from 40 to 520 (center 280, r 240).
- Text: y from 545 to 590 (baseline ~585).

Hmm, that's tight. Let me make viewBox taller: 0 to 660. Ring center (300, 280), r=235 (y: 65 to 515). Text baseline at 575.

Actually, let me simplify and NOT use a ring. The clean look with just the elements is fine and matches the request. Let me go with clean.

Decision: No ring. Just crossed sticks, owl, and text. Clean, transparent background.

Hmm, wait. Let me reconsider. Actually a lot of team logos do have the emblem framed. But the user specifically said "Der Hintergrund des Logos soll einfarbig sein, am besten besitzt das Logo gar keinen Hintergrund." (The background should be solid, preferably the logo has no background at all.) This is about the BACKGROUND being transparent/solid, not about framing. So I can add a ring (frame) as long as background is transparent. But to be safe and clean, let me add a subtle ring as framing since it's a "logo."

Let me add a thin ring. Final decision: add a subtle ring.

Let me restructure:
- viewBox 0 0 600 660
- Ring: center (300, 285), r=245, stroke dark green, no fill, stroke-width 7. Maybe a second thinner ring inside for style.
- Owl + sticks inside ring.
- Text below ring at y=575.

Wait, but if the sticks stick out and the ring is at r=245, the stick handles at distance ~232 from center (300,285): let me recompute. Handle at (438,104): distance from (300,285) = sqrt(138² + 181²) = sqrt(19044+32761)=sqrt(51805)=227.6 < 245. Inside. Good. Blade at (184,446): sqrt(116²+161²)=sqrt(13456+25921)=sqrt(39377)=198 <245. Inside. Good.

So everything fits inside the ring. 

But actually, if the sticks' handles and blades are inside the ring, the ring frames them nicely. Good.

Let me reconsider: with the ring, the design looks like a badge/emblem. The text below completes it. 

Let me set:
- Ring: center (300, 285), r=245.
- Text: baseline y=575, centered. But ring bottom is at 285+245=530. Text at 575 is 45px below ring. Good spacing.

Hmm, but 575 baseline means text occupies ~530-575, which is right at the ring bottom (530). Let me put text baseline at 590. Text top ~545. Ring bottom 530. Gap 15px. OK. Let me use baseline 588.

Let me reconsider the owl size to fit inside the ring. The owl head top ~150, body bottom ~394. Within ring (ring spans y=40-530). Good. The owl eyes at y=197, body to 394. Ring center 285. Owl is centered vertically-ish. Good.

Let me also make sure the owl doesn't touch the ring too much. Owl head at (240-360, 150-260), body (226-374, 150-394). Ring at r=245 from (300,285): at the owl's extent, e.g., owl body bottom (300,394): distance from center = 109 <245. Owl wing tips at ~(216, 356): distance = sqrt(84²+71²)=sqrt(7056+5041)=sqrt(12097)=110 <245. So owl is well inside the ring with margin. Good. The sticks fill the outer area. Good.

Alright, let me finalize with the ring.

Actually, let me reconsider whether to add the ring at all, because it adds complexity and the sticks crossing the ring area might look cluttered. Let me look at it holistically: a ring around crossed sticks with an owl in the center is a very classic sports logo. I think it'll look good. Let me add it.

Let me write the final SVG.

Let me also add a subtle inner ring or just one ring. One ring is cleaner. Let me do one ring, stroke-width 6, color #184B3B. Maybe add a thin gold inner accent line. Let me keep one ring.

Hmm, actually, let me reconsider the color of the ring. Dark green #184B3B matches the owl. Good.

Let me also reconsider: should I add a gold accent somewhere to tie in the eyes/sticks? The sticks are gold/wood, eyes gold. A gold ring accent could tie it together. Let me make the ring dark green with a thin gold inner line. Or just keep dark green. Let me do dark green ring + thin gold inner ring for a bit of flair.

Two rings:
- Outer: r=248, stroke #184B3B, width 8.
- Inner: r=237, stroke #E5B80B, width 3.

Hmm, might be too much. Let me just do one green ring, width 6. Clean.

Actually, let me add a bit of gold. Let me do the ring in dark green, and add small gold "stars" or dots, or a gold line. Let me keep it simple: one green ring. I'll add gold accents in the owl (already have gold eyes and beak is orange).

Let me finalize.

Let me write it out carefully:

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 660" width="600" height="660">
  <defs>
    <linearGradient id="bodyGrad" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#459E76"/>
      <stop offset="0.55" stop-color="#2B7054"/>
      <stop offset="1" stop-color="#164738"/>
    </linearGradient>
    <linearGradient id="bellyGrad" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#EFF5E8"/>
      <stop offset="1" stop-color="#CDE0C2"/>
    </linearGradient>
    <linearGradient id="stickGrad" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="#CE9A58"/>
      <stop offset="0.5" stop-color="#AE7636"/>
      <stop offset="1" stop-color="#7C4E1F"/>
    </linearGradient>
    <radialGradient id="irisGrad" cx="0.5" cy="0.35" r="0.65">
      <stop offset="0" stop-color="#FDF0B8"/>
      <stop offset="0.45" stop-color="#F5C518"/>
      <stop offset="1" stop-color="#C28F08"/>
    </radialGradient>
  </defs>

  <!-- Emblem ring -->
  <circle cx="300" cy="285" r="248" fill="none" stroke="#164738" stroke-width="7"/>

  <!-- Hockey Sticks -->
  <g>
    <g transform="rotate(35 300 300)">
      <rect x="294" y="60" width="12" height="340" rx="6" fill="url(#stickGrad)"/>
      <path d="M 287 396 L 313 396 L 314 433 L 333 438 C 342 440, 343 452, 334 456 L 266 456 C 257 452, 258 440, 267 438 L 286 433 Z" fill="url(#stickGrad)"/>
    </g>
    <g transform="rotate(-35 300 300)">
      <rect x="294" y="60" width="12" height="340" rx="6" fill="url(#stickGrad)"/>
      <path d="M 287 396 L 313 396 L 314 433 L 333 438 C 342 440, 343 452, 334 456 L 266 456 C 257 452, 258 440, 267 438 L 286 433 Z" fill="url(#stickGrad)"/>
    </g>
  </g>

  <!-- Owl -->
  <g>
    <path d="M 300 150 C 266 150, 244 172, 240 206 C 234 248, 226 302, 248 344 C 264 376, 283 394, 300 394 C 317 394, 336 376, 352 344 C 374 302, 366 248, 360 206 C 356 172, 334 150, 300 150 Z"
          fill="url(#bodyGrad)" stroke="#12382c" stroke-width="3"/>

    <path d="M 258 170 L 231 118 L 287 159 Z" fill="url(#bodyGrad)" stroke="#12382c" stroke-width="2.5"/>
    <path d="M 342 170 L 369 118 L 313 159 Z" fill="url(#bodyGrad)" stroke="#12382c" stroke-width="2.5"/>

    <ellipse cx="300" cy="333" rx="51" ry="63" fill="url(#bellyGrad)" stroke="#B9CCA8" stroke-width="2"/>

    <g stroke="#AEBF97" stroke-width="3" fill="none" stroke-linecap="round">
      <path d="M 271 303 Q 300 319 329 303"/>
      <path d="M 267 335 Q 300 353 333 335"/>
      <path d="M 272 367 Q 300 384 328 367"/>
    </g>

    <path d="M 246 258 C 220 278, 216 324, 241 357 C 230 316, 240 282, 265 266 Z" fill="#164738"/>
    <path d="M 354 258 C 380 278, 384 324, 359 357 C 370 316, 360 282, 335 266 Z" fill="#164738"/>

    <circle cx="268" cy="197" r="37" fill="#E7F0DE" stroke="#12382c" stroke-width="3"/>
    <circle cx="332" cy="197" r="37" fill="#E7F0DE" stroke="#12382c" stroke-width="3"/>

    <circle cx="268" cy="197" r="25" fill="url(#irisGrad)"/>
    <circle cx="332" cy="197" r="25" fill="url(#irisGrad)"/>

    <circle cx="269" cy="198" r="12" fill="#141414"/>
    <circle cx="331" cy="198" r="12" fill="#141414"/>

    <circle cx="260" cy="188" r="6" fill="#FFFFFF"/>
    <circle cx="324" cy="188" r="6" fill="#FFFFFF"/>
    <circle cx="274" cy="204" r="3" fill="#FFFFFF" opacity="0.7"/>
    <circle cx="336" cy="204" r="3" fill="#FFFFFF" opacity="0.7"/>

    <path d="M 285 228 Q 300 223 315 228 Q 308 251 300 261 Q 292 251 285 228 Z" fill="#F0931E" stroke="#B5660F" stroke-width="2"/>
  </g>

  <!-- Text -->
  <text x="300" y="590" text-anchor="middle" font-family="Arial, Helvetica, sans-serif" font-size="50" font-weight="bold" fill="#164738" letter-spacing="2">Owayo Eulers</text>
</svg>
```

Wait, I have the ring at r=248 centered (300,285). The text at y=590. Ring bottom at 285+248=533. Text at 590 is 57px below ring bottom. Good.

But wait, the stick handles at (438,104) — distance from (300,285): sqrt(138²+181²)=sqrt(19044+32761)=sqrt(51805)=227.6 < 248. Inside ring. Good. But the ring is drawn BEFORE the sticks, so the ring is behind the sticks. That means the ring would be partly covered by the sticks where they cross the ring. Hmm, I want the ring on top (as a frame) or the sticks inside the ring.

If I draw ring first (behind), then sticks, then owl, the ring is behind everything. The sticks would overlap the ring. The parts of the ring not covered by sticks would show. Since the sticks are in the middle and the ring is the outer boundary, most of the ring would show (the sticks don't cover the whole ring). But where sticks cross the ring area, the stick is on top. That might look a bit off (sticks overlapping the frame).

Better: draw ring LAST (on top), so the frame is crisp and on top. But then the ring would cover the top parts of the stick handles where they cross the ring. Let me check: stick handle at (438,104), the shaft goes from there down to the crossing. Near the handle (top-right), the shaft is at the ring's edge. If ring is on top, it'd cover the shaft there, creating a gap. Hmm.

Alternatively, draw the ring first, then sticks, then owl, then text. The ring is behind. The sticks overlap the ring in the middle-ish area. Since the sticks are thin (shaft width 12) and the ring is the outer boundary, the overlap is minimal (only where the shafts cross near the ring). Actually, the shafts cross the ring at the top-right (stick 1) and top-left (stick 2), near the handles. And the blades near the bottom-left/right. So a few spots where sticks touch the ring. If ring is behind, sticks show on top there. If ring is on top, ring shows on top, cutting the sticks.

For a clean emblem, I'd want the sticks to be INSIDE the ring, not crossing it. But my sticks' handles and blades are at distance ~227 and ~198 from center, while ring is at 248. So they're inside, not crossing. Wait, 227 < 248, so handles are inside the ring. 198 < 248, blades inside. So the sticks are entirely inside the ring! They don't cross the ring. 

So the ring is outside all the sticks. If I draw ring first (behind), the ring is behind the sticks but since sticks are inside, the ring shows all around them. The ring is only covered where sticks are, but sticks are inside so they don't cover the ring (ring is outside). Wait, no—if ring is behind and sticks are in front and inside, then the ring is visible in the annular region outside the sticks. The ring is a circle; the sticks are inside it. So the ring shows as a complete circle around the sticks. The sticks don't cover any part of the ring (since sticks are strictly inside). 

Wait, is that right? The ring is at radius 248. The sticks are at radius ≤227. So the sticks are inside the ring circle. The ring is a thin circle at radius 248. The sticks don't reach radius 248, so they don't overlap the ring. Therefore, whether the ring is drawn before or after, there's no overlap between ring and sticks. 

So it doesn't matter much. But to be safe, let me draw the ring first (behind), then sticks, then owl, then text. Actually, since no overlap, order doesn't matter for ring vs sticks. Let me draw ring first.

Hmm wait, but actually I should double-check the stick handles don't exceed radius 248. Handle at (438,104): 227.6. What about the very top of the shaft before rotation? Base shaft top at (300,60), distance from (300,285) = 225. After rotation, handle at (438,104), distance 227.6. So max ~228 < 248. Good, inside.

Blades: base blade at (300, 450), distance from (300,285) = 165. After rotation, blade tips at ~(184,446): distance = sqrt(116²+161²)=198. Still <248. Good.

So everything is inside the ring. 

Now, one concern: the ring at r=248 is quite large. The owl and sticks should fill most of it for a balanced look. The sticks reach radius ~228 (handles). The owl reaches ~198 (wing tips) and body. So there's a gap between the owl/sticks and the ring (from ~228 to 248). That's a 20px gap. Acceptable, gives breathing room.

Actually, let me reconsider—the sticks' handles at radius 228, ring at 248. 20px gap. The text is below the ring. Should be fine.

Let me reconsider if the design is too sparse. The owl is central, sticks frame it, ring frames all, text below. Should look good.

Let me also reconsider: maybe I should make the sticks a bit longer so they reach closer to the ring, filling it better. Let me extend the shaft length. Current shaft from y=60 to y=400 (length 340). Let me extend to y=50 (handle top) and blade to y=460. Then handles reach radius ~237, closer to ring. Let me adjust.

Base shaft: x=294, y=50, height=360 (to y=410). Blade at bottom around y=460.

Let me recompute handle position with rotation center (300,300):
Base handle (300,50): rotate +35°: 
  x' = 300 + 0 - (50-300)sin35 = 300 - (-250)(0.574) = 300+143.5 = 443.5
  y' = 300 + (-250)cos35 = 300 - 214.8 = 85.2
  → (443, 85). Distance from (300,285) = sqrt(143²+200²)=sqrt(20449+40000)=sqrt(60449)=246. Close to ring (248)! 

Hmm, that's very close to the ring. Might touch it. Let me keep shaft a bit shorter so handles are at radius ~230. Let me use base handle at y=60 (as before), giving radius 227.6. Good margin from ring 248.

Actually, 227 vs 248 is a 20px gap, which is fine. Let me keep it. Or I could reduce ring radius to 235 to close the gap. Let me set ring r=240. Then gap is 240-227=13px. Hmm. Let me keep ring r=248 and handles at 227. 20px gap is fine.

Wait, I realize I should double-check the stick blade doesn't go below the ring or outside. Blade tips at radius 198, inside 248. Good.

OK let me also reconsider: the text "Owayo Eulers" — let me make sure it's not too close to the ring. Ring bottom at y=533. Text baseline 590, text top ~545. Gap between ring bottom (533) and text top (545) = 12px. A bit close. Let me move text down to baseline 600. Text top ~555, gap 22px. Better. But then text bottom ~595, within 660. Good. Let me use baseline 600.

Hmm, actually font-size 50, cap height ~36px. Text from baseline-36 to baseline. Baseline 600 → text 564 to 600. Ring bottom 533. Gap 31px. Good.

Let me finalize with baseline 600.

Wait, let me reconsider total height. viewBox 660. Text baseline 600, text bottom at 600. 60px below text. Good. Ring top at 285-248=37. Text... everything fits.

Let me also reconsider the stick handles not going above the ring. Handle at (443,85) or (438,104). Ring top at 37. Handle at y=104, below ring top. Good. And handle x=438 or 443, within ring (ring right edge at 300+248=548). Good.

Alright. Let me also reconsider adding a subtle shadow or making elements pop. Probably not needed. Keep it flat and clean (flat design is nice for logos).

Let me reconsider the belly feather lines. I have 3 arcs. Let me maybe add more or make them look like little scallops. 3 is fine.

Let me reconsider the wings. I have two dark wing shapes on the sides. Let me make sure they look like wings. The path "M 246 258 C 220 278, 216 324, 241 357 C 230 316, 240 282, 265 266 Z" — this creates a shape on the left side. Let me visualize: starts at (246,258), curves out-left to (216,324), back to (241,357), then curves back via (230,316),(240,282) to (265,266), close. So it's a pointed wing shape pointing down-left. OK, looks like a wing. Good.

Let me reconsider the beak. "M 285 228 Q 300 223 315 228 Q 308 251 300 261 Q 292 251 285 228 Z" — a shield/triangle beak pointing down. Good. Orange with darker stroke.

Let me reconsider eye highlights. Two main highlights (upper-left) and two small (lower-right). Gives a lively eye. Good.

I think the design is solid. Let me write the final version.

Oh wait, I should double check the rotation direction makes the blades point outward (down-left and down-right) as I calculated. Let me re-verify Stick 1 (rotate +35°):

Base blade: from (287,396) to (333,456) roughly (the blade shape). Let me take blade center (300, 426) and blade right tip (337, 454), blade left tip (263, 454).

Rotate +35° around (300,300):
Blade center (300,426):
  x' = 300 + 0 - (426-300)sin35 = 300 - 126·0.574 = 300-72.3 = 227.7
  y' = 300 + 126·cos35 = 300 + 102.7 = 402.7
  → (228, 403)
Blade left tip (263,454):
  x' = 300 + (263-300)cos35 - (454-300)sin35 = 300 + (-37)(0.819) - (154)(0.574) = 300 - 30.3 - 88.4 = 181.3
  y' = 300 + (-37)(0.574) + (154)(0.819) = 300 - 21.2 + 126.1 = 404.9
  → (181, 405)
Blade right tip (337,454):
  x' = 300 + 37·0.819 - 154·0.574 = 300 + 30.3 - 88.4 = 241.9
  y' = 300 + 37·0.574 + 154·0.819 = 300 + 21.2 + 126.1 = 447.3
  → (242, 447)

So Stick 1 blade: center (228,403), left tip (181,405), right tip (242,447). So the blade extends from (181,405) down-right to (242,447). The toe (right tip) points down-right, but relative to the stick's outward direction (down-left), hmm. 

Wait, the blade's "toe" is the tip. In the base, the blade is symmetric from x=263 to x=337 (left to right), flat-ish bottom. After rotation, left tip (181,405), right tip (242,447). So the blade goes from (181,405) to (242,447), i.e., down and to the right. The blade is oriented diagonally. The "flat" part of the blade... 

Hmm, this blade is pointing down-right, which for Stick 1 (a "\" stick going top-right to bottom-left) means the blade toe points toward the center/right, not outward. That's the asymmetry I worried about.

Let me reconsider. For Stick 1 going from top-right (handle) to bottom-left, the blade at the bottom-left should point outward = down-left. But my blade points down-right (toward center). 

The issue is the base blade is symmetric, so after rotation it doesn't point outward cleanly.

Hmm. Let me reconsider. Maybe I should make the blade asymmetric, pointing to one side, and choose rotations so both blades point outward.

Alternatively, accept the current look. Let me visualize: Stick 1 blade from (181,405) to (242,447). Stick 2 blade (rotate -35°): by symmetry, from (372,405) to (413,447). Wait let me compute Stick 2.

Stick 2 (rotate -35°):
Blade center (300,426):
  x' = 300 + 0 - (126)sin(-35) = 300 - 126·(-0.574) = 300+72.3 = 372.3
  y' = 300 + 126·cos(-35) = 300+102.7 = 402.7
  → (372, 403)
Blade left tip (263,454):
  x' = 300 + (-37)cos(-35) - (154)sin(-35) = 300 + (-37)(0.819) - (154)(-0.574) = 300 - 30.3 + 88.4 = 358.1
  y' = 300 + (-37)(-0.574) + (154)(0.819) = 300 + 21.2 + 126.1 = 447.3
  → (358, 447)
Blade right tip (337,454):
  x' = 300 + 37·0.819 - 154·(-0.574) = 300 + 30.3 + 88.4 = 418.7
  y' = 300 + 37·(-0.574) + 154·0.819 = 300 - 21.2 + 126.1 = 404.9
  → (419, 405)

So Stick 2 blade: center (372,403), left tip (358,447), right tip (419,405). Blade from (358,447) to (419,405), up and to the right.

So:
- Stick 1 blade: from (181,405) to (242,447). Points down-right.
- Stick 2 blade: from (358,447) to (419,405). Points up-right.

Hmm, these are mirror images. Stick 1 blade points down-right (toward center-bottom), Stick 2 blade points up-right (toward center-right). 

Wait, that doesn't look symmetric/clean. Let me reconsider.

Stick 1: handle top-right (443,85), blade at bottom-left region (181-242, 403-447).
Stick 2: handle top-left (157,85), blade at bottom-right region (358-419, 403-447).

The two blades: Stick 1 blade is at bottom-left (x=181-242), Stick 2 blade is at bottom-right (x=358-419). They're separated. Each blade is a diagonal shape. Stick 1 blade points down-right (its toe at (242,447) is lower-right), Stick 2 blade points up-right (its toe at (419,405)... hmm).

Actually, let me reconsider what "blade points" means. A hockey blade has a heel (connects to shaft) and a toe (the tip). In my base, the heel is at the top (connects to shaft at y=396) and the toe is at the bottom (y=456). The blade bottom is flat-ish from x=263 to x=337.

After rotation, for Stick 1: the heel (top of blade, near shaft) is at ~(228-242, 403-405) [upper part], and the toe (bottom of blade) is at ~(181-242, 405-447) [lower part]. 

Hmm, this is confusing. Let me just think of the blade as a shape and see if it looks like a hockey stick.

Actually, maybe the cleaner approach is to make the blade point clearly to one side (like a real hockey stick blade which curves). Let me make the base blade asymmetric: flat bottom, and the toe curving up on the right side only. Like a real stick.

Real hockey stick blade (side view): the bottom is flat (touches ice), the front (toe) curves up. The heel connects to the shaft.

Let me define base blade with toe pointing right and curving up:
```
M 293 396 (heel top, near shaft)
L 307 396
L 307 430 (down the heel)
L 330 432 (out toward toe)
C 340 432, 343 440, 337 446 (toe curves up)
L 333 446 ... 
```

Hmm, let me think about the blade orientation after rotation.

Actually, let me reconsider. Maybe the issue is that with symmetric blades and rotation ±35°, the blades end up pointing in "weird" directions. Let me instead make the blades point straight down in the base, and use a smaller rotation so they stay pointing down-ish (outward).

Wait, if the blade points straight down in base (toe at bottom), then after rotation by ±35°, the toe points down-and-outward. Let me reconsider.

Base blade pointing straight down: heel at top (connects to shaft), toe at bottom curving. Symmetric around x=300, toe at the bottom.

After Stick 1 rotate +35°: the whole stick rotates clockwise. The toe (was pointing down, 6 o'clock) now points to 6+35=... clockwise means 6 o'clock → 7 o'clock direction? In visual terms (y down), rotating clockwise by 35° moves the down-pointing toe toward the lower-left? Let me think. Down is (0,1). Rotate clockwise by 35° (in screen coords, clockwise = negative angle in math, but let me just think visually). 

Clockwise rotation (visual): a vector pointing down (6 o'clock) rotated clockwise (toward 7, 8 o'clock) points down-left. So Stick 1 toe points down-left. Outward for Stick 1 (which is on the... hmm, Stick 1 handle is top-right, so Stick 1 is the "\" stick, its bottom is on the left, outward is down-left). So toe down-left = outward. 

Stick 2 rotate -35° (counterclockwise): down-pointing toe rotates counterclockwise (toward 5, 4 o'clock) = down-right. Stick 2 is the "/" stick, bottom on the right, outward is down-right. Toe down-right = outward. 

So if the base blade points straight DOWN (symmetric, toe at bottom), then after rotation ±35°, both toes point outward-down. That's what I want!

But in my current base, the blade is a flat-bottom shape from x=263 to x=337, which does point down (toe at bottom y=456). So why did my calculation show the toe pointing down-right for Stick 1?

Let me recompute Stick 1 blade toe. The blade bottom edge is from (263,454) to (337,454) [the flat bottom]. Wait, in my path, the bottom is "L 266 456 C 257 452, 258 440, 267 438" on the left and "L 333 438 C 342 440, 343 452, 334 456" on the right, with "L 266 456" and the top "L 333 438". Let me re-read my blade path:

```
M 287 396 
L 313 396 
L 314 433 
L 333 438 
C 342 440, 343 452, 334 456 
L 266 456 
C 257 452, 258 440, 267 438 
L 286 433 
Z
```

So the path: 
- Start (287,396)
- to (313,396) [top edge, width 26]
- to (314,433) [down right side]
- to (333,438) [out to right]
- curve to (334,456) [toe, curving down and the right tip]
- to (266,456) [bottom edge, from right tip to left tip, y=456]
- curve to (267,438) [left tip up]
- to (286,433)
- close to (287,396)

So the blade is symmetric-ish: bottom edge flat from (266,456) to (334,456), centered at x=300. The toe tips are at (266,456) and (334,456) (both at y=456, the bottom). The top connects to shaft at (287-313, 396-433).

So the blade is symmetric, flat bottom from x=266 to x=334, centered at 300. Toe tips at both ends (266,456) and (334,456).

Now rotate +35° around (300,300):
Left toe tip (266,456):
  x' = 300 + (266-300)cos35 - (456-300)sin35 = 300 + (-34)(0.819) - (156)(0.574) = 300 - 27.8 - 89.5 = 182.7
  y' = 300 + (-34)(0.574) + (156)(0.819) = 300 - 19.5 + 127.8 = 408.3
  → (183, 408)
Right toe tip (334,456):
  x' = 300 + 34·0.819 - 156·0.574 = 300 + 27.8 - 89.5 = 238.3
  y' = 300 + 34·0.574 + 156·0.819 = 300 + 19.5 + 127.8 = 447.3
  → (238, 447)

So Stick 1 blade: left toe tip (183,408), right toe tip (238,447). The flat bottom edge (from (183,408) to (238,447)) now runs from upper-left to lower-right. The blade's flat face... the bottom edge points down-left (from (238,447) to (183,408), direction is up-left, so the flat face points down-right). Hmm.

Wait, the flat bottom edge vector: from (183,408) to (238,447) is (55, 39), pointing down-right. The flat face of the blade is perpendicular to the shaft. The shaft direction (for Stick 1) is along (handle to blade): handle (443,85) to blade center (~230,403), direction (−213, 318), i.e., down-left. The blade is perpendicular to this, so blade flat face points down-right (perpendicular to down-left). 

So the blade flat face points down-right, meaning the toe (the rounded/curved tip) ... hmm, in a real hockey stick, the flat bottom touches the ice and the toe curves up. Here, the "flat bottom" now points down-right (as the face), and the tips...

I think I'm overcomplicating. Let me just accept that the blades look like hockey stick blades (flat bottom, attached to shaft) and they're at the bottom-left and bottom-right. The exact toe direction is a minor detail. For a stylized logo, this is fine.

But let me reconsider whether it looks clean. The two blades:
- Stick 1: flat edge from (183,408) to (238,447), at bottom-left.
- Stick 2: by symmetry, flat edge from (372,408)... let me compute. Actually Stick 2 is mirror, so flat edge from (358,447) to (417,408), at bottom-right.

So Stick 1 blade is at bottom-left (x=183-238), Stick 2 blade at bottom-right (x=358-417). They're separated by ~120px in the middle. Both flat edges are diagonal. Stick 1 flat edge goes from upper-left (183,408) to lower-right (238,447). Stick 2 flat edge from upper-right... 

Hmm, let me reconsider. This might look like the blades are "facing" each other or away. Let me just go with it and trust it looks OK. Actually, let me reconsider making the blades point more clearly.

Alternative: Let me make the base blade point to ONE side (asymmetric, like a real stick with toe on one side), and arrange so both toes point outward.

Real hockey stick: shaft at top, blade at bottom with toe curving up on the FRONT side. If I want both sticks' toes to point outward (away from center):
- Stick 1 (bottom-left): toe should point down-left. So the blade's toe (curved up part) is on the left.
- Stick 2 (bottom-right): toe should point down-right. Blade toe on the right.

So Stick 1 blade has toe on left, Stick 2 blade has toe on right. They're mirror images. 

Let me define base blade with toe on the RIGHT (curved up on right):
```
M 293 396 (heel top-left)
L 307 396 (heel top-right)
L 308 430 (down right heel)
L 330 432 (out to toe)
C 340 432, 342 442, 335 448 (toe curving up, right side)
L 332 448 ... 
```

Hmm, this is getting complicated. Let me define it more carefully.

Base blade (toe on right, curving up):
- Heel connects to shaft at top (x=293-307, y=396).
- Right side goes down to the toe.
- Toe curves up at the right.
- Bottom is flat from toe back to heel.
- Left side goes up.

```
M 294 396
L 306 396
L 306 432
L 328 434
C 338 435, 341 444, 335 450
C 330 454, 322 452, 321 446
L 320 444
L 300 444
L 298 432
Z
```

Hmm, this is messy. Let me simplify.

Actually, let me reconsider. For the crossed sticks, maybe I'm overcomplicating the blade. Let me make the blade a simple shape: a flat bottom with the toe slightly raised on one end, attached to the shaft. And I'll make Stick 2 the mirror of Stick 1.

Let me define base blade (asymmetric, toe raised on right):
```
M 294 396
L 306 396
L 307 430
L 326 432
C 336 433, 338 445, 330 450
C 324 453, 318 450, 318 445
L 317 443
L 300 443
L 298 430
Z
```

Ugh, too complex. Let me step back.

Simplest clean blade: a "P" or "J" shape, or just a flat blade. Let me make the blade a simple shape:
- A rectangle-ish bottom with a slight toe curve.

Let me define:
```
Blade:
M 294 396
L 306 396
L 306 432
L 330 434
L 330 450
C 330 458, 318 460, 306 458
L 298 456
L 296 432
Z
```

This makes a blade: flat top (connects shaft), right side down, toe at bottom-right curving, bottom flat-ish, left side up. Hmm.

I think I'm way overthinking the blade. Let me just use a symmetric flat-bottom blade (like I have) and accept the look. It will read as hockey sticks. The key elements (long shaft + blade at bottom) are there.

Actually, let me reconsider using a totally different, simpler representation for the sticks that's cleaner. 

What if the sticks are drawn more simply: just a shaft (line) and a simple blade (a short curved line or shape) at the end? Like a "hockey stick" icon.

Let me define a hockey stick as:
- Shaft: line from top to bottom.
- Blade: a hook at the bottom.

And cross two of them.

Let me use a simpler blade: at the bottom of the shaft, a short horizontal line with a curve up at the toe. 

Let me define base stick:
- Shaft: from (300, 60) to (300, 430) — but I'll draw as a rect.
- Blade: from (300, 430) extend to the right and curve: a path.

Blade (toe on right):
```
M 300 430 
L 300 448 
C 300 456, 312 458, 320 454 
L 322 452
```
Plus the blade thickness. Let me make the blade a filled shape:
```
M 295 428
L 305 428
L 305 448
L 324 450
C 332 450, 334 442, 328 440
L 300 440
L 295 436
Z
```

Hmm. Let me just go with my original symmetric blade. It's fine. Let me not obsess.

Actually, let me reconsider the whole thing. Let me look at my original blade and just verify it looks reasonable as a hockey stick when rotated. 

Original base blade: flat bottom from (266,456) to (334,456), attached to shaft at (287-313, 396). This is a symmetric blade, flat bottom, like a "table" on the shaft. When rotated, it becomes a blade on the shaft. It'll look like a hockey stick blade (the flat bottom = the part touching ice, the top = connects to shaft). The slight curve at the tips (257-267 and 334-343) gives a bit of toe shape. 

I think it's fine. Let me go with it.

Let me reconsider: with symmetric blades and rotation ±35°, do the two blades look like they're in a nice crossed position? 

Stick 1 blade: flat edge from (183,408) to (238,447), at bottom-left.
Stick 2 blade: flat edge from (372,408) to (358,447)... let me recompute Stick 2.

Stick 2 (rotate -35°):
Left toe tip (266,456):
  x' = 300 + (-34)cos(-35) - (156)sin(-35) = 300 + (-34)(0.819) - (156)(-0.574) = 300 - 27.8 + 89.5 = 361.7
  y' = 300 + (-34)(-0.574) + (156)(0.819) = 300 + 19.5 + 127.8 = 447.3
  → (362, 447)
Right toe tip (334,456):
  x' = 300 + 34·0.819 - 156·(-0.574) = 300 + 27.8 + 89.5 = 417.3
  y' = 300 + 34·(-0.574) + 156·0.819 = 300 - 19.5 + 127.8 = 447.3
  → (417, 447)

So Stick 2 blade: left toe tip (362,447), right toe tip (417,447). Flat edge from (362,447) to (417,447) — this is HORIZONTAL at y=447! Interesting. Because for Stick 2, the flat bottom edge was horizontal (both at y=456), and after -35° rotation... wait, why is it horizontal now?

Oh I see, because the rotation is around (300,300) and the flat edge was at y=456 (below center). Rotating by ±35° tilts it. For Stick 1 (+35°), the left end (266,456) goes up less... let me see, (266,456)→(183,408) and (334,456)→(238,447). So the edge tilts: left end higher (408), right end lower (447). For Stick 2 (-35°): (266,456)→(362,447) and (334,456)→(417,447). Both at y=447? That's odd.

Wait, let me recompute Stick 2 right toe tip (334,456):
  x' = 300 + (334-300)cos(-35) - (456-300)sin(-35)
     = 300 + 34·0.819 - 156·(-0.574)
     = 300 + 27.8 + 89.5 = 417.3
  y' = 300 + (334-300)sin(-35) + (456-300)cos(-35)
     = 300 + 34·(-0.574) + 156·0.819
     = 300 - 19.5 + 127.8 = 447.3

And left toe tip (266,456):
  x' = 300 + (266-300)cos(-35) - (456-300)sin(-35)
     = 300 + (-34)(0.819) - 156·(-0.574)
     = 300 - 27.8 + 89.5 = 361.7
  y' = 300 + (266-300)sin(-35) + (456-300)cos(-35)
     = 300 + (-34)(-0.574) + 156·0.819
     = 300 + 19.5 + 127.8 = 447.3

So both at y=447. The flat edge stays horizontal for Stick 2?! 

Oh, I see. The flat bottom edge is at y=456, which is 156px below center (300). When rotated, points at the same distance from center trace a circle. The flat edge endpoints are at (266,456) and (334,456), both at distance sqrt(34²+156²) from center... no wait, they're at different positions. (266,456): dx=-34, dy=156. (334,456): dx=+34, dy=156. Both at distance sqrt(34²+156²)=159.6 from center. 

When I rotate by -35° (Stick 2), both points rotate by the same angle around center. Since they were symmetric about the vertical axis (dx=±34, same dy), after rotation they become... 

For a point (dx,dy) rotated by θ: (dx cosθ - dy sinθ, dx sinθ + dy cosθ).
(266,456) → dx=-34, dy=156, θ=-35: 
  dx' = -34·cos(-35) - 156·sin(-35) = -34·0.819 - 156·(-0.574) = -27.8 + 89.5 = 61.7
  dy' = -34·sin(-35) + 156·cos(-35) = -34·(-0.574) + 156·0.819 = 19.5 + 127.8 = 147.3
  → (300+61.7, 300+147.3) = (361.7, 447.3)
(334,456) → dx=34, dy=156, θ=-35:
  dx' = 34·0.819 - 156·(-0.574) = 27.8 + 89.5 = 117.3
  dy' = 34·(-0.574) + 156·0.819 = -19.5 + 127.8 = 147.3
  → (417.3, 447.3)

So both have dy'=147.3, meaning both at y=447.3. The edge is horizontal. 

Why? Because the original edge was horizontal (both points at dy=156), and... no, rotating a horizontal line by a non-zero angle should make it tilted. Unless... oh! The two points are symmetric about the vertical axis. When rotated, they map to two points that are symmetric about the rotated vertical axis. Since the edge was horizontal and centered below, after rotation... 

Hmm, actually the reason both end up at the same y is a coincidence of the symmetry. Let me reconsider. Original points: A=(-34,156), B=(34,156) relative to center. These are symmetric about the dy-axis (vertical). After rotation by θ, they become A' and B', symmetric about the rotated vertical axis (the image of the vertical axis). The rotated vertical axis is at angle θ from vertical. So A' and B' are symmetric about this tilted axis. That doesn't mean they have the same y-coordinate.

But my calculation shows they do (both dy'=147.3). Let me double check.
A=(-34,156), θ=-35°:
A'_x = -34·cos(-35) - 156·sin(-35) = -34·(0.8192) - 156·(-0.5736) = -27.85 + 89.48 = 61.63
A'_y = -34·sin(-35) + 156·cos(-35) = -34·(-0.5736) + 156·(0.8192) = 19.50 + 127.79 = 147.29
B=(34,156):
B'_x = 34·0.8192 - 156·(-0.5736) = 27.85 + 89.48 = 117.33
B'_y = 34·(-0.5736) + 156·0.8192 = -19.50 + 127.79 = 147.29

Yes, both y'=147.29. So the edge is horizontal. Interesting.

This is because A and B are symmetric about the vertical, and rotating... Actually, the midpoint of A,B is (0,156), on the vertical axis. After rotation, midpoint goes to (0·cosθ - 156 sinθ, 0·sinθ + 156 cosθ) = (-156 sinθ, 156 cosθ) = (89.48, 127.79) for θ=-35. So midpoint → (389.48, 427.79). And A', B' are symmetric about the line through center and this midpoint (the rotated vertical axis). A'=(361.63,447.29), B'=(417.33,447.29). Midpoint of A',B' = (389.48, 447.29). 

Hmm, but I calculated the original midpoint (0,156) rotates to (89.48, 127.79), i.e., (389.48, 427.79). But the actual midpoint of A',B' is (389.48, 447.29). These don't match! Contradiction.

Let me recompute. Oh, I think I made an error. Let me recompute the midpoint rotation.
Midpoint M = (0, 156) relative to center.
Rotate by θ=-35°:
M'_x = 0·cos(-35) - 156·sin(-35) = 0 - 156·(-0.5736) = 89.48
M'_y = 0·sin(-35) + 156·cos(-35) = 0 + 156·0.8192 = 127.79
So M' = (89.48, 127.79), absolute (389.48, 427.79).

But midpoint of A' and B' = ((361.63+417.33)/2, (447.29+447.29)/2) = (389.48, 447.29).

These differ in y (427.79 vs 447.29). So I made an arithmetic error somewhere. Let me recompute A'_y and B'_y.

A'_y = dx·sinθ + dy·cosθ where (dx,dy)=(-34,156), θ=-35.
= -34·sin(-35) + 156·cos(-35)
= -34·(-0.5736) + 156·(0.8192)
= 19.50 + 127.79 = 147.29. 

M'_y should be (A'_y + B'_y)/2 = 147.29. But I computed M'_y = 127.79. 

The issue: M'_y = dx_M·sinθ + dy_M·cosθ = 0·sinθ + 156·cosθ = 156·0.8192 = 127.79.
(A'_y+B'_y)/2 = [(-34 sinθ + 156 cosθ) + (34 sinθ + 156 cosθ)]/2 = [2·156 cosθ]/2 = 156 cosθ = 127.79.

Wait, that gives 127.79, not 147.29. Let me recompute A'_y.
A'_y = dx·sinθ + dy·cosθ = (-34)·sin(-35°) + 156·cos(-35°).
sin(-35°) = -0.5736. cos(-35°) = 0.8192.
= (-34)·(-0.5736) + 156·(0.8192)
= 19.50 + 127.79 = 147.29.

And M'_y = 0·(-0.5736) + 156·0.8192 = 127.79.

(A'_y + B'_y)/2: B'_y = (34)·sin(-35) + 156·cos(-35) = 34·(-0.5736) + 156·0.8192 = -19.50 + 127.79 = 108.29.

Oh! I made an error for B'_y earlier. Let me redo.
B'_y = dx·sinθ + dy·cosθ = 34·sin(-35°) + 156·cos(-35°) = 34·(-0.5736) + 156·(0.8192) = -19.50 + 127.79 = 108.29.

So B'_y = 108.29, not 147.29! I made an arithmetic error before (I wrote +19.50 for B but it should be -19.50). Let me recheck: B'_y = 34·sin(-35). sin(-35) is negative, so 34·(negative) = negative = -19.50. Yes. So B'_y = -19.50 + 127.79 = 108.29.

So Stick 2 blade: A'=(361.63, 447.29), B'=(417.33, 408.29). 

So the flat edge goes from (361.63, 447.29) [left toe] to (417.33, 408.29) [right toe]. This tilts from lower-left to upper-right. 

And Stick 1 blade: A=(266,456)→A', B=(334,456)→B', θ=+35°.
A'_y = -34·sin(35) + 156·cos(35) = -34·0.5736 + 156·0.8192 = -19.50 + 127.79 = 108.29.
A'_x = -34·cos(35) - 156·sin(35) = -34·0.8192 - 156·0.5736 = -27.85 - 89.48 = -117.33 → x=182.67.
B'_y = 34·sin(35) + 156·cos(35) = 19.50 + 127.79 = 147.29.
B'_x = 34·cos(35) - 156·sin(35) = 27.85 - 89.48 = -61.63 → x=238.37.

So Stick 1 blade: A'=(182.67, 108.29)?? Wait, that's y=108, which is near the top! That can't be right.

Oh no, I think I messed up. Let me recompute. A=(266,456), relative to center (300,300): dx=266-300=-34, dy=456-300=156. OK.
Rotate +35°:
A'_x = dx·cos35 - dy·sin35 = -34·0.8192 - 156·0.5736 = -27.85 - 89.48 = -117.33. Absolute x = 300-117.33 = 182.67.
A'_y = dx·sin35 + dy·cos35 = -34·0.5736 + 156·0.8192 = -19.50 + 127.79 = 108.29. Absolute y = 300+108.29 = 408.29.

So A'=(182.67, 408.29). OK I forgot to add 300 to y. A'_y absolute = 300+108.29 = 408.29. Good, that's bottom-left. 

B=(334,456), dx=34, dy=156.
B'_x = 34·0.8192 - 156·0.5736 = 27.85 - 89.48 = -61.63. Absolute x = 238.37.
B'_y = 34·0.5736 + 156·0.8192 = 19.50 + 127.79 = 147.29. Absolute y = 447.29.
So B'=(238.37, 447.29). Bottom-left. Good.

So Stick 1 blade: from A'=(182.67, 408.29) to B'=(238.37, 447.29). Tilts from upper-left to lower-right. 

And Stick 2 blade: A=(266,456)→ with θ=-35:
A'_x = -34·cos(-35) - 156·sin(-35) = -34·0.8192 - 156·(-0.5736) = -27.85 + 89.48 = 61.63. Absolute x=361.63.
A'_y = -34·sin(-35) + 156·cos(-35) = -34·(-0.5736) + 156·0.8192 = 19.50 + 127.79 = 147.29. Absolute y=447.29.
A'=(361.63, 447.29).
B=(334,456), dx=34, dy=156, θ=-35:
B'_x = 34·cos(-35) - 156·sin(-35) = 27.85 + 89.48 = 117.33. Absolute x=417.33.
B'_y = 34·sin(-35) + 156·cos(-35) = 34·(-0.5736) + 156·0.8192 = -19.50 + 127.79 = 108.29. Absolute y=408.29.
B'=(417.33, 408.29).

So Stick 2 blade: from A'=(361.63, 447.29) to B'=(417.33, 408.29). Tilts from lower-left to upper-right.

So:
- Stick 1 blade: (182,408) to (238,447). Bottom-left, tilting down-right.
- Stick 2 blade: (362,447) to (417,408). Bottom-right, tilting up-right.

These are mirror images (across x=300). Stick 1 tilts like "/" (down-right), Stick 2 tilts like "\" ... no. Stick 1 from (182,408) to (238,447): as x increases, y increases (down). So it goes down-right, like "/". Stick 2 from (362,447) to (417,408): as x increases, y decreases (up). So up-right, like "\". 

Hmm, so the two blades tilt in opposite directions, forming a shape like "/" and "\" at the bottom. Together they might look like a "^" or "v" or an X at the bottom. 

Actually, the flat bottoms: Stick 1 flat bottom faces... the blade shape has the flat bottom edge (A'B') and the toe curve. For Stick 1, the flat edge from (182,408) to (238,447). The blade body extends "up" from this edge toward the shaft. So the flat face points down-left (perpendicular to the edge, away from shaft). 

This is getting too detailed. Let me just accept it. The blades will be at the bottom-left and bottom-right, tilted. It should look like crossed hockey sticks with blades at the bottom. Good enough.

Actually, you know what, let me reconsider whether the blades look right by thinking about the overall silhouette. Two sticks crossed in an X. Each stick: long shaft + a blade near the end. The blades are at the bottom, pointing outward and down. This is the classic hockey logo. Even if the exact blade orientation is slightly off, the overall read is "crossed hockey sticks." I'm confident it'll look fine.

Let me finalize the SVG. Let me clean it up.

Actually, let me reconsider the blade shape once more to make it look more like a hockey stick blade (with a clear toe). Let me make the blade more distinct:

Base blade:
```
M 294 396
L 306 396
L 307 432
L 328 434
C 337 435, 340 445, 333 451
C 328 455, 320 453, 319 447
L 318 445
L 300 445
L 297 432
Z
```

Hmm, this makes a blade with the toe curving up on the right side (toe at ~333,451 curving to 319,447). And the left side is the heel going up to the shaft. This is an asymmetric blade (toe on right, heel on left).

But then for symmetry, Stick 2 should be the mirror (toe on left). If I use the same base for both and just rotate, both would have toe on right, which isn't symmetric. 

For a clean crossed look with toes pointing outward:
- Stick 1 (bottom-left, outward = down-left): toe should be on the... hmm.

This is the crux. Let me think clearly.

For Stick 1, after +35° rotation, the shaft goes from top-right to bottom-left. The blade is at the bottom-left end. For the toe to point outward (down-left, away from center), the toe should be on the lower-left side of the blade.

In the base (shaft up, blade down), if the toe is on the RIGHT side of the blade, then after +35° clockwise rotation, the right side goes to... clockwise rotation moves right to bottom. So toe (right) → bottom. Hmm, not down-left.

If toe is on the LEFT in base, after +35° clockwise, left goes to top. So toe → top. Not down-left either.

Ugh. The rotation makes the toe point in a direction determined by its base position. Let me just compute for different base toe positions.

Base blade, toe at bottom (pointing down, symmetric): after +35°, toe points down-left (as computed, the bottom edge rotates). Actually I computed the flat bottom edge endpoints go to (182,408) and (238,447), so the "bottom" (was at y=456) now spans these, and the center of the bottom edge was (300,456)→ rotate +35: 
  dx=0, dy=156. 
  x' = 0 - 156·sin35 = -89.48 → 210.52
  y' = 0 + 156·cos35 = 127.79 → 427.79
  Center of bottom → (210.5, 427.8). 

So the bottom-center of the blade is at (210,428), which is down-left of the shaft bottom. The toe (the rounded tip) — in a symmetric blade, both ends are "toes". The bottom-center points down-left (away from center). Good enough—the blade points outward-down-left.

For Stick 2 (rotate -35°), bottom-center (300,456)→:
  x' = 0 - 156·sin(-35) = 89.48 → 389.5
  y' = 156·cos(-35) = 127.79 → 427.8
  → (389.5, 427.8). Down-right of shaft bottom. Blade points outward-down-right. Good.

So with symmetric blades, both blades point outward-down. The exact toe tips are at the ends. This is fine.

OK so my original symmetric blade is actually correct for pointing outward. My earlier confusion was about the toe tips specifically, but the blade as a whole points outward-down. 

So let me keep the symmetric blade. It's fine.

Let me reconsider the blade shape to make it look good. My original:
```
M 287 396 L 313 396 L 314 433 L 333 438 C 342 440, 343 452, 334 456 L 266 456 C 257 452, 258 440, 267 438 L 286 433 Z
```
This has a flat bottom from (266,456) to (334,456), with the ends curving up a bit (257-267 and 334-343). And connects to shaft at (287-313,396) via (314,433) and (286,433). So the blade is like a shallow tray. Good.

Actually, let me simplify the blade to make it cleaner. Let me make it a bit more blade-like:

```
M 293 396
L 307 396
L 308 430
L 326 432
C 335 433, 337 445, 329 451
C 324 455, 316 453, 316 447
L 315 445
L 300 445
L 296 445
L 295 430
Z
```

Hmm, this is asymmetric (toe on right). Let me not do asymmetric.

Let me just use a clean symmetric blade:
```
M 293 396
L 307 396
L 308 432
L 328 434
C 336 435, 337 448, 328 452
L 272 452
C 263 448, 264 435, 272 434
L 292 432
Z
```
This is symmetric: flat-ish bottom from (272,452) to (328,452), curving up at both ends, connecting to shaft at (293-307,396). Good.

Let me use this.

Actually, let me simplify even more. Let me make the blade a simple trapezoid with slightly rounded bottom corners:
```
M 294 396
L 306 396
L 307 430
L 326 432
L 326 448
L 274 448
L 274 432
L 293 430
Z
```
A flat-bottom tray. But the flat bottom at both ends (274,448) and (326,448) — these are the toe tips. For a hockey blade, the tips should curve up slightly. But a flat bottom is fine and clean.

Hmm, but a completely flat bottom might look like a table leg. Let me add a slight upward curve at the tips:
```
M 294 396
L 306 396
L 307 430
L 326 432
C 332 432, 333 442, 327 447
L 273 447
C 267 442, 268 432, 274 432
L 293 430
Z
```
This curves up at both tips. Looks like a hockey blade. Good.

Let me use this.

OK, let me finalize the whole SVG now. Let me also reconsider the stick shaft—maybe make it a bit thicker or add a slight gradient. Current rect x=294 w=12 is fine.

Let me also reconsider: should the sticks have a darker outline? The gradient gives some dimensionality. Let me add a subtle stroke to the sticks for definition. Actually, the gradient from light (left) to dark (right) gives a cylindrical look. Good enough.

Let me write the final SVG.

Also, I realize I should double-check the owl body path is smooth and owl-like. Let me re-examine:
```
M 300 150 
C 266 150, 244 172, 240 206 
C 234 248, 226 302, 248 344 
C 264 376, 283 394, 300 394 
C 317 394, 336 376, 352 344 
C 374 302, 366 248, 360 206 
C 356 172, 334 150, 300 150 Z
```
This starts at top center (300,150), curves to the left head (240,206), down the left side (226,302), to bottom belly (300,394), up the right side (360,206), back to top. 

Wait, the left side goes from (240,206) to (226,302) — that's the wing area, bulging out to x=226. Then to (248,344) (belly), then (300,394) bottom. This creates a body that's widest around y=300 (x=226 to 374). That's a good owl body shape (rounded, widest at the belly). Good.

The top goes from (300,150) curving out to (240,206) — the head. Good.

With ear tufts at (258,170)-(231,118)-(287,159) and mirror, the head has pointed ears. Good.

Let me finalize.

Let me reconsider the text font. Arial bold, size 50, might be a bit large. "Owayo Eulers" — let me count: O-w-a-y-o (5) space E-u-l-e-r-s (6) = 11 chars + space. At size 50, width ~ 11·28 + 30 = 338px. Centered, x from 131 to 469. Fits. Good. Let me keep size 50. Maybe reduce to 48 for safety. Let me use 48.

Hmm, let me reconsider. Actually 50 should be fine. Let me use 48 to be safe and add letter-spacing.

Let me also reconsider: the text color is dark green #164738. Good, matches owl. Maybe I should add a subtle outline or shadow to the text to make it pop. Let me keep it simple—just fill. Or add a thin outline. Let me add a very subtle effect: keep it simple.

Let me write the final SVG.

Actually, let me reconsider adding a small design element to make it more "logo-like": maybe two small stars or a line under the text, or the text inside a banner. Let me keep it clean: just the text. Clean and modern.

Let me also reconsider the ring. I'll keep the ring (dark green, width

### Antwort

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 660" width="600" height="660">
  <defs>
    <linearGradient id="bodyGrad" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#459E76"/>
      <stop offset="0.55" stop-color="#2B7054"/>
      <stop offset="1" stop-color="#164738"/>
    </linearGradient>
    <linearGradient id="bellyGrad" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#EFF5E8"/>
      <stop offset="1" stop-color="#CDE0C2"/>
    </linearGradient>
    <linearGradient id="stickGrad" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="#CE9A58"/>
      <stop offset="0.5" stop-color="#AE7636"/>
      <stop offset="1" stop-color="#7C4E1F"/>
    </linearGradient>
    <radialGradient id="irisGrad" cx="0.5" cy="0.35" r="0.65">
      <stop offset="0" stop-color="#FDF0B8"/>
      <stop offset="0.45" stop-color="#F5C518"/>
      <stop offset="1" stop-color="#C28F08"/>
    </radialGradient>
  </defs>

  <!-- Emblem ring -->
  <circle cx="300" cy="285" r="248" fill="none" stroke="#164738" stroke-width="7"/>

  <!-- Hockey Sticks (behind owl) -->
  <g>
    <g transform="rotate(35 300 300)">
      <rect x="294" y="60" width="12" height="340" rx="6" fill="url(#stickGrad)"/>
      <path d="M 293 396 L 307 396 L 308 432 L 328 434 C 336 435, 337 448, 328 452 L 272 452 C 263 448, 264 435, 272 434 L 292 432 Z" fill="url(#stickGrad)"/>
    </g>
    <g transform="rotate(-35 300 300)">
      <rect x="294" y="60" width="12" height="340" rx="6" fill="url(#stickGrad)"/>
      <path d="M 293 396 L 307 396 L 308 432 L 328 434 C 336 435, 337 448, 328 452 L 272 452 C 263 448, 264 435, 272 434 L 292 432 Z" fill="url(#stickGrad)"/>
    </g>
  </g>

  <!-- Owl -->
  <g>
    <path d="M 300 150 C 266 150, 244 172, 240 206 C 234 248, 226 302, 248 344 C 264 376, 283 394, 300 394 C 317 394, 336 376, 352 344 C 374 302, 366 248, 360 206 C 356 172, 334 150, 300 150 Z"
          fill="url(#bodyGrad)" stroke="#12382c" stroke-width="3"/>

    <path d="M 258 170 L 231 118 L 287 159 Z" fill="url(#bodyGrad)" stroke="#12382c" stroke-width="2.5"/>
    <path d="M 342 170 L 369 118 L 313 159 Z" fill="url(#bodyGrad)" stroke="#12382c" stroke-width="2.5"/>

    <ellipse cx="300" cy="333" rx="51" ry="63" fill="url(#bellyGrad)" stroke="#B9CCA8" stroke-width="2"/>

    <g stroke="#AEBF97" stroke-width="3" fill="none" stroke-linecap="round">
      <path d="M 271 303 Q 300 319 329 303"/>
      <path d="M 267 335 Q 300 353 333 335"/>
      <path d="M 272 367 Q 300 384 328 367"/>
    </g>

    <path d="M 246 258 C 220 278, 216 324, 241 357 C 230 316, 240 282, 265 266 Z" fill="#164738"/>
    <path d="M 354 258 C 380 278, 384 324, 359 357 C 370 316, 360 282, 335 266 Z" fill="#164738"/>

    <circle cx="268" cy="197" r="37" fill="#E7F0DE" stroke="#12382c" stroke-width="3"/>
    <circle cx="332" cy="197" r="37" fill="#E7F0DE" stroke="#12382c" stroke-width="3"/>

    <circle cx="268" cy="197" r="25" fill="url(#irisGrad)"/>
    <circle cx="332" cy="197" r="25" fill="url(#irisGrad)"/>

    <circle cx="269" cy="198" r="12" fill="#141414"/>
    <circle cx="331" cy="198" r="12" fill="#141414"/>

    <circle cx="260" cy="188" r="6" fill="#FFFFFF"/>
    <circle cx="324" cy="188" r="6" fill="#FFFFFF"/>
    <circle cx="274" cy="204" r="3" fill="#FFFFFF" opacity="0.7"/>
    <circle cx="336" cy="204" r="3" fill="#FFFFFF" opacity="0.7"/>

    <path d="M 285 228 Q 300 223 315 228 Q 308 251 300 261 Q 292 251 285 228 Z" fill="#F0931E" stroke="#B5660F" stroke-width="2"/>
  </g>

  <!-- Text -->
  <text x="300" y="600" text-anchor="middle" font-family="Arial, Helvetica, sans-serif" font-size="48" font-weight="bold" fill="#164738" letter-spacing="2">Owayo Eulers</text>
</svg>
```
