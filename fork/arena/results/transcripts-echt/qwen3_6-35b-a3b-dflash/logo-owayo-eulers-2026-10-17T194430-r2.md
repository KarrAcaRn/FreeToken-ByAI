# qwen3_6-35b-a3b-dflash - logo-owayo-eulers (2026-10-17T19:44:30)

## Antwort (4833 Tokens, 22.099 s, Ende: stop)

### Denkphase

Der Benutzer möchte ein SVG-Logo für eine Eishockeymannschaft namens "Owayo Eulers". Das Logo soll:
- Eine Eule enthalten
- Eishockeyschläger enthalten
- Den Namen "Owayo Eulers" zeigen
- Einen einfarbigen Hintergrund oder keinen Hintergrund haben

Ich werde ein vollständiges SVG-Dokument erstellen, das eine stilisierte Eule mit Eishockeyschlägern zeigt. Ich muss das SVG von Hand zeichnen, ohne externe Ressourcen.

Ich werde ein ansprechendes Logo mit:
- Eine stilisierte Eule im Zentrum
- Eishockeyschläger gekreuzt hinter der Eule
- Den Text "Owayo Eulers" darunter
- Einfarbiger Hintergrund (dunkelblau oder ähnlich)
- Sportliches, dynamisches Design

Lass mich das SVG sorgfältig aufbauen mit Pfaden und Formen.


### Antwort



