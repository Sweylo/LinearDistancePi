#!.venv/bin/python

"""
High-precision nested-radical / polygon π approximation
------------------------------------------------------

This script implements the polygon-based nested-radical approach for
approximating pi using only integer arithmetic and square roots.
It uses a fixed-point representation where numbers are integers
scaled by 2**SHIFT (binary fixed point). The main heavy-lift is
`isqrt` on large integers (via gmpy2); gmpy2/GMP will be much faster
than pure-Python arithmetic.

Features
- Fixed-point integer arithmetic (scale = 2**SHIFT)
- Start from sin(pi/6)=1/2 and repeatedly apply half-angle recurrences
  to compute sin(pi / (6 * 2^m))
- Use gmpy2.isqrt (fast integer sqrt) for numerical stability / speed
- Optional parallel benchmark mode: compute approximations at several
  precisions in parallel (useful to stress-test hardware / GMP)

Notes on parallelism
- The nested-radical chain is sequential: each iteration depends on the
  previous. That structural dependency limits intra-algo parallelism.
- However, the heavy operations (large integer mul/div used inside
  `isqrt`) are handled by gmpy2/GMP which use optimized algorithms
  (Karatsuba, Toom-Cook, FFT) and may be multi-threaded depending on
  how GMP was built. Building GMP with multi-threading and using a
  multiprocess benchmarking wrapper is often the practical route.
- For ultra-high throughput you'd implement the underlying big-int
  arithmetic and FFT multiplication in low-level code (C/C++), then
  expose it to Python; a sketch for that is given at the end of this
  file.

Usage
  python nested_radical_pi.py --iterations 10 --shift 16384

Requires
  pip install gmpy2

"""

from __future__ import annotations
import argparse
import time
from dataclasses import dataclass
import sys

import gmpy2
from gmpy2 import mpz
from tqdm import tqdm


@dataclass
class FixedPointConfig:
  # Number of fractional bits for fixed-point scaling (power of two scale)
  SHIFT: int = 4096  # default — increase for more precision

  @property
  def SCALE(self) -> mpz:
    return mpz(1) << self.SHIFT


def fp_from_rational(num: int, den: int, cfg: FixedPointConfig) -> mpz:
  """Return fixed-point integer representing num/den scaled by 2**SHIFT."""
  return (mpz(num) * (mpz(1) << cfg.SHIFT)) // mpz(den)


def fp_to_decimal_str(x: mpz, cfg: FixedPointConfig, digits: int = 50) -> str:
  """Convert fixed-point integer to a decimal string with `digits` digits after point.
  This is a simple conversion — not optimized for extreme speed, but fine for output.
  """
  # integer part
  intpart = x >> cfg.SHIFT
  frac = x - (intpart << cfg.SHIFT)
  # convert fractional part to decimal by repeated multiplication
  tenpow = 10 ** digits
  frac_as_int = (frac * tenpow) >> cfg.SHIFT
  sys.set_int_max_str_digits(max(650, digits + 10))  # avoid Python warning for large ints
  return f"{int(intpart)}.{str(int(frac_as_int)).rjust(digits, '0')}"


def fp_isqrt(a: mpz) -> mpz:
  """Integer square root using gmpy2.isqrt — returns floor(sqrt(a))."""
  return gmpy2.isqrt(a)


def fp_mul(a: mpz, b: mpz) -> mpz:
  """Multiply two fixed-point numbers (scaled by 2**SHIFT) and return fixed-point scaled product.
  (a * b) >> SHIFT
  """
  return (a * b) >> cfg.SHIFT


