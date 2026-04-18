class ClimateDomainAdapter:
    def __init__(self, o=None): pass
    async def optimise_carbon_trajectory(self, e, r): return [x*(1-r) for x in e]
