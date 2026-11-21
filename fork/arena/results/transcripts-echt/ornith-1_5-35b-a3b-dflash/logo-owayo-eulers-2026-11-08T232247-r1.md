# ornith-1_5-35b-a3b-dflash - logo-owayo-eulers (2026-11-08T23:22:47)

## Antwort (32036 Tokens, 158.773 s, Ende: stop)

### Denkphase

The user wants a logo for an ice hockey team called "Owayo Eulers". The logo should contain an owl and an ice hockey stick. The background should be solid or have no background.

I need to respond with exactly one complete SVG document in a code block. No external resources, no scripts.

Let me create an SVG logo with:
1. An owl (Eule)
2. An ice hockey stick (Eishockeyschläger)
3. The team name "Owayo Eulers"
4. No background (or solid background)

Let me design this carefully. I'll create a stylized owl holding or positioned with a hockey stick, with the team name incorporated.

Let me think about the design:
- An owl face/body in the center
- A hockey stick behind or crossing
- Text "Owayo Eulers"
- Maybe a circular or shield shape

Let me create a nice SVG. I'll use an owl with big eyes (typical owl look), feathers, and a hockey stick.

Let me build this step by step.

I'll create a circular logo with:
- Background circle (maybe transparent or a colored ring)
- Owl in the center
- Hockey stick
- Text

Let me write the SVG:

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 500 500" width="500" height="500">
  <!-- Definitions -->
  <defs>
    <radialGradient id="eyeGlow" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#fff9c4"/>
      <stop offset="60%" stop-color="#ffd54f"/>
      <stop offset="100%" stop-color="#ff8f00"/>
    </radialGradient>
    <linearGradient id="bodyGrad" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#6d4c41"/>
      <stop offset="100%" stop-color="#4e342e"/>
    </linearGradient>
    <linearGradient id="stickGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#ffb74d"/>
      <stop offset="100%" stop-color="#f57c00"/>
    </linearGradient>
  </defs>
  
  <!-- Outer ring -->
  <circle cx="250" cy="250" r="240" fill="none" stroke="#1a237e" stroke-width="12"/>
  ...
</svg>
```

Let me think more carefully about the owl design. Owls have:
- Big round eyes
- A small beak
- Ear tufts (some species)
- A rounded body
- Feather patterns

For a hockey theme, I'll add a hockey stick.

Let me create a complete, well-designed logo.

I'll make:
1. A dark navy circle background ring (the "no background" means the owl area is transparent, but I can have a circular emblem)
2. The owl
3. A hockey stick
4. Text "Owayo Eulers"

Actually, "am besten besitzt das Logo gar keinen Hintergrund" means "best if the logo has no background at all". So I should avoid a solid background rectangle. I can have a circular emblem outline though.

Let me design the owl:

Owl head:
- Two big eyes with pupils
- Beak
- Head feathers
- Ear tufts

Owl body:
- Body shape
- Chest feathers (small V or U shapes)

Hockey stick:
- A long shaft
- A curved blade at the bottom

Let me place the hockey stick diagonally behind the owl, or the owl could be "holding" it.

Let me write this out carefully.

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 500 500" width="500" height="500">
  <defs>
    <radialGradient id="eyeYellow" cx="50%" cy="45%" r="55%">
      <stop offset="0%" stop-color="#fffde7"/>
      <stop offset="50%" stop-color="#ffe082"/>
      <stop offset="100%" stop-color="#ffb300"/>
    </radialGradient>
    <linearGradient id="bodyGrad" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#8d6e63"/>
      <stop offset="100%" stop-color="#5d4037"/>
    </linearGradient>
    <linearGradient id="stickGrad" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#ffca28"/>
      <stop offset="100%" stop-color="#ff8f00"/>
    </linearGradient>
  </defs>
  
  <!-- Circular emblem border -->
  <circle cx="250" cy="250" r="238" fill="none" stroke="#0d1b5e" stroke-width="10"/>
  <circle cx="250" cy="250" r="222" fill="none" stroke="#cfd8dc" stroke-width="3"/>
  
  <!-- Hockey stick (behind owl) -->
  <g>
    <rect x="300" y="120" width="14" height="280" rx="7" fill="url(#stickGrad)" transform="rotate(18 307 260)"/>
    ... blade
  </g>
</svg>
```

Hmm, let me think about the hockey stick placement. A hockey stick has a long shaft and a blade at the bottom that curves. Let me place it diagonally.

Actually, let me make the design cleaner. Let me create the owl prominently in the center, with a hockey stick crossing behind it.

Let me reconsider. I'll make:
- Owl centered
- Hockey stick behind, going from top-right to bottom-left
- Text at the bottom "Owayo Eulers"
- Maybe "EISHOCKEY" at top or a banner

Let me write the full thing.

For the owl eyes, I'll create circles with dark pupils.

Let me build the owl:

Head: A large rounded shape.
Eyes: Two white circles with yellow rings and dark pupils.
Beak: A small triangle.
Ear tufts: Two triangular points at top.
Body: Below the head.
Chest: Lighter colored with feather lines.

Let me write it all out.

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 500 500" width="500" height="500">
  <defs>
    <radialGradient id="eyeYellow" cx="50%" cy="45%" r="55%">
      <stop offset="0%" stop-color="#fffde7"/>
      <stop offset="55%" stop-color="#ffe082"/>
      <stop offset="100%" stop-color="#ffb300"/>
    </radialGradient>
    <linearGradient id="bodyGrad" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#8d6e63"/>
      <stop offset="100%" stop-color="#4e342e"/>
    </linearGradient>
    <linearGradient id="wingGrad" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#6d4c41"/>
      <stop offset="100%" stop-color="#3e2723"/>
    </linearGradient>
    <linearGradient id="stickGrad" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#ffca28"/>
      <stop offset="100%" stop-color="#ff8f00"/>
    </linearGradient>
  </defs>
  
  <!-- Emblem outer ring -->
  <circle cx="250" cy="250" r="240" fill="none" stroke="#0d1b5e" stroke-width="12"/>
  <circle cx="250" cy="250" r="220" fill="none" stroke="#e0e0e0" stroke-width="4"/>
  
  <!-- Hockey Stick -->
  <g transform="rotate(-24 250 300)">
    <rect x="244" y="70" width="12" height="300" rx="6" fill="url(#stickGrad)"/>
    <!-- blade -->
    <path d="M250 368 L250 400 Q250 420 230 425 L195 430 Q180 431 178 418 L176 405" 
          fill="none" stroke="#ff8f00" stroke-width="14" stroke-linecap="round"/>
  </g>
  ...
</svg>
```

This is getting complex. Let me simplify and make it look good.

Let me reconsider the whole approach. I'll create a nice flat-design owl logo.

Final design plan:
- viewBox 0 0 500 500
- No background rectangle (transparent)
- Circular navy border ring
- Owl in center (brown/tan colors)
- Hockey stick behind
- "OWAYO EURLERS" text curved or straight at bottom
- Maybe "ISHOCKEY" or a small star

Let me write clean SVG.

For text, I'll use a text element. For a curved text, I could use a path, but straight text is simpler and cleaner. Let me put "OWAYO EURLERS" at the bottom in a bold font.

Actually, let me make it more logo-like. Let me put the team name in a banner or just as text below the owl.

Let me finalize:

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 500 500" width="500" height="500">
  <defs>
    <radialGradient id="eyeYellow" cx="50%" cy="45%" r="55%">
      <stop offset="0%" stop-color="#fffde7"/>
      <stop offset="55%" stop-color="#ffe082"/>
      <stop offset="100%" stop-color="#ffb300"/>
    </radialGradient>
    <linearGradient id="bodyGrad" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#8d6e63"/>
      <stop offset="100%" stop-color="#4e342e"/>
    </linearGradient>
    <linearGradient id="wingGrad" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#6d4c41"/>
      <stop offset="100%" stop-color="#3e2723"/>
    </linearGradient>
    <linearGradient id="stickGrad" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#ffca28"/>
      <stop offset="100%" stop-color="#ff8f00"/>
    </linearGradient>
  </defs>
  
  <!-- Emblem outer ring -->
  <circle cx="250" cy="250" r="240" fill="none" stroke="#0d1b5e" stroke-width="12"/>
  <circle cx="250" cy="250" r="220" fill="none" stroke="#e0e0e0" stroke-width="4"/>
  
  <!-- Hockey Stick -->
  <g transform="rotate(-24 250 300)">
    <rect x="244" y="70" width="12" height="300" rx="6" fill="url(#stickGrad)"/>
    <!-- blade -->
    <path d="M250 368 L250 400 Q250 420 230 425 L195 430 Q180 431 178 418 L176 405" 
          fill="none" stroke="#ff8f00" stroke-width="14" stroke-linecap="round"/>
  </g>
  ...
</svg>
```

Hmm, let me think more carefully about the owl design. Owls have:
- Big round eyes
- A small beak
- Ear tufts (some species)
- A rounded body
- Feather patterns

For a hockey theme, I'll add a hockey stick.

Let me create a complete, well-designed logo.

I'll make:
1. A dark navy circle background ring (the "no background" means the owl area is transparent, but I can have a circular emblem)
2. The owl
3. A hockey stick
4. Text "Owayo Eulers"

Let me write this out carefully.

I'll create a nice flat-design owl logo.

Final design plan:
- viewBox 0 0 500 500
- No background rectangle (transparent)
- Circular navy border ring
- Owl in center (brown/tan colors)
- Hockey stick behind
- "OWAYO EURLERS" text curved or straight at bottom
- Maybe "ISHOCKEY" or a small star

Let me write clean SVG.

For text, I'll use a text element. For a curved text, I could use a path, but straight text is simpler and cleaner. Let me put "OWAYO EURLERS" at the bottom in a bold font.

Actually, let me make it more logo-like. Let me put the team name in a banner or just as text below the owl.

Let me finalize the SVG. I'll build it piece by piece and make sure it's valid.

Let me define the owl more precisely.

Owl head: circle at (250, 200), radius 90.
Eyes: white circles. Left eye at (215, 185), right eye at (285, 185), radius 32.
Pupils: dark circles at center of eyes.
Beak: orange triangle below between eyes, from (250, 210) pointing down to (250, 240).
Ear tufts: two triangles at top of head.
Body: below head, an ellipse or path.
Chest: lighter area with feather lines.
Wings: two shapes on sides.

Let me also add the hockey stick. I'll place it behind the owl, going diagonally.

Let me write the full SVG now.

For the hockey stick, let me make it cleaner. A hockey stick:
- Long shaft (rectangle, rotated)
- Blade at the bottom (curved)

Let me place the stick from upper right to lower left, behind the owl.

Actually, for simplicity and clean look, let me have the hockey stick vertical-ish but tilted, with the blade at the bottom.

Let me create the blade as a path.

OK here's my plan for the stick:
- Shaft: a long thin rotated rectangle
- Blade: at the bottom, an L-shape or curve

Let me use a group with rotation.

Let me write it:

