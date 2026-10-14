// Erwartete Werte aus referenz.py (sRGB D65 -> CIELAB -> CIEDE2000, geprüft gegen Sharma et al. 2005).
// Toleranz 0.05: so weit streuen übliche Varianten der sRGB-Matrix und des Weißpunkts.

const
  Tol = 0.05;

procedure Test_GleicheFarbe;
begin
  CheckNear(DeltaE2000(255, 0, 0, 255, 0, 0), 0.0000, Tol, 'DeltaE2000(255, 0, 0, 255, 0, 0)');
  CheckNear(DeltaE2000(37, 99, 201, 37, 99, 201), 0.0000, Tol, 'DeltaE2000(37, 99, 201, 37, 99, 201)');
end;

procedure Test_SchwarzWeiss;
begin
  CheckNear(DeltaE2000(0, 0, 0, 255, 255, 255), 100.0000, Tol, 'DeltaE2000(0, 0, 0, 255, 255, 255)');
end;

procedure Test_Grautoene;
begin
  CheckNear(DeltaE2000(128, 128, 128, 130, 130, 130), 0.7530, Tol, 'DeltaE2000(128, 128, 128, 130, 130, 130)');
  CheckNear(DeltaE2000(10, 10, 10, 0, 0, 0), 1.5882, Tol, 'DeltaE2000(10, 10, 10, 0, 0, 0)');
end;

procedure Test_RotGegenBlau;
begin
  CheckNear(DeltaE2000(255, 0, 0, 0, 0, 255), 52.8814, Tol, 'DeltaE2000(255, 0, 0, 0, 0, 255)');
end;

procedure Test_Blaubereich;
begin
  CheckNear(DeltaE2000(0, 0, 255, 0, 0, 200), 7.0174, Tol, 'DeltaE2000(0, 0, 255, 0, 0, 200)');
  CheckNear(DeltaE2000(30, 60, 200, 60, 30, 210), 6.7944, Tol, 'DeltaE2000(30, 60, 200, 60, 30, 210)');
  CheckNear(DeltaE2000(70, 130, 180, 100, 149, 237), 10.0015, Tol, 'DeltaE2000(70, 130, 180, 100, 149, 237)');
end;

procedure Test_FarbtonUeberNull;
begin
  CheckNear(DeltaE2000(255, 0, 128, 255, 40, 0), 27.4543, Tol, 'DeltaE2000(255, 0, 128, 255, 40, 0)');
  CheckNear(DeltaE2000(200, 20, 60, 210, 30, 20), 11.4833, Tol, 'DeltaE2000(200, 20, 60, 210, 30, 20)');
end;

procedure Test_GruenGelb;
begin
  CheckNear(DeltaE2000(0, 255, 0, 40, 200, 60), 13.2610, Tol, 'DeltaE2000(0, 255, 0, 40, 200, 60)');
  CheckNear(DeltaE2000(255, 255, 0, 240, 230, 40), 5.5879, Tol, 'DeltaE2000(255, 255, 0, 240, 230, 40)');
end;

procedure Test_Gemischt;
begin
  CheckNear(DeltaE2000(120, 200, 180, 100, 190, 200), 11.7269, Tol, 'DeltaE2000(120, 200, 180, 100, 190, 200)');
  CheckNear(DeltaE2000(250, 128, 114, 233, 150, 122), 8.0595, Tol, 'DeltaE2000(250, 128, 114, 233, 150, 122)');
  CheckNear(DeltaE2000(128, 0, 128, 128, 128, 128), 34.6783, Tol, 'DeltaE2000(128, 0, 128, 128, 128, 128)');
end;

procedure Test_Symmetrie;
begin
  CheckNear(DeltaE2000(255, 40, 0, 255, 0, 128), DeltaE2000(255, 0, 128, 255, 40, 0), 1e-9, 'Vertauschte Farben');
  CheckNear(DeltaE2000(60, 30, 210, 30, 60, 200), DeltaE2000(30, 60, 200, 60, 30, 210), 1e-9, 'Vertauschte Farben');
end;
