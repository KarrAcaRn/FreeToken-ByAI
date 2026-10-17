# qwen3_8-27b - logo-owayo-eulers (2026-10-17T20:28:56)

## Antwort (2574 Tokens, 53.68 s, Ende: stop)

### Denkphase

The user is asking for an SVG logo for the ice hockey team "Owayo Eulers" featuring an owl and a hockey stick, with a transparent background. Create an SVG with a circular emblem, owl (head with eyes and beak), hockey stick, and text around it or below it. Keep it self-contained.

Design: circular badge (but "no background" — is a transparent badge ring acceptable? It's better to use a circular outline). Owl face at the center, crossed hockey stick behind it, text on a banner "OWAYO EULERS".

Let's build the SVG:
- viewBox 0 0 400 400
- Crossed sticks: two lines with a blade at the bottom, drawn behind the owl.
- Owl: circular head, two large eyes, beak, ear tufts, body.
- Text on an arc via textPath, or simply horizontal text "OWAYO EULERS" below.

Keep it moderate. Use gradients? No problem, keep colors flat.

Sticks: group rotated ±25 degrees, shaft is rect, blade is path.

Owl:
- Head circle at (200,180) with radius about 90
- Ear tufts: triangles on top
- Eyes: white circles at (165,165) and (235,165) r=30, pupils r=14
- Beak: downward-pointing triangle at (200,205)
- Body below: ellipse.

Text: "OWAYO EULERS" at the bottom, possibly on a banner path with textPath. Easier way: just horizontal text.

Use textPath on an arc for a sporty look. Provide a font-family fallback.

Let's write the SVG:

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 420" ...>
```

Colors: navy #1b2a4a, gold #f0b429, white, ice blue #a8d8f0.

Sticks: group transform translate(200,190), rotate(±28). Shaft: rect x=-7 y=-150 width=14 height=230 rx=6 fill #8a5a2b; blade: path with a horizontal foot: M -7 80 L 55 80 L 55 110 L -7 110 Z ... actually, is the blade at the bottom of the rotated group? A hockey stick's blade extends laterally from the bottom of the shaft. Path: M -7 70 L -7 105 L 60 105 Q 70 105 70 95 L 70 95 ... more simply: blade shape M -7 75 L -7 108 L 62 108 Q 72 108 72 96 L 72 88 Q 40 88 -7 75? Hmm. Just do this simply: M -7 75 L 65 90 L 65 115 L -7 100 Z — a slanted blade. Good enough.

Two sticks: left rotated -25, right rotated 25, with blades outward at the bottom.

Owl on top:
- Ear tufts: path M 130 120 L 150 70 L 175 115 Z and mirror M 270 120 L 250 70 L 225 115 Z, fill navy.
- Head: circle cx 200 cy 185 r 85 fill #4a6fa5? Make the owl navy #24365e with a lighter face.
- Face disks: two overlapping white circles at (167,180) and (233,180) r 34.
- Pupils r 13 navy, with small white highlights.
- Beak: path M 200 205 L 185 190 L 215 190 Z downward-pointing triangle: M 188 192 L 212 192 L 200 218 Z fill gold.
- Body: path/ellipse below the head cx200 cy 290 rx 60 ry 45, but the bottom might be covered by the banner. Add a wing detail.

Banner: arc path M 60 320 Q 200 360 340 320, band: fill a path, place text on top of it. Use a ribbon shape:
path d="M 50 315 Q 200 355 350 315 L 350 355 Q 200 395 50 355 Z" fill gold, and place textPath text on the centerline.

Text font-size 30, bold, letter-spacing.

textPath: id="arc", path M 55 342 Q 200 382 345 342, text "OWAYO EULERS" startOffset 50% text-anchor middle.

The sticks cross behind the owl, and the blade area is around y 300 near the banner. That's fine.

Add a small "ICE HOCKEY" text? Not requested; omit it or add small text. Keep it clean.

Ensure no scripts or external resources. Provide the code block.


### Antwort



```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 420" width="400" height="420">
  <!-- Owayo Eulers – Eishockey-Logo: Eule + gekreuzte Schläger -->

  <!-- Gekreuzte Eishockeyschläger (hinter der Eule) -->
  <g transform="translate(200,195)">
    <g transform="rotate(-26)">
      <rect x="-8" y="-150" width="16" height="240" rx="7" fill="#8a5a2b"/>
      <rect x="-8" y="-150" width="16" height="30" rx="7" fill="#c9924e"/>
      <path d="M -8 78 L 62 92 L 62 120 L -8 104 Z" fill="#8a5a2b"/>
    </g>
    <g transform="rotate(26)">
      <rect x="-8" y="-150" width="16" height="240" rx="7" fill="#8a5a2b"/>
      <rect x="-8" y="-150" width="16" height="30" rx="7" fill="#c9924e"/>
      <path d="M 8 78 L -62 92 L -62 120 L 8 104 Z" fill="#8a5a2b"/>
    </g>
  </g>

  <!-- Eule -->
  <g>
    <!-- Ohrfedern -->
    <path d="M 128 128 L 146 66 L 180 118 Z" fill="#24365e"/>
    <path d="M 272 128 L 254 66 L 220 118 Z" fill="#24365e"/>

    <!-- Kopf -->
    <circle cx="200" cy="185" r="86" fill="#24365e"/>

    <!-- Gesichtsscheiben -->
    <circle cx="166" cy="180" r="36" fill="#f5f1e6"/>
    <circle cx="234" cy="180" r="36" fill="#f5f1e6"/>

    <!-- Augen -->
    <circle cx="166" cy="180" r="15" fill="#24365e"/>
    <circle cx="234" cy="180" r="15" fill="#24365e"/>
    <circle cx="171" cy="175" r="5" fill="#ffffff"/>
    <circle cx="239" cy="175" r="5" fill="#ffffff"/>

    <!-- Schnabel -->
    <path d="M 184 200 L 216 200 L 200 230 Z" fill="#f0b429"/>

    <!-- Brust -->
    <path d="M 148 240 Q 200 210 252 240 L 258 300 Q 200 330 142 300 Z" fill="#3b5583"/>
    <!-- Feder-Muster auf der Brust -->
    <path d="M 175 255 Q 200 245 225 255" stroke="#f0b429" stroke-width="4" fill="none" stroke-linecap="round"/>
    <path d="M 168 280 Q 200 268 232 280" stroke="#f0b429" stroke-width="4" fill="none" stroke-linecap="round"/>
    <path d="M 172 305 Q 200 295 228 305" stroke="#f0b429" stroke-width="4" fill="none" stroke-linecap="round"/>
  </g>

  <!-- Banner mit Teamnamen -->
  <path d="M 45 312 Q 200 352 355 312 L 355 356 Q 200 396 45 356 Z" fill="#f0b429"/>
  <path d="M 45 312 Q 200 352 355 312 L 355 320 Q 200 360 45 320 Z" fill="#d1961a"/>
  <path id="nameArc" d="M 55 336 Q 200 376 345 336" fill="none"/>
  <text font-family="Arial, Helvetica, sans-serif" font-size="30" font-weight="bold"
        fill="#24365e" letter-spacing="2">
    <textPath href="#nameArc" startOffset="50%" text-anchor="middle">OWAYO EULERS</textPath>
  </text>
</svg>
```
