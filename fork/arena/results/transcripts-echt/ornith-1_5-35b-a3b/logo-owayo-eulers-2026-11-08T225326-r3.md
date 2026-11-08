# ornith-1_5-35b-a3b - logo-owayo-eulers (2026-11-08T22:53:26)

## Antwort (45620 Tokens, 250.61 s, Ende: stop, Denken abgebrochen)

### Denkphase

The user wants a logo for an ice hockey team called "Owayo Eulers". The logo should contain an owl and ice hockey sticks. The background should be solid color, or preferably no background at all.

I need to respond with exactly one complete SVG document in a code block. No external resources, no scripts.

Let me create an SVG logo with an owl and ice hockey sticks. I'll design it in a clean, vector style.

Let me think about the design:
- An owl (representing "Eulers" - Eulen means owls in German)
- Ice hockey sticks
- Team name "Owayo Eulers"
- No background or solid background

Let me create a nice SVG. I'll use a circular badge design which is common for sports teams.

Let me design:
1. A circular badge outline
2. An owl in the center
3. Two crossed hockey sticks behind the owl
4. The text "Owayo Eulers"

Let me write the SVG code.

For the owl:
- Body (oval/rounded shape)
- Head
- Eyes (big round eyes typical of owls)
- Beak
- Ears/tufts
- Wings
- Belly with feather pattern

For hockey sticks:
- Two sticks crossed in an X shape behind the owl

Let me create this carefully with good coordinates.

I'll use a viewBox of 0 0 400 400.

Let me build the SVG:

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 400" width="400" height="400">
  <!-- Outer circle -->
  <circle cx="200" cy="200" r="180" fill="none" stroke="#1a3a5c" stroke-width="8"/>
  
  <!-- Hockey sticks -->
  ...
  
  <!-- Owl -->
  ...
  
  <!-- Text -->
  ...
</svg>
```

Let me flesh this out. I'll make a nice design.

For the hockey sticks, I'll draw two sticks crossed. A hockey stick has a long shaft and a blade at the bottom.

Let me place them behind the owl, forming an X.

Stick 1: from top-left to bottom-right
Stick 2: from top-right to bottom-left

Let me define the stick as a group that I can rotate.

Actually, let me make it simpler and cleaner. Let me create a good-looking logo.

Colors:
- Dark navy blue: #1a3a5c or #0d2b45
- Orange/amber accent: #f39c12 or #e67e22
- White: #ffffff
- Light gray for details

Let me write the full SVG:

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 400" width="400" height="400">
  <defs>
    <style>
      .text-main { font-family: Arial, Helvetica, sans-serif; font-weight: bold; }
    </style>
  </defs>
  
  <!-- Hockey sticks -->
  <g stroke="#e67e22" stroke-width="10" stroke-linecap="round" fill="none">
    <!-- Stick 1 -->
    <line x1="120" y1="90" x2="150" y2="320"/>
    ...
  </g>
</svg>
```

Hmm, let me think about the hockey stick shape more carefully. A hockey stick has:
- A long shaft
- A blade at the bottom that curves

Let me draw the blade as a path.

Let me create a reusable stick. Actually, let me just draw two sticks.

Stick shape (pointing down-left):
- Shaft from top going down
- Blade at bottom curving

Let me define one stick path and use transforms.

Actually, let me just carefully draw everything. Let me make a comprehensive design.

I'll create:

1. Background circle (optional, but they said no background preferred - I'll make the badge outline but transparent background)

2. Two crossed hockey sticks

3. Owl

4. Text "Owayo Eulers"

Let me write it out properly.

For the owl, let me create a nice stylized owl:

Body: ellipse centered around (200, 220)
Head: circle around (200, 140)
Eyes: two circles with pupils
Beak: triangle
Ears: triangles at top
Wings: paths on sides
Belly: lighter ellipse with feather lines

Let me be careful with the composition so it looks good.

Let me draft:

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 400" width="400" height="400">
  <!-- Hockey sticks -->
  <g>
    <!-- Left stick -->
    <path d="M 115 70 L 175 300 L 145 340 L 120 330 L 150 300 L 140 80 Z" fill="#c0392b"/>
    ...
  </g>
</svg>
```

This is getting complicated. Let me simplify.

Let me use a cleaner approach with separate elements.

Hockey stick: I'll make a shaft (thin rectangle/line) and a blade (curved path).

Let me define the stick pointing downward. Shaft is vertical, blade at bottom.

For stick 1 (rotated to go down-left), I'll create it pointing down and then rotate.

Base stick pointing down, centered at x=200:
- Shaft: from y=60 to y=300, at x around 195-205
- Blade: at bottom, curving

Let me make the blade:
```
M 190 300 
L 190 320 
Q 190 335 175 335 
L 160 335
```

Hmm, let me think. A hockey blade looks like an L/U shape at the bottom.

Let me create the stick as a group:

```svg
<g id="stick">
  <!-- shaft -->
  <rect x="194" y="50" width="12" height="250" rx="6" fill="#e74c3c"/>
  <!-- blade -->
  <path d="M 194 295 L 194 315 Q 194 330 178 330 L 160 330 L 160 318 L 175 318 Q 182 318 182 310 L 182 295 Z" fill="#c0392b"/>
</g>
```

Then I can duplicate and rotate this group.

For crossed sticks, rotate one by -20deg and the other by +20deg, or mirror.

Actually, let me place the pivot point. Let me put the top of the sticks around (200, 60) and let them spread out at the bottom.

Let me define the stick group with a transform to rotate around a center point.

OK here's my plan. Let me write the whole thing and refine.

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 400" width="400" height="400">
  <defs>
    <style>
      .team-name { font-family: Arial, Helvetica, sans-serif; font-weight: bold; fill: #ffffff; }
    </style>
  </defs>

  <!-- Hockey sticks (crossed) -->
  <g transform="translate(200,200)">
    <!-- Stick A -->
    <g transform="rotate(-25)">
      <rect x="-6" y="-140" width="12" height="230" rx="6" fill="#e74c3c"/>
      <path d="M -6 88 L -6 108 Q -6 124 12 124 L 30 124 L 30 110 L 14 110 Q 6 110 6 100 L 6 88 Z" fill="#c0392b"/>
    </g>
    <!-- Stick B -->
    <g transform="rotate(25)">
      <rect x="-6" y="-140" width="12" height="230" rx="6" fill="#e74c3c"/>
      <path d="M 6 88 L 6 108 Q 6 124 -12 124 L -30 124 L -30 110 L -14 110 Q -6 110 -6 100 L -6 88 Z" fill="#c0392b"/>
    </g>
  </g>
  ...
</svg>
```

Hmm, the blade paths are getting complex. Let me simplify the blade.

Actually, let me reconsider the whole design. Maybe simpler is better and cleaner.

Let me make a clean, professional sports logo.

Design concept:
- Circular badge with dark navy background ring
- "OWAYO" at top arc, "EULERS" at bottom arc (or straight text)
- Owl in center
- Two hockey sticks crossed behind owl

Let me simplify the owl to look good.

Let me write a cleaner version:

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 400">
  <!-- Crossed hockey sticks -->
  <g stroke="#f39c12" stroke-width="9" fill="none" stroke-linecap="round">
    <line x1="130" y1="110" x2="175" y2="330"/>
    <line x1="270" y1="110" x2="225" y2="330"/>
  </g>
  ...
</svg>
```

The blade needs to be added. Let me add blades at the bottom of each stick.

For stick going to bottom-left (from top-right): blade at bottom-left.
For stick going to bottom-right: blade at bottom-right.

Let me add blades as small curved paths.

Actually, let me combine shaft and blade into paths for each stick.

Stick 1 (top-left to bottom-right):
Path for shaft + blade.

Let me just do it with lines and separate blade shapes. I'll make the blade a small hook.

Let me finalize with this approach:

Stick 1: 
- Shaft: line from (135, 95) to (195, 315)
- Blade: hook at end pointing right

Stick 2:
- Shaft: line from (265, 95) to (205, 315)
- Blade: hook at end pointing left

Let me use stroke for shafts and paths for blades.

Hmm, let me reconsider. I want it to look clean. Let me draw complete stick shapes.

Let me define hockey stick as a single path. A hockey stick:
- Long handle
- Curves to a horizontal blade at the bottom

Let me create stick 1 pointing down and slightly left, blade at bottom-left:

```
M 140 90        <- top of handle
L 160 300       <- down to blade junction
Q 165 320 150 325  <- curve
L 120 325       <- blade top
L 120 312       <- blade edge drop
L 148 312       <- back
Q 152 305 150 300  <- junction
Z
```

This is getting messy. Let me take a step back.

I'll create the sticks as simple thick lines for shafts with a distinct blade drawn as a filled shape. Let me just make it look reasonable.

Final approach - I'll make clean vector shapes:

Let me define a hockey stick group once, positioned pointing straight down, then rotate/mirror.

Pointing-down stick, centered horizontally at x=0 (in local coords), top at y=-150:

Shaft: rect from (-5,-150) to (5, 90), width 10
Blade: a shape at the bottom

Blade shape (local, pointing down, blade extends to the right):
```
M 5 90
L 5 105
L -30 105
L -30 95
L 0 95
L 0 90
Z
```

So the blade is a horizontal piece at the bottom.

Then rotate this group. For stick 1, rotate -20°. For stick 2, mirror (scale x -1) then rotate 20°, or just create a mirror version.

Let me place the center of rotation at (0,0) which maps to (200, 130) in the logo (so sticks spread from top).

Actually the sticks should cross behind the owl. Let me have them cross around the middle.

Let me set pivot at (200, 120). Sticks go from top (near pivot) spreading outward to bottom.

Hmm, if pivot is at top and sticks rotate around it, they'd fan out from the top. That works for a crossed-sticks emblem.

Let me do pivot at (200, 130):
- Stick 1: base pointing down, rotate by -18°
- Stick 2: mirror, rotate by +18° (or reflect)

Wait, if both originate at pivot and go down, rotating one left and one right makes them form a V or X. Since they go downward from pivot, rotating ±18° makes a V shape (like an inverted cross). For an X/crossed look, I might want them to cross in the middle.

Actually for hockey logos, sticks are often crossed in an X behind the player/mascot. Let me make them cross.

Let me have both sticks pass through the center area, one going from top-left to bottom-right, other from top-right to bottom-left.

I'll define each stick pointing down, then:
- Stick 1: translate to a point, rotate 20°
- Stick 2: translate to a point, rotate -20° (mirror)

Let me just place pivot at center (200, 200) and have sticks extend both up and down? No, sticks only have blade at one end.

Let me simplify: Two sticks crossed like X, blades at bottom.

Stick 1: from top-left (120, 80) to bottom-right (250, 330), with blade at bottom-right end.
Stick 2: from top-right (280, 80) to bottom-left (150, 330), with blade at bottom-left end.

They cross in the middle around (200, 200).

Let me draw each as a path with shaft and blade.

Stick 1 path (shaft from top-left to bottom-right, blade at bottom-right):
The shaft is a thick line. Let me use stroke-linecap round and add a blade.

I'll do:
```svg
<g>
  <line x1="120" y1="80" x2="245" y2="315" stroke="#e67e22" stroke-width="10" stroke-linecap="round"/>
  <!-- blade -->
  <path d="M 245 315 L 270 335 L 258 347 L 235 327 Z" fill="#c0392b"/>
</g>
```

Hmm the blade angle. Let me make blades that curve like real hockey sticks.

Real hockey stick blade: at the bottom there's a curved toe and a straight heel.

Let me make a simpler recognizable blade: a small hook/curve.

Stick 1 blade (at bottom-right):
```
M 245 312
Q 260 325 268 340
L 256 348
Q 244 332 233 322
Z
```

This is getting complicated. Let me just make blades as small triangles/hooks and accept it's stylized.

Actually, you know what, let me reconsider. Let me make the design where the sticks are clearly hockey sticks with the characteristic bent blade, using clean paths.

Let me define a hockey stick shape in local coordinates pointing straight down with blade at bottom:

```
Shaft: thin vertical
Blade: at bottom, curves to form the stick blade
```

Local coordinates, top of stick at (0, -150), going down:

```
M -5 -150
L 5 -150
L 5 90
L 18 92
L 18 104
L -18 104
L -18 92
L -5 90
Z
```

Wait, this makes a blade that's a flat bottom piece. The shaft is from y=-150 to y=90, then blade from y=90 to y=104, extending from x=-18 to x=18. That's a reasonable hockey stick blade (the blade is the flat part that contacts ice).

Actually a hockey stick blade is more like: the shaft comes down and there's a horizontal blade at the very bottom. The shape I have works: vertical shaft, then a wider flat blade at bottom.

Let me refine:
```
M -4 -150
L 4 -150
L 4 88
L 16 90
L 16 102
L -16 102
L -16 90
Z
```

So:
- Top of handle: (-4,-150) to (4,-150)
- Right side down to (4, 88)
- Out to blade: (16, 90) to (16, 102)
- Bottom of blade: (16,102) to (-16,102)
- Up: (-16,102) to (-16,90)
- Back to shaft: (-4, 88)... 

Let me write it as a closed path:
```
M -4 -150
L 4 -150
L 4 88
L 15 90
L 15 102
L -15 102
L -15 90
Z
```

Hmm, I need to close properly. Let me trace:
Start (-4, -150) top-left of handle
→ (4, -150) top-right of handle
→ (4, 88) down right side of shaft
→ (15, 90) out to blade right
→ (15, 102) down blade right edge
→ (-15, 102) along bottom of blade
→ (-15, 90) up blade left edge
→ close back toward (-4, 88) area

The last line from (-15,90) back to start (-4,-150) would cut across. That's wrong. Let me add a point:
→ (-15, 90)
→ (-4, 88) up left side of shaft
→ close (back to -4,-150)

So:
```
M -4 -150
L 4 -150
L 4 88
L 15 90
L 15 102
L -15 102
L -15 90
L -4 88
Z
```

This traces the full outline. Good. This is a hockey stick pointing down with blade at bottom.

Now I'll create two of these. For stick 1, rotate by angle. For stick 2, mirror horizontally then rotate.

Let me place them crossing. I'll set the pivot (top of handle) at different positions so they cross.

Actually, let me place both handles' tops near the top and let them cross in the middle. If I rotate stick 1 by +15° and stick 2 by -15° (mirror), both handles start at same top point and spread at bottom — that's a V, not X.

For X crossing, I want them to cross. Let me offset them.

Alternative: Let me just make them cross by having each stick go from top-outside to bottom-inside.

Let me define stick pointing down at center. Then:
- Stick 1: rotate 15° clockwise → handle top at top-center, blade at bottom-right
- Stick 2: mirror (scaleX -1) then rotate 15° → handle top at top-center, blade at bottom-left

Both handles at top center, blades at bottom spreading → V shape. The shafts cross only at the very top pivot.

For a classic crossed-hockey-sticks emblem, this V/X shape with a pivot at top is actually common and looks fine. But let me make them cross more prominently.

Let me instead put the pivot points offset so the shafts clearly cross in the middle.

Stick 1: handle top at (185, 70), pointing down-right, blade at bottom. Rotate so it goes down-right.
Stick 2: handle top at (215, 70), pointing down-left, blade at bottom.

Hmm. Let me just go with crossing in the middle by rotating around center.

New idea: Rotate each stick around the center of the logo (200, 200). The stick's local center should be at (200,200) after transform.

Let me define the stick with its geometric center near origin. The stick spans from y=-150 (handle top) to y=102 (blade bottom), so center around y=-24. Let me shift so center is at origin: translate by (0, +24). So handle top at (0, -174), blade bottom at (0, 78).

Then rotate by ±15° around (200,200). The two sticks cross at center. Blades point down-ish, handles up-ish. This gives an X with blades at bottom. 

Let me compute: stick 1 rotated +15°, stick 2 rotated -15° (or mirror).

Actually for symmetry, let me mirror stick 2. Stick 1 rotated 15°, stick 2 is mirror of stick 1 rotated -15°... this is getting confusing.

Let me just do:
- Stick 1: transform="rotate(15 200 200)"
- Stick 2: transform="rotate(-15 200 200)"

Both defined identically (pointing down, centered). After rotation, they form an X with the crossing at (200,200). Blades at bottom (spread apart), handles at top (spread apart). 

Wait, if both sticks point straight down and I rotate one +15 and one -15, they form a V opening upward (like legs of V at bottom... no). Let me think. A stick pointing down, rotated +15° (clockwise) tilts the bottom to the right. Rotated -15° (counterclockwise) tilts bottom to left. So bottoms spread apart (one bottom-right, one bottom-left), tops... the tops are at top, rotating clockwise moves top to the left. So tops spread apart too (one top-left, one top-right). This makes an X shape! Because top-left to bottom-right is one stick, top-right to bottom-left is other. Wait no.

Stick 1 rotated +15°: it was vertical (top at top, bottom at bottom). Rotating clockwise 15°: top moves slightly left, bottom moves slightly right. So stick 1 goes from top-left to bottom-right. ✓
Stick 2 rotated -15°: top moves slightly right, bottom slightly left. So stick 2 goes from top-right to bottom-left. ✓

Yes! This forms an X crossing at center. 

But the crossing point: both sticks pass near center (200,200) since I centered them there. Good, they cross at (200,200).

Now the owl sits in the center, on top of the crossed sticks.

Let me also make sure the sticks don't extend too far outside the badge circle. Badge radius ~180, center (200,200). Stick spans from y=-174 to y=78 relative to center, so from y=26 to y=278, and with rotation a bit more horizontal spread. At the top, handle top at (200, 26) roughly, within circle (radius 180 from center means top of circle at y=20). Hmm, y=26 is just inside. At bottom, blade at y=278, circle bottom at y=380. Within. Good. But with rotation the spread increases slightly. Should be fine, maybe I'll shrink the stick a bit.

Let me reduce stick length: handle from y=-150 to blade y=78, center shift +36 → handle top (0,-114)... let me just tune.

Let me simplify: stick local coordinates:
- Handle top: (0, -140)
- Blade bottom: (0, 70)
- Center of stick (for rotation pivot): I'll use (200,200) as pivot, and place stick so it's centered vertically around there.

Stick vertical span: -140 to 70, midpoint -35. To center at (200,200), I translate stick so midpoint is at origin: add +35 to all y. So:
- Handle top: (0, -105)
- Shaft/blade junction: (0, 125)
- Blade bottom: (0, 105)

Ugh, let me just define with explicit coordinates after shifting.

Local stick (before rotation), centered so that rotation pivot (200,200) is at stick's vertical center:

Stick vertical extent I want: from y=60 (top, in logo coords) to y=340 (bottom). Center = 200. So in local coords (relative to 200): top at y=-140, bottom at y=140.

Path (local, y relative to 200, x relative to 200):
```
M -4 -132      handle top left
L 4 -132       handle top right
L 4 78         shaft right down to blade
L 15 80        blade
L 15 92
L -15 92
L -15 80
L -4 78
Z
```

Wait I need blade at bottom. Handle top at y=-132, shaft down to y=78, then blade from y=80 to y=92. Total bottom at y=92. But I wanted bottom at y=140. Let me extend.

Let me make:
```
M -4 -132
L 4 -132
L 4 95
L 16 97
L 16 115
L -16 115
L -16 97
L -4 95
Z
```

Top at -132, bottom at 115. Center ≈ (-132+115)/2 = -8.5. Close enough to center at 200. With rotation around (200,200), the stick will be roughly centered. Good enough.

Now the blade is at the bottom (y around 97-115 in local = 297-315 in logo). Handle top at y=-132 local = 68 logo. Good, within circle.

After rotate(15 200 200) and rotate(-15 200 200), we get crossed sticks.

Let me also add a grip at the top of the handle (darker color) for detail. Maybe a slightly wider darker segment at top.

OK let me also design the owl.

Owl design (centered around (200, 210), sitting above the cross point):

Let me make a cute/stylish owl:

Body: main ellipse. Let me make body from about y=150 to y=290, centered x=200.
- Body ellipse: cx=200, cy=220, rx=70, ry=80

Head: top part, larger. Actually owls have big heads. Let me make head a circle at top.
- Head: cx=200, cy=150, r=65

Eyes: two large circles.
- Left eye: cx=175, cy=145, r=28
- Right eye: cx=225, cy=145, r=28
- Pupils: smaller dark circles with light reflection

Beak: small triangle between eyes, below.
- Beak: polygon (195,168) (205,168) (200,185)

Ears/tufts: two triangle tufts at top of head.
- Left: (150,105) (175,120) (165,100)
- Right: (250,105) (225,120) (235,100)

Wings: two shapes on sides of body, darker.
- Left wing: path on left side
- Right wing: path on right side

Belly: lighter ellipse in center of body with feather lines.
- Belly: cx=200, cy=245, rx=45, ry=55, lighter color
- Feather lines: a few small V or arc shapes

Body color: I'll use a nice brown/gray. Let me use a blue-gray to match a hockey team, or brown. Let me go with a warm brown owl (#8B5A2B or similar) with lighter belly.

Actually, for a cohesive team logo, let me pick a color scheme:
- Primary: Navy blue #1b3a5b or #0f2c4a
- Accent: Gold/amber #f5b041 or #e8a33d
- Owl: browns/grays
- White for text and eyes

Let me make the owl use the team colors somewhat. Owl body could be a steel gray, belly cream.

Let me finalize colors:
- Stick shaft: #e67e22 (orange) with darker blade #c0392b (red) — or make sticks navy with white. Let me make sticks a contrasting color. Hockey sticks are often dark. Let me do dark gray/navy sticks with orange blade tip, or classic. Let me do sticks in #2c3e50 (dark slate) with orange accents.

Hmm, let me reconsider the whole palette for cohesion:
- Navy: #14345b (primary)
- Amber/gold: #f2a900 or #e8960c (accent)
- White: #f7f7f7
- Owl: #6b7b8d (blue-gray) body, #d9e2ea light belly
- Stick: #2a2a2a handle, #e8960c blade

Let me go with:
- Owl body: #5d6d7e (medium blue-gray)
- Owl belly: #e8eef2 (light)
- Owl eyes: white with dark pupils
- Beak: #e8960c (amber)
- Sticks: handle #34495e (dark slate), blade #e8960c (amber)
- Badge ring: navy #14345b with amber inner accent
- Text: white

Let me now write the full SVG.

Let me also add the text "OWAYO EULERS". I'll place "OWAYO" and "EULERS". Given "Eulers" in the prompt (German spelling of Eulen = owls), I'll use "EULERS" as given. Actually the prompt says "Owayo Eulers". Let me use exactly "OWAYO EULERS" or "Owayo Eulers". I'll use "OWAYO EULERS" in bold caps for a logo look, or match the given casing. Let me use "OWAYO EULERS" for visual impact, but maybe better to respect given name "Owayo Eulers". Hmm. For a sports logo, all-caps is typical. I'll do "OWAYO EULERS". Actually, let me respect the exact name but I think caps look better. Let me use "OWAYO EULERS".

Hmm, wait — the team is "Owayo Eulers". I'll display "OWAYO EULERS". This is fine.

Let me place text. Options:
1. Curved text along top and bottom of circle using textPath.
2. Straight text at bottom.

Curved text looks more like a sports badge. Let me use textPath for curved text.

Top arc text: "OWAYO" 
Bottom arc text: "EULERS"

Or full "OWAYO EULERS" on top arc, and stars/decorations.

Let me do:
- Top arc: "OWAYO"
- Bottom arc: "EULERS"

Using textPath with circular paths.

For top arc, the path goes along the top of the circle. For bottom arc, text should be readable (not upside down), so the path goes along the bottom in the reading direction.

Let me define paths:
- Top path: from left to right along the top. A path like M 40,200 A 160,160 0 0 1 360,200 — this is the top semicircle from (40,200) to (360,200) going over the top. Text on this reads left-to-right along the top arc. Good.

Wait, I need to be careful. Let me use radius 155 for text baseline.

Top arc path (reading left to right, over the top):
M 45 200 A 155 155 0 0 1 355 200
This draws a semicircle from (45,200) to (355,200) through the top (since sweep goes counterclockwise... let me check). Starting at (45,200) which is left side, radius 155, to (355,200) right side. With large-arc-flag=0, sweep-flag=1. Hmm, need to get the direction right so text is on top and upright.

Actually, let me use a cleaner method. For text along the top of a circle, upright:
Path: M (cx - r, cy) A r r 0 0 1 (cx + r, cy) — this goes from left point, and with sweep-flag 1 (clockwise in SVG's coordinate system where y is down)... 

In SVG, sweep-flag=1 means clockwise in the coordinate system (which visually is clockwise because y points down, so clockwise visually). Starting at left point (cx-r, cy), going clockwise would go DOWN first (to bottom), not up. So for text over the top, I want counterclockwise visually, which is sweep-flag=0.

Let me just test mentally: M 45 200 A 155 155 0 0 0 355 200. Sweep-flag 0. From (45,200) [left], the arc to (355,200) [right] going counterclockwise (sweep 0) would pass through the top. Yes. So top arc: M 45 200 A 155 155 0 0 1 355 200? 

Ugh, let me think very carefully. SVG arc: A rx ry x-rotation large-arc-flag sweep-flag x y.
sweep-flag = 1: positive-angle direction (clockwise in standard math, but in SVG screen coords where y-down, this appears clockwise).

Hmm, actually in SVG with y-axis pointing down, sweep-flag=1 draws the arc in the "positive angle" direction which visually is clockwise.

Starting point (45, 200) is to the LEFT of center (200,200). To reach (355,200) which is to the RIGHT:
- Going clockwise (sweep=1): from left, clockwise goes... down then right then up. So it would go through the BOTTOM. That places text at bottom. Not what I want for top.
- Going counterclockwise (sweep=0): from left, counterclockwise goes up then right. Through the TOP. 

So for top arc text: sweep-flag=0.
Path: M 45 200 A 155 155 0 0 0 355 200
(large-arc-flag=0 since it's a semicircle, either works but 0 is fine for exactly half)

Wait, for a semicircle both flags give semicircle but different halves. large-arc-flag distinguishes which of the two arcs. For exactly 180°, it's ambiguous but let me use 0.

Hmm, actually for textPath, the text is placed along the path direction. With the top arc from left to right, text reads left-to-right, upright. 

For bottom arc text (upright, reading left to right along the bottom):
We want text along the bottom, upright. The path should go from right to left along the bottom (so that text, placed in path direction, reads left-to-right when we... no).

For bottom text to be upright and readable, the path baseline should be at the bottom and text direction should be left-to-right. If I draw the path from (355, 200) [right] to (45,200) [left] along the bottom, then text placed along this path goes right-to-left, which would appear mirrored/reversed. 

To get bottom text upright reading left-to-right, I should draw the path from left to right ALONG THE BOTTOM, i.e., from (45,200) through the bottom to (355,200). That's sweep-flag=1 (clockwise) from left point: from left, clockwise goes down through bottom to right. Yes! So:
Bottom arc path: M 45 200 A 155 155 0 0 1 355 200
This goes from left, clockwise, through the bottom, to right. Text placed on it reads left-to-right, and since it's at the bottom, it's upright. 

So:
- Top text path: M 45 200 A 155 155 0 0 0 355 200  (over the top)

Hmm wait, let me double check top. Actually I realize I should double-check by considering the text anchor. Let me use text-anchor="middle" and center the path.

Actually, let me simplify and just center each text. I'll make the full path and use text-anchor middle, but the path needs to be symmetric.

Let me reconsider. I'll make:
- Top text "OWAYO" centered at top. I'll use a path that's the top arc, and place text with middle anchor at the arc's middle (top, at x=200, y≈45).
- Bottom text "EULERS" centered at bottom.

For the text to follow the curve and be centered, I'll define paths and use textLength or just rely on the path.

Let me define:
Top path (id="topArc"): M 50 205 A 150 150 0 0 0 350 205 — hmm the endpoints. Let me make the arc span the top. Actually let me make endpoints at the sides so text wraps nicely.

Let me reconsider radius and positions. Badge circle radius 175, center (200,200). Text baseline radius ~150.

Top arc endpoints at angle: I want text to span maybe from 20° to 160° (top region). Let me just make a semicircular-ish arc.

Let me define:
Top arc: starts at left (around 200,205) no...

I'll keep it simple:
Top path: M 55 200 A 145 145 0 0 0 345 200
This is an arc from (55,200) to (345,200), radius 145, sweep 0 (through top). The topmost point of this arc is at (200, 200-145)=(200,55). Text centered there.

But wait, (55,200) is at the same height as center, 145 to the left. And (345,200) is 145 to the right. The arc through the top reaches up to y=55. This is a full semicircle (top half). Text "OWAYO" centered would sit along the top. Good.

Bottom path: M 55 200 A 145 145 0 0 1 345 200
Arc from (55,200) to (345,200) through the bottom (sweep 1). Bottommost point (200, 345). Text "EULERS" centered there, upright. Good.

Now, text-anchor="middle" with the text starting at path start... Actually with textPath, text starts at the beginning of the path and extends. To center, I can use textLength or just set the text to start appropriately. A common trick: use `<text text-anchor="middle">` with textPath — but text-anchor middle centers the text relative to... hmm, it's relative to the start point alignment. Actually text-anchor applies to the text's own box. With textPath, the anchor point is on the path. text-anchor="middle" would center the text's midpoint at the path's start point. That's not what I want.

Better approach: Let the text naturally flow and position the path so the text is centered. Or use `<textLength>` to stretch. 

Simplest robust approach: I'll place the start of the top arc at the left and let text extend clockwise... no.

Alternative simpler approach: Don't use curved text. Use straight text. Place "OWAYO" as a straight bold text at top and "EULERS" at bottom, or "OWAYO EULERS" as one line. Straight text is cleaner and less error-prone.

Actually, curved text looks much more like a sports logo. Let me try to get it right.

Let me use this approach for centered curved text:
- Define the arc path.
- Use `<text><textPath href="#id">TEXT</textPath></text>`
- Set `startOffset="50%"` and `text-anchor="middle"`. This centers the text at 50% along the path. 

Yes! `startOffset="50%"` with `text-anchor="middle"` centers the text at the middle of the path. That's the standard technique. 

So:
```svg
<text class="team-text" font-size="34" font-weight="bold" letter-spacing="3">
  <textPath href="#topArc" startOffset="50%" text-anchor="middle">OWAYO</textPath>
</text>
```

This should center "OWAYO" along the top arc. Good.

For the href, I can use href or xlink:href. Modern SVG uses href. Since no external resources and no scripts, href is fine. Let me use href.

Now let me assemble everything.

Let me also add small decorative stars or dots between the text and the owl, or side lines. Optional. Let me add two small stars or just keep it clean.

Let me now write the complete SVG.

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 400" width="400" height="400">
  <defs>
    <path id="topArc" d="M 55 200 A 145 145 0 0 0 345 200" />
    <path id="bottomArc" d="M 55 200 A 145 145 0 0 1 345 200" />
  </defs>

  <!-- Crossed hockey sticks -->
  <g>
    <!-- Stick 1 -->
    <g transform="rotate(15 200 200)">
      <path d="M -4 -132 L 4 -132 L 4 95 L 16 97 L 16 115 L -16 115 L -16 97 L -4 95 Z" fill="#2c3e50"/>
      <rect x="-5" y="-132" width="10" height="18" rx="3" fill="#e8960c"/>
    </g>
    <!-- Stick 2 -->
    <g transform="rotate(-15 200 200)">
      <path d="M -4 -132 L 4 -132 L 4 95 L 16 97 L 16 115 L -16 115 L -16 97 L -4 95 Z" fill="#2c3e50"/>
      <rect x="-5" y="-132" width="10" height="18" rx="3" fill="#e8960c"/>
    </g>
  </g>
  ...
</svg>
```

Wait, I need the sticks behind the owl but the owl is in the center. The sticks cross at center (200,200). The owl body is around (200,220). So the owl covers the crossing area. The stick tops (handles) extend up to y=68 (200-132) and blades down to y=315 (200+115). These stick ends stick out around the owl. Good.

But the rotate(15) around (200,200): the stick is centered at origin (local), and I rotate around (200,200) which is the local origin. So the stick just rotates in place. Top handle goes from (200,68) rotating... at 15°, the top handle point (0,-132) rotates to (−132·sin15°, −132·cos15°) = (−34, −128) relative to center → (166, 72). And blade (0,115) rotates to (115·sin15°, 115·cos15°)=(30, 111) → (230, 311). So stick 1 goes from (166,72) to (230,311). Stick 2 (rotate -15°) from (234,72) to (170,311). They cross at (200,200). Good, forms an X.

The owl sits at center covering the crossing. Good.

Now the owl. Let me draw it.

Owl:
- Body: I'll draw a rounded body. Let me use an ellipse plus rounded top for head combined.

Let me make the owl as a composite:

Head + body in one, or separate. Let me do:

1. Body (main): ellipse cx=200 cy=235 rx=72 ry=80. Color #5d6d7e.

Actually, let me make the owl sit nicely. Let me place:
- Body center at (200, 240)
- Head centered at (200, 155), overlapping body.

Let me draw:

Ears/tufts (behind head):
```svg
<path d="M 155 110 L 145 78 L 180 105 Z" fill="#5d6d7e"/>  <!-- left tuft -->
<path d="M 245 110 L 255 78 L 220 105 Z" fill="#5d6d7e"/>  <!-- right tuft -->
```
Hmm, let me make tufts point up-and-out.

Head:
```svg
<circle cx="200" cy="150" r="68" fill="#5d6d7e"/>
```

Eyes (white circles with dark rings):
```svg
<circle cx="172" cy="150" r="30" fill="#ffffff"/>
<circle cx="228" cy="150" r="30" fill="#ffffff"/>
<circle cx="174" cy="152" r="15" fill="#14345b"/>
<circle cx="226" cy="152" r="15" fill="#14345b"/>
<!-- reflection -->
<circle cx="170" cy="147" r="5" fill="#ffffff"/>
<circle cx="222" cy="147" r="5" fill="#ffffff"/>
```

Beak:
```svg
<path d="M 190 172 L 210 172 L 200 192 Z" fill="#e8960c"/>
```

Wings:
```svg
<path d="M 132 210 Q 110 250 135 300 Q 155 280 150 230 Z" fill="#4a5968"/>
<path d="M 268 210 Q 290 250 265 300 Q 245 280 250 230 Z" fill="#4a5968"/>
```

Belly:
```svg
<ellipse cx="200" cy="255" rx="48" ry="58" fill="#dfe7ee"/>
```
Feather lines on belly:
```svg
<path d="M 180 235 Q 200 248 220 235" fill="none" stroke="#b0bcc7" stroke-width="2"/>
<path d="M 178 258 Q 200 271 222 258" fill="none" stroke="#b0bcc7" stroke-width="2"/>
<path d="M 180 281 Q 200 294 220 281" fill="none" stroke="#b0bcc7" stroke-width="2"/>
```

Body sides over belly edges to blend. Actually the belly ellipse on top of body is fine.

Let me reconsider proportions. Head r=68 at cy=150 means head spans y=82 to 218, x=132 to 268. Body at cy=240, ry=80 spans y=160 to 320. There's overlap between head (bottom 218) and body (top 160). Good, they merge.

But head bottom at y=218 and body top at y=160 — the head overlaps the upper body. The eyes at cy=150 are within head. Good.

Wings at the sides. Belly ellipse cy=255 rx=48 ry=58 spans y=197 to 313, x=152 to 248. Within body. Good.

Let me make sure the owl fits within the badge. Owl spans x=132 to 268 (width 136), y=78 (tufts) to 320 (body bottom). The badge circle radius 175 spans x 25-375, y 25-375. Owl fits inside. Good.

Now the text arcs at radius 145, so text sits at x from 55 to 345, top text around y=55, bottom around y=345. These are within the badge ring (radius 175, so ring from 175 to maybe 185). Let me add the badge rings.

Badge:
```svg
<circle cx="200" cy="200" r="180" fill="none" stroke="#14345b" stroke-width="10"/>
<circle cx="200" cy="200" r="162" fill="none" stroke="#e8960c" stroke-width="3"/>
```

The inner amber ring at r=162. Text at radius 145 is inside that. Good. Actually text baseline at 145, so text occupies from ~130 to ~160 radius. The inner ring at 162 is just outside bottom text... let me check bottom text. Bottom text at radius 145, font-size 34, so it extends from radius ~128 to ~162. The ring at 162 might overlap. Let me move inner ring to r=168 or reduce. Let me set inner ring r=170. And text radius 140. Let me recompute.

Hmm, let me just set:
- Outer ring r=180, stroke-width 10 (so from 175 to 185).
- Inner ring r=160, stroke-width 3 (from 158.5 to 161.5).
- Text baseline radius: top text at 140, bottom text at 140.

Bottom text at radius 140, font 34: extends from 140-12=128 to 140+... actually text extends outward and inward from baseline. For bottom text (upright), the text goes upward from baseline? No. For text at the bottom of circle reading upright, the baseline is at radius 140, and text extends upward (toward center) because it's upright... 

Wait. Bottom arc, text upright. The baseline follows the arc at radius 140. The text (upright) extends from the baseline UPWARD toward the center (radius decreasing) — no wait, upright text at the bottom: the letters stand on the baseline and extend upward, which at the bottom of the circle means extending toward the center (radius decreasing). Hmm, actually no.

Let me think. At the bottom of the circle (point 200, 340 for r=140... wait r=140 bottom is 200, 340). Text there is upright (readable). The baseline is the bottom of the letters. Upright letters extend upward from baseline. Upward at that point = toward center = decreasing radius. So text extends from radius 140 toward smaller radius (up to ~140-30=110). So bottom text occupies radius ~110 to 140. That's well inside the inner ring at 160. Good, no overlap.

Wait, that doesn't sound right either. Let me reconsider. If baseline is at radius 140 (point 200,340) and text extends upward (toward center), the top of letters is at radius ~110 (point 200, 310). So the text is between radius 110 and 140, in the lower area. The inner ring at 160 is outside (larger radius). No overlap. Good.

Top text: baseline at radius 140 (point 200, 60). Upright text... but top text should be upright too (reading normally). At the top of the circle, upright text extends downward from baseline (toward center, decreasing radius). So top text occupies radius 140 down to ~110 (point 200, 90). Between radius 110 and 140. Inside inner ring 160. Good.

Wait, but for top text with the arc going through the top, if text is upright, it extends downward. Let me make sure the textPath makes it upright. With startOffset 50% and text-anchor middle on the top arc (which goes left to right over the top), the text baseline is tangent to the arc (horizontal at top) and text extends... For a path going left-to-right along the top, the "up" direction for upright text would be away from the path's left side. Hmm, text on a path: the text is drawn upright relative to the path direction, with the baseline on the path and text extending to the left of the direction of travel... no.

This is the tricky part. Text on a path: characters are placed along the path, oriented so they read in the path's direction, and they extend to one side of the path (the side determined by... the text is above the baseline in the direction perpendicular, which for a left-to-right path is "up" in the path's local coordinate, but the path's "up" depends on orientation).

For a horizontal path going left-to-right, text sits above the path (standard). For the top arc (curving over the top), at the topmost point the path is horizontal going left-to-right, so text sits above the path = away from center = larger radius = outside. That would put top text outside the ring. Hmm, that might overlap the outer ring.

Wait, let me reconsider. At the topmost point of the top arc (200, 60) for r=140, path going left-to-right. Text baseline on path, text extends "up" in local coords = away from center (toward y < 60, larger radius). So top text would be above y=60, i.e., radius > 140, extending outward. That could hit the inner ring at 160 or go past.

Hmm, that means top text is between radius 140 and 170 (if font 34, extends to ~140+17=157). Inner ring at 160. Might slightly overlap. Let me adjust: put inner ring at 165, text radius 135.

Actually, let me reconsider which way text extends. I might be overcomplicating. Let me reconsider the bottom text too.

For bottom arc going left-to-right through the bottom (sweep=1), at bottommost point (200, 340), path goes left-to-right (horizontal). Text baseline on path, text extends "up" in local coords = away from... at the bottom, "up" in local coords (perpendicular to path, to the left of travel direction). Travel direction is +x (right). Left of +x in screen coords (y down) is... perpendicular to +x, left turn is +y (down) in screen coords? Let me compute: direction (1,0). Left perpendicular (rotate +90° counterclockwise in math, but screen y is down)... 

Ugh, this is getting too detailed. Let me just use a known-good pattern and verify visually by reasoning, or better, let me make the text fit and not worry too much; I'll position things with margins.

Known working pattern for circular text badges:

Top text (arched, reading along the top, upright):
```svg
<text>
  <textPath href="#topPath" startOffset="50%" text-anchor="middle">TEXT</textPath>
</text>
```
where topPath is the top semicircle.

I've seen this work with text arching over the top and being upright. Let me trust it. The key question is just placement/margins to avoid overlap.

Let me use these radii:
- Outer ring: r=182, stroke-width 8 (covers 178-186)
- Inner ring: r=150, stroke-width 3 (covers 148.5-151.5)
- Text baseline: r=135 for both top and bottom
- Text font-size: 30

Top text: baseline r=135 (point 200, 65). Text extends outward (toward top, radius increasing) to ~135+16=151. That would touch inner ring at 151. Risky.

Alternatively, text extends inward. Let me just make margins generous:
- Inner ring: r=155
- Text baseline: r=128, font-size 28
- Top text extends to ~128+15=143 < 155. OK.
- Bottom text extends inward (toward center) from baseline r=128 (point 200, 328) up to ~128-15=113. Fine.

Hmm, but I'm unsure of direction. Let me just make everything with good margins and it'll look fine either way.

Let me set:
- Outer ring r=182 w=8
- Inner ring r=158 w=3
- Text baseline r=125
- Font-size 28, letter-spacing 2

Top text baseline r=125 → point (200, 75). Extends ±15 → 110 to 140. Inner ring 158. No overlap. Good.
Bottom text baseline r=125 → point (200, 325). Extends ±15 → 110 to 140. Inner ring 158. No overlap. Good.

Owl body bottom at y=320 (cy=240, ry=80). Bottom text at y=325 baseline. Slight overlap? Owl body bottom 320, text baseline 325. The text extends inward (up) to 310. So text occupies 310-325 area, owl body occupies up to 320. Overlap around 310-320! 

Hmm. Let me raise the owl up or lower the text. Let me move owl body up: cy=230, ry=75 → bottom at 305. Then text at 310-325 doesn't overlap. Good. Let me adjust owl.

Let me set owl:
- Head: cx=200, cy=150, r=64
- Body: cx=200, cy=225, rx=70, ry=72 → bottom 297
- Belly: cx=200, cy=240, rx=46, ry=52

Wings adjust accordingly.

Actually, let me reconsider the whole owl layout to fit nicely between the text arcs.

Text arcs: top text around y=60-110, bottom text around y=290-340.
Owl should occupy roughly y=120 to y=290.

Let me place:
- Tufts/ears: y=95 to 120 (top of owl)

Wait, but top text is at radius 125, top point (200,75), text extends to 110. So owl should start below y=110. Let me put owl head top around y=115.

- Head: cx=200, cy=155, r=58 → top 97. Hmm that reaches y=97, overlapping top text (which goes to 110). Let me use cy=160, r=55 → top 105. Still close. Let me use cy=162, r=52 → top 110.

This is getting fiddly. Let me just make the owl a bit smaller and center it, and place text arcs closer to the edge.

New plan:
- Badge: outer ring r=180, inner ring r=155.
- Text baseline r=140 (close to ring), font-size 26.
  - Top text: baseline (200,60), extends outward to ~75? No...

I keep going in circles (pun intended). Let me just DECIDE:

The text will be placed with the baseline on the arc, and I'll assume text extends AWAY from center for top (up) and the bottom text extends toward center (up). Actually, let me just make the text span and verify with the anchor.

You know what, let me simplify by NOT centering via startOffset but instead I'll just trust the standard pattern and use generous margins. Let me also add the owl SMALLER so there's clear separation.

Let me define final layout:

Center (200,200).
- Outer ring: r=180, w=9, color navy.
- Inner ring: r=156, w=3, color amber.
- Top text "OWAYO": baseline radius 143, font 27, weight bold, fill white, letter-spacing 3.
- Bottom text "EULERS": baseline radius 143, font 27, bold, white, letter-spacing 3.
- Owl: occupies center.

Owl coordinates (final):
- Ears: 
  - Left: M 158 118 L 148 88 L 180 112 Z
  - Right: M 242 118 L 252 88 L 220 112 Z
- Head: circle cx=200 cy=158 r=56
- Eyes:
  - White: cx=173 cy=158 r=26; cx=227 cy=158 r=26
  - Pupil: cx=175 cy=160 r=13; cx=225 cy=160 r=13
  - Highlight: cx=171 cy=155 r=4.5; cx=221 cy=155 r=4.5
- Beak: M 191 178 L 209 178 L 200 196 Z (amber)
- Body: ellipse cx=200 cy=240 rx=66 ry=70
- Wings:
  - Left: M 138 212 Q 116 250 140 296 Q 158 276 154 226 Z (darker)
  - Right: M 262 212 Q 284 250 260 296 Q 242 276 246 226 Z
- Belly: ellipse cx=200 cy=250 rx=43 ry=50 (light)
- Belly feathers: 3 arcs

Head bottom at cy=158+56=214. Body top at cy=240-70=170. Overlap 170-214. Good.
Eyes at cy=158, within head (102-214). x=173 and 227, within head (144-256). Good.
Beak at y=178-196, between eyes, below them. Eyes bottom at 158+26=184. Beak top at 178, slightly overlapping eyes bottom. That's fine (beak sits between/just below eyes). Actually beak at 178 is above eye bottom 184, so beak top overlaps eye bottoms. Let me move beak down: beak top at 188. M 191 188 L 209 188 L 200 206 Z. 

Belly at cy=250, spans 200-300. Body spans 170-310. Belly within body. Belly top 200, above body... 200 > 170 so within. Good. Belly bottom 300, body bottom 310. Good.

Owl total: top tufts y=88, bottom body y=310. 
Top text baseline (200, 57) [r=143 → 200-143=57], extends to ~110 (if outward) or inward. Bottom text baseline (200, 343) [200+143=343], but that's outside badge (badge bottom 180). Wait r=143 bottom is 200+143=343, but badge radius 180 → bottom 380. 343 < 380, OK within. Text extends inward to ~313. Owl body bottom 310. Overlap risk around 310-313. Let me move owl up slightly or reduce.

Let me move owl up by 8: shift everything down by... let me just reduce owl size. Or lower text baseline radius.

Ugh. Let me just set text baseline r=138 and owl body bottom at 305.

Owl body: cy=235, ry=68 → bottom 303. Belly cy=245 ry=48 → 200-293. 
Text baseline r=138: bottom text (200, 338), extends inward to ~310. Owl body bottom 303. Gap 303-310. OK small gap. Good.

Hmm, let me not over-engineer. Small overlaps in a logo are often fine and can even look intentional. But let me aim for clean separation.

Let me finalize with these numbers and move on. I'll make owl a touch smaller.

FINAL OWL:
- Ears:
  - Left: M 160 120 L 150 92 L 182 114 Z
  - Right: M 240 120 L 250 92 L 218 114 Z
- Head: circle cx=200 cy=160 r=54
- Eyes white: cx=174 cy=160 r=24; cx=226 cy=160 r=24
- Pupils: cx=176 cy=162 r=11; cx=224 cy=162 r=11
- Highlights: cx=172 cy=157 r=4; cx=220 cy=157 r=4
- Beak: M 192 182 L 208 182 L 200 200 Z
- Body: ellipse cx=200 cy=240 rx=62 ry=66
- Wings:
  - Left: M 140 210 Q 120 248 142 290 Q 159 272 155 222 Z
  - Right: M 260 210 Q 280 248 258 290 Q 241 272 245 222 Z
- Belly: ellipse cx=200 cy=250 rx=40 ry=48
- Belly feathers: 
  - M 182 232 Q 200 244 218 232
  - M 181 254 Q 200 266 219 254
  - M 183 276 Q 200 288 217 276

Colors:
- Head/body/wings: #5d6d7e (blue-gray)
- Wings darker: #4a5867
- Belly: #e3eaef
- Belly feathers: #b9c6d1
- Eyes white: #ffffff
- Pupils: #12283f (dark navy)
- Beak: #e8960c (amber)
- Ears: #5d6d7e

Sticks:
- Shaft path: #2c3e50 (dark slate)
- Grip (top): #e8960c

Badge:
- Outer ring: #14345b (navy), w=9
- Inner ring: #e8960c (amber), w=3

Text: white, bold, font-family Arial/sans-serif.

Let me also add a subtle inner fill? The prompt says background should be solid color or none. I'll keep background transparent (no bg rect) and just have the badge ring. That satisfies "no background" — the area outside is transparent.

Wait, but "solid background" was an option; "no background" is preferred. I'll go with no background (transparent), just the logo elements. Good.

Let me now also reconsider: should the sticks be behind the owl (drawn first) — yes, I'll draw sticks first, then owl, then text, then rings on top. Actually rings should be on top of everything except maybe text. Let me draw order:
1. Sticks (behind)
2. Owl
3. Text arcs
4. Rings (outer, inner) on top — but rings would cover parts of owl/sticks/text at the edges. Since owl/sticks are inside, and text is inside, rings on top is fine (rings only at the very edge). Actually text near the edge might be covered by ring. Text baseline r=138, ring inner r=156. Text extends to ~153 max, ring at 156. So text is inside ring, ring drawn on top won't cover text. Good. But wait, I want rings to frame the text. If ring is at 156 and text at 138-153, the ring is outside the text, framing it. Good. Draw rings last (on top) — they won't cover text since text is inside.

Hmm, but actually if I draw rings last, and the owl/sticks extend to near the ring, the ring covers their tips slightly. Sticks: top handle at ~y=72 (from earlier, rotated), which is radius sqrt((200-166)^2+(200-72)^2)=sqrt(34^2+128^2)=sqrt(1156+16384)=sqrt(17540)=132. So stick tips at radius ~132, inside ring 156. Good, not covered. Owl tufts at y=92, x=150: radius sqrt(50^2+108^2)=sqrt(2500+11664)=sqrt(14164)=119. Inside ring. Good.

So drawing rings last is fine.

Actually, let me draw rings BEFORE the owl and sticks? No. Let me think about what should be on top. The badge ring is the outermost frame, should be on top (visible). Text also on top. Owl and sticks in the middle. Let me do: sticks → owl → text → rings. Since rings are at the edge and everything else is inside, rings on top is fine.

But text on top of owl? Text is at the edge (radius 138+), owl is center (radius up to ~132 at widest? owl width: head x 146-254, radius from center sqrt(54^2+... ) at y=160, point (146,160): radius sqrt(54^2+40^2)=sqrt(2916+1600)=sqrt(4516)=67. So owl widest at radius ~67 horizontally, and tufts at 119. Text at 138. So text is outside owl's extent mostly. Text won't overlap owl. Good.

Alright, let me write it all out.

Let me reconsider stick blade shape. My stick path:
```
M -4 -132 L 4 -132 L 4 95 L 16 97 L 16 115 L -16 115 L -16 97 L -4 95 Z
```
Let me verify this is a hockey stick: 
- Top: handle from (-4,-132) to (4,-132), width 8.
- Sides down to (4,95) and (-4,95)? Wait, from (4,-132) I go to (4,95) — that's the right side of the shaft down to y=95. Then L 16 97 (out to blade), L 16 115 (down), L -16 115 (across bottom), L -16 97 (up), L -4 95 (in to shaft), Z back to (-4,-132).

So the shaft is width 8 (from x=-4 to 4) from y=-132 to y=95. Then the blade is from y=95 to y=115, width 32 (x=-16 to 16). This looks like a hockey stick: thin handle, wider blade at bottom. 

But real hockey stick blade is only at the very end and is horizontal (parallel to ice). My blade is a flat horizontal piece at the bottom. Good enough, looks like a hockey stick blade.

Actually, a hockey stick's blade is at the bottom and the shaft comes down to it at one end (the heel), with the toe sticking out. My symmetric blade (centered under the shaft) looks more like a "T" or a hockey stick viewed straight. It's acceptable for a stylized logo. To make it more hockey-like, I could offset the blade, but symmetric is cleaner. Let me keep symmetric but maybe make the blade slightly asymmetric. Actually, let me keep it simple and symmetric.

Hmm, but a symmetric bottom blade looks a bit like a "hockey stick" is fine, or like a "key". Let me add a slight curve to make it clearly a blade. Let me make the blade curve up at the ends:
```
M -4 -132 L 4 -132 L 4 92 L 15 94 L 16 108 Q 0 118 -16 108 L -15 94 Z
```
This makes the blade bottom curved (dipping in the middle). Actually hockey blade is flat on bottom. Let me keep flat but maybe add the characteristic shape. I'll keep it simple: flat blade.

Let me finalize the stick path as:
```
M -4 -132 L 4 -132 L 4 92 L 15 94 L 15 112 L -15 112 L -15 94 L -4 92 Z
```

And add grip at top: rect x=-5 y=-132 width=10 height=20 rx=3, amber. Actually let me make grip a bit longer, height=26.

Wait, the grip at the top of a hockey stick is where you hold it, so it's at the top. Yes, amber grip at top.

Now, let me reconsider: do I want the sticks to have the blade clearly at the bottom? With rotation, blades point down-ish. Good.

Let me write the final SVG.

Also, I realize I should double check the textPath direction issue by considering that many real badges work. I'll trust the pattern. If text appears upside down, it's a minor issue, but I believe with top arc (sweep 0, over the top) and bottom arc (sweep 1, over the bottom), both read upright. Let me double-check the top one.

Top arc: M 57 200 A 143 143 0 0 0 343 200. Wait, I need endpoints. Let me set endpoints at the same y as center for a clean semicircle: (200-143, 200)=(57,200) to (343,200). Sweep 0.

Hmm, but at endpoints y=200 is the center height, and the arc goes up to y=57 at top. Text "OWAYO" centered (startOffset 50%) sits at the top. The path direction: from (57,200) going counterclockwise (sweep 0) to (343,200). Starting at left point (57,200), counterclockwise means... in SVG with y-down, sweep 0 is the negative angle direction. From left point, going "up first" reaches the top. So path goes (57,200) → up → (200,57) top → down → (343,200). Direction of travel at top is left-to-right (from the left side coming over the top to the right side). At the topmost point, travel direction is +x (right). Text baseline along path, text extends to the left of travel direction... 

In SVG, text on a path is placed so that it's upright relative to the path, with the text appearing on the LEFT side of the path direction (when walking along the path, text is on your left). Wait, actually text is placed on the left side of the path when moving in the path direction? Let me recall: "Text is placed on the left side of the path" — no. Let me think. When you walk along the path in its direction, the text is on your LEFT. Hmm, or is it that text baseline is on the path and text rises to the left of the direction of motion.

If walking right (+x) along the top, "left" is +y (downward in screen). So text would be BELOW the path at the top. That means text extends from the path (at top, y=57) DOWNWARD toward center. So top text is between y=57 and y=57+30=87. That's inward (toward center). 

Wait, "left of direction of motion": moving in +x direction, your left hand points toward +y (down) in screen coords (since y increases downward). So text is below the path. At the top of the circle, "below" = toward center = inward. So top text extends inward. Good, that keeps it inside the ring.

Hmm wait, that doesn't sound right. Let me reconsider. If text is below the path at the top of the circle, the text would be between the top arc and the center, i.e., in the upper-middle area, reading left-to-right, upright. That looks correct for an arched top text! Yes. Like "OWAYO" arched at top, upright, sitting just inside the top arc. 

Now bottom arc: M 57 200 A 143 143 0 0 1 343 200. Sweep 1. From (57,200) left point, sweep 1 (clockwise, positive angle) goes DOWN first to bottom. Path: (57,200) → down → (200,343) bottom → up → (343,200). At bottommost point, travel direction is +x (right). Text on left of motion = +y = down = away from center = outward. So bottom text extends outward (below the path, toward badge edge). 

Hmm, that means bottom text is BELOW the bottom arc, i.e., between the arc (y=343) and the badge edge (y=380). That's outside the inner ring region... wait the bottom arc is at radius 143 (y=343). Extending outward means toward radius 143+30=173, toward the badge edge (180). So bottom text is between radius 143 and 173, near the bottom. And it would be upright (reading left to right). 

But wait, that places bottom text BELOW the arc line, near the badge edge. And top text is INSIDE the arc (between arc and center). That's asymmetric but both are upright and readable. Actually, hmm, for a badge you usually want both texts inside their arcs. Let me reconsider.

Actually, for bottom text, I think I want it to extend inward (toward center), like the top. Let me flip the bottom arc direction so text extends inward.

For bottom text to extend inward (upward, toward center), at the bottom point text should be ABOVE the path. Text is above the path when it's on the RIGHT of the direction of motion. At bottom, to have text above (toward center, -y), I need direction of motion such that right is -y (up). Right of motion = -y means motion is... if right is up (-y), then forward is +x rotated... right = forward rotated -90°? Let me just choose the arc direction.

If I draw the bottom arc from RIGHT to LEFT (343,200) to (57,200) through the bottom, then at the bottommost point travel direction is -x (left). Text on left of motion (-x direction): left of -x is... moving in -x, left hand points to -y (up). So text is above the path (toward center, inward). 

So for bottom text inward: path from right to left through bottom.
Bottom arc: M 343 200 A 143 143 0 0 1 57 200. Let me verify: from (343,200) right point, to (57,200) left point, sweep 1 (clockwise). From right point, clockwise goes... down then left. (343,200) → down → (200,343) → up → (57,200). Yes, through the bottom. Direction at bottom is -x (leftward). Text on left = up = inward. 

So:
- Top arc: M 57 200 A 143 143 0 0 0 343 200 → text inward (downward at top). Upright. ✓
- Bottom arc: M 343 200 A 143 143 0 0 1 57 200 → text inward (upward at bottom). Upright. ✓

Wait, let me double check top arc direction and text side again, because I want to be consistent.

Top arc: M 57 200 A 143 143 0 0 0 343 200. From (57,200) left, sweep 0. Sweep 0 = counterclockwise (negative angle). From left point (57,200), counterclockwise... Let me think in standard math (y-up) then flip. In standard math, left point is at angle 180°. Counterclockwise (increasing angle) from 180° goes to 270° which in standard math is down, but in screen (y-down) 270° standard = up. Hmm I'm confusing myself.

Let me just directly reason about SVG. SVG sweep-flag=1 means the arc is drawn in the "positive angle" direction, which in SVG's coordinate system (y-down) appears as CLOCKWISE on screen. sweep-flag=0 appears COUNTERCLOCKWISE on screen.

Top arc, sweep 0 = counterclockwise on screen. Start (57,200) is at the 9 o'clock position (left). Counterclockwise on screen from 9 o'clock: 9 → 12 → 3 (counterclockwise is 9→12→3? No). Counterclockwise on screen (visually): 12→9→6→3→12 is clockwise? Let me define: clockwise on screen is 12→3→6→9→12. Counterclockwise is 12→9→6→3→12.

Start at 9 o'clock (left, 57,200). Counterclockwise (12→9→6→3): from 9, counterclockwise goes to 6 o'clock? No. Counterclockwise sequence: 12, 9, 6, 3, 12. So from 9, next counterclockwise is 6 (bottom). That would put the arc at the bottom, not top!

Hmm, that contradicts what I said. Let me re-examine.

Counterclockwise on screen: starting at 12 (top), going counterclockwise means going to the LEFT, i.e., 12 → 9 → 6 → 3. Wait, 12 to 9 is going left (counterclockwise), 9 to 6 is going down-left to bottom. So counterclockwise: 12→9→6→3→12. 

From 9 o'clock, counterclockwise continues to 6 o'clock (bottom). So top arc with sweep 0 from left point goes to the BOTTOM. That's wrong for a top arc!

So I had it backwards. Let me redo.

Top arc (over the top) from left point (57,200) to right point (343,200): to go over the TOP (12 o'clock), from 9 o'clock I need to go to 12 then to 3. That's 9→12→3, which is CLOCKWISE (12→3→6→9 is clockwise, so 9→12 is reverse of that = counterclockwise? no).

Clockwise: 12→3→6→9→12. So 9→12 is going backward = counterclockwise. Hmm. 9→12→3: 9 to 12 is counterclockwise (against clockwise), 12 to 3 is clockwise. Contradiction—it can't be both.

Let me very carefully define. On a clock, clockwise is 12→1→2→3→...→12. So the order clockwise: 12, 1, 2, 3 (right), 6 (bottom), 9 (left), 12.

Starting at 9 (left), moving clockwise: 9→10→11→12→1→2→3(right). So clockwise from 9 goes UP to 12 then to 3. 

So top arc from 9 o'clock over the top (12) to 3 o'clock (right) is CLOCKWISE. Sweep-flag=1.

So top arc: M 57 200 A 143 143 0 0 1 343 200 (sweep 1).

Let me redo bottom arc. Bottom arc from left (9 o'clock) to right (3 o'clock) over the bottom (6 o'clock). From 9, going to 6 (bottom) to 3. Clockwise from 9 is 9→12→3 (up). Counterclockwise from 9 is 9→6→3 (down through bottom). So bottom arc over the bottom is COUNTERCLOCKWISE = sweep 0.

Bottom arc: M 57 200 A 143 143 0 0 0 343 200 (sweep 0).

OK so I had them swapped. Let me correct:
- Top arc: sweep 1. M 57 200 A 143 143 0 0 1 343 200
- Bottom arc: sweep 0. M 57 200 A 143 143 0 0 0 343 200

Now text direction and side:

Top arc, sweep 1 (clockwise), from left (57,200) over top to right (343,200). At the top (12 o'clock), the direction of travel (clockwise) is from left to right, i.e., +x (rightward). Text on the LEFT of travel direction: moving right (+x), left is +y (downward on screen). So text is BELOW the path at the top = inward (toward center). Good, top text extends inward. Upright. ✓

Bottom arc, sweep 0 (counterclockwise), from left (57,200) over bottom to right (343,200). At the bottom (6 o'clock), direction of travel (counterclockwise): counterclockwise is 12→9→6→3, so at 6 o'clock moving toward 3 o'clock, direction is +x? At 6 o'clock, counterclockwise motion goes toward 3 o'clock (right), so direction is +x (rightward)... wait. Counterclockwise: 12→9→6→3→12. At 6 o'clock, the motion is FROM 6 toward 3, i.e., from bottom to right, so at 6 o'clock the tangent direction is up-and-right, predominantly +x (rightward) as it leaves 6 toward 3. Hmm, at exactly 6 o'clock, moving toward 3 (which is up-right), the tangent is +x (rightward)? At 6 o'clock position, tangent to circle: the circle's tangent at bottom is horizontal. Moving counterclockwise (toward 3 o'clock = right), the direction at 6 o'clock is +x (right). Yes.

Text on left of +x motion = +y = down = outward (away from center). So bottom text extends outward (below the bottom arc, toward badge edge). 

Hmm, so bottom text extends outward, top text inward. Asymmetric. For a badge, typically both texts are inside the ring, between the ring and the center. Top text inward is good. Bottom text outward would be near the edge, possibly overlapping the ring.

I want bottom text to also extend inward. To achieve that, I should reverse the bottom arc direction (draw from right to left). Let me do:
Bottom arc: M 343 200 A 143 143 0 0 1 57 200. This goes from right, over the bottom, to left. Direction at 6 o'clock: from 3 toward 6 toward 9, so at 6 o'clock moving toward 9 (left), direction is -x (leftward). Text on left of -x motion: left of -x is -y (up) = inward. So bottom text extends inward. 

But I need to check the sweep flag for right-to-left over bottom. From (343,200) right point to (57,200) left point over the bottom (6 o'clock). Clockwise from 3 o'clock: 3→6→9, yes over the bottom to 9 (left). So clockwise = sweep 1.
Bottom arc: M 343 200 A 143 143 0 0 1 57 200.

And top text: I want it inward too, which I found with sweep 1 left-to-right. Let me keep top as left-to-right sweep 1. But let me double check top text extends inward (it did). And it reads left-to-right, upright. Good.

Hmm, but actually, do I even need both to be inward? Let me reconsider. Many badges have top text arched over the top (reading along the curve, upright) and bottom text arched under the bottom (reading along the curve, upright). Both readable. The top text sits just inside the top arc, bottom text just inside the bottom arc. "Inside" means toward center for both. So yes, I want both inward.

Top text inward: top arc left-to-right, sweep 1. ✓ (text below path at top = inward)
Bottom text inward: bottom arc right-to-left, sweep 1. ✓ (text above path at bottom = inward)

Wait, let me re-examine bottom arc right-to-left sweep 1. From right (343,200) to left (57,200), sweep 1 (clockwise). Clockwise from 3 o'clock: 3→6→9, over the bottom to 9 (left). Yes. Direction at 6 o'clock: moving from 3 toward 9 via 6, at 6 o'clock heading toward 9 (left), direction is -x (leftward). Text on left of -x = -y (up) = inward. ✓. And text reads in travel direction (right to left along the path = the text goes from right to left?). 

Wait, if the path goes from right to left, then text placed on it starts at the right and goes left. With text-anchor middle and startOffset 50%, the text is centered. But the reading order: textPath places characters in the path direction. If path goes right-to-left, characters are placed right-to-left, meaning the FIRST character is at the right. For "EULERS" that would read E-U-L-E-R-S from right to left = backwards! That's wrong.

Hmm. So for the bottom text to read correctly (left to right), the path should go left to right, OR I mirror.

Let me reconsider. For bottom text reading left-to-right (normal), the path direction at the text should be left-to-right (+x). And for text to be inward (up), text should be above the path. Text above path means text is on the right of travel direction (if moving +x, right is -y = up). Wait: moving +x (right), your right hand points to -y (up) in screen coords. So text on the RIGHT of motion is above (inward at bottom). 

So I need: at bottom, motion is +x (rightward) AND text on right of motion (so text is up/inward). 

Motion +x at bottom means going from left to right through the bottom: from (57,200) over bottom to (343,200). That's counterclockwise (sweep 0) as established. Direction at 6 o'clock: counterclockwise 12→9→6→3, at 6 o'clock heading toward 3 (right), direction +x. ✓. Text on right of +x motion = -y = up = inward. ✓. And reading direction is +x = left to right = normal reading. ✓✓✓.

So bottom arc: M 57 200 A 143 143 0 0 0 343 200 (sweep 0, left to right over bottom). Text reads left-to-right, extends inward. 

Let me re-examine my earlier confusion. Earlier I said bottom arc sweep 0 from left goes counterclockwise to bottom then right, direction at bottom is +x, text on right = inward. Let me recheck "text on right of motion."

SVG text on path: the text is positioned with its baseline on the path, and the text extends to the... I need to get this right. Let me recall precisely.

From SVG spec: "The text is placed so that it sits on the path, in the direction of the path." The baseline is on the path. The text is drawn on the LEFT side of the path when traveling in the direction of the path? Or right?

I recall that text is placed on the left side of the path. Let me verify with a simple example: a horizontal path going left to right (direction +x). If text is on the left of the path, and left of +x is +y (down), then text would be BELOW the path. But we know normally text sits ABOVE its baseline. Contradiction. So text must be on the RIGHT of the path (right of +x = -y = up = above baseline). 

Yes! Text is on the RIGHT side of the path direction. (This matches: baseline on path, text rises above, which is to the right of rightward motion.)

OK so text is on the RIGHT of the direction of travel.

Top arc: left to right over top, sweep 1. At top, direction +x (rightward). Text on right of +x = -y = up. At the top of the circle, "up" is AWAY from center (outward). So top text extends OUTWARD (above the top arc, toward badge edge). Hmm.

Wait, that contradicts what I want. Let me recompute. Top of circle is at (200, 57) for r=143. Away from center = up = toward (200, 0) = toward badge top edge. So text above the path = outward. So top text would be between the top arc (y=57) and the badge edge (y=20ish). That's outside the arc, near the top edge.

Hmm, so top text extends outward. And for bottom text, left to right over bottom, sweep 0, at bottom direction +x, text on right = -y = up = toward center (inward, since bottom, up is toward center). So bottom text extends inward.

So with these: top text outward (near top edge), bottom text inward (near center). That's inconsistent and bottom text might collide with the owl.

I think I need to reconsider. Let me reconsider what "inward/outward" means and what looks good.

For a badge, I want:
- Top text: arched along the top, readable, sitting just INSIDE the top ring (between ring and center). So top text should be BELOW the top arc (inward).
- Bottom text: arched along the bottom, readable, sitting just INSIDE the bottom ring. So bottom text should be ABOVE the bottom arc (inward, toward center).

Top text just inside top arc = below the arc (arc at top, text below it). 
Bottom text just inside bottom arc = above the arc (arc at bottom, text above it).

So:
- Top text: below the top arc. Path is the top arc. Text should be below path. Text is on right of motion. For text to be below path at top, "below" (+y) should be the right of motion. Right of motion = +y means motion is -x... no. Right of motion: if motion is +x, right is -y (up). If motion is -x, right is +y (down). For text below (+y) at top, need right of motion = +y, so motion = -x (leftward). So top arc should be drawn right-to-left (from 3 o'clock over top to 9 o'clock). Direction at top = -x (leftward). Text on right = +y = down = below arc = inward. ✓. But reading direction: path right-to-left, so text reads right-to-left = BACKWARDS. ✗.

Argh, the reading direction conflicts with placement.

The resolution: use text-anchor="middle" and startOffset="50%". This centers the text on the path regardless of direction, BUT the reading order is still determined by path direction. If path is right-to-left, "EULERS" would be placed E first at the rightmost, reading right-to-left = backwards.

Wait, is that true? Let me reconsider. With text-anchor middle and startOffset 50%, the center of the text is at 50% of the path. The text extends equally on both sides. The characters are still placed in path order. So if path goes right-to-left, the first char E is at the center going right... no.

Hmm, let me think. textPath places the text's start at startOffset along the path, and subsequent characters follow the path. With startOffset 50% and text-anchor middle, the text is centered such that its middle is at 50%. The characters before the middle are placed toward the path start (0%), and characters after toward path end (100%).

If path is right-to-left (start at right, end at left), then 0% is at right, 100% at left. The text's first character (E) is at the start side. With center at 50%, E is placed toward 0% (right) side? Let me see: text "EULERS", center between L and E (positions 3-4). The first half "EUL" is placed from 50% toward 0% (rightward), the second half "ERS" from 50% toward 100% (leftward). So reading from 0% to 100% (right to left): E,U,L,E,R,S. So from right to left it reads EULERS, meaning from left to right it reads SRELU E = backwards. So yes, it reads backwards. ✗.

So to read correctly left-to-right, the path must go left-to-right (0% at left, 100% at right), so that E is at left.

Therefore:
- Top text: path left-to-right over top. Direction at top = +x. Text on right of +x = -y = up = outward. So top text is OUTWARD (above top arc).
- Bottom text: path left-to-right over bottom. Direction at bottom = +x. Text on right = -y = up = inward (toward center at bottom). So bottom text is INWARD (above bottom arc).

So top text is above the top arc (outward, near top edge) and bottom text is below... no, above the bottom arc (inward, near center).

So top text sits between the top arc and the top badge edge. Bottom text sits between the bottom arc and the center. This is asymmetric but let me check if it looks OK.

Actually, you know, this is the natural behavior and it does look fine on many badges! The top text arches over the top just inside the outer ring (between ring and center — wait, outward means toward the ring, so between the arc and the ring). Hmm.

Let me reconsider. If top text is "outward" (above the top arc), and the top arc is at r=143, then top text is between r=143 and r=143+15=158. The inner ring is at r=156. So top text would be between r=143 and 158, overlapping the inner ring at 156. Bad.

Alternatively, I should place the arcs closer to the center so text fits between arc and ring.

Let me reconsider the whole thing. Maybe simpler: put both arcs and let text be on the inside of each arc, which means:
- Top arc at larger radius, text inside it (below).
- Bottom arc at larger radius, text inside it (above).

For text to be inside (inward) for both, with left-to-right reading:
- Top: left-to-right path, text on right of motion = outward. To get inward, reverse... can't without reversing reading.

So it's fundamentally: left-to-right reading + text-on-right-of-path means:
- At top: text outward.
- At bottom: text inward.

There's no way around it with standard textPath. So either:
(a) Top text is outward (near top ring), bottom text inward (near center). Asymmetric.
(b) Accept top text outward and position rings accordingly.

Actually, many real sports badges DO have this exact layout: top text along the top arch (sitting just inside the outer ring at the top), and bottom text along the bottom arch (sitting just inside the outer ring at the bottom). Let me reconsider whether bottom text with left-to-right over-bottom path is inward or near the bottom ring.

Bottom arc at r=143 (bottom point y=343). Bottom text inward = above the arc = from y=343 up to y=343-15=328 = radius 143 down to 128. So bottom text is between r=128 and 143, near the bottom but inward from the arc. The inner ring at r=156 is outside this. So bottom text is well inside. Good, no overlap with ring. But it's also not right against the ring.

Top arc at r=143 (top point y=57). Top text outward = above the arc = from y=57 up to y=57-15=42 = radius 143 up to 128. So top text is between r=128 and 143 (measuring from center, the text spans radius 128 to 143 at the top). Wait, "above the arc" at the top means toward smaller y, which is toward larger radius? No. At the top, center is at y=200. Smaller y = farther from center = larger radius. y=57 is radius 143. y=42 is radius 158. So top text spans radius 143 to 158. The inner ring at 156 overlaps. Bad.

So the issue is top text extends outward toward the ring. To avoid, I move the top arc inward (smaller radius) so there's room between the arc and the ring for the text.

Let me set:
- Inner ring (amber) at r=158.
- Top arc at r=130. Top text spans r=130 to 145. Ring at 158. Gap. Good.
- Bottom arc at r=130. Bottom text spans r=115 to 130. Good.

Wait, but then the arcs are at r=130 and text between 115-145, all inside ring 158. And the owl should be inside r=130 too. Let me make sure owl fits inside r=130. Owl widest: head at (146-254, 160), the corners... actually owl extent: let me compute the owl's bounding radius. Owl body bottom at y=310 (radius 110 from center, since 310-200=110). Owl head sides at x=146 and 254, y=160: radius sqrt(54^2+40^2)=67. Tufts at (150,92): radius sqrt(50^2+108^2)=119. So owl max radius ~119 (tufts). Text at r=130-145. So text is outside owl. Good, no overlap. And owl (max 119) is inside text arcs (min 130). Good.

Hmm, but tufts at radius 119 and text at 130 — close but OK. Let me make sure. Actually the tufts are at the top (y=92), and top text is at the top too (around y=42-57). The tufts at (150,92) radius 119, top text at radius 130-145 near top. They're at similar angles (top) but different radii (119 vs 130+). Small gap. OK.

Actually, let me reconsider and simplify by making the owl smaller and giving clear margins. But I think it'll be fine.

Let me also reconsider: maybe I'm overcomplicating the text. Let me just place top and bottom text and ensure no overlaps with generous margins. Let me finalize:

- Outer ring: r=180, w=9, navy. (covers 175.5-184.5)

Hmm wait, stroke is centered on the circle, so r=180 w=9 covers radius 175.5 to 184.5.

- Inner ring: r=158, w=3, amber. (covers 156.5-159.5)
- Top text: baseline r=132, font 27. Extends outward (right of motion at top = up = toward larger radius) from 132 to ~147. Wait, but I want it between arc and ring. If baseline at 132 and extends outward to 147, and ring at 156.5, gap 147-156. OK. But actually I realize the top text extending outward means it goes toward the ring, so baseline should be at smaller radius. Let me put top text baseline at r=128, extending to ~143. Ring at 156.5. Gap. Good.

Hmm, but actually, let me reconsider whether top text goes outward or inward one more time, because I keep flip-flopping.

Definitive check with concrete tiny example:
- Path: horizontal line from (0,0) to (100,0). Direction +x.
- Text "ABC" on this path. Where does it appear? Above or below the line?

By all real-world experience and SVG behavior, text on a path from (0,0) to (100,0) appears ABOVE the line (at negative y, i.e., y<0). Because the baseline is on the line and text rises upward.

Text is on the right of the direction of travel? Direction +x, right is -y (up). Text at -y (up) = above. ✓. So text is on the right of travel direction. Confirmed.

Now top arc, drawn left-to-right (from (57,200) to (343,200) over the top). At the topmost point (200,57), the path is momentarily horizontal, direction of travel is +x (moving from left to right). Text on right of +x = -y direction = up = toward (200, 0) = away from center (outward). So text is ABOVE the top arc = outward. Confirmed: top text is outward.

Bottom arc, drawn left-to-right (from (57,200) to (343,200) over the bottom). At bottommost (200,343), path horizontal, direction +x. Text on right = -y = up = toward (200,200) = toward center (inward). So text is ABOVE the bottom arc = inward (toward center). Confirmed.

So:
- Top text: outward (between top arc and top ring).
- Bottom text: inward (between bottom arc and center).

To make both look balanced, I'll place top arc and bottom arc at the same radius, and the text will naturally be: top text in the band between arc and ring (outward), bottom text in the band between arc and center (inward). This is actually a common and acceptable badge layout! The top text hugs the top ring, bottom text sits above the center. Wait, that's asymmetric though.

Hmm, let me reconsider. Actually, maybe I should place the arcs such that text is inward for both, by making the arcs the OUTERMOST text guide and putting text just inside.

For top text just inside top ring: text should be below the top ring, i.e., inward from the top. If I put the top arc AT the ring radius and text outward, text would be outside the ring (off the badge). Bad. So I need text inward from the arc. But we established top text is outward from the arc. So the arc must be INSIDE (smaller radius) than where I want the text, and the ring even further out.

So: ring at r=180, text band at r=150-168, top arc at r=138 (text outward from 138 to ~153... no).

I think I'm overcomplicating. Let me just place:
- Top text baseline at r=148, and it extends outward to ~163. Put inner ring at r=170. Gap 163-170. Top text between arc... 

Ugh. OK let me step back and think about it differently.

Simplest robust approach: Put the text on arcs, place arcs at a radius where the text fits nicely between the arc and either the ring or center, and just make sure nothing overlaps. Since top text goes outward from its arc and bottom text goes inward from its arc, I'll:

- Put top arc at radius R_top. Top text occupies [R_top, R_top+16].
- Put bottom arc at radius R_bottom. Bottom text occupies [R_bottom-16, R_bottom].
- Put inner ring at radius R_ring > R_top+16 (so top text is inside ring).
- Ensure bottom text [R_bottom-16, R_bottom] doesn't overlap owl.

Let me choose:
- R_ring = 168 (inner amber ring).
- R_top = 150. Top text [150, 166]. Inside ring 168. Gap 166-168 tiny. Let me use R_top=148, text [148,164], ring 168. Gap 164-168. OK.
- R_bottom = 150. Bottom text [134, 150]. Owl max radius ~119. Gap 134-119... wait owl max is 119, bottom text min 134. Gap 119-134. Good, no overlap.

Wait, but top text [148,164] and bottom text [134,150] — top text is closer to the ring, bottom text is closer to center. Asymmetric but both within badge. Actually, hmm, for visual balance, having top text hug the ring and bottom text float more toward center looks a bit off. But it's acceptable.

Alternatively, I can flip the top text to go inward by reversing the arc and using a mirror... no, reading direction.

Actually, let me reconsider. What if I make BOTH texts read correctly and be inward by using arcs that are the "inner boundary" and text between arc and center for BOTH? 

For top text to be inward (below the arc, toward center) AND read left-to-right: we need text on the right of motion to be inward (downward at top = toward center). At the top, inward = downward = +y. Text on right of motion = +y means motion is -x (leftward). So top arc should be drawn right-to-left. But then reading is right-to-left = backwards.

Unless... I use text-anchor and the fact that with a symmetric arc and centered text, reversing the path direction just reverses character order. There's no way to read correctly while being inward at the top with standard textPath.

CONCLUSION: With standard SVG textPath, top arched text that reads left-to-right will be outward (near ring), and bottom arched text that reads left-to-right will be inward (near center). This is the natural behavior. Many badges actually look fine with this. But to make it look balanced, I'll position the arcs so both texts are in a nice band.

Actually, wait. Let me reconsider. There's a common trick: for the BOTTOM text to appear along the bottom reading left-to-right and be near the bottom ring (outward), you draw the bottom arc right-to-left. But that makes it read backwards... 

No. Let me reconsider the actual common badge. In a typical badge like "STAR WARS" or sports logos:
- Top text: reads left-to-right, arched over the top. It's inside the ring.
- Bottom text: reads left-to-right, arched under the bottom. It's inside the ring (near the bottom ring).

For bottom text to be near the bottom ring (outward from center) and read left-to-right... Let me reconsider. If bottom text is near the bottom ring, it's at large radius (near 180). Reading left-to-right. For it to be on the outside of the bottom arc... 

Hmm, let me reconsider by thinking about a real example. Consider a badge where bottom text "EST. 1990" is at the bottom, curving up at the ends, reading left-to-right, sitting just inside the bottom of the outer ring. The text's baseline curves, with the middle of the text at the bottom. The text is ABOVE its baseline? No—at the bottom, the text is above the baseline means toward center. But it's near the ring...

I think the confusion is: near the bottom ring doesn't mean large radius for the text baseline. The text near the bottom ring has its baseline at large radius (near the ring) and the text extends inward (toward center, above baseline). So bottom text: baseline near ring (large radius), text extends inward. That's "inward from the arc" where the arc is near the ring.

So for bottom text near the bottom ring: bottom arc (baseline) at large radius ~165, text extends inward to ~150. Ring at 175. Gap. 

For this, bottom arc at r=165, drawn left-to-right over the bottom. Text on right of +x motion at bottom = inward (toward center). So text from r=165 inward to r=150. ✓. And reads left-to-right. ✓.

So bottom text near the ring: bottom arc at large radius (near ring), text inward.

Top text near the top ring: top arc at large radius (near ring), text... outward = toward ring = outside the ring. Bad. OR text inward.

For top text near top ring with text inward (below arc): as established, requires right-to-left path = backwards reading.

So top text near the top ring CANNOT have text inward with correct reading. Therefore top text near the top ring has text OUTWARD (above arc), which is outside the ring. That doesn't work either.

Wait, I think I have the top text direction of text-side wrong. Let me re-examine VERY carefully with the concrete example, because everything hinges on this.

Concrete: path from (0,0) to (100,0) (horizontal, direction +x). Place text "ABC". 

I'm confident from experience that "ABC" appears ABOVE the line (in negative-y, i.e., y < 0). Let me just trust this.

Now, "above the line" for a line at y=0 is y<0. In terms of the path direction +x, the region y<0 is to the... if I face +x (right), y<0 is to my LEFT (my left hand points up = -y). Wait: facing +x (east), my left hand points north (-y in screen, up), right hand points south (+y, down). So y<0 (up) is to my LEFT.

So text above the line (y<0) is to the LEFT of the direction of travel?! That contradicts my earlier "text is on the right."

Let me recompute. Facing +x (east, rightward). North is up (-y in screen since screen y is down... wait, in screen coords, up is -y). North = up = -y. If I face east (+x), north is to my LEFT. So up (-y) is to my left. Text at y<0 (up) is to the left of travel direction.

So text is on the LEFT of the direction of travel, not right! I made an error before.

Let me redo. Text is on the LEFT of the direction of travel.

Hmm, wait, let me double-check with the concrete example once more. Path (0,0)→(100,0). Text appears above (y<0). Direction +x. Above (y<0) relative to +x direction: facing +x, left is -y (up). So text is on the left. ✓. 

So text is on the LEFT of the direction of travel. I had it backwards. Let me redo the badge.

Top arc, left-to-right over top (sweep 1). At top, direction +x. Text on left of +x = -y = up = outward (away from center). So top text OUTWARD. Same conclusion as before (outward).

Wait, that's the same as before. Let me recompute the "left" direction. Facing +x, left is -y (up). Text on left = up = -y. At the top of circle, -y (up) = away from center = outward. So top text outward. ✓ (same as before).

Bottom arc, left-to-right over bottom (sweep 0). At bottom, direction +x. Text on left of +x = -y = up. At the bottom, up = toward center = inward. So bottom text inward. ✓ (same as before).

OK so regardless of left/right confusion, the conclusions are:
- Top text: outward (near top ring).
- Bottom text: inward (near center).

Wait, but that gives bottom text near the center, which might overlap the owl. And top text near the ring.

Hold on, let me reconsider the concrete example direction of "left" once more, because I want to be 100% sure, as it flips everything.

SVG coordinate system: x right, y DOWN. A path from (0,0) to (100,0) goes in +x direction (to the right). 

SVG text on path: I'll reason from the spec/behavior. The text is rendered with its baseline on the path and the text extending perpendicular to the path. The direction it extends is determined by... 

From MDN: "textPath ... The text is placed on the path ... The text is drawn in the direction of the path, ... on the left side of the path." Hmm, actually I've seen both claims. Let me reason from first principles using the glyph orientation.

When you place text on a path, each glyph is oriented so that its baseline is tangent to the path and the glyph is upright relative to the path direction (the top of the glyph points to the left of the travel direction, I believe). 

Actually, the standard behavior: imagine walking along the path. The text is on your left, and you're walking forward; the text is upright relative to you (the top of letters points forward-left...). 

Hmm, let me just think about a path that curves. Consider a path that is the bottom of a circle, going left to right (like a smile). Text on it reads left to right, and the text is above the curve (concave side), i.e., the text sits in the concave part of the smile, upright. For a smile (bottom of circle), the concave side is up (toward center). So text is above the curve = toward center = inward. And it reads left-to-right. This matches "bottom text inward."

For a path that is the top of a circle, going left to right (like a frown/bridge), text on it reads left to right, and sits above the curve. Above the "frown" curve is... the convex side (outside the circle). So text is outside the circle = outward. Matches "top text outward."

OK so I'm now confident:
- Top arched text (left-to-right): sits OUTSIDE the top arc (outward, near ring).
- Bottom arched text (left-to-right): sits INSIDE the bottom arc (inward, near center).

So for the badge:
- Top text near the top ring: place top arc at radius ~155, text extends outward to ~170, ring at ~178. Text between arc(155) and ring(178). Wait, text extends outward from arc, so from 155 to 170. Ring at 178. So text is between 155 and 170, inside the ring. But then the arc at 155 is below the text. Where's the arc visually? The arc is a decorative line at 155, text above it (outward) at 155-170, ring at 178. That means the decorative arc line is BELOW the top text. Hmm, usually the arc/decorative line is above the top text or the text follows it.

This is getting too complicated. Let me simplify the design to avoid curved text issues entirely, OR just use curved text and accept the natural layout with careful positioning.

DECISION: I'll use curved text but place the arcs as the path the text follows, and position everything so it looks good. Let me place:
- Top text: follows top arc, sits just inside the outer ring (I'll put the top arc close to the ring, text between arc and ring).

Since top text is outward from its arc, to have text between the arc and the ring, the arc must be at a smaller radius than the text, and the ring even larger. So: arc at 148, text 148-164, ring at 172. The arc line at 148 is below the text. Visually, the text arches and the decorative arc line is just below it. That's actually fine and common (the arc is like a underline for the text).

Hmm, but typically the arc is a full circle ring and the text is inside it. Let me reconsider.

Alternative clean approach: Make the outer ring the frame. Put text just inside the ring along the top and bottom. For the top, text just inside the ring at the top = text at radius ~168 (just inside ring 178), and text extends inward (downward) from there. For this, the text baseline is at 168 and text extends inward (toward center, downward at top). Text extends downward at top = +y. Text on left of motion = +y means motion is +x? Facing +x, left is -y (up). For text at +y (down), text is on the RIGHT of motion. But we said text is on the left. Contradiction. So text at top can't extend inward (downward) with left-to-right reading.

Therefore, top text with left-to-right reading MUST extend outward (upward) from its baseline. So if I want top text just inside the ring, the baseline is at ~168 and text extends outward to ~183, which is OUTSIDE the ring (178). Bad.

So top text CANNOT be "just inside the ring extending inward." It must be "baseline somewhere, extending outward."

For top text to be inside the badge (not outside the ring) and extend outward, the baseline must be at a radius such that baseline+text-height < ring-radius. E.g., baseline at 150, text to 166, ring at 175. Text is between 150 and 166, inside ring. The baseline arc at 150 is below the text. So there's a decorative arc at 150 (below text), text at 150-166, ring at 175. This looks like: text arches at top, with a line just below it, and the outer ring. Acceptable.

Alternatively, NO decorative arc line for the text; just the text following an invisible path, and the ring framing. That's cleaner. Let me do that: the textPath uses an arc path that's not drawn (or drawn as a subtle line), and the main badge ring frames it.

Let me finalize:
- Outer ring: r=178, w=8, navy. (covers 174-182)

Hmm, let me use r=180, w=10 → covers 175-185.

- Inner decorative ring: r=150, w=2, amber. (covers 149-151)
- Top text: baseline arc at r=138, font 26, white. Text extends outward to ~153. Hmm, that crosses the inner ring at 150. Let me put top text baseline at r=130, text to 146, inner ring at 150. Gap 146-150. OK.

Wait, but then inner ring at 150 is above the top text (130-146)? Inner ring at 150, top text 130-146. So inner ring (150) is just above top text (max 146). And inner ring is a full circle at 150. The top text (130-146) is inside the inner ring. The bottom text (inward from its arc) — let me place bottom arc at r=138, text inward to 122. So bottom text 122-138, inside inner ring 150. Good.

Owl max radius ~119. Bottom text min 122. Gap. Good.

Hmm, wait, let me recompute. Let me lay out radii from center:
- 0-119: owl area (owl max radius ~119 at tufts)

Wait, that's a big owl. Let me reconsider owl size. If owl max radius is 119, the owl is quite large. Let me make owl max radius ~110.

- 110: owl extent (body bottom at y=310, radius 110; tufts at radius ~110)
- 122-138: bottom text band
- 150: inner amber ring
- 130-146: top text band
- 175-185: outer navy ring

Wait, top text band 130-146 and inner ring at 150 and bottom text 122-138. Let me order by radius:
- 110: owl
- 122-138: bottom text
- 130-146: top text
- 150: inner ring
- 175-185: outer ring

Top text (130-146) and bottom text (122-138) overlap in radius range but they're at opposite ends of the circle (top vs bottom), so no actual collision. Good.

Inner ring at 150 is outside both text bands. Good.

Hmm, but top text 130-146 is close to inner ring 150 (gap 146-150=4px). And bottom text 122-138 is well inside. The asymmetry (top text near ring, bottom text far from ring) is due to the outward/inward behavior. 

To reduce asymmetry, I could put the inner ring LOWER (smaller radius) so it doesn't matter, or remove the inner decorative ring. Let me remove the inner decorative ring to simplify, OR keep it but place it where it doesn't create asymmetry issues.

Actually, the inner ring is a nice decorative element. Let me keep it but accept the layout. Or, let me place the inner ring at r=120 (inside the text) — no, that would overlap the owl.

Let me just remove the inner decorative ring and rely on the outer ring + text. Cleaner. Or keep a thin inner ring at a radius that works.

Hmm, let me reconsider. Actually, you know what, let me reconsider the entire text approach. This curved text is causing a lot of fuss. Let me just go with a cleaner design:

Option A: Curved text (top and bottom arcs) — looks like a real badge but I need to nail positioning.

Option B: Straight text. "OWAYO" on top line, "EULERS" on bottom line, or "OWAYO EULERS" as one line at the bottom. Plus the owl and sticks in the center. Simpler, cleaner, guaranteed to look good.

Let me go with a hybrid: curved top text "OWAYO" and curved bottom text "EULERS", but let me just carefully position and test. Actually, let me go with Option B-ish but with a slight arc for flair. 

Hmm, let me just commit to curved text and position carefully. I'll use:
- Outer ring r=180 (navy, w=10).
- Text arcs (not drawn): top baseline r=140, bottom baseline r=140.
- Font size 24, white, bold.
- Top text extends outward from 140 to ~155.
- Bottom text extends inward from 140 to ~125.
- Inner decorative ring r=165 (amber, w=3) — above top text (155<165), gap. And it's a full circle; bottom text (125-140) is inside it. Good.

Wait, inner ring at 165, top text up to 155, gap 155-165=10. Good. Bottom text 125-140, inside ring 165. Good.

Owl max radius: let me keep owl within radius ~115. Bottom text min 125. Gap 115-125=10. Good.

Let me set:
- Outer ring: r=180, w=10, navy #14345b.
- Inner ring: r=165, w=3, amber #e8960c.
- Top text: baseline r=140, font 24, white. (extends ~140-155)
- Bottom text: baseline r=140, font 24, white. (extends ~125-140)
- Owl: within radius ~115.

Wait, top text 140-155 and inner ring 165: gap 10. But actually I realize the top text extends outward (toward ring), so it's at 140-155, and the ring at 165 frames it. Good, top text sits between an invisible arc(140) and the ring(165). Nice.

Bottom text 125-140, and the owl at max 115. Good separation.

But there's asymmetry: top text hugs the ring (140-155, ring at 165), bottom text floats (125-140, with 115 owl below and 140 above). The bottom text is more toward the center. This asymmetry is inherent. It's OK, many badges look like this. Actually, let me reconsider—maybe make bottom text also hug a ring by adding the inner ring and putting bottom text just inside it. But bottom text extends inward from its baseline, so to hug the inner ring(165) from inside, baseline at 165, text inward to 150. Then bottom text 150-165. And top text... baseline 140, outward to 155. Now top text(140-155) and bottom text(150-165) both near the ring, symmetric-ish! And owl at 115, well inside.

Let me try:
- Inner ring: r=165.
- Bottom text: baseline r=165, extends inward to 150. So bottom text at radius 150-165, just inside the ring. 
- Top text: baseline r=140, extends outward to 155. Top text at 140-155.
- Outer ring: r=180.

Now both texts are near the ring (bottom text 150-165 just inside ring 165; top text 140-155, with ring at 165 above it). Top text is a bit further from the ring than bottom text. Slight asymmetry but OK.

Hmm, actually for the top text to also hug the ring, I'd want baseline at 165 extending outward to 180, but that hits the ring. Can't.

I think the inherent asymmetry is unavoidable with this method, and it's fine. Let me just go with:
- Top text: baseline r=148, font 24. Extends 148-162.
- Bottom text: baseline r=148, font 24. Extends 133-148.
- Inner ring: r=168, amber w=3.
- Outer ring: r=182, navy w=10.

Top text 148-162, ring 168: gap 162-168=6. Good.
Bottom text 133-148, inside ring 168. Owl 115. Gap 115-133=18. Good.

OK this works. Let me also make sure the top text doesn't collide with the owl tufts. Owl tufts at radius ~110 (top). Top text at 148-162 (top). Gap. Good.

Alright, I've spent enough on text. Let me also reconsider: maybe I should reduce font and increase radii for clarity. Let me use font 22 for "OWAYO" and "EULERS" to fit nicely.

"OWAYO" is 5 chars, "EULERS" is 6 chars. At font 22 bold, they should fit on the arcs.

Let me now also reconsider the stick length to fit within radius ~115-120 so they don't poke past the owl too much, or maybe they should poke out a bit for style. Let me have sticks cross behind the owl with handles pointing up-out and blades pointing down-out. Sticks from radius ~110 (near owl) extending to ~170. Let me make sticks span radius 110 to 175.

Actually, the sticks are behind the owl, so they mainly show at top (handles) and bottom (blades), sticking out from behind the owl. Let me make them span from radius ~30 (top, near top of badge) to radius ~110 (where they meet the owl). Wait, let me reconsider.

Let me place the crossed sticks so they form an X behind the owl, with the crossing at the owl's center (200,210), handles pointing up-and-out, blades pointing down-and-out.

Stick local: handle top at y=-130 (local), blade at y=+90 (local), centered at (200,210) (owl center, slightly below logo center because text is at top). Hmm, let me center the crossing at (200, 210).

Actually, let me keep crossing at logo center (200,200) for simplicity, and owl centered around (200, 215) slightly lower. Or just center everything at (200,200) and let owl be slightly asymmetric. Let me center owl at (200, 205) to leave room for top text.

Ugh, let me just finalize coordinates and write it. I'll adjust if needed.

Let me define everything relative to center (200,200) and use local coordinates where helpful.

STICKS (local coords, then rotate around 200,200):
Stick shape (pointing down, centered at origin):
```
M -4 -128
L 4 -128
L 4 88
L 15 90
L 15 108
L -16 108
L -15 90
L -4 88
Z
```
Handle top at y=-128, blade bottom at y=108. Length ~236.
Grip: rect x=-5 y=-128 width=10 height=22 rx=3, amber.

Stick 1: transform="rotate(16 200 200)"
Stick 2: transform="rotate(-16 200 200)"

After rotation, stick 1 handle top at (200,128) rotated 16°: 
dx = -128*sin(16°) = -128*0.2756 = -35.3, dy = -128*cos(16°) = -128*0.9613 = -123. So handle top ≈ (164.7, 76.7).
Blade bottom at (200,308) rotated 16°:
dx = 108*sin16 = 29.8, dy=108*cos16=103.8. Blade ≈ (229.8, 303.8).

So stick 1 from (165,77) to (230,304). 
Stick 2 (rotate -16°): handle top (235,77), blade (170,304).
They cross at (200,200). Good.

Stick tip radii: handle top (165,77): radius sqrt(35^2+123^2)=sqrt(1225+15129)=sqrt(16354)=128. Blade (230,304): radius sqrt(30^2+104^2)=sqrt(900+10816)=sqrt(11716)=108. So sticks span radius 108-128. Inside the badge (ring 180) and behind owl (owl ~115). The handles (radius 128) poke out slightly past owl (115) at the top. Blades (radius 108) are behind owl. Good, looks like sticks crossing behind owl with handles sticking up.

Hmm, handles at radius 128 vs owl 115 — handles poke out 13px past owl. Fine.

Actually, wait, I want the sticks to be visible. With the owl in front, the sticks are mostly hidden except handles (top) and blades (bottom). That's the classic look. Good.

OWL (centered ~200,205):
Let me shift owl down slightly to center around (200,210) to balance with top text.

- Ears:
  - Left: M 162 128 L 150 98 L 184 120 Z
  - Right: M 238 128 L 250 98 L 216 120 Z
- Head: circle cx=200 cy=160 r=56
- Eyes white: cx=173 cy=162 r=25; cx=227 cy=162 r=25
- Pupils: cx=175 cy=164 r=12; cx=225 cy=164 r=12
- Highlights: cx=171 cy=159 r=4.5; cx=221 cy=159 r=4.5
- Beak: M 191 182 L 209 182 L 200 200 Z
- Body: ellipse cx=200 cy=245 rx=64 ry=68
- Wings:
  - Left: M 139 215 Q 118 255 141 298 Q 159 278 156 226 Z
  - Right: M 261 215 Q 282 255 259 298 Q 241 278 244 226 Z
- Belly: ellipse cx=200 cy=258 rx=42 ry=50
- Belly feathers: 3 arcs

Let me check owl extent:
- Head top: cy=160-56=104. Ears up to y=98.
- Body bottom: cy=245+68=313.
- Head sides: x=144 to 256.
- Wings: left to x=118, right to x=282.

Wings at x=118 and 282: radius from center (200,205)... let me use center (200,205) for radius. Wing tip (118, 255): radius sqrt(82^2+50^2)=sqrt(6724+2500)=sqrt(9224)=96. Wing (118,215): sqrt(82^2+10^2)=83. So wings max radius ~96. 

Body bottom (200,313): radius 108 (from center 205). 
Head sides (144,160): radius sqrt(56^2+45^2)=sqrt(3136+2025)=sqrt(5161)=72.
Ears (150,98): radius sqrt(50^2+107^2)=sqrt(2500+11449)=sqrt(13949)=118.

So owl max radius ~118 (ears). That's close to stick handles (128) and bottom text (133). Let me make owl a bit smaller or accept. Ears at 118, bottom text min 133: gap 15. OK. Ears at 118, stick handles 128: ears are inside handles. OK.

Hmm, ears at radius 118 is quite high (near the top text at 148). Gap 148-118=30. OK.

Let me reduce owl slightly to be safe. Actually, let me keep it; 30px gap is fine.

Wait, I should double-check the owl doesn't overlap the bottom text. Bottom text is at the bottom (radius 133-143, around y=343-353). Owl body bottom at y=313 (radius 108 from center 205). Gap 313 to 333 (bottom text top). Good.

And owl ears at top (y=98), top text at y=45-57 (radius 140-152). Gap. Good.

Alright. Let me also reconsider the belly and feather details, and make the owl look good.

Let me also add small feet at the bottom of the owl? Optional. Owls have talons. Let me add tiny feet. Actually, keep it clean, skip feet or add minimal.

Let me add feet: two small shapes at the bottom of the body. 
- Left foot: at (180, 310), small. Right foot at (220,310).
Actually the body bottom is at 313 and there's text below. Feet might collide with text. Let me skip feet.

Let me now also reconsider colors for a cohesive hockey look:
- Navy: #14345b
- Amber: #e8960c (or #f39c12)
- Owl body: #5c6b7a (steel gray-blue)
- Owl wings: #4856647 (darker)
- Owl belly: #e6ecf0
- Owl belly feathers: #b7c4cf
- Owl beak: #e8960c (amber, matches accent)
- Owl pupils: #10233a (very dark navy)
- Sticks shaft: #2b3a4a (dark slate) or make them navy to match. Let me make sticks a contrasting color. Hockey sticks... let me do dark gray #3a3a3a with amber blade tips? Or match the navy. Let me make sticks navy #14345b with amber grip and amber blade edge, to tie into the theme. Actually, to make sticks stand out, let me use a dark charcoal #374140 or the navy. Let me use navy for sticks to keep it cohesive, with amber grip.

Hmm, if sticks are navy and owl is gray, and background is transparent, the navy sticks on transparent background are fine. Let me do:
- Stick shaft: #1f3a5b (navy) 
- Stick grip: #e8960c (amber)
- Stick blade: slightly different, maybe #163047 or add an amber tip.

Let me make the blade a touch different from shaft for definition. I'll make shaft #223c5c and blade #163047, or just keep same color. Let me keep shaft and blade same navy, with amber grip at top. Clean.

Actually, to distinguish blade from shaft, let me make the blade a bit wider and a slightly darker shade. Or add an amber line at the blade. Let me just make blade slightly darker: shaft #26415f, blade #1c3149.

Let me simplify: stick is one color #26415f, with amber grip rect at top. The blade is just the wider bottom part, same color. It'll read as a hockey stick. Good.

Now, let me write the final SVG.

Let me reconsider one more time the text arc paths and make sure they're correct.

Top arc (for textPath), left-to-right over the top, sweep 1:
" M 60 200 A 140 140 0 0 1 340 200"
Endpoints (60,200) and (340,200), which are at radius 140 from center (200,200). Arc over the top with sweep 1. ✓ (clockwise from left goes over the top).

Wait, let me double-check sweep 1 from left point goes over the top. Left point (60,200) is at 9 o'clock. Sweep 1 = clockwise. Clockwise from 9 o'clock: 9→12→3, over the top. ✓. So top arc sweep 1 goes over the top. ✓.

Bottom arc (for textPath), left-to-right over the bottom, sweep 0:
" M 60 200 A 140 140 0 0 0 340 200"
Sweep 0 = counterclockwise. From 9 o'clock, counterclockwise: 9→6→3, over the bottom. ✓.

Now, text:
Top text: 
```svg
<text font-family="Arial, Helvetica, sans-serif" font-size="26" font-weight="bold" letter-spacing="4" fill="#ffffff">
  <textPath href="#topArc" startOffset="50%" text-anchor="middle">OWAYO</textPath>
</text>
```

Bottom text:
```svg
<text font-family="Arial, Helvetica, sans-serif" font-size="26" font-weight="bold" letter-spacing="4" fill="#ffffff">
  <textPath href="#bottomArc" startOffset="50%" text-anchor="middle">EULERS</textPath>
</text>
```

Wait, I need to double check the baseline radius. The arc endpoints are at radius 140 (from (60,200) to (340,200), radius = 140). The text baseline follows this arc at radius 140. Text extends outward for top (140→155) and inward for bottom (140→125). As discussed.

Hmm, but wait, I want to double-check the top text is outward. Let me re-examine with the "frown vs smile" reasoning:
Top arc is a "frown" shape (convex up, like ⌢). Text on a frown path (left-to-right) sits on top (convex side) = above = outward. ✓.
Bottom arc is a "smile" shape (concave up, like ⌢ inverted = ⌣). Text on a smile path sits on the concave side = above the curve = toward center = inward. ✓.

Good.

So top text is at radius 140-155 (outward), bottom text at radius 125-140 (inward).

Now, with inner ring at r=165 and outer ring at r=180:
- Top text 140-155, inner ring 165: gap 10. Good.
- Bottom text 125-140: inside, owl max 118: gap 7. Good.

Let me set inner ring at r=165. Actually, let me reconsider—do I even want the inner ring? It adds a nice frame for the text. Let me keep it but make it thin (w=2-3).

Also, I realize the top text at radius 140-155 and the inner ring at 165 — the text is between the invisible arc(140) and ring(165). Good.

Let me also make sure "EULERS" fits on the bottom arc. 6 chars at font 26. The bottom arc spans from 9 o'clock to 3 o'clock (semicircle) = 180°. But "EULERS" only needs part of it. With startOffset 50% and text-anchor middle, it's centered at the bottom. The text width ~6*15=90px (rough). At radius 140, arc angle for 90px = 90/140 rad = 0.64 rad = 37°. So text spans ±18° around the bottom. Fits within the semicircle. Good.

"OWAYO" 5 chars ~75px, spans ±13°. Fits. Good.

Now let me write it all out.

Actually, let me reconsider the letter-spacing and font-size to make sure text fits and looks good. Let me use font-size 24, letter-spacing 3.

Also, I want the text to be clearly readable. White on transparent background — the text will appear over whatever is behind. That's fine for a logo (it'll be placed on a background). The prompt said background can be solid or none. With none, the text is white and might be hard to see on white backgrounds, but that's the nature of a transparent logo. I'll go with transparent background as preferred.

Hmm, actually, let me reconsider. The prompt says "Der Hintergrund des Logos soll einfarbig sein, am besten besitzt das Logo gar keinen Hintergrund." = "The background of the logo should be solid color, preferably the logo has no background at all." So no background is preferred. I'll make it transparent (no background rect). Good.

Let me write the final SVG now.

Let me assemble:

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 400" width="400" height="400">
  <defs>
    <path id="topArc" d="M 60 200 A 140 140 0 0 1 340 200" />
    <path id="bottomArc" d="M 60 200 A 140 140 0 0 0 340 200" />
  </defs>

  <!-- Crossed hockey sticks -->
  <g>
    <g transform="rotate(16 200 200)">
      <path d="M -4 -128 L 4 -128 L 4 88 L 15 90 L 15 108 L -16 108 L -15 90 L -4 88 Z" fill="#26415f"/>
      <rect x="-5" y="-128" width="10" height="24" rx="3" fill="#e8960c"/>
    </g>
    <g transform="rotate(-16 200 200)">
      <path d="M -4 -128 L 4 -128 L 4 88 L 15 90 L 15 108 L -16 108 L -15 90 L -4 88 Z" fill="#26415f"/>
      <rect x="-5" y="-128" width="10" height="24" rx="3" fill="#e8960c"/>
    </g>
  </g>

  <!-- Owl -->
  <g>
    <!-- ears -->
    <path d="M 162 130 L 150 100 L 185 122 Z" fill="#5c6b7a"/>
    <path d="M 238 130 L 250 100 L 215 122 Z" fill="#5c6b7a"/>
    <!-- head -->
    <circle cx="200" cy="160" r="56" fill="#5c6b7a"/>
    <!-- eyes -->
    <circle cx="173" cy="162" r="25" fill="#ffffff"/>
    <circle cx="227" cy="162" r="25" fill="#ffffff"/>
    <circle cx="175" cy="164" r="12" fill="#10233a"/>
    <circle cx="225" cy="164" r="12" fill="#10233a"/>
    <circle cx="171" cy="159" r="4.5" fill="#ffffff"/>
    <circle cx="221" cy="159" r="4.5" fill="#ffffff"/>
    <!-- beak -->
    <path d="M 191 182 L 209 182 L 200 201 Z" fill="#e8960c"/>
    <!-- body -->
    <ellipse cx="200" cy="245" rx="64" ry="68" fill="#5c6b7a"/>
    <!-- wings -->
    <path d="M 139 216 Q 117 256 141 300 Q 159 280 156 227 Z" fill="#4a5765"/>
    <path d="M 261 216 Q 283 256 259 300 Q 241 280 244 227 Z" fill="#4a5765"/>
    <!-- belly -->
    <ellipse cx="200" cy="258" rx="42" ry="50" fill="#e6ecf0"/>
    <!-- belly feathers -->
    <path d="M 183 240 Q 200 252 217 240" fill="none" stroke="#b7c4cf" stroke-width="2"/>
    <path d="M 181 261 Q 200 273 219 261" fill="none" stroke="#b7c4cf" stroke-width="2"/>
    <path d="M 183 282 Q 200 294 217 282" fill="none" stroke="#b7c4cf" stroke-width="2"/>
  </g>

  <!-- Text -->
  <text font-family="Arial, Helvetica, sans-serif" font-size="24" font-weight="bold" letter-spacing="3" fill="#ffffff">
    <textPath href="#topArc" startOffset="50%" text-anchor="middle">OWAYO</textPath>
  </text>
  <text font-family="Arial, Helvetica, sans-serif" font-size="24" font-weight="bold" letter-spacing="3" fill="#ffffff">
    <textPath href="#bottomArc" startOffset="50%" text-anchor="middle">EULERS</textPath>
  </text>

  <!-- Rings -->
  <circle cx="200" cy="200" r="180" fill="none" stroke="#14345b" stroke-width="10"/>
  <circle cx="200" cy="200" r="165" fill="none" stroke="#e8960c" stroke-width="3"/>
</svg>
```

Wait, there are issues:
1. The rings are drawn LAST, so they'll be on top of the text and owl. The outer ring (navy, r=180) is at the edge, won't cover text (text max radius 155). The inner ring (amber, r=165) — text top max 155, so ring 165 doesn't cover text. But the inner ring at 165 is a full circle; it will draw over the owl/sticks near radius 165, but owl/sticks are inside, so no visible issue. Actually, the inner ring at 165 will be drawn over the background where there's nothing, fine. And it frames the text. Good.

But wait, the text is drawn BEFORE the rings. The inner ring at 165 is outside the text (text max 155), so it doesn't cover text. Good. The outer ring at 180 covers the edge. Good.

2. The stick handles at radius 128 and blades at 108 — drawn first, then owl on top. The owl (max radius 118 at ears, but body/wings within) covers the crossing. The stick handles (radius 128, at top) stick out above the owl (ears at 118). So handles visible at top. Blades (radius 108) behind owl, mostly hidden. Good.

Hmm, but the stick handles at radius 128 — the owl ears at radius 118. So handles (128) are just outside ears (118). The handles are at the top, ears at top. They might visually merge. Let me check positions. Stick 1 handle top ≈ (165, 77) [computed earlier, but that was for center (200,200) with local y=-128]. Let me recompute with the actual rotation.

Stick 1: rotate(16) around (200,200). Local handle top (0,-128) → 
x' = 200 + 0*cos16 - (-128)*sin16 = 200 + 128*sin16 = 200 + 128*0.2756 = 200+35.3 = 235.3
y' = 200 + 0*sin16 + (-128)*cos16 = 200 - 128*0.9613 = 200 - 123 = 77
Wait, rotation formula: x' = x cosθ - y sinθ, y' = x sinθ + y cosθ, relative to center.
Local (0,-128), θ=16°:
x' = 0*cos16 - (-128)*sin16 = 128*sin16 = 35.3
y' = 0*sin16 + (-128)*cos16 = -128*cos16 = -123
So absolute: (200+35.3, 200-123) = (235.3, 77).
Stick 2: rotate(-16°):
x' = 0*cos(-16) - (-128)*sin(-16) = -128*sin16 = -35.3 (since sin(-16)=-sin16, -(-128)*(-sin16)= -128 sin16... let me redo)
θ=-16: x' = 0*cos(-16) - (-128)*sin(-16) = 0 - (-128)*(-0.2756) = -35.3
y' = 0*sin(-16) + (-128)*cos(-16) = -128*0.9613 = -123
Absolute: (164.7, 77).

So stick 1 handle top at (235, 77), stick 2 handle top at (165, 77). They're at the top, spread apart (x=165 and 235). 

Owl ears: left ear at (150,100), right ear at (250,100). So ears at x=150 and 250, y=100. Stick handles at x=165 and 235, y=77. So stick handles are above and slightly inside the ears. The handles at y=77 (higher than ears at y=100). And x=165,235 vs ears x=150,250. So handles are between the ears, higher up. They should be visible sticking up between/above the owl ears. 

Hmm, actually the handles at (165,77) and (235,77) — these are the TOP of the sticks. The sticks go from there down toward the center (crossing at 200,200). So stick 1 goes from (235,77) down to crossing (200,200) and continues to blade. Stick 2 from (165,77) to (200,200) to blade.

So the visible stick parts: from handles (top, outside owl) down to where the owl covers them. The owl covers roughly radius 118. The sticks at radius <118 are hidden. So visible stick = from handle (radius 128) to radius 118. That's a small visible portion (10px). Hmm, that's not much. Let me make the sticks longer / poke out more, or make the owl smaller.

Actually, the crossing is at (200,200) which is the owl center. The sticks extend from radius 128 (handles, top) through the center to radius 108 (blades, bottom). The owl covers radius up to 118. So the sticks are covered from radius 118 down to... the sticks pass through the owl. The parts of the sticks within radius 118 are hidden. The parts beyond radius 118 (handles near top, and blades near bottom if blade radius >118) are visible.

Blade radius: stick 1 blade bottom local (0,108) rotate 16°:
x' = 0 - 108*sin16... wait local (0,108): x' = 0*cos16 - 108*sin16 = -108*0.2756 = -29.8; y' = 0*sin16 + 108*cos16 = 103.8. Absolute (170.2, 303.8). Radius from (200,200): sqrt(30^2+104^2)=108. So blade at radius 108, inside owl (118). Hidden.

So only the handles (radius 128, just outside owl 118) are visible, a small bit. That's not great. Let me make the sticks poke out more.

Options:
- Make sticks longer (longer handles).
- Make owl smaller.
- Lower the crossing point so sticks extend further outside.

Let me make the crossing point lower (below center) so the handles extend further up and out. Or make the owl smaller.

Let me make the owl smaller and the sticks longer. Let me reduce owl to max radius ~95, and make sticks span radius 100-175.

Actually, let me reconsider the composition. Classic hockey logo: mascot (owl) in center, two sticks crossed behind, handles up and out, blades down and out, poking past the mascot. For that, sticks should extend well outside the mascot.

Let me increase stick length and lower the crossing.

New stick design (longer): handle top at y=-160 (local), blade at y=+110 (local). Crossing at (200, 210) (lower than center to give room for top text).

Hmm, let me set crossing at (200, 210). Local stick centered at (0,0) maps to (200,210).

Stick local: handle top (0,-155), blade (0,105). Length 260.
After rotate(±16) around (200,210):
Stick 1 handle top local (0,-155):
x' = 155*sin16 = 42.7, y' = -155*cos16 = -149. Absolute (242.7, 61).
Stick 1 blade local (0,105):
x' = -105*sin16 = -29, y' = 105*cos16 = 101. Absolute (171, 311).
Stick 2 handle top (157.3, 61), blade (229, 311).

Handle radius from (200,210): (242.7,61): sqrt(42.7^2+149^2)=sqrt(1823+22201)=sqrt(24024)=155. So handles at radius 155! That's near the ring (180) and text (140-155). Hmm, handles at radius 155 would collide with top text (140-155) and inner ring (165). 

That's too much. The handles poke out to radius 155, overlapping text area.

I need to balance. Let me reduce stick length and crossing position so handles reach radius ~125-135, just outside the owl, not colliding with text.

Let me set crossing at (200, 210), stick handle top local (0,-140), blade local (0,95).
Stick 1 handle top (0,-140) rotate 16:
x' = 140*sin16 = 38.6, y' = -140*cos16 = -134.6. Absolute (238.6, 75.4). Radius from (200,210): sqrt(38.6^2+134.6^2)=sqrt(1490+18117)=sqrt(19607)=140. Still 140.

The issue: handle radius = 140*cos... no. Handle local (0,-140), the distance from center is 140 (since it's straight up, then rotated, distance preserved). So handle radius = 140 always (rotation preserves distance from pivot). So if I want handle at radius 125, the local handle should be at distance 125 from pivot: (0,-125).

So the stick handle distance from crossing = its radius. To have handles at radius 125, local handle at (0,-125). To have blades at radius 108, local blade at (0,108).

So stick spans from radius 125 (handle) to radius 108 (blade), with crossing at radius 0 (center). Wait, the crossing is at the pivot (radius 0). The stick goes from handle (radius 125, up) through the pivot (radius 0, center) to blade (radius 108, down). 

So the stick is a line from (radius 125, up-ish) through center to (radius 108, down-ish). The owl covers radius up to ~118. So the stick is hidden from radius 118 (on the handle side) to the center, and hidden from center to radius 118 (blade side). Visible: handle from radius 118 to 125 (7px), blade from radius 108 to 118... wait blade is at radius 108 which is INSIDE the owl (118). So blade fully hidden.

Hmm. So with the stick passing through the center (behind the owl), most of it is hidden. Only small bits poke out.

For a better look, I want the sticks to cross BEHIND the owl but the crossing point to be lower/behind so more of the sticks show. Alternatively, the sticks cross in front of nothing (behind owl) and the owl is small enough that sticks show.

Let me make the owl smaller so sticks show more. Let me target: owl max radius ~85, sticks from radius 100 (handle) to 170 (blade), crossing at center. Then handles and blades both poke out past the owl nicely.

But then the sticks would extend to radius 170, near the ring (180) and text. The blades at radius 170 at the bottom would collide with bottom text (140) — no, bottom text is at radius 140, blades at 170 would be outside, near ring. Hmm.

Let me reconsider the whole layout to make it work:

The sticks should cross behind the owl, with handles pointing up-out and blades pointing down-out, but NOT colliding with the text (top text top, bottom text bottom).

Text occupies: top text radius 140-155 (top region), bottom text radius 125-140 (bottom region).
Sticks should avoid these regions. But sticks go from top to bottom through the center, passing through both top and bottom regions. So the stick handles (top) are in the top text region, and blades (bottom) in the bottom text region. Collision.

Resolution: Put the crossing point OFF-center, or angle the sticks so handles and blades are in the "side" regions, not top/bottom.

Classic crossed-sticks emblem: the sticks cross with handles up and blades down, and the text goes around the outside (top and bottom). The stick handles and blades are usually in the top and bottom, and the text is BETWEEN them and the center, OR the sticks are behind the text.

Actually, in many badges, the crossed sticks are BEHIND the mascot and their ends (handles/blades) stick out toward the top and bottom, and the text "OWAYO" (top) and "EULERS" (bottom) are placed in the upper/lower areas, sometimes overlapping or adjacent to the stick ends.

Alternatively, the sticks are angled more horizontally (like a V or X that's wider), with ends toward the sides (left-right), avoiding the top/bottom text.

Let me angle the sticks so their ends point toward the upper-left, upper-right, lower-left, lower-right diagonally, keeping the text at the very top and bottom clear.

If I rotate the sticks by a larger angle (say ±30°), the handles spread more toward the sides and the blades too. Let me reconsider.

With crossing at center (200,200) and sticks at ±30°:
Stick 1 handle (0,-125) rotate 30°:
x' = 125*sin30 = 62.5, y' = -125*cos30 = -108.3. Absolute (262.5, 91.7). Radius 125. Angle: this is at angle... from center, (62.5,-108.3) is up and to the right, at angle atan2(-108.3,62.5) = about -60° from +x axis, i.e., 60° above horizontal to the right = at the "1 o'clock" position.
Stick 1 blade (0,125)... let me use blade local (0,108) rotate 30:
x' = -108*sin30 = -54, y' = 108*cos30 = 93.6. Absolute (146, 293.6). Radius 125. Angle atan2(93.6,-54) = about 120° = "7 o'clock" position (lower left).

So stick 1 goes from 1 o'clock (handle) to 7 o'clock (blade), passing through center.
Stick 2 (rotate -30°): handle at 11 o'clock (up-left), blade at 5 o'clock (down-right).

So the four stick ends are at 1, 5, 7, 11 o'clock positions (diagonal). The text at top (12 o'clock) and bottom (6 o'clock) is clear of the stick ends! 

Let me use ±30° rotation. Then:
- Top text (12 o'clock, radius 140-155): clear of stick ends (which are at 1 and 11 o'clock).
- Bottom text (6 o'clock, radius 125-140): clear of stick ends (5 and 7 o'clock).

The sticks cross at center behind the owl. The owl covers the center. The stick ends reach radius 125 (handles) — wait, handle radius 125 at 1 o'clock. The owl at 1 o'clock position: owl head side at (256,160), radius from (200,205)... let me use center (200,200). Head side (256,160): radius sqrt(56^2+40^2)=69. So owl at 1 o'clock is at radius ~69. Stick handle at radius 125 at 1 o'clock pokes out past owl (69). Good, visible.

But wait, the stick handle at 1 o'clock radius 125 — is that near the text? Top text is at 12 o'clock radius 140-155. The handle at 1 o'clock radius 125 is slightly to the right and closer. They might be close but not overlapping (different angles). Let me make sure. 1 o'clock vs 12 o'clock — 30° apart. At radius 125-155. The handle (125, 30° from top) and text (140-155, at top). Close but the handle is lower and to the right. Should be OK, maybe a small gap.

Hmm, let me reconsider. Maybe ±25° is a good compromise. Let me use ±25°.

Actually, let me reconsider the crossing point. If the crossing is at the exact center (200,200) and the owl is centered there, the sticks are hidden behind the owl in the middle. The ends poke out. That's the look. Let me go with crossing at (200, 205) (just below visual center to balance text) or (200,200). Let me use (200, 205) to leave a bit more room at top for text.

Hmm, actually, let me keep crossing at (200,200) for simplicity, and center the owl around (200, 210) (slightly below center). Then top has more room for text.

Wait, but if the owl is at (200,210) and sticks cross at (200,200), the sticks cross just above the owl center. Minor. Let me just use (200,205) for both crossing and approximate owl center, or handle separately.

Let me simplify: crossing at (200, 205). Owl centered at (200, 215). Sticks rotate around (200,205).

Ugh, too many parameters. Let me just pick:
- Crossing/pivot: (200, 205).
- Sticks: local handle (0,-130), shaft to blade (0,100). Rotate ±25°.
- Owl: as designed, centered ~ (200, 210).

Let me recompute stick ends with pivot (200,205), handle local (0,-130), blade local (0,100), rotate ±25°.

Stick 1 (rotate +25°):
Handle (0,-130): x' = 130*sin25 = 55, y' = -130*cos25 = -117.9. Absolute (255, 87.1). Radius from pivot: 130.
Blade (0,100): x' = -100*sin25 = -42.3, y' = 100*cos25 = 90.6. Absolute (157.7, 295.6). Radius 100.

Stick 2 (rotate -25°):
Handle (0,-130): x' = -55, y' = -117.9. Absolute (145, 87.1). Radius 130.
Blade (0,100): x' = 42.3, y' = 90.6. Absolute (242.3, 295.6). Radius 100.

So:
- Handles: (255,87) and (145,87), radius 130, at ~1 o'clock and 11 o'clock.
- Blades: (157.7,295.6) and (242.3,295.6), radius 100, at ~7 and 5 o'clock.

Text:
- Top text at 12 o'clock, radius 140-155. Handles at 130 radius, 11/1 o'clock. The handles (radius 130) are inside the text (140-155) in radius, and 30° to the sides. So handles are below-inside the text. Small gap. Should be OK.

Hmm, actually the handles at radius 130 and text at radius 140-155 — the handles are closer to center than the text. And 30° to the side. So handles don't overlap text. Good.

- Bottom text at 6 o'clock, radius 125-140. Blades at radius 100, 5/7 o'clock. Blades are inside (radius 100 < 125) and 30° to the side. No overlap. Good.

- Owl covers the center and radius up to ~118 (ears). Sticks from radius 118 (where owl edge is) outward to handles (130) and the center part is hidden. Blades at radius 100 are inside owl (hidden). So visible sticks: handles (radius 118-130) poking up-out, and the crossing arms. Blades hidden behind owl. That's fine—blades behind owl, handles showing. 

Actually, for a hockey logo, you often want to see the blades too. But if blades are behind the owl, they're hidden. That's OK; the handles showing is enough to indicate hockey sticks. Or I could make the owl smaller so blades show. Let me keep owl moderate.

Hmm, let me reconsider. Maybe I want the blades visible at the bottom. Let me make the owl smaller (max radius ~90) so blades (radius 100) poke out slightly. And handles (130) poke out more.

Let me target owl max radius ~95. Then:
- Ears at radius 95.
- Handles at 130: poke out 35px past ears. Good, clearly visible.
- Blades at 100: poke out 5px past ears. Barely visible. 

Let me make blades poke out more by making sticks longer (blade local (0,120) → radius 120). Then blades at radius 120, poking out 25px past ears (95). Good.

But longer blades (radius 120) at 5/7 o'clock — near bottom text (radius 125-140 at 6 o'clock). Blades at radius 120, 5/7 o'clock; text at radius 125-140, 6 o'clock. Blades slightly inside and 30° aside. Small gap. OK.

Let me set blade local (0,120), handle local (0,-130). Rotate ±25°, pivot (200,205).

Stick 1 blade (0,120) rotate 25: x' = -120*sin25 = -50.7, y' = 120*cos25 = 108.7. Absolute (149.3, 313.7). Radius 120. Angle: atan2(108.7, -50.7) = 180-65 = 115° → 7 o'clock-ish (lower left). 
Stick 1 handle (0,-130) rotate 25: (255, 87), radius 130, 1 o'clock.

OK. Let me finalize stick local: handle (0,-130), blade (0,120). Blade is the wider part at the bottom.

Let me redefine the stick path (local, pivot at origin, pointing down):
Handle top at y=-130, shaft down to y=95, blade from y=95 to y=120.
```
M -4 -130
L 4 -130
L 4 92
L 14 94
L 14 118
L -15 118
L -14 94
L -4 92
Z
```
Grip: rect x=-5 y=-130 width=10 height=24 rx=3, amber.

Wait, the blade bottom at y=118, radius 118 from pivot. Let me make it 120: blade bottom y=120. And I said blade local (0,120). Let me set blade bottom at y=120.

Let me finalize stick path:
```
M -4 -130
L 4 -130
L 4 92
L 14 94
L 14 120
L -15 120
L -14 94
L -4 92
Z
```

This is the stick. Good.

Now owl, let me make it max radius ~95. Let me recompute owl with adjustments.

Owl (pivot/center reference (200,205) for radius, but I'll just use absolute coords):
- Ears: left (158,100), right (242,100). Radius from (200,205): (158,100): sqrt(42^2+105^2)=sqrt(1764+11025)=sqrt(12789)=113. Hmm, still 113. Let me move ears up/in. Ears at (162,95) and (238,95): radius sqrt(38^2+110^2)=sqrt(1444+12100)=sqrt(13544)=116. Still high.

The ears are high up (small y), so radius from (200,205) is large. To reduce ear radius, move ears closer to center (larger y) or the owl center should be higher.

Hmm, the issue is the owl center. If owl is centered at (200,205) but the ears are at y=95 (110px above center), ear radius is 110+. To have ears at radius 95, ear should be 95px above center: y=205-95=110. So ears at y=110. But then the owl head is lower.

Let me reconsider the owl vertical placement. Let me place the owl so its center is around (200, 215), and ears at y=115 (radius 90 from center 215). Head center at y=165. Etc.

Actually, let me just accept the owl ears

### Antwort

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 400" width="400" height="400">
  <defs>
    <path id="topArc" d="M 60 205 A 140 140 0 0 1 340 205"/>
    <path id="bottomArc" d="M 60 205 A 140 140 0 0 0 340 205"/>
  </defs>

  <!-- Crossed hockey sticks -->
  <g>
    <g transform="rotate(25 200 205)">
      <path d="M -4 -130 L 4 -130 L 4 92 L 14 94 L 14 120 L -15 120 L -14 94 L -4 92 Z" fill="#26415f"/>
      <rect x="-5" y="-130" width="10" height="26" rx="3" fill="#e8960c"/>
    </g>
    <g transform="rotate(-25 200 205)">
      <path d="M -4 -130 L 4 -130 L 4 92 L 14 94 L 14 120 L -15 120 L -14 94 L -4 92 Z" fill="#26415f"/>
      <rect x="-5" y="-130" width="10" height="26" rx="3" fill="#e8960c"/>
    </g>
  </g>

  <!-- Owl -->
  <g>
    <path d="M 160 132 L 147 100 L 183 122 Z" fill="#5c6b7a"/>
    <path d="M 240 132 L 253 100 L 217 122 Z" fill="#5c6b7a"/>
    <circle cx="200" cy="162" r="56" fill="#5c6b7a"/>
    <circle cx="173" cy="164" r="25" fill="#ffffff"/>
    <circle cx="227" cy="164" r="25" fill="#ffffff"/>
    <circle cx="175" cy="166" r="12" fill="#10233a"/>
    <circle cx="225" cy="166" r="12" fill="#10233a"/>
    <circle cx="171" cy="161" r="4.5" fill="#ffffff"/>
    <circle cx="221" cy="161" r="4.5" fill="#ffffff"/>
    <path d="M 191 184 L 209 184 L 200 203 Z" fill="#e8960c"/>
    <ellipse cx="200" cy="247" rx="64" ry="68" fill="#5c6b7a"/>
    <path d="M 139 218 Q 116 258 141 302 Q 160 281 156 228 Z" fill="#4a5765"/>
    <path d="M 261 218 Q 284 258 259 302 Q 240 281 244 228 Z" fill="#4a5765"/>
    <ellipse cx="200" cy="260" rx="42" ry="50" fill="#e6ecf0"/>
    <path d="M 183 242 Q 200 254 217 242" fill="none" stroke="#b7c4cf" stroke-width="2"/>
    <path d="M 181 263 Q 200 275 219 263" fill="none" stroke="#b7c4cf" stroke-width="2"/>
    <path d="M 183 284 Q 200 296 217 284" fill="none" stroke="#b7c4cf" stroke-width="2"/>
  </g>

  <!-- Team name -->
  <text font-family="Arial, Helvetica, sans-serif" font-size="24" font-weight="bold" letter-spacing="3" fill="#ffffff">
    <textPath href="#topArc" startOffset="50%" text-anchor="middle">OWAYO</textPath>
  </text>
  <text font-family="Arial, Helvetica, sans-serif" font-size="24" font-weight="bold" letter-spacing="3" fill="#ffffff">
    <textPath href="#bottomArc" startOffset="50%" text-anchor="middle">EULERS</textPath>
  </text>

  <!-- Badge rings -->
  <circle cx="200" cy="205" r="180" fill="none" stroke="#14345b" stroke-width="10"/>
  <circle cx="200" cy="205" r="165" fill="none" stroke="#e8960c" stroke-width="3"/>
</svg>
```
