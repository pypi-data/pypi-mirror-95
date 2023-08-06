import abc
from collections import OrderedDict

import sympy as sp

from pystencils import Assignment, AssignmentCollection, Field


class AbstractConservedQuantityComputation(abc.ABC):
    r"""

    This class defines how conserved quantities are computed as functions of the pdfs.
    Conserved quantities are used for output and as input to the equilibrium in the collision step

    Depending on the method they might also be computed slightly different, e.g. due to a force model.

    An additional method describes how to get the conserved quantities for the equilibrium for initialization.
    In most cases the inputs can be used directly, but for some methods they have to be altered slightly.
    For example in zero centered hydrodynamic schemes with force model, the density has
    to be decreased by one, and the given velocity has to be shifted dependent on the force.

    .. image:: /img/moment_shift.svg

    """

    @property
    @abc.abstractmethod
    def conserved_quantities(self):
        """
        Dict, mapping names (symbol) to dimensionality (int)
        For example: {'density' : 1, 'velocity' : 3}
        The naming strings can be used in :func:`output_equations_from_pdfs`
        and :func:`equilibrium_input_equations_from_init_values`
        """

    def defined_symbols(self, order='all'):
        """
        Returns a dict, mapping names of conserved quantities to their symbols
        """

    @property
    @abc.abstractmethod
    def default_values(self):
        """
        Returns a dict of symbol to default value, where "default" means that
        the equilibrium simplifies to the weights if these values are inserted.
        Hydrodynamic example: rho=1, u_i = 0
        """

    @abc.abstractmethod
    def equilibrium_input_equations_from_pdfs(self, pdfs):
        """
        Returns an equation collection that defines all necessary quantities to compute the equilibrium as functions
        of the pdfs.
        For hydrodynamic LBM schemes this is usually the density and velocity.

        Args:
            pdfs: values or symbols for the pdf values
        """

    @abc.abstractmethod
    def output_equations_from_pdfs(self, pdfs, output_quantity_names_to_symbols):
        """
        Returns an equation collection that defines conserved quantities for output. These conserved quantities might
        be slightly different that the ones used as input for the equilibrium e.g. due to a force model.

        Args:
            pdfs: values for the pdf entries
            output_quantity_names_to_symbols: dict mapping of conserved quantity names
             (See :func:`conserved_quantities`) to symbols or field accesses where they should be written to
        """

    @abc.abstractmethod
    def equilibrium_input_equations_from_init_values(self, **kwargs):
        """
        Returns an equation collection that defines all necessary quantities to compute the equilibrium as function of
        given conserved quantities. Parameters can be names that are given by
        symbol names of :func:`conserved_quantities`.
        For all parameters not specified each implementation should use sensible defaults. For example hydrodynamic
        schemes use density=1 and velocity=0.
        """


