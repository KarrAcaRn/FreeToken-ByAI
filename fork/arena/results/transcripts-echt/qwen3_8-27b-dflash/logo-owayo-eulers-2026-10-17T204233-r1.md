# qwen3_8-27b-dflash - logo-owayo-eulers (2026-10-17T20:42:33)

## Antwort (2354 Tokens, 18.444 s, Ende: stop)

### Denkphase

The user is asking for an SVG logo of an owl holding a hockey stick, a transparent background, and the team name "Owayo Eulers". I'll create a vector owl with crossed hockey sticks. I'll make the paths clean and handcrafted.

Design: an owl's face with big eyes, triangular ears, a beak, a body with wings, and two crossed hockey sticks behind. The text "OWAYO EULERS" on an arc or banner at the bottom.

Let me try writing the SVG. Canvas is 400x400. The owl in the center, with sticks crossed behind it.

Elements:
- Crossed hockey sticks: two lines rotated ±25°, with blades.
- Owl: head shape (two ear tufts), a circular face, big eyes, beak, body, wing detail, talons gripping the sticks.

Colors: dark blue (#1B3A5C?), gold (#E8B54A), white, dark gray.

Let me try writing the code:

Sticks: shafts as rotated rectangles. Using group with transform rotate around the center.

Stick: rect x=-6 y=-150 width=12 height=200, blade as a path at the bottom. Rotate ±30° around (200,160).

Owl: body is an ellipse cx=200 cy=170 rx=70 ry=80. Ear tufts: paths on top of the head. Eyes: white circles with dark pupils. Beak is a triangle. Brow feather pattern. Wings: curves on the sides.

Text: "OWAYO" arched on top or at the bottom; "EULERS" on a banner at the bottom. More simply: place text along an arc path using textPath, or use straight-line text on top and bottom. Use two text elements with an arc-shaped path.

Arc path for the bottom text: M 60 300 A 160 160 0 0 0 340 300? For text to follow the bottom curve, use a path with a downward-bulging arc: M 70 310 Q 200 360 330 310.

Top text: M 70 80 Q 200 40 330 80.

Using <textPath> with a path defined in defs, startOffset 50%, text-anchor middle.

Add the talons: small circles/paths over the sticks.

Alright, let me put together the SVG.


### Antwort



```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 420" width="400" height="420">
  <defs>
    <path id="topArc" d="M 55 105 Q 200 45 345 105" fill="none"/>
    <path id="bottomArc" d="M 55 320 Q 200 380 345 320" fill="none"/>
  </defs>

  <!-- ============ GEKREUZTE EISHOCKEYSCHLÄGER ============ -->
  <g stroke-linecap="round">
    <!-- Schläger links -->
    <g transform="rotate(28 200 190)">
      <rect x="194" y="30" width="12" height="290" rx="6" fill="#8C5A2B" stroke="#1B2A41" stroke-width="4"/>
      <path d="M 194 312 L 194 322 L 250 322 L 258 330 L 258 342 L 194 342 Z"
            fill="#8C5A2B" stroke="#1B2A41" stroke-width="4" stroke-linejoin="round"/>
    </g>
    <!-- Schläger rechts -->
    <g transform="rotate(-28 200 190)">
      <rect x="194" y="30" width="12" height="290" rx="6" fill="#8C5A2B" stroke="#1B2A41" stroke-width="4"/>
      <path d="M 206 312 L 206 322 L 150 322 L 142 330 L 142 342 L 206 342 Z"
            fill="#8C5A2B" stroke="#1B2A41" stroke-width="4" stroke-linejoin="round"/>
    </g>
  </g>

  <!-- ============ EULE ============ -->
  <!-- Flügel -->
  <path d="M 118 150 Q 92 190 108 248 Q 132 236 146 205 Q 142 170 118 150 Z"
        fill="#C9922E" stroke="#1B2A41" stroke-width="5" stroke-linejoin="round"/>
  <path d="M 282 150 Q 308 190 292 248 Q 268 236 254 205 Q 258 170 282 150 Z"
        fill="#C9922E" stroke="#1B2A41" stroke-width="5" stroke-linejoin="round"/>

  <!-- Körper -->
  <path d="M 200 92
           C 150 92 128 130 128 168
           C 128 232 158 272 200 272
           C 242 272 272 232 272 168
           C 272 130 250 92 200 92 Z"
        fill="#E8B54A" stroke="#1B2A41" stroke-width="6"/>

  <!-- Ohren (Federbüschel) -->
  <path d="M 148 106 L 128 58 L 178 88 Z" fill="#E8B54A" stroke="#1B2A41" stroke-width="6" stroke-linejoin="round"/>
  <path d="M 252 106 L 272 58 L 222 88 Z" fill="#E8B54A" stroke="#1B2A41" stroke-width="6" stroke-linejoin="round"/>

  <!-- Brust (Federmuster) -->
  <path d="M 200 190
           C 168 190 154 214 154 236
           C 154 262 174 272 200 272
           C 226 272 246 262 246 236
           C 246 214 232 190 200 190 Z"
        fill="#F6E2B3" stroke="#1B2A41" stroke-width="4"/>
  <g stroke="#C9922E" stroke-width="3" fill="none" stroke-linecap="round">
    <path d="M 176 214 q 8 8 16 0 q 8 8 16 0"/>
    <path d="M 170 234 q 8 8 16 0 q 8 8 16 0 q 8 8 16 0"/>
    <path d="M 178 254 q 8 8 16 0 q 8 8 16 0"/>
  </g>

  <!-- Augen -->
  <circle cx="168" cy="150" r="30" fill="#FFFFFF" stroke="#1B2A41" stroke-width="5"/>
  <circle cx="232" cy="150" r="30" fill="#FFFFFF" stroke="#1B2A41" stroke-width="5"/>
  <circle cx="172" cy="152" r="13" fill="#1B2A41"/>
  <circle cx="228" cy="152" r="13" fill="#1B2A41"/>
  <circle cx="177" cy="146" r="4.5" fill="#FFFFFF"/>
  <circle cx="233" cy="146" r="4.5" fill="#FFFFFF"/>

  <!-- Schnäbelchen -->
  <path d="M 200 168 L 184 178 L 200 200 L 216 178 Z"
        fill="#E07B39" stroke="#1B2A41" stroke-width="4" stroke-linejoin="round"/>

  <!-- Krallen, die die Schläger umfassen -->
  <g fill="#E07B39" stroke="#1B2A41" stroke-width="4" stroke-linejoin="round">
    <path d="M 168 262 q -14 18 2 30 q 14 6 18 -8 q -4 -14 -20 -22 Z"/>
    <path d="M 232 262 q 14 18 -2 30 q -14 6 -18 -8 q 4 -14 20 -22 Z"/>
  </g>
</svg>
```
