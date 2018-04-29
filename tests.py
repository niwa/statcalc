#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

import kappa
import kappa_simple


class BaseTest(unittest.TestCase):

    def must_contain(self, text, token):
        self.assertTrue(token in text)

class KappaTests(BaseTest):

    def test_eval_01(self):
        # --npp 1.0 --npa 1.0 --nap 2.0 --naa 2.0 --kappatest 0.5
        output = kappa.calculate_kappa(1.0, 1.0, 2.0, 2.0, 0.5)
        self.must_contain(output, 'present   | 1         | 1')
        self.must_contain(output, 'absent    | 2         | 2')
        self.must_contain(output, '= 0.3849')
        self.must_contain(output, 'kappa= 0.5] = 0.9030')

    def test_eval_02(self):
        # --npp 100.0 --npa 100.0 --nap 1.0 --naa 1.0 --kappatest 0.5
        output = kappa.calculate_kappa(100.0, 100.0, 1.0, 1.0, 0.5)
        self.must_contain(output, 'present   | 100       | 100')
        self.must_contain(output, 'absent    | 1         | 1')
        self.must_contain(output, '= 0.0139')
        self.must_contain(output, 'kappa= 0.5] > 0.9999')

    def test_eval_03(self):
        # --npp 100.0 --npa 100.0 --nap 1.0 --naa 1.0 --kappatest 0
        output = kappa.calculate_kappa(100.0, 100.0, 1.0, 1.0, 0)
        self.must_contain(output, 'present   | 100       | 100')
        self.must_contain(output, 'absent    | 1         | 1')
        self.must_contain(output, '= 0.0139')
        self.must_contain(output, 'kappa=0] = 0.5000')
        self.must_contain(output, 'kappa= 0.0] > 0.9999')

    def test_kappa_less_than_zero(self):
        output = kappa.calculate_kappa(1.0, 1.0, 2.0, 2.0, -1)
        self.must_contain(output, 'Kappatest must be greater than or equal to zero and less than 1')

    def test_kappa_validate_input_01(self):
        output = kappa.calculate_kappa(1.0, 0.0, 0.0, 0.0, 0.5)
        self.must_contain(output, 'Perfect agreement (all rating pairs are "present")')

    def test_kappa_validate_input_02(self):
        output = kappa.calculate_kappa(0.0, 1.0, 0.0, 0.0, 0.5)
        self.must_contain(output, 'Perfect disagreement (all rating pairs are "present"/"absent")')

    def test_kappa_validate_input_03(self):
        output = kappa.calculate_kappa(0.0, 0.0, 1.0, 0.0, 0.5)
        self.must_contain(output, 'Perfect disagreement (all rating pairs are "present"/"absent")')

    def test_kappa_validate_input_04(self):
        output = kappa.calculate_kappa(0.0, 0.0, 0.0, 1.0, 0.5)
        self.must_contain(output, 'Perfect agreement (all rating pairs are "absent")')

    def test_kappa_validate_input_05(self):
        output = kappa.calculate_kappa(0.0, 1.0, 1.0, 0.0, 0.5)
        self.must_contain(output, 'Perfect disagreement (some rating pairs are "present/absent", all others are "absent/present")')

    def test_kappa_validate_input_06(self):
        output = kappa.calculate_kappa(1.0, 0.0, 1.0, 0.0, 0.5)
        self.must_contain(output, 'Rater B has marked all tests as "present"; rater A has "present" and "absent"')

    def test_kappa_validate_input_07(self):
        output = kappa.calculate_kappa(0.0, 1.0, 0.0, 1.0, 0.5)
        self.must_contain(output, 'Rater B has marked all tests as "absent"; rater A has "present" and "absent"')

    def test_kappa_validate_input_08(self):
        output = kappa.calculate_kappa(1.0, 1.0, 0.0, 0.0, 0.5)
        self.must_contain(output, 'Rater A has marked all tests as "present"; rater B has "present" and "absent"')

    def test_kappa_validate_input_09(self):
        output = kappa.calculate_kappa(0.0, 0.0, 1.0, 1.0, 0.5)
        self.must_contain(output, 'Rater A has marked all tests as "absent"; rater B has "present" and "absent"')

    def test_kappa_validate_input_10(self):
        output = kappa.calculate_kappa(1.0, 0.0, 0.0, 1.0, 0.5)
        self.must_contain(output, 'Perfect agreement (some rating pairs are "present", all others are "absent")')


