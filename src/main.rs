/**************************************************************************************************
 * Linear Distance Pi Algorithm
 * Author: Logan Nichols aka sweylo (logan@sweylo.net)
 * License: MIT License
 *************************************************************************************************/

use std;

use malachite_base::num::arithmetic::traits::Pow;
// use malachite_base::num::arithmetic::traits::Sqrt;
use malachite_base::num::arithmetic::traits::FloorSqrt;
use malachite_base::num::conversion::string::options::ToSciOptions;
use malachite_base::num::conversion::traits::ToSci;
use malachite::rational::Rational;
use malachite::natural::Natural;
// use malachite::natural::arithmetic::sqrt::FloorSqrt;

use clap::Parser;

mod linear_distance_pi;
use linear_distance_pi::Args;

fn main() -> Result<(), Box<dyn std::error::Error>> {

  std::env::set_var("RUST_BACKTRACE", "full");

  // parse cli args
  let args = Args::parse();

  println!("Running with args: {:#?}\n", args);

	let mut options = ToSciOptions::default();
	options.set_precision(args.prec);
	println!("{}", Rational::from(2).pow(3i64).to_sci_with_options(options));
  println!("{}", Natural::from(2u64).floor_sqrt().to_sci_with_options(options));

  Ok(())

}