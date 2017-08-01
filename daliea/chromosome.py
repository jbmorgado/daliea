# -*- coding: UTF-8 -*-
from gene import Gene
import numpy as np
from PIL import (Image, ImageChops, ImageDraw, ImageStat)


class Chromosome(object):
    """Define class to hold chromosome"""

    def __init__(self):
        """Initialize chromosome bare"""

        self.size_x = None
        self.size_y = None
        self.n_vertices = None
        self.n_genes = None
        self.genes = []
        self.phenotype = None
        self.fitness = None  # the closer to 0 the better
        self.mutations = 0
        self.improvements = 0
        self.evolution_time = 0

    def setup(self, size_x, size_y, n_vertices, n_genes):
        """Setup  chromosome with all values at zero

        Attributes
            size_x      Maximum X coordinate (can't exceed the image)
            size_y      Maximum Y coordinate (can't exceed the image)
            n_vertices  The number of vertices per gene
            n_genes     Number of genes per chromosome"""

        self.size_x = size_x
        self.size_y = size_y
        self.n_vertices = n_vertices
        self.n_genes = n_genes

        self.genes = []
        for i in range(n_genes):
            gene = Gene(size_x, size_y, n_vertices)
            self.genes.append(gene)
        self.phenotype = None
        self.make_phenotype()
        self.fitness = None  # the closer to 0 the better
        self.fitness_p = None  # the closer to 100 the better
        self.max_handicap = size_x * size_y * 3 * 256
        self.mutations = 0
        self.improvements = 0
        self.neutrals = 0

    def make_phenotype(self, color=(255, 255, 255, 255)):
        """Update phenotype atribute by rendering the image.

        Attributes
            color       Color tuple, defaults to all white."""
        canvas = Image.new('RGBA', (self.size_x, self.size_y), color)
        poly = Image.new('RGBA', (self.size_x, self.size_y))
        pdraw = ImageDraw.Draw(poly)
        for gene in self.genes:
            # if fully transparent, don't render it
            if gene.color[3] != 0:
                pdraw.polygon(gene.vertices, gene.color)
                canvas.paste(poly, mask=poly)
        self.phenotype = canvas.convert("RGB")
        del pdraw
        del poly
        del canvas

    def calc_fitness(self, target):
        """Update fitness atribute by comparing with the target image. The lower
        the number the better the fitness.

        Attributes
            target      Target image in PIL Image format."""
        img1 = target
        img2 = self.phenotype
        handicap = ImageChops.difference(img1, img2)
        img_stats = ImageStat.Stat(handicap)
        self.fitness = np.sum(img_stats.sum)
        self.fitness_p = 100. * (1. - (self.fitness/self.max_handicap))

    def mutate(self, mutation, n_mut=1):
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
                           normal distribution around the current value.
            n_mut       Number of mutations"""

        for i in range(0, n_mut):
            gene_n = np.random.randint(self.n_genes)
            self.genes[gene_n].mutate(mutation)