class KappaSimpleTests(BaseTest):

    def test_eval_01(self):
        # --npp 1.0 --npa 1.0 --nap 2.0 --naa 2.0 --kappa_simpletest 0.5
        output = kappa_simple.calculate_kappa(1.0, 1.0, 2.0, 2.0, 0.5)
        self.must_contain(output, 'present   | 1         | 1')
        self.must_contain(output, 'absent    | 2         | 2')
        self.must_contain(output, '= 0.3849')
        self.must_contain(output, 'kappa= 0.5] = 0.9030')

    def test_eval_02(self):
        # --npp 0.0 --npa 0.1 --nap 1.0 --naa 0.0 --kappa_simpletest 0.5
        output = kappa_simple.calculate_kappa(0.0, 0.1, 1.0, 0.0, 0.5)
        self.must_contain(output, 'present   | 0         | 0')
        self.must_contain(output, 'absent    | 1         | 0')
        self.must_contain(output, 'estimated kappa = -0.198')
        self.must_contain(output, '= 0.6437')
        self.must_contain(output, 'kappa= 0.5] = 0.8608')

    def test_eval_03(self):
        # --npp 0.0 --npa 1.0 --nap 1.0 --naa 0.0 --kappa_simpletest 0.5
        with self.assertRaises(ZeroDivisionError) as context:
            kappa_simple.calculate_kappa(0.0, 1.0, 1.0, 0.0, 0.5)

    def test_kappa_less_than_zero(self):
        output = kappa_simple.calculate_kappa(1.0, 1.0, 2.0, 2.0, -1)
        self.must_contain(output, 'Kappatest must be greater than or equal to zero and less than 1')

    def test_kappa_validate_input_01(self):
        output = kappa_simple.calculate_kappa(1.0, 0.0, 0.0, 0.0, 0.5)
        self.must_contain(output, 'Perfect agreement (all rating pairs are "present")')

    def test_kappa_validate_input_02(self):
        output = kappa_simple.calculate_kappa(0.0, 1.0, 0.0, 0.0, 0.5)
        self.must_contain(output, 'Perfect disagreement (all rating pairs are "present"/"absent")')

    def test_kappa_validate_input_03(self):
        output = kappa_simple.calculate_kappa(0.0, 0.0, 1.0, 0.0, 0.5)
        self.must_contain(output, 'Perfect disagreement (all rating pairs are "present"/"absent")')

    def test_kappa_validate_input_04(self):
        output = kappa_simple.calculate_kappa(0.0, 0.0, 0.0, 1.0, 0.5)
        self.must_contain(output, 'Perfect agreement (all rating pairs are "absent")')

    def test_kappa_validate_input_05(self):
        output = kappa_simple.calculate_kappa(1.0, 0.0, 1.0, 0.0, 0.5)
        self.must_contain(output, 'Rater B has marked all tests as "present"; rater A has "present" and "absent"')

    def test_kappa_validate_input_06(self):
        output = kappa_simple.calculate_kappa(0.0, 1.0, 0.0, 1.0, 0.5)
        self.must_contain(output, 'Rater B has marked all tests as "absent"; rater A has "present" and "absent"')

    def test_kappa_validate_input_07(self):
        output = kappa_simple.calculate_kappa(1.0, 1.0, 0.0, 0.0, 0.5)
        self.must_contain(output, 'Rater A has marked all tests as "present"; rater B has "present" and "absent"')

    def test_kappa_validate_input_08(self):
        output = kappa_simple.calculate_kappa(0.0, 0.0, 1.0, 1.0, 0.5)
        self.must_contain(output, 'Rater A has marked all tests as "absent"; rater B has "present" and "absent"')

    def test_kappa_validate_input_09(self):
        output = kappa_simple.calculate_kappa(1.0, 0.0, 0.0, 1.0, 0.5)
        self.must_contain(output, 'Perfect agreement (some rating pairs are "present", all others are "absent")')


if __name__ == '__main__':
    unittest.main()