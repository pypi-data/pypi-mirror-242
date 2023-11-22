/*
    Nyx, blazing fast astrodynamics
    Copyright (C) 2023 Christopher Rabotin <christopher.rabotin@gmail.com>

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as published
    by the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
*/

pub use crate::dynamics::{Dynamics, NyxError};
pub use crate::{cosmic::Cosm, State, TimeTagged};
mod arc;
pub use arc::TrackingArcSim;
mod schedule;
pub use schedule::Schedule;
mod trackdata;
pub use trackdata::TrackingDeviceSim;
mod trkconfig;
pub use trkconfig::{EpochRanges, TrkConfig};
mod start_mode;
pub use start_mode::Availability;
