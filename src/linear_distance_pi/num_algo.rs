use num::FromPrimitive;
use num::ToPrimitive;
use num::bigint::BigInt;
use num::rational::{Ratio, BigRational};


pub fn estimate(iter: usize, pow: i32, prec: usize) -> String {

  let n_dec = get_n_dec(iter, pow, prec);
  let mut arclen = Ratio::from_u64(0u64).unwrap();
  let mut x1 = Ratio::from_u64(0u64).unwrap();
  let mut y1 = circle_func(&x1, prec);
  
  for i in 0..iter {
    let x2 = Ratio::from_usize(i + 1).unwrap() / &n_dec;
    let y2 = circle_func(&x2, prec);
    let dist = sqrt(&((&x2 - &x1).pow(2) + (&y2 - &y1).pow(2)), prec);
    arclen += dist;
    x1 = x2;
    y1 = y2;
  }

	// let mut options = ToSciOptions::default();
	// options.set_precision(prec);

	let two:Ratio<BigInt> = Ratio::from_u64(2u64).unwrap();
  let pi_est = two.pow(pow) * arclen;

	// return pi_est.to_sci_with_options(options).to_string();
	return pi_est.to_string();

}


fn circle_func(x: &BigRational, prec: usize) -> BigRational {
  return sqrt(&(Ratio::from_u64(1u64).unwrap() - x.pow(2)), prec);
}


fn get_n_dec(n: usize, power: i32, precision: usize) -> BigRational {

  let mut pow = power;
  let mut prec = precision;
  
  if pow <= 3 {
    eprintln!("Warning: pow <= 3 not supported, setting to 4");
    pow = 4;
  } 

  pow -= 3;
  prec += 2;

  let mut n_dec = Ratio::from_usize(n).unwrap();
  let mut cos_expansion = sqrt(&Ratio::from_u64(2u64).unwrap(), prec);

  for _ in 0..pow {
    cos_expansion = sqrt(&(&Ratio::from_u64(2u64).unwrap() + &cos_expansion), prec);
  }

  n_dec = n_dec / (Ratio::from_f64(0.5f64).unwrap() * sqrt(&(Ratio::from_u64(2u64).unwrap() - cos_expansion), prec));

  return n_dec;

}

fn sqrt(number: &BigRational, iterations: usize) -> BigRational {
	let start = number.clone();
	let mut approx = start.clone();

	println!("Start: {}", start.to_f64().unwrap());

	for _ in 0..iterations {
		approx = (&approx + (&start / &approx)) /
				Ratio::from_integer(FromPrimitive::from_u64(2).unwrap());
		println!("Approx: {}", approx.to_f64().unwrap());
	}

	approx
}