class DensityVelocityComputation(AbstractConservedQuantityComputation):
    def __init__(self, stencil, compressible, force_model=None,
                 zeroth_order_moment_symbol=sp.Symbol("rho"),
                 first_order_moment_symbols=sp.symbols("u_:3")):
        dim = len(stencil[0])
        self._stencil = stencil
        self._compressible = compressible
        self._forceModel = force_model
        self._symbolOrder0 = zeroth_order_moment_symbol
        self._symbolsOrder1 = first_order_moment_symbols[:dim]

    @property
    def conserved_quantities(self):
        return {'density': 1,
                'velocity': len(self._stencil[0])}

    @property
    def compressible(self):
        return self._compressible

    def defined_symbols(self, order='all'):
        if order == 'all':
            return {'density': self._symbolOrder0,
                    'velocity': self._symbolsOrder1}
        elif order == 0:
            return 'density', self._symbolOrder0
        elif order == 1:
            return 'velocity', self._symbolsOrder1
        else:
            return None

    @property
    def zero_centered_pdfs(self):
        return not self._compressible

    @property
    def zeroth_order_moment_symbol(self):
        return self._symbolOrder0

    @property
    def first_order_moment_symbols(self):
        return self._symbolsOrder1

    @property
    def default_values(self):
        result = {self._symbolOrder0: 1}
        for s in self._symbolsOrder1:
            result[s] = 0
        return result

    def equilibrium_input_equations_from_pdfs(self, pdfs):
        dim = len(self._stencil[0])
        eq_coll = get_equations_for_zeroth_and_first_order_moment(self._stencil, pdfs, self._symbolOrder0,
                                                                  self._symbolsOrder1[:dim])
        if self._compressible:
            eq_coll = divide_first_order_moments_by_rho(eq_coll, dim)

        eq_coll = apply_force_model_shift('equilibrium_velocity_shift', dim, eq_coll,
                                          self._forceModel, self._compressible)
        return eq_coll

    def equilibrium_input_equations_from_init_values(self, density=1, velocity=(0, 0, 0)):
        dim = len(self._stencil[0])
        zeroth_order_moment = density
        first_order_moments = velocity[:dim]
        vel_offset = [0] * dim

        if self._compressible:
            if self._forceModel and hasattr(self._forceModel, 'macroscopic_velocity_shift'):
                vel_offset = self._forceModel.macroscopic_velocity_shift(zeroth_order_moment)
        else:
            if self._forceModel and hasattr(self._forceModel, 'macroscopic_velocity_shift'):
                vel_offset = self._forceModel.macroscopic_velocity_shift(sp.Rational(1, 1))
            zeroth_order_moment -= sp.Rational(1, 1)
        eqs = [Assignment(self._symbolOrder0, zeroth_order_moment)]

        first_order_moments = [a - b for a, b in zip(first_order_moments, vel_offset)]
        eqs += [Assignment(l, r) for l, r in zip(self._symbolsOrder1, first_order_moments)]

        return AssignmentCollection(eqs, [])

    def output_equations_from_pdfs(self, pdfs, output_quantity_names_to_symbols):
        dim = len(self._stencil[0])

        ac = get_equations_for_zeroth_and_first_order_moment(self._stencil, pdfs,
                                                             self._symbolOrder0, self._symbolsOrder1)

        if self._compressible:
            ac = divide_first_order_moments_by_rho(ac, dim)
        else:
            ac = add_density_offset(ac)

        ac = apply_force_model_shift('macroscopic_velocity_shift', dim, ac, self._forceModel, self._compressible)

        main_assignments = []
        eqs = OrderedDict([(eq.lhs, eq.rhs) for eq in ac.all_assignments])

        if 'density' in output_quantity_names_to_symbols:
            density_output_symbol = output_quantity_names_to_symbols['density']
            if isinstance(density_output_symbol, Field):
                density_output_symbol = density_output_symbol.center
            if density_output_symbol != self._symbolOrder0:
                main_assignments.append(Assignment(density_output_symbol, self._symbolOrder0))
            else:
                main_assignments.append(Assignment(self._symbolOrder0, eqs[self._symbolOrder0]))
                del eqs[self._symbolOrder0]
        if 'velocity' in output_quantity_names_to_symbols:
            vel_output_symbols = output_quantity_names_to_symbols['velocity']
            if isinstance(vel_output_symbols, Field):
                vel_output_symbols = vel_output_symbols.center_vector
            if tuple(vel_output_symbols) != tuple(self._symbolsOrder1):
                main_assignments += [Assignment(a, b) for a, b in zip(vel_output_symbols, self._symbolsOrder1)]
            else:
                for u_i in self._symbolsOrder1:
                    main_assignments.append(Assignment(u_i, eqs[u_i]))
                    del eqs[u_i]
        if 'momentum_density' in output_quantity_names_to_symbols:
            # get zeroth and first moments again - force-shift them if necessary
            # and add their values directly to the main equations assuming that subexpressions are already in
            # main equation collection
            # Is not optimal when velocity and momentum_density are calculated together,
            # but this is usually not the case
            momentum_density_output_symbols = output_quantity_names_to_symbols['momentum_density']
            mom_density_eq_coll = get_equations_for_zeroth_and_first_order_moment(self._stencil, pdfs,
                                                                                  self._symbolOrder0,
                                                                                  self._symbolsOrder1)
            mom_density_eq_coll = apply_force_model_shift('macroscopic_velocity_shift', dim, mom_density_eq_coll,
                                                          self._forceModel, self._compressible)
            for sym, val in zip(momentum_density_output_symbols, mom_density_eq_coll.main_assignments[1:]):
                main_assignments.append(Assignment(sym, val.rhs))
        if 'moment0' in output_quantity_names_to_symbols:
            moment0_output_symbol = output_quantity_names_to_symbols['moment0']
            if isinstance(moment0_output_symbol, Field):
                moment0_output_symbol = moment0_output_symbol.center
            main_assignments.append(Assignment(moment0_output_symbol, sum(pdfs)))
        if 'moment1' in output_quantity_names_to_symbols:
            moment1_output_symbol = output_quantity_names_to_symbols['moment1']
            if isinstance(moment1_output_symbol, Field):
                moment1_output_symbol = moment1_output_symbol.center_vector
            main_assignments.extend([Assignment(lhs, sum(d[i] * pdf for d, pdf in zip(self._stencil, pdfs)))
                                     for i, lhs in enumerate(moment1_output_symbol)])

        ac = ac.copy(main_assignments, [Assignment(a, b) for a, b in eqs.items()])
        return ac.new_without_unused_subexpressions()

    def __repr__(self):
        return "ConservedValueComputation for %s" % (", " .join(self.conserved_quantities.keys()),)