def compute_pi_nested_polygon(iterations: int, cfg: FixedPointConfig) -> mpz:
  """Compute polygon perimeter approximation of pi via nested half-angle recurrences.

  We track h = sin(pi / current_n) in fixed-point. Start with sin(pi/6) = 1/2.
  Recurrence (half-angle for sine):
    cos_theta = sqrt(1 - h^2)
    h_next = sqrt((1 - cos_theta) / 2)

  All operations are done in fixed-point integers.
  After `iterations` doublings, n = 6 * (2**iterations). perimeter = n * (2*h)
  """
  SHIFT = cfg.SHIFT
  SCALE = cfg.SCALE

  # starting h = sin(pi/6) = 1/2
  h = SCALE // 2  # fixed-point

  for i in tqdm(range(iterations)):
    # compute h^2 in fixed-point: (h*h) >> SHIFT
    h2 = (h * h) >> SHIFT

    # compute 1 - h^2 in fixed-point
    one_fp = SCALE
    inner = one_fp - h2
    if inner <= 0:
      raise ValueError("numeric underflow in inner sqrt; increase SHIFT")

    # cos_theta = sqrt(1 - h^2)  --> sqrt(inner / SCALE) scaled by SCALE
    # integer sqrt of (inner * SCALE) gives sqrt(inner/SCALE) scaled by SCALE
    cos_theta = fp_isqrt(inner * SCALE)

    # compute (1 - cos_theta) / 2 in fixed-point
    numer = one_fp - cos_theta
    # divide by 2: shift right 1
    numer = numer >> 1

    # h_next = sqrt(numer / SCALE) scaled by SCALE -> isqrt(numer * SCALE)
    h = fp_isqrt(numer * SCALE)

  # after iterations, number of sides
  n = mpz(6) * (mpz(1) << iterations)
  # side length = 2 * h  (fixed-point)
  side = (h << 1)
  # perimeter = n * side  (fixed-point)
  perimeter = n * side
  return perimeter // 2


def benchmark(iterations: int, shift: int, show_time: bool = True):
  cfg = FixedPointConfig(SHIFT=shift)
  t0 = time.time()
  pi = compute_pi_nested_polygon(iterations, cfg)
  t1 = time.time()
  if show_time:
    print(f"Completed: iterations={iterations}, SHIFT={shift}, time={t1-t0:.3f}s")
  # approximate digits recovered: roughly SHIFT * log10(2)  (very rough)
  approx_digits = int(shift * 0.30102999566398114)
  print(f"Estimated decimal precision: ~{approx_digits} digits")
  s = fp_to_decimal_str(pi, cfg, digits=min(80, approx_digits))
  print("pi ≈ ")
  print(s)
  return pi


if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='High-precision nested-radical pi via polygon doubling')
	parser.add_argument('--iterations', '-m', type=int, default=10, help='number of doublings (m)')
	parser.add_argument('--shift', '-s', type=int, default=4096, help='fixed-point fractional bits (SHIFT)')
	parser.add_argument('--benchmark-multiprecision', '-b', action='store_true', help='run multiprecision parallel benchmark (spawns workers)')
	args = parser.parse_args()

	iterations = args.iterations
	shift = args.shift

	approx_digits = int(shift * 0.30102999566398114)
	print(f"Estimated decimal precision: ~{approx_digits} digits")

	# Basic run
	cfg = FixedPointConfig(SHIFT=shift)
	print(f"Running nested-radical polygon pi with iterations={iterations}, SHIFT={shift}")
	print('Note: this uses gmpy2.isqrt for big-integer sqrt operations (fast).')
	pi = compute_pi_nested_polygon(iterations, cfg)

	print(fp_to_decimal_str(pi, cfg, digits=approx_digits))

	# multiprecision benchmark mode (if requested) — spawn multiple processes
	if args.benchmark_multiprecision:
		import multiprocessing as mp
		shifts = [shift // 2, shift, shift * 2]
		def worker(s):
			return benchmark(iterations, s, show_time=True)
		with mp.Pool(processes=min(3, mp.cpu_count())) as pool:
			results = pool.map(worker, shifts)


# END

# ------------------------------------------------------------
# Notes for a low-level parallel implementation (C/C++ sketch)
# ------------------------------------------------------------
# 1) Use a binary fixed-point representation (base = 2) so shifts are cheap.
# 2) Implement big-integer arithmetic with FFT multiplication (Schonhage–Strassen
#    or better) and make it multi-threaded (divide the FFT across threads).
# 3) Implement integer sqrt using Newton iterations. Each Newton step needs a
#    few big multiplications and one division; these multiplications are the
#    place to exploit FFT + multi-threading.
# 4) Optionally: compute the nested radical chain to moderate depth (cheap)
#    in high precision, then switch to an AGM or Chudnovsky method for the
#    final stretch; the latter parallelizes better at the term level.
# 5) Expose the low-level library to Python via cffi / cython for orchestration.
#
# If you'd like, I can sketch the C implementation outline and the math to
# parallelize FFT-based multiplication and Newton sqrt more explicitly.
