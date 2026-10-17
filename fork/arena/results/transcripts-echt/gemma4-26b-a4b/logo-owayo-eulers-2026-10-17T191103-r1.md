# gemma4-26b-a4b - logo-owayo-eulers (2026-10-17T19:11:03)

## Antwort (1148 Tokens, 7.094 s, Ende: stop)

### Denkphase



### Antwort

Hier ist das Logo für die "Owayo Eulers". Es wurde in einem modernen, sportlichen Stil als Vektor-Grafik erstellt. Die Eule ist aggressiv und fokussiert gestaltet, die Schläger kreuzen sich hinter dem Kopf der Eule, um ein klassisches Team-Emblem zu bilden.

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 500 500">
  <!-- Definitionen für Schatten und Effekte -->
  <defs>
    <linearGradient id="eyeGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#ffcc00;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#ff8800;stop-opacity:1" />
    </linearGradient>
  </defs>

  <!-- Eishockeyschläger (Hintergrund der Eule) -->
  <g id="sticks" stroke="#ffffff" stroke-width="12" stroke-linecap="round">
    <!-- Schläger 1 -->
    <line x1="150" y1="150" x2="350" y2="400" />
    <path d="M350 400 L380 430 L340 440 L330 410 Z" fill="#ffffff" />
    <!-- Schläger 2 -->
    <line x1="350" y1="150" x2="150" y2="400" />
    <path d="M150 400 L120 430 L160 440 L170 410 Z" fill="#ffffff" />
  </g>

  <!-- Eulen-Körper / Kopf Silhouette -->
  <path d="M250 80 C180 80 140 150 140 250 C140 350 180 420 250 420 C320 420 360 350 360 250 C360 150 320 80 250 80Z" fill="#1a1a1a" />
  
  <!-- Augen (Aggressiver Eulen-Look) -->
  <g id="eyes">
    <!-- Links -->
    <path d="M170 200 Q210 160 240 220 L200 250 Z" fill="url(#eyeGrad)" />
    <circle cx="200" cy="210" r="12" fill="black" />
    <!-- Rechts -->
    <path d="M330 200 Q290 160 260 220 L300 250 Z" fill="url(#eyeGrad)" />
    <circle cx="300" cy="210" r="12" fill="black" />
  </g>

  <!-- Schnabel -->
  <path d="M250 240 L235 280 L250 300 L265 280 Z" fill="#ffcc00" />

  <!-- Feder-Details / Brust -->
  <path d="M250 320 Q220 350 200 330 Q220 380 250 400 Q280 380 300 330 Q280 350 250 320" fill="#333333" />

  <!-- Text-Banner / Teamname -->
  <path id="textPath" d="M50 400 Q250 480 450 400" fill="none" />
  <text font-family="Arial, sans-serif" font-weight="bold" font-size="42" fill="#ffffff" text-anchor="middle">
    <textPath href="#textPath" startOffset="50%">OWAYO EULERS</textPath>
  </text>

  <!-- Akzent-Linien für Dynamik -->
  <path d="M140 250 Q100 250 80 200" stroke="#ffffff" stroke-width="4" fill="none" opacity="0.6" />
  <path d="M360 250 Q400 250 420 200" stroke="#ffffff" stroke-width="4" fill="none" opacity="0.6" />
</svg>
```
