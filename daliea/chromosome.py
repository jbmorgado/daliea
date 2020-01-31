# -*- coding: UTF-8 -*-
from gene import Gene
import numpy as np
from PIL import (Image, ImageChops, ImageDraw, ImageStat)
import copy

DELTA_FACTOR = 0.01  # Max delta factor for soft mutations
SIGMA_FACTOR = 0.01  # Sigma as factor of max dimensions for gaussian mutations


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
        self.generations = 0
        self.h_mutations = 0
        self.m_mutations = 0
        self.s_mutations = 0
        self.g_mutations = 0
        self.mutations = 0
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
        self.generations = 0
        self.h_mutations = 0
        self.m_mutations = 0
        self.s_mutations = 0
        self.g_mutations = 0
        self.mutations = 0
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

    def mutate(self, mutation, swap=False, n_mut=1):
        """Inplace mutate one gene according to type of mutation.

        Attributes
            mutation    Mutation type is one of the following:
                        - 'All': randomly choose one of the mutations
                        - 'Hard': change a color and transparency of one
                          polygon to a completely random value together with
                          changing one vertex to a completely random point
                          and perform swap.
                        - 'Medium': change one parameter to random number.
                        - 'Soft': change one parameter (R, G, B, A, X, Y) by
                          small delta.
                        - 'Gaussian': change one parameter by delta picked from
                           normal distribution around the current value.
            swap        Chromosome level mutation alowing gene shifting.
            n_mut       Number of mutations"""

        if mutation == 'All':
            mutation = np.random.choice(['Hard', 'Medium', 'Soft', 'Gaussian'])
            
        if mutation == 'Hard':
            self.h_mutations = self.h_mutations + 1
        elif mutation == 'Medium':
            self.m_mutations = self.m_mutations + 1
        elif mutation == 'Soft':
            self.s_mutations = self.s_mutations + 1
        elif mutation == 'Gaussian':
            self.g_mutations = self.g_mutations + 1
            
        for i in range(0, n_mut):
            gene_n = np.random.randint(self.n_genes)
            if swap is True:
                if mutation == 'Hard':
                    self.genes[gene_n].mutate(mutation)
                    self._swap_vertices(mutation, gene_n)

                swap_rand = np.random.rand()
                if swap_rand < 0.33:
                    if mutation == 'Medium':
                        self._swap_vertices(mutation, gene_n)
                        return
                    elif mutation == 'Soft':
                        self._swap_vertices(mutation, gene_n)
                        return
                    elif mutation == 'Gaussian':
                        self._swap_vertices(mutation, gene_n)
                        return
                else:
                    self.genes[gene_n].mutate(mutation)
            else:
                self.genes[gene_n].mutate(mutation)

    def _swap_vertices(self, mutation, gene_n1):
        """Inplace swap the place of two genes.

        Attributes
            mutation    Mutation type is one of the following:
                        - 'Hard': swap gene_n1 with random gene.
                        - 'Medium': swap gene_n1 with random gene.
                        - 'Soft': swap gene_n1 with nearby gene picked by a
                          small delta.
                        - 'Gaussian': swap gene_n1 with nearby gene picked by a
                          normal distribution around the current value.
            gene_n1     Gene to swap."""

        if mutation == 'Hard' or mutation == 'Medium':
            gene_n2 = np.random.randint(self.n_genes)  # choose 2nd rnd gene
        elif mutation == 'Soft':
            delta_max = np.int(self.n_genes * DELTA_FACTOR)
            delta = np.random.randint(low=-delta_max, high=delta_max+1)
            gene_n2 = gene_n1 + delta
            gene_n2 = np.maximum(0, np.minimum(gene_n2, self.n_genes-1))
        elif mutation == 'Gaussian':
            sigma = self.n_genes * SIGMA_FACTOR
            gene_n2 = np.int(np.round(np.random.normal(gene_n1, sigma)))
            gene_n2 = np.maximum(0, np.minimum(gene_n2, self.n_genes-1))

        gene1 = copy.copy(self.genes[gene_n1])
        gene2 = copy.copy(self.genes[gene_n2])

        self.genes[gene_n1] = gene2
        self.genes[gene_n2] = gene1
