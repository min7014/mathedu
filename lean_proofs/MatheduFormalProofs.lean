/-
  MatheduFormalProofs.lean
  ========================
  Pure Lean 4 (v4.36.0) machine-checked formal proofs corresponding to
  core visual-proof topics in the MathEdu interactive catalog.
  Zero external dependencies, zero incomplete placeholders.
-/

-- 1. [2017090101] Pythagorean Theorem via Square Area Dissection
theorem pythagorean_square_dissection
    (a b c : Int)
    (h_partition : (a + b) * (a + b) = c * c + 2 * (a * b)) :
    a * a + b * b = c * c := by
  grind

-- 2. [2014111902] Ceva's Theorem via Triangle Area Ratios
theorem ceva_area_ratio_concurrency
    (bd dc ce ea af fb sA sB sC : Int)
    (hsA : sA > 0) (hsB : sB > 0) (hsC : sC > 0)
    (h1 : bd * sC = dc * sB)
    (h2 : ce * sA = ea * sC)
    (h3 : af * sB = fb * sA) :
    bd * ce * af = dc * ea * fb := by
  have hprod : (bd * ce * af) * (sA * sB * sC) = (dc * ea * fb) * (sA * sB * sC) := by
    calc
      (bd * ce * af) * (sA * sB * sC)
          = (bd * sC) * (ce * sA) * (af * sB) := by grind
      _   = (dc * sB) * (ea * sC) * (fb * sA) := by rw [h1, h2, h3]
      _   = (dc * ea * fb) * (sA * sB * sC) := by grind
  have hs : sA * sB * sC ≠ 0 := by
    have h12 : 0 < sA * sB := Int.mul_pos hsA hsB
    have h123 : 0 < sA * sB * sC := Int.mul_pos h12 hsC
    omega
  exact Int.eq_of_mul_eq_mul_right hs hprod

-- 3. [2014111901] Menelaus' Theorem via Parallel Auxiliary Segment
theorem menelaus_parallel_ratio_product
    (bd dc ce ea af fb ck p q : Int)
    (hck : ck > 0) (hp : p > 0) (hq : q > 0)
    (h1 : bd * ck = dc * p)
    (h2 : ce * q = ea * ck)
    (h3 : af * p = fb * q) :
    bd * ce * af = dc * ea * fb := by
  have hprod : (bd * ce * af) * (ck * p * q) = (dc * ea * fb) * (ck * p * q) := by
    calc
      (bd * ce * af) * (ck * p * q)
          = (bd * ck) * (ce * q) * (af * p) := by grind
      _   = (dc * p) * (ea * ck) * (fb * q) := by rw [h1, h2, h3]
      _   = (dc * ea * fb) * (ck * p * q) := by grind
  have hnz : ck * p * q ≠ 0 := by
    have h12 : 0 < ck * p := Int.mul_pos hck hp
    have h123 : 0 < ck * p * q := Int.mul_pos h12 hq
    omega
  exact Int.eq_of_mul_eq_mul_right hnz hprod

-- 4. [2014080601] Cauchy-Schwarz Inequality in R^2 via Lagrange Identity
theorem cauchy_schwarz_lagrange_r2
    (a1 a2 b1 b2 : Int) :
    (a1 * b1 + a2 * b2) * (a1 * b1 + a2 * b2)
      ≤ (a1 * a1 + a2 * a2) * (b1 * b1 + b2 * b2) := by
  have h_id :
      (a1 * a1 + a2 * a2) * (b1 * b1 + b2 * b2) =
        (a1 * b1 + a2 * b2) * (a1 * b1 + a2 * b2) +
        (a1 * b2 - a2 * b1) * (a1 * b2 - a2 * b1) := by
    grind
  have h_sq : 0 ≤ (a1 * b2 - a2 * b1) * (a1 * b2 - a2 * b1) := by
    by_cases hsign : 0 ≤ a1 * b2 - a2 * b1
    · exact Int.mul_nonneg hsign hsign
    · have hneg : a1 * b2 - a2 * b1 ≤ 0 := by omega
      exact Int.mul_nonneg_of_nonpos_of_nonpos hneg hneg
  omega

-- 5. [2020062702] Arithmetic Mean Midpoint & Square Inequality
theorem arithmetic_mean_and_square_inequality
    (a b m : Int)
    (h_mean : 2 * m = a + b) :
    m - a = b - m ∧ 4 * (a * b) ≤ (a + b) * (a + b) := by
  have h_sq : 0 ≤ (a - b) * (a - b) := by
    by_cases hsign : 0 ≤ a - b
    · exact Int.mul_nonneg hsign hsign
    · have hneg : a - b ≤ 0 := by omega
      exact Int.mul_nonneg_of_nonpos_of_nonpos hneg hneg
  have h_id : (a + b) * (a + b) = 4 * (a * b) + (a - b) * (a - b) := by
    grind
  constructor
  · omega
  · omega

