use malachite::Integer;
use malachite_base::num::arithmetic::traits::Pow;
use malachite_base::num::conversion::string::options::ToSciOptions;
use malachite_base::num::conversion::traits::ToSci;
use malachite::rational::Rational;


pub fn estimate(iter: u64, pow: u64, prec: u64) -> String {

  let n_dec = get_n_dec(iter, pow, prec);
	let n_dec_fast = get_n_dec_fast(iter, pow, prec);
  let mut arclen = Rational::from(0u64);
  let mut x1 = Rational::from(0u64);
  let mut y1 = circle_func(&x1, prec);
  
  for i in 0..iter {
    let x2 = Rational::from(i + 1u64) / &n_dec;
    let y2 = circle_func(&x2, prec);
    let dist = sqrt(&((&x2 - &x1).pow(2u64) + (&y2 - &y1).pow(2u64)), prec);
    arclen += dist;
    x1 = x2;
    y1 = y2;
  }

	let mut options = ToSciOptions::default();
	options.set_precision(prec);

	println!("n_dec: {}", n_dec.to_sci_with_options(options).to_string());
	println!("n_dec_fast: {}", n_dec_fast.to_sci_with_options(options).to_string());
	println!("n_dec_ratio: {}", (&n_dec / &n_dec_fast).to_sci_with_options(options).to_string());

  let pi_est = Rational::from(2u64).pow(pow) * arclen;

	arclen = Rational::from(0u64);
  x1 = Rational::from(0u64);
  y1 = circle_func(&x1, prec);

	for i in 0..iter {
    let x2 = Rational::from(i + 1u64) / &n_dec_fast;
    let y2 = circle_func(&x2, prec);
    let dist = sqrt(&((&x2 - &x1).pow(2u64) + (&y2 - &y1).pow(2u64)), prec);
    arclen += dist;
    x1 = x2;
    y1 = y2;
  }

  let pi_est_fast = Rational::from(2u64).pow(pow) * arclen;

	println!("\nEstimated Pi: {}", pi_est.to_sci_with_options(options).to_string());
	println!("Estimated Pi: {}", pi_est_fast.to_sci_with_options(options).to_string());
	
	return pi_est.to_sci_with_options(options).to_string();

}


fn circle_func(x: &Rational, prec: u64) -> Rational {
  return sqrt(&(Rational::from(1u64) - x.pow(2u64)), prec);
}


fn get_n_dec(n: u64, power: u64, precision: u64) -> Rational {

  let mut pow = power;
  let mut prec = precision;
	let mut options = ToSciOptions::default();
	options.set_precision(prec);
  
  if pow <= 3 {
    eprintln!("Warning: pow <= 3 not supported, setting to 4");
    pow = 4;
  } 

  pow -= 3;
  prec += 2;

  let mut n_dec = Rational::from(n);
  let mut cos_expansion = sqrt(&Rational::from(2u64), prec);

  for i in 0..pow {
    cos_expansion = sqrt(&(&Rational::from(2u64) + &cos_expansion), prec);
		println!("cos_expansion ({}): {}", i, cos_expansion.to_sci_with_options(options).to_string());
  }

	let one_half = Rational::from_integers(Integer::from(1u64), Integer::from(2u64));
	let outer_sqrt = sqrt(&(Rational::from(2u64) - &cos_expansion), prec);
	println!("outer_sqrt: {}", outer_sqrt.to_sci_with_options(options).to_string());

  n_dec = n_dec / (one_half * outer_sqrt);
	// println!("n_dec: {}", n_dec.to_sci_with_options(options).to_string());

  return n_dec;

}


fn get_n_dec_fast(n: u64, power: u64, precision: u64) -> Rational {

  let mut pow = power;
  let mut prec = precision;
	let mut options = ToSciOptions::default();
	options.set_precision(prec + 5);
  
  if pow <= 3 {
    eprintln!("Warning: pow <= 3 not supported, setting to 4");
    pow = 4;
  } 

  pow -= 3;
  prec += 2;

  let mut n_dec = Rational::from(n);
  // let mut cos_expansion = sqrt(&Rational::from(2u64), prec);
	let inside = &Rational::from_integers(Integer::from(1u64), Integer::from(10u64).pow(prec-3));
	println!("inside: {}", inside.to_sci_with_options(options).to_string());
	let cos_expansion = Rational::from(2u64) - inside;
	println!("cos_expansion ( 0): {}", cos_expansion.to_sci_with_options(options).to_string());

  // for _ in 0..pow {
  //   cos_expansion = sqrt(&(&Rational::from(2u64) + &cos_expansion), prec);
	// 	println!("cos_expansion: {}", cos_expansion.to_sci_with_options(options).to_string());
  // }

	let one_half = Rational::from_integers(Integer::from(1u64), Integer::from(2u64));
	let outer_sqrt = sqrt(&(Rational::from(2u64) - &cos_expansion), prec);
	println!("outer_sqrt: {}", outer_sqrt.to_sci_with_options(options).to_string());

  n_dec = n_dec / (one_half * outer_sqrt);

	// println!("n_dec: {}", n_dec.to_sci_with_options(options).to_string());

  return n_dec;

}


fn sqrt(x: &Rational, prec: u64) -> Rational {

  let mut res = Rational::from(1u64);
  let mut req = x.clone();

  for _ in 0..prec {
    let mut i = Rational::from(0u64);
    loop {
      let check = &res + &i;
      let term = check.pow(2u64);
      // println!("i = {}", i);
      // println!("check = {}", check);
      // println!("term = {}", term);
      // println!("req = {}", req);
      // println!("res = {}", res);
      // println!();
      if term > req {
        i -= Rational::from(1u64);
        break;
      }
      i += Rational::from(1u64);
      // std::thread::sleep(std::time::Duration::from_millis(1000));
    }
    res = Rational::from(10u64) * (res + i);
    req *= Rational::from(100u64);
    // println!("res = {}", res);
    // println!("req = {}", req);
    // println!("-------------------");
  }

  return res / Rational::from(10u64).pow(prec as u64);
  
}

// fn sqrt(number: &Rational, iterations: u64) -> Rational {
// 	let start = number.clone();
// 	let mut approx = start.clone();
// 	let mut options = ToSciOptions::default();
// 	options.set_precision(iterations);

// 	println!("Start: {}", start.to_sci_with_options(options).to_string());

// 	for _ in 0..iterations {
// 		approx = (&approx + (&start / &approx)) /
// 				Rational::from(2u64);
// 		println!("Approx: {}", approx.to_sci_with_options(options).to_string());
// 	}

// 	approx
// }