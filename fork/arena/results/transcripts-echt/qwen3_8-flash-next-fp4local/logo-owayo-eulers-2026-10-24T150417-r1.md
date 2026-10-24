# qwen3_8-flash-next-fp4local - logo-owayo-eulers (2026-10-24T15:04:17)

## Antwort (2733 Tokens, 78.166 s, Ende: stop)

### Denkphase

The user is asking for a logo SVG of an owl holding crossed hockey sticks, with the team name "Owayo Eulers" (a pun on "Owl-Ers"). A transparent background is preferred. I'll create a single SVG containing a vector-drawn owl and crossed hockey sticks, and add text as well. Let me design a nice owl: body, head, big eyes, ear tufts, wings, feet, and crossed hockey sticks behind the owl. Colors: brown/orange owl, maybe teal accents too.

Let me write a clean SVG, roughly 500x600. Crossed hockey sticks behind the owl, with the owl in the center and the text "OWAYO EULERS" at the bottom.

Drawing the crossed hockey sticks: two diagonal sticks from bottom-left to top-right, and vice versa. Each stick: shaft (thick line, rounded) + blade at the bottom. Placing them in an X shape behind the owl, with the blades at the top? Usually crossed sticks have the blades at the top. Sticks cross behind the owl, blades at the top.

Stick 1: shaft goes from (150,460) to (350,120), with the blade at the top… actually the blade is at the end of the stick. Crossed sticks displayed in a shield-shaped logo: shafts run diagonally, blades at the top going outward.

Simply put: stick A's shaft is a line from (140,470) to (330,110), stroke width 16, wood color, with the blade at the top: a path curving right from (330,110). Stick B is mirrored: shaft (460,470) to (270,110)? Hmm, they should cross behind the owl's center (around (300,300)).

Let me place the owl's center at (300,300). Sticks: A from (160,480) to (320,110) — top blade extends to the right: a curve from (320,110) to (390,130). B is mirrored: (440,480) to (280,110), blade extending left from (280,110) to (210,130). Use stroke-linecap round.

Owl: body is an ellipse, head is a circle with ear tufts, eyes are big white circles with black pupils and white highlights, beak is an orange triangle, wings, belly feather pattern, feet, maybe holding a small puck too.

Colors: owl body #8B5E3C brown, belly #D9A96B, eyes white, pupils dark, beak and feet orange #E8862E, maybe teal #1B7F79 for accents.

Text: "OWAYO EULERS" at the bottom, font-family is sans-serif, bold, maybe two lines. Text as <text> is fine.

No background — transparent.

Let me write the SVG.


### Antwort



