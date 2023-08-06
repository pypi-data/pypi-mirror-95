# MIT License
#
# Copyright (c) 2020 University of Oxford
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
"""
Test cases for the python API for tsdate.
"""
import json
import unittest

import attr
import msprime
import numpy as np
import pytest
import tsinfer
import utility_functions

import tsdate
from tsdate.base import LIN
from tsdate.base import LOG


class TestPrebuilt(unittest.TestCase):
    """
    Tests for tsdate on prebuilt tree sequences
    """

    def test_dangling_failure(self):
        ts = utility_functions.single_tree_ts_n2_dangling()
        with pytest.raises(ValueError, match="dangling"):
            tsdate.date(ts, Ne=1)

    def test_unary_warning(self):
        with self.assertLogs(level="WARNING") as log:
            tsdate.date(utility_functions.single_tree_ts_with_unary(), Ne=1)
            assert len(log.output) == 1
            assert "unary nodes" in log.output[0]

    def test_fails_with_recombination(self):
        ts = utility_functions.two_tree_mutation_ts()
        for probability_space in (LOG, LIN):
            with pytest.raises(NotImplementedError):
                tsdate.date(
                    ts,
                    Ne=1,
                    recombination_rate=1,
                    probability_space=probability_space,
                )
            with pytest.raises(NotImplementedError):
                tsdate.date(
                    ts,
                    Ne=1,
                    recombination_rate=1,
                    probability_space=probability_space,
                    mutation_rate=1,
                )

    def test_intervals(self):
        ts = utility_functions.two_tree_ts()
        long_ts = utility_functions.two_tree_ts_extra_length()
        keep_ts = long_ts.keep_intervals([[0.0, 1.0]])
        delete_ts = long_ts.delete_intervals([[1.0, 1.5]])
        dated_ts = tsdate.date(ts, Ne=1)
        dated_keep_ts = tsdate.date(keep_ts, Ne=1)
        dated_deleted_ts = tsdate.date(delete_ts, Ne=1)
        assert np.allclose(
            dated_ts.tables.nodes.time[:], dated_keep_ts.tables.nodes.time[:]
        )
        assert np.allclose(
            dated_ts.tables.nodes.time[:], dated_deleted_ts.tables.nodes.time[:]
        )


