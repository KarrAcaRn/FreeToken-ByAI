"""Referenz für die erwarteten Werte in tests.pas: sRGB (D65) -> CIELAB -> CIEDE2000 (kL = kC = kH = 1)."""
from math import atan2, cos, degrees, exp, hypot, radians, sin, sqrt

M = ((0.4124564, 0.3575761, 0.1804375), (0.2126729, 0.7151522, 0.0721750), (0.0193339, 0.1191920, 0.9503041))
WHITE = (0.95047, 1.0, 1.08883)


def rgb_to_lab(rgb, m=M, white=WHITE, thr=0.04045):
    lin = [c / 255 / 12.92 if c / 255 <= thr else ((c / 255 + 0.055) / 1.055) ** 2.4 for c in rgb]
    xyz = [sum(m[i][j] * lin[j] for j in range(3)) / white[i] for i in range(3)]
    f = [t ** (1 / 3) if t > (6 / 29) ** 3 else t / (3 * (6 / 29) ** 2) + 4 / 29 for t in xyz]
    return 116 * f[1] - 16, 500 * (f[0] - f[1]), 200 * (f[1] - f[2])


def ciede2000(lab1, lab2):
    L1, a1, b1 = lab1
    L2, a2, b2 = lab2
    Cbar = (hypot(a1, b1) + hypot(a2, b2)) / 2
    G = 0.5 * (1 - sqrt(Cbar ** 7 / (Cbar ** 7 + 25 ** 7)))
    a1p, a2p = (1 + G) * a1, (1 + G) * a2
    C1p, C2p = hypot(a1p, b1), hypot(a2p, b2)
    h1p = degrees(atan2(b1, a1p)) % 360 if C1p else 0.0
    h2p = degrees(atan2(b2, a2p)) % 360 if C2p else 0.0
    dLp, dCp = L2 - L1, C2p - C1p
    if C1p * C2p == 0:
        dhp = 0.0
    elif abs(h2p - h1p) <= 180:
        dhp = h2p - h1p
    elif h2p - h1p > 180:
        dhp = h2p - h1p - 360
    else:
        dhp = h2p - h1p + 360
    dHp = 2 * sqrt(C1p * C2p) * sin(radians(dhp / 2))
    Lbp, Cbp = (L1 + L2) / 2, (C1p + C2p) / 2
    if C1p * C2p == 0:
        hbp = h1p + h2p
    elif abs(h1p - h2p) <= 180:
        hbp = (h1p + h2p) / 2
    elif h1p + h2p < 360:
        hbp = (h1p + h2p + 360) / 2
    else:
        hbp = (h1p + h2p - 360) / 2
    T = 1 - 0.17 * cos(radians(hbp - 30)) + 0.24 * cos(radians(2 * hbp)) + 0.32 * cos(radians(3 * hbp + 6)) - 0.20 * cos(radians(4 * hbp - 63))
    dtheta = 30 * exp(-(((hbp - 275) / 25) ** 2))
    Rc = 2 * sqrt(Cbp ** 7 / (Cbp ** 7 + 25 ** 7))
    Sl = 1 + 0.015 * (Lbp - 50) ** 2 / sqrt(20 + (Lbp - 50) ** 2)
    Sc = 1 + 0.045 * Cbp
    Sh = 1 + 0.015 * Cbp * T
    Rt = -sin(radians(2 * dtheta)) * Rc
    return sqrt((dLp / Sl) ** 2 + (dCp / Sc) ** 2 + (dHp / Sh) ** 2 + Rt * (dCp / Sc) * (dHp / Sh))


def delta_e(c1, c2, **kw):
    return ciede2000(rgb_to_lab(c1, **kw), rgb_to_lab(c2, **kw))


# Sharma, Wu, Dalal (2005), Tabelle 1: Lab-Paare mit veröffentlichtem Delta E 2000.
SHARMA = [
    ((50, 2.6772, -79.7751), (50, 0, -82.7485), 2.0425), ((50, 3.1571, -77.2803), (50, 0, -82.7485), 2.8615),
    ((50, 2.8361, -74.0200), (50, 0, -82.7485), 3.4412), ((50, -1.3802, -84.2814), (50, 0, -82.7485), 1.0000),
    ((50, 0, 0), (50, -1, 2), 2.3669), ((50, -1, 2), (50, 0, 0), 2.3669),
    ((50, 2.49, -0.001), (50, -2.49, 0.0009), 7.1792), ((50, 2.49, -0.001), (50, -2.49, 0.0011), 7.2195),
    ((50, 2.5, 0), (50, 0, -2.5), 4.3065), ((50, 2.5, 0), (73, 25, -18), 27.1492),
    ((50, 2.5, 0), (61, -5, 29), 22.8977), ((50, 2.5, 0), (56, -27, -3), 31.9030),
    ((50, 2.5, 0), (58, 24, 15), 19.4535), ((60.2574, -34.0099, 36.2677), (60.4626, -34.1751, 39.4387), 1.2644),
    ((63.0109, -31.0961, -5.8663), (62.8187, -29.7946, -4.0864), 1.2630), ((22.7233, 20.0904, -46.6940), (23.0331, 14.9730, -42.5619), 2.0373),
    ((90.8027, -2.0831, 1.4410), (91.1528, -1.6435, 0.0447), 1.4441), ((2.0776, 0.0795, -1.1350), (0.9033, -0.0636, -0.5514), 0.9082),
]

PAIRS = [
    ((255, 0, 0), (255, 0, 0)), ((0, 0, 0), (255, 255, 255)), ((128, 128, 128), (130, 130, 130)),
    ((255, 0, 0), (0, 0, 255)), ((0, 0, 255), (0, 0, 200)), ((30, 60, 200), (60, 30, 210)),
    ((255, 0, 128), (255, 40, 0)), ((200, 20, 60), (210, 30, 20)), ((0, 255, 0), (40, 200, 60)),
    ((255, 255, 0), (240, 230, 40)), ((10, 10, 10), (0, 0, 0)), ((120, 200, 180), (100, 190, 200)),
    ((250, 128, 114), (233, 150, 122)), ((70, 130, 180), (100, 149, 237)), ((128, 0, 128), (128, 128, 128)),
]

if __name__ == "__main__":
    worst = max(abs(ciede2000(a, b) - e) for a, b, e in SHARMA)
    print(f"Sharma: größte Abweichung {worst:.5f}")
    variants = [dict(), dict(m=((0.4124, 0.3576, 0.1805), (0.2126, 0.7152, 0.0722), (0.0193, 0.1192, 0.9505))),
                dict(white=(0.95047, 1.0, 1.08883)), dict(white=(0.950456, 1.0, 1.088754)), dict(thr=0.03928),
                dict(white=(0.9505, 1.0, 1.089), m=((0.4124, 0.3576, 0.1805), (0.2126, 0.7152, 0.0722), (0.0193, 0.1192, 0.9505)))]
    for a, b in PAIRS:
        vals = [delta_e(a, b, **v) for v in variants]
        print(a, b, f"{vals[0]:.4f}", f"Streuung der Varianten {max(vals) - min(vals):.4f}")
