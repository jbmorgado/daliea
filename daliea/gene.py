import numpy as np

DELTA_FACTOR = 0.01  # Max delta factor for soft mutations
SIGMA_FACTOR = 0.01  # Sigma as factor of max dimensions for gaussian mutations


class Gene(object):
    """Define class to hold gene"""

    def __init__(self, size_x, size_y, n_vertices):
        """Initialize gene with all values at zero

        Attributes
            size_x          Maximum X coordinate (can't exceed the image)
            size_y          Maximum Y coordinate (can't exceed the image)
            n_vertices      The number of vertices per gene"""

        self.size_x = size_x
        self.size_y = size_y
        self.n_vertices = n_vertices

        self.vertices = list(zip(np.random.randint(size_x, size=n_vertices),
                                 np.random.randint(size_y, size=n_vertices)))
        rgba = [np.random.randint(256, size=3), [0]]
        self.color = tuple(np.concatenate(rgba, axis=0))

    def _make_rnd_color(self):
        """Return a random color composed of int from 0 to 255."""
        rgba = [np.random.randint(256, size=3),
                np.random.randint(20, 120, size=1)]
        return(tuple(np.concatenate(rgba, axis=0)))

    def _make_rnd_vertex(self):
        """Return a random vertex tuple with maximum size of image."""
        return((np.random.randint(self.size_x),
                np.random.randint(self.size_y)))

    def soft_mutate_color(self):
        """Inplace mutate one element of color by a small delta."""
        color = list(self.color)
        ele_n = np.random.randint(4)  # choose rnd element
        delta_max = np.int(np.rint(256 * DELTA_FACTOR))
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
            # delta_max = np.int(np.rint(self.size_x * DELTA_FACTOR))
            delta_max = np.int(np.round(self.size_x * DELTA_FACTOR))
            delta = np.random.randint(low=-delta_max, high=delta_max+1)
            vertex[coord_n] = vertex[coord_n] + delta
            # ensure it's bellow  size_x
            vertex[coord_n] = np.minimum(vertex[coord_n], self.size_x-1)
        else:
            # Y coordinate
            # delta_max = np.int(np.rint(self.size_y * DELTA_FACTOR))
            delta_max = np.int(np.round(self.size_y * DELTA_FACTOR))
            delta = np.random.randint(low=-delta_max, high=delta_max+1)
            vertex[coord_n] = vertex[coord_n] + delta
            # ensure it's bellow  size_y
            vertex[coord_n] = np.minimum(vertex[coord_n], self.size_y-1)

        # ensure it's above 0
        vertex[coord_n] = np.maximum(vertex[coord_n], 0)
        self.vertices[vertex_n] = tuple(vertex)

    def gaussian_mutate_color(self):
        """Inplace mutate one element of color by a normal distribution."""
        color = list(self.color)
        ele_n = np.random.randint(4)  # choose rnd element
        sigma = 256 * SIGMA_FACTOR
        color[ele_n] = np.int(np.round(np.random.normal(color[ele_n], sigma)))
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
            sigma = self.size_x * SIGMA_FACTOR
            vertex[coord_n] = np.int(np.round(np.random.normal(vertex[coord_n],
                                                               sigma)))
            # ensure it's bellow  size_x
            vertex[coord_n] = np.minimum(vertex[coord_n], self.size_x-1)
        else:
            # Y coordinate
            sigma = self.size_y * SIGMA_FACTOR
            vertex[coord_n] = np.int(np.round(np.random.normal(vertex[coord_n],
                                                               sigma)))
            # ensure it's bellow  size_y
            vertex[coord_n] = np.minimum(vertex[coord_n], self.size_y-1)

        # ensure it's above 0
        vertex[coord_n] = np.maximum(vertex[coord_n], 0)
        self.vertices[vertex_n] = tuple(vertex)

    def mutate(self, mutation):
        """Inplace mutate the gene according to type of mutation.

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

        if mutation != 'Hard':
            target = np.random.choice(['Color', 'Vertex'])
            if mutation == 'Medium':
                if target == 'Color':
                    self.color = self._make_rnd_color()
                else:
                    vertex_n = np.random.randint(self.n_vertices)
                    self.vertices[vertex_n] = self._make_rnd_vertex()
            elif mutation == 'Soft':
                if target == 'Color':
                    self.soft_mutate_color()
                else:
                    self.soft_mutate_vertices()
            elif mutation == 'Gaussian':
                if target == 'Color':
                    self.gaussian_mutate_color()
                else:
                    self.gaussian_mutate_vertices()
        elif mutation == 'Hard':
            self.color = self._make_rnd_color()
            for i in range(0, 2):
                vertex = np.random.randint(self.n_vertices)
                self.vertices[vertex] = self._make_rnd_vertex()
        else:
            raise ValueError("method mutate @ gene doesn't accept\
                             attribute %s" % mutation)
