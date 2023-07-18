def risk_index(risk_level):
    # risk levels range from 0.0 to 1.0,
    # but we want eleven bins, with bins for 0 - 0.05 and 0.95 - 1.0,
    # since risk = 0, 0.5, and 1 are all special cases we want clearly captured.

    # if we think of it as a range from -0.05 to 1.05,
    # then we can work with evenly sized 0.1 bins
    minval = -0.05
    binwidth = 0.1
    nbins = 11

    # Determine which bin this element belongs in
    binnum = int((risk_level - minval) // binwidth)  # // = floor division
    # convert bin number to 0-based index
    return min(nbins - 1, binnum)


def agent_portrayal(agent):
    import math
    from simulatingrisk.risky_bet.model import divergent_colors

    # initial display
    portrayal = {
        "Shape": "circle",
        "Color": "gray",
        "Filled": "true",
        "Layer": 0,
        "r": 0.5,
    }

    # color based on risk level, with ten bins
    # convert 0.0 to 1.0 to 1 - 10
    color_index = math.floor(agent.risk_level * 10)
    portrayal["Color"] = divergent_colors[color_index]

    # size based on wealth within current distribution
    max_wealth = agent.model.max_agent_wealth
    wealth_index = math.floor(agent.wealth / max_wealth * 10)
    # set radius based on wealth, but don't go smaller than 0.1 radius
    # or too large to fit in the grid
    portrayal["r"] = wealth_index / 15 + 0.1

    # TODO: change shape based on number of times risk level has been adjusted?
    # can't find a list of available shapes; setting to triangle and square
    # results in a 404 for a local custom url

    return portrayal
