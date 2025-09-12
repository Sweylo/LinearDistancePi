use clap::Parser;

pub mod malachite_algo;
pub mod num_algo;


#[derive(Parser, Debug)]
#[command(name = "LinearDistancePi")]
#[command(about = "Calculates Pi using linear distance (pythagorean)", long_about = None)]
pub struct Args {

  /// Number of iterations to run
	#[arg(short, long, default_value_t = 10)]
  pub iter: usize,

	/// Power of two used to get portion of the unit circle (2^n)
	#[arg(short, long, default_value_t = 4)]
  pub pow: i32,

  /// Precision (decimal places) to use
	#[arg(short, long, default_value_t = 32)]
  pub prec: usize,

  /// Enable silent mode
  #[arg(short, long)]
  pub silent: bool,

}