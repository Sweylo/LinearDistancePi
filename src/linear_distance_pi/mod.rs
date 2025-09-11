use clap::Parser;


#[derive(Parser, Debug)]
#[command(name = "LinearDistancePi")]
#[command(about = "Calculates Pi using linear distance (pythagorean)", long_about = None)]
pub struct Args {

  /// Number of iterations to run
	#[arg(short, long, default_value_t = 10)]
  pub iter: u64,

	/// Power of two used to get portion of the unit circle (2^n)
	#[arg(short, long, default_value_t = 4)]
  pub pow: u64,

  /// Precision (decimal places) to use
	#[arg(short, long, default_value_t = 32)]
  pub prec: u64,

  /// Enable silent mode
  #[arg(short, long)]
  pub silent: bool,

}