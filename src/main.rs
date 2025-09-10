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

  let numerator = Integer::from(args.iter);
  let denominator = Integer::from(1u64);

  let now = std::time::Instant::now();

  let sqrt = sqrt(&Rational::from_integers(numerator, denominator), args.prec);

  let mut options = ToSciOptions::default();
	options.set_precision(args.prec);

  println!("{}", sqrt.to_sci_with_options(options));

  println!("\nTime elapsed: {:.2?}\n", now.elapsed());

  Ok(())

}

fn sqrt(x: &Rational, prec: u64) -> Rational {

  let one = Rational::from(1u64);
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
        i -= one.clone();
        break;
      }
      i += one.clone();
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