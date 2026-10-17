# qwen3_6-35b-a3b - logo-owayo-eulers (2026-10-17T19:31:39)

## Antwort (3959 Tokens, 17.658 s, Ende: stop)

### Denkphase

Der Benutzer möchte ein SVG-Logo für eine Eishockeymannschaft namens "Owayo Eulers". Das Logo soll eine Eule (Euler = Eule auf Englisch/Finnisch/etc.) und einen Eishockeyschläger enthalten. Kein Hintergrund, einfarbiger Hintergrund wird als "kein Hintergrund" bevorzugt.

Ich werde ein vollständiges SVG erstellen mit:
- Einem stilisierten Eulen-Kopf als Wappen/Schild
- Einem Eishockeyschläger (Kreuz oder im Hintergrund)
- Dem Schriftzug "Owayo Eulers"
- Keine externen Ressourcen, alles inline gezeichnet

Ich werde eine schöne, sportliche Darstellung erstellen mit einem klassischen Sport-Logo-Stil.


### Antwort



```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 500 500" width="500" height="500">
  <defs>
    <linearGradient id="shieldGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#1a237e;stop-opacity:1"/>
      <stop offset="100%" style="stop-color:#0d1442;stop-opacity:1"/>
    </linearGradient>
    <linearGradient id="goldGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#ffd54f;stop-opacity:1"/>
      <stop offset="100%" style="stop-color:#f9a825;stop-opacity:1"/>
    </linearGradient>
    <linearGradient id="owlBody" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" style="stop-color:#5c6bc0;stop-opacity:1"/>
      <stop offset="100%" style="stop-color:#283593;stop-opacity:1"/>
    </linearGradient>
  </defs>

  <!-- Äußerer goldener Rand -->
  <polygon points="250,20 470,130 470,350 250,480 30,350 30,130"
           fill="none" stroke="url(#goldGrad)" stroke-width="8" stroke-linejoin="round"/>

  <!-- Schild-Füllung -->
  <polygon points="250,28 462,134 462,346 250,472 38,346 38,134"
           fill="url(#shieldGrad)" stroke="none"/>

  <!-- Weißer innerer Rand -->
  <polygon points="250,36 454,138 454,342 250,464 46,342 46,138"
           fill="none" stroke="#ffffff" stroke-width="2" stroke-linejoin="round"/>

  <!-- Eishockeyschläger - gekreuzt im Hintergrund -->
  <!-- Schläger 1 (von links unten nach rechts oben) -->
  <g transform="rotate(-35, 250, 280)">
    <!-- Schaft -->
    <rect x="240" y="180" width="20" height="200" rx="3" fill="#e0e0e0" stroke="#9e9e9e" stroke-width="1"/>
    <!-- Klinge -->
    <path d="M210,370 Q210,340 230,330 L310,330 Q330,340 330,370 L330,395 Q310,405 290,405 L250,405 Q210,405 210,395 Z"
          fill="#e0e0e0" stroke="#9e9e9e" stroke-width="1"/>
    <!-- Drahtnetz in der Klinge -->
    <line x1="240" y1="332" x2="240" y2="400" stroke="#bdbdbd" stroke-width="0.75"/>
    <line x1="260" y1="332" x2="260" y2="400" stroke="#bdbdbd" stroke-width="0.75"/>
    <line x1="280" y1="332" x2="280" y2="400" stroke="#bdbdbd" stroke-width="0.75"/>
    <line x1="300" y1="332" x2="300" y2="400" stroke="#bdbdbd" stroke-width="0.75"/>
    <line x1="212" y1="350" x2="328" y2="350" stroke="#bdbdbd" stroke-width="0.75"/>
    <line x1="212" y1="370" x2="328" y2="370" stroke="#bdbdbd" stroke-width="0.75"/>
    <line x1="212" y1="390" x2="328" y2="390" stroke="#bdbdbd" stroke-width="0.75"/>
  </g>

  <!-- Schläger 2 (von rechts unten nach links oben) -->
  <g transform="rotate(35, 250, 280)">
    <rect x="240" y="180" width="20" height="200" rx="3" fill="#e0e0e0" stroke="#9e9e9e" stroke-width="1"/>
    <path d="M210,370 Q210,340 230,330 L310,330 Q330,340 330,370 L330,395 Q310,405 290,405 L250,405 Q210,405 210,395 Z"
          fill="#e0e0e0" stroke="#9e9e9e" stroke-width="1"/>
    <line x1="240" y1="332" x2="240" y2="400" stroke="#bdbdbd" stroke-width="0.75"/>
    <line x1="260" y1="332" x2="260" y2="400" stroke="#bdbdbd" stroke-width="0.75"/>
    <line x1="280" y1="332" x2="280" y2="400" stroke="#bdbdbd" stroke-width="0.75"/>
    <line x1="300" y1="332" x2="300" y2="400" stroke="#bdbdbd" stroke-width="0.75"/>
    <line x1="212" y1="350" x2="328" y2="350" stroke="#bdbdbd" stroke-width="0.75"/>
    <line x1="212" y1="370" x2="328" y2="370" stroke="#bdbdbd" stroke-width="0.75"/>
    <line x1="212" y1="390" x2="328" y2="390" stroke="#bdbdbd" stroke-width="0.75"/>
  </g>

  <!-- Eulen-Kopf (Mitte) -->
  <!-- Ohren -->
  <path d="M175,155 L155,95 L210,140 Z" fill="url(#owlBody)" stroke="#3949ab" stroke-width="1"/>
  <path d="M325,155 L345,95 L290,140 Z" fill="url(#owlBody)" stroke="#3949ab" stroke-width="1"/>

  <!-- Kopf -->
  <ellipse cx="250" cy="180" rx="80" ry="70" fill="url(#owlBody)" stroke="#3949ab" stroke-width="2"/>

  <!-- Gesicht (hellere Bereich) -->
  <ellipse cx="250" cy="190" rx="65" ry="55" fill="#7986cb"/>

  <!-- Augenringe -->
  <ellipse cx="215" cy="180" rx="30" ry="28" fill="#e8eaf6"/>
  <ellipse cx="285" cy="180" rx="30" ry="28" fill="#e8eaf6"/>

  <!-- Augen -->
  <circle cx="215" cy="178" r="18" fill="#ffd54f"/>
  <circle cx="285" cy="178" r="18" fill="#ffd54f"/>
  <circle cx="215" cy="178" r="10" fill="#1a237e"/>
  <circle cx="285" cy="178" r="10" fill="#1a237e"/>
  <!-- Augen-Glanz -->
  <circle cx="210" cy="172" r="4" fill="#ffffff"/>
  <circle cx="280" cy="172" r="4" fill="#ffffff"/>

  <!-- Schnabel -->
  <polygon points="242,195 258,195 250,225" fill="#f9a825" stroke="#e65100" stroke-width="1"/>
  <polygon points="244,196 256,196 250,222" fill="#ffb300"/>

  <!-- Körper/Federungen -->
  <path d="M210,230 Q200,270 215,310 L285,310 Q300,270 290,230 Z" fill="url(#owlBody)" stroke="#3949ab" stroke-width="2"/>

  <!-- Brustfedern (V-Form) -->
  <path d="M230,245 L250,260 L270,245" fill="none" stroke="#e8eaf6" stroke-width="2.5" stroke-linecap="round"/>
  <path d="M225,258 L250,275 L275,258" fill="none" stroke="#e8eaf6" stroke-width="2.5" stroke-linecap="round"/>
  <path d="M220,271 L250,290 L280,271" fill="none" stroke="#e8eaf6" stroke-width="2.5" stroke-linecap="round"/>
  <path d="M225,284 L250,300 L275,284" fill="none" stroke="#e8eaf6" stroke-width="2.5" stroke-linecap="round"/>

  <!-- Flügel -->
  <path d="M175,220 Q150,240 155,290 Q160,320 180,310 Q175,270 180,240 Z" fill="#3949ab" stroke="#283593" stroke-width="1.5"/>
  <path d="M325,220 Q350,240 345,290 Q340,320 320,310 Q325,270 320,240 Z" fill="#3949ab" stroke="#283593" stroke-width="1.5"/>

  <!-- Flügel-Details -->
  <line x1="165" y1="250" x2="175" y2="250" stroke="#e8eaf6" stroke-width="1.5" stroke-linecap="round"/>
  <line x1="160" y1="265" x2="178" y2="263" stroke="#e8eaf6" stroke-width="1.5" stroke-linecap="round"/>
  <line x1="158" y1="280" x2="176" y2="278" stroke="#e8eaf6" stroke-width="1.5" stroke-linecap="round"/>
  <line x1="335" y1="250" x2="345" y2="250" stroke="#e8eaf6" stroke-width="1.5" stroke-linecap="round"/>
  <line x1="322" y1="263" x2="340" y2="265" stroke="#e8eaf6" stroke-width="1.5" stroke-linecap="round"/>
  <line x1="324" y1="278" x2="342" y2="280" stroke="#e8eaf6" stroke-width="1.5" stroke-linecap="round"/>

  <!-- Eishockey-Puck (unter der Eule) -->
  <ellipse cx="250" cy="325" rx="22" ry="8" fill="#1a1a2e" stroke="#333" stroke-width="1"/>
  <ellipse cx="250" cy="323" rx="22" ry="7" fill="#2a2a4a"/>

  <!-- Text: OWAYO oben im Bogen -->
  <path id="topArc" d="M100,200 Q250,80 400,200" fill="none"/>
  <text font-family="'Arial Black', 'Impact', sans-serif" font-size="28" font-weight="900" fill="url(#goldGrad)" text-anchor="middle" letter-spacing="4">
    <textPath href="#topArc" startOffset="50%">O W A Y O</textPath>
  </text>

  <!-- Text: EURLS unten im Bogen -->
  <path id="bottomArc" d="M100,340 Q250,460 400,340" fill="none"/>
  <text font-family="'Arial Black', 'Impact', sans-serif" font-size="24" font-weight="900" fill="url(#goldGrad)" text-anchor="middle" letter-spacing="4">
    <textPath href="#bottomArc" startOffset="50%">E U R L S</textPath>
  </text>

  <!-- Kleine Sterne als Dekoration -->
  <polygon points="140,175 143,183 151,183 145,188 147,196 140,191 133,196 135,188 129,183 137,183" fill="#ffd54f" opacity="0.8"/>
  <polygon points="360,175 363,183 371,183 365,188 367,196 360,191 353,196 355,188 349,183 357,183" fill="#ffd54f" opacity="0.8"/>

  <!-- Eishockey-Skate-Laub / Gitter unter dem Puck -->
  <path d="M200,340 Q250,330 300,340" fill="none" stroke="rgba(255,255,255,0.15)" stroke-width="1"/>
  <path d="M195,345 Q250,335 305,345" fill="none" stroke="rgba(255,255,255,0.1)" stroke-width="1"/>
</svg>
```
