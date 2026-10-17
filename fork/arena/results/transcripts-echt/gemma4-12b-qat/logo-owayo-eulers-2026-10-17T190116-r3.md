# gemma4-12b-qat - logo-owayo-eulers (2026-10-17T19:01:16)

## Antwort (1376 Tokens, 13.008 s, Ende: stop)

### Denkphase



### Antwort

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 500 500">
  <!-- Hintergrund ist transparent -->
  
  <!-- Definitionen für Schatten und Verläufe -->
  <defs>
    <linearGradient id="goldGrad" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" style="stop-color:#FFD700" />
      <stop offset="100%" style="stop-color:#B8860B" />
    </linearGradient>
    <filter id="shadow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="3" />
      <feOffset dx="2" dy="2" result="offsetblur"/>
      <feComponentTransfer>
        <feFuncA type="linear" tableValues="0 0 1 1" />
        <feColorMatrix type="matrix" values="1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0.3 0" />
      </feComponentTransfer>
      <feComposite operator=" Ferguson" in="SourceGraphic" in2="offsetblur" />
    </filter>
  </defs>

  <!-- Eishockeyschläger im Hintergrund (gekreuzt) -->
  <g fill="#2C3E50" stroke="#FFFFFF" stroke-width="2">
    <!-- Schläger links oben nach rechts unten -->
    <rect x="120" y="100" width="30" height="300" transform="rotate(25, 150, 150)" />
    <path d="M 100 350 Q 150 400 220 360 L 230 380 Q 160 430 110 380 Z" transform="rotate(25, 150, 150)" />
    
    <!-- Schläger rechts oben nach links unten -->
    <rect x="350" y="100" width="30" height="300" transform="rotate(-25, 350, 150)" />
    <path d="M 380 350 Q 330 400 280 360 L 270 380 Q 340 430 390 380 Z" transform="rotate(-25, 350, 150)" />
  </g>

  <!-- Die Eule (Zentrales Element) -->
  <g transform="translate(140, 80)">
    <!-- Kopf & Körper Umriss -->
    <path d="M 50 250 C 20 250 10 150 50 80 C 90 10 150 10 200 80 C 280 150 280 250 250 250 L 50 250 Z" fill="#1A1A1A" stroke="#FFFFFF" stroke-width="4"/>
    
    <!-- Augen (Aggressiv) -->
    <path d="M 70 130 Q 100 80 130 130 Z" fill="#FFD700" />
    <path d="M 170 130 Q 200 80 230 130 Z" fill="#FFD700" />
    <circle cx="100" cy="115" r="10" fill="black" />
    <circle cx="200" cy="115" r="10" fill="black" />
    
    <!-- Schnabel -->
    <path d="M 140 140 L 160 140 L 150 170 Z" fill="#FFD700" />
    
    <!-- Federn/Flügel-Andeutung -->
    <path d="M 40 180 Q 10 100 80 140" fill="none" stroke="#FFFFFF" stroke-width="2" />
    <path d="M 260 180 Q 290 100 220 140" fill="none" stroke="#FFFFFF" stroke-width="2" />
    
    <!-- Federn unten -->
    <path d="M 100 240 L 80 280 L 120 280 Z" fill="#333" />
    <path d="M 150 240 L 140 290 L 160 290 Z" fill="#333" />
    <path d="M 200 240 L 190 290 L 210 290 Z" fill="#333" />
  </g>

  <!-- Banner mit Teamname -->
  <path d="M 50 400 Q 250 450 450 400 L 440 430 Q 250 480 60 430 Z" fill="#B8860B" />
  <text x="250" y="425" font-family="Arial, sans-serif" font-weight="bold" font-size="35" fill="white" text-anchor="middle">OWAYO EULERS</text>
</svg>
```