```svg
<!-- Hockey Stick -->
<g transform="translate(310 130) rotate(22)">
  <!-- shaft -->
  <rect x="-7" y="0" width="14" height="270" rx="7" fill="url(#stickGrad)"/>
  <!-- blade -->
  <path d="M0 268 L0 285 Q0 300 -18 303 L-62 306 Q-74 306 -74 294 L-74 285 Q-74 278 -62 279 L-20 276 Q-6 275 -4 265 Z" 
        fill="#ff8f00" stroke="#e65100" stroke-width="2"/>
</g>
```

Hmm, this is getting complicated. Let me simplify the blade.

Actually, let me reconsider. Maybe I'll make the hockey stick simpler and cleaner. Let me use a standard hockey stick shape.

A hockey stick viewed from the side:
- Shaft: vertical line
- Blade: at the bottom, curves forward (like a J shape or an L)

Let me make the blade a simple shape:

```svg
<path d="M0 270 L0 290 Q-3 305 -20 308 L-55 310" 
      fill="none" stroke="#ff8f00" stroke-width="16" stroke-linecap="round"/>
```

This makes a shaft ending in a curved blade. That might look OK.

Actually, let me make the blade more like a real hockey stick blade - it has a flat bottom and curves up at the front.

Let me think about it differently. The blade is like:
- A horizontal bottom
- A vertical part connecting to the shaft
- A curved toe at the front

Let me just make a clean stylized version.

I'll create the whole logo now. Let me be decisive and write it.

