import numpy as np
DELTA_FACTOR = 0.01  # Max delta factor for soft mutations
SIGMA_FACTOR = 0.01  # Sigma as factor of max dimensions for gaussian mutations


class gene(object):
    """Define class to hold gene."""

    def __init__(self, n_vertices, cl_type, max_x, max_y):
        """Initialize gene with all values at zero

        Attributes
            n_vertices    The number of vertices per gene
            cl_type         Color type is one of the following:
                            - 'RGBA': RGB with transparency
                            - 'RGB': RGB simple
            max_x           Maximum X coordinate (can't exceed the image)
            max_y           Maximum Y coordinate (can't exceed the image)"""

        self.n_vertices = n_vertices
        if cl_type == 'RGBA':
            self.__cl_type = 'RGBA'
            self.__n_colors = 4
        elif cl_type == 'RGB':
            self.__cl_type = 'RGB'
            self.__n_colors = 3
        else:
            raise ValueError("method __init__ @ gene doesn't accept\
                             attribute %s" % cl_type)
        self.max_x = max_x
        self.max_y = max_y

        self.vertices = list(zip([0]*n_vertices, [0]*n_vertices))
        self.color = tuple([0]*self.__n_colors)

    def _make_rnd_color(self):
        """Return a random color composed of int from 0 to 255."""
        return(tuple(np.random.randint(256, size=self.__n_colors)))

    def _make_rnd_vertex(self):
        """Return a random vertex with maximum size of image."""
        return(tuple(np.random.randint(self.max_x),
                     np.random.randint(self.max_y)))

    def soft_mutate_color(self):
        """Inplace mutate one element of color by a small delta."""
        color = list(self.color)
        ele_n = np.random.randint(self.__n_colors)  # choose rnd element
        delta_max = np.rint(256 * DELTA_FACTOR)
        delta = np.random.randint(low=-delta_max, high=delta_max+1)
        color[ele_n] = color[ele_n] + delta
        # ensure it's between 0 to 255
        color[ele_n] = np.minimum(color[ele_n], 255)
        color[ele_n] = np.maximum(color[ele_n], 0)
        self.color = tuple(color)

    def soft_mutate_vertices(self):
        """Inplace mutate one element of one vertex by a small delta."""
        vertex_n = np.random.randint(self.n_vertices)  # choose rnd vertex
        vertex = list(self.vertices[vertex_n])
        coord_n = np.random.randint(2)  # choose X or Y coordinate
        if coord_n == 0:
            # X coordinate
            delta_max = np.rint(self.max_x * DELTA_FACTOR)
            delta = np.random.randint(low=-delta_max, high=delta_max+1)
            vertex[coord_n] = vertex[coord_n] + delta
            # ensure it's bellow  max_x
            vertex[coord_n] = np.minimum(vertex[coord_n], self.max_x)
        else:
            # Y coordinate
            delta_max = np.rint(self.max_y * DELTA_FACTOR)
            delta = np.random.randint(low=-delta_max, high=delta_max+1)
            vertex[coord_n] = vertex[coord_n] + delta
            # ensure it's bellow  max_y
            vertex[coord_n] = np.minimum(vertex[coord_n], self.max_y)

        # ensure it's above 0
        vertex[coord_n] = np.maximum(vertex[coord_n], 0)
        self.vertices[vertex_n] = tuple(vertex)

    def gaussian_mutate_color(self):
        """Inplace mutate one element of color by a normal distribution."""
        color = list(self.color)
        ele_n = np.random.randint(self.__n_colors)  # choose rnd element
        sigma = 256 * SIGMA_FACTOR
        color[ele_n] = np.random.normal(color[ele_n], sigma)
        # ensure it's between 0 to 255
        color[ele_n] = np.minimum(color[ele_n], 255)
        color[ele_n] = np.maximum(color[ele_n], 0)
        self.color = tuple(color)

    def gaussian_mutate_vertices(self):
        """Inplace mutate one element of one vertex by normal distribution."""
        vertex_n = np.random.randint(self.n_vertices)  # choose rnd vertex
        vertex = list(self.vertices[vertex_n])
        coord_n = np.random.randint(2)  # choose X or Y coordinate
        if coord_n == 0:
            # X coordinate
            sigma = self.max_x * SIGMA_FACTOR
            vertex[coord_n] = np.random.normal(vertex[coord_n], sigma)
            # ensure it's bellow  max_x
            vertex[coord_n] = np.minimum(vertex[coord_n], self.max_x)
        else:
            # Y coordinate
            sigma = self.max_y * SIGMA_FACTOR
            vertex[coord_n] = np.random.normal(vertex[coord_n], sigma)
            # ensure it's bellow  max_y
            vertex[coord_n] = np.minimum(vertex[coord_n], self.max_y)

        # ensure it's above 0
        vertex[coord_n] = np.maximum(vertex[coord_n], 0)
        self.vertices[vertex_n] = tuple(vertex)

    def mutate(self, mutation):
        """Mutates the gene according to type of mutation.

        Attributes
            mutation        Mutation type is one of the following:
                            - 'Hard': change a color and transparency of one
                                polygon to a completely random value together
                                with changing one vertex to a completely random
                                point.
                            - 'Medium': change one parameter to random number.
                            - 'Soft': change one parameter (R, G, B, A, X, Y)
                                by small delta.
                            - 'Gaussian': change one parameter by delta picked
                                from normal distribution of values around the
                                current value."""

        if mutation == 'Hard':
            self.color = self._make_rnd_color()
            vertex = np.random.randint(self.n_vertices)
            self.vertices[vertex] = self._make_rnd_vertex()
        elif mutation == 'Medium':
            if np.random.choice(['Color', 'Vertex']) == 'Color':
                self.color = self._make_rnd_color()
            else:
                rnd_vertex = np.random.randint(self.n_vertices)
                self.vertices[rnd_vertex] = self._make_rnd_vertex()
        elif mutation == 'Soft':
            cl_factor = self.__n_colors/(self.__n_colors+self.n_vertices*2)
            if np.random.random() < cl_factor:
                self.soft_mutate_color()
            else:
                self.soft_mutate_vertices
        elif mutation == 'Gaussian':
            cl_factor = self.__n_colors/(self.__n_colors+self.n_vertices*2)
            if np.random.random() < cl_factor:
                self.gaussian_mutate_color()
            else:
                self.gaussian_mutate_vertices
        else:
            raise ValueError("method mutate @ gene doesn't accept\
                             attribute %s" % mutation)
