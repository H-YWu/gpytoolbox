from .context import gpytoolbox as gpy
from .context import numpy as np
from .context import unittest

class TestBiharmonicEnergyIntrinsic(unittest.TestCase):

    def test_uniform_triangle(self):
        c = np.random.default_rng().random() + 0.1

        l_sq = c * np.array([[1., 1., 1.]])
        f = np.array([[0,1,2]],dtype=int)

        Q = gpy.biharmonic_energy_intrinsic(l_sq, f, bc='mixedfem_zero_neumann')
        Q_gt = np.sqrt(3)/c * np.array([[2., -1., -1.],
            [-1., 2., -1.],
            [-1., -1., 2.]])
        self.assertTrue(np.isclose(Q.toarray(), Q_gt).all())

        Q = gpy.biharmonic_energy_intrinsic(l_sq, f, bc='curved_hessian')
        Q_gt = np.zeros((3,3))
        self.assertTrue(np.isclose(Q.toarray(), Q_gt).all())


    def test_regression(self):
        V,F = gpy.read_mesh("test/unit_tests_data/cube.obj")
        l_sq = gpy.halfedge_lengths_squared(V,F)

        Qmzn = gpy.biharmonic_energy_intrinsic(l_sq, F, bc='mixedfem_zero_neumann')
        Qmzn_gt = np.array([[16.                , -8.                , -8.                ,
         2.6666666666666665,  2.6666666666666665,  0.                ,
        -8.                ,  2.6666666666666665],
       [-8.                , 16.                ,  2.6666666666666665,
        -8.                ,  0.                ,  2.666666666666667 ,
         2.6666666666666665, -8.                ],
       [-8.                ,  2.6666666666666665, 16.                ,
        -8.                , -8.                ,  2.666666666666667 ,
         2.6666666666666665,  0.                ],
       [ 2.6666666666666665, -8.                , -8.                ,
        16.                ,  2.666666666666667 , -8.                ,
         0.                ,  2.666666666666667 ],
       [ 2.6666666666666665,  0.                , -8.                ,
         2.666666666666667 , 16.                , -8.                ,
        -8.                ,  2.666666666666667 ],
       [ 0.                ,  2.666666666666667 ,  2.666666666666667 ,
        -8.                , -8.                , 16.                ,
         2.666666666666667 , -8.                ],
       [-8.                ,  2.6666666666666665,  2.6666666666666665,
         0.                , -8.                ,  2.666666666666667 ,
        16.                , -8.                ],
       [ 2.6666666666666665, -8.                ,  0.                ,
         2.666666666666667 ,  2.666666666666667 , -8.                ,
        -8.                , 16.                ]])
        self.assertTrue(np.isclose(Qmzn.toarray(), Qmzn_gt).all())

        Qch = gpy.biharmonic_energy_intrinsic(l_sq, F, bc='curved_hessian')
        Qch_gt = np.array([[ 22.37758040957278  , -10.403392041388944 , -10.403392041388944 ,
          1.9999999999999982,   3.0471975511965974,   0.7382006122008503,
        -10.403392041388942 ,   3.0471975511965974],
       [-10.403392041388942 ,  21.853981633974485 ,   3.5707963267948966,
        -10.403392041388942 ,   0.73820061220085  ,   2.523598775598298 ,
          2.523598775598298 , -10.403392041388946 ],
       [-10.403392041388944 ,   3.5707963267948966,  21.853981633974488 ,
        -10.403392041388944 , -10.403392041388946 ,   2.5235987755982974,
          2.5235987755982974,   0.73820061220085  ],
       [  1.9999999999999982, -10.40339204138894  , -10.40339204138894  ,
         22.37758040957278  ,   3.047197551196597 , -10.403392041388942 ,
          0.7382006122008503,   3.047197551196597 ],
       [  3.0471975511965974,   0.7382006122008502, -10.403392041388944 ,
          3.0471975511965974,  22.37758040957278  , -10.403392041388944 ,
        -10.403392041388944 ,   1.9999999999999978],
       [  0.7382006122008499,   2.5235987755982974,   2.5235987755982974,
        -10.403392041388942 , -10.403392041388942 ,  21.85398163397448  ,
          3.5707963267948952, -10.403392041388942 ],
       [-10.403392041388942 ,   2.5235987755982974,   2.5235987755982974,
          0.7382006122008499, -10.40339204138894  ,   3.5707963267948952,
         21.85398163397448  , -10.40339204138894  ],
       [  3.047197551196597 , -10.403392041388944 ,   0.7382006122008502,
          3.047197551196597 ,   1.9999999999999976, -10.40339204138894  ,
        -10.40339204138894  ,  22.37758040957278  ]])
        self.assertTrue(np.isclose(Qch.toarray(), Qch_gt).all())

if __name__ == '__main__':
    unittest.main()