-- 6. [2017091805] Circumcenter Concurrency of Perpendicular Bisectors
theorem circumcenter_perpendicular_bisectors_concurrency
    (dOA dOB dOC : Int)
    (hAB : dOA = dOB)
    (hBC : dOB = dOC) :
    dOA = dOC ∧ dOA = dOB ∧ dOB = dOC := by
  exact ⟨Eq.trans hAB hBC, hAB, hBC⟩

-- 7. [2017091809] Incenter Equidistance & Inradius Area Partition
theorem incenter_angle_bisectors_and_inradius_area
    (r a b c areaBC areaCA areaAB dAB dBC dCA : Int)
    (h1 : dAB = dBC) (h2 : dBC = dCA)
    (hBC : 2 * areaBC = r * a)
    (hCA : 2 * areaCA = r * b)
    (hAB : 2 * areaAB = r * c) :
    dAB = dCA ∧ 2 * (areaBC + areaCA + areaAB) = r * (a + b + c) := by
  constructor
  · exact Eq.trans h1 h2
  · grind

-- 8. [2019111301] Equidistance on a Perpendicular Bisector (Coordinate Proof)
theorem perpendicular_bisector_equidistance
    (ax ay bx by_ mx my px py : Int)
    (hmx : 2 * mx = ax + bx)
    (hmy : 2 * my = ay + by_)
    (hperp : (px - mx) * (bx - ax) + (py - my) * (by_ - ay) = 0) :
    (px - ax) * (px - ax) + (py - ay) * (py - ay) =
      (px - bx) * (px - bx) + (py - by_) * (py - by_) := by
  have h_diff :
      ((px - ax) * (px - ax) + (py - ay) * (py - ay)) -
      ((px - bx) * (px - bx) + (py - by_) * (py - by_)) =
        2 * ((px - mx) * (bx - ax) + (py - my) * (by_ - ay)) := by
    grind
  rw [hperp] at h_diff
  omega

-- 9. [2017091820] Space Diagonal of a Rectangular Prism (6-3-5 Example)
theorem space_diagonal_6_3_5_prism
    (a b c dBaseSq dSpaceSq : Int)
    (hbase : dBaseSq = a * a + b * b)
    (hspace : dSpaceSq = dBaseSq + c * c) :
    dSpaceSq = a * a + b * b + c * c ∧
      6 * 6 + 3 * 3 + 5 * 5 = (70 : Int) := by
  constructor
  · omega
  · decide

-- 10. [2017090405] Base Angles of an Isosceles Triangle
theorem isosceles_base_angles_sum
    (apex b1 b2 : Int)
    (hsum : apex + b1 + b2 = 180)
    (hcong : b1 = b2) :
    apex + 2 * b1 = 180 ∧ 2 * b2 = 180 - apex := by
  omega

-- 11. [2017032702] Denominator Rationalization via Conjugate Difference of Squares
theorem conjugate_rationalization_identity
    (a b sA sB : Int)
    (ha : sA * sA = a)
    (hb : sB * sB = b) :
    (sA + sB) * (sA - sB) = a - b := by
  grind

-- 12. [math20250130001] Pythagoras Tree Generational Area Conservation
theorem pythagoras_tree_area_conservation
    (g0 b1 b2 c1 c2 c3 c4 : Int)
    (hlvl1 : g0 = b1 + b2)
    (hlvl2L : b1 = c1 + c2)
    (hlvl2R : b2 = c3 + c4) :
    g0 = c1 + c2 + c3 + c4 := by
  omega

-- 13. [2012093001] Inscribed Angle Theorem (Central Angle = 2x Inscribed Angle)
theorem inscribed_angle_double_central
    (a1 a2 b1 b2 ext1 ext2 : Int)
    (hisosc1 : a1 = b1) (hsum1 : ext1 = a1 + b1)
    (hisosc2 : a2 = b2) (hsum2 : ext2 = a2 + b2) :
    ext1 + ext2 = 2 * (a1 + a2) := by
  omega

-- 14. [2012100304] Alternate Segment Theorem (Tangent-Chord Angle Equality)
theorem alternate_segment_tangent_chord
    (tangentAngle compAngle inscribedAngle : Int)
    (htan : tangentAngle + compAngle = 90)
    (htri : inscribedAngle + compAngle = 90) :
    tangentAngle = inscribedAngle := by
  omega
