import numpy as np
from matplotlib.figure import Figure

def generate_mesh(start: float, end: float, num_elements: int) -> np.ndarray:
    """
    Creates mesh nodes in the interval [start, end] divided into num_elements elements.
    Returns node vector x of size (num_elements + 1).
    """
    return np.linspace(start, end, num_elements + 1)

def get_quadrature_data() -> tuple[np.ndarray, np.ndarray]:
    """
    Returns points and weights for 2-point Gauss-Legendre quadrature
    on the reference interval [-1, 1].
    """
    points = np.array([-1.0 / np.sqrt(3), 1.0 / np.sqrt(3)])
    weights = np.array([1.0, 1.0])
    return points, weights

def calculate_shape_functions(xi: float) -> tuple[np.ndarray, np.ndarray]:
    """
    Calculates shape functions and their derivatives at point xi.
    """
    shape_functions = np.array([0.5 * (1 - xi), 0.5 * (1 + xi)])
    derivatives = np.array([-0.5, 0.5])
    return shape_functions, derivatives

def compute_element_matrix_entry(dN_dx_i: float, dN_dx_j: float, 
                                 N_i: float, N_j: float, 
                                 weight: float, jacobian: float) -> float:
    """
    Computes single entry of local element matrix Ae.
    """
    return (dN_dx_i * dN_dx_j - N_i * N_j) * weight * jacobian

def compute_element_vector_entry(N_i: float, x: float, 
                                 weight: float, jacobian: float) -> float:
    """
    Computes single entry of local element vector Fe.
    """
    return (np.sin(x) + 2) * N_i * weight * jacobian

def compute_element_matrices(x_left: float, x_right: float, 
                           quad_points: np.ndarray, 
                           quad_weights: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """
    Computes local matrices for given element.
    """
    element_length = x_right - x_left
    jacobian = 0.5 * element_length
    local_matrix = np.zeros((2, 2))
    local_vector = np.zeros(2)

    for point, weight in zip(quad_points, quad_weights):
        x_physical = 0.5 * (x_right + x_left + element_length * point)
        shape_functions, dN_dxi = calculate_shape_functions(point)
        dN_dx = dN_dxi / jacobian

        for i in range(2):
            for j in range(2):
                local_matrix[i, j] += compute_element_matrix_entry(
                    dN_dx[i], dN_dx[j], 
                    shape_functions[i], shape_functions[j], 
                    weight, jacobian
                )
            local_vector[i] += compute_element_vector_entry(
                shape_functions[i], x_physical, weight, jacobian
            )

    return local_matrix, local_vector

def apply_boundary_conditions(matrix: np.ndarray, vector: np.ndarray) -> None:
    """
    Applies boundary conditions to global matrix A and vector F.
    """
    matrix[0, :] = 0.0
    matrix[0, 0] = 1.0
    vector[0] = -2.0
    vector[-1] += 6.0

def assemble_global_system(nodes: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """
    Assembles global system matrices based on local element matrices.
    """
    num_nodes = len(nodes)
    global_matrix = np.zeros((num_nodes, num_nodes))
    global_vector = np.zeros(num_nodes)
    quad_points, quad_weights = get_quadrature_data()

    for elem_idx in range(num_nodes - 1):
        x_left, x_right = nodes[elem_idx:elem_idx + 2]
        local_matrix, local_vector = compute_element_matrices(
            x_left, x_right, quad_points, quad_weights
        )

        for i in range(2):
            global_i = elem_idx + i
            global_vector[global_i] += local_vector[i]
            for j in range(2):
                global_j = elem_idx + j
                global_matrix[global_i, global_j] += local_matrix[i, j]

    apply_boundary_conditions(global_matrix, global_vector)
    return global_matrix, global_vector

def galerkin_method(interval: tuple[float, float], 
                  num_elements: int = 8) -> tuple[np.ndarray, np.ndarray]:
    """
    Solves the problem using Galerkin method.
    Returns nodes and corresponding function values.
    """
    nodes = generate_mesh(interval[0], interval[1], num_elements)
    matrix, vector = assemble_global_system(nodes)
    solution = np.linalg.solve(matrix, vector)
    return nodes, solution

def create_plot(x_values: np.ndarray, 
                        u_values: np.ndarray) -> Figure:
    """
    Creates a plot of the numerical solution.
    """
    fig = Figure(figsize=(8, 6), dpi=100)
    ax = fig.add_subplot(111)
    ax.plot(x_values, u_values, 'bo-', label='Numerical solution')
    ax.set_xlabel('x')
    ax.set_ylabel('u(x)')
    ax.set_title('Numerical solution of the equation')
    ax.legend()
    ax.grid(True)
    return fig