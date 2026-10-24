# qwen3_8-flash-next-fp4local - logo-owayo-eulers (2026-10-24T15:05:35)

## Antwort (2111 Tokens, 62.742 s, Ende: stop)

### Denkphase

The user is asking for an SVG logo of an ice hockey team "Owayo Eulers" featuring an owl and hockey sticks. A solid background or no background is preferable. Provide one complete SVG in a code block. Let's design an SVG of an owl with crossed hockey sticks behind it, plus the text "OWAYO EULERS".

Create the owl: round head, ear tufts, large eyes, beak, body, wings. Crossed hockey sticks behind the owl. Text at the bottom.

Let's write clean SVG code using gradients and such. Keep it self-contained.

Design: viewBox 0 0 400 400. Crossed hockey sticks: two lines forming an X with blades at the bottom. The owl is in the center, sitting perched. Below, an optional shield outline (none — no background). Text is "OWAYO EULERS".

Let's build the coordinates:

Hockey sticks: stick 1 goes from (80,60) to (150,300), with the blade extending to (210,320). Stick 2 is mirrored. Use a thick stroke path, color brown/tan (#8B5A2B).

Owl: body is an ellipse centered at (200,210), head is a circle at (200,150). Ear tufts are triangles. Eyes: white circles with black pupils, brows. Beak is an orange triangle. Wings are ellipses on both sides. Feet are small.

Text is at y=375: "OWAYO" in large letters, and "EULERS" below it? Or one line "OWAYO EULERS" at y=380.

Add an ice hockey stick blade with tape. Keep it simple.

Let's write the SVG.


### Antwort



```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 440" width="400" height="440">
  <!-- Gekreuzte Eishockeyschläger -->
  <g stroke-linecap="round" fill="none">
    <!-- Schläger 1 -->
    <path d="M 95 65 L 150 290" stroke="#8B5A2B" stroke-width="12"/>
    <path d="M 150 290 Q 155 315 185 318 L 235 318" stroke="#8B5A2B" stroke-width="14" stroke-linecap="round"/>
    <path d="M 205 318 L 235 318" stroke="#1a1a1a" stroke-width="14" stroke-linecap="butt"/>
    <!-- Schläger 2 -->
    <path d="M 305 65 L 250 290" stroke="#8B5A2B" stroke-width="12"/>
    <path d="M 250 290 Q 245 315 215 318 L 165 318" stroke="#8B5A2B" stroke-width="14" stroke-linecap="round"/>
    <path d="M 195 318 L 165 318" stroke="#1a1a1a" stroke-width="14" stroke-linecap="butt"/>
  </g>

  <!-- Eule -->
  <g>
    <!-- Ohren -->
    <path d="M 148 95 L 138 50 L 172 78 Z" fill="#3d3d5c"/>
    <path d="M 252 95 L 262 50 L 228 78 Z" fill="#3d3d5c"/>

    <!-- Körper -->
    <ellipse cx="200" cy="220" rx="78" ry="88" fill="#4a4a6a"/>

    <!-- Bauch -->
    <ellipse cx="200" cy="240" rx="50" ry="60" fill="#c9c9dd"/>
    <g fill="#9a9ab8">
      <path d="M 175 210 q 10 12 20 0 q 10 12 20 0 q 10 12 20 0 l -4 14 h -52 z"/>
      <path d="M 172 240 q 10 12 20 0 q 10 12 20 0 q 10 12 20 0 l -4 14 h -52 z"/>
      <path d="M 178 270 q 10 12 20 0 q 10 12 20 0 l -4 12 h -32 z"/>
    </g>

    <!-- Flügel -->
    <ellipse cx="128" cy="215" rx="22" ry="60" fill="#3d3d5c" transform="rotate(8 128 215)"/>
    <ellipse cx="272" cy="215" rx="22" ry="60" fill="#3d3d5c" transform="rotate(-8 272 215)"/>

    <!-- Kopf -->
    <circle cx="200" cy="140" r="62" fill="#4a4a6a"/>

    <!-- Gesichtsscheibe -->
    <path d="M 200 105 q -30 -12 -48 8 q -16 22 2 44 q 18 22 46 22 q 28 0 46 -22 q 18 -22 2 -44 q -18 -20 -48 -8 z" fill="#c9c9dd"/>

    <!-- Augen -->
    <circle cx="176" cy="138" r="20" fill="#f5b301"/>
    <circle cx="224" cy="138" r="20" fill="#f5b301"/>
    <circle cx="176" cy="138" r="10" fill="#1a1a1a"/>
    <circle cx="224" cy="138" r="10" fill="#1a1a1a"/>
    <circle cx="180" cy="134" r="3.5" fill="#ffffff"/>
    <circle cx="228" cy="134" r="3.5" fill="#ffffff"/>

    <!-- Augenbrauen (entschlossen) -->
    <path d="M 152 118 L 194 128" stroke="#2b2b40" stroke-width="7" stroke-linecap="round"/>
    <path d="M 248 118 L 206 128" stroke="#2b2b40" stroke-width="7" stroke-linecap="round"/>

    <!-- Schnabel -->
    <path d="M 200 148 L 190 162 L 200 180 L 210 162 Z" fill="#e8871e"/>

    <!-- Füße -->
    <g fill="#e8871e">
      <path d="M 170 300 q -8 12 -14 14 h 34 q -4 -8 -6 -14 z"/>
      <path d="M 230 300 q 8 12 14 14 h -34 q 4 -8 6 -14 z"/>
    </g>
  </g>

  <!-- Puck -->
  <ellipse cx="200" cy="336" rx="20" ry="7" fill="#1a1a1a"/>
  <rect x="180" y="330" width="40" height="6" fill="#1a1a1a"/>
  <ellipse cx="200" cy="330" rx="20" ry="7" fill="#333333"/>

  <!-- Schriftzug -->
  <text x="200" y="392" font-family="Arial, Helvetica, sans-serif" font-size="38" font-weight="bold" fill="#2b2b40" text-anchor="middle" letter-spacing="2">OWAYO</text>
  <text x="200" y="428" font-family="Arial, Helvetica, sans-serif" font-size="32" font-weight="bold" fill="#e8871e" text-anchor="middle" letter-spacing="4">EULERS</text>
</svg>
```