```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 680" width="600" height="680">
  <!-- Gekreuzte Eishockeyschläger (hinten) -->
  <g stroke-linecap="round" fill="none">
    <!-- Schläger 1: unten links nach oben rechts -->
    <line x1="165" y1="490" x2="330" y2="130" stroke="#7a4a21" stroke-width="18"/>
    <path d="M330 130 q55 -8 85 22" stroke="#7a4a21" stroke-width="18"/>
    <path d="M330 130 q55 -8 85 22" stroke="#c98a4b" stroke-width="8"/>
    <line x1="165" y1="490" x2="205" y2="402" stroke="#1b7f79" stroke-width="20"/>
    <!-- Schläger 2: unten rechts nach oben links -->
    <line x1="435" y1="490" x2="270" y2="130" stroke="#8a5626" stroke-width="18"/>
    <path d="M270 130 q-55 -8 -85 22" stroke="#8a5626" stroke-width="18"/>
    <path d="M270 130 q-55 -8 -85 22" stroke="#d99a5b" stroke-width="8"/>
    <line x1="435" y1="490" x2="395" y2="402" stroke="#1b7f79" stroke-width="20"/>
  </g>

  <!-- Eule -->
  <g>
    <!-- Ohren (Federbüschel) -->
    <path d="M212 168 L196 108 L246 148 Z" fill="#6d4322"/>
    <path d="M388 168 L404 108 L354 148 Z" fill="#6d4322"/>

    <!-- Körper -->
    <ellipse cx="300" cy="330" rx="145" ry="165" fill="#8b5e3c" stroke="#5c3a1c" stroke-width="6"/>

    <!-- Bauch -->
    <ellipse cx="300" cy="370" rx="95" ry="115" fill="#e3b878"/>
    <!-- Bauchfedern -->
    <g fill="none" stroke="#b98a4e" stroke-width="4" stroke-linecap="round">
      <path d="M265 320 q12 14 24 0 q12 14 24 0 q12 14 24 0"/>
      <path d="M255 355 q12 14 24 0 q12 14 24 0 q12 14 24 0 q12 14 24 0"/>
      <path d="M262 390 q12 14 24 0 q12 14 24 0 q12 14 24 0"/>
      <path d="M272 425 q12 14 24 0 q12 14 24 0"/>
    </g>

    <!-- Flügel -->
    <path d="M163 275 q-22 90 18 165 q30 30 48 8 q-30 -90 -18 -160 Z" fill="#6d4322" stroke="#5c3a1c" stroke-width="5"/>
    <path d="M437 275 q22 90 -18 165 q-30 30 -48 8 q30 -90 18 -160 Z" fill="#6d4322" stroke="#5c3a1c" stroke-width="5"/>

    <!-- Kopf -->
    <circle cx="300" cy="215" r="105" fill="#8b5e3c" stroke="#5c3a1c" stroke-width="6"/>

    <!-- Gesichtsscheibe -->
    <path d="M300 155 q-70 0 -80 60 q-6 55 45 75 q30 12 35 12 q5 0 35 -12 q51 -20 45 -75 q-10 -60 -80 -60 Z" fill="#e3b878"/>

    <!-- Augen -->
    <circle cx="258" cy="212" r="38" fill="#ffffff" stroke="#5c3a1c" stroke-width="5"/>
    <circle cx="342" cy="212" r="38" fill="#ffffff" stroke="#5c3a1c" stroke-width="5"/>
    <circle cx="262" cy="216" r="18" fill="#1d2b33"/>
    <circle cx="338" cy="216" r="18" fill="#1d2b33"/>
    <circle cx="268" cy="209" r="6" fill="#ffffff"/>
    <circle cx="344" cy="209" r="6" fill="#ffffff"/>

    <!-- Augenbrauen (entschlossener Blick) -->
    <path d="M222 186 L296 198" stroke="#5c3a1c" stroke-width="9" stroke-linecap="round"/>
    <path d="M378 186 L304 198" stroke="#5c3a1c" stroke-width="9" stroke-linecap="round"/>

    <!-- Schnabel -->
    <path d="M300 235 L316 258 L300 282 L284 258 Z" fill="#e8862e" stroke="#b35f14" stroke-width="4"/>

    <!-- Füße -->
    <g fill="#e8862e" stroke="#b35f14" stroke-width="4">
      <path d="M258 488 q-6 22 -16 26 m16 -26 q0 24 -2 30 m2 -30 q8 22 16 26"/>
      <path d="M342 488 q-6 22 -16 26 m16 -26 q0 24 -2 30 m2 -30 q8 22 16 26"/>
    </g>

    <!-- Puck zwischen den Flügeln -->
    <ellipse cx="300" cy="470" rx="42" ry="14" fill="#23272b" stroke="#0d0f11" stroke-width="3"/>
    <rect x="258" y="458" width="84" height="12" fill="#23272b"/>
    <ellipse cx="300" cy="458" rx="42" ry="14" fill="#3a4046" stroke="#0d0f11" stroke-width="3"/>
  </g>

  <!-- Teamname -->
  <text x="300" y="575" text-anchor="middle" font-family="Arial Black, Arial, sans-serif" font-weight="900" font-size="62" fill="#1b7f79" stroke="#0f4a46" stroke-width="2">OWAYO</text>
  <text x="300" y="645" text-anchor="middle" font-family="Arial Black, Arial, sans-serif" font-weight="900" font-size="62" fill="#e8862e" stroke="#9c5310" stroke-width="2">EULERS</text>
</svg>
```
