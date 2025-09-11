/**************************************************************************************************
 * Linear Distance Pi Algorithm
 * Author: Logan Nichols aka sweylo (logan@sweylo.net)
 * License: MIT License
 *************************************************************************************************/

use std;

use malachite::Integer;
use malachite_base::num::arithmetic::traits::Pow;
use malachite_base::num::conversion::string::options::ToSciOptions;
use malachite_base::num::conversion::traits::ToSci;
use malachite::rational::Rational;

use clap::Parser;

mod linear_distance_pi;
use linear_distance_pi::Args;

fn main() -> Result<(), Box<dyn std::error::Error>> {

  std::env::set_var("RUST_BACKTRACE", "full");

  // parse cli args
  let args = Args::parse();

  println!("\nRunning with args: {:#?}\n", args);

  let mut options = ToSciOptions::default();
	options.set_precision(args.prec);

  let now = std::time::Instant::now();

  let pi_est = estimate(args.iter, args.pow, args.prec);

  println!("\nEstimated Pi: {}", pi_est.to_sci_with_options(options));
  println!("\nTime elapsed: {:.2?}\n", now.elapsed());

  Ok(())

}

fn estimate(iter: u64, pow: u64, prec: u64) -> Rational {

  let n_dec = get_n_dec(iter, pow, prec);
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

  return Rational::from(2u64).pow(pow) * arclen;

}

fn circle_func(x: &Rational, prec: u64) -> Rational {
  return sqrt(&(Rational::from(1u64) - x.pow(2u64)), prec);
}

fn get_n_dec(n: u64, power: u64, precision: u64) -> Rational {

  let mut pow = power;
  let mut prec = precision;
  
  if pow <= 3 {
    eprintln!("Warning: pow <= 3 not supported, setting to 4");
    pow = 4;
  } 

  pow -= 3;
  prec += 2;

  let mut n_dec = Rational::from(n);
  let mut cos_expansion = sqrt(&Rational::from(2u64), prec);

  for _ in 0..pow {
    cos_expansion = sqrt(&(&Rational::from(2u64) + &cos_expansion), prec);
  }

  n_dec = n_dec / (Rational::from_integers(Integer::from(1u64), Integer::from(2u64)) * sqrt(&(Rational::from(2u64) - cos_expansion), prec));

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