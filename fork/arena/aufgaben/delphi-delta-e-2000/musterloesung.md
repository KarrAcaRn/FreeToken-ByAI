```delphi
uses
  System.Math;

function SrgbToLinear(C: Byte): Double;
var
  V: Double;
begin
  V := C / 255.0;
  if V <= 0.04045 then
    Result := V / 12.92
  else
    Result := Power((V + 0.055) / 1.055, 2.4);
end;

function LabF(T: Double): Double;
const
  Delta = 6.0 / 29.0;
begin
  if T > Delta * Delta * Delta then
    Result := Power(T, 1.0 / 3.0)
  else
    Result := T / (3.0 * Delta * Delta) + 4.0 / 29.0;
end;

procedure RgbToLab(R, G, B: Byte; out L, A, BB: Double);
var
  Rl, Gl, Bl, X, Y, Z: Double;
begin
  Rl := SrgbToLinear(R);
  Gl := SrgbToLinear(G);
  Bl := SrgbToLinear(B);
  X := (0.4124564 * Rl + 0.3575761 * Gl + 0.1804375 * Bl) / 0.95047;
  Y := (0.2126729 * Rl + 0.7151522 * Gl + 0.0721750 * Bl) / 1.0;
  Z := (0.0193339 * Rl + 0.1191920 * Gl + 0.9503041 * Bl) / 1.08883;
  L := 116.0 * LabF(Y) - 16.0;
  A := 500.0 * (LabF(X) - LabF(Y));
  BB := 200.0 * (LabF(Y) - LabF(Z));
end;

function HueDeg(B, A: Double): Double;
begin
  if (A = 0) and (B = 0) then
    Exit(0);
  Result := RadToDeg(ArcTan2(B, A));
  if Result < 0 then
    Result := Result + 360.0;
end;

function DeltaE2000(R1, G1, B1, R2, G2, B2: Byte): Double;
var
  L1, A1, Bb1, L2, A2, Bb2: Double;
  CBar, G, A1p, A2p, C1p, C2p, H1p, H2p, DLp, DCp, Dhp, DHpBig: Double;
  LBp, CBp, HBp, T, DTheta, Rc, Sl, Sc, Sh, Rt: Double;
begin
  RgbToLab(R1, G1, B1, L1, A1, Bb1);
  RgbToLab(R2, G2, B2, L2, A2, Bb2);
  CBar := (Hypot(A1, Bb1) + Hypot(A2, Bb2)) / 2.0;
  G := 0.5 * (1.0 - Sqrt(Power(CBar, 7) / (Power(CBar, 7) + Power(25.0, 7))));
  A1p := (1.0 + G) * A1;
  A2p := (1.0 + G) * A2;
  C1p := Hypot(A1p, Bb1);
  C2p := Hypot(A2p, Bb2);
  H1p := HueDeg(Bb1, A1p);
  H2p := HueDeg(Bb2, A2p);

  DLp := L2 - L1;
  DCp := C2p - C1p;
  if C1p * C2p = 0 then
    Dhp := 0
  else if Abs(H2p - H1p) <= 180.0 then
    Dhp := H2p - H1p
  else if H2p - H1p > 180.0 then
    Dhp := H2p - H1p - 360.0
  else
    Dhp := H2p - H1p + 360.0;
  DHpBig := 2.0 * Sqrt(C1p * C2p) * Sin(DegToRad(Dhp / 2.0));

  LBp := (L1 + L2) / 2.0;
  CBp := (C1p + C2p) / 2.0;
  if C1p * C2p = 0 then
    HBp := H1p + H2p
  else if Abs(H1p - H2p) <= 180.0 then
    HBp := (H1p + H2p) / 2.0
  else if H1p + H2p < 360.0 then
    HBp := (H1p + H2p + 360.0) / 2.0
  else
    HBp := (H1p + H2p - 360.0) / 2.0;

  T := 1.0 - 0.17 * Cos(DegToRad(HBp - 30.0)) + 0.24 * Cos(DegToRad(2.0 * HBp))
     + 0.32 * Cos(DegToRad(3.0 * HBp + 6.0)) - 0.20 * Cos(DegToRad(4.0 * HBp - 63.0));
  DTheta := 30.0 * Exp(-Sqr((HBp - 275.0) / 25.0));
  Rc := 2.0 * Sqrt(Power(CBp, 7) / (Power(CBp, 7) + Power(25.0, 7)));
  Sl := 1.0 + 0.015 * Sqr(LBp - 50.0) / Sqrt(20.0 + Sqr(LBp - 50.0));
  Sc := 1.0 + 0.045 * CBp;
  Sh := 1.0 + 0.015 * CBp * T;
  Rt := -Sin(DegToRad(2.0 * DTheta)) * Rc;

  Result := Sqrt(Sqr(DLp / Sl) + Sqr(DCp / Sc) + Sqr(DHpBig / Sh) + Rt * (DCp / Sc) * (DHpBig / Sh));
end;
```