class TestSimulated:
    """
    Tests for tsdate on simulated tree sequences.
    """

    def ts_equal_except_times(self, ts1, ts2):
        assert ts1.sequence_length == ts2.sequence_length
        t1 = ts1.tables
        t2 = ts2.tables
        assert t1.sites == t2.sites
        # Edges may have been re-ordered, since sortedness requirements specify
        # they are sorted by parent time, and the relative order of
        # (unconnected) parent nodes might have changed due to time inference
        assert set(t1.edges) == set(t2.edges)
        # The dated and undated tree sequences should not have the same node times
        assert not np.array_equal(ts1.tables.nodes.time, ts2.tables.nodes.time)
        # New tree sequence will have node times in metadata and all mutation times
        # set to tskit.UNKNOWN_TIME
        for column_name in t1.nodes.column_names:
            if column_name not in ["time", "metadata", "metadata_offset"]:
                col_t1 = getattr(t1.nodes, column_name)
                col_t2 = getattr(t2.nodes, column_name)
                assert np.array_equal(col_t1, col_t2)
        for column_name in t1.mutations.column_names:
            if column_name not in ["time"]:
                col_t1 = getattr(t1.mutations, column_name)
                col_t2 = getattr(t2.mutations, column_name)
                assert np.array_equal(col_t1, col_t2)
        # Assert that last provenance shows tree sequence was dated
        assert len(t1.provenances) == len(t2.provenances) - 1
        for index, (prov1, prov2) in enumerate(zip(t1.provenances, t2.provenances)):
            assert prov1 == prov2
            if index == len(t1.provenances) - 1:
                break
        assert json.loads(t2.provenances[-1].record)["software"]["name"] == "tsdate"

    def test_simple_sim_1_tree(self):
        ts = msprime.simulate(8, mutation_rate=5, random_seed=2)
        max_dated_ts = tsdate.date(ts, Ne=1, mutation_rate=5, method="maximization")
        self.ts_equal_except_times(ts, max_dated_ts)
        io_dated_ts = tsdate.date(ts, Ne=1, mutation_rate=5)
        self.ts_equal_except_times(ts, io_dated_ts)

    def test_simple_sim_multi_tree(self):
        ts = msprime.simulate(8, mutation_rate=5, recombination_rate=5, random_seed=2)
        assert ts.num_trees > 1
        max_dated_ts = tsdate.date(ts, Ne=1, mutation_rate=5, method="maximization")
        self.ts_equal_except_times(ts, max_dated_ts)
        io_dated_ts = tsdate.date(ts, Ne=1, mutation_rate=5)
        self.ts_equal_except_times(ts, io_dated_ts)

    def test_simple_sim_larger_example(self):
        # This makes ~1700 trees, and previously caused a failure
        ts = msprime.simulate(
            sample_size=10,
            length=2e6,
            Ne=10000,
            mutation_rate=1e-8,
            recombination_rate=1e-8,
            random_seed=11,
        )
        io_ts = tsdate.date(ts, Ne=10000, mutation_rate=1e-8)
        maximized_ts = tsdate.date(
            ts, Ne=10000, mutation_rate=1e-8, method="maximization"
        )
        self.ts_equal_except_times(ts, io_ts)
        self.ts_equal_except_times(ts, maximized_ts)

    def test_linear_space(self):
        # This makes ~1700 trees, and previously caused a failure
        ts = msprime.simulate(
            sample_size=10,
            length=2e6,
            Ne=10000,
            mutation_rate=1e-8,
            recombination_rate=1e-8,
            random_seed=11,
        )
        priors = tsdate.build_prior_grid(ts, timepoints=10, approximate_priors=None)
        dated_ts = tsdate.date(
            ts, Ne=10000, mutation_rate=1e-8, priors=priors, probability_space=LIN
        )
        maximized_ts = tsdate.date(
            ts,
            Ne=10000,
            mutation_rate=1e-8,
            priors=priors,
            method="maximization",
            probability_space=LIN,
        )
        self.ts_equal_except_times(ts, dated_ts)
        self.ts_equal_except_times(ts, maximized_ts)

    def test_with_unary(self):
        ts = msprime.simulate(
            8,
            mutation_rate=10,
            recombination_rate=10,
            record_full_arg=True,
            random_seed=12,
        )
        max_dated_ts = tsdate.date(ts, Ne=1, mutation_rate=10, method="maximization")
        self.ts_equal_except_times(ts, max_dated_ts)
        io_dated_ts = tsdate.date(ts, Ne=1, mutation_rate=10)
        self.ts_equal_except_times(ts, io_dated_ts)

    def test_fails_multi_root(self):
        ts = msprime.simulate(8, mutation_rate=2, random_seed=2)
        tree = ts.first()
        tables = ts.dump_tables()
        tables.edges.clear()
        internal_edge_removed = False
        for row in ts.tables.edges:
            if row.parent not in tree.roots and row.child not in ts.samples():
                if not internal_edge_removed:
                    continue
            tables.edges.add_row(**attr.asdict(row))
        multiroot_ts = tables.tree_sequence()
        good_priors = tsdate.build_prior_grid(ts)
        with pytest.raises(ValueError):
            tsdate.build_prior_grid(multiroot_ts)
        with pytest.raises(ValueError):
            tsdate.date(multiroot_ts, 1, 2)
        with pytest.raises(ValueError):
            tsdate.date(multiroot_ts, 1, 2, None, good_priors)

    def test_non_contemporaneous(self):
        samples = [
            msprime.Sample(population=0, time=0),
            msprime.Sample(population=0, time=0),
            msprime.Sample(population=0, time=0),
            msprime.Sample(population=0, time=1.0),
        ]
        ts = msprime.simulate(samples=samples, Ne=1, mutation_rate=2, random_seed=12)
        with pytest.raises(NotImplementedError):
            tsdate.date(ts, 1, 2)

    @pytest.mark.skip("Add when msprime 1.0 is released")
    def test_no_mutation_times(self):
        ts = msprime.simulate(20, Ne=1, mutation_rate=1, random_seed=12)
        assert np.all(ts.tables.mutations.time > 0)
        dated = tsdate.date(ts, 1, 1)
        assert np.all(np.isnan(dated.tables.mutations.time))

    @pytest.mark.skip("YAN to fix")
    def test_truncated_ts(self):
        Ne = 1e2
        mu = 2e-4
        ts = msprime.simulate(
            10,
            Ne=Ne,
            length=400,
            recombination_rate=1e-4,
            mutation_rate=mu,
            random_seed=12,
        )
        truncated_ts = utility_functions.truncate_ts_samples(
            ts, average_span=200, random_seed=123
        )
        dated_ts = tsdate.date(truncated_ts, Ne=Ne, mutation_rate=mu)
        # We should ideally test whether *haplotypes* are the same here
        # in case allele encoding has changed. But haplotypes() doesn't currently
        # deal with missing data
        self.ts_equal_except_times(truncated_ts, dated_ts)


class TestInferred:
    """
    Tests for tsdate on simulated then inferred tree sequences.
    """

    def test_simple_sim_1_tree(self):
        ts = msprime.simulate(8, mutation_rate=5, random_seed=2)
        for use_times in [True, False]:
            sample_data = tsinfer.SampleData.from_tree_sequence(
                ts, use_sites_time=use_times
            )
            inferred_ts = tsinfer.infer(sample_data)
            max_dated_ts = tsdate.date(
                inferred_ts, Ne=1, mutation_rate=5, method="maximization"
            )
            assert all(
                [a == b for a, b in zip(ts.haplotypes(), max_dated_ts.haplotypes())]
            )
            io_dated_ts = tsdate.date(inferred_ts, Ne=1, mutation_rate=5)
            assert all(
                [a == b for a, b in zip(ts.haplotypes(), io_dated_ts.haplotypes())]
            )

    def test_simple_sim_multi_tree(self):
        ts = msprime.simulate(8, mutation_rate=5, recombination_rate=5, random_seed=2)
        assert ts.num_trees > 1
        for use_times in [True, False]:
            sample_data = tsinfer.SampleData.from_tree_sequence(
                ts, use_sites_time=use_times
            )
            inferred_ts = tsinfer.infer(sample_data)
            max_dated_ts = tsdate.date(
                inferred_ts, Ne=1, mutation_rate=5, method="maximization"
            )
            assert all(
                [a == b for a, b in zip(ts.haplotypes(), max_dated_ts.haplotypes())]
            )
            io_dated_ts = tsdate.date(inferred_ts, Ne=1, mutation_rate=5)
            assert all(
                [a == b for a, b in zip(ts.haplotypes(), io_dated_ts.haplotypes())]
            )
