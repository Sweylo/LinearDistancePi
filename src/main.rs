/**************************************************************************************************
 * Linear Distance Pi Algorithm
 * Author: Logan Nichols aka sweylo (logan@sweylo.net)
 * License: MIT License
 *************************************************************************************************/

use std;

use clap::Parser;

mod linear_distance_pi;
use linear_distance_pi::Args;
use linear_distance_pi::malachite_algo;
use linear_distance_pi::num_algo;

fn main() -> Result<(), Box<dyn std::error::Error>> {

  std::env::set_var("RUST_BACKTRACE", "full");

  // parse cli args
  let args = Args::parse();

  println!("\nRunning with args: {:#?}\n", args);

  let now = std::time::Instant::now();

  let pi_est = malachite_algo::estimate(args.iter as u64, args.pow as u64, args.prec as u64);  
  // let pi_est = num_algo::estimate(args.iter, args.pow, args.prec);

  // println!("\nEstimated Pi: {}", pi_est);
  println!("\nTime elapsed: {:.2?}\n", now.elapsed());

  Ok(())

}

