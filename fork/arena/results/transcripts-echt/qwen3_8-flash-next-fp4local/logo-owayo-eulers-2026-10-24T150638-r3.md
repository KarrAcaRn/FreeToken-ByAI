# qwen3_8-flash-next-fp4local - logo-owayo-eulers (2026-10-24T15:06:38)

## Antwort (2834 Tokens, 79.484 s, Ende: stop)

### Denkphase

The user is requesting a logo SVG of an owl and a hockey stick for the "Owayo Eulers." Create an SVG with no background, including an owl with crossed hockey sticks, along with text. Output only one SVG code block.


### Antwort



```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 460" width="400" height="460">
  <defs>
    <linearGradient id="bodyGrad" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#4a5a72"/>
      <stop offset="100%" stop-color="#2b3648"/>
    </linearGradient>
    <linearGradient id="stickGrad" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#c98a4b"/>
      <stop offset="100%" stop-color="#8a5a2b"/>
    </linearGradient>
  </defs>

  <!-- Gekreuzte Eishockeyschläger hinter der Eule -->
  <g stroke="#1a2230" stroke-width="2">
    <!-- Schläger 1 (von links oben nach rechts unten) -->
    <g transform="rotate(35 200 230)">
      <rect x="192" y="40" width="16" height="300" rx="7" fill="url(#stickGrad)"/>
      <path d="M 192 330 Q 190 365 165 375 Q 145 382 140 372 Q 138 362 155 352 Q 178 340 180 328 Z" fill="#2b3648"/>
      <rect x="192" y="40" width="16" height="45" rx="7" fill="#1a2230"/>
    </g>
    <!-- Schläger 2 (gespiegelt) -->
    <g transform="rotate(-35 200 230)">
      <rect x="192" y="40" width="16" height="300" rx="7" fill="url(#stickGrad)"/>
      <path d="M 208 330 Q 210 365 235 375 Q 255 382 260 372 Q 262 362 245 352 Q 222 340 220 328 Z" fill="#2b3648"/>
      <rect x="192" y="40" width="16" height="45" rx="7" fill="#1a2230"/>
    </g>
  </g>

  <!-- Eule -->
  <g>
    <!-- Ohren / Federbüschel -->
    <path d="M 138 118 L 128 78 L 160 105 Z" fill="#2b3648" stroke="#1a2230" stroke-width="2"/>
    <path d="M 262 118 L 272 78 L 240 105 Z" fill="#2b3648" stroke="#1a2230" stroke-width="2"/>

    <!-- Körper -->
    <path d="M 200 85 C 140 85 110 135 110 195 C 110 265 150 320 200 320 C 250 320 290 265 290 195 C 290 135 260 85 200 85 Z"
          fill="url(#bodyGrad)" stroke="#1a2230" stroke-width="3"/>

    <!-- Flügel -->
    <path d="M 115 170 C 100 210 105 265 135 295 C 140 265 132 210 138 175 Z" fill="#1f2836" stroke="#1a2230" stroke-width="2"/>
    <path d="M 285 170 C 300 210 295 265 265 295 C 260 265 268 210 262 175 Z" fill="#1f2836" stroke="#1a2230" stroke-width="2"/>

    <!-- Bauch mit Feder Muster -->
    <path d="M 200 175 C 165 175 150 215 150 250 C 150 290 172 312 200 312 C 228 312 250 290 250 250 C 250 215 235 175 200 175 Z"
          fill="#d9e2ec" stroke="#1a2230" stroke-width="2"/>
    <g fill="none" stroke="#8d99ae" stroke-width="2">
      <path d="M 172 205 Q 180 218 188 205 Q 196 218 204 205 Q 212 218 220 205 Q 228 218 232 208"/>
      <path d="M 165 235 Q 173 248 181 235 Q 189 248 197 235 Q 205 248 213 235 Q 221 248 229 235 Q 235 245 237 240"/>
      <path d="M 168 265 Q 176 278 184 265 Q 192 278 200 265 Q 208 278 216 265 Q 224 278 232 265"/>
      <path d="M 178 292 Q 186 303 194 292 Q 202 303 210 292 Q 218 303 222 295"/>
    </g>

    <!-- Gesichtsscheibe -->
    <path d="M 200 105 C 155 105 130 135 130 170 C 130 205 160 220 200 220 C 240 220 270 205 270 170 C 270 135 245 105 200 105 Z"
          fill="#e8edf2" stroke="#1a2230" stroke-width="2.5"/>

    <!-- Augenringe -->
    <circle cx="168" cy="160" r="30" fill="#f4a300" stroke="#1a2230" stroke-width="2.5"/>
    <circle cx="232" cy="160" r="30" fill="#f4a300" stroke="#1a2230" stroke-width="2.5"/>
    <!-- Augenweiß -->
    <circle cx="168" cy="160" r="21" fill="#ffffff" stroke="#1a2230" stroke-width="1.5"/>
    <circle cx="232" cy="160" r="21" fill="#ffffff" stroke="#1a2230" stroke-width="1.5"/>
    <!-- Pupillen (entfernt blickend, konzentriert) -->
    <circle cx="172" cy="158" r="10" fill="#1a2230"/>
    <circle cx="228" cy="158" r="10" fill="#1a2230"/>
    <circle cx="175" cy="154" r="3.5" fill="#ffffff"/>
    <circle cx="231" cy="154" r="3.5" fill="#ffffff"/>

    <!-- Zornige Augenbrauen -->
    <path d="M 140 138 L 192 128 L 192 137 L 146 146 Z" fill="#1a2230"/>
    <path d="M 260 138 L 208 128 L 208 137 L 254 146 Z" fill="#1a2230"/>

    <!-- Schnabel -->
    <path d="M 200 172 L 212 190 L 200 208 L 188 190 Z" fill="#e07b00" stroke="#1a2230" stroke-width="2"/>

    <!-- Füße / Krallen -->
    <g fill="#e07b00" stroke="#1a2230" stroke-width="2">
      <path d="M 170 315 Q 168 330 158 335 Q 168 336 172 328 Q 174 336 182 336 Q 178 328 178 315 Z"/>
      <path d="M 230 315 Q 232 330 242 335 Q 232 336 228 328 Q 226 336 218 336 Q 222 328 222 315 Z"/>
    </g>
  </g>

  <!-- Eishockey-Puck -->
  <g>
    <ellipse cx="200" cy="348" rx="26" ry="9" fill="#1a2230"/>
    <rect x="174" y="340" width="52" height="8" fill="#1a2230"/>
    <ellipse cx="200" cy="340" rx="26" ry="9" fill="#2e3a4e"/>
  </g>

  <!-- Teamname -->
  <text x="200" y="398" font-family="Arial Black, Arial, sans-serif" font-size="36" font-weight="900"
        text-anchor="middle" fill="#1a2230" letter-spacing="2">OWAYO</text>
  <text x="200" y="440" font-family="Arial Black, Arial, sans-serif" font-size="36" font-weight="900"
        text-anchor="middle" fill="#f4a300" letter-spacing="3">EULERS</text>
</svg>
```
