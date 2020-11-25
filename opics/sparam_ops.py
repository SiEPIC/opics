""" Functions operating on s-parameter matrices
"""
from typing import Optional
import numpy as np
from numpy import ndarray


def connect_s(
    A: ndarray,
    k: int,
    B: Optional[ndarray],
    l: int,
    create_composite_matrix: bool = True,
) -> ndarray:
    """
    connect two n-port networks' s-matrices together.

    specifically, connect port `k` on network `A` to port `l` on network
    `B`. The resultant network has nports = (A.rank + B.rank-2). This
    function operates on, and returns s-matrices. The function
    :func:`connect` operates on :class:`Network` types.

    Parameters
    -----------
    A : :class:`numpy.ndarray`
            S-parameter matrix of `A`, shape is fxnxn
    k : int
            port index on `A` (port indices start from 0)
    B : :class:`numpy.ndarray`
            S-parameter matrix of `B`, shape is fxnxn
    l : int
            port index on `B`

    Returns
    -------
    C : :class:`numpy.ndarray`
        new S-parameter matrix


    Notes
    -------
    internally, this function creates a larger composite network
    and calls the  :func:`innerconnect_s` function. see that function for more
    details about the implementation

    See Also
    --------
        connect : operates on :class:`Network` types
        innerconnect_s : function which implements the connection
            connection algorithm


    """

    if create_composite_matrix:
        if k > A.shape[-1] - 1 or l > B.shape[-1] - 1:
            raise (ValueError("port indices are out of range"))

        nf = A.shape[0]  # num frequency points
        nA = A.shape[1]  # num ports on A
        nB = B.shape[1]  # num ports on B
        nC = nA + nB  # num ports on C

        # create composite matrix, appending each sub-matrix diagonally
        C = np.zeros((nf, nC, nC), dtype="complex")
        C[:, :nA, :nA] = A.copy()
        C[:, nA:, nA:] = B.copy()

        # call innerconnect_s() on composit matrix C
        return innerconnect_s(C, k, nA + l)
    else:
        # call innerconnect_s() on non-composit matrix A
        return innerconnect_s(A, k, l)


def innerconnect_s(A: ndarray, k: int, l: int) -> ndarray:
    """
    connect two ports of a single n-port network's s-matrix.

    Specifically, connect port `k` to port `l` on `A`. This results in
    a (n-2)-port network.  This     function operates on, and returns
    s-matrices. The function :func:`innerconnect` operates on
    :class:`Network` types.

    Parameters
    -----------
    A : :class:`numpy.ndarray`
        S-parameter matrix of `A`, shape is fxnxn
    k : int
        port index on `A` (port indices start from 0)
    l : int
        port index on `A`

    Returns
    -------
    C : :class:`numpy.ndarray`
            new S-parameter matrix

    Notes
    -----
    The algorithm used to calculate the resultant network is called a
    'sub-network growth',  can be found in [#]_. The original paper
    describing the  algorithm is given in [#]_.

    References
    ----------
    - Compton, R.C.; , "Perspectives in microwave circuit analysis,"
    Circuits and Systems, 1989.,
    Proceedings of the 32nd Midwest Symposium on , vol., no., pp.716-718 vol.2, 14-16
    Aug 1989.
    http://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=101955&isnumber=3167

    - Filipsson, Gunnar;
    "A New General Computer Algorithm for S-Matrix Calculation of Interconnected
    Multiports," Microwave Conference, 1981. 11th European , vol., no., pp.700-704,
    7-11 Sept. 1981.
    http://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=4131699&isnumber=4131585
    """

    if k > A.shape[-1] - 1 or l > A.shape[-1] - 1:
        raise (ValueError("port indices are out of range"))

    nA = A.shape[1]  # num of ports on input s-matrix

    # create an empty s-matrix, to store the result
    C = np.zeros(shape=A.shape, dtype="complex")

    # loop through ports and calulates resultant s-parameters
    for i in range(nA):
        for j in range(nA):
            C[:, i, j] = (
                A[:, i, j]
                * (A[:, l, l] * A[:, k, k] - (A[:, l, k] - 1) * (A[:, k, l] - 1))
                + A[:, k, j] * A[:, i, l] * (A[:, l, k] - 1)
                - A[:, k, j] * A[:, i, k] * A[:, l, l]
                - A[:, i, l] * A[:, l, j] * A[:, k, k]
                + A[:, l, j] * A[:, i, k] * (A[:, k, l] - 1)
            ) / (A[:, l, l] * A[:, k, k] - (A[:, l, k] - 1) * (A[:, k, l] - 1))

    # remove ports that were `connected`
    C = np.delete(C, (k, l), 1)
    C = np.delete(C, (k, l), 2)

    return C
