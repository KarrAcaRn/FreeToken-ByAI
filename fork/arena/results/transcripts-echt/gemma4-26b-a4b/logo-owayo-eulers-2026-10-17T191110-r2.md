# gemma4-26b-a4b - logo-owayo-eulers (2026-10-17T19:11:10)

## Antwort (1255 Tokens, 7.749 s, Ende: stop)

### Denkphase



### Antwort

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 500 500">
  <!-- Definitions for gradients and shadows to give depth -->
  <defs>
    <linearGradient id="eyeGradient" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#FFD700;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#FFA500;stop-opacity:1" />
    </linearGradient>
  </defs>

  <!-- Background is transparent as requested -->

  <!-- MAIN OWL HEAD -->
  <g id="owl">
    <!-- Ears/Tufts -->
    <path d="M150,150 L100,80 L180,140 Z" fill="#2C3E50" />
    <path d="M350,150 L400,80 L320,140 Z" fill="#2C3E50" />
    
    <!-- Face Shape -->
    <path d="M120,200 Q120,100 250,100 Q380,100 380,200 Q380,350 250,380 Q120,350 120,200" fill="#34495E" />
    
    <!-- Eye Patches (White) -->
    <circle cx="190" cy="200" r="50" fill="#ECF0F1" />
    <circle cx="310" cy="200" r="50" fill="#ECF0F1" />
    
    <!-- Eyes (Glowing Yellow) -->
    <circle cx="190" cy="200" r="30" fill="url(#eyeGradient)" />
    <circle cx="310" cy="200" r="30" fill="url(#eyeGradient)" />
    
    <!-- Pupils -->
    <circle cx="190" cy="200" r="12" fill="#000000" />
    <circle cx="310" cy="200" r="12" fill="#000000" />
    
    <!-- Beak -->
    <path d="M250,230 L230,270 L270,270 Z" fill="#F1C40F" />
    
    <!-- Feather details/markings -->
    <path d="M220,320 Q250,350 280,320" stroke="#2C3E50" stroke-width="5" fill="none" opacity="0.5" />
  </g>

  <!-- HOCKEY STICKS (Crossed behind/below the owl) -->
  <g id="sticks" transform="translate(0, 40)">
    <!-- Stick 1 (Left to Right) -->
    <g transform="rotate(-45, 250, 250)">
      <rect x="240" y="50" width="20" height="400" fill="#BDC3C7" rx="5" />
      <path d="M220,450 Q250,480 280,450 L280,420 L220,420 Z" fill="#BDC3C7" />
    </g>
    <!-- Stick 2 (Right to Left) -->
    <g transform="rotate(45, 250, 250)">
      <rect x="240" y="50" width="20" height="400" fill="#BDC3C7" rx="5" />
      <path d="M220,450 Q250,480 280,450 L280,420 L220,420 Z" fill="#BDC3C7" />
    </g>
  </g>

  <!-- TEXT SECTION -->
  <g id="text">
    <!-- Team Name: Owayo -->
    <text x="250" y="460" font-family="Arial, sans-serif" font-weight="bold" font-size="32" text-anchor="middle" fill="#E74C3C">OWAYO</text>
    <!-- Team Name: Eulers -->
    <text x="250" y="495" font-family="Arial, sans-serif" font-weight="900" font-size="48" text-anchor="middle" fill="#FFFFFF" stroke="#2C3E50" stroke-width="2">EULERS</text>
  </g>

  <!-- Decorative Border Ring (to frame the logo) -->
  <circle cx="250" cy="250" r="230" fill="none" stroke="#E74C3C" stroke-width="8" stroke-dasharray="10,5" opacity="0.6" />
</svg>
```
