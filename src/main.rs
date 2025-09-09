/**************************************************************************************************
 * Cryptocurrency Trading Monk
 * Author: Logan Nichols aka sweylo (logan@sweylo.net)
 * License: ISC License
 *************************************************************************************************/

use malachite::num::arithmetic::traits::Pow;
use malachite::num::conversion::string::options::ToSciOptions;
use malachite::num::conversion::traits::ToSci;
use malachite::Rational;

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
	println!("{}", Rational::from(3).pow(-1_000_000i64).to_sci_with_options(options));

  Ok(())

}