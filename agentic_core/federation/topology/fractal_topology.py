class FractalTopology:
    @staticmethod
    def fractal_service_mesh(b, d): return [(0, b)] + [(1, b/1.44)]*3 if d>0 else [(0, b)]
