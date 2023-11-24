import numpy as np
from .calc import CalcV, CalcD
from tqdm import tqdm
import dill


class Solver:

    def __init__(self, l=None, x=None, t=None, rho0=None, c=None, boundary=None, diff=False, potential=None):
        '''
        constructor of the class
        Parameters
        ----------
        l : list or numpy array
        x : list or numpy array
        t : list or numpy array
        rho0 : function or tuple of functions
        c : float or tuple of floats
        boundary : None or tuple
        diff : bool
        '''
        self.l, self.x, self.t = self.correct_l_x_t(l, x, t)
        self.c, self.rho0 = self.to_tuple(c, rho0)
        self.boundary = self.correct_boundary(boundary)
        self.potential = self.get_potential(potential)
        self.int_x, self.int_t, self.int_l, self.steps_number = self.get_ints()
        self.diff = diff
        self.convergence = []
        self.grid = self.create_initial_grid()

    def correct_l_x_t(self, l, x, t):
        '''
        checking correctnes of the input and changes list into the numpy arrays
        Parameters
        ----------
        l : list or numpy array
        x : list or numpy array
        t : list or numpy array

        Returns
        -------
        l, x, t as numpy arrays
        '''
        if isinstance(x, np.ndarray) == False:
            x = np.array(x)

        if isinstance(t, np.ndarray) == False:
            t = np.array(t)

        if isinstance(l, np.ndarray) == False:
            l = np.array(l)

        if t.size < 2:
            raise ValueError('t grid size cannot be smaller than 2')

        if l.ndim != 1 or x.ndim != 1 or t.ndim != 1:
            raise ValueError('x, l and t should be 1D arrays')

        return l, x, t

    def correct_boundary(self, boundary):
        '''
        checks if boundary is inputted correctly
        Parameters
        ----------
        boundary : None or tuple

        Returns
        -------
        Raises error or unchanged boundary
        '''
        if boundary is None:
            return None

        if isinstance(boundary, tuple) == False or len(boundary) != 2:
            raise TypeError('boundary argument should be a tuple of lenght 2')

        return boundary

    def get_potential(self, potential):

        if potential is not None:
            potential = potential(self.x)[np.newaxis, np.newaxis, :]

        return potential

    def to_tuple(self, c, rho0):
        '''
        ensures that c and rho0 are tuple and have this same size
        Parameters
        ----------
        c
        rho0

        Returns
        -------
        c and rho0 as tuple
        '''
        if isinstance(c, tuple) == False:
            c = (c,)

        if isinstance(rho0, tuple) == False:
            rho0 = (rho0,)

        if len(c) != len(rho0):
            raise TypeError('c and rho0 have to have this same size')

        return c, rho0

    def get_ints(self):
        '''
        extracts required data from x,t grids
        Returns
        -------
        int_x, int_l, int_t : floats representing spacing in dimensions
        steps_number : int, number of time iterations
        '''
        int_x = np.diff(self.x).mean()

        int_t = np.diff(self.t).mean()

        int_l = np.diff(self.l).mean()

        steps_number = self.t.size

        return int_x, int_t, int_l, steps_number

    # creates grid filled with initial condition
    def create_initial_grid(self):
        '''
        Returns
        -------
        numpy array which is solution grid filled only with initial state
        '''
        # dimensions: N, l, x, t

        grid = np.zeros((len(self.c), self.l.size, self.x.size, self.t.size))

        N_dim = []

        for item in self.rho0:
            N = item(self.l[:, np.newaxis], self.x[np.newaxis, :])

            N_dim.append(N)

        initial_state = np.stack(N_dim)

        grid[Ellipsis, 0] = initial_state

        return grid

    def create_matrix(self, time):
        '''

        Parameters
        ----------
        time : int

        Returns
        -------
        numpy array which is a matrix required for implicit solving of GHD
        '''
        # dimensions N, l, x for rho and V

        rho = self.grid[Ellipsis, time]

        # calculating V using class CalcV

        V = CalcV(rho, self.l, self.c).V

        # changing indices back to proper order

        V = np.einsum('Nxl -> Nlx', V)

        h = self.int_t / (2 * self.int_x)

        V_V_h = h * V[Ellipsis, np.newaxis, :] * np.ones_like(V)[Ellipsis, np.newaxis]

        off_diagonal = np.zeros((V_V_h.shape[-1], V_V_h.shape[-1]))

        np.fill_diagonal(off_diagonal[:, 1:], 1)
        np.fill_diagonal(off_diagonal[1:, 0:], -1)

        off_diagonal = V_V_h * off_diagonal[np.newaxis, np.newaxis, Ellipsis]

        diagonal = np.zeros((V_V_h.shape[-1], V_V_h.shape[-1]))

        np.fill_diagonal(diagonal, 1)

        diagonal = np.ones_like(V_V_h) * diagonal[np.newaxis, np.newaxis, Ellipsis]

        matrix = diagonal + off_diagonal

        if self.boundary is None:

            matrix[Ellipsis, 0, -1] = -V_V_h[Ellipsis, 0, -1]

            matrix[Ellipsis, -1, 0] = V_V_h[Ellipsis, -1, 0]

        else:

            matrix[Ellipsis, 0, 0] = self.boundary[0]

            matrix[Ellipsis, 0, 1] = 0

            matrix[Ellipsis, -1, -1] = self.boundary[1]
            matrix[Ellipsis, -1, -2] = 0

        return matrix

    def x_der(self, arr):
        '''

        Parameters
        ----------
        arr : numpy array of the grid at given time

        Returns
        -------
        numpy array which is a derivative in x dimension of inputted arr
        '''
        der = 1 / (2 * self.int_x) * (np.roll(arr, -1, axis=-1) - np.roll(arr, 1, axis=-1))

        # der = np.gradient(arr, self.int_x, axis = -1)

        return der

    def lambda_der(self, arr):
        '''

        Parameters
        ----------
        arr : numpy array of the grid at given time

        Returns
        -------
        numpy array which is a derivative in l dimension of inputted arr
        '''
        der = 1 / (2 * self.int_l) * (np.roll(arr, -1, axis=-2) - np.roll(arr, 1, axis=-2))

        return der

    def diff_fixed_point_func(self, rho, rho_next, D, V):
        '''
        functions utilizing fixed point iteration method for solving GHD with diffusion
        Parameters
        ----------
        rho : numpy array, state for which it is calculated
        rho_next
        D : numpy  array diffusion operator
        V : numpy array, effective velocity

        Returns
        -------

        '''
        diff = rho_next

        # D, V dimensions N, x, momenta

        D_op = np.einsum('Nxos, Nsx -> Nox', D, self.x_der(rho_next), optimize=True)

        V_rho = np.einsum('Nxl, Nlx -> Nlx', V, rho_next, optimize=True)

        if self.potential is None:

            foo = rho + self.int_t * (self.x_der(D_op) / 2 - self.x_der(V_rho))

        else:

            foo = rho + self.int_t * (
                    self.x_der(D_op) / 2 - self.x_der(V_rho) + self.x_der(self.potential) * self.lambda_der(rho))

        diff = np.abs(diff - foo).mean()

        return foo, diff

    def diff_equ(self, time):
        '''
        solves GHD at given time with diffusion using fixed point iteration method
        Parameters
        ----------
        time : int

        Returns
        -------
        rho_next: numpy array, state at another time
        diff : list, collects convergence of the method
        '''
        rho_next = self.grid[Ellipsis, time]

        rho = self.grid[Ellipsis, time]

        Diff = CalcD(rho, self.l, self.c)

        D, V = Diff.D, Diff.V  # dimensions N, x, momenta

        diff = []

        for i in range(15):
            rho_next, difference = self.diff_fixed_point_func(rho, rho_next, D, V)

            diff.append(difference)

        return rho_next, diff

    def solve_equation(self, path=None):
        '''
        Function solving GHD or GHD with diffusion using previous methods
        Parameters
        ----------
        path : optional string, if is not None, Solver objects is saved to localization

        Returns

        numpy array which is solution to GHD equations
        -------

        '''
        if self.diff is False:

            for time in tqdm(range(self.t.size - 1)):
                matrix = self.create_matrix(time)

                self.grid[Ellipsis, time + 1] = np.linalg.solve(matrix, self.grid[Ellipsis, time])

        else:

            for time in tqdm(range(self.t.size - 1)):
                rho_next, diff = self.diff_equ(time)

                self.grid[Ellipsis, time + 1] = rho_next

                self.convergence.append(diff)

        if path is not None:
            with open(path, 'wb') as file:
                dill.dump(self, file)

    def save_array(self, path):
        '''
        Saves array of the solutin
        Parameters
        ----------
        path : string, location to which array is saved

        '''
        with open(path, 'wb') as file:
            dill.dump(self.grid, file)

    def save(self, path):
        '''
        Saves Solver object as binary dill file to path localization
        Parameters
        ----------
        path : string, location to which object is saved
        '''
        with open(path, 'wb') as file:
            dill.dump(self, file)

            # loading arrays

    @staticmethod
    def load(path):
        '''
        Loads array or Solver object from the binary file
        Parameters
        ----------
        path : string, localizaction of binary file

        Returns
        -------
        Solver object from the path localization
        '''
        with open(path, 'rb') as file:
            arr = dill.load(file)

        return arr
