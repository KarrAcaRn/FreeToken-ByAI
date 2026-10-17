# gemma4-e4b - logo-owayo-eulers (2026-10-17T18:43:32)

## Antwort (1048 Tokens, 8.22 s, Ende: stop)

### Denkphase



### Antwort

```svg
<svg width="600" height="300" viewBox="0 0 600 300" xmlns="http://www.w3.org/2000/svg">
  <!-- Hintergrund: Transparent (kein Hintergrund definiert) -->

  <!-- Definition von Farben -->
  <defs>
    <linearGradient id="teamGradient" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:rgb(255,255,255);stop-opacity:1" />
      <stop offset="100%" style="stop-color:rgb(0,0,0);stop-opacity:1" />
    </linearGradient>
  </defs>

  <!-- Hauptelement: Eule (Stilisiert) -->
  <g id="owl">
    <!-- Körper der Eule (vereinfacht) -->
    <path d="M 150 100 Q 100 50, 150 30 C 200 50, 280 80, 250 120 Z" fill="#333333" stroke="#000000" stroke-width="3"/>
    <!-- Kopf/Gesicht (vereinfacht) -->
    <circle cx="180" cy="70" r="30" fill="#555555" stroke="#000000" stroke-width="3"/>
    <!-- Augen -->
    <circle cx="165" cy="65" r="5" fill="white" stroke="black" stroke-width="1"/>
    <circle cx="195" cy="65" r="5" fill="white" stroke="black" stroke-width="1"/>
    <!-- Schnabel -->
    <path d="M 180 80 L 190 95 L 180 90 Z" fill="#FFD700"/>
  </g>

  <!-- Hauptelement: Eishockeyschläger (Kreuzend hinter/vor der Eule) -->
  <g id="hockeyStick">
    <!-- Schlägerblatt (links) -->
    <path d="M 100 180 L 50 200 L 150 220 L 200 160 L 150 180 Z" fill="#AAAAAA" stroke="#000000" stroke-width="3"/>
    <!-- Schlägerkelle/Griff (rechts) -->
    <rect x="250" y="100" width="40" height="120" rx="10" fill="#AAAAAA" stroke="#000000" stroke-width="3"/>
  </g>

  <!-- Logo-Komposition: Eule und Schläger überlappend -->
  <g transform="translate(150, 150)">
    <!-- Schläger leicht in die Szene integriert -->
    <g transform="translate(-10, 0)">
        <path d="M 0 150 L -100 170 L -120 190 L -50 180 L 0 150 Z" fill="#666666" stroke="#000000" stroke-width="4"/>
        <rect x="-50" y="-10" width="100" height="150" rx="15" fill="#666666" stroke="#000000" stroke-width="4"/>
    </g>

    <!-- Eule in die Mitte platziert -->
    <use href="#owl" transform="translate(30, 0) scale(0.8)"/>
  </g>


  <!-- Text: Owayo Eulers -->
  <text x="300" y="60" font-family="Impact, Arial Black, sans-serif" font-size="60" text-anchor="middle" fill="#000000">
    Owayo Eulers
  </text>

  <!-- Optional: Ein kleiner Strich als "Hockey"-Akzent unter dem Text -->
  <line x1="220" y1="100" x2="380" y2="100" stroke="#000000" stroke-width="4"/>

</svg>
```