```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 500 500" width="500" height="500">
  <defs>
    <linearGradient id="bgGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#0a1628"/>
      <stop offset="100%" style="stop-color:#1a2d50"/>
    </linearGradient>
    <linearGradient id="bladeGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#c0c8d4"/>
      <stop offset="100%" style="stop-color:#7a8595"/>
    </linearGradient>
    <linearGradient id="stickGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#2a4a7f"/>
      <stop offset="100%" style="stop-color:#1a2d50"/>
    </linearGradient>
    <linearGradient id="bodyGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#f0e6d3"/>
      <stop offset="100%" style="stop-color:#c9b896"/>
    </linearGradient>
    <linearGradient id="wingGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#3a5a8c"/>
      <stop offset="100%" style="stop-color:#1e3a5f"/>
    </linearGradient>
    <linearGradient id="eyeGrad" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" style="stop-color:#ffdd44"/>
      <stop offset="100%" style="stop-color:#cc9900"/>
    </linearGradient>
    <filter id="shadow" x="-10%" y="-10%" width="130%" height="130%">
      <feDropShadow dx="2" dy="3" stdDeviation="4" flood-color="#000" flood-opacity="0.5"/>
    </filter>
    <filter id="glow">
      <feGaussianBlur stdDeviation="3" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <!-- Background Circle -->
  <circle cx="250" cy="240" r="220" fill="url(#bgGrad)" filter="url(#shadow)"/>
  <circle cx="250" cy="240" r="218" fill="none" stroke="#2a4a7f" stroke-width="3"/>
  <circle cx="250" cy="240" r="210" fill="none" stroke="#3a6aad" stroke-width="1" opacity="0.4"/>

  <!-- Crossed Hockey Sticks -->
  <!-- Stick 1 (left to right diagonal) -->
  <g transform="rotate(-35, 250, 240)" filter="url(#shadow)">
    <!-- Stick shaft -->
    <rect x="240" y="60" width="12" height="320" rx="4" fill="url(#stickGrad)" stroke="#1a2d50" stroke-width="1"/>
    <!-- Stick blade -->
    <path d="M 220 360 Q 220 395 250 400 Q 280 395 280 360" fill="url(#bladeGrad)" stroke="#5a6575" stroke-width="1"/>
    <path d="M 230 365 L 230 385 Q 230 395 250 398 Q 270 395 270 385 L 270 365" fill="none" stroke="#8a95a5" stroke-width="0.5"/>
    <!-- Tape on stick -->
    <rect x="239" y="120" width="14" height="30" rx="2" fill="#333" opacity="0.7"/>
    <rect x="239" y="155" width="14" height="30" rx="2" fill="#333" opacity="0.7"/>
  </g>

  <!-- Stick 2 (right to left diagonal) -->
  <g transform="rotate(35, 250, 240)" filter="url(#shadow)">
    <!-- Stick shaft -->
    <rect x="240" y="60" width="12" height="320" rx="4" fill="url(#stickGrad)" stroke="#1a2d50" stroke-width="1"/>
    <!-- Stick blade -->
    <path d="M 220 360 Q 220 395 250 400 Q 280 395 280 360" fill="url(#bladeGrad)" stroke="#5a6575" stroke-width="1"/>
    <path d="M 230 365 L 230 385 Q 230 395 250 398 Q 270 395 270 385 L 270 365" fill="none" stroke="#8a95a5" stroke-width="0.5"/>
    <!-- Tape on stick -->
    <rect x="239" y="120" width="14" height="30" rx="2" fill="#333" opacity="0.7"/>
    <rect x="239" y="155" width="14" height="30" rx="2" fill="#333" opacity="0.7"/>
  </g>

  <!-- Eule Body -->
  <g filter="url(#shadow)">
    <!-- Main body -->
    <ellipse cx="250" cy="230" rx="65" ry="80" fill="url(#bodyGrad)" stroke="#8a7a5a" stroke-width="1.5"/>

    <!-- Belly -->
    <ellipse cx="250" cy="250" rx="45" ry="55" fill="#f5eedd" stroke="#b0a080" stroke-width="0.5"/>

    <!-- Belly stripes -->
    <path d="M 220 230 Q 235 235 250 230 Q 265 235 280 230" fill="none" stroke="#c9b896" stroke-width="2" stroke-linecap="round"/>
    <path d="M 215 245 Q 235 250 250 245 Q 265 250 285 245" fill="none" stroke="#c9b896" stroke-width="2" stroke-linecap="round"/>
    <path d="M 210 260 Q 235 265 250 260 Q 265 265 290 260" fill="none" stroke="#c9b896" stroke-width="2" stroke-linecap="round"/>
    <path d="M 215 275 Q 235 280 250 275 Q 265 280 285 275" fill="none" stroke="#c9b896" stroke-width="2" stroke-linecap="round"/>

    <!-- Left Wing -->
    <path d="M 190 180 Q 150 200 140 250 Q 135 280 150 310 Q 165 330 185 320 Q 195 310 200 280 L 205 250 Q 200 220 190 200 Z" fill="url(#wingGrad)" stroke="#1a2d50" stroke-width="1"/>
    <!-- Wing feather lines -->
    <path d="M 185 200 Q 160 220 155 260" fill="none" stroke="#2a4a7f" stroke-width="1" opacity="0.6"/>
    <path d="M 188 210 Q 165 230 160 270" fill="none" stroke="#2a4a7f" stroke-width="1" opacity="0.6"/>
    <path d="M 190 220 Q 170 240 165 280" fill="none" stroke="#2a4a7f" stroke-width="1" opacity="0.6"/>

    <!-- Right Wing -->
    <path d="M 310 180 Q 350 200 360 250 Q 365 280 350 310 Q 335 330 315 320 Q 305 310 300 280 L 295 250 Q 300 220 310 200 Z" fill="url(#wingGrad)" stroke="#1a2d50" stroke-width="1"/>
    <!-- Wing feather lines -->
    <path d="M 315 200 Q 340 220 345 260" fill="none" stroke="#2a4a7f" stroke-width="1" opacity="0.6"/>
    <path d="M 312 210 Q 335 230 340 270" fill="none" stroke="#2a4a7f" stroke-width="1" opacity="0.6"/>
    <path d="M 310 220 Q 330 240 335 280" fill="none" stroke="#2a4a7f" stroke-width="1" opacity="0.6"/>

    <!-- Left Ear Tuft -->
    <path d="M 200 165 L 185 110 L 215 150 Z" fill="#2a4a7f" stroke="#1a2d50" stroke-width="1"/>
    <path d="M 205 160 L 192 120 L 212 150 Z" fill="#3a6aad" opacity="0.5"/>

    <!-- Right Ear Tuft -->
    <path d="M 300 165 L 315 110 L 285 150 Z" fill="#2a4a7f" stroke="#1a2d50" stroke-width="1"/>
    <path d="M 295 160 L 308 120 L 288 150 Z" fill="#3a6aad" opacity="0.5"/>

    <!-- Head -->
    <ellipse cx="250" cy="170" rx="55" ry="45" fill="url(#bodyGrad)" stroke="#8a7a5a" stroke-width="1.5"/>

    <!-- Face disc -->
    <ellipse cx="250" cy="175" rx="48" ry="38" fill="#f5eedd" stroke="#c9b896" stroke-width="1"/>

    <!-- Eyes -->
    <!-- Left eye -->
    <circle cx="225" cy="168" r="18" fill="url(#eyeGrad)" stroke="#aa7700" stroke-width="1"/>
    <circle cx="225" cy="168" r="14" fill="#ffcc00"/>
    <circle cx="228" cy="168" r="9" fill="#1a1a1a"/>
    <circle cx="223" cy="163" r="3" fill="white" opacity="0.8"/>
    <circle cx="231" cy="171" r="1.5" fill="white" opacity="0.5"/>

    <!-- Right eye -->
    <circle cx="275" cy="168" r="18" fill="url(#eyeGrad)" stroke="#aa7700" stroke-width="1"/>
    <circle cx="275" cy="168" r="14" fill="#ffcc00"/>
    <circle cx="278" cy="168" r="9" fill="#1a1a1a"/>
    <circle cx="273" cy="163" r="3" fill="white" opacity="0.8"/>
    <circle cx="281" cy="171" r="1.5" fill="white" opacity="0.5"/>

    <!-- Beak -->
    <path d="M 245 180 L 250 175 L 255 180 L 253 195 L 247 195 Z" fill="#e88500" stroke="#c06a00" stroke-width="0.5"/>
    <path d="M 247 182 L 250 178 L 253 182 L 252 192 L 248 192 Z" fill="#f5a000"/>

    <!-- Feet -->
    <path d="M 230 305 L 220 330 L 225 330 L 232 310 Z" fill="#e88500" stroke="#c06a00" stroke-width="0.5"/>
    <path d="M 235 308 L 228 332 L 233 332 L 238 312 Z" fill="#e88500" stroke="#c06a00" stroke-width="0.5"/>
    <path d="M 240 310 L 236 334 L 241 334 L 244 314 Z" fill="#e88500" stroke="#c06a00" stroke-width="0.5"/>

    <path d="M 270 305 L 280 330 L 275 330 L 268 310 Z" fill="#e88500" stroke="#c06a00" stroke-width="0.5"/>
    <path d="M 265 308 L 272 332 L 267 332 L 262 312 Z" fill="#e88500" stroke="#c06a00" stroke-width="0.5"/>
    <path d="M 260 310 L 264 334 L 259 334 L 256 314 Z" fill="#e88500" stroke="#c06a00" stroke-width="0.5"/>
  </g>

  <!-- Hockey Puck near feet -->
  <ellipse cx="250" cy="335" rx="12" ry="5" fill="#1a1a1a" stroke="#333" stroke-width="0.5"/>
  <ellipse cx="250" cy="334" rx="10" ry="3.5" fill="#2a2a2a"/>

  <!-- Team Name Text -->
  <text x="250" y="410" text-anchor="middle" font-family="Arial, Helvetica, sans-serif" font-size="36" font-weight="bold" fill="#ffffff" filter="url(#glow)" letter-spacing="2">OWAYO</text>
  <text x="250" y="445" text-anchor="middle" font-family="Arial, Helvetica, sans-serif" font-size="30" font-weight="bold" fill="#4a9ae0" letter-spacing="4">EURLERS</text>

  <!-- Decorative elements -->
  <line x1="160" y1="395" x2="200" y2="395" stroke="#4a9ae0" stroke-width="2"/>
  <line x1="300" y1="395" x2="340" y2="395" stroke="#4a9ae0" stroke-width="2"/>

  <!-- Small stars/dots -->
  <circle cx="175" cy="400" r="2" fill="#4a9ae0"/>
  <circle cx="325" cy="400" r="2" fill="#4a9ae0"/>

  <!-- Snowflake accents -->
  <g transform="translate(130, 150)" opacity="0.3">
    <line x1="0" y1="-6" x2="0" y2="6" stroke="#ffffff" stroke-width="1.5"/>
    <line x1="-5" y1="-3" x2="5" y2="3" stroke="#ffffff" stroke-width="1.5"/>
    <line x1="-5" y1="3" x2="5" y2="-3" stroke="#ffffff" stroke-width="1.5"/>
  </g>
  <g transform="translate(370, 130)" opacity="0.3">
    <line x1="0" y1="-5" x2="0" y2="5" stroke="#ffffff" stroke-width="1.5"/>
    <line x1="-4" y1="-2.5" x2="4" y2="2.5" stroke="#ffffff" stroke-width="1.5"/>
    <line x1="-4" y1="2.5" x2="4" y2="-2.5" stroke="#ffffff" stroke-width="1.5"/>
  </g>
  <g transform="translate(340, 180)" opacity="0.25">
    <line x1="0" y1="-4" x2="0" y2="4" stroke="#ffffff" stroke-width="1"/>
    <line x1="-3" y1="-2" x2="3" y2="2" stroke="#ffffff" stroke-width="1"/>
    <line x1="-3" y1="2" x2="3" y2="-2" stroke="#ffffff" stroke-width="1"/>
  </g>
</svg>
```
