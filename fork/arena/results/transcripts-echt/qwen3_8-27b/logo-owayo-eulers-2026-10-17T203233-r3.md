# qwen3_8-27b - logo-owayo-eulers (2026-10-17T20:32:33)

## Antwort (2262 Tokens, 47.124 s, Ende: stop)

### Denkphase

Create an SVG logo: an owl + hockey stick, with the text "Owayo Eulers", transparent background. Make a stylized owl with eyes, and arrange crossed hockey sticks behind it. Use blue/white colors.

Let's design it: two crossed hockey sticks forming an X behind a circular badge... but no background. So just the owl and the sticks, and the text.

Simple approach:
- Crossed sticks: 2 rotated rectangles, one with a blade at the bottom.
- Owl: body shape (ellipse), eyes, beak, wings.
- Text "OWAYO EULERS" arched or straight, below or above.

Write the SVG with viewBox 0 0 400 400.

Sticks: rotate about 25 degrees around the center. Stick = shaft rectangle + curved blade path. Simplified: use path for each stick: vertical line from (200,60) to (200,300), blade curving at the bottom. Rotate ±25 around (200,200).

Owl on top: body ellipse center (200,190), rx 70 ry 80. Head circle. Eyes: big circles with pupils. Ear tufts. Beak triangle. Feet optional.

Colors: navy #1B3A5C, orange #E87722, white.

Text: "OWAYO EULERS" at y=360, bold font.

Owl design:
- Body path: rounded shape. Use ellipse cx=200 cy=195 rx=65 ry=75, navy fill.
- Head tufts: 2 triangles at the top.
- Face: lighter belly ellipse cx=200 cy=210 rx=40 ry=48 white.
- Eyes: 2 white circles cx=175/225 cy=165 r=22, navy pupils r=10, small highlight.
- Eye ring: orange stroke.
- Beak: downward-pointing triangle (200,180)-(190,175)-(210,175).
- Wing: side path, darker.
- Feet: 2 small orange shapes.

Sticks behind the owl: color orange, shaft slightly darker.

Stick 1 path (before rotation): shaft from x=195 to 205, y=40 to y=270; blade curves to the left: path "M195 40 h10 v230 c0 20 -10 35 -35 38 h-8 c-4 0 -6 -3 -5 -7 c2 -6 8 -9 14 -11 c16 -6 24 -12 24 -24 z" — roughly. Simpler: use a stroke-based stick: path with round linecap, stroke width 10: M200 45 L200 275 Q200 305 165 310, stroke #E87722. Then rotate the group.

Stick 1: rotate(-25 200 200); Stick 2: rotate(25 200 200), mirrored blade: M200 45 L200 275 Q200 305 235 310.

The top ends are round, the blades curve. Add slightly darker tips? Keep it simple.

Text: use textPath for arched text? Keep it straight: 2 lines "OWAYO" larger, "EULERS" below, or a single line "OWAYO EULERS". Let's go with one line, bold, navy fill, with a slight letter-spacing.

Add a subtle underline swoosh? Keep it simple.

Font: font-family="Arial, sans-serif" font-weight="bold".

Let's write it out.


### Antwort



```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 420" width="400" height="420">
  <!-- Eishockeyschläger (gekreuzt, im Hintergrund) -->
  <g fill="none" stroke-linecap="round">
    <!-- Schläger links -->
    <g transform="rotate(-25 200 200)">
      <path d="M200 40 L200 270 Q200 305 162 312" stroke="#E87722" stroke-width="12"/>
      <path d="M200 40 L200 270 Q200 305 162 312" stroke="#C05C12" stroke-width="4"/>
      <circle cx="200" cy="42" r="6" fill="#1B3A5C" stroke="none"/>
    </g>
    <!-- Schläger rechts -->
    <g transform="rotate(25 200 200)">
      <path d="M200 40 L200 270 Q200 305 238 312" stroke="#E87722" stroke-width="12"/>
      <path d="M200 40 L200 270 Q200 305 238 312" stroke="#C05C12" stroke-width="4"/>
      <circle cx="200" cy="42" r="6" fill="#1B3A5C" stroke="none"/>
    </g>
  </g>

  <!-- Eule -->
  <g>
    <!-- Körper -->
    <ellipse cx="200" cy="195" rx="68" ry="78" fill="#1B3A5C"/>
    <!-- Federohren -->
    <path d="M145 135 L130 95 L170 118 Z" fill="#1B3A5C"/>
    <path d="M255 135 L270 95 L230 118 Z" fill="#1B3A5C"/>
    <!-- Flügeln -->
    <path d="M133 180 Q110 220 138 255 Q158 235 150 195 Z" fill="#0F2438"/>
    <path d="M267 180 Q290 220 262 255 Q242 235 250 195 Z" fill="#0F2438"/>
    <!-- Brust -->
    <ellipse cx="200" cy="212" rx="42" ry="50" fill="#FFFFFF"/>
    <path d="M175 220 l10 8 l10 -8 l10 8 l10 -8" fill="none" stroke="#1B3A5C" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>
    <path d="M175 240 l10 8 l10 -8 l10 8 l10 -8" fill="none" stroke="#1B3A5C" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>
    <!-- Augenränder -->
    <circle cx="172" cy="165" r="26" fill="#E87722"/>
    <circle cx="228" cy="165" r="26" fill="#E87722"/>
    <!-- Augen -->
    <circle cx="172" cy="165" r="20" fill="#FFFFFF"/>
    <circle cx="228" cy="165" r="20" fill="#FFFFFF"/>
    <!-- Pupillen -->
    <circle cx="175" cy="167" r="10" fill="#0F2438"/>
    <circle cx="225" cy="167" r="10" fill="#0F2438"/>
    <circle cx="178" cy="163" r="3.5" fill="#FFFFFF"/>
    <circle cx="228" cy="163" r="3.5" fill="#FFFFFF"/>
    <!-- Schnabel -->
    <path d="M200 190 L186 176 L214 176 Z" fill="#E87722"/>
    <!-- Füße -->
    <path d="M170 272 q-8 14 6 14 q10 0 6 -10" fill="#E87722"/>
    <path d="M230 272 q8 14 -6 14 q-10 0 -6 -10" fill="#E87722"/>
  </g>

  <!-- Teamname -->
  <text x="200" y="380" text-anchor="middle"
        font-family="Arial, Helvetica, sans-serif" font-weight="bold"
        font-size="40" fill="#1B3A5C" letter-spacing="2">OWAYO EULERS</text>
  <!-- Unterschrift-Linie -->
  <path d="M70 395 L330 395" stroke="#E87722" stroke-width="5" stroke-linecap="round"/>
</svg>
```