Let me reconsider colors for a hockey team. Common hockey colors: navy blue, red, white, gold. Let me use:
- Navy blue (#0d1b5e or #1a237e)
- Gold/yellow (#ffca28)
- White
- Brown for the owl (natural owl colors)

The owl should be distinguishable. Let me use warm browns.

Let me write the final SVG:

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 500 500" width="500" height="500">
  <defs>
    <radialGradient id="eyeYellow" cx="50%" cy="45%" r="55%">
      <stop offset="0%" stop-color="#fffde7"/>
      <stop offset="55%" stop-color="#ffe082"/>
      <stop offset="100%" stop-color="#ffb300"/>
    </radialGradient>
    <linearGradient id="bodyGrad" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#8d6e63"/>
      <stop offset="100%" stop-color="#4e342e"/>
    </linearGradient>
    <linearGradient id="wingGrad" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#6d4c41"/>
      <stop offset="100%" stop-color="#3e2723"/>
    </linearGradient>
    <linearGradient id="stickGrad" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#ffca28"/>
      <stop offset="100%" stop-color="#ff8f00"/>
    </linearGradient>
  </defs>
  
  <!-- Emblem outer ring -->
  <circle cx="250" cy="250" r="240" fill="none" stroke="#0d1b5e" stroke-width="12"/>
  <circle cx="250" cy="250" r="220" fill="none" stroke="#e0e0e0" stroke-width="4"/>
  
  <!-- Hockey Stick -->
  <g transform="rotate(-24 250 300)">
    <rect x="244" y="70" width="12" height="300" rx="6" fill="url(#stickGrad)"/>
    <!-- blade -->
    <path d="M250 368 L250 400 Q250 420 230 425 L195 430 Q180 431 178 418 L176 405" 
          fill="none" stroke="#ff8f00" stroke-width="14" stroke-linecap="round"/>
  </g>
  ...
</svg>
```

Hmm, let me think about the owl design. Let me create a nice owl.

Owl head: circle at (250, 190), radius 95.
Eyes: big. Left eye center (212, 185), right eye center (288, 185), radius 34.
Beak: orange, between eyes, pointing down.
Ear tufts: two triangles.
Body: below head.
Chest: lighter with feather pattern.

Let me place the eyes higher on the head (owls have high eyes).

Let me write the owl:

Head:
```svg
<circle cx="250" cy="185" r="95" fill="url(#bodyGrad)"/>
```

Ear tufts (ear feathers):
```svg
<path d="M170 130 L150 70 L205 115 Z" fill="url(#wingGrad)"/>
<path d="M330 130 L350 70 L295 115 Z" fill="url(#wingGrad)"/>
```

Eyes - white circles with yellow:
```svg
<circle cx="212" cy="190" r="38" fill="#fffde7"/>
<circle cx="288" cy="190" r="38" fill="#fffde7"/>
<circle cx="212" cy="190" r="34" fill="url(#eyeYellow)"/>
<circle cx="288" cy="190" r="34" fill="url(#eyeYellow)"/>
```

Pupils (dark):
```svg
<circle cx="214" cy="190" r="16" fill="#1a1a1a"/>
<circle cx="286" cy="190" r="16" fill="#1a1a1a"/>
```

Eye shine:
```svg
<circle cx="208" cy="183" r="5" fill="#fff"/>
<circle cx="280" cy="183" r="5" fill="#fff"/>
```

Beak:
```svg
<path d="M250 215 L235 245 L250 255 L265 245 Z" fill="#ff8f00"/>
```

Hmm, let me make the beak nicer. Owl beaks are like a small curved shape. Let me use:
```svg
<path d="M235 218 Q250 210 265 218 Q268 240 250 255 Q232 240 235 218 Z" fill="#ffa000"/>
```

Body:
```svg
<path d="M160 250 Q150 360 250 380 Q350 360 340 250 Z" fill="url(#bodyGrad)"/>
```

Chest (lighter):
```svg
<path d="M200 260 Q195 340 250 360 Q305 340 300 260 Z" fill="#d7ccc0"/>
```

Chest feather lines:
```svg
<path d="M250 280 L240 292 L250 304 L260 292 Z" fill="#bcaaa4"/>
... repeated
```

Wings:
```svg
<path d="M160 255 Q120 300 145 360 Q160 330 175 300 Z" fill="url(#wingGrad)"/>
<path d="M340 255 Q380 300 355 360 Q340 330 325 300 Z" fill="url(#wingGrad)"/>
```

Feather pattern on body/chest - small V shapes:
```svg
<g fill="none" stroke="#bcaaa4" stroke-width="3">
  <path d="M220 290 Q230 300 240 290"/>
  ...
</g>
```

This is getting detailed. Let me assemble everything and make sure it looks coherent.

For the text "OWAYO EURLERS", I'll place it at the bottom. Let me use two lines or one line. "OWAYO EURLERS" is long. Let me use a bold font.

Actually the team name is "Owayo Eulers". Let me write it as "OWAYO EURLERS" in caps, or keep the original case. Let me use a nice bold style.

Let me place text at the bottom, maybe with a curved path along the circle, or just straight.

Straight text at bottom:
```svg
<text x="250" y="460" font-family="Arial Black, Arial, sans-serif" font-size="42" font-weight="bold" text-anchor="middle" fill="#fff">OWAYO EURLERS</text>
```

Hmm, 42px might be too wide. "OWAYO EURLERS" is 13 characters. At 42px bold, that's roughly 13 * 26 = 338px, which fits in 500 width with margins. OK.

Let me also add "EISHOCKEY" or a subtitle. Actually, let me keep it simple with just the team name, and maybe add a small "EST." or a hockey element.

Let me reconsider the layout. The owl takes up the center. Text at the bottom. The hockey stick behind.

Let me make sure elements don't overlap badly. The owl body goes down to about y=380. Text at y=450. That works.

Actually, let me reconsider - maybe put the text in an arc at the bottom following the circle, which looks more logo-like. But that requires a textPath. Let me use a simple arc path.

Let me create a curved text path at the bottom:
```svg
<path id="bottomArc" d="M90 350 A160 160 0 0 1 410 350" fill="none"/>
<textPath href="#bottomArc" ...>OWAYO EURLERS</textPath>
```

Hmm, but the owl is there. Let me place the text in the lower arc area.

Actually, let me keep it simpler and cleaner. I'll do straight text at the bottom, and maybe "EISHOCKEY" smaller above or a decorative line.

Let me finalize. I'll write the complete SVG and review it.

Let me reconsider the whole composition to make it look professional:

1. Outer navy ring (border)
2. Inner thin light ring
3. Hockey stick diagonally behind (gold shaft, orange blade) - partially hidden by owl
4. Owl centered
5. Text "OWAYO EURLERS" at bottom in white/gold
6. Maybe "EISHOCKEY" in small letters

Let me write it all.

Actually, I realize I should double check the "no background" requirement. The user says the background should be solid or best have no background. I'll make it transparent (no background rectangle), but I can have the circular ring which is fine (it's part of the logo, not a background).

Let me write the final SVG.

Let me refine the owl and make it look good. I'll add more detail.

Final SVG:

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 500 500" width="500" height="500">
  <defs>
    <radialGradient id="eyeYellow" cx="50%" cy="45%" r="55%">
      <stop offset="0%" stop-color="#fffde7"/>
      <stop offset="55%" stop-color="#ffe082"/>
      <stop offset="100%" stop-color="#ffb300"/>
    </radialGradient>
    <linearGradient id="bodyGrad" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#8d6e63"/>
      <stop offset="100%" stop-color="#4e342e"/>
    </linearGradient>
    <linearGradient id="wingGrad" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#6d4c41"/>
      <stop offset="100%" stop-color="#3e2723"/>
    </linearGradient>
    <linearGradient id="stickGrad" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#ffca28"/>
      <stop offset="100%" stop-color="#ff8f00"/>
    </linearGradient>
  </defs>
  
  <!-- Emblem rings -->
  <circle cx="250" cy="250" r="240" fill="none" stroke="#0d1b5e" stroke-width="12"/>
  <circle cx="250" cy="250" r="222" fill="none" stroke="#f0c300" stroke-width="4"/>
  
  <!-- Hockey Stick (behind owl) -->
  <g transform="translate(318 118) rotate(24)">
    <rect x="-8" y="0" width="16" height="290" rx="8" fill="url(#stickGrad)"/>
    <path d="M0 286 L0 306 Q-3 322 -24 326 L-64 328 Q-76 328 -76 315 L-76 304 Q-76 296 -63 297 L-22 294 Q-6 293 -3 283 Z" 
          fill="#ff8f00" stroke="#c43e00" stroke-width="2"/>
  </g>
  
  <!-- Owl -->
  ...
</svg>
```

Let me continue with the owl.

Owl ears/tufts:
```svg
<path d="M168 128 L146 66 L210 112 Z" fill="url(#wingGrad)"/>
<path d="M332 128 L354 66 L290 112 Z" fill="url(#wingGrad)"/>
```

Head:
```svg
<circle cx="250" cy="188" r="96" fill="url(#bodyGrad)"/>
```

Eye patches (lighter circles around eyes):
```svg
<circle cx="210" cy="192" r="40" fill="#efe7dd"/>
<circle cx="290" cy="192" r="40" fill="#efe7dd"/>
```

Eyes yellow:
```svg
<circle cx="210" cy="192" r="34" fill="url(#eyeYellow)"/>
<circle cx="290" cy="192" r="34" fill="url(#eyeYellow)"/>
```

Pupils:
```svg
<circle cx="212" cy="192" r="15" fill="#1a1a1a"/>
<circle cx="288" cy="192" r="15" fill="#1a1a1a"/>
```

Shine:
```svg
<circle cx="206" cy="185" r="5" fill="#ffffff"/>
<circle cx="282" cy="185" r="5" fill="#ffffff"/>
```

Beak:
```svg
<path d="M234 214 Q250 206 266 214 Q270 238 250 256 Q230 238 234 214 Z" fill="#ff9800" stroke="#e65100" stroke-width="1"/>
```

Body:
```svg
<path d="M156 256 Q138 368 250 388 Q362 368 344 256 Z" fill="url(#bodyGrad)"/>
```

Chest:
```svg
<path d="M202 264 Q196 350 250 370 Q304 350 298 264 Z" fill="#e8ddcf"/>
```

Chest feathers (scutes) - small arcs:
```svg
<g stroke="#c3b09c" stroke-width="3" fill="none" stroke-linecap="round">
  <path d="M224 286 q10 8 20 0"/>
  <path d="M256 286 q10 8 20 0"/>
  <path d="M218 308 q10 8 20 0"/>
  <path d="M252 308 q10 8 20 0"/>
  <path d="M224 330 q10 8 20 0"/>
  <path d="M256 330 q10 8 20 0"/>
  <path d="M232 352 q8 6 16 0"/>
  <path d="M256 352 q8 6 16 0"/>
</g>
```

Wings:
```svg
<path d="M158 262 Q118 310 142 372 Q158 336 172 300 Q176 278 168 262 Z" fill="url(#wingGrad)"/>
<path d="M342 262 Q382 310 358 372 Q342 336 328 300 Q324 278 332 262 Z" fill="url(#wingGrad)"/>
```

Feet (optional):
```svg
<path d="M220 382 L216 400 M228 384 L228 402 M236 382 L240 400" stroke="#ff9800" stroke-width="4" stroke-linecap="round" fill="none"/>
...
```

Maybe skip feet to keep it clean, or add small feet.

Text:
```svg
<text x="250" y="462" font-family="'Arial Black', Arial, sans-serif" font-size="44" font-weight="bold" letter-spacing="2" text-anchor="middle" fill="#ffffff">OWAYO EURLERS</text>
```

Hmm wait, "OWAYO EURLERS" - the team is "Owayo Eulers". Let me keep the spelling: "OURLERS" not "EURLERS". The user wrote "Eulers" (German for owls). So "OWAYO EURLERS"? No. "Eulers" -> "EURLERS". Let me write "OWAYO EURLERS".

Wait, "Eulers" is the plural-ish of "Euler" (owl in German is "Eule"). So the team is "Owayo Eulers". In caps: "OWAYO EURLERS". Let me use that.

Actually, let me keep it as "OWAYO EURLERS" - capitalizing each letter. O-W-A-Y-O space E-U-R-L-E-R-S. Yes, "OURLERS"? No: E-U-R-L-E-R-S = "EURLERS". Yes.

Let me finalize the text as "OWAYO EURLERS".

Let me also add a subtitle "EISHOCKEY" maybe. Or a small decorative element. Let me add "EISHOCKEY" in small letters above the main text or as part of the top arc.

Actually, let me add top text "EISHOCKEY CLUB" or just keep it clean. Let me add "EISHOCKEY" small at the top arc and "OWAYO EURLERS" at the bottom, OR main text straight at bottom.

Let me do:
- Top arc text: "EISHOCKEY"
- Bottom straight text: "OWAYO EURLERS"

Hmm, that might be cluttered. Let me just do the main name prominently and add a small "EISHOCKEY" subtitle.

Let me reconsider. A clean logo:
- Owl + hockey stick in center
- "OWAYO EURLERS" as the main text at the bottom
- Maybe a small star or puck decorative element

Let me add a hockey puck too, actually. That reinforces the hockey theme. A black disc. Maybe near the bottom or as part of design.

Let me finalize. I'll write it out and make sure it's valid.

Let me reconsider the stick blade path - I want it to look like a hockey stick blade. Let me simplify.

A hockey stick blade from the side looks like: the shaft comes down and the blade extends forward and curves up at the toe. Let me make:

```svg
<path d="M0 286 L0 300 Q-2 314 -20 316 L-58 318 Q-70 318 -70 306 L-70 298 Q-70 292 -58 293 L-18 291 Q-4 290 -1 283 Z" 
      fill="#ff8f00" stroke="#c43e00" stroke-width="2"/>
```

This makes a blade with a bottom, toe curve, and heel. Should look reasonable.

Actually, let me reconsider the stick orientation. I rotated it 24 degrees. The shaft goes from (0,0) to (0,286) in local coords, translated to (318,118) and rotated. So the top of the stick is at around (318,118) and it goes down-right. The blade is at the bottom.

Hmm, with rotation 24 degrees clockwise, the stick tilts. Let me make sure the blade ends up at the bottom near the ground.

Actually, this is hard to visualize. Let me just place the stick and trust the coordinates. Let me use a smaller rotation or make it vertical with the blade at bottom-left.

Let me reconsider: maybe place the stick behind the owl, mostly vertical, tilted slightly, with blade at bottom. The owl covers the middle part.

Let me set the stick group: translate to (300, 100), rotate 18 degrees.
- Shaft: rect x=-8 y=0 w=16 h=300
- Blade at y=290ish

After rotation 18° and translate (300,100):
- Top of shaft: (300,100)
- Bottom of shaft before blade: (300,400) rotated... 

The rotation is around origin (0,0) of the group which is at (300,100). So a point (0, 300) becomes (300 + 300*sin(18°), 100 + 300*cos(18°)) = (300 + 92.7, 100 + 285.7) = (392.7, 385.7). So the bottom of the stick is at around (393, 386), to the lower right. The blade would extend further right.

That places the stick going from upper-left (300,100) to lower-right (393,386). The blade at the lower right. That could look good, crossing behind the owl.

Hmm, but I want the blade near the bottom. Let me adjust.

Actually, let me make the stick more vertical and let the blade point down. Let me not rotate much.

Let me do: translate (320, 90), rotate 10 degrees.
- Shaft from (320,90) to ~(320+300*sin10, 90+300*cos10) = (320+52, 90+295) = (372, 385)
- Blade below that.

OK let me just go with it. The exact positioning doesn't need to be perfect; it'll look like a hockey stick behind the owl.

Actually, let me reconsider and make the design cleaner by having the hockey stick clearly visible on one side. Let me place it on the right side, vertical-ish, with the blade curving at the bottom right.

Let me just write it and see. I'll finalize.

Let me also reconsider: should the owl hold the stick? That's harder. Let me just have it behind.

Let me write the complete final SVG now.

I'll also add subtle details like eyebrow ridges for the owl to give character.

Let me write:

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 500 500" width="500" height="500">
  <defs>
    <radialGradient id="eyeYellow" cx="50%" cy="45%" r="55%">
      <stop offset="0%" stop-color="#fffde7"/>
      <stop offset="55%" stop-color="#ffe082"/>
      <stop offset="100%" stop-color="#ffb300"/>
    </radialGradient>
    <linearGradient id="bodyGrad" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#8d6e63"/>
      <stop offset="100%" stop-color="#4e342e"/>
    </linearGradient>
    <linearGradient id="wingGrad" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#6d4c41"/>
      <stop offset="100%" stop-color="#3e2723"/>
    </linearGradient>
    <linearGradient id="stickGrad" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#ffca28"/>
      <stop offset="100%" stop-color="#ff8f00"/>
    </linearGradient>
  </defs>
  
  <!-- Emblem rings -->
  <circle cx="250" cy="250" r="240" fill="none" stroke="#0d1b5e" stroke-width="12"/>
  <circle cx="250" cy="250" r="224" fill="none" stroke="#f4c200" stroke-width="4"/>
  
  <!-- Hockey Stick -->
  <g transform="translate(318 96) rotate(16)">
    <rect x="-8" y="0" width="16" height="300" rx="8" fill="url(#stickGrad)"/>
    <path d="M0 288 L0 304 Q-2 320 -22 323 L-62 325 Q-74 325 -74 312 L-74 302 Q-74 294 -61 295 L-20 293 Q-4 292 -1 284 Z"
          fill="#ff8f00" stroke="#b33600" stroke-width="2"/>
  </g>
  
  <!-- Owl -->
  <!-- ear tufts -->
  <path d="M166 130 L142 64 L212 110 Z" fill="url(#wingGrad)"/>
  <path d="M334 130 L358 64 L288 110 Z" fill="url(#wingGrad)"/>
  
  <!-- head -->
  <circle cx="250" cy="188" r="97" fill="url(#bodyGrad)"/>
  
  <!-- eye patches -->
  <circle cx="208" cy="192" r="41" fill="#efe7dd"/>
  <circle cx="292" cy="192" r="41" fill="#efe7dd"/>
  
  <!-- eyes -->
  <circle cx="208" cy="192" r="35" fill="url(#eyeYellow)"/>
  <circle cx="292" cy="192" r="35" fill="url(#eyeYellow)"/>
  
  <!-- pupils -->
  <circle cx="210" cy="192" r="16" fill="#141414"/>
  <circle cx="290" cy="192" r="16" fill="#141414"/>
  
  <!-- shine -->
  <circle cx="203" cy="185" r="5.5" fill="#ffffff"/>
  <circle cx="283" cy="185" r="5.5" fill="#ffffff"/>
  
  <!-- beak -->
  <path d="M234 214 Q250 207 266 214 Q271 240 250 258 Q229 240 234 214 Z" fill="#ff9800" stroke="#e65100" stroke-width="1"/>
  
  <!-- body -->
  <path d="M154 258 Q134 372 250 392 Q366 372 346 258 Z" fill="url(#bodyGrad)"/>
  
  <!-- chest -->
  <path d="M200 266 Q194 352 250 374 Q306 352 300 266 Z" fill="#e9dfcf"/>
  
  <!-- chest feathers -->
  <g stroke="#c3b09c" stroke-width="3" fill="none" stroke-linecap="round">
    <path d="M222 288 q10 8 20 0"/>
    <path d="M258 288 q10 8 20 0"/>
    <path d="M216 310 q10 8 20 0"/>
    <path d="M252 310 q10 8 20 0"/>
    <path d="M258 310 q10 8 20 0"/>
    <path d="M222 332 q10 8 20 0"/>
    <path d="M258 332 q10 8 20 0"/>
    <path d="M230 354 q8 6 16 0"/>
    <path d="M258 354 q8 6 16 0"/>
  </g>
  
  <!-- wings -->
  <path d="M156 264 Q116 312 140 374 Q157 336 171 300 Q176 278 168 264 Z" fill="url(#wingGrad)"/>
  <path d="M344 264 Q384 312 360 374 Q343 336 329 300 Q324 278 332 264 Z" fill="url(#wingGrad)"/>
  
  <!-- feet -->
  <g stroke="#ff9800" stroke-width="5" stroke-linecap="round" fill="none">
    <path d="M216 388 l-3 16 M224 390 l0 18 M232 388 l3 16"/>
    <path d="M268 388 l-3 16 M276 390 l0 18 M284 388 l3 16"/>
  </g>
  
  <!-- text -->
  <text x="250" y="466" font-family="'Arial Black', Arial, sans-serif" font-size="46" font-weight="bold" letter-spacing="2" text-anchor="middle" fill="#ffffff">OWAYO EURLERS</text>
  <text x="250" y="490" font-family="Arial, sans-serif" font-size="16" letter-spacing="6" text-anchor="middle" fill="#f4c200">EISHOCKEY</text>
</svg>
```

Wait, the text "EISHOCKEY" at y=490 with font-size 16 - the bottom of characters would be around 490. The viewBox is 0-500, so it fits. But the ring is at r=240, so at the bottom the ring is at y=490 (250+240). The text at y=466 and 490 might overlap with the ring border. Let me check: the inner ring is at r=224, so bottom at y=474. The text at y=466 is just inside. The main text baseline at 466, so text spans roughly 466-430 = 430 to 466. That's inside the ring. Good. The "EISHOCKEY" at 490 baseline would be at the very edge, overlapping the ring. Let me move it up a bit or make it smaller.

Actually, let me reconsider. Let me put "EISHOCKEY" at y=468 and main text... no. Let me reorganize.

Let me put:
- Main text "OWAYO EURLERS" at y=462, font-size 44
- Subtitle "EISHOCKEY" at y=486, font-size 15

But the ring bottom is at y=490. The subtitle at 486 baseline would be right at the ring. Let me reduce font-size or move up.

Hmm, let me reconsider the whole vertical layout. The owl body goes to about y=392, feet to y=406. Then text. Let me place main text baseline at 458 and subtitle at 482.

Actually, the bottom of the circle is at 250+240 = 490. So there's limited space. Let me make the text fit between y=430 and y=485.

Main text "OWAYO EURLERS" at font-size 44, baseline ~460. Text top ~425.
Subtitle "EISHOCKEY" at font-size 15, baseline ~482. Text top ~470.

That should fit. Let me adjust.

Actually, "OWAYO EURLERS" at 44px bold - width ~ 13 chars. Let me estimate: with Arial Black, average char width ~0.6em = 26px. 13 * 26 = 338px. Centered at 250, spans 81 to 419. Fits within the ring (inner radius 224, so at y=450 the ring spans x from 250-sqrt(224²-... hmm the ring is a circle, at y=450, x range is 250 ± sqrt(224² - 200²) = 250 ± sqrt(50176-40000) = 250 ± sqrt(10176) = 250 ± 100. So x from 150 to 350 at y=450. But my text spans 81 to 419, which is wider than 150-350! So it would extend beyond the ring.

Let me reduce font size. At font-size 38, width ~ 13*21 = 273px, spans 113 to 387. Still a bit wide. At 34px: ~13*18 = 234px, spans 133 to 367. Better. At 32px: ~224px, spans 138 to 362. Good.

Hmm, but I want it prominent. Let me use font-size 36 and letter-spacing. Let me estimate 36px: char width ~0.58em for Arial Black ≈ 21px. 13*21 = 273. Spans 113-387. At y=458, ring spans 250 ± sqrt(224² - 208²) = 250 ± sqrt(50176 - 43264) = 250 ± sqrt(6912) = 250 ± 83 = 167 to 333. Text 113-387 still too wide.

Hmm. Let me reconsider. Maybe reduce font to 30. 30px: ~17px/char, 13 chars = 221px, spans 140-360. Ring at y=455: 250 ± sqrt(224²-205²)= 250±sqrt(50176-42025)=250±sqrt(8151)=250±90=160-340. Text 140-360 still slightly wide.

Let me just use font-size 28 for safety: ~16px/char, 13 chars=208px, spans 146-354. Ring at y=455: 160-340. Close enough, text slightly wider at edges. Let me use 26px. Actually, let me not overthink. Let me use font-size 30 and it'll be fine, maybe slightly overlapping the ring at the very edges which is acceptable for a logo, or I'll reduce.

Actually, let me reconsider - maybe I'm overcomplicating. Let me place the text and if it's slightly wide, that's OK for a logo (text often sits inside and may touch the border). Let me use font-size 32, baseline 460.

Hmm, let me reconsider the ring radius. Maybe make the inner content area bigger by reducing border. Let me make outer ring r=240 width 14, inner ring r=222 width 3. Content area within r=222.

At y=458, inner content x-range: 250 ± sqrt(222² - 208²) = 250 ± sqrt(49284 - 43264) = 250 ± sqrt(6020) = 250 ± 77.6 = 172 to 322.

For text to fit in 172-322 (width 150) at y=458... that's narrow. Text width must be < 150. At font-size 20, Arial Black ~11px/char, 13 chars = 143px. Fits. But 20px is small.

Hmm, the issue is the text is near the bottom where the circle is narrow. Let me place the text higher up, but then it overlaps the owl.

Alternative: Use a banner/ribbon behind the text, or place text in a rectangular area.

Alternative: Make the text curved along the bottom arc (textPath on a circular arc). Curved text at the bottom can be larger because it follows the circle.

Let me use curved text. Create a path for the bottom arc and place text along it.

Bottom arc path (text along the inside bottom of the circle):
```svg
<path id="arcBottom" d="M70 300 A180 180 0 0 0 430 300" fill="none"/>
```
This creates an arc from (70,300) to (430,300) bulging downward (the bottom of a circle centered at 250,300 with radius 180). Wait, let me think. A circle centered at (250, 300) radius 180. The bottom of it is at (250, 480). An arc from (70,300) [left] to (430,300) [right] going through the bottom (250,480):

```svg
<path id="arcBottom" d="M70 300 A180 180 0 0 1 430 300" fill="none"/>
```
The flag flag=1 means clockwise. From (70,300) to (430,300)... Let me think. Center (250,300). Point (70,300) is at angle 180° (left). Point (430,300) is at angle 0° (right). Going clockwise from 180° to 0°... clockwise from left point would go up (through top, 250,120) then to right. Counterclockwise would go down (through bottom, 250,480) then to right. 

For text along the bottom, I want the arc to go through the bottom. So I need the arc dipping down. Let me use large-arc-flag=0, sweep=1 or 0. Let me just try and adjust.

Actually, curved text can be tricky to get right without testing. Let me instead use a simpler approach: place the text straight but within a banner shape, OR reduce the text size to fit.

Let me reconsider. Maybe I'll drop the circular ring constraint on text by using a banner.

Actually, you know what, let me just make the text fit with a reasonable font size and place it where it fits. Let me use a larger inner area.

New plan: Make the emblem with the owl in the upper 2/3 and text in a banner at the bottom.

Let me create a banner (ribbon) at the bottom with "OWAYO EURLERS" on it. A banner is a common logo element and gives space for text.

Banner design: a horizontal ribbon with slightly pointed ends, behind the text.

```svg
<g>
  <path d="M70 430 L430 430 L410 460 L430 490 L70 490 L90 460 Z" fill="#0d1b5e" stroke="#f4c200" stroke-width="3"/>
  <path d="M70 430 L60 445 L70 460 M430 430 L440 445 L430 460" fill="#0d1b5e"/> <!-- not needed -->
  <text x="250" y="470" font-family="..." font-size="34" font-weight="bold" text-anchor="middle" fill="#fff">OWAYO EURLERS</text>
</g>
```

Hmm, but the banner would cover the owl's feet. Let me position the banner lower, around y=440-490, and keep the owl above y=410.

Actually, let me reconsider the whole layout to avoid overlap:
- Owl: head center (250,185), body down to ~360, feet to ~380
- Banner: y=415 to y=475
- Gap between owl and banner

Let me place owl feet around y=375, banner from y=410.

Hmm, but then the owl is small relative to the circle. Let me make the owl bigger.

Let me reconsider. Circle r=240, content within r=222. 

Let me make the owl larger:
- Head center (250, 175), radius 90
- Body from y=250 to y=380
- Feet to y=400

Banner at y=415-475.

Actually the feet would be at y=400 and banner at 415, close but OK.

Let me just go with a clean layout and not stress about perfect fit. Let me write it out.

Let me reconsider using curved text since it looks more professional for a sports logo. Let me try the arc approach and make it work.

For the bottom text following the arc, I'll define a path and use textPath. Let me define the arc so text reads left-to-right along the bottom curve.

Path for bottom arc (reading left to right, curving at the bottom):
The text should be upright at the bottom center and curve up on the sides. 

A common approach:
```svg
<path id="bottomText" d="M95 440 A165 165 0 0 1 405 440" .../>
```
Wait, that curves upward (convex up). Let me think about what I want.

I want the text to sit along the bottom inner edge of the circle, so it curves like the bottom of the circle — concave up (like a U). At the center it's at the lowest point, and it rises toward the sides.

For text to read normally (upright) at the bottom center and follow a U-shape, the path should go from left, down to center, up to right. 

Path: from (90, 410) to (410, 410) curving down through (250, 470).
```svg
<path id="bottomText" d="M90 410 A170 170 0 0 0 410 410" fill="none"/>
```
Center of this arc: the chord from (90,410) to (410,410) has midpoint (250,410). Radius 170. The arc passes through (250, 470) if it dips down: distance from center to (250,470). If center of circle is at (250, 410 - d)... let me compute. For a circle of radius 170 passing through (90,410) and (410,410), the center is at (250, k) where (250-90)² + (k-410)² = 170² → 160² + (k-410)² = 170² → 25600 + (k-410)² = 28900 → (k-410)² = 3300 → k-410 = ±57.4. So center at (250, 352.6) or (250, 467.4). 

If center at (250, 352.6) (above the chord), the arc dipping below the chord (through (250,470)) would be the far arc. The point (250,470): distance from center (250,352.6) = 117.4, not 170. So (250,470) is not on this circle. Let me recompute where the bottom of this arc is.

If center at (250, 352.6), the bottom of the circle is at (250, 352.6+170) = (250, 522.6). That's outside. The arc from (90,410) to (410,410) with the lower part... hmm.

This is getting complicated. Let me just place text straight and accept a slightly wider or smaller text. It's cleaner to reason about.

DECISION: Straight text, positioned to fit, with a decorative banner behind it for style and to give clear space.

Let me finalize with a banner.

Actually, simpler: Let me just use straight text and make it fit by choosing font size carefully, and place a small decorative underline or the word "EISHOCKEY" as subtitle. No banner needed.

Let me compute for straight text at baseline y=462, font-size 30, Arial Black. Char width ≈ 0.58 * 30 = 17.4px. 13 chars (including space) = 226px. But space is narrower. Let me estimate "OWAYO EURLERS" width: O,W,A,Y,O (5) + space + E,U,R,L,E,R,S (7). Roughly 12.5 effective chars. 12.5 * 17.4 = 218px. Centered: spans 250-109=141 to 250+109=359. 

Ring inner radius 222, at y=462: x-range 250 ± sqrt(222² - 212²) = 250 ± sqrt(49284 - 44944) = 250 ± sqrt(4340) = 250 ± 65.9 = 184 to 316. Text spans 141-359. Text is wider than the available space (184-316). So it overflows.

I need text width < 132px (from 184 to 316). At font-size 30, that's 132/17.4 = 7.6 chars. Too small.

So straight text at the very bottom won't fit well due to the circular shape. 

Options:
1. Curved text (follows arc) - more space
2. Banner/rectangle behind text - decouples text width from circle
3. Smaller text with the circle bigger relative to text area

Let me go with a banner. A banner behind the text solves this elegantly.

Banner: horizontal ribbon. Let me make it span from x=70 to x=430 (width 360), centered, with pointed ends, positioned at y=420 to y=478.

The banner will overlap the owl's lower body/feet. To avoid that, I'll make the owl end around y=395 and start the banner at y=415.

Wait, but a banner overlapping the owl is actually common in logos (the owl "sits" on or behind the banner). Let me have the banner in front of the lower body, partially covering it. That can look good. Or I keep the owl above.

Let me design:
- Owl: head (250,175) r=88, body to y=375, feet to y=395
- Banner: y=412 to y=474, x=68 to x=432
- Text on banner: "OWAYO EURLERS" baseline y=450, font-size 34, white
- Subtitle or top text: "EISHOCKEY" somewhere

Let me also add top text "EISHOCKEY" or a small element at the top arc. Actually, let me add "EISHOCKEY · CLUB" at top or just keep it minimal.

Hmm, let me reconsider. Let me add "EISHOCKEY" as a subtitle on a separate small line or make the banner two-part.

Let me keep it clean:
- Main banner: "OWAYO EURLERS"
- Small "EISHOCKEY" above or below

Let me put "EISHOCKEY" in small letters just above the banner, centered. And maybe a small puck or stars.

OK let me just write it. I'll finalize.

Let me reconsider the banner shape. A classic ribbon banner:

```svg
<g>
  <!-- banner body -->
  <path d="M72 418 L428 418 L408 446 L428 474 L72 474 L92 446 Z" fill="#0d1b5e" stroke="#f4c200" stroke-width="4"/>
  <!-- left fold -->
  <path d="M72 418 L56 430 L72 446" fill="none" stroke="#f4c200" stroke-width="4"/>
  <!-- right fold -->
  <path d="M428 418 L444 430 L428 446" fill="none" stroke="#f4c200" stroke-width="4"/>
</g>
```

Hmm, the fold triangles. Let me make the banner ends fold behind. Actually let me simplify: just a rectangle-ish banner with slightly angled ends.

Let me do:
```svg
<path d="M68 420 L432 420 L416 446 L432 472 L68 472 L84 446 Z" .../>
```

This creates a banner with the middle pushed out at the center (416,446) giving a slight arch, and pointed ends. Actually the path: start (68,420) top-left, to (432,420) top-right, to (416,446) center-dip, to (432,472) bottom-right (pointed), to (68,472) bottom-left, to (84,446) center-dip, close. This makes a banner that's arched in the middle. Hmm, might look odd.

Let me simplify to a clean ribbon:
```svg
<path d="M70 420 L430 420 L415 446 L430 472 L70 472 L85 446 Z" fill="#0d1b5e" stroke="#f4c200" stroke-width="4"/>
```

This is a banner: top edge straight from (70,420) to (430,420). Then down-left to (415,446) — creating a notch? No. Let me think about the shape.

Points in order:
1. (70,420) - top left
2. (430,420) - top right
3. (415,446) - 
4. (430,472) - bottom right
5. (70,472) - bottom left
6. (85,446) - 

Connecting 1→2 (top edge), 2→3 (top-right to center), 3→4 (center to bottom-right point), 4→5 (bottom edge), 5→6 (bottom-left to center), 6→1 (center to top-left).

This creates a banner with the left and right ends having a "V" notch cut toward the center, giving a pennant/ribbon look. Actually it creates pointed ends where the notch points inward. Let me visualize: right side goes from top (430,420) to (415,446) to (430,472). So the right end has a point that goes inward to x=415 at the middle, then back out to 430 at bottom. That's a "swallowtail" or folded ribbon end. Yes, that looks like a ribbon. Good.

OK let me finalize. I'll write the complete SVG now and make sure it's valid.

Let me also reconsider colors for contrast. The banner is navy (#0d1b5e) with white text — good contrast. The owl is brown — good. Hockey stick gold/orange — good.

Let me write the final version.

Actually, let me reconsider whether to include the banner or go simpler. The user just wants a logo with an owl and hockey stick, team name, no background. A banner is a nice touch. Let me include it.

Let me also double-check the hockey stick is visible. It's behind the owl, coming out from behind. The shaft top is at (318,96) area and goes down-right, blade at lower right. The owl body covers the middle. So we see the top of the shaft (upper right) and the blade (lower right). That works — like the owl is holding/leaning on the stick.

Hmm, actually with the banner at the bottom covering y=420-472, the stick blade (around y=400-425 area) might be partially covered. Let me position the stick so the blade is visible. Or move the stick more to the right so it's outside the banner.

Let me reconsider stick placement. Let me put it more vertically on the right side, blade at bottom-right, mostly not overlapping the banner.

Stick group: translate(330, 100), rotate(8).
- Shaft: rect x=-8 y=0 w=16 h=310. So from (330,100) down to ~(330+310*sin8, 100+310*cos8) = (330+43, 100+306) = (373, 406).
- Blade at the end around (373, 406), extending right.

The banner is x=70-430, y=420-472. The stick blade at ~(373,406) is just above the banner. Good, visible.

But the shaft from (330,100) to (373,406) passes behind the owl's right side. The owl body spans x=154-346 at the top (y=258), narrowing. At y=300, owl body... the body path is M154 258 Q134 372 250 392 Q366 372 346 258. At y=300, the body x-range: interpolate. This is getting complicated. The shaft at x≈340-373 would be at the right edge of or outside the owl. Probably fine — stick shows on the right side of the owl.

Let me just go with it.

Actually, let me reconsider — maybe two sticks crossed behind the owl (like a hockey cross) looks cooler. But that's more complex. Let me keep one stick.

Let me also add a hockey puck near the bottom for extra hockey flavor. A black ellipse/disc. Place it at bottom center or right. Maybe at (250, 410) small. But the banner is there. Let me skip the puck to avoid clutter, or place it subtly.

OK, let me finalize the SVG. Let me write it out completely and carefully.

Let me reconsider the owl body/feet overlap with banner. Owl feet at y=395. Banner top at y=420. Gap of 25px. Good.

Let me write it:

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 500 500" width="500" height="500">
  <defs>
    <radialGradient id="eyeYellow" cx="50%" cy="45%" r="55%">
      <stop offset="0%" stop-color="#fffde7"/>
      <stop offset="55%" stop-color="#ffe082"/>
      <stop offset="100%" stop-color="#ffb300"/>
    </radialGradient>
    <linearGradient id="bodyGrad" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#8d6e63"/>
      <stop offset="100%" stop-color="#4e342e"/>
    </linearGradient>
    <linearGradient id="wingGrad" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#6d4c41"/>
      <stop offset="100%" stop-color="#3e2723"/>
    </linearGradient>
    <linearGradient id="stickGrad" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#ffca28"/>
      <stop offset="100%" stop-color="#ff8f00"/>
    </linearGradient>
  </defs>

  <!-- Emblem rings -->
  <circle cx="250" cy="250" r="240" fill="none" stroke="#0d1b5e" stroke-width="14"/>
  <circle cx="250" cy="250" r="224" fill="none" stroke="#f4c200" stroke-width="4"/>

  <!-- Hockey Stick (behind owl) -->
  <g transform="translate(330 100) rotate(8)">
    <rect x="-8" y="0" width="16" height="312" rx="8" fill="url(#stickGrad)"/>
    <path d="M0 296 L0 314 Q-2 330 -22 333 L-64 335 Q-76 335 -76 322 L-76 311 Q-76 303 -63 304 L-21 302 Q-5 301 -1 291 Z"
          fill="#ff8f00" stroke="#b33600" stroke-width="2"/>
  </g>

  <!-- Owl -->
  <!-- ear tufts -->
  <path d="M168 128 L144 60 L214 108 Z" fill="url(#wingGrad)"/>
  <path d="M332 128 L356 60 L286 108 Z" fill="url(#wingGrad)"/>

  <!-- head -->
  <circle cx="250" cy="180" r="92" fill="url(#bodyGrad)"/>

  <!-- eye patches -->
  <circle cx="206" cy="186" r="40" fill="#efe7dd"/>
  <circle cx="294" cy="186" r="40" fill="#efe7dd"/>

  <!-- eyes -->
  <circle cx="206" cy="186" r="34" fill="url(#eyeYellow)"/>
  <circle cx="294" cy="186" r="34" fill="url(#eyeYellow)"/>

  <!-- pupils -->
  <circle cx="208" cy="186" r="15" fill="#141414"/>
  <circle cx="292" cy="186" r="15" fill="#141414"/>

  <!-- shine -->
  <circle cx="201" cy="179" r="5.5" fill="#ffffff"/>
  <circle cx="285" cy="179" r="5.5" fill="#ffffff"/>

  <!-- brows -->
  <path d="M172 150 Q206 132 238 152" fill="none" stroke="#3e2723" stroke-width="6" stroke-linecap="round"/>
  <path d="M328 150 Q294 132 262 152" fill="none" stroke="#3e2723" stroke-width="6" stroke-linecap="round"/>

  <!-- beak -->
  <path d="M234 208 Q250 201 266 208 Q271 232 250 250 Q229 232 234 208 Z" fill="#ff9800" stroke="#e65100" stroke-width="1"/>

  <!-- body -->
  <path d="M158 256 Q138 368 250 386 Q362 368 342 256 Z" fill="url(#bodyGrad)"/>

  <!-- chest -->
  <path d="M202 264 Q196 348 250 368 Q304 348 298 264 Z" fill="#e9dfcf"/>

  <!-- chest feathers -->
  <g stroke="#c3b09c" stroke-width="3" fill="none" stroke-linecap="round">
    <path d="M222 286 q10 8 20 0"/>
    <path d="M258 286 q10 8 20 0"/>
    <path d="M216 308 q10 8 20 0"/>
    <path d="M252 308 q10 8 20 0"/>
    <path d="M258 308 q10 8 20 0"/>
    <path d="M222 330 q10 8 20 0"/>
    <path d="M258 330 q10 8 20 0"/>
    <path d="M230 352 q8 6 16 0"/>
    <path d="M258 352 q8 6 16 0"/>
  </g>

  <!-- wings -->
  <path d="M158 262 Q118 312 142 372 Q158 334 172 298 Q177 276 169 262 Z" fill="url(#wingGrad)"/>
  <path d="M342 262 Q382 312 358 372 Q342 334 328 298 Q323 276 331 262 Z" fill="url(#wingGrad)"/>

  <!-- feet -->
  <g stroke="#ff9800" stroke-width="5" stroke-linecap="round" fill="none">
    <path d="M216 384 l-3 16 M224 386 l0 18 M232 384 l3 16"/>
    <path d="M268 384 l-3 16 M276 386 l0 18 M284 384 l3 16"/>
  </g>

  <!-- Banner -->
  <g>
    <path d="M70 420 L430 420 L415 446 L430 472 L70 472 L85 446 Z"
          fill="#0d1b5e" stroke="#f4c200" stroke-width="4"/>
    <text x="250" y="454" font-family="'Arial Black', Arial, sans-serif" font-size="34" font-weight="bold" letter-spacing="1" text-anchor="middle" fill="#ffffff">OWAYO EURLERS</text>
  </g>

  <!-- subtitle -->
  <text x="250" y="150" font-family="Arial, sans-serif" font-size="18" letter-spacing="8" text-anchor="middle" fill="#f4c200" font-weight="bold">EISHOCKEY</text>
</svg>
```

Wait, the subtitle "EISHOCKEY" at y=150 would overlap the owl's head (head center y=180, top at y=88) and brows. The brows are at y=150. The subtitle at y=150 would be right there. Let me move it. The head top is at y=88. The ear tufts go up to y=60. Let me place "EISHOCKEY" at the top, around y=75, above the head between the ear tufts. But ear tufts are at x=144-214 and x=286-356. Center x=250, y=75 is between them and above head. That could work.

Hmm, but y=75 with the top ring at y=10 (250-240). Space between ring top (y=10) and head top (y=88). y=75 is fine. Let me place "EISHOCKEY" at y=72, font-size 18, letter-spacing 8. Width ~ 9 chars * ~13px + 8*7 spacing = 117+56 = 173px. Spans 163-337. That's within the upper area. OK.

Actually, letter-spacing adds space between each pair. "EISHOCKEY" has 9 letters, 8 gaps. 8 * 8 = 64px extra. Base width ~9*11=99. Total ~163. Spans 168-332. Fits. Good.

Let me reconsider the brows overlapping with anything. Brows at y=150, that's on the head, fine.

Let me double check the "EISHOCKEY" subtitle doesn't overlap head. Head top at y=88. Subtitle baseline y=72, so text spans ~60-72. That's above head top (88). Good gap.

Now, let me reconsider the banner text "OWAYO EURLERS" at font-size 34. Width ~ 13 chars * ~20px = 260px. Spans 120-380. Banner spans x=70-430. Fits within banner. Good.

Let me reconsider the whole composition once more. It should look like a hockey team logo with an owl.

I think this is good. Let me refine a few things:
1. The stick blade path — let me make sure it looks like a blade.
2. Add a subtle shadow or outline to owl for separation.

Actually, let me reconsider the stick. Let me make it cleaner. The blade should clearly look like a hockey stick. Let me redraw.

A hockey stick: shaft (long, thin) + blade (at bottom, flat on ground, curves up at toe).

In my rotated group, the shaft is vertical (local y from 0 to 312). The blade is at local y=296-335. The blade path:
```
M0 296 L0 314 Q-2 330 -22 333 L-64 335 Q-76 335 -76 322 L-76 311 Q-76 303 -63 304 L-21 302 Q-5 301 -1 291 Z
```
Let me trace: Start (0,296) — top of blade where shaft meets. Line to (0,314). Curve to (-2,330) — the blade dips down. Line to (-22,333), (-64,335) — the bottom (sole) of the blade going left. Curve to (-76,335)... wait I have Q-76 335 then L-76 322. Hmm. Let me redo.

Actually the blade of a hockey stick: the sole (bottom) is horizontal, the back (heel side) connects to shaft, the toe side curves up. In side view (blade pointing left in my local coords since x goes negative):

Let me define blade pointing left (negative x):
- Heel/top connects to shaft at (0, 300)
- Goes down-left along the back to the sole
- Sole is the bottom, horizontal, going left to the toe
- Toe curves up at the far left

Path (pointing left):
```
M0 292 (heel top)
L-18 296 
L-20 308 (down to sole)
L-60 312 (sole going left)
Q-74 313 -74 300 (toe curves up)
L-74 292 (toe top back up)
... 
```
This is getting confusing. Let me simplify the blade to a recognizable hockey stick blade silhouette.

Simplified hockey stick blade (side view, pointing left):
```svg
<path d="M0 294 
         L-16 298 
         L-18 312 
         L-58 314 
         Q-74 314 -74 301 
         L-74 296 
         Q-74 290 -60 290 
         L-20 288 
         Z" 
      fill="#ff8f00" stroke="#b33600" stroke-width="2"/>
```

Hmm. Let me think of it as: a thin horizontal blade. The top of the blade connects to the shaft. The blade extends forward (left) and has a slight curve at the toe.

Actually, maybe simpler: make the blade a curved hook shape:
```svg
<path d="M0 290 L0 308 L-16 310 L-54 312 Q-72 312 -70 298" 
      fill="none" stroke="#ff8f00" stroke-width="15" stroke-linecap="round"/>
```
This draws the shaft bottom into the blade as a thick line that curves up at the end. Might look like a hockey stick. But it's a stroke, not filled.

Let me use a filled blade for clarity. Let me make a proper blade shape:

The blade is like a flat paddle angled. In side view:
- It's a thin elongated shape
- One end (heel) attaches to shaft
- Other end (toe) has a rounded/curved tip

Let me make:
```svg
<path d="M-2 290 L4 290 L2 312 L-40 314 Q-70 314 -72 300 L-72 296 Q-70 290 -55 290 L-4 289 Z"
      fill="#ff8f00" stroke="#b33600" stroke-width="1.5"/>
```

Ugh, I keep fumbling. Let me just make a clean, simple blade and move on. The exact blade geometry isn't critical; a rotated shaft with a curved end reads as a hockey stick.

Let me use this blade:
```svg
<path d="M0 292 
         L6 292 
         L4 312 
         L-46 314 
         Q-74 314 -74 300 
         Q-74 292 -58 292 
         L-2 290 Z" 
      fill="#ff8f00" stroke="#b33600" stroke-width="2"/>
```

Trace: 
- (0,292) to (6,292): top edge (heel area), short
- (6,292) to (4,312): down the back/heel
- (4,312) to (-46,314): the sole (bottom), going left
- (-46,314) to (-74,300): toe curving up
- (-74,300) to (-74,292): up the toe front... wait Q-74 292 means curve to (-58,292) through control near (-74,292). So from (-74,300) curve to (-58,292). 
- (-58,292) to (-2,290): back along top to start area
- close to (0,292)

This makes a blade that's like a flat bottom with a curved toe. Should look like a hockey stick blade. OK good enough.

Let me finalize. Actually, let me reconsider — since the stick is rotated 8° and translated, and the blade is at the bottom, it should look fine.

Let me also reconsider: do I want the stick on the right? The owl's right wing is around x=342. The stick shaft at x≈330-373. So the stick is at the owl's left... no, x=330-373 is to the right of center, so it's on the owl's left side (viewer's right). The owl's right wing (viewer's left) is at x=158. So the stick is on the viewer's right, near the owl's left wing. There might be slight overlap between stick and owl's left wing. Let me move the stick a bit more right or accept overlap (stick behind owl).

Since the stick is drawn before the owl, it's behind. So even if they overlap in screen space, the stick appears behind the owl. Good. The stick top (upper right) and blade (lower right) poke out from behind the owl. That's the intended look.

Let me finalize the SVG. Let me write the complete clean version.

One more consideration: the "no background" requirement. I have no background rect, so the SVG background is transparent. Good. The rings and elements are the logo.

Let me also make sure there are no scripts or external resources. I'm using only basic shapes, gradients defined locally, and text. Good.

Let me write the final version. Let me reconsider the text font — using 'Arial Black' might not render everywhere, but it's a common fallback. Let me use a generic bold sans-serif stack: font-family="'Arial Black', 'Arial', 'Helvetica Neue', Helvetica, sans-serif". Good.

Let me finalize.

Actually, let me reconsider the overall look and add a couple more details to make it polished:
- Add a subtle outline to the owl head/body for definition
- Maybe add small stars or a puck

Let me keep it clean but add an outline to the owl elements. Actually, flat design without heavy outlines looks modern. Let me add thin outlines only where needed.

Let me reconsider the eyes — they're the focal point. Big yellow eyes with dark pupils and shine. Good.

Let me also make sure the beak is visible against the chest. Beak at y=208-250, chest at y=264+. So beak is above chest, on the face. Good.

Let me write the final SVG. I'll review for validity.

Let me reconsider the banner fold lines. I have the banner path creating pointed ends. Let me also add the "fold" triangles to make it look like a ribbon. Actually, the path I have already creates a notched/pointed end. Let me verify by tracing:

Banner path: `M70 420 L430 420 L415 446 L430 472 L70 472 L85 446 Z`
- (70,420) top-left
- L(430,420) top-right — top edge straight
- L(415,446) — goes left-down to center
- L(430,472) — goes right-down to bottom-right point
- L(70,472) — bottom edge straight (from right to left)
- L(85,446) — goes right-up to center
- Z — close to top-left (70,420)

So the right end: from (430,420) top, to (415,446) middle-in, to (430,472) bottom. This creates a "V" notch pointing left (inward) at the right end — a swallowtail/ribbon fold look. Similarly the left end has a notch at (85,446). 

This gives a ribbon banner with notched ends. Good, looks like a classic banner.

Let me finalize.

Actually, I realize the notch at (415,446) and (85,446) makes the banner edges angle inward at the middle, which is the ribbon fold effect. Good.

Now let me write out the complete final SVG and double-check all tags are closed.

Let me reconsider font sizes and positions one final time:
- "EISHOCKEY" subtitle: y=72, font-size 18, letter-spacing 8, fill gold
- "OWAYO EURLERS" main: y=454, font-size 34, fill white, on banner

Wait, banner is y=420-472. Text baseline y=454 means text is mostly above 454, spanning ~428-454. That's within the banner (420-472). Good. Actually baseline 454 with font-size 34 → text top ~428. Banner top 420. So text fits. Good. Let me maybe center vertically: banner center y=446. Text baseline should be around 450 for vertical centering of ~34px text (text spans 416-450). Let me use baseline 450.

Hmm, let me use y=451 for the main text.

Let me finalize with y=451.

Let me write the final SVG now.

Actually, I want to double-check the stick blade will be visible and not too weird. Let me reconsider placing it. Let me reduce rotation to make it more vertical so the blade is clearly at the bottom.

Stick: translate(335, 95), rotate(6).
- Shaft: x=-8 y=0 w=16 h=315. Local bottom at (0,315).
- After rotation 6°: (335 + 315*sin6, 95 + 315*cos6) = (335+32.9, 95+313.1) = (368, 408).
- Blade at local y=290-314, so at the end around (368, 408), extending left (negative x) to about (368-70*cos6, 408-70*sin6)... roughly (368-69, 408-7) = (299, 401). Hmm, the blade extends back toward the center-left. That might overlap the owl body more.

Let me reconsider. The blade points in the -x direction locally. After rotation, -x locally points to... rotating by 6° clockwise, the local -x axis points to (cos(180+6), sin(180+6)) = (-cos6, -sin6) direction? This is getting complicated.

Let me simplify: I'll make the stick vertical (no rotation or minimal) and place the blade at the bottom. Let me use translate(340, 90), rotate(3). Then the stick is nearly vertical, blade at bottom-right around (340, 400). The blade extends left slightly. Should be fine, mostly behind the owl's right side.

Actually, let me just go with rotate(10) and translate(335, 95). It'll look fine. Let me not overthink the exact blade position.

Hmm, let me reconsider — maybe I should make the stick NOT behind but clearly visible in front on one side, held by the owl. But "held" is hard. Let me keep it behind, peeking out. That's a common and clean look.

Final decision: stick behind, vertical-ish, blade at lower area. Let me write it.

Let me write the complete SVG:

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 500 500" width="500" height="500">
  <defs>
    <radialGradient id="eyeYellow" cx="50%" cy="45%" r="55%">
      <stop offset="0%" stop-color="#fffde7"/>
      <stop offset="55%" stop-color="#ffe082"/>
      <stop offset="100%" stop-color="#ffb300"/>
    </radialGradient>
    <linearGradient id="bodyGrad" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#8d6e63"/>
      <stop offset="100%" stop-color="#4e342e"/>
    </linearGradient>
    <linearGradient id="wingGrad" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#6d4c41"/>
      <stop offset="100%" stop-color="#3e2723"/>
    </linearGradient>
    <linearGradient id="stickGrad" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#ffca28"/>
      <stop offset="100%" stop-color="#ff8f00"/>
    </linearGradient>
  </defs>

  <!-- Emblem rings -->
  <circle cx="250" cy="250" r="240" fill="none" stroke="#0d1b5e" stroke-width="14"/>
  <circle cx="250" cy="250" r="224" fill="none" stroke="#f4c200" stroke-width="4"/>

  <!-- Hockey Stick (behind owl) -->
  <g transform="translate(335 95) rotate(10)">
    <rect x="-8" y="0" width="16" height="315" rx="8" fill="url(#stickGrad)"/>
    <path d="M0 292 L6 292 L4 314 L-46 316 Q-74 316 -74 301 L-74 296 Q-72 290 -56 290 L-2 289 Z"
          fill="#ff8f00" stroke="#b33600" stroke-width="2"/>
  </g>

  <!-- Owl -->
  ...
</svg>
```

OK let me just write the whole thing out cleanly now. I've planned enough.

Let me reconsider the blade path once more. I want it to look like a hockey stick blade. Let me make it a clean filled shape:

The blade (local coords, shaft coming from top at x=0):
- The blade extends to the left (negative x) and slightly down.
- Top edge of blade connects near the shaft.
- Bottom edge (sole) is at the bottom.
- Toe at the far left curves.

Let me define:
```
M0 290      <- top near shaft (heel top)
L-4 314     <- down the heel to sole level
L-50 316    <- along the sole to the toe
Q-74 316 -74 300  <- toe rounds up
L-74 292    <- up the front of the toe
Q-72 288 -58 288  <- back edge near top
L-2 289     <- back to near shaft
Z
```

Hmm, let me simplify to avoid a messy shape. Let me just use:
```
M0 290 L-2 314 L-52 316 Q-74 316 -72 298 L-72 292 Q-70 288 -54 288 L-1 289 Z
```

This should make a reasonable blade. Let me go with it.

Actually, I worry the blade might look odd. Let me make it more clearly a hockey stick by using a simpler, bolder blade. Let me use a thick stroked path for the whole stick (shaft + blade) instead of separate filled shapes. That's cleaner:

```svg
<g transform="translate(335 95) rotate(10)">
  <path d="M0 0 L0 290 Q0 316 -26 320 L-64 322" 
        fill="none" stroke="#ff8f00" stroke-width="16" stroke-linecap="round"/>
</g>
```

This draws: from (0,0) down to (0,290), then curve to (-26,320), then to (-64,322). With thick stroke, this is a stick with a curved blade at the end. The blade curves up at the toe. This is cleaner and looks like a hockey stick!

Let me use this approach. The stroke-linecap="round" makes ends rounded.

But wait, the shaft should be a consistent width. The path from (0,0) to (0,290) is the shaft (vertical), then the curve to (-64,322) is the blade. With uniform stroke-width 16, it looks like a hockey stick. 

Let me refine the blade curve: after the shaft reaches (0,290), the blade should extend forward and the toe curves up. Let me do:
```
M0 0 L0 288 L-8 300 Q-14 320 -40 322 L-66 322
```
Hmm. Let me think about the blade shape. A hockey stick blade in side view: the shaft comes down, then there's a "heeled" section that angles forward and down to the sole, the sole runs forward, then the toe curves up.

For a stylized version:
```
M0 0 (top of shaft)
L0 280 (shaft down)
L-6 300 (start of blade, angle forward-down)
L-50 304 (sole, running forward)
Q-72 304 -72 290 (toe curves up)
L-72 284 (top of toe)
```
Then the blade is the outline. But as a single stroked path, I'd draw the centerline. Let me just draw:
```
M0 0 L0 288 Q-2 304 -18 308 L-58 310 Q-72 310 -70 296
```
with stroke-width 16. This gives shaft + a blade that extends forward and the toe rounds. 

Let me go with:
```svg
<g transform="translate(335 95) rotate(10)">
  <path d="M0 0 L0 286 Q-2 304 -20 308 L-60 310 Q-74 310 -72 296"
        fill="none" stroke="#ff8f00" stroke-width="15" stroke-linecap="round"/>
</g>
```

This is cleaner. The blade is the curved part. Good.

Hmm, but with round linecaps, the top of the shaft (0,0) is rounded, which is fine (stick top). And the blade end is rounded.

Let me use this. It's simpler and looks like a hockey stick.

Actually, let me add a second thinner line or highlight to the shaft for style. Nah, keep it simple.

Let me also reconsider: maybe draw the stick with a filled shape so it has a nice look. But stroked is fine and simple.

Final stick:
```svg
<g transform="translate(335 95) rotate(10)">
  <path d="M0 0 L0 286 Q-2 304 -20 308 L-60 310 Q-74 310 -72 296"
        fill="none" stroke="#ff8f00" stroke-width="15" stroke-linecap="round"/>
</g>
```

Wait, but I want the stick to look like it has a proper blade (flat bottom). The curve Q-74 310 -72 296 makes the toe curve up, and the sole is roughly at y=310 from x=-60 to x=-72. Actually the last segment L-60 310 Q-74 310 -72 296: from (-60,310) curve to (-72,296) with control point (-74,310). So it goes from (-60,310) up to (-72,296), curving. The bottom (sole) is the line from (-20,308) to (-60,310), roughly horizontal. Good, that's the sole. Then toe curves up. Looks like a hockey stick blade. 

Let me finalize.

Now let me write the complete SVG with all owl parts.

Let me assemble and review:

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 500 500" width="500" height="500">
  <defs>
    <radialGradient id="eyeYellow" cx="50%" cy="45%" r="55%">
      <stop offset="0%" stop-color="#fffde7"/>
      <stop offset="55%" stop-color="#ffe082"/>
      <stop offset="100%" stop-color="#ffb300"/>
    </radialGradient>
    <linearGradient id="bodyGrad" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#8d6e63"/>
      <stop offset="100%" stop-color="#4e342e"/>
    </linearGradient>
    <linearGradient id="wingGrad" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#6d4c41"/>
      <stop offset="100%" stop-color="#3e2723"/>
    </linearGradient>
    <linearGradient id="stickGrad" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#ffca28"/>
      <stop offset="100%" stop-color="#ff8f00"/>
    </linearGradient>
  </defs>

  <!-- Emblem rings -->
  <circle cx="250" cy="250" r="240" fill="none" stroke="#0d1b5e" stroke-width="14"/>
  <circle cx="250" cy="250" r="224" fill="none" stroke="#f4c200" stroke-width="4"/>

  <!-- Hockey Stick (behind owl) -->
  <g transform="translate(335 95) rotate(10)">
    <path d="M0 0 L0 286 Q-2 304 -20 308 L-60 310 Q-74 310 -72 296"
          fill="none" stroke="#ff8f00" stroke-width="15" stroke-linecap="round"/>
  </g>

  <!-- Owl -->
  <!-- ear tufts -->
  <path d="M168 128 L144 60 L214 108 Z" fill="url(#wingGrad)"/>
  <path d="M332 128 L356 60 L286 108 Z" fill="url(#wingGrad)"/>

  <!-- head -->
  <circle cx="250" cy="180" r="92" fill="url(#bodyGrad)"/>

  <!-- eye patches -->
  <circle cx="206" cy="186" r="40" fill="#efe7dd"/>
  <circle cx="294" cy="186" r="40" fill="#efe7dd"/>

  <!-- eyes -->
  <circle cx="206" cy="186" r="34" fill="url(#eyeYellow)"/>
  <circle cx="294" cy="186" r="34" fill="url(#eyeYellow)"/>

  <!-- pupils -->
  <circle cx="208" cy="186" r="15" fill="#141414"/>
  <circle cx="292" cy="186" r="15" fill="#141414"/>

  <!-- shine -->
  <circle cx="201" cy="179" r="5.5" fill="#ffffff"/>
  <circle cx="285" cy="179" r="5.5" fill="#ffffff"/>

  <!-- brows -->
  <path d="M170 148 Q206 128 238 150" fill="none" stroke="#3e2723" stroke-width="7" stroke-linecap="round"/>
  <path d="M330 148 Q294 128 262 150" fill="none" stroke="#3e2723" stroke-width="7" stroke-linecap="round"/>

  <!-- beak -->
  <path d="M234 208 Q250 201 266 208 Q271 232 250 250 Q229 232 234 208 Z" fill="#ff9800" stroke="#e65100" stroke-width="1"/>

  <!-- body -->
  <path d="M158 256 Q138 368 250 386 Q362 368 342 256 Z" fill="url(#bodyGrad)"/>

  <!-- chest -->
  <path d="M202 264 Q196 348 250 368 Q304 348 298 264 Z" fill="#e9dfcf"/>

  <!-- chest feathers -->
  <g stroke="#c3b09c" stroke-width="3" fill="none" stroke-linecap="round">
    <path d="M222 286 q10 8 20 0"/>
    <path d="M258 286 q10 8 20 0"/>
    <path d="M216 308 q10 8 20 0"/>
    <path d="M252 308 q10 8 20 0"/>
    <path d="M258 308 q10 8 20 0"/>
    <path d="M222 330 q10 8 20 0"/>
    <path d="M258 330 q10 8 20 0"/>
    <path d="M230 352 q8 6 16 0"/>
    <path d="M258 352 q8 6 16 0"/>
  </g>

  <!-- wings -->
  <path d="M158 262 Q118 312 142 372 Q158 334 172 298 Q177 276 169 262 Z" fill="url(#wingGrad)"/>
  <path d="M342 262 Q382 312 358 372 Q342 334 328 298 Q323 276 331 262 Z" fill="url(#wingGrad)"/>

  <!-- feet -->
  <g stroke="#ff9800" stroke-width="5" stroke-linecap="round" fill="none">
    <path d="M216 384 l-3 16 M224 386 l0 18 M232 384 l3 16"/>
    <path d="M268 384 l-3 16 M276 386 l0 18 M284 384 l3 16"/>
  </g>

  <!-- Banner -->
  <g>
    <path d="M70 420 L430 420 L415 446 L430 472 L70 472 L85 446 Z"
          fill="#0d1b5e" stroke="#f4c200" stroke-width="4"/>
    <text x="250" y="451" font-family="'Arial Black', Arial, Helvetica, sans-serif" font-size="34" font-weight="bold" letter-spacing="1" text-anchor="middle" fill="#ffffff">OWAYO EURLERS</text>
  </g>

  <!-- subtitle -->
  <text x="250" y="72" font-family="Arial, Helvetica, sans-serif" font-size="18" letter-spacing="8" text-anchor="middle" fill="#f4c200" font-weight="bold">EISHOCKEY</text>
</svg>
```

Let me review this for correctness:
- All tags closed? Let me check. defs, svg, circles, path, g, text... should be fine.
- The subtitle "EISHOCKEY" at y=72 — is it above the head? Head top at y=180-92=88. So y=72 is above 88. Good, but the ear tufts go up to y=60. The subtitle at x=250, y=72 is between the ear tufts, above the head. Good.

Wait, actually the subtitle might overlap the top ring. Top ring at y=10. Subtitle at y=72, font-size 18, so text spans ~60-72. Ring at top is at y=10. Plenty of gap. Good.

Hmm, but is there enough space between the subtitle (y=72) and the ear tufts (which reach y=60 at their tips)? The ear tufts are at x=144-214 and 286-356. The subtitle is centered at x=250. At x=250, the ear tufts aren't there (they're at the sides). So subtitle at center x=250, y=60-72 doesn't overlap ear tufts. Good.

Let me reconsider the banner text width. "OWAYO EURLERS" at font-size 34, Arial Black. Let me estimate width. Arial Black avg char width ~0.62em = 21px. 13 chars = 273px. But space is ~0.3em. Let me estimate total ~260px. Banner spans x=70-430 = 360px wide. Text 260px centered fits with ~50px margin each side. Good.

Actually, let me double check the text doesn't extend beyond the banner's notched ends. The banner ends at x=70 and x=430 (with notches at x=85 and x=415). Text spans 250±130 = 120-380. Within 70-430. Good.

Let me reconsider the overall visual balance. The owl is large and centered. The stick pokes out on the right. The banner at the bottom with the name. The subtitle at top. Looks like a cohesive logo.

I think this is good. Let me make a few refinements:
1. Add a subtle stroke to the head for definition.
2. Maybe add small "stars" or keep minimal.

Let me add a thin darker outline to the owl body and head to make it pop:
Actually, flat design is fine. But a subtle outline helps separation from background. Let me add stroke to head and body.

Hmm, adding strokes to all elements increases complexity. Let me add a subtle stroke to the head and body only.

Actually, let me add a subtle darker edge to give depth. Let me add to the head:
```svg
<circle cx="250" cy="180" r="92" fill="url(#bodyGrad)" stroke="#3e2723" stroke-width="2"/>
```
And body similarly. And chest, wings. Let me add light strokes.

Let me add stroke="#3e2723" stroke-width="2" to head, body, wings. Eye patches and eyes no stroke.

Let me refine. Actually, let me keep it clean and just add stroke to head and body for definition.

Let me also reconsider: the eyes are big and the focal point. Good.

Let me finalize with subtle strokes.

Final version:

Let me write it out. I'll add stroke to head and body.

Actually, I realize I should double-check: does the design clearly show an owl AND a hockey stick? Yes: owl (eyes, beak, body, wings, ear tufts) + hockey stick (shaft + blade). Good.

Team name "OWAYO EURLERS" present. Subtitle "EISHOCKEY". No background (transparent). Good.

Let me write the final answer.

Let me reconsider one thing: the user wrote "Owayo Eulers". I'm capitalizing to "OWAYO EURLERS". That should be fine for a logo. But let me double-check the spelling: E-U-R-L-E-R-S. "Eulers" → "EURLERS". Yes.

Let me finalize.

Actually, let me reconsider the subtitle placement and whether "EISHOCKEY" at the top looks good. Alternatively, I could put "EISHOCKEY" as part of a top arc or just above the banner. Let me keep it at the top, it's fine.

Hmm, one concern: with "EISHOCKEY" at top and "OWAYO EURLERS" at bottom, and the owl in the middle, it's a balanced composition. Good.

Let me write the final SVG.

Let me also add a small hockey puck for extra theme, placed at bottom center just above/behind banner, or not. Let me skip to avoid clutter. Actually, a small puck could look nice. Let me add a small black disc near the bottom right or left of the banner. Hmm, might clutter. Let me skip.

Let me finalize and write the answer.

Let me reconsider the gradient for the stick — I defined stickGrad but now use a solid stroke for the stick. Let me remove stickGrad or keep it (unused gradients are fine but let me remove to be clean). Actually, let me keep the stick as a gradient by using a different approach, or just remove stickGrad. Let me remove stickGrad since I'm using solid color for the stick. Actually, a gradient on the stick would look nicer (metallic). But with a stroked path, I can't easily use a linear gradient that follows the path. Let me just use solid orange for the stick. Remove stickGrad.

Wait, actually I could keep stickGrad unused — it won't break anything. But cleaner to remove. Let me remove it.

Let me write the final SVG now.

Let me reconsider the eyes shine position. Pupils at (208,186) and (292,186). Shine at (201,179) and (285,179) — upper left of each pupil. That gives a light source from upper-left. Consistent. Good.

Let me finalize.

Also, let me reconsider the brows — they're above the eyes, giving the owl a determined look. Good.

Let me write the final answer.

Let me reconsider whether the owl body path looks right:
`M158 256 Q138 368 250 386 Q362 368 342 256 Z`
- Start (158,256) — left shoulder
- Quadratic to (250,386) with control (138,368) — the left/bottom curve, control pulls toward lower-left
- Quadratic to (342,256) with control (362,368) — the right/bottom curve, control pulls toward lower-right
- Close to (158,256)

This creates a rounded body that's wider at top (shoulders) and rounded at the bottom. Looks like an owl body. Good.

Chest path:
`M202 264 Q196 348 250 368 Q304 348 298 264 Z`
- Start (202,264) left
- Quad to (250,368) control (196,348) — bottom-left curve
- Quad to (298,264) control (304,348) — bottom-right curve
- Close

This is a shield/oval chest shape, lighter colored, on the belly. Good.

Chest feathers (the q paths) are small arcs within the chest. Good.

Alright, I'm confident. Let me write the final answer.

Let me make one final check on the "no background" — I have no <rect> background and no fill on svg. The background will be transparent. The only fills are the logo elements. Good.

Let me write it.

Actually, let me reconsider adding a subtle outer glow or making the rings nicer. The outer ring is navy width 14, inner ring gold width 4. That frames the logo nicely. Good.

Let me also make sure the colors work together: navy (#0d1b5e), gold (#f4c200), brown owl (#8d6e63/#4e342e), orange beak/stick (#ff9800/#ff8f00), white text. Classic hockey team palette. Good.

Final answer below.

Let me write it cleanly with comments.

I'll present just the SVG in a code block as requested.

### Antwort



```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 500 500" width="500" height="500">
  <defs>
    <radialGradient id="eyeYellow" cx="50%" cy="45%" r="55%">
      <stop offset="0%" stop-color="#fffde7"/>
      <stop offset="55%" stop-color="#ffe082"/>
      <stop offset="100%" stop-color="#ffb300"/>
    </radialGradient>
    <linearGradient id="bodyGrad" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#8d6e63"/>
      <stop offset="100%" stop-color="#4e342e"/>
    </linearGradient>
    <linearGradient id="wingGrad" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#6d4c41"/>
      <stop offset="100%" stop-color="#3e2723"/>
    </linearGradient>
  </defs>

  <!-- Emblem rings -->
  <circle cx="250" cy="250" r="240" fill="none" stroke="#0d1b5e" stroke-width="14"/>
  <circle cx="250" cy="250" r="224" fill="none" stroke="#f4c200" stroke-width="4"/>

  <!-- Hockey Stick (behind owl) -->
  <g transform="translate(335 95) rotate(10)">
    <path d="M0 0 L0 286 Q-2 304 -20 308 L-60 310 Q-74 310 -72 296"
          fill="none" stroke="#ff8f00" stroke-width="15" stroke-linecap="round"/>
  </g>

  <!-- Owl -->
  <!-- ear tufts -->
  <path d="M168 128 L144 60 L214 108 Z" fill="url(#wingGrad)"/>
  <path d="M332 128 L356 60 L286 108 Z" fill="url(#wingGrad)"/>

  <!-- head -->
  <circle cx="250" cy="180" r="92" fill="url(#bodyGrad)" stroke="#3e2723" stroke-width="2"/>

  <!-- eye patches -->
  <circle cx="206" cy="186" r="40" fill="#efe7dd"/>
  <circle cx="294" cy="186" r="40" fill="#efe7dd"/>

  <!-- eyes -->
  <circle cx="206" cy="186" r="34" fill="url(#eyeYellow)"/>
  <circle cx="294" cy="186" r="34" fill="url(#eyeYellow)"/>

  <!-- pupils -->
  <circle cx="208" cy="186" r="15" fill="#141414"/>
  <circle cx="292" cy="186" r="15" fill="#141414"/>

  <!-- shine -->
  <circle cx="201" cy="179" r="5.5" fill="#ffffff"/>
  <circle cx="285" cy="179" r="5.5" fill="#ffffff"/>

  <!-- brows -->
  <path d="M170 148 Q206 128 238 150" fill="none" stroke="#3e2723" stroke-width="7" stroke-linecap="round"/>
  <path d="M330 148 Q294 128 262 150" fill="none" stroke="#3e2723" stroke-width="7" stroke-linecap="round"/>

  <!-- beak -->
  <path d="M234 208 Q250 201 266 208 Q271 232 250 250 Q229 232 234 208 Z" fill="#ff9800" stroke="#e65100" stroke-width="1"/>

  <!-- body -->
  <path d="M158 256 Q138 368 250 386 Q362 368 342 256 Z" fill="url(#bodyGrad)" stroke="#3e2723" stroke-width="2"/>

  <!-- chest -->
  <path d="M202 264 Q196 348 250 368 Q304 348 298 264 Z" fill="#e9dfcf"/>

  <!-- chest feathers -->
  <g stroke="#c3b09c" stroke-width="3" fill="none" stroke-linecap="round">
    <path d="M222 286 q10 8 20 0"/>
    <path d="M258 286 q10 8 20 0"/>
    <path d="M216 308 q10 8 20 0"/>
    <path d="M252 308 q10 8 20 0"/>
    <path d="M258 308 q10 8 20 0"/>
    <path d="M222 330 q10 8 20 0"/>
    <path d="M258 330 q10 8 20 0"/>
    <path d="M230 352 q8 6 16 0"/>
    <path d="M258 352 q8 6 16 0"/>
  </g>

  <!-- wings -->
  <path d="M158 262 Q118 312 142 372 Q158 334 172 298 Q177 276 169 262 Z" fill="url(#wingGrad)" stroke="#3e2723" stroke-width="2"/>
  <path d="M342 262 Q382 312 358 372 Q342 334 328 298 Q323 276 331 262 Z" fill="url(#wingGrad)" stroke="#3e2723" stroke-width="2"/>

  <!-- feet -->
  <g stroke="#ff9800" stroke-width="5" stroke-linecap="round" fill="none">
    <path d="M216 384 l-3 16 M224 386 l0 18 M232 384 l3 16"/>
    <path d="M268 384 l-3 16 M276 386 l0 18 M284 384 l3 16"/>
  </g>

  <!-- Banner -->
  <g>
    <path d="M70 420 L430 420 L415 446 L430 472 L70 472 L85 446 Z"
          fill="#0d1b5e" stroke="#f4c200" stroke-width="4"/>
    <text x="250" y="452" font-family="'Arial Black', Arial, Helvetica, sans-serif" font-size="34" font-weight="bold" letter-spacing="1" text-anchor="middle" fill="#ffffff">OWAYO EURLERS</text>
  </g>

  <!-- subtitle -->
  <text x="250" y="72" font-family="Arial, Helvetica, sans-serif" font-size="18" letter-spacing="8" text-anchor="middle" fill="#f4c200" font-weight="bold">EISHOCKEY</text>
</svg>
```