# -----------------------------------------  Helper functions ----------------------------------------------------------


def get_equations_for_zeroth_and_first_order_moment(stencil, symbolic_pdfs,
                                                    symbolic_zeroth_moment, symbolic_first_moments):
    r"""
    Returns an equation system that computes the zeroth and first order moments with the least amount of operations

    The first equation of the system is equivalent to

    .. math :

        \rho = \sum_{d \in S} f_d
        u_j = \sum_{d \in S} f_d u_jd

    Args:
        stencil: called :math:`S` above
        symbolic_pdfs: called :math:`f` above
        symbolic_zeroth_moment:  called :math:`\rho` above
        symbolic_first_moments: called :math:`u` above
    """
    def filter_out_plus_terms(expr):
        result = 0
        for term in expr.args:
            if not type(term) is sp.Mul:
                result += term
        return result

    dim = len(stencil[0])

    subexpressions = []
    pdf_sum = sum(symbolic_pdfs)
    u = [0] * dim
    for f, offset in zip(symbolic_pdfs, stencil):
        for i in range(dim):
            u[i] += f * int(offset[i])

    plus_terms = [set(filter_out_plus_terms(u_i).args) for u_i in u]
    for i in range(dim):
        rhs = plus_terms[i]
        for j in range(i):
            rhs -= plus_terms[j]
        eq = Assignment(sp.Symbol("vel%dTerm" % (i,)), sum(rhs))
        subexpressions.append(eq)

    for subexpression in subexpressions:
        pdf_sum = pdf_sum.subs(subexpression.rhs, subexpression.lhs)

    for i in range(dim):
        u[i] = u[i].subs(subexpressions[i].rhs, subexpressions[i].lhs)

    equations = []
    equations += [Assignment(symbolic_zeroth_moment, pdf_sum)]
    equations += [Assignment(u_i_sym, u_i) for u_i_sym, u_i in zip(symbolic_first_moments, u)]

    return AssignmentCollection(equations, subexpressions)


def divide_first_order_moments_by_rho(assignment_collection, dim):
    r"""
    Assumes that the equations of the passed equation collection are the following
        - rho = f_0  + f_1 + ...
        - u_0 = ...
        - u_1 = ...
    Returns a new equation collection where the u terms (first order moments) are divided by rho.
    The dim parameter specifies the number of first order moments. All subsequent equations are just copied over.
    """
    old_eqs = assignment_collection.main_assignments
    rho = old_eqs[0].lhs
    new_first_order_moment_eq = [Assignment(eq.lhs, eq.rhs / rho) for eq in old_eqs[1:dim + 1]]
    new_eqs = [old_eqs[0]] + new_first_order_moment_eq + old_eqs[dim + 1:]
    return assignment_collection.copy(new_eqs)


def add_density_offset(assignment_collection, offset=sp.Rational(1, 1)):
    r"""
    Assumes that first equation is the density (zeroth moment). Changes the density equations by adding offset to it.
    """
    old_eqs = assignment_collection.main_assignments
    new_density = Assignment(old_eqs[0].lhs, old_eqs[0].rhs + offset)
    return assignment_collection.copy([new_density] + old_eqs[1:])


def apply_force_model_shift(shift_member_name, dim, assignment_collection, force_model, compressible, reverse=False):
    """
    Modifies the first order moment equations in assignment collection according to the force model shift.
    It is applied if force model has a method named shift_member_name. The equations 1: dim+1 of the passed
    equation collection are assumed to be the velocity equations.
    """
    if force_model is not None and hasattr(force_model, shift_member_name):
        old_eqs = assignment_collection.main_assignments
        density = old_eqs[0].lhs if compressible else sp.Rational(1, 1)
        old_vel_eqs = old_eqs[1:dim + 1]
        shift_func = getattr(force_model, shift_member_name)
        vel_offsets = shift_func(density)
        if reverse:
            vel_offsets = [-v for v in vel_offsets]
        shifted_velocity_eqs = [Assignment(old_eq.lhs, old_eq.rhs + offset)
                                for old_eq, offset in zip(old_vel_eqs, vel_offsets)]
        new_eqs = [old_eqs[0]] + shifted_velocity_eqs + old_eqs[dim + 1:]
        return assignment_collection.copy(new_eqs)
    else:
        return assignment_collection
