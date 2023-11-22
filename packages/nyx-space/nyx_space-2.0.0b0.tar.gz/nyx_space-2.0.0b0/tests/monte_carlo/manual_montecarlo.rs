extern crate nyx_space as nyx;
extern crate rand;
extern crate rand_distr;
extern crate rayon;

use nyx::cosmic::{Bodies, Cosm, Orbit};
use nyx::dynamics::Harmonics;
use nyx::dynamics::{OrbitalDynamics, PointMasses};
use nyx::io::gravity::*;
use nyx::propagators::*;
use nyx::time::{Epoch, Unit};
use nyx::State;
use rand::thread_rng;
use rand_distr::{Distribution, Normal};
use rayon::prelude::*;
use std::sync::Arc;
use std::time::Instant as StdInstant;

#[allow(clippy::identity_op)]
#[test]
fn multi_thread_monte_carlo_demo() {
    /*
    In this demo, we'll be running a 100 runs with the same dynamics and end state, but with a slightly variation in eccentricity.
    */
    extern crate pretty_env_logger;
    let _ = pretty_env_logger::try_init();

    let cosm = Cosm::de438();
    let eme2k = cosm.frame("EME2000");
    let iau_earth = cosm.frame("IAU Earth");

    let earth_sph_harm = HarmonicsMem::from_cof("data/JGM3.cof.gz", 70, 70, true).unwrap();
    let harmonics = Harmonics::from_stor(iau_earth, earth_sph_harm, cosm.clone());

    let dt = Epoch::from_gregorian_utc_at_midnight(2021, 1, 31);
    let state = Orbit::keplerian(8_191.93, 1e-6, 12.85, 306.614, 314.19, 99.887_7, dt, eme2k);

    let orbital_dyn = OrbitalDynamics::new(vec![
        PointMasses::new(
            &[Bodies::Sun, Bodies::Luna, Bodies::JupiterBarycenter],
            cosm,
        ),
        harmonics,
    ]);

    // We need to wrap the propagator setup in an Arc to enable multithreading.
    let setup = Arc::new(Propagator::default_dp78(orbital_dyn));

    // Around 1 km of error
    let sma_dist = Normal::new(0.0, 1.0).unwrap();

    // Generate all 100 initial states
    let init_states: Vec<Orbit> = sma_dist
        .sample_iter(&mut thread_rng())
        .take(100)
        .map(|delta_sma| state.with_sma(state.sma_km() + delta_sma))
        .collect();

    let prop_time = 1 * Unit::Day;
    let start = StdInstant::now();
    let end_epoch = dt + prop_time;
    init_states.par_iter().for_each_with(setup, |setup, state| {
        let final_state = setup.with(*state).for_duration(prop_time).unwrap();
        assert_eq!(end_epoch, final_state.epoch());
    });

    let clock_time = StdInstant::now() - start;
    println!(
        "Propagated {} states in {} seconds",
        init_states.len(),
        clock_time.as_secs_f64()
    );
}
