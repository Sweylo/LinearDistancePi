/**************************************************************************************************
 * Cryptocurrency Trading Monk
 * Author: Logan Nichols aka sweylo (logan@sweylo.net)
 * License: ISC License
 *************************************************************************************************/

use clap::Parser;

mod linear_distance_pi;
use linear_distance_pi::Args;

fn main() -> Result<(), Box<dyn std::error::Error>> {

  std::env::set_var("RUST_BACKTRACE", "full");

  // parse cli args
  let args = Args::parse();

  println!("Running with args: {:#?}\n", args);

  Ok(())

}