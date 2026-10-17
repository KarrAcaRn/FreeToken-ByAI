# gemma4-12b-qat - logo-owayo-eulers (2026-10-17T19:01:05)

## Antwort (1214 Tokens, 11.477 s, Ende: stop)

### Denkphase



### Antwort

```svg
<svg width="500" height="500" viewBox="0 0 500 500" xmlns="http://www.w3.org/2000/svg">
  <!-- Definitionen für Farben und Stile -->
  <defs>
    <linearGradient id="owlGrad" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" style="stop-color:#ffffff;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#cccccc;stop-opacity:1" />
    </linearGradient>
    <filter id="shadow" x="-20%" y="-20%" width="140%" height="140%">
      <feOffset result="offOut" in="SourceAlpha" dx="3" dy="3" />
      <feGaussianBlur result="blurOut" in="offOut" stdDeviation="2" />
      <feBlend in="SourceAlpha" in2="blurOut" mode="normal" />
      <feMerge>
        <feMergeNode />
        <feMergeNode in="SourceGraphic" />
      </feBlend>
    </filter>
  </defs>

  <!-- Eishockeyschläger im Hintergrund (gekreuzt) -->
  <g fill="#333333" stroke="#000000" stroke-width="2">
    <!-- Schläger 1 (von links unten nach rechts oben) -->
    <path d="M100,400 L350,100 L380,120 L130,430 Z" /> <!-- Schlägerblatt -->
    <rect x="100" y="390" width="250" height="20" transform="rotate(-30 125 410)" /> <!-- Schlägerstiel -->
    
    <!-- Schläger 2 (von rechts unten nach links oben) -->
    <path d="M400,400 L150,100 L180,120 L430,430 Z" /> <!-- Schlägerblatt -->
    <rect x="400" y="390" width="250" height="20" transform="rotate(30 375 410)" /> <!-- Schlägerstiel -->
  </g>

  <!-- Die Eule (Zentrales Element) -->
  <g filter="url(#shadow)">
    <!-- Kopf der Eule -->
    <path d="M180,250 Q180,100 250,100 Q320,100 320,250 Q320,350 250,380 Q180,350 180,250 Z" fill="#555555" />
    
    <!-- Augen (Groß und markant) -->
    <circle cx="215" cy="200" r="35" fill="white" />
    <circle cx="215" cy="200" r="25" fill="black" />
    <circle cx="222" cy="192" r="8" fill="white" /> <!-- Lichtreflexion -->
    
    <circle cx="285" cy="200" r="35" fill="white" />
    <circle cx="285" cy="200" r="25" fill="black" />
    <circle cx="278" cy="192" r="8" fill="white" /> <!-- Lichtreflexion -->

    <!-- Schnabel -->
    <path d="M240,250 L260,250 L250,280 Z" fill="#FFD700" />

    <!-- Ohren/Federn oben -->
    <path d="M180,150 Q160,100 210,130 Z" fill="#444444" />
    <path d="M320,150 Q340,100 290,130 Z" fill="#444444" />

    <!-- Flügel (leicht gespreizt neben der Eule) -->
    <path d="M150,200 Q100,250 130,350 L180,300 Z" fill="#333333" />
    <path d="M350,200 Q400,250 370,350 L320,300 Z" fill="#333333" />
  </g>

  <!-- Text "Owayo Eulers" -->
  <g font-family="Arial, sans-serif" font-weight="bold" font-size="42" fill="white" stroke="black" stroke-width="1.5">
    <text x="100" y="450">Owayo Eulers</text>
  </g>
</svg>
```
