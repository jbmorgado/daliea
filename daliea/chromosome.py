from gene import Gene
import numpy as np
from PIL import Image
from PIL import ImageChops
from PIL import ImageDraw


class Chromosome(object):
    """Define class to hold chromosome"""

    def __init__(self, size_x, size_y, n_vertices, cl_type, n_genes, target):
        """Initialize gene with all values at zero

        Attributes
            size_x      Maximum X coordinate (can't exceed the image)
            size_y      Maximum Y coordinate (can't exceed the image)
            n_vertices  The number of vertices per gene
            cl_type     Color type is one of the following:
                        - 'RGBA': RGB with transparency
                        - 'RGB': RGB simple
            n_genes     Number of genes per chromosome
            target      The image to evolve into"""

        self.size_x = size_x
        self.size_y = size_y
        self.n_vertices = n_vertices
        if cl_type == 'RGBA':
            self._cl_type = 'RGBA'
            self._n_colors = 4
        elif cl_type == 'RGB':
            self._cl_type = 'RGB'
            self._n_colors = 3
        else:
            raise ValueError("method __init__ @ Chromosome doesn't accept\
                                attribute %s" % cl_type)
        self.n_genes = n_genes

        self.genes = []
        for i in range(n_genes):
            gene = Gene(size_x, size_y, n_vertices, cl_type)
            self.genes.append(gene)
        self.phenotype = None
        self.make_phenoeetype()
        self.fitness = None  # the closer to 0 the better
        self.calc_fitness(target)

    def make_phenotype(self, color=(255, 255, 255, 255)):
        """Update phenotype atribute by rendering the image.

        Attributes
            color       Color tuple, defaults to all white."""
        canvas = Image.new('RGBA', (self.size_x, self.size_y), color)
        poly = Image.new('RGBA', (self.size_x, self.size_y))
        pdraw = ImageDraw.Draw(poly)
        for gene in self.genes:
            pdraw.polygon(gene.vertices, gene.color)
            canvas.paste(poly, mask=poly)
        self.phenotype = canvas
        del pdraw
        del poly
        del canvas

    def calc_fitness(self, target):
        """Update fitness atribute by comparing with the target image. The lower
        the number the better the fitness.

        Attributes
            target      Target image in PIL Image format."""
        img_diff = ImageChops.difference(target, self.phenotype)
        self.fitness = np.sum(list(img_diff.getdata()))

    def mutate(self, mutation):
        """Inplace mutate one gene according to type of mutation.

        Attributes
            mutation    Mutation type is one of the following:
                        - 'Hard': change a color and transparency of one
                          polygon to a completely random value together with
                          changing one vertex to a completely random point.
                        - 'Medium': change one parameter to random number.
                        - 'Soft': change one parameter (R, G, B, A, X, Y) by
                          small delta.
                        - 'Gaussian': change one parameter by delta picked from
                           normal distribution around the current value."""

        gene_n = np.random.randint(self.n_genes)
        self.genes(gene_n).mutate(mutation)
