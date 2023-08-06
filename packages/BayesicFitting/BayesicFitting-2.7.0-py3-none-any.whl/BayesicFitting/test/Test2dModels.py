# run with : python3 -m unittest Test2dModels

import unittest
import os
import numpy as numpy
from astropy import units
import matplotlib.pyplot as plt
import warnings

from BayesicFitting import *

__author__ = "Do Kester"
__year__ = 2017
__license__ = "GPL3"
__version__ = "0.9"
__maintainer__ = "Do"
__status__ = "Development"

#  * This file is part of the BayesicFitting package.
#  *
#  * BayesicFitting is free software: you can redistribute it and/or modify
#  * it under the terms of the GNU Lesser General Public License as
#  * published by the Free Software Foundation, either version 3 of
#  * the License, or ( at your option ) any later version.
#  *
#  * BayesicFitting is distributed in the hope that it will be useful,
#  * but WITHOUT ANY WARRANTY; without even the implied warranty of
#  * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#  * GNU Lesser General Public License for more details.
#  *
#  * The GPL3 license can be found at <http://www.gnu.org/licenses/>.
#  *
#  *  2006 Do Kester

class Test2dModels( unittest.TestCase ):
    """
    Test harness for 2d-Models

    Author:      Do Kester

    """
    def __init__( self, testname ):
        super( ).__init__( testname )
        self.doplot = ( "DOPLOT" in os.environ and os.environ["DOPLOT"] == "1" )


    def testPolySurfaceModel( self ):
        x  = numpy.asarray( [[-1.0, -0.8], [-0.6, -0.4], [-0.2, 0.0], [0.2, 0.4], [0.6, 0.8],
                [1.0, -1.0], [-0.8, -0.6], [-0.4, -0.2], [0.0, 0.2], [0.4, 0.6], [0.8, 1.0]] )
        print( "******POLYSURFACE********************" )
        m = PolySurfaceModel( 2 )
        self.assertTrue( m.npchain == 6 )
        self.assertTrue( m.npbase == 6 )
        p = [-1.1, 0.5, 0.04, 1.2, -0.5, -0.03]
        self.stdModeltest( m, p, plot=self.doplot )

    def testKernel2dModel1( self ):
        x  = numpy.asarray( [[-1.0, -0.8], [-0.6, -0.4], [-0.2, 0.0], [0.2, 0.4], [0.6, 0.8],
                [1.0, -1.0], [-0.8, -0.6], [-0.4, -0.2], [0.0, 0.2], [0.4, 0.6], [0.8, 1.0]] )
        print( "******KERNEL2D CIRCULAR********************" )
        m = Kernel2dModel( )
        self.assertTrue( m.npchain == 4 )
        self.assertTrue( m.npbase == 4 )
        p = [-1.1, 0.5, 0.04, 1.2]
        self.stdModeltest( m, p, plot=self.doplot )

    def testKernel2dModel2( self ):
        x  = numpy.asarray( [[-1.0, -0.8], [-0.6, -0.4], [-0.2, 0.0], [0.2, 0.4], [0.6, 0.8],
                [1.0, -1.0], [-0.8, -0.6], [-0.4, -0.2], [0.0, 0.2], [0.4, 0.6], [0.8, 1.0]] )
        print( "******KERNEL2D ELLIPTIC********************" )
        m = Kernel2dModel( shape=2 )
        self.assertTrue( m.npchain == 5 )
        self.assertTrue( m.npbase == 5 )
        p = [-1.1, 0.5, 0.04, 1.2, 1.4]
        self.stdModeltest( m, p, plot=self.doplot )

    def testKernel2dModel3( self ):
        x  = numpy.asarray( [[-1.0, -0.8], [-0.6, -0.4], [-0.2, 0.0], [0.2, 0.4], [0.6, 0.8],
                [1.0, -1.0], [-0.8, -0.6], [-0.4, -0.2], [0.0, 0.2], [0.4, 0.6], [0.8, 1.0]] )
        print( "******KERNEL2D ROTATED********************" )
        m = Kernel2dModel( shape=3 )
        self.assertTrue( m.npchain == 6 )
        self.assertTrue( m.npbase == 6 )
        p = [-1.1, 0.5, 0.04, 1.2, 1.3, 1.1]
        self.stdModeltest( m, p, plot=self.doplot )

    def testProductModel( self ):
        rng = numpy.random.RandomState( 1234 )
        x = rng.rand( 100, 2 )
        x[:,0] *= 3
        x[:,1] *= 2

        xy  = numpy.asarray( [[-1.0, -0.8], [-0.6, -0.4], [-0.2, 0.0], [0.2, 0.4], [0.6, 0.8],
                [1.0, -1.0], [-0.8, -0.6], [-0.4, -0.2], [0.0, 0.2], [0.4, 0.6], [0.8, 1.0]] )
        print( "******2D PRODUCT*****************" )
        gm = GaussModel()
        pm = PolynomialModel( 2 )
        m = ProductModel( [gm,pm] )
        # print( m.models )
        print( m )
        print( m.npchain )

        self.assertTrue( m.npchain == 6 )
        self.assertTrue( m.npbase == 6 )
        p = [1.1, 0.5, 1.4, 1.2, -0.5, -0.03]
        self.stdModeltest( m, p, xdata=x, plot=self.doplot )

    def testSurfaceSplinesModel( self ):
        rng = numpy.random.RandomState( 1234 )
        x = rng.rand( 100, 2 )
        x[:,0] *= 3
        x[:,1] *= 2

        xy  = numpy.asarray( [[-1.0, -0.8], [-0.6, -0.4], [-0.2, 0.0], [0.2, 0.4], [0.6, 0.8],
                [1.0, -1.0], [-0.8, -0.6], [-0.4, -0.2], [0.0, 0.2], [0.4, 0.6], [0.8, 1.0]] )
        print( "******SURFACESPLINES*****************" )
        xk = numpy.arange( 4, dtype=float )
        yk = numpy.arange( 3, dtype=float )
        m = SurfaceSplinesModel( [xk,yk] )
        print( m.knots )
        print( m.order )
        print( m.models )

        self.assertTrue( m.npchain == 30 )
        self.assertTrue( m.npbase == 30 )
        p = [-1.1, 0.5, 0.04, 1.2, -0.5, -0.03, -1.1, 0.5, 0.04, 1.2, -0.5, -0.03,
             -1.1, 0.5, 0.04, 1.2, -0.5, -0.03, -1.1, 0.5, 0.04, 1.2, -0.5, -0.03,
             -1.1, 0.5, 0.04, 1.2, -0.5, -0.03]
        self.stdModeltest( m, p, xdata=x, plot=self.doplot )

    def testSurfaceSplinesModel2( self ):
        rng = numpy.random.RandomState( 1234 )
        x = rng.rand( 100, 2 )
        x[:,0] *= 3
        x[:,1] *= 2

        xy  = numpy.asarray( [[-1.0, -0.8], [-0.6, -0.4], [-0.2, 0.0], [0.2, 0.4], [0.6, 0.8],
                [1.0, -1.0], [-0.8, -0.6], [-0.4, -0.2], [0.0, 0.2], [0.4, 0.6], [0.8, 1.0]] )
        print( "******SURFACESPLINES 2***************" )
        xk = numpy.arange( 4, dtype=float )
        yk = numpy.arange( 3, dtype=float )
        m = SurfaceSplinesModel( [xk,yk], order=[3,0] )
        print( m )
        print( "knots at ", m.knots[0], m.knots[1] )
        print( "orders   ", m.order )

        self.assertTrue( m.npchain == 12 )
        self.assertTrue( m.npbase == 12 )
        p = [-1.1, 0.5, 0.04, 1.2, -0.5, -0.03, -1.1, 0.5, 0.04, 1.2, -0.5, -0.03]

        self.stdModeltest( m, p, xdata=x, plot=self.doplot )



    def stdModeltest( self, model, par, xdata=None, plot=None, warn=[] ):
        print( "***StdModelTest***************" )
        if xdata is None :
            x  = numpy.asarray( [[-1.0, -0.8], [-0.6, -0.4], [-0.2, 0.0], [0.2, 0.4], [0.6, 0.8],
                    [1.0, -1.0], [-0.8, -0.6], [-0.4, -0.2], [0.0, 0.2], [0.4, 0.6], [0.8, 1.0]] )
        else :
            x = xdata

        print( model )
        if "nopart" in warn :
            self.assertWarns( UserWarning, model.basePartial, x, par )
            print( model.shortName() + ": Further no-partial warnings ignored." )
            warnings.simplefilter( "ignore" )

        numpy.set_printoptions( precision=3, suppress=True )
        print( model.partial( x, par ) )
        print( x[5,:] )
        self.assertTrue( model.testPartial( [x[5,:]], model.parameters ) == 0 )

        self.assertTrue( model.testPartial( [x[0,:]], par ) == 0 )
        model.xUnit = [units.m, units.s]
        model.yUnit = units.kg
        for k in range( model.getNumberOfParameters() ):
            print( "%d  %-12s  %-12s"%(k, model.getParameterName( k ), model.getParameterUnit( k ) ) )

        print( "Integral   ", model.getIntegralUnit( ) )
        self.assertTrue( model.testPartial( x, par ) == 0 )

        part = model.partial( x, par )
        nump = model.numPartial( x, par )
        k = 0
        for (pp,nn) in zip( part.flatten(), nump.flatten() ) :
            self.assertAlmostEqual( pp, nn, 3 )
            k += 1

        mc = model.copy( )
        Tools.printclass( model )
        Tools.printclass( mc )

        for k in range( min( mc.npchain, 10 ) ):
            print( "%d  %-12s  %-12s"%(k, mc.getParameterName( k ), mc.getParameterUnit( k ) ) )
        mc.parameters = par
        model.parameters = par

        for (k,xk,r1,r2) in zip( range( 11 ), x, model.result( x ), mc.result( x ) ) :
            print( "%3d %8.3f,%8.3f  %10.3f %10.3f" % ( k, xk[0], xk[1], r1, r2 ) )
            self.assertEqual( r1, r2 )
        self.assertTrue( mc.testPartial( x, par ) == 0 )

#        if plot :
#            self.plotModel( model, par )

    def TBDplotModel( self, model, par ) :
        xx = numpy.linspace( -1, +1, 1001 )
        plt.plot( xx, model.result( xx, par ), '-', linewidth=2 )
        x2 = numpy.linspace( -1, +1, 11 )
        dy = model.derivative( x2, par )
        yy = model.result( x2, par )
        for k in range( 11 ) :
            x3 = numpy.asarray( [-0.05, +0.05] )
            y3 = x3 * dy[k] + yy[k]
            plt.plot( x2[k] + x3, y3, 'r-' )

        plt.show()


    @classmethod
    def suite( cls ):
        return unittest.TestCase.suite( TestModels.__class__ )

if __name__ == '__main__':
    unittest.main( )


