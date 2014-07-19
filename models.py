# -*- coding: utf8 -*-
# - GUI program for fast processing of 2D X-ray data
# Copyright (C) 2014  Clemens Prescher (clemens.prescher@gmail.com)
# GSECARS, University of Chicago
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
#
#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
#
#     You should have received a copy of the GNU General Public License
#     along with this program.  If not, see <http://www.gnu.org/licenses/>.
__author__ = 'Clemens Prescher'
from measurement import collect_single_data, collect_step_data, collect_wide_data


class MainData(object):
    def __init__(self):
        self.experiment_setups = []
        self.sample_points = []

    def add_experiment_setup(self, name, detector_pos_x=0, detector_pos_y=49, omega_start=0, omega_end=0, omega_step=0,
                             time_per_step=0):
        self.experiment_setups.append(
            ExperimentSetup(name, detector_pos_x, detector_pos_y, omega_start, omega_end, omega_step, time_per_step))

        for point in self.sample_points:
            point.register_setup(self.experiment_setups[-1])

    def delete_experiment_setup(self, ind):
        for point in self.sample_points:
            point.unregister_setup(self.experiment_setups[ind])
        del self.experiment_setups[ind]

    def clear_experiment_setups(self):
        for ind, setup in enumerate(self.experiment_setups):
            self.delete_experiment_setup(ind)

    def get_experiment_state(self):
        data = []
        for point in self.sample_points:
            point_data = []
            for ind, experiment in enumerate(self.experiment_setups):
                point_data.append([point.perform_step_scan_for_setup[ind],
                                   point.perform_wide_scan_for_setup[ind]])
            data.append(point_data)
        return data

    def add_sample_point(self, name, x, y, z):
        self.sample_points.append(SamplePoint(name, x, y, z))
        for setup in self.experiment_setups:
            self.sample_points[-1].register_setup(setup)

    def delete_sample_point(self, ind):
        del self.sample_points[ind]

    def clear_sample_points(self):
        self.sample_points = []

    def get_experiment_setup_names(self):
        res = []
        for experiment_setup in self.experiment_setups:
            res.append(experiment_setup.name)
        return res

    def setup_name_existent(self, name):
        for setup in self.experiment_setups:
            if name == setup.name:
                return True
        return False

    def sample_name_existent(self, name):
        for setup in self.sample_points:
            if name == setup.name:
                return True
        return False


class ExperimentSetup(object):
    def __init__(self, name, detector_pos_x=0, detector_pos_z=49, omega_start=0, omega_end=0, omega_step=0,
                 time_per_step=0):
        self.name = name
        self.detector_pos_x = detector_pos_x
        self.detector_pos_z = detector_pos_z
        self.omega_start = omega_start
        self.omega_end = omega_end
        self.omega_step = omega_step
        self.time_per_step = time_per_step

    def get_total_exposure_time(self):
        return (self.omega_end - self.omega_start) / self.omega_step * self.time_per_step

    def get_step_exposure_time(self, total_time):
        return total_time * self.omega_step / (self.omega_end - self.omega_start)

    def __str__(self):
        return "{}: {}, {}, {}, {}, {}, {}".format(self.name, self.detector_pos_x, self.detector_pos_z,
                                                   self.omega_start, self.omega_end, self.omega_step,
                                                   self.time_per_step)


class SamplePoint(object):
    def __init__(self, name='P', x=0, y=0, z=0):
        self.name = name
        self.x = x
        self.y = y
        self.z = z

        self.experiment_setups = []
        self.perform_wide_scan_for_setup = []
        self.perform_step_scan_for_setup = []

    def set_position(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def set_perform_wide_scan_setup(self, exp_ind, state):
        self.perform_wide_scan_for_setup[exp_ind] = state

    def set_perform_step_scan_setup(self, exp_ind, state):
        self.perform_step_scan_for_setup[exp_ind] = state

    def register_setup(self, experiment_setup):
        self.experiment_setups.append(experiment_setup)
        self.perform_step_scan_for_setup.append(False)
        self.perform_wide_scan_for_setup.append(False)

    def unregister_setup(self, experiment_setup):
        ind = self.experiment_setups.index(experiment_setup)
        del self.experiment_setups[ind]
        del self.perform_step_scan_for_setup[ind]
        del self.perform_wide_scan_for_setup[ind]

    def __str__(self):
        return "{}, {}, {}, {}, {}, {}".format(self.name, self.x, self.y, self.z,
                                               self.perform_step_scan_for_setup,
                                               self.perform_wide_scan_for_setup)